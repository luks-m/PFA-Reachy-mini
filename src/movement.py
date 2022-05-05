from turtle import pos
import time
import numpy as np
import sys
sys.path.append("../session")
from session import *

#Switch on the motorisation of the head
def motor_on(session):
    session.turn_on()

#Switch off the motorisation of the head
def motor_off(session):
    session.turn_off()

#Convert euler angles into quaternion
def __euler_to_quaternion(roll, pitch, yaw):
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qx, qy, qz, qw]

#Convert degree angles into radian
def __degree_to_radian(theta):
    return theta*2*np.pi / 360

#Check the validity of the angles and correct them if necessary
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

#Convert spherical cooridnates into cartesian
def __spherical_to_cartesian(radius, theta, phi):
    theta = __degree_to_radian(theta)
    phi = __degree_to_radian(phi)
    x = round(radius*np.sin(theta)*np.cos(phi), 2)
    y = round(radius*np.sin(theta)*np.sin(phi), 2)
    z = round(radius*np.cos(theta), 2)
    return [x, y, z]

#Compute the duration of the move according to the velocity and the previous and next positions
def __duration(coordinates_prev, coordinates_next, v):
    duration = round(np.sqrt((coordinates_next[0] - coordinates_prev[0])**2 + (coordinates_next[1]-coordinates_prev[1])**2 + (coordinates_next[2]-coordinates_prev[2])**2)/v, 2)
    if duration <= 0:
        return 0.5
    else:
        return duration

#Make the head move to the given position without storing the previous position (emotional move)
def move_to(session, radius, theta, phi, v):
    position_prev = __spherical_to_cartesian(0.5, session.TMP_THETA, session.TMP_PHI)
    session.TMP_THETA, session.TMP_PHI = __fit_angles(theta, phi)
    position = __spherical_to_cartesian(radius, session.TMP_THETA, session.TMP_PHI)
    session.look_at(position[0], position[1], position[2], __duration(position_prev, position, v))

#Make the head move and store the previous position to move back if necessary
def update_position(session, theta, phi, v):
    theta, phi = round(theta,2), round(phi,2)

    session.THETA, session.PHI = __fit_angles(session.TMP_THETA + theta, session.TMP_PHI + phi)
    
    mouv = None

    try:
        tmp = True
        mouv = session.inverse_kinematics(__euler_to_quaternion(0, __degree_to_radian(session.THETA - session.TMP_THETA), __degree_to_radian(session.PHI - session.TMP_PHI)))
    except ValueError:
        tmp = False

    if tmp:
        angles = session.get_angles()
        angle = {
            angles["neck_disk_top"]: mouv[0],
            angles["neck_disk_middle"]: mouv[1],
            angles["neck_disk_bottom"]: mouv[2],
        }

    session.goto(angle, __duration(__spherical_to_cartesian(0.5, session.TMP_THETA, session.TMP_PHI), __spherical_to_cartesian(1, session.THETA, session.PHI), v))

    session.TMP_THETA = session.THETA
    session.TMP_PHI = session.PHI

#Make the emotion of listening
def listen(session):
    session.r_antenna_set_position(0)
    session.l_antenna_set_position(0)

    move_to(session, 0.5, session.THETA, session.PHI, 0.15)
        
#Make the emotion of being sad
def sad(session):
    session.r_antenna_set_position(70.0)
    session.l_antenna_set_position(70.0)

    session.r_antenna_set_position(-140.0)
    session.l_antenna_set_position(140.0)

    move_to(session, 0.5, 31.15 + session.THETA, session.PHI, 0.13)

#Make the emotion of being happy
def happy(session):
    move_to(session, 0.5, 5.74 + session.THETA, session.PHI, 0.15)

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

#Make the move to attract people
def incentive(session):
    session.antennas_speed_limit(70.0)
    session.r_antenna_set_position(-35.0)
    session.l_antenna_set_position(35.0)

    move_to(session, 0.5, -5.74 + session.THETA, session.PHI, 0.1)

#Make the move of thinking
def thinking(session):
    session.antennas_speed_limit(70.0)
    session.r_antenna_set_position(40.0)
    session.l_antenna_set_position(-40.0)

    move_to(session, 0.5, -16.13 + session.THETA, 16.7 + session.PHI, 0.21)

#Make the move to thank people
def thanking(session):
    session.antennas_speed_limit(70.0)
    session.r_antenna_set_position(0.0)
    session.l_antenna_set_position(0.0)

    move_to(session, 0.5, 90, 0, 0.15)

    time.sleep(0.1)

    session.r_antenna_set_position(-40.0)
    session.l_antenna_set_position(40.0)
    
    move_to(session, 0.5, 120, 0, 0.35)
    
    time.sleep(0.3)
    
    session.r_antenna_set_position(0.0)
    session.l_antenna_set_position(0.0)
    
    move_to(session, 0.5, 90, 0, 0.35)

#move back to the previous position
def move_back(session):
    update_position(session, session.THETA, session.PHI, 0.15)
    # position_prev = __spherical_to_cartesian(0.5, session.TMP_THETA, session.TMP_PHI)
    # session.TMP_THETA = session.THETA
    # session.TMP_PHI = session.PHI
    # position = __spherical_to_cartesian(0.5, session.THETA, session.PHI)
    # session.look_at(position[0], position[1], position[2], __duration(position_prev, position, 0.15))