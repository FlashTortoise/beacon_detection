import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 62, 202])
    upper_color = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)

    # print contours

    cv2.imshow('img', img)

    cnt = contours[0]
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])

    picture_size = mask.shape

    error_percent = 0.01  # 1%

    down_boundary = picture_size[1] / 2 - picture_size[1] * error_percent
    up_boundary = picture_size[1] / 2 + picture_size[1] * error_percent

    if down_boundary <= cx <= up_boundary:
        # pass
        print 'middle'
    elif cx < down_boundary:
        # turn right
        # pass
        print 'need to turn right'
    else:
        # turn left
        # pass
        print 'need to turn left'

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    # cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()