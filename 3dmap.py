import numpy as np
# from matplotlib.mlab import griddata
import scipy
# import pandas as pd
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import *
import matplotlib.pyplot as plt
import scipy as sp
import scipy.interpolate

# df = pd.read_csv("home/aniruddha/coords.csv", header = None, usecols=[1,2,3])
# # y = pd.read_csv("home/aniruddha/coords.csv", usecols=[1])
# # z = pd.read_csv("home/aniruddha/coords.csv", usecols=[2])
# print(df.values)

fig = plt.figure()
ax = Axes3D(fig)

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter3D(x,y,z,c=z,cmap=plt.cm.jet)  
# plt.show()

x_orig = np.random.rand(10000000)
y_orig = np.random.rand(10000000)
z_orig = np.random.rand(1000000)
i = 0
while(1):

    x = x_orig[i:i+200]
    y = y_orig[i:i+200]
    z = z_orig[i:i+200]


    plt.cla()
    # 2D grid construction
    spline = sp.interpolate.Rbf(x,y,z,function='thin-plate')
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(xi, yi)
    # interpolation
    Z = spline(X,Y)
    i += 50
    

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,linewidth=1, antialiased=True)
    
    plt.pause(0.4)


plt.show()

