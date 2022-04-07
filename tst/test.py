from movement import *
from face_detection import *
from reachy_session import ReachySession
from math import radians
import cv2
from reachy_sdk import ReachySDK
from time import *

# session = ReachySession()
# f = session._robot._camera.last_frame
# print(f)
# cv2.imshow("test", f)

# # camera = reachy.left_camera

# # camera.start_autofocus
# # time.sleep(2)
# # camera.stop_autofocus

# initiate_reachy_camera(session)
# print("robot ok")
# motor_on(session)
# print("motor on")

# move_to(session, 1, 90, 0, 0.5)

# time.sleep(2)
# t = time.time()



# while((time.time() - t) < 5):
#     frame = get_frame(session)
#     frame_display(frame, "image")
#     angle = n_closest_angle(frame, 1)
#     print(angle.h , angle.v)
# #   update_position(session, -radians(angle.v),-radians(angle.h) , 0.5)
#     time.sleep(2)


# print("end")
# time.sleep(5)
# motor_off(session)
# print("motor off")

#robot1 = ReachySDK('localhost')
robot2 = ReachySession()

#frame1 = robot1.right_camera.last_frame
#frame2 = robot2.get_frame()

#cv2.imshow("test", frame1)
#cv2.imshow("test", frame2)
initiate_reachy_camera(robot2)
robot2.start_autofocus()
sleep(5)
robot2.stop_autofocus()
i = 0
while(i < 20):
    angle = smart_give_angle(robot2, 10, n_closest_angle, 1, True)
    update_position(robot2, angle.v, angle.h, 0.5)
    i+=1
    
cv2.waitKey(0)

