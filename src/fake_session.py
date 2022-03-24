from movement import *
from session import *

class FakeSession(Session):

    def turn_on(self):
        print("Last call : turn_on")

    def turn_off(self):
        print("Last call : turn_off")

    def look_at(self, x, y, z, d):
        print("Last call : look_at")

    def inverse_kinematics(self, quaternion):
        print("Last call : look_at")

    def goto(self, dict, duration):
        print("Last call : goto")

    def r_antenna_set_position(self, position):
        print("Last call : r_antenna_set_position")
    
    def l_antenna_set_position(self, position):
        print("Last call : l_antenna_set_position")

    def antennas_speed_limit(self, v):
        print("Last call : antennas_speed_limit")

    def get_angles(self):
        print("get angles")

    def start_autofocus(self):
        print("start autofocus")
    
    def stop_autofocus(self):
        print("stop autofocus")

    def get_frame(self):
        print("get frame")