__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import matplotlib.pyplot as plt
import numpy as np
import math


n, d = 50, 100
pts = np.random.random(size=(n, d)) - 0.5
D, ANG = [], []
for i, p1 in enumerate(pts):
    for j, p2 in enumerate(pts[i+1:]):
        dist = sum((p1-p2)**2)**0.5
        ang = 180/math.pi*math.acos(np.dot(p1,p2)/np.linalg.norm(p1)/np.linalg.norm(p2))
        D.append(dist)
        ANG.append(ang)

plt.scatter(D, ANG, alpha=0.4)
plt.xlabel('Distance b/w pair')
plt.ylabel('Angle b/w pair')

#  plt.subplot(122)
#  plt.scatter(ANG)
#  plt.title('Angle between two vectors')

plt.title(f'dim={d}, num points={n}')
plt.tight_layout()

plt.show()

