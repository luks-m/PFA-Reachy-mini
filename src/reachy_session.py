from session import *
from reachysdk import ReachySDK

class ReachySession(Session):

    def __init__(self):
        self._robot = ReachySDK('localhost')

    def turn_on(self):
        self._robot.turn_on('head')

    def turn_off(self):
        self._robot.turn_off('head')

    def look_at(self, x, y, z, d):
        self._robot.head.look_at(x, y, z, d)

    def inverse_kinematics(self, quaternion):
        self._robot.head.inverse_kinematics(quaternion)

    def goto(self, dict, duration):
        self._robot.head.goto(dict, duration)

    def r_antenna_set_position(self, position):
        self._robot.head.r_antenna.goal_position = position
    
    def l_antenna_set_position(self, position):
        self._robot.head.l_antenna.goal_position = position

    def antennas_speed_limit(self, v):
        self._robot.head.r_antenna.speed_limit = v
        self._robot.head.l_antenna.speed_limit = v

    def start_autofocus(self):
        self._robot.left_camera.start_autofocus()

    def stop_autofocus(self):
        self._robot.left_camera.stop_autofocus()

    def get_frame(self):
        return _robot.left_camera.last_frame