from reachy_sdk import ReachySDK
import cv2


# Defining the face recogniser
Face_recognizer = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Useful classes
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Scale:
    def __init__(self, w, h):
        self.width = w
        self.height = h

class Angles:
    def __init__(self, horizontal, vertical):
        self.h = horizontal
        self.v = vertical

class Face:
    def __init__(self, x, y, w, h):
        self.pos = Pos(x, y)
        self.scale = Scale(w, h)

class Face_and_value:
    def __init__(self, face, val):
        self.face = face
        self.value = val



# Mathematical transformations
def give_face_center(face):
    return Pos(face.pos.x + face.scale.width/2, face.pos.y + face.scale.height/2)

def vector_center_to_pos(frame_center_pos, pos):
    return Scale(pos.x - frame_center_pos.x, pos.y - frame_center_pos.y)

def vector_center_to_face(frame_center_pos, face):
    center_pos = give_face_center(face)
    return vector_center_to_pos(frame_center_pos, center_pos)

def scale_to_angle(dist):
    return dist / 150 * 20

def faces_to_faces_and_values(faces):
    faces_and_values = []
    for face in faces:
        faces_and_values.append(Face_and_value(face, 0))
    return faces_and_values

def faces_and_values_to_faces(faces_and_values):
    faces = []
    for face_and_value in faces_and_values:
        faces.append(face_and_value.face)
    return faces

def face_and_value_buble_sort(faces_and_values):
    if(len(faces_and_values) < 2):
        return faces_and_values
    has_switched = True
    while has_switched:
        has_switched = False
        for i in range(len(faces_and_values) - 1):
            if(faces_and_values[i].value > faces_and_values[i+1].value):
                has_switched = True
                faces_and_values[i], faces_and_values[i+1] = faces_and_values[i+1], faces_and_values[i]
    return faces_and_values

def get_mean_position(faces):
    x, y, n = 0, 0, len(faces)
    for face in faces:
        cent_pos = give_face_center(face)
        x += cent_pos.x; y += cent_pos.y
    x /= n; y /= n
    return Pos(x, y)

def get_n_closest_faces(faces, n):
    faces_and_values = faces_to_faces_and_values(faces)
    for face_and_val in range(len(faces_and_values)):
        face_and_val.val = face_and_val.face.height     # Height is an approximation of distances, despite of the different face dimensions
    faces_and_values = face_and_value_buble_sort(faces_and_values)
    return faces_and_values_to_faces(faces_and_values[:n])

def get_closest_to_mean_faces(faces, percent_relat_to_avg):
    s, n = 0, len(faces)
    # Mean face height computation
    for face in faces:
        s += face.height
    avg_size = s/n
    kept_faces = []
    # Adding only faces having width grater than average x minimum_%
    for face in faces:
        if abs(face.height - avg) <= (percent_relat_to_avg * avg):
            kept_faces.append(face)
    return kept_faces


# Capture functionalities
def open_capture(index):  # index is typed int
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    return cap

def read_capture(cap):
    return cap.read()

def face_recognition(frame):
    return Face_recognizer.detectMultiScale(frame, 1.5, 4)

def get_faces(frame):
    recognised = face_recognition(frame)
    faces = []
    for (x, y, w, h) in recognised:
        faces.append(Face(x, y, w, h))
    return faces

def draw_rectangle_on_frame(frame, face):
    cv2.rectangle(frame, (face.pos.x, face.pos.y), (face.pos.x + face.scale.width, face.pos.y + face.scale.height), (255, 0, 0), 2)

def frame_display(frame, window_name):
    cv2.imshow(window_name, frame)

def free_capture_and_windows(cap):
    cap.release()
    cv2.destroyAllWindows()



# Interface functions
def n_closest_angle(frame, n): # USES get_n_closest_face
    faces = get_faces(frame)
    faces = get_n_closest_faces(faces, n)
    mean_faces_pos = get_mean_position(faces)
    scale = vector_center_to_pos(Pos(frame.shape[1]/2, frame.shape[0]/2), mean_faces_pos)
    return Angles(scale_to_angle(scale.width), scale_to_angle(scale.height))


def framing_for_group_photo(frame, percent_relat_to_avg): # USES get_mean_distant_faces
    faces = get_faces(frame)
    faces = get_closest_to_mean_faces(faces, percent_relat_to_avg)
    mean_faces_pos = get_mean_position(faces)
    scale = vector_center_to_pos(Pos(frame.shape[1]/2, frame.shape[0]/2), mean_faces_pos)
    return Angles(scale_to_angle(scale.width), scale_to_angle(scale.height))


# Test function$
def run_test(get_frame, with_angle_to_center):
    while True:
        frame = get_frame()
        
        faces = get_faces(frame)
        
        for i in range(len(faces)):
            face = faces[i]
            draw_rectangle_on_frame(frame, face)
            if with_angle_to_center:
                center_to_face = vector_center_to_face(Pos(frame.shape[1]/2, frame.shape[0]/2), face)
                print(f"Face n°{i} - horizontal angle is {round(scale_to_angle(center_to_face.width), 1)}° - vertical angle is {round(scale_to_angle(center_to_face.height), 1)}°")

        frame_display(frame, 'face_recognition')
        if cv2.waitKey(1) == ord('q'):
            break

def test_all_face_recognised(with_angle_to_center): # Not working on Reachy
    cap = open_capture(0)

    def get_frame():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return frame

    run_test(get_frame, with_angle_to_center)    
    free_capture_and_windows(cap)

def test_all_face_recognised_with_reachy_api(with_angle_to_center):
    reachy = ReachySDK(host='localhost')  # Replace with the actual IP
    camera = reachy.camera.Camera('left')

    def get_frame():
        frame = camera.last_frame
        return frame

    run_test(get_frame, with_angle_to_center)       



if __name__ == '__main__':
    # test_all_face_recognised(True)
    test_all_face_recognised_with_reachy_api(True)