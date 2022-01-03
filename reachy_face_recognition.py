import cv2
from math import radians

def give_center(x, y, w, h):
    return (x + w/2, y + h/2)

def give_pos_from_center(frame_center_x, frame_center_y, sqr_info):
    center_pos = give_center(sqr_info[0], sqr_info[1], sqr_info[2], sqr_info[3])
    return (frame_center_x - center_pos[0], frame_center_y - center_pos[1])

def scale_to_angle(gap_from_center):
    return gap_from_center / 150 * 20

def to_radians(angle):
    return radians(angle)


face_recognizer = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    success, frame = cap.read() 
    if not success:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    faces = face_recognizer.detectMultiScale(frame, 1.5, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        pos_2_center = give_pos_from_center(frame.shape[1]/2, frame.shape[0]/2, (x, y, w, h))
        print("horizontal angle is", round(scale_to_angle(pos_2_center[0]), 1), "° ", "vertical angle is", round(scale_to_angle(pos_2_center[1]), 1), "°")

    cv2.imshow('face_recognition', frame)
    if cv2.waitKey(30) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()