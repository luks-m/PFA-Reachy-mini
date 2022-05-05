# from click import launch
# from reachy_sdk import ReachySDK
from math import sqrt
import time
import cv2
import dlib
# from turtle import right
from cv2 import aruco
import sys
sys.path.append("../session")


# Defining the face and ArUco detedtors
Face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
MARKER_DIC = aruco.Dictionary_get(aruco.DICT_4X4_50)
PARAM_MMARKERS = aruco.DetectorParameters_create()
DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor("../../assets/vision/shape_predictor_68_face_landmarks.dat")


# Useful classes
class Pos:      # Represent a face square upper left position
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Scale:    # Represent a face dimensions, or a vector coordinates
    def __init__(self, w, h):
        self.width = w
        self.height = h

class Angle:   # Represent both angle values (resp. for the horizontal angle and the vertical one)
    def __init__(self, horizontal, vertical):
        self.h = horizontal
        self.v = vertical

class Face:     # Represent a face square, with its position and dimensions
    def __init__(self, x, y, w, h):
        self.pos = Pos(x, y)
        self.scale = Scale(w, h)

class Face_and_value:   # Represent a face square extended with a value
    def __init__(self, face, value):
        self.face = face
        self.value = value

# Mathematical transformations
def give_face_center(face): # Given a face square object, gice the square center
    return Pos(face.pos.x + face.scale.width/2, face.pos.y + face.scale.height/2)

def vector_center_to_pos(frame_center_pos, pos):    # Give the vector from the center to the given position
    return Scale(pos.x - frame_center_pos.x, frame_center_pos.y - pos.y)

def vector_center_to_face(frame_center_pos, face):  # Give the vector from the frame_center to the face center
    center_pos = give_face_center(face)
    return vector_center_to_pos(frame_center_pos, center_pos)

def vector_magnitude(pos):  # Give the vector euclidian's magnitude
    return sqrt((pos.x)**2 + (pos.y)**2)

def scale_to_angle(dist):   # A transformation to translate pixel distance in angle
    return dist / 150 * 20

# Array management
def faces_to_faces_and_values(faces):   # Conversion from a face table to a face_and_value table
    faces_and_values = []
    for face in faces:
        faces_and_values.append(Face_and_value(face, 0))
    return faces_and_values

def faces_and_values_to_faces(faces_and_values):    # Conversion from a face face_and_value table to a face table
    faces = []
    for face_and_value in faces_and_values:
        faces.append(face_and_value.face)
    return faces

def face_and_value_decreasing_buble_sort(faces_and_values): # A buble sort based on the values into a face_and_value table, giving a decreasing order
    if(len(faces_and_values) < 2):
        return faces_and_values
    has_switched = True
    while has_switched:
        has_switched = False
        for i in range(len(faces_and_values) - 1):
            if faces_and_values[i].value < faces_and_values[i+1].value:
                has_switched = True
                faces_and_values[i], faces_and_values[i+1] = faces_and_values[i+1], faces_and_values[i]
    return faces_and_values

def get_average_position(faces):   # Give the face center average position for a face table
    x, y, n = 0, 0, len(faces)
    for face in faces:
        cent_pos = give_face_center(face)
        x += cent_pos.x; y += cent_pos.y
    x /= n; y /= n
    return Pos(x, y)

def extract_index_nparray(nparray):     # Useful extration for face swapping
    index = None
    for num in nparray[0]:
        index = num
        break
    return index

# Subfunctions for interfaces functions
def get_n_closest_faces(faces, n):  # Give the n closest faces unsing the face height as distance approximation
    faces_and_values = faces_to_faces_and_values(faces)
    for face_and_val in faces_and_values:
        face_and_val.value = face_and_val.face.scale.height     # Height is an approximation of distances, despite of the different face dimensions
    faces_and_values = face_and_value_decreasing_buble_sort(faces_and_values)
    return faces_and_values_to_faces(faces_and_values[:n])

