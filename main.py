import cv2
import numpy as np
from matplotlib import pyplot as plt

import Astar_optimised as A
import check_line_of_sight as los
import path_smoothing as ps
import shp

# CONSTANTS
DILATION_SIZE = 6


# open the image
image1 = cv2.imread("./assets/techviko.pgm")
#image1 = cv2.imread("./assets/blank_map_with_obstacle.pgm")
#image1 = cv2.imread("./assets/map_dtu.pgm")
imageNp = np.array(image1)

# dilate the map
kernel = np.ones((DILATION_SIZE, DILATION_SIZE), np.uint8)
img_erosion = cv2.erode(imageNp, kernel, iterations=3)
mapDilated = cv2.dilate(img_erosion, kernel, iterations=1)
mapgs = cv2.cvtColor(mapDilated, cv2.COLOR_BGR2GRAY)


# find the path
path = A.optimal_path((433, 452), (1490, 1750), mapgs)  # techviko.pgm
# blank_map_with_obstacle.pgm
#path = A.optimal_path((100, 240), (550, 210), mapgs)
#path = A.optimal_path((220, 200), (154, 180), mapgs)


# line of sight minimisation

newPath = ps.los_minimisation(mapgs, path)


# Draw the images
plt.figure(figsize=(12, 12))

# draw corners
corners = ps.find_corners(newPath)
cornersx = [coord[0] for coord in corners]
cornersy = [coord[1] for coord in corners]
plt.scatter(cornersx, cornersy)

plt.imshow(image1, plt.cm.gray)  # draw map


# path smoothing
smoothPath = shp.shp_smooth_path(newPath, curve_factor=100, max_Rl=15)


# draw paths
""" try:
    plt.plot(*zip(*newPath), label="los minimised path")  # draw path
except:
    print("no los") """

try:
    plt.plot(*zip(*smoothPath), label="smooth path")  # draw path
except:
    print("no smooth path")

""" try:
    plt.plot(*zip(*path))  # draw path
except:
    print("no path") """

plt.show()
