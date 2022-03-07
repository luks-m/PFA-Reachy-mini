from reachy_sdk import ReachySDK
from movement import *

class Session:

    def __init__(sel, robot: r):
        self._robot = r or ReachySDK('localhost')
        self.reachy = Movement(self._robot)

    def motor_on(self):
        self._robot.motor_on()

    def motor_off(self):
        self._robot.motor_off()

    def move_to(self, radius, theta, phi, v):
        self.reachy.move_to(radius, theta, phi, v)

    def update_position(self, theta, phi, v):
        self.reachy.update_position(theta, phi, v)
    
    def listen(self):
        self.reachy.listen()

    def sad(self):
        self.reachy.sad()

    def happy(self):
        self.reachy.happy()

    def incentive(self):
        self.reachy.incentive()
    
    def thanking(self):
        self.reachy.thanking()
    
    def thinking(self):
        self.reachy.thinking()
    
    def move_back(self):
        self.reachy.move_back()
        
