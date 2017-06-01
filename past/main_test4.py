#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import beacon_test4 as bt14
import beacon2_test2 as bt22
import beacon3_test2 as bt32
import ultrasonic_test4 as ut4

import cv2
import numpy as np

import tortoise as t

import turning as turn

import time

t.update_config(TORTOISE_WALK_PERIOD = 0.1)


class TestPatio2(t.Task):
    def __init__(self):
        super(TestPatio2, self).__init__()

        self.beacon1_tracing = bt14.beacon_detection()
        self.beacon2_tracing = bt22.beacon_detection()
        self.beacon3_tracing = bt32.beacon_detection()
        self.running_against_wall = ut4.distance_maintaining()
        self.lll = 0
        self.kkk = 0
        self.ccc = 0
        self.count = 0
        self.count_pic = 0
        self.turn_over1 = False
        self.turn_over2 = False
        self.turning = turn.Turning()

    def step(self):
        print '*'*20

        if not self.beacon1_tracing.flag_beacon_end1:
            self.beacon1_tracing.step()
            # print self.beacon1_tracing.flag_beacon_end1
            print 1111111
        else:
            if self.lll == 0:
                st1 = time.time()
                while time.time() < st1 + 0.3:
                    l, r = [0.5, 0.3]
                    t.peripheral.wheels.set_lr(l, r)
                self.lll += 1
            else:
                if not self.running_against_wall.flag_ranging_end:
                    self.running_against_wall.step()
                    # print self.running_against_wall.flag_ranging_end
                    print 2222222
                else:
                    if self.kkk == 0:
                        self.turning.want_degree = -110
                        if self.turn_over1 == False:
                            while self.turn_over1 == False:
                                self.turn_over1 = self.turning.step()
                        self.kkk += 1
                    else:
                        print '-'*20
                        if self.count <= 3:
                            self.count += 1
                            return
                        else:
                            if not self.beacon2_tracing.flag_beacon_end2:
                                self.beacon2_tracing.step()
                                print 3333333
                            else:
                                if self.ccc == 0:
                                    self.turning.want_degree = -200
                                    if self.turn_over2 == False:
                                        while self.turn_over2 == False:
                                            self.turn_over2 = self.turning.step()
                                    self.ccc += 1
                                else:
                                    if self.count <= 6:
                                        self.count += 1
                                        return
                                    else:
                                        if not self.beacon3_tracing.flag_beacon_end3:
                                            self.beacon3_tracing.step()
                                            newname = str(self.count_pic)
                                            newname = newname.zfill(8)
                                            cv2.imwrite(
                                                '/home/pi/ftp/tortoise-mbed/beacon_test/picture/' + newname + '.png',
                                                self.beacon3_tracing.frame)
                                            self.count_pic += 1
                                            print 4444444
                                        else:
                                            t.peripheral.wheels.set_lr(0, 0)
                                            t.p.rxtx.send('team: tortoise')
                                            sys.exit()
                                            while len(t.p.rxtx.recv()) == 0:
                                                print "waiting"
                                            t.peripheral.wheels.set_lr(0.5, 0.5)
                                            print 5555555


if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = TestPatio2()
    tttt.walk()
