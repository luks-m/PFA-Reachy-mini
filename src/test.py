from movement import *
from face_detection import *

reachy = ReachySDK(host='localhost')

print(reachy.head)

print("head")
robot = Movement(reachy)

# camera = reachy.left_camera

# camera.start_autofocus
# time.sleep(2)
# camera.stop_autofocus

reachy_cam = initiate_reachy_camera(reachy)
print("robot ok")
robot.motor_on()
print("motor on")

robot.head.look_at(1, 0, 0, 2)

time.sleep(5)


angle = n_closest_angle(reachy_cam.get_frame(), 1)
print(angle.h , angle.v)
robot.update_position(angle.v, angle.h, 0.5)

print("end")
time.sleep(5)
robot.motor_off()
print("motor off")