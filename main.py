import Astar_optimised as A
import path_smoothing as ps
import check_line_of_sight as los
import numpy as np
import cv2 
from matplotlib import pyplot as plt

## CONSTANTS
DILATION_SIZE = 6


# open the image
#image1 = cv2.imread("techviko.pgm")
image1 = cv2.imread("blank_map_with_obstacle.pgm")
imageNp = np.array(image1)

#dilate the map
kernel = np.ones((DILATION_SIZE, DILATION_SIZE), np.uint8)
img_erosion = cv2.erode(imageNp, kernel, iterations=2)
mapDilated = cv2.dilate(img_erosion, kernel, iterations=1)
mapgs = cv2.cvtColor(mapDilated, cv2.COLOR_BGR2GRAY)


# find the path
#path = A.optimal_path((433, 452),(1490, 1750), mapgs) # techviko.pgm
path = A.optimal_path((100, 100),(550, 450), mapgs) # blank_map_with_obstacle.pgm


# line of sight minimisation
newPath = ps.los_minimisation(mapgs, path)

# path smoothing



# Draw the images
plt.figure(figsize=(12,12))

plt.imshow(mapgs, plt.cm.gray) # draw map
# draw corners
corners = ps.find_corners(path)
cornersx = [coord[0] for coord in corners]
cornersy = [coord[1] for coord in corners]
plt.scatter(cornersx, cornersy)


# draw paths
try:
    plt.plot(*zip(*newPath)) # draw path
except:
    print("no path found")

""" try:
    plt.plot(*zip(*path)) # draw path
except:
    print("no path found") """

plt.show()