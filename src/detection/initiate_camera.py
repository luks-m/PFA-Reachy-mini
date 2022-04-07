import sys
sys.path.append("../session")
from session import *

# To set the focus

session = ReachySession()
session.start_autofocus()

while True:
        frame = get_frame(session)
        # time.sleep(0.1)
        frame_display(frame, 'focus_setting_window')
        if cv2.waitKey(1) == ord('q'):
            break

session.stop_autofocus()