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
from numpy.linalg import norm

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

def angle_between(v1, v2, acw=False):
    """
    if acw = True, will calculate the angle clockwise from v1 to v2
    """
    if not acw:
        return np.arccos(v1.dot(v2)/(norm(v1)*norm(v2)))
    else:
        pass

def polar2cart(polar):
    return polar[0]*m.cos(polar[1]), polar[0]*m.sin(polar[1])

def generate_curve(v1, v2, center, Rl = 4):
    """
    Rl defining how big the larger circle is
    eg. how large the curve is
    """
    angle = angle_between(v1, v2)
    mu = 2*PI/angle
    Rs = Rl/mu

    coords = []

    thetas = np.arange(0, 2*PI/mu, 0.01)
    
    for theta in thetas:
        x=(Rl-Rs)*np.cos(theta)+Rs*np.cos((Rl-Rs)*theta/Rs) + center[0]
        y=(Rl-Rs)*np.sin(theta)-Rs*np.sin((Rl-Rs)*theta/Rs) + center[1]
        coords.append((x,y))
        
    rcoords = coords

    # find first point acw from 1,0 and rotate there
    firstV = v1
    start = np.array([1,0])
    if angle_between(start, v2) < angle_between(start, v1):
        firstV = v2
    print("firstV:", firstV)
    rcoords = rotate_curve(coords, center, angle_between(start, firstV))

    return coords, rcoords

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + m.cos(angle) * (px - ox) - m.sin(angle) * (py - oy)
    qy = oy + m.sin(angle) * (px - ox) + m.cos(angle) * (py - oy)
    return qx, qy


def rotate_curve(curve, center, theta):
    return [rotate(center, coord, theta) for coord in curve]

# find which is least rotated from [1,0] then rotate to that one or the other one

def find_smaller_angle(v1, v2, acw=True):
    """
    finds which angle is smaller v1-v2 or v2-v1 going acw
    """
    x1,y1 = v1
    x2, y2 = v2
    dot = x1*x2 + y1*y2      # dot product between [x1, y1] and [x2, y2]
    det = x1*y2 - y1*x2      # determinant
    angle = m.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    if angle < 0:
        return v2
    return v1