from turtle import pos
from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
import time
import numpy as np

class Movement :
    def __init__(self, reachy):
        self.robot = reachy
        self.head = reachy.head
        self._phi = 0
        self._theta = 90
        self._tmpphi = 0
        self._tmptheta = 90

    def motor_on(self):
        self.robot.turn_on('head')

    def motor_off(self):
        self.robot.turn_off('head')

    def euler_to_quaternion(roll, pitch, yaw):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw]
    
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
        self.head.look_at(position[0], position[1], position[2], self.duration(position_prev, position, v))

    def update_position(self, theta, phi, v):
        self.move_back()
        position_prev = self.spherical_to_cartesian(0.5, self._theta, self._phi)
        self._theta, self._phi = self.fit_angles(self._theta + theta, self._phi + phi)

        self._tmptheta = self._theta
        self._tmpphi = self._phi
        position = self.spherical_to_cartesian(1, self._theta, self._phi)

        mouv = self.head.inverse_kinematics(self.euler_to_quaternion(0,theta, phi))
        angle = { self.head.neck_disk_top : mouv[0],
           self.head.neck_disk_middle : mouv[1],
           self.head.neck_disk_bottom : mouv[2]}
        goto(angle, self.duration(position_prev, position, v))

    def listen(self):
        self.head.l_antenna.goal_position = 0
        self.head.r_antenna.goal_position = 0

        self.move_to(0.5, self._theta, self._phi, 0.15)
        
    def sad(self):
        self.head.l_antenna.speed_limit = 70.0
        self.head.r_antenna.speed_limit = 70.0

        self.head.l_antenna.goal_position = 140.0
        self.head.r_antenna.goal_position = -140.0

        self.move_to(0.5, 31.15 + self._theta, self._phi, 0.13)

    def happy(self):
        self.move_to(0.5, 5.74 + self._theta, self._phi, 0.15)

        self.head.l_antenna.speed_limit = 300.0
        self.head.r_antenna.speed_limit = 300.0
        
        for _ in range(10):
            self.head.l_antenna.goal_position = 20.0
            self.head.r_antenna.goal_position = -20.0
            time.sleep(0.1)
            self.head.l_antenna.goal_position = -20.0
            self.head.r_antenna.goal_position = 20.0
            time.sleep(0.1)
        
        self.head.l_antenna.goal_position = 0.0
        self.head.r_antenna.goal_position = 0.0
    
    def incentive(self):
        self.head.l_antenna.speed_limit = 70.0
        self.head.r_antenna.speed_limit = 70.0
        self.head.l_antenna.goal_position = +35.0
        self.head.r_antenna.goal_position = -35.0

        self.move_to(0.5, -5.74 + self._theta, self._phi, 0.1)

    def thinking(self):
        self.head.l_antenna.speed_limit = 70.0
        self.head.r_antenna.speed_limit = 70.0
        self.head.l_antenna.goal_position = -40.0
        self.head.r_antenna.goal_position = +40.0

        self.move_to(0.5, -16.13 + self._theta, 16.7 + self._phi, 0.21)

    def thanking(self):
        self.head.l_antenna.speed_limit = 70.0
        self.head.r_antenna.speed_limit = 70.0
        self.head.l_antenna.goal_position = 0.0
        self.head.r_antenna.goal_position = 0.0

        self.move_to(0.5, 5.74 + self._theta, self._phi, 0.15)

        time.sleep(0.1)

        self.head.l_antenna.goal_position = +40.0
        self.head.r_antenna.goal_position = -40.0
        
        self.move_to(0.5, 26.51 + self._theta, self._phi, 0.35)
        
        time.sleep(0.3)
        
        self.head.l_antenna.goal_position = 0.0
        self.head.r_antenna.goal_position = 0.0
        
        self.move_to(0.5, 5.74 + self._theta, self._phi, 0.35)

    def move_back(self):
        position_prev = self.spherical_to_cartesian(0.5, self._tmptheta, self._tmpphi)
        self._tmptheta = self._theta
        self._tmpphi = self._phi
        position = self.spherical_to_cartesian(0.5, self._theta, self._phi)
        self.head.look_at(position[0], position[1], position[2], self.duration(position_prev, position, 0.15))


# reachy = ReachySDK(host='localhost')

# print(reachy.head)

# print("head")
# robot = Movement(reachy)
# print("robot ok")
# robot.motor_on()
# print("motor on")

# robot.head.look_at(1, 0, 0, 2)

# robot.update_position(0,20,0.5)

# robot.listen()
# time.sleep(0.5)
# robot.sad()
# time.sleep(0.5)
# robot.listen()
# time.sleep(0.5)
# robot.happy()
# time.sleep(0.5)
# robot.incentive()
# time.sleep(0.5)
# robot.thinking()
# time.sleep(0.5)
# robot.thanking()
# time.sleep(0.5)


# print("end")
# time.sleep(5)
# robot.motor_off()
# print("motor off")