from pylab import *
import matplotlib.pyplot as plt
from mayavi import mlab
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import Sources.configs.potentialFieldConfig as pfConfig
import math
import sys

x_min = 0
y_min = 0
x_max = 100
y_max = 100

def gaussian_obstacle(X,Y, x_obs, y_obs, size_robot, size_obstacle):
    #We extend the size of the obstacle with the size of the robot (border expansion)
    ext_size = size_robot + size_obstacle
    sigma_x = (ext_size/2)/2.3548
    sigma_y = (ext_size/2)/2.3548
    theta = 0
    A = 100 #Weight of the Gaussian
    Z = zeros_like(X)
    a = cos(theta)**2/2/sigma_x**2 + sin(theta)**2/2/sigma_y**2
    b = -sin(2*theta)/4/sigma_x**2 + sin(2*theta)/4/sigma_y**2
    c = sin(theta)**2/2/sigma_x**2 + cos(theta)**2/2/sigma_y**2
    Z[:] = Z[:]+A*exp( - (a*(X-x_obs)**2 + 2*b*(X-x_obs)*(Y-y_obs) + c*(Y-y_obs)**2))
    return Z

if __name__ == '__main__':
    X, Y = mgrid[x_min:x_max + 1:1, y_min: y_max + 1:1]
    Z = gaussian_obstacle(X, Y, 50, 50, 10, 10)
    # plot surface
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    fig.colorbar(surf)
    plt.show()