def get_closest_to_mean_faces(faces, percent_relat_to_avg): # Give the faces whose the height is 'percent_relat_to_avg' or less near from the height average
    s, n = 0, len(faces)
    if n == 0 :
        return []
    # Mean face height computation
    for face in faces:
        s += face.scale.height
    avg_size = s/n
    kept_faces = []
    # Adding only faces having a distance between height and height average of at most percent_relat_to_avg
    for face in faces:
        if abs(face.scale.height - avg_size) <= (percent_relat_to_avg * avg_size):
            kept_faces.append(face)
    return kept_faces

def global_face_detection_service(frame, specific_getter_function, specific_getter_param, for_test):    # A code factorization function for interface functions, using multiple services defined in this file
    frame = give_in_gray(frame)
    faces = get_faces(frame)
    faces = specific_getter_function(faces, specific_getter_param)
    if len(faces) == 0 :
        return Angle(0, 0)
    if for_test:
        for i in range(len(faces)):
            face = faces[i]
            draw_rectangle_on_frame(frame, face)
        # frame_display(frame, 'face_detection')
    mean_faces_pos = get_average_position(faces)
    scale = vector_center_to_pos(Pos(frame.shape[1]/2, frame.shape[0]/2), mean_faces_pos)
    return Angle(scale_to_angle(scale.width), scale_to_angle(scale.height))

def swap_two_faces(frame):  # If the given frame contain at least two faces, swap two faces (the first and second accordingly to the detector)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width, channels = frame.shape
    img2_new_face = np.zeros((height, width, channels), np.uint8)

    faces = DETECTOR(img_gray)
#
    faces_and_values = faces_to_faces_and_values(faces)
    for face_and_val in faces_and_values:
        print(face_and_val.face)
        face_and_val.value = face_and_val.face.h     # Height is an approximation of distances, despite of the different face dimensions
    faces_and_values = face_and_value_decreasing_buble_sort(faces_and_values)
    faces = faces_and_values_to_faces(faces_and_values)
