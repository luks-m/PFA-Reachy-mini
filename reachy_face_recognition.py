import cv2
from math import radians

class face_rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

# Mathematical transformations
def give_center(x, y, w, h):
    return (x + w/2, y + h/2)

def give_pos_from_center(frame_center_x, frame_center_y, sqr_info):
    center_pos = give_center(sqr_info[0], sqr_info[1], sqr_info[2], sqr_info[3])
    return (frame_center_x - center_pos[0], frame_center_y - center_pos[1])

def scale_to_angle(gap_from_center):
    return gap_from_center / 150 * 20

def to_radians(angle):
    return radians(angle)

def get_forward_faces(cv_face_rectangles, minimum_percentage):
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

def face_recognition(frame, face_recognizer):
    return face_recognizer.detectMultiScale(frame, 1.5, 4)

def draw_rectangle_on_frame(frame, x, y, w, h):
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

def frame_display(frame, window_name):
    cv2.imshow(window_name, frame)

def free_capture_and_windows(cap):
    cap.release()
    cv2.destroyAllWindows()


def main():
    face_recognizer = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = open_capture(0)

    while True:
        sucess, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        faces = face_recognition(frame, face_recognizer)
        for (x, y, w, h) in faces:
            draw_rectangle_on_frame(frame, x, y, w, h)
            pos_2_center = give_pos_from_center(frame.shape[1]/2, frame.shape[0]/2, (x, y, w, h))
            print("horizontal angle is", round(scale_to_angle(pos_2_center[0]), 1), "° ", "vertical angle is", round(scale_to_angle(pos_2_center[1]), 1), "°")

        frame_display('face_recognition', frame)
        if cv2.waitKey(30) == ord('q'):
            break
    
    free_capture_and_windows(cap)
    

main()