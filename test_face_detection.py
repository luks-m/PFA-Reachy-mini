import time
from face_detection import *


# Test functions

## For first MVP
def run_all_face_tests(get_frame, with_angle_to_center):    # Code factorization function to identify all faces without interface functions
    while True:
        frame = get_frame()
        
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

    def get_frame():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return give_in_gray(frame)

    run_all_face_tests(get_frame, with_angle_to_center)    
    free_capture_and_windows(cap)

def test_all_face_recognised_with_reachy_api(with_angle_to_center):
    camera = initiate_reachy_camera(ReachySDK(host='localhost'))  # Replace with the actual IP

    def get_frame():
        return give_in_gray(camera.get_frame())

    run_all_face_tests(get_frame, with_angle_to_center)       


## For interface functions
def run_get_angle_functions_tests(get_frame, get_angle, get_angle_args):    # Code factorization function to print the average angle given by the get_angle function
    while True:
        frame = get_frame()
        
        angle = get_angle(frame, get_angle_args, for_test = True)
        
        print(f"horizontal angle is {round(angle.h, 1)}° - vertical angle is {round(angle.v, 1)}°")

        time.sleep(0.1)
        if cv2.waitKey(1) == ord('q'):
            break

def test_n_closest_angle(n): # Not working on Reachy
    cap = open_capture(0)

    def get_frame():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return frame

    run_get_angle_functions_tests(get_frame, n_closest_angle, n)    
    free_capture_and_windows(cap)

def test_n_closest_angle_with_reachy_api(n):
    camera = initiate_reachy_camera(ReachySDK(host='localhost'))  # Replace with the actual IP

    def get_frame():
        return camera.get_frame()

    run_get_angle_functions_tests(get_frame, n_closest_angle, n)

def test_framing_for_group_photo_angle(percent_relat_to_avg): # Not working on Reachy
    cap = open_capture(0)

    def get_frame():
        success, frame = read_capture(cap)
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return frame

    run_get_angle_functions_tests(get_frame, framing_for_group_photo_angle, percent_relat_to_avg)    
    free_capture_and_windows(cap)

def test_framing_for_group_photo_angle__with_reachy_api(percent_relat_to_avg):
    camera = initiate_reachy_camera(ReachySDK(host='localhost'))  # Replace with the actual IP

    def get_frame():
        return camera.get_frame()

    run_get_angle_functions_tests(get_frame, framing_for_group_photo_angle, percent_relat_to_avg)


if __name__ == '__main__': # Relevant test experiences
    test_all_face_recognised(True)
    # test_all_face_recognised_with_reachy_api(False)

    # test_n_closest_angle(0)
    # test_n_closest_angle(1)
    # test_n_closest_angle(2)
    # test_n_closest_angle_with_reachy_api(0)
    # test_n_closest_angle_with_reachy_api(1)
    # test_n_closest_angle_with_reachy_api(2)

    # test_framing_for_group_photo_angle(0.2)
    # test_framing_for_group_photo_angle(0.5)
    # test_framing_for_group_photo_angle__with_reachy_api(0.2)
    # test_framing_for_group_photo_angle__with_reachy_api(0.5)