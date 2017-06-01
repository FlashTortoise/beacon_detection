#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import beacon_test3 as bt3
import ultrasonic_test2 as ut2

import tortoise as t

import time

t.update_config(TORTOISE_WALK_PERIOD = 0.1)

class TestPatio2(t.Task):
    def __init__(self):
        super(TestPatio2, self).__init__()

        self.beacon_tracing = bt3.beacon_detection()
        self.running_against_wall = ut2.distance_maintaining()
        self.lll = 0

    def step(self):
        if not self.beacon_tracing.flag_beacon_end:
            self.beacon_tracing.step()
            print 1111111
        else:
            if self.lll == 0:
                st1 = time.time()
                while time.time() < st1 + 0.5:
                    l, r = [0.5, 0.3]
                    t.peripheral.wheels.set_lr(r, l)
                self.lll += 1
            else:
                if not self.running_against_wall.flag_ranging_end:
                    self.running_against_wall.step()
                    print 2222222
                else:
                    t.peripheral.wheels.set_lr(0, 0)
                    print 3333333


if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = TestPatio2()
    tttt.walk()
