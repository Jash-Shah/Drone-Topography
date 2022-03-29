#!/usr/bin/env python
# coding: utf-8

# In[5]:


#Importing important libraries
import cv2
import numpy as np
import os
from ContourDetection import Contours
from ContourDetection import Bounding_Box


 
cap = cv2.VideoCapture("C:/Users/Arnav/Downloads/Drone_Beach.mp4")                      #opens the webcam
ret = True                                     #creates a boolean 
ret, old_frame = cap.read()                    #ret is true and the first frame of video saved in old_frame

bg_sub = cv2.createBackgroundSubtractorMOG2(history=500, #subrtacting background from the objects
           varThreshold=200, detectShadows=True)
#Height and wdith of the frames in which video will be written
   
# Below VideoWriter will create object
# a frame of above defined The output 
# is stored in 'Recording.avi' file

kernel = np.ones((20,20),np.uint8) 
# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while ret:
    ret, frame = cap.read()          #saves the first frame of video in frame 
    
    #uses the euclidean function created above to calculate the similarit
    
    contours, areas, image = Contours(bg_sub, kernel, frame)
    
    #if no contour detected
    if len(areas) < 1:
        continue
    #if contour detected
    else:
        max_index = np.argmax(areas) #take the largest movement causing object(area)
        
        frame = Bounding_Box(frame, contours, max_index)
        
    
    # if(sime>95000):                  #Threshold set to 94000 for euclidean distance 
    #     rec_vid.write(frame)         #Records video when movement detected
    
    cv2.imshow('Input', frame)   #opens the webcam in a pop-up window
    cv2.imshow('Threshold', image)
    c = cv2.waitKey(1)           #new frame comes after () ms
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q on keyboard to stop the webcam
        break
    
    
cap.release()
cv2.destroyAllWindows()          #Once out of the while loop, the pop-up window closes automatically

