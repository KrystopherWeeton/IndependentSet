import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmap
from matplotlib.axes import Axes

# Generate surface
"""
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)
"""

x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 2, 3])

z = []
for y_i in y:
    z.append([y_i + x_i for x_i in x])

plt.imshow(z, cmap=cmap.summer, vmin=0, vmax=10)
ax: Axes = plt.gca()

ax.set_xticks(np.arange(len(x)))
ax.set_yticks(np.arange(len(y)))

ax.set_xticklabels(x)
ax.set_yticklabels(y)

for i in range(len(x)):
    for j in range(len(y)):
        ax.text(i, j, str(z[j][i]), ha="center", va="center", color="black")

plt.colorbar()
plt.show()



"""
ax = plt.axes(projection='3d')

ax.contour3D(X, Y, z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');
"""

plt.show()