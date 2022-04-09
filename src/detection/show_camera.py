import sys
sys.path.append("../session")
import reachy_session as rs
from face_detection import *

# To set the focus
def show_camera():
    session = rs.ReachySession()

    while True:
        frame = get_frame(session)
        time.sleep(0.1)
        frame_display(frame, 'focus_setting_window')
        if cv2.waitKey(0):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    show_camera()