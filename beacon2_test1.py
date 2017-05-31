#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import numpy as np
# 1280*720

import tortoise as t
#import recording

import turning as turn

import time

t.update_config(TORTOISE_WALK_PERIOD = 0.1)
eye = t.peripheral.eye

class beacon_detection(t.Task):
    def __init__(self):
        super(beacon_detection, self).__init__()
        self.flag_beacon_end2 = False
        self.turn_over = False
        self.turning = turn.Turning()

    def step(self):

        flag = 0
        frame = eye.see()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_color = np.array([150, 80, 80])
        upper_color = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)

        thresh = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # img = cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)
        # cv2.imshow('img', img)

        m = []
        cx = 0
        cxi = []
        total_area = []

        for i in range(0, len(contours)):
            m.append(cv2.moments(contours[i]))

        for i in range(0, len(contours)):
            if m[i]['m00'] != 0:
                total_area.append(cv2.contourArea(contours[i]))
            else:
                total_area.append(0)
        total_area.sort(reverse=True)
        area_max = total_area[0]
        total_area.pop(0)
        total_area_n2 = sum(total_area)

        for i in range(0, len(contours)):
            if m[i]['m00'] != 0:
                if cv2.contourArea(contours[i]) == area_max:
                    continue
                else:
                    cxi.append(int(m[i]['m10'] / m[i]['m00'] * cv2.contourArea(contours[i]) / total_area_n2))
            else:
                cxi.append(0)

        for i in range(0, len(cxi)):
            cx = cxi[i] + cx

        # k = cv2.waitKey(5) & 0xFF
        # if k == 27:
        #     break

        picture_size = mask.shape

        error_percent = 0.05  # 1%

        left_boundary = picture_size[1] / 2 - picture_size[1] * error_percent
        right_boundary = picture_size[1] / 2 + picture_size[1] * error_percent

        # print picture_size[1]
        # print cx
        # print left_boundary
        # print right_bou

        # if self.flag_beacon_end == True:
        #     l, r = [0, 0]
        # else:
        if total_area_n2 > 140000:
                st1 = time.time()
                while time.time() < st1 + 0.4:
                    l, r = [0.4, 0.4]
                    t.peripheral.wheels.set_lr(l, r)
                self.turning.want_degree = -110
                if self.turn_over == False:
                    while self.turn_over == False:
                        self.turn_over = self.turning.step()
                l, r = [0, 0]
                self.flag_beacon_end2 = True
        else:
            if left_boundary <= cx <= right_boundary:
                # pass
                # print 'middle'
                l, r=[0.4, 0.4]
            if cx < left_boundary:
                # turn left
                # pass
                # print 'need to turn left'
                l, r = [0.1, 0.4]
            if cx > right_boundary:
                # turn right
                # pass
                # print 'need to turn right'
                l, r = [0.4, 0.1]

        print "left"+str(l)
        print "right"+str(r)
        print "total_area_n2"+str(total_area_n2)

        t.peripheral.wheels.set_lr(l, r)

if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = beacon_detection()
    tttt.walk()