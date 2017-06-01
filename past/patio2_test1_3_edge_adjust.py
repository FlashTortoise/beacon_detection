# coding=utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt


#blurred:
#kernel = np.ones((5,5),np.float32)/25
#dst = cv2.filter2D(img,-1,kernel)

#blur = cv2.blur(img,(5,5))

#median = cv2.medianBlur(img,5)

#blur = cv2.bilateralFilter(img,9,75,75)

def nothing(x):
    pass
# 创建一副黑色图像
#img=np.zeros((300,512,3),np.uint8)
img = cv2.imread('E:\stone.jpg',0)

cv2.namedWindow('image')
cv2.createTrackbar('minVal','image',0,300,nothing)
cv2.createTrackbar('maxVal','image',0,300,nothing)
#cv2.createTrackbar('B','image',0,255,nothing)
switch='0:OFF\n1:ON'
cv2.createTrackbar(switch,'image',0,1,nothing)

while(1):


    minVal=cv2.getTrackbarPos('minVal','image')
    maxVal=cv2.getTrackbarPos('maxVal','image')
    #b=cv2.getTrackbarPos('B','image')
    s=cv2.getTrackbarPos(switch,'image')
    if s==0:
        maxVal_1 = maxVal
        minVal_1 = minVal
    else:
        maxVal_1=maxVal
        minVal_1=minVal

    edges = cv2.Canny(img, minVal_1, maxVal_1)
    cv2.imshow('edges', edges)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # edges = cv2.Canny(img, minVal_1, maxVal_1)
    # plt.subplot(131), plt.imshow(img, cmap='gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # # plt.subplot(132),plt.imshow(blur,cmap = 'gray')
    # # plt.title('Blurred Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(133), plt.imshow(edges, cmap='gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()

cv2.destroyAllWindows()


