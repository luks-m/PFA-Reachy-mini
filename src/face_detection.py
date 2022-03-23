# from click import launch
# from reachy_sdk import ReachySDK
from math import sqrt
import time
import cv2
# from turtle import right
from cv2 import aruco


# Defining the face and ArUco detedtors
Face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
MARKER_DIC = aruco.Dictionary_get(aruco.DICT_4X4_50)
PARAM_MMARKERS = aruco.DetectorParameters_create()


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

# class Reachy_camera:
#     def __init__(self, session):
#         self.session = session
#     def launch_focus(self): # Launch an automatic zoom during 2 seconds
#         self.session.start_autofocus()
#     def get_frame(self):
#         return self.session.get_frame()
#     def take_picture(self, noun): # Take a picture, with an automatic focus, and save it at the 'path' location
#        self.launch_focus()
#        cv2.imwrite("./tmp/" + noun + ".png", self.get_frame())
#     def smart_get_aruco_code(self, nbr_trials):
#         for i in range(nbr_trials):
#             id = get_aruco_code(self.get_frame())
#             if id != None :
#                 return id
#         return None


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

def get_n_closest_faces(faces, n):  # Give the n closest faces unsing the face height as distance approximation
    faces_and_values = faces_to_faces_and_values(faces)
    for face_and_val in faces_and_values:
        face_and_val.value = face_and_val.face.scale.height     # Height is an approximation of distances, despite of the different face dimensions
    faces_and_values = face_and_value_decreasing_buble_sort(faces_and_values)
    return faces_and_values_to_faces(faces_and_values[:n])

def get_closest_to_mean_faces(faces, percent_relat_to_avg): # Give the faces whose the height is 'percent_relat_to_avg' or less near from the height average
    s, n = 0, len(faces)
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
    if for_test:
        for i in range(len(faces)):
            face = faces[i]
            draw_rectangle_on_frame(frame, face)
        frame_display(frame, 'face_detection')
    if len(faces) == 0 :
        return Angle(0, 0)
    mean_faces_pos = get_average_position(faces)
    scale = vector_center_to_pos(Pos(frame.shape[1]/2, frame.shape[0]/2), mean_faces_pos)
    return Angle(scale_to_angle(scale.width), scale_to_angle(scale.height))


# Capture and camera functionalities
def open_capture(index):  # index is typed int
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    return cap

def free_capture_and_windows(cap):
    cap.release()
    cv2.destroyAllWindows()

def read_capture(cap):
    return cap.read()

def give_in_gray(frame):
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

def draw_rectangle_on_frame(frame, face):
    cv2.rectangle(frame, (face.pos.x, face.pos.y), (face.pos.x + face.scale.width, face.pos.y + face.scale.height), (255, 0, 0), 2)

def frame_display(frame, window_name):
    cv2.imshow(window_name, frame)

def get_aruco_code(frame):
    grey_frame = give_in_gray(frame)
    bbox, ids, r = aruco.detectMarkers(grey_frame, MARKER_DIC, parameters=PARAM_MMARKERS)
    if len(ids) == 0:
        return None
    return ids[1]


# Service function for interface
def launch_focus(session): # Launch an automatic zoom during 2 seconds
        session.start_autofocus()
        time.sleep(5)

def get_frame(session):
    return session.get_frame()


# Interface functions
def initiate_reachy_camera(session): # Initiate and give the reachy's camera chosen by the Reachy_camera class
    launch_focus(session)

def n_closest_angle(frame, n, for_test = False): # Give the average angle for the n closest faces using get_n_closest_face
    return global_face_detection_service(frame, get_n_closest_faces, n, for_test)

def framing_for_group_photo_angle(frame, percent_relat_to_avg, for_test = False): # Give the average angle for the faces whose the height is 'percent_relat_to_avg' or less near from the height average, using get_mean_distant_faces
    return global_face_detection_service(frame, get_closest_to_mean_faces, percent_relat_to_avg, for_test)

def smart_give_angle(nbr_frame_to_compute, session, give_angle_function, give_angle_parameter, for_test = False):  # Give the angle, taking face detection hazard into account (no faces detected, non face object detected) to avoid errors whenever possible
    angle_table = []
    avg_angle = Angle(0, 0)
    
    for i in range(nbr_frame_to_compute) :   # Angles to analyse, taking only non null angles into account (==> no faces detected not taken into account)
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
    return nearest_angle   

def take_picture(session, noun): # Take a picture, with an automatic focus, and save it at the 'path' location
   # launch_focus(session)
   cv2.imwrite("./tmp/" + noun + ".png", get_frame(session))

def smart_get_aruco_code(session, nbr_trials):
    for i in range(nbr_trials):
        id = get_aruco_code(get_frame(session))
        if id != None :
            return id
    return None