#
    if len(faces) >= 2 :
        face_1 = faces[0]
        face_2 = faces[1]
    else :
        return frame, False

    # Face 1
    landmarks = PREDICTOR(img_gray, face_1)
    landmarks_points = []
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        landmarks_points.append((x, y))

    points = np.array(landmarks_points, np.int32)
    convexhull = cv2.convexHull(points)

    # Face 2
    landmarks = PREDICTOR(img_gray, face_2)
    landmarks_points2 = []
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        landmarks_points2.append((x, y))

    points2 = np.array(landmarks_points2, np.int32)
    convexhull2 = cv2.convexHull(points2)

    # Delaunay triangulation
    rect = cv2.boundingRect(convexhull)
    subdiv = cv2.Subdiv2D(rect)
    subdiv.insert(landmarks_points)
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)

    indexes_triangles = []
    for t in triangles:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        index_pt1 = np.where((points == pt1).all(axis=1))
        index_pt1 = extract_index_nparray(index_pt1)

        index_pt2 = np.where((points == pt2).all(axis=1))
        index_pt2 = extract_index_nparray(index_pt2)

        index_pt3 = np.where((points == pt3).all(axis=1))
        index_pt3 = extract_index_nparray(index_pt3)

        if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
            triangle = [index_pt1, index_pt2, index_pt3]
            indexes_triangles.append(triangle)

    # Triangulation of both faces
    for triangle_index in indexes_triangles:
        # Triangulation of the first face
        tr1_pt1 = landmarks_points[triangle_index[0]]
        tr1_pt2 = landmarks_points[triangle_index[1]]
        tr1_pt3 = landmarks_points[triangle_index[2]]
        triangle1 = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

        rect1 = cv2.boundingRect(triangle1)
        (x, y, w, h) = rect1
        cropped_triangle = frame[y: y + h, x: x + w]
        cropped_tr1_mask = np.zeros((h, w), np.uint8)

        points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
                           [tr1_pt2[0] - x, tr1_pt2[1] - y],
                           [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

        cv2.fillConvexPoly(cropped_tr1_mask, points, 255)

        # Triangulation of second face
        tr2_pt1 = landmarks_points2[triangle_index[0]]
        tr2_pt2 = landmarks_points2[triangle_index[1]]
        tr2_pt3 = landmarks_points2[triangle_index[2]]
        triangle2 = np.array([tr2_pt1, tr2_pt2, tr2_pt3], np.int32)

        rect2 = cv2.boundingRect(triangle2)
        (x2, y2, w2, h2) = rect2
        cropped_triangle2 = frame[y2: y2 + h2, x2: x2 + w2]
        cropped_tr2_mask = np.zeros((h2, w2), np.uint8)

        points2 = np.array([[tr2_pt1[0] - x2, tr2_pt1[1] - y2],
                            [tr2_pt2[0] - x2, tr2_pt2[1] - y2],
                            [tr2_pt3[0] - x2, tr2_pt3[1] - y2]], np.int32)

        cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)

        # Warp triangles
        points = np.float32(points)
        points2 = np.float32(points2)
        M = cv2.getAffineTransform(points, points2)
        M2 = cv2.getAffineTransform(points2, points)

        warped_triangle = cv2.warpAffine(cropped_triangle, M, (w2, h2))
        warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_tr2_mask)
        warped_triangle2 = cv2.warpAffine(cropped_triangle2, M2, (w, h))
        warped_triangle2 = cv2.bitwise_and(warped_triangle2, warped_triangle2, mask=cropped_tr1_mask)

        # Reconstructing destination face
        img2_new_face_rect_area = img2_new_face[y: y + h, x: x + w]
        img2_new_face_rect_area2 = img2_new_face[y2: y2 + h2, x2: x2 + w2]

        img2_new_face_rect_area_gray = cv2.cvtColor(img2_new_face_rect_area, cv2.COLOR_BGR2GRAY)
        img2_new_face_rect_area_gray2 = cv2.cvtColor(img2_new_face_rect_area2, cv2.COLOR_BGR2GRAY)

        _, mask_triangles_designed = cv2.threshold(img2_new_face_rect_area_gray, 1, 255, cv2.THRESH_BINARY_INV)
        _, mask_triangles_designed2 = cv2.threshold(img2_new_face_rect_area_gray2, 1, 255, cv2.THRESH_BINARY_INV)

        warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=mask_triangles_designed2)
        warped_triangle2 = cv2.bitwise_and(warped_triangle2, warped_triangle2, mask=mask_triangles_designed)

        img2_new_face_rect_area = cv2.add(img2_new_face_rect_area, warped_triangle2)
        img2_new_face_rect_area2 = cv2.add(img2_new_face_rect_area2, warped_triangle)

        img2_new_face[y: y + h, x: x + w] = img2_new_face_rect_area
        img2_new_face[y2: y2 + h2, x2: x2 + w2] = img2_new_face_rect_area2

    # Face swapped (putting 1st face into 2nd face)
    img2_face_mask = np.zeros_like(img_gray)
    img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull2, 255)
    img2_face_mask = cv2.bitwise_not(img2_head_mask)
    img2_face_mask2 = np.zeros_like(img_gray)
    img2_head_mask2 = cv2.fillConvexPoly(img2_face_mask2, convexhull, 255)
    img2_face_mask2 = cv2.bitwise_not(img2_head_mask2)


    img2_head_noface = cv2.bitwise_and(frame, frame, mask=img2_face_mask)
    img2_head_noface = cv2.bitwise_and(img2_head_noface, img2_head_noface, mask=img2_face_mask2)

    result = cv2.add(img2_head_noface, img2_new_face)

    (x, y, w, h) = cv2.boundingRect(convexhull2)
    center_face = (int((x + x + w) / 2), int((y + y + h) / 2))
    (x2, y2, w2, h2) = cv2.boundingRect(convexhull)
    center_face2 = (int((x2 + x2 + w2) / 2), int((y2 + y2 + h2) / 2))

    seamlessclone = cv2.seamlessClone(result, frame, img2_head_mask, center_face, cv2.NORMAL_CLONE)
    seamlessclone = cv2.seamlessClone(result, seamlessclone, img2_head_mask2, center_face2, cv2.NORMAL_CLONE)

    return seamlessclone, True

# Capture and camera functionalities
def open_capture(index):  # index is typed int
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    return cap

def free_capture_and_windows(cap):  # Free all windows and release the given capture
    cap.release()
    cv2.destroyAllWindows()

