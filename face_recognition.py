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

def vector_face_from_center(frame_center_pos, face):
    center_pos = give_face_center(face)
    return [frame_center_pos.x - center_pos.x, frame_center_pos.y - center_pos.y]

def scale_to_angle(dist):
    return dist / 150 * 20

def get_n_closest_face(n, cv_face_rectangles): # TODO ==============================================================
    n = len(cv_face_rectangles)
    # Adding only faces having width grater than average x minimum_%
    if(n < 1):
        return 
    else:
        kept_face = cv_face_rectangles[0]
    for i in range(n):
        if cv_face_rectangles[i].w < dist:
            dist = cv_face_rectangles[i].w
            ketp_face = cv_face_rectangles[i]
    return kept_faces

def get_mean_distant_faces(cv_face_rectangles, minimum_percentage): # TODO VERIFY ==============================================================
    sum = 0
    n = len(cv_face_rectangles)
    # Mean face width computation
    for i in range(n):
        sum += cv_face_rectangles[i].w
    avg = sum/n
    kept_faces = []
    # Adding only faces having width grater than average x minimum_%
    for i in range(n):
        if cv_face_rectangles[i].w >= (minimum_percentage * avg):
            kept_faces.append(cv_face_rectangles[i])
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
def angles_to_closest(frame): # USES get_n_closest_face
    pass

def framing_for_group_photo(frame): # USES get_mean_distant_faces
    pass


# Test function
def test_all_face_recognised(with_angle_to_center): # Not working on Reachy
    cap = open_capture(0)

    while True:
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        faces = get_faces(frame)
        
        for i in range(len(faces)):
            face = faces[i]
            draw_rectangle_on_frame(frame, face)
            if with_angle_to_center:
                center_to_face = vector_face_from_center(Pos(frame.shape[1]/2, frame.shape[0]/2), face)
                print(f"Face n°{i} - horizontal angle is {round(scale_to_angle(center_to_face[0]), 1)}° - vertical angle is {round(scale_to_angle(center_to_face[1]), 1)}°")

        frame_display(frame, 'face_recognition')
        if cv2.waitKey(1) == ord('q'):
            break
    
    free_capture_and_windows(cap)

if __name__ == '__main__':
    test_all_face_recognised(True)