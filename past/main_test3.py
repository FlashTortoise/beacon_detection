#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import beacon_test4 as bt14
import beacon2_test1 as bt21
import beacon3_test2 as bt32
import ultrasonic_test3 as ut3


import tortoise as t

import time

t.update_config(TORTOISE_WALK_PERIOD = 0.1)

class TestPatio2(t.Task):
    def __init__(self):
        super(TestPatio2, self).__init__()

        self.beacon1_tracing = bt14.beacon_detection()
        self.beacon2_tracing = bt21.beacon_detection()
        self.beacon3_tracing = bt32.beacon_detection()
        self.running_against_wall = ut3.distance_maintaining()
        self.lll = 0

    def step(self):
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
                    if not self.beacon2_tracing.flag_beacon_end2:
                        self.beacon2_tracing.step()
                        print 3333333
                    else:
                        if not self.beacon3_tracing.flag_beacon_end3:
                            self.beacon3_tracing.step()
                            print 4444444
                        else:
                            t.peripheral.wheels.set_lr(0, 0)
                            t.p.rxtx.send('team: tortoise')
                            while len(t.p.rxtx.recv()) == 0:
                                print "waiting"
                            t.peripheral.wheels.set_lr(0.5, 0.5)
                            print 5555555

if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = TestPatio2()
    tttt.walk()
