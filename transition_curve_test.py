import random as r
import numpy as np
from matplotlib import pyplot as plt

import shp

# should start at A, go past B and end at C

A = np.array([((r.random()*50)-25), ((r.random()*50)-25)])
B = np.array([((r.random()*50)-25), ((r.random()*50)-25)])
C = np.array([((r.random()*50)-25), ((r.random()*50)-25)])

trans_curve = shp.transition_curve(A, B, C, 10, 5)

plt.plot(*zip(*trans_curve), label="curve")


plt.scatter(*zip(*[A, B, C]))

plt.show()
