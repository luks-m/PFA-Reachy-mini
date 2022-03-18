from movement import *
from face_detection import *
from reachy_session import ReachySession
from math import radians

session = ReachySession()
robot = Movement(session, session._robot)

# camera = reachy.left_camera

# camera.start_autofocus
# time.sleep(2)
# camera.stop_autofocus

reachy_cam = initiate_reachy_camera(session._robot)
print("robot ok")
robot.motor_on()
print("motor on")

session._robot.head.look_at(1, 0, 0, 2)

time.sleep(5)
t = time.time()

while((time.time() - t) < 20):
    angle = n_closest_angle(reachy_cam.get_frame(), 1)
    print(angle.h , angle.v)
    robot.update_position(-radians(angle.v),-radians(angle.h) , 0.5)
    time.sleep(1)


print("end")
time.sleep(5)
robot.motor_off()
print("motor off")