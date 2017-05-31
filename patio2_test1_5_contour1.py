import cv2
import numpy as np
# 1280

cap = cv2.VideoCapture(0)


while (1):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([145, 45, 150])
    upper_color = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    thresh = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 2)

    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)
    cv2.imshow('img', img)

    M = []
    cx = 0
    cxi = []
    total_area = []

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

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    picture_size = mask.shape

    error_percent = 0.05  # 1%

    left_boundary = picture_size[1] / 2 - picture_size[1] * error_percent
    right_boundary = picture_size[1] / 2 + picture_size[1] * error_percent

    print picture_size[1]
    print cx
    print left_boundary
    print right_boundary

    if left_boundary <= cx <= right_boundary:
        # pass
        print 'middle'
    if cx < left_boundary:
        # turn left
        # pass
        print 'need to turn left'
    if cx > right_boundary:
        # turn right
        # pass
        print 'need to turn right'

    if total_area_n > 100000:
        print 'need to stop'

    print "end\n"
cv2.destroyAllWindows()
