from reachy_sdk import ReachySDK

import time
import numpy as np


angle_cote = 0
angle_hauteur = 90

def motor_on():
    reachy.turn_on('head')

def notor_off():
    reachy.turn_off('head')

def degree_to_radian(angle):
    return angle*2*np.pi / 360

def spherical_to_cartesian(radius, theta, phi):
    t = degree_to_radian(theta)
    p = degree_to_radian(phi)
    x = round(radius*np.sin(t)*np.cos(p), 2)
    y = round(radius*np.sin(t)*np.sin(p), 2)
    z = round(radius*np.cos(t), 2)
    return [x, y, z]

def duree(coords,v):
    pos_act = spherical_to_cartesian(0.5, angle_hauteur, angle_cote)
    return np.sqrt((coords[0]-pos_act[0])**2 + (coords[1]-pos_act[1])**2 + (coords[2]-pos_act[2])**2)*v

ecoute = spherical_to_cartesian(0.5, 5.74 + angle_hauteur, angle_cote)
triste = spherical_to_cartesian(0.5, 31.15 + angle_hauteur, angle_cote)
content = spherical_to_cartesian(0.5, 5.74 + angle_hauteur, angle_cote)
incitation = spherical_to_cartesian(0.5, -5.74 + angle_hauteur, angle_cote)
reflexion = spherical_to_cartesian(0.5, -16.13 + angle_hauteur, 16.7 + angle_cote)
remerciement = spherical_to_cartesian(0.5, 26.51 + angle_hauteur, angle_cote)

def mouv(position,d):
    reachy.head.look_at(x=position[0], y=position[1], z=position[2], duration=d)

def ecoute():
    reachy.head.l_antenna.goal_position = 0
    reachy.head.r_antenna.goal_position = 0
    mouv(ecoute, duree(ecoute,0.25))

def triste():
    reachy.head.l_antenna.speed_limit = 70.0
    reachy.head.r_antenna.speed_limit = 70.0
    
    reachy.head.l_antenna.goal_position = 140.0
    reachy.head.r_antenna.goal_position = -140.0
    mouv(triste, duree(triste,0.29))

def content():
    mouv(content, duree(content,0.25))
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

def incitation():
    reachy.head.l_antenna.speed_limit = 70.0
    reachy.head.r_antenna.speed_limit = 70.0
    reachy.head.l_antenna.goal_position = +35.0
    reachy.head.r_antenna.goal_position = -35.0
    mouv(incitation, duree(incitation,0.50))

def reflexion():
    reachy.head.l_antenna.speed_limit = 70.0
    reachy.head.r_antenna.speed_limit = 70.0
    reachy.head.l_antenna.goal_position = -40.0
    reachy.head.r_antenna.goal_position = +40.0
    mouv(reflexion,duree(reflexion,0.54))

def remerciement():
    reachy.head.l_antenna.speed_limit = 70.0
    reachy.head.r_antenna.speed_limit = 70.0
    reachy.head.l_antenna.goal_position = 0.0
    reachy.head.r_antenna.goal_position = 0.0
    
    mouv(ecoute, duree(ecoute,0.25))
    time.sleep(0.1)    
    reachy.head.l_antenna.goal_position = +40.0
    reachy.head.r_antenna.goal_position = -40.0
    mouv(remerciement,duree(remerciement,1.11))
    time.sleep(0.3)
    reachy.head.l_antenna.goal_position = 0.0
    reachy.head.r_antenna.goal_position = 0.0
    mouv(ecoute,duree(ecoute,1.11))

def mouv_cam(angles):
    mouv(1, angle_hauteur + angles[0], angle_cote + angles[1])

reachy = ReachySDK(host='localhost')  # Replace with the actual IP

reachy.head

for name, joint in reachy.joints.items():
    print(f'Joint "{name}" position is {joint.present_position} degree.')

content()
