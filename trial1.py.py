# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 18:48:32 2021

@author: Arpita
"""

import cv2
  
# Load our input image
image = cv2.imread("C:\Users\lenovo\Pictures\user_image\000183_0.jpg")
cv2.waitKey()
  
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#filename = 'output.jpg'
cv2.imwrite('C:\\Users\\lenovo\\Pictures\\user_image\\output.jpg', gray_image)
  
cv2.imshow('Grayscale', gray_image)
cv2.waitKey(0)  
  
cv2.destroyAllWindows()