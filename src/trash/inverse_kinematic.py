from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
import time
import numpy as np

def f(x,y,z,angle):
    m3 = np.around(R.from_euler('z', np.deg2rad(angle)).as_matrix(), 3)
    m4 = np.zeros((4,4))
    for i in range(3):
        for j in range(3):
            m4[i][j] = m3[i][j]
    m4[0][3] = x
    m4[1][3] = y
    m4[2][3] = z
    m4[3] = np.array([0,0,0,1])
    print(m4)
    mouv = reachy.head.inverse_kinematics(m4)
    reachy.head.goto({joint: pos for joint,pos in zip(reachy.head.joints.values(), mouv)}, duration=1.0)


def euler_to_quaternion(roll, pitch, yaw):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw]

reachy = ReachySDK(host='localhost')

print(reachy.head)

print("head")

reachy.turn_on('head')
print("on")

mouv = reachy.head.inverse_kinematics(euler_to_quaternion(0,0,-3.14/2))
print(mouv)
# tab = {joint: pos for joint,pos in zip(reachy.head.joints.values(), mouv)}
# tab = tab
angle = { reachy.head.neck_disk_top : mouv[0],
           reachy.head.neck_disk_middle : mouv[1],
           reachy.head.neck_disk_bottom : mouv[2]}
print(angle)
goto(angle, duration=1.0)
time.sleep(5)

# angle = { reachy.head.neck_disk_top : -104.70,
#           reachy.head.neck_disk_middle : -111.47,
#           reachy.head.neck_disk_bottom : -110.86,}
# goto(angle, 1)
# time.sleep(5)
# angle = { reachy.head.neck_disk_top : -4.66,
#           reachy.head.neck_disk_middle : -5.8,
#           reachy.head.neck_disk_bottom : -2.88,}
# goto(angle, 1)
# time.sleep(5)

reachy.turn_off('head')
print("off")