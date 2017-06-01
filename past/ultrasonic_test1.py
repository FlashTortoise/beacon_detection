#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tortoise as t
# import recording

import time

from tortoise.sensors import Ranging as Dis

# unit: mm, min: 50mm, max: 500mm
t.update_config(TORTOISE_WALK_PERIOD = 0.1)

d = Dis()

def distance():
    # while True:
    st = time.time()
    distance_set_raw = [0, 0, 0, 0, 0]
    for i in range(5):
        print "%9.0f" % d.get(i),
        distance_set_raw[i] = d.get(i)
    ed = time.time()
    print '   ', st - ed
    # time.sleep(1)
    return distance_set_raw


# t.update_config(TORTOISE_WALK_PERIOD = 0.1)

class distance_maintaining(t.Task):
    def __init__(self):
        super(distance_maintaining, self).__init__()
        self.flag_ranging_end = False

    def step(self):

        distance_set = distance()
        distance_front = distance_set[2]
        distance_front_left = distance_set[4]
        distance_front_right = distance_set[0]
        distance_rear_left = distance_set[3]
        distance_rear_right = distance_set[1]

        lower_boundary = 150
        upper_boundary = 250
        error_distance = 10

        count = 0

        if distance_front_left > 5000 or distance_rear_left > 5000:
            l, r = [0, 0]
        else:
            if distance_front_left == 0 and 10 < distance_rear_left < upper_boundary:
                l, r = [0.1, 0.5]
            elif distance_front_left == 0 and distance_rear_left > upper_boundary:
                l, r = [0.1, 0.5]
            elif distance_front_left == 0 or distance_rear_left == 0:
                l, r = [0, 0]
            else:
                # if 200 < distance_front < 800:
                #     l, r = [0.7, 0.2]
                # else:
                    if distance_front_left < lower_boundary and distance_rear_left < lower_boundary:
                        l, r = [0.5, 0.2]
                    elif distance_front_left > upper_boundary and distance_rear_left > upper_boundary:
                        if distance_front_left > 1000 and distance_rear_left > 1000:
                            l, r = [0.2, 0.9]
                        elif 500 < distance_front_left < 1000 or 500 < distance_rear_left < 1000:
                            l, r = [0.2, 0.5]
                        else:
                            st1 = time.time()
                            while time.time() < st1+0.5:
                                l, r = [0.4, 0.4]
                                t.peripheral.wheels.set_lr(r, l)
                            l, r =[0.1, 0.5]
                    elif distance_front_left < lower_boundary and distance_rear_left > lower_boundary:
                        l, r =[0.5, 0.2]
                    elif distance_front_left > lower_boundary and distance_rear_left < lower_boundary:
                        if distance_front_left > 500 or distance_rear_left < 10:
                            l, r = [0.1, 0.5]
                        else:
                            st1 = time.time()
                            while time.time() < st1+0.5:
                                l, r = [0.4, 0.4]
                                t.peripheral.wheels.set_lr(r, l)
                            l, r =[0.1, 0.5]
                    elif distance_front_left < upper_boundary and distance_rear_left > upper_boundary:
                        st1 = time.time()
                        while time.time() < st1 + 0.5:
                            l, r = [0.4, 0.4]
                            t.peripheral.wheels.set_lr(r, l)
                        l, r = [0.5, 0.2]
                    elif distance_front_left > upper_boundary and distance_rear_left < upper_boundary:
                        l, r = [0.1, 0.6]
                    else:
                        if distance_front_left < (distance_rear_left - error_distance) or distance_rear_left > (distance_front_left + error_distance):
                            l, r = [0.5, 0.2]
                        elif distance_front_left > (distance_rear_left+error_distance) or distance_rear_left < (distance_front_left-error_distance):
                            l, r = [0.2, 0.5]
                        else:
                            l, r = [0.4, 0.4]

        if distance_front < lower_boundary:
            l, r = [0, 0]
            self.flag_ranging_end = True

        print "left" + str(l)
        print "right" + str(r)

        # if distance_front<lower_boundary:
        #     #rotate the car 90 degree clockwise
        #     count += 1

        t.peripheral.wheels.set_lr(r, l)


if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = distance_maintaining()
    tttt.walk()
