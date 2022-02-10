from attr import attributes
from reachy_sdk import ReachySDK

import time
import numpy as np

class Mouvement:
    #attributes
    _angle_cote = 0
    _angle_hauteur = 90
    _ecoute = [0,0,0]
    _triste = [0,0,0]
    _content = [0,0,0]
    _incitation = [0,0,0]
    _reflexion = [0,0,0]
    _remerciement = [0,0,0]

    def __init__(self):
        None

    def motor_on(self):
        reachy.turn_on('head')

    def notor_off(self):
        reachy.turn_off('head')

    def degree_to_radian(self,angle):
        return angle*2*np.pi / 360

    def verif(self, theta, phi):
        if theta > 45:
            if theta < 130:
                t = self.degree_to_radian(theta)
            else:
                t = self.degree_to_radian(130)
        else:
            t = self.degree_to_radian(45)
        if phi > -45:
            if phi < 45:
               p = self.degree_to_radian(phi)
            else:
                p = self.degree_to_radian(45)
        else:
            p = self.degree_to_radian(-45)
        return t,p

    def spherical_to_cartesian(self,radius, theta, phi):
        t,p = self.verif(theta,phi)
        x = round(radius*np.sin(t)*np.cos(p), 2)
        y = round(radius*np.sin(t)*np.sin(p), 2)
        z = round(radius*np.cos(t), 2)
        return [x, y, z]

    def duree(self,coords,v):
        pos_act = self.spherical_to_cartesian(0.5, self._angle_hauteur, self._angle_cote)
        return np.sqrt((coords[0]-pos_act[0])**2 + (coords[1]-pos_act[1])**2 + (coords[2]-pos_act[2])**2)*v

    def mouv(self,position,d):
        reachy.head.look_at(x=position[0], y=position[1], z=position[2], duration=d)

    def ecoute(self):
        reachy.head.l_antenna.goal_position = 0
        reachy.head.r_antenna.goal_position = 0
        self._ecoute = self.spherical_to_cartesian(0.5, 5.74 + self._angle_hauteur, self._angle_cote)
        self.mouv(self._ecoute, self.duree(self._ecoute,0.25))

    def triste(self):
        reachy.head.l_antenna.speed_limit = 70.0
        reachy.head.r_antenna.speed_limit = 70.0
        
        reachy.head.l_antenna.goal_position = 140.0
        reachy.head.r_antenna.goal_position = -140.0
        self._triste = self.spherical_to_cartesian(0.5, 31.15 + self._angle_hauteur, self._angle_cote)
        self.mouv(self._triste, self.duree(self._triste,0.29))

    def content(self):
        self._content = self.spherical_to_cartesian(0.5, 5.74 + self._angle_hauteur, self._angle_cote)
        self.mouv(self._content, self.duree(self._content,0.25))
        reachy.head.l_antenna.speed_limit = 300.0
        reachy.head.r_antenna.speed_limit = 300.0
        
        for _ in range(10):
            reachy.head.l_antenna.goal_position = 20.0
            reachy.head.r_antenna.goal_position = -20.0
            time.sleep(0.1)
            reachy.head.l_antenna.goal_position = -20.0
            reachy.head.r_antenna.goal_position = 20.0
            time.sleep(0.1)
        
        reachy.head.l_antenna.goal_position = 0.0
        reachy.head.r_antenna.goal_position = 0.0

    def incitation(self):
        reachy.head.l_antenna.speed_limit = 70.0
        reachy.head.r_antenna.speed_limit = 70.0
        reachy.head.l_antenna.goal_position = +35.0
        reachy.head.r_antenna.goal_position = -35.0
        self._incitation = self.spherical_to_cartesian(0.5, -5.74 + self._angle_hauteur, self._angle_cote)
        self.mouv(self._incitation, self.duree(self._incitation,0.50))

    def reflexion(self):
        reachy.head.l_antenna.speed_limit = 70.0
        reachy.head.r_antenna.speed_limit = 70.0
        reachy.head.l_antenna.goal_position = -40.0
        reachy.head.r_antenna.goal_position = +40.0
        self._reflexion = self.spherical_to_cartesian(0.5, -16.13 + self._angle_hauteur, 16.7 + self._angle_cote)
        self.mouv(self._reflexion,self.duree(self._reflexion,0.54))

    def remerciement(self):
        reachy.head.l_antenna.speed_limit = 70.0
        reachy.head.r_antenna.speed_limit = 70.0
        reachy.head.l_antenna.goal_position = 0.0
        reachy.head.r_antenna.goal_position = 0.0
        
        self._ecoute = self.spherical_to_cartesian(0.5, 5.74 + self._angle_hauteur, self._angle_cote)
        self._remerciement = self.spherical_to_cartesian(0.5, 26.51 + self._angle_hauteur, self._angle_cote)

        self.mouv(self._ecoute, self.duree(self._ecoute,0.25))
        time.sleep(0.1)    
        reachy.head.l_antenna.goal_position = +40.0
        reachy.head.r_antenna.goal_position = -40.0
        self.mouv(self._remerciement,self.duree(self._remerciement,1.11))
        time.sleep(0.3)
        reachy.head.l_antenna.goal_position = 0.0
        reachy.head.r_antenna.goal_position = 0.0
        self.mouv(self._ecoute,self.duree(self._ecoute,1.11))

    def mouv_cam(self,angles):
        t,p = self.verif(self._angle_hauteur + angles[0], self._angle_cote + angles[1])
        self._angle_hauteur = t
        self._angle_cote = p
        pos = self.spherical_to_cartesian(1, self._angle_hauteur, self._angle_cote)
        self.mouv(pos,self.duree(pos,2))


reachy = ReachySDK(host='localhost')  # Replace with the actual IP

reachy.head

for name, joint in reachy.joints.items():
    print(f'Joint "{name}" position is {joint.present_position} degree.')

mouv = Mouvement()
mouv.motor_on()
mouv.content()
