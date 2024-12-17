import numpy as np
import matplotlib.pyplot as plt
# Define three one-dimensional arrays
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
z = np.array([7, 8, 9])
print(np.linspace(1, 5, 10)[::-1])
# Create a meshgrid
X, Y = np.meshgrid(x, y)

# Create a 3D surface by combining the meshgrid with the z array
Z = np.array([z] * len(y))
fig = plt.Figure((5,4))
ax = fig.add_subplot(111, projection = "3d")
ax.plot_surface(X, Y, Z)
print("X:", X)
print("Y:", Y)
print("Z:", Z)

