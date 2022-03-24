from movement import *
from face_detection import *
from reachy_session import ReachySession
from math import radians

session = ReachySession()

# camera = reachy.left_camera

# camera.start_autofocus
# time.sleep(2)
# camera.stop_autofocus

initiate_reachy_camera(session)
print("robot ok")
motor_on(session)
print("motor on")

move_to(session, 1, 90, 0, 0.5)

time.sleep(2)
t = time.time()

while((time.time() - t) < 20):
    angle = n_closest_angle(get_frame(session), 1)
    print(angle.h , angle.v)
    update_position(session, -radians(angle.v),-radians(angle.h) , 0.5)
    time.sleep(1)


print("end")
time.sleep(5)
motor_off(session)
print("motor off")