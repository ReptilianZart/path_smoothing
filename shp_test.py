import numpy as np
from matplotlib import pyplot as plt

import shp 

point1 = np.array([7,1])
point2 = np.array([7,7])

Rl = 5.61
Rs = 1

print(shp.generate_curve(Rl,Rs)[0])

Polar = shp.generate_curve(Rl, Rs)



t=np.linspace(0, 2*np.pi,100)
xc1=Rl*np.cos(t) #biggest circle
yc1=Rl*np.sin(t) #biggest circle
plt.plot(xc1,yc1)

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')


plt.plot(*zip(*Polar))

plt.show()