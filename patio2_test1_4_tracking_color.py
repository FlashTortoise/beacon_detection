# coding=utf-8
import cv2
import numpy as np

def nothing(x):
    pass

frame = cv2.imread('E:\pink_test.jpg', -1)

# 转换到 HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

cv2.namedWindow('image')
cv2.createTrackbar('hmin', 'image', 0, 255, nothing)
cv2.createTrackbar('smin', 'image', 0, 255, nothing)
cv2.createTrackbar('vmin', 'image', 0, 255, nothing)
cv2.createTrackbar('hmax', 'image', 0, 180, nothing)
switch = '0:OFF\n1:ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

while (1):

    hmin = cv2.getTrackbarPos('hmin', 'image')
    smin = cv2.getTrackbarPos('smin', 'image')
    vmin = cv2.getTrackbarPos('vmin', 'image')
    hmax = cv2.getTrackbarPos('hmax', 'image')
    s = cv2.getTrackbarPos(switch, 'image')

    # 设定橙色的阈值
    lower_orange = np.array([hmin, smin, vmin])
    upper_orange = np.array([hmax, 255, 255])
    # 根据阈值构建掩模
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # 对原图像和掩模进行位运算
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # 显示图像
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    # edges = cv2.Canny(img, minVal_1, maxVal_1)
    # cv2.imshow('edges', edges)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
