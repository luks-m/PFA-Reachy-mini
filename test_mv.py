import numpy as np
from reachy_sdk import ReachySDK

r = 1
t = 0
p = 0


def spherical_to_cartesian(radius, theta, phi):
    t = degree_to_radian(theta)
    p = degree_to_radian(phi)
    x = round(radius*np.sin(t)*np.cos(p), 2)
    y = round(radius*np.sin(t)*np.sin(p), 2)
    z = round(radius*np.cos(t), 2)
    return x, y, z


def degree_to_radian(angle):
    return angle*2*np.pi / 360

def radian_to_degree(angle):
    return angle*360/(2*np.pi)


def cartesian_to_spherical(x, y, z):
    r = round(np.sqrt(x**2+y**2+z**2),2)
    phi = round(radian_to_degree(np.arccos(x/(np.sqrt(x**2+y**2)))),2)
    theta = round(radian_to_degree(np.arccos(z/r)),2)
    return r, theta, phi

ecoute = cartesian_to_spherical(0.5, 0, -0.05)
triste = cartesian_to_spherical(0.5, 0, -0.3)
content = cartesian_to_spherical(0.5, 0, -0.05)
incitation = cartesian_to_spherical(0.5, 0, 0.05)
reflexion = cartesian_to_spherical(0.5, 0.15, 0.15)
remerciement = cartesian_to_spherical(0.5, 0, -0.25)


ec = spherical_to_cartesian(0.5, 95.74, 0)
tr = spherical_to_cartesian(0.58, 121.15, 0)
t=2
v = np.sqrt((ec[0]-tr[0])**2+(ec[1]-tr[1])**2+(0.3-tr[2])**2)/t
print(v)



