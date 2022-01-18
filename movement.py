import reachy_sdk_api
from reachy_sdk import ReachySDK

import time

reachy = ReachySDK(host='localhost')  # Replace with the actual IP

for name, joint in reachy.joints.items():
    print(f'Joint "{name}" position is {joint.present_position} degree.')

reachy.turn_on('head') # Don't forget to put the hand in stiff mode
reachy.head.look_at(x=0.5, y=0, z=0, duration=1.0)

look_right = reachy.head.look_at(x=0.5, y=-0.5, z=0.1, duration=1.0)
time.sleep(0.1)
look_down = reachy.head.look_at(x=0.5, y=0, z=-0.4, duration=1.0)
time.sleep(0.1)
look_left = reachy.head.look_at(x=0.5, y=0.3, z=-0.3, duration=1.0)
time.sleep(0.1)
look_front = reachy.head.look_at(x=0.5, y=0, z=0, duration=1.0)