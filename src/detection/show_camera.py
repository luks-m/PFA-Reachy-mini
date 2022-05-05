import sys
sys.path.append("../session")
import reachy_session as rs
from face_detection import *


def show_camera():
    session = rs.ReachySession()

    while True:
        frame = get_frame(session)
        time.sleep(0.1)
        frame_display(frame, 'show_camera')
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    show_camera()