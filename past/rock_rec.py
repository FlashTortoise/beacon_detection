# -*- coding: utf-8 -*-
"""
Created on Sat May 20 14:58:17 2017

@author: YS W
"""

import numpy as np
import cv2

rock_cascade = cv2.CascadeClassifier('E:\wenyisi\Rock_cascade.xml')

img1 = cv2.imread('E:\wenyisi\Test_1.jpg')
# img2 = cv2.imread('g:\rec\test_2.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


# Detects objects of different sizes in the input image.
# The detected objects are returned as a list of rectangles.
# cv2.CascadeClassifier.detectMultiScale(image, scaleFactor, minNeighbors, flags, minSize, maxSize)
# scaleFactor – Parameter specifying how much the image size is reduced at each image
# scale.
# minNeighbors – Parameter specifying how many neighbors each candidate rectangle should
# have to retain it.
# minSize – Minimum possible object size. Objects smaller than that are ignored.
# maxSize – Maximum possible object size. Objects larger than that are ignored.
rock = rock_cascade.detectMultiScale(gray1, 1, 10)
for (x, y, w, h) in rock:
    img1 = cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray1[y:y + h, x:x + w]
    roi_color = img1[y:y + h, x:x + w]

cv2.imshow('img', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
