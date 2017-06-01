import cv2
import numpy as np

frame = cv2.imread('E:/pink3.jpg', -1)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_color = np.array([150, 24, 150])
upper_color = np.array([180, 255, 255])
mask = cv2.inRange(hsv, lower_color, upper_color)
# cv2.imwrite('Final2.jpg',mask)

# im = cv2.imread('E:\Rectangle_shape.jpg')
# imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# ret, thresh = cv2.threshold(mask, 127, 255, 0)

thresh = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)
cv2.imshow('img', img)

M = []
cx = 0
cxi = []
total_area = []

j = 0

for i in range(0, len(contours)):
    M.append(cv2.moments(contours[i]))

for i in range(0, len(contours)):
    if M[i]['m00'] != 0:
        total_area.append(cv2.contourArea(contours[i]))
    else:
        total_area.append(0)
total_area.sort(reverse=True)
area_max = total_area[0]
total_area.pop(0)
total_area_n = sum(total_area)

for i in range(0, len(contours)):
    if M[i]['m00'] != 0:
        if cv2.contourArea(contours[i]) == area_max:
            continue
        else:
            cxi.append(int(M[i]['m10'] / M[i]['m00'] * cv2.contourArea(contours[i]) / total_area_n))
    else:
        cxi.append(0)

for i in range(0, len(cxi)):
    cx = cxi[i] + cx

print total_area_n
print cx

k = cv2.waitKey(10000) & 0xFF
# cnt = contours[0]
# M = cv2.moments(cnt)
# cx = int(M['m10']/M['m00'])
# cy = int(M['m01']/M['m00'])
# print cx,cy
# print mask.shape

picture_size = mask.shape

error_percent = 0.05  # 1%

left_boundary = picture_size[1] / 2 - picture_size[1] * error_percent
right_boundary = picture_size[1] / 2 + picture_size[1] * error_percent

print left_boundary
print right_boundary

if left_boundary <= cx <= right_boundary:
    # pass
    print 'middle'
elif cx < left_boundary:
    # turn left
    # pass
    print 'need to turn left'
else:
    # turn right
    # pass
    print 'need to turn right'
