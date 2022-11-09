import numpy as np
from matplotlib import pyplot as plt

import shp 

PI = np.pi

point1 = np.array([6,1])
point2 = np.array([-5,6])
cornerP = np.array([0,0])

Rl = 3 # changes how big the curve is


print("angle-between",shp.angle_between(point1, point2))

coords, rcoords = shp.generate_curve(point1, point2, cornerP, Rl=Rl)
print(coords[0])


t=np.linspace(0, 2*np.pi,100)
xc1=Rl*np.cos(t) + cornerP[0] #biggest circle
yc1=Rl*np.sin(t) + cornerP[1] #biggest circle
plt.plot(xc1,yc1)

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')


plt.plot([point1[0], cornerP[0], point2[0], ], [point1[1], cornerP[1], point2[1]], label="straigh_path")
plt.scatter([point1[0], cornerP[0], point2[0], ], [point1[1], cornerP[1], point2[1]])


plt.plot(*zip(*rcoords), label="rcoords")
plt.plot(*zip(*coords), label="coords")
ax.legend(loc="upper left")
plt.show()