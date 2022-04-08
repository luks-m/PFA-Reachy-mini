from turtle import pos
import time
import numpy as np
import sys
sys.path.append("../session")
from session import *

global PHI
global THETA
global TMP_PHI
global TMP_THETA

PHI = 0
THETA = 90
TMP_PHI = 0
TMP_THETA = 90

def motor_on(session):
    session.turn_on()

def motor_off(session):
    session.turn_off()

def __euler_to_quaternion(roll, pitch, yaw):

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qx, qy, qz, qw]

def __degree_to_radian(theta):
    return theta*2*np.pi / 360

def __fit_angles(theta, phi):
    if 45 < theta and theta < 130:
        t = theta
    elif 130 <= theta:
        t = 130
    elif 45 >= theta:
        t = 45
    if -45 < phi and phi < 45:
        p = phi
    elif 45 <= phi:
        p = 45
    elif -45 >= phi:
        p = -45
    return t, p

def __spherical_to_cartesian(radius, theta, phi):
    theta = __degree_to_radian(theta)
    phi = __degree_to_radian(phi)
    x = round(radius*np.sin(theta)*np.cos(phi), 2)
    y = round(radius*np.sin(theta)*np.sin(phi), 2)
    z = round(radius*np.cos(theta), 2)
    return [x, y, z]

def __duration(coordinates_prev, coordinates_next, v):
    duration = round(np.sqrt((coordinates_next[0] - coordinates_prev[0])**2 + (coordinates_next[1]-coordinates_prev[1])**2 + (coordinates_next[2]-coordinates_prev[2])**2)/v, 2)
    if duration <= 0:
        return 0.5
    else:
        return duration

def move_to(session, radius, theta, phi, v):
    global TMP_PHI
    global TMP_THETA
    position_prev = __spherical_to_cartesian(0.5, TMP_THETA, TMP_PHI)
    TMP_THETA, TMP_PHI = __fit_angles(theta, phi)
    position = __spherical_to_cartesian(radius, TMP_THETA, TMP_PHI)
    session.look_at(position[0], position[1], position[2], __duration(position_prev, position, v))

def update_position(session, theta, phi, v):
    global PHI
    global THETA
    global TMP_PHI
    global TMP_THETA

    t = THETA
    p = PHI
    theta, phi = round(theta,2), round(phi,2)

    position_prev = __spherical_to_cartesian(0.5, THETA, PHI)
    THETA, PHI = __fit_angles(THETA + theta, PHI + phi)

    TMP_THETA = THETA
    TMP_PHI = PHI

    print(THETA, PHI, theta, phi)

    position = __spherical_to_cartesian(1, THETA, PHI)
    
    mouv = None

    try:
        tmp = True
        mouv = session.inverse_kinematics(__euler_to_quaternion(0, __degree_to_radian(THETA - t), __degree_to_radian(PHI - p)))
    except ValueError:
        tmp = False

    if tmp:
        angles = session.get_angles()
        angle = {
            angles["neck_disk_top"]: mouv[0],
            angles["neck_disk_middle"]: mouv[1],
            angles["neck_disk_bottom"]: mouv[2],
        }
        #NoneObject is not subscriptable mouv = None

        session.goto(angle, __duration(position_prev, position, v))

def listen(session):
    session.r_antenna_set_position(0)
    session.l_antenna_set_position(0)

    move_to(session, 0.5, THETA, PHI, 0.15)
        
def sad(session):
    session.r_antenna_set_position(70.0)
    session.l_antenna_set_position(70.0)

    session.r_antenna_set_position(-140.0)
    session.l_antenna_set_position(140.0)

    move_to(session, 0.5, 31.15 + THETA, PHI, 0.13)

def happy(session):
    move_to(session, 0.5, 5.74 + THETA, PHI, 0.15)

    session.antennas_speed_limit(300.0)
    
    for _ in range(10):
        session.r_antenna_set_position(-20.0)
        session.l_antenna_set_position(20.0)
        time.sleep(0.1)
        session.r_antenna_set_position(20.0)
        session.l_antenna_set_position(-20.0)
        time.sleep(0.1)
    
    session.r_antenna_set_position(0.0)
    session.l_antenna_set_position(0.0)

def incentive(session):
    session.antennas_speed_limit(70.0)
    session.r_antenna_set_position(-35.0)
    session.l_antenna_set_position(35.0)

    move_to(session, 0.5, -5.74 + THETA, PHI, 0.1)

def thinking(session):
    session.antennas_speed_limit(70.0)
    session.r_antenna_set_position(40.0)
    session.l_antenna_set_position(-40.0)

    move_to(session, 0.5, -16.13 + THETA, 16.7 + PHI, 0.21)

def thanking(session):
    session.antennas_speed_limit(70.0)
    session.r_antenna_set_position(0.0)
    session.l_antenna_set_position(0.0)

    move_to(session, 0.5, 5.74 + THETA, PHI, 0.15)

    time.sleep(0.1)

    session.r_antenna_set_position(-40.0)
    session.l_antenna_set_position(40.0)
    
    move_to(session, 0.5, 26.51 + THETA, PHI, 0.35)
    
    time.sleep(0.3)
    
    session.r_antenna_set_position(0.0)
    session.l_antenna_set_position(0.0)
    
    move_to(session, 0.5, 5.74 + THETA, PHI, 0.35)

def move_back(session):
    global TMP_PHI
    global TMP_THETA
    global THETA
    global PHI

    position_prev = __spherical_to_cartesian(0.5, TMP_THETA, TMP_PHI)
    TMP_THETA = THETA
    TMP_PHI = PHI
    position = __spherical_to_cartesian(0.5, THETA, PHI)
    session.look_at(position[0], position[1], position[2], __duration(position_prev, position, 0.15))
