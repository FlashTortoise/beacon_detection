import cv2
import numpy as np

def nothing(x):
    pass

im = cv2.imread('E:\Rectangle_shape.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(imgray, 127, 255, 0)

thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                      cv2.THRESH_BINARY, 11, 2)

image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(im, contours, -1, (0, 255, 0), 2)
print max(contours)
cv2.imshow('img', img)
k = cv2.waitKey(5000) & 0xFF
cnt = contours[0]
M = cv2.moments(cnt)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print cx,cy
print imgray.shape

picture_size = imgray.shape

error_percent = 0.01 # 1%

down_boundary = picture_size[1]/2 - picture_size[1]*error_percent
up_boundary = picture_size[1]/2 + picture_size[1]*error_percent

if down_boundary <= cx <= up_boundary:
    # pass
    print 'middle'
elif cx < down_boundary:
    # turn right
    # pass
    print 'need to turn right'
else:
    #turn left
    # pass
    print 'need to turn left'