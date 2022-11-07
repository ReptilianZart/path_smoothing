import Astar_optimised as A
import path_smoothing as ps
import check_line_of_sight as los
import numpy as np
import cv2 
from matplotlib import pyplot as plt

## CONSTANTS
DILATION_SIZE = 6


# open the image
image1 = cv2.imread("techviko.pgm")
imageNp = np.array(image1)

#dilate the map
kernel = np.ones((DILATION_SIZE, DILATION_SIZE), np.uint8)
img_erosion = cv2.erode(imageNp, kernel, iterations=5)
mapDilated = cv2.dilate(img_erosion, kernel, iterations=1)
mapgs = cv2.cvtColor(mapDilated, cv2.COLOR_BGR2GRAY)


# find the path
#path = A.optimal_path((433, 452),(1490, 1750), mapgs) # techviko.pgm
path = A.optimal_path((100, 100),(75, 300), mapgs) # blank_map_with_obstacle.pgm


# path smoothing


# controlPoints = ps.find_control_points(path,5)

# newPath = ps.smoothed_path(mapgs, path)



# Draw the images
plt.figure(figsize=(12,12))

plt.imshow(mapgs, plt.cm.gray) # draw map
# draw corners
corners = ps.find_corners(path)
cornersx = [coord[0] for coord in corners]
cornersy = [coord[1] for coord in corners]
plt.scatter(cornersx, cornersy)
print("corners",corners[0],corners[1])


# draw paths
try:
    plt.plot(*zip(*newPath)) # draw path
except:
    print("no path found")

try:
    plt.plot(*zip(*path)) # draw path
except:
    print("no path found")
plt.show()