def read_capture(cap):  # Give the current frame reading the given capture
    return cap.read()

def give_in_gray(frame):    # Give the given frame colored in gray
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def face_detection_haar_cascade(frame): # A face detection using the Haar cascade method
    return Face_detector.detectMultiScale(frame, 
                                          scaleFactor=1.1,
                                          minNeighbors=4,
                                          minSize=(60, 60),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

def get_faces(frame):   # Translate the faces detected into a face class table
    recognised = face_detection_haar_cascade(frame)
    faces = []
    for (x, y, w, h) in recognised:
        faces.append(Face(x, y, w, h))
    return faces

def draw_rectangle_on_frame(frame, face):   # Draw a rectangle matching with the given face on the frame
    cv2.rectangle(frame, (face.pos.x, face.pos.y), (face.pos.x + face.scale.width, face.pos.y + face.scale.height), (255, 0, 0), 2)

def frame_display(frame, window_name):
    cv2.imshow(window_name, frame)

def get_aruco_code(frame):  # Give the aruco code associated to an aruco pattern if on the given frame
    grey_frame = give_in_gray(frame)
    bbox, ids, r = aruco.detectMarkers(grey_frame, MARKER_DIC, parameters=PARAM_MMARKERS)
    if not bbox:
        return None
    return ids[0][0]

def get_frame(session):     # An interface function to deal with the session interface
    return session.get_frame()

# Interface functions
def n_closest_angle(frame, n, for_test = False): # Give the average angle for the n closest faces using get_n_closest_face
    return global_face_detection_service(frame, get_n_closest_faces, n, for_test)

def framing_for_group_photo_angle(frame, percent_relat_to_avg, for_test = False): # Give the average angle for the faces whose the height is 'percent_relat_to_avg' or less near from the height average, using get_mean_distant_faces
    return global_face_detection_service(frame, get_closest_to_mean_faces, percent_relat_to_avg, for_test)

def smart_give_angle(session, nbr_trials, give_angle_function, give_angle_parameter, for_test = False):  # Give the angle, taking face detection hazard into account (no faces detected, non face object detected) to avoid errors whenever possible
    angle_table = []
    avg_angle = Angle(0, 0)
    
    for i in range(nbr_trials) :   # Angles to analyse, taking only non null angles into account (==> no faces detected not taken into account)
        angle = give_angle_function(get_frame(session), give_angle_parameter, for_test)
        if not(angle.h == 0 and angle.v == 0) :
            avg_angle.h += angle.h
            avg_angle.v += angle.v
            angle_table.append(angle)

    if len(angle_table) == 0 :  # Failure to found a face
        return Angle(0, 0)

    avg_angle.h /= len(angle_table)
    avg_angle.v /= len(angle_table)
    dist = vector_magnitude(Pos(angle_table[0].h - avg_angle.h, angle_table[0].v - avg_angle.v))
    nearest_angle = angle_table[0]
    for angle in angle_table :  # Searching for the nearest angle to the average one (it is supposed faces are detected more times than non face objects ==> true face is the nearest from the average location)
        new_dist = vector_magnitude(Pos(angle.h - avg_angle.h, angle.v - avg_angle.v))
        if new_dist < dist :
            dist = new_dist
            nearest_angle = angle
    nearest_angle.v *= -1
    nearest_angle.h *= -1
    return nearest_angle   

def take_picture(session, noun): # Take a picture, with an automatic focus, and save it at the 'path' location
   time.sleep(2)
   cv2.imwrite("../../tmp/img/" + noun + ".png", get_frame(session))

def take_swapped_faces_picture(session, noun, nbr_trials): # Take a picture, swapping two faces
    for i in range(max(nbr_trials, 1)):
        frame, res = swap_two_faces(get_frame(session))
        if res :
            break
    cv2.imwrite("../../tmp/" + noun + ".png", frame)

def smart_get_aruco_code(session, nbr_trials): # Search an aruco pattern on nbr_trials frames and return the associated code if a pattern is detected, None otherwise
    for i in range(nbr_trials):
        id = get_aruco_code(get_frame(session))
        if id != None :
            return id
    return None