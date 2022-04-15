import code
import pyrealsense2 as rs
import numpy as np
import cv2
import numpy as np
# from matplotlib.mlab import griddata
import scipy
# import pandas as pd
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import *
import matplotlib.pyplot as plt
import scipy as sp
import scipy.interpolate
from mpl_toolkits.mplot3d.axes3d import *
import matplotlib.pyplot as plt
from matplotlib import cm


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    fig = plt.figure()
    ax = Axes3D(fig)
    well = 0
    while (True):

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        # print(np.unique(depth_image))
        # np.arrange
        print("one array done", well)
        well += 1

    #     print(np.shape(depth_image))
        # x =  np.zeros(307200)
        # y = np.zeros(307200)
        # z = np.zeros(307200)
        x = []
        y = []
        z=[]


        plt.cla()

    #     #mapping code
        count = 0
        # for i in range(depth_image.shape[0]):
        #     for j in range(depth_image.shape[1]):
        for i in range(480):
            for j in range(640):
                if(depth_image[i][j]>=2000):
                    # x[count] = i
                    # y[count] = j
                    # z[count] = depth_image[i][j]

                    x.append(i)
                    y.append(j)
                    z.append(depth_image[i][j])
                    count = count + 1
    #             # print(i,j,depth_image[i][j])
    #         #     count = count +  5
    #         #     j = j+ 5
    #         # i = i + 5

        x = np.asarray(x, dtype='uint8')
        y = np.asarray(y, dtype='uint8')
        z = np.asarray(z, dtype='uint8')
    #     # print("finally", "\nx, ", x, "\ny ", y, "\nz", z)
        
    #     # 2D grid construction
        spline = sp.interpolate.Rbf(x,y,z,function='thin-plate')
        xi = np.linspace(min(x), max(x))
        yi = np.linspace(min(y), max(y))
        X, Y = np.meshgrid(xi, yi)
        # interpolation
        Z = spline(X,Y)
        

        ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.jet,linewidth=1, antialiased=True)
    #     ax.scatter3D(x,y,z,c=z,cmap=plt.cm.jet)
        
        plt.pause(0.05)
    plt.show()
    
        


        # color_image = np.asanyarray(color_frame.get_data())

        # # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # depth_colormap_dim = depth_colormap.shape
        # color_colormap_dim = color_image.shape

        # # If depth and color resolutions are different, resize color image to match depth image for display
        # if depth_colormap_dim != color_colormap_dim:
        #     resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        #     images = np.hstack((resized_color_image, depth_colormap))
        # else:
        #     images = np.hstack((color_image, depth_colormap))

        # # Show images
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)
        # cv2.waitKey(1)
        
finally:

    # Stop streaming
    pipeline.stop()