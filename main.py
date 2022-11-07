import Astar_optimised as A
import path_smoothing as ps
import check_line_of_sight as los
import numpy as np
import cv2 
from matplotlib import pyplot as plt

## CONSTANTS
DILATION_SIZE = 6


# open the image
image1 = cv2.imread("blank_map_with_obstacles.pgm")
imageNp = np.array(image1)

#dilate the map
kernel = np.ones((DILATION_SIZE, DILATION_SIZE), np.uint8)
img_erosion = cv2.erode(imageNp, kernel, iterations=2)
mapDilated = cv2.dilate(img_erosion, kernel, iterations=1)
mapgs = cv2.cvtColor(mapDilated, cv2.COLOR_BGR2GRAY)


# find the path
# path = A.optimal_path((433, 452),(1490, 1750), map) # techviko map
path = A.optimal_path((100, 100),(550, 550), mapgs) # blank_map_with_obstacle.pgm


# path smoothing
corners = ps.find_corners(path)
cornersx = [coord[0] for coord in corners]
cornersy = [coord[1] for coord in corners]

controlPoints = ps.find_control_points(path,5)

newPath = ps.smoothed_path(mapgs, path)



# Draw the images
plt.figure(figsize=(12,12))

plt.imshow(mapDilated, plt.cm.gray) # draw map
plt.scatter(cornersx, cornersy)
try:
    plt.plot(*zip(*newPath)) # draw path
except:
    print("no path found")

plt.show()