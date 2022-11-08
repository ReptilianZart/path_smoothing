import check_line_of_sight as los
import numpy as np
from collections import namedtuple
from scipy.interpolate import BSpline


# corner which will hols p0 to p3
corner_control_points = namedtuple("controlPoints",["p0", "p1", "p2", "p3"])




# outputs a list of tuples of coordinates of corners
def find_corners(path):
    corners = []
    # path is a list of tuples of ints
    prevx, prevy = 0, 0
    prevdx, prevdy = 0, 0
    try:
        for i, point in enumerate(path):
            x, y = point
            dx = x-prevx
            dy = y-prevy    

            if i == 0:
                prevx, prevy = x, y
                prevdx, prevdy = dx, dy
                continue

            # check if straight
            elif dx == prevdx and dy == prevdy:
                prevx, prevy = x, y
                prevdx, prevdy = dx, dy
                continue

            # found a corner
            else:
                corners.append(np.array((prevx,prevy))) # add prevx because that is where the corner is
                prevx, prevy = x, y
                prevdx, prevdy = dx, dy
        corners.append(path[-1])
        return corners
    except Exception as e:
        print("\n------------------\nfind_corners error:\n------------------\n",e)


def find_control_points(path, sharpness):
    corners = find_corners(path)
    controlPoints = []
    # find vector from corner to previous
    # get unit vector
    # multiply unit vector by sharpness parameter

    
    for i, corner in enumerate(corners):
        if i == 0 or i == len(corners)-1:
            continue
            
        prevCorner = corners[i-1]
        nextCorner = corners[i+1]
        
        # P0
        v = prevCorner-corner
        unitV = np.divide(v, abs(v), out=np.zeros_like(v), where=v!=0, casting="unsafe")
        p0 = (unitV*sharpness) + corner

        # P3
        v = corner-nextCorner
        unitV = np.divide(v, abs(v), out=np.zeros_like(v), where=v!=0, casting="unsafe")
        p3 = (unitV*sharpness) + corner

        # P1,P2
        p1, p2 =  corner, corner

        cornerPoints = corner_control_points(p0, p1, p2, p3)
        prevCorner = corner
        controlPoints.append(cornerPoints)
    return controlPoints

def display_control_points(obj):
    print("p0", obj.p0, "p1", obj.p1, "p2", obj.p2, "p3", obj.p3)
    


# line of sight minimisation
# start at p1 check p1-p3, p1-p4 etc. until line of sight is false
def los_minimisation(image, path):
    # find the corners
    corners = find_corners(path)
    newPath = []

    # iterate through to find the smoothed path
    currentP = corners[0] # start at p1
    newPath.append(currentP)
    end = False

    while end == False:
        for i,corner in enumerate(corners):
            if corner[0] == corners[-1][0] and corner[1] == corners[-1][1]: # if the corner is the last
                newPath.append(corner)
                end = True
            elif los.check_line_of_sight(image, currentP[0], currentP[1], corner[0], corner[1]):
                # if line of sight continue
                continue
            else:
                newPath.append(corners[i-1])
                currentP = corners[i-1]
        # remove last index from list of indexes and set that to currentP
        
    return newPath


