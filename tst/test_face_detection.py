import time
import sys
sys.path.append("../src/detection")
sys.path.append("../src/session")

from face_detection import *
from reachy_session import ReachySession

# Test functions

## For first MVP
def run_all_face_tests(get_frame_bis, with_angle_to_center):    # Code factorization function to identify all faces without interface functions
    while True:
        frame = get_frame_bis()
        
        faces = get_faces(frame)
        
        for i in range(len(faces)):
            face = faces[i]
            draw_rectangle_on_frame(frame, face)
            if with_angle_to_center:
                center_to_face = vector_center_to_face(Pos(frame.shape[1]/2, frame.shape[0]/2), face)
                print(f"Face n°{i} - horizontal angle is {round(scale_to_angle(center_to_face.width), 1)}° - vertical angle is {round(scale_to_angle(center_to_face.height), 1)}°")

        time.sleep(0.1)
        frame_display(frame, 'face_detection')
        if cv2.waitKey(1) == ord('q'):
            break

def test_all_face_recognised(with_angle_to_center): # Not working on Reachy
    cap = open_capture(0)

    def get_frame_bis():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return give_in_gray(frame)

    run_all_face_tests(get_frame_bis, with_angle_to_center)    
    free_capture_and_windows(cap)

def test_all_face_recognised_with_reachy_api(with_angle_to_center):
    session = ReachySession()

    def get_frame_bis():
        return give_in_gray(get_frame(session))

    run_all_face_tests(get_frame_bis, with_angle_to_center)       


## For interface functions
def run_get_angle_functions_tests(get_frame_bis, get_angle, get_angle_args):    # Code factorization function to print the average angle given by the get_angle function
    while True:
        frame = get_frame_bis()
        
        angle = get_angle(frame, get_angle_args, for_test = True)
        
        print(f"horizontal angle is {round(angle.h, 1)}° - vertical angle is {round(angle.v, 1)}°")

        time.sleep(0.1)
        if cv2.waitKey(1) == ord('q'):
            break

def test_n_closest_angle(n): # Not working on Reachy
    cap = open_capture(0)

    def get_frame_bis():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return frame

    run_get_angle_functions_tests(get_frame_bis, n_closest_angle, n)
    free_capture_and_windows(cap)

def test_n_closest_angle_with_reachy_api(n):
    session = ReachySession()

    def get_frame_bis():
        return give_in_gray(get_frame(session))

    run_get_angle_functions_tests(get_frame_bis, n_closest_angle, n)

def test_framing_for_group_photo_angle(percent_relat_to_avg): # Not working on Reachy
    cap = open_capture(0)

    def get_frame_bis():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return frame

    run_get_angle_functions_tests(get_frame_bis, framing_for_group_photo_angle, percent_relat_to_avg)    
    free_capture_and_windows(cap)

def test_framing_for_group_photo_angle_with_reachy_api(percent_relat_to_avg):
    session = ReachySession()

    def get_frame_bis():
        return give_in_gray(get_frame(session))

    run_get_angle_functions_tests(get_frame_bis, framing_for_group_photo_angle, percent_relat_to_avg)

def smart_give_angle_test():
    cap = open_capture(0)

    def get_frame_bis():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return frame
    
    while True :
        angle = smart_give_angle(5, get_frame_bis, n_closest_angle, 2, for_test = True)

        print(f"horizontal angle is {round(angle.h, 1)}° - vertical angle is {round(angle.v, 1)}°")

        time.sleep(0.1)
        if cv2.waitKey(1) == ord('q'):
            break

def smart_give_angle_test_with_reachy_api():
    session = ReachySession()

    def get_frame_bis():
        return give_in_gray(get_frame(session))
    
    while True :
        angle = smart_give_angle(session, 5, n_closest_angle, 1, for_test = True)

        print(f"horizontal angle is {round(angle.h, 1)}° - vertical angle is {round(angle.v, 1)}°")

        time.sleep(0.1)
        if cv2.waitKey(1) == ord('q'):
            break



if __name__ == '__main__': # Relevant test experiences
    # test_all_face_recognised(True)
    #test_all_face_recognised_with_reachy_api(True)

    # test_n_closest_angle(0)
    # test_n_closest_angle(1)
    # test_n_closest_angle(2)
    # test_n_closest_angle_with_reachy_api(0)
    # test_n_closest_angle_with_reachy_api(1)
    # test_n_closest_angle_with_reachy_api(2)

    # test_framing_for_group_photo_angle(0.2)
    # test_framing_for_group_photo_angle(0.5)
    # test_framing_for_group_photo_angle_with_reachy_api(0.2)
    # test_framing_for_group_photo_angle_with_reachy_api(0.5)

    # smart_give_angle_test()
    smart_give_angle_test_with_reachy_api()