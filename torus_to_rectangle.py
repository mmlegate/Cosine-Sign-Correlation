import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Note I am using y-axis as the canonical z-axis

def cylinder(v):
    # Initialize rectangle (width 2, height 4)
    x = np.linspace(-1, 1, 100)
    y = np.linspace(-2, 2, 100)
    z = np.linspace(-1, 1, 100)

    theta_i = np.sign(x) * np.arctan(np.absolute(x))
    r_i = np.sqrt(np.square(x) + 1)

    theta_f = np.linspace(-np.pi, np.pi, 100)
    r_f = 1

    x_list = []
    z_list = []
    y_list = []
    for j in range(100):
      yy = y[j]
      for i in range(100):
          theta = theta_i[i] + (theta_f[i] - theta_i[i]) * v / 100
          r = r_i[i] + (r_f - r_i[i]) * v / 100
          xx = r * np.cos(theta)
          zz = r * np.sin(theta)
          x_list.append(xx)
          z_list.append(zz)
          y_list.append(yy)
    return np.array(x_list), np.array(z_list), np.array(y_list)

def torus(v):
  x_i, z_i, y_i = cylinder(100)
  theta = np.sign(z_i) * np.arccos(x_i)
  R = np.sqrt(np.square(y_i) + np.square(2-x_i))
  r = 1
  R_f = 2
  phi_i = np.sign(y_i) * np.arctan(np.absolute(y_i)/(2-x_i))
  phi_f = np.linspace(-np.pi, np.pi, 10000)

  myr_f = R_f + r * np.cos(theta)
  z_f = z_i.copy()
  x_f = x_i.copy()
  y_f = y_i.copy()

  for i in range(10000):
    myr_chosen = myr_f[i]
    xwow = myr_chosen * np.cos(phi_f[i])
    x_f[i] = x_i[i] + (xwow - x_i[i]) * v/100
    ywow = myr_chosen * np.sin(phi_f[i])
    y_f[i] = y_i[i] + (ywow - y_i[i]) * v/100

  return np.array(x_f), np.array(z_f), np.array(y_f)

# Number of points to use for drawing the shapes
n_points = 100

# Define plot
fig = plt.figure()
my_cmap = plt.get_cmap('coolwarm')
ax = fig.add_subplot(111, projection='3d')

# Function to update the frame
def update(frame):
    ax.clear()
    if frame < 50:
        # Draw rectangle
        version = 0
        a,b,c = cylinder(version)
        ax.scatter(a, b, c, c = c, cmap = my_cmap, linewidth=0, alpha=0.1)
        ax.set_title('Rectangle')

    elif frame < 150:
        # Transform rectangle to cylinder
        version = frame - 50
        a,b,c = cylinder(version)
        ax.scatter(a, b, c, c = c, cmap = my_cmap, linewidth=0, alpha=0.1)

    elif frame < 200:
        # Draw cylinder
        version = 100
        a,b,c = cylinder(version)
        ax.scatter(a, b, c, c = c, cmap = my_cmap, linewidth=0, alpha=0.1)
        ax.set_title('Cylinder')

    elif frame < 300:
        # Transform cylinder to torus
        version = frame - 200
        a,b,c = torus(version)
        ax.scatter(a, b, c, c = c, cmap = my_cmap, linewidth=0, alpha = 0.1)

    else:
        version = 100
        a,b,c = torus(version)
        ax.scatter(a, b, c, c = c, cmap = my_cmap, linewidth=0, alpha = 0.1)
        ax.set_title('Torus')


    # Set the view limits and labels
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.axis('off')

# Create the animation
n_frames = 350
ani = FuncAnimation(fig, update, frames=np.arange(350, -1, -1), interval=50)

ani.save('cylinder.gif', fps=30)