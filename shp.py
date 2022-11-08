"""
SHP Smooth Hypocycloid path, is a path smoothed 
as shown in https://journals.sagepub.com/doi/epub/10.5772/63458

using the corner point as the center a circle of r = Rl, can be created. 
a smaller circle of r = Rs rolls on the inside of the big circle
creating a hypocycloid

mu = number of cusps
epsilon = Rs / Rl

"""

import math as m
import numpy as np

PI = 3.1415

def generate_shp_curve(before_corner, corner, after_corner):
    """ 
        generates a curve from 2 unit vectors and a center point
        where the curvature can be defined by Rl and Rs
        takes the corner point which will be the center
    """
    # get angle between 2 vectors
    # mu = 360/theta
    # 
    return None

def calc_distance(point1, point2):
    return np.linalg.norm((point2-point1))

def calc_unit_vector(point1, point2):
    """takes np as input, point1 to point2 unit vector"""
    vector = point2 - point1
    magn = calc_distance(point1, point2)
    unitV = np.divide(vector, magn)
    return unitV

def angle_between(v1, v2):
    return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

def polar2cart(polar):
    return polar[0]*m.cos(polar[1]), polar[0]*m.sin(polar[1])

def generate_curve(Rl, Rs):
    epsilon = Rs/Rl
    mu = 1/epsilon

    coords = []
    thetas = np.arange(0, 2*PI*mu, 0.01)
    
    for theta in thetas:

        x = Rl*(epsilon)*((mu-1)*m.cos(theta) + m.cos((mu-1)*theta))
        y = Rl*(epsilon)*((mu-1)*m.sin(theta) + m.sin((mu-1)*theta))

        y = (1-r)*np.sin(theta)-r*np.sin((1-r)/r*theta)
        x = (1-r)*np.cos(theta)+r*np.cos((1-r)/r*theta)

        coords.append((x,y))
        
    return coords

