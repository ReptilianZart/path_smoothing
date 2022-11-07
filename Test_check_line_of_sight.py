import check_line_of_sight as los
import cv2 
import numpy as np
from matplotlib import pyplot as plt

x1, y1, x2, y2 = 110, 220, 500, 390

# open the image
image1 = cv2.imread("blank_map_with_obstacle.pgm")
imagegs = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#imageNp = np.array(imagegs)

#dilate the map
kernel = np.ones((20, 20), np.uint8)
img_erosion = cv2.erode(imagegs, kernel, iterations=1)
mapDilated = cv2.erode(img_erosion, kernel, iterations=1)





print("line of sight is: ", los.check_line_of_sight(mapDilated, x1, y1, x2, y2))

# Draw the images
plt.imshow(mapDilated, plt.cm.gray) # draw map
line = los.get_line(x1, y1, x2, y2)
X = [point[0] for point in line]
Y = [point[1] for point in line]
plt.plot(X,Y)

plt.show()