import numpy as np
from reachy_sdk import ReachySDK

r = 1
t = 0
p = 0


def spherical_to_cartesian(radius, theta, phi):
    t = degree_to_radian(theta)
    p = degree_to_radian(phi)
    x = radius*np.sin(t)*np.cos(p)
    y = radius*np.sin(t)*np.sin(p)
    z = radius*np.cos(t)
    return x, y, z


def degree_to_radian(angle):
    return angle*2*np.pi / 360


def cartesian_to_spherical(x, y, z):
    r = np.sqrt(x**2+y**2+z**2)
    theta = np.arccos(x/(np.sqrt(x**2+y**2)))
    phi = np.arccos(z/r)
    return r, theta, phi

ecoute = cartesian_to_spherical(0.5, 0, -0.05)
triste = cartesian_to_spherical(0.5, 0, -0.3)
content = cartesian_to_spherical(0.5, 0, -0.05)
incitation = cartesian_to_spherical(0.5, 0, 0.05)
reflexion = cartesian_to_spherical(0.5, 0.15, 0.15)
remerciement = cartesian_to_spherical(0.5, 0, -0.25)

print(ecoute)
print(triste)
print(content)
print(incitation)
print(reflexion)
print(remerciement)
