from turtle import pos
from reachy_sdk import ReachySDK
import time
import numpy as np

class Movement :
    def __init__(self, robot: reachy):
        self.robot = reachy
        self._phi = 0
        self._theta = 90
        self._tmpphi = 0
        self._tmptheta = 90

    def motor_on(self):
        return True

    def motor_off(self):
        return True
    
    def degree_to_radian(self, theta):
        return theta*2*np.pi / 360

    def fit_angles(self, theta, phi):
        if 45 < theta and theta < 130:
            t = theta 
        elif 130 < theta:
            t = 130
        else:
            t = 45
        if -45 < phi and phi < 45:
            p = phi
        elif 45 < phi:
            p = 45
        else:
            p = -45
        return t,p

    def spherical_to_cartesian(self,radius, theta, phi):
        theta = self.degree_to_radian(theta)
        phi = self.degree_to_radian(phi)
        x = round(radius*np.sin(theta)*np.cos(phi), 2)
        y = round(radius*np.sin(theta)*np.sin(phi), 2)
        z = round(radius*np.cos(theta), 2)
        return [x, y, z]
    
    def duration(self, coordinates_prev, coordinates_next, v):
        duration = round(np.sqrt((coordinates_next[0]-coordinates_prev[0])**2 + (coordinates_next[1]-coordinates_prev[1])**2 + (coordinates_next[2]-coordinates_prev[2])**2)/v,2)
        if duration <= 0:
            return 0.5
        else:
            return duration


    def move_to(self, radius, theta, phi, v):
        position_prev = self.spherical_to_cartesian(0.5, self._tmptheta, self._tmpphi)
        self._tmptheta, self._tmpphi = self.fit_angles(theta, phi)
        position = self.spherical_to_cartesian(radius, self._tmptheta, self._tmpphi)
        return True

    def update_position(self, theta, phi, v):
        print(self._theta, self._phi)
        position_prev = self.spherical_to_cartesian(0.5, self._theta, self._phi)
        self._theta, self._phi = self.fit_angles(self._theta + theta, self._phi + phi)
        print(self._theta, self._phi)
        self._tmptheta = self._theta
        self._tmpphi = self._phi
        position = self.spherical_to_cartesian(1, self._theta, self._phi)
        print(self.duration(position_prev, position, v))
        return True

    def listen(self):
        self.move_to(0.5, self._theta, self._phi, 0.15)
        
    def sad(self):
        self.move_to(0.5, 31.15 + self._theta, self._phi, 0.13)

    def happy(self):
        self.move_to(0.5, 5.74 + self._theta, self._phi, 0.15)

    def incentive(self):
        self.move_to(0.5, -5.74 + self._theta, self._phi, 0.1)

    def thinking(self):
        self.move_to(0.5, -16.13 + self._theta, 16.7 + self._phi, 0.21)

    def thanking(self):
        self.move_to(0.5, 5.74 + self._theta, self._phi, 0.15)
        time.sleep(0.1)
        self.move_to(0.5, 26.51 + self._theta, self._phi, 0.35)
        time.sleep(0.3)
        self.move_to(0.5, 5.74 + self._theta, self._phi, 0.35)

    def move_back(self):
        return True
