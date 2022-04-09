import sys
sys.path.append("../session")
import reachy_session as rs
from face_detection import *

# To set the focus
def set_focus():
    session = rs.ReachySession()
    session.start_autofocus()

    while True:
        frame = get_frame(session)
        time.sleep(0.1)
        frame_display(frame, 'focus_setting_window')
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    set_focus()