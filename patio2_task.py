import logging

import tortoise as t
from beacon_detect import BeaconDetectionTask

t.update_config(TORTOISE_WALK_PERIOD=0.1)
logging.getLogger('tortoise.p').setLevel(logging.WARN)


class Patio2(t.Task):
    logger = logging.getLogger('tortoise.patio2')

    def __init__(self):
        super(Patio2, self).__init__()
        self.beacon_task = BeaconDetectionTask()

    def step(self):
        self.beacon_task.step()

        print 'Area: {:9.1f}, direction: {:8s}'.format(
            self.beacon_task.beacon_area, self.beacon_task.turn_dir)
        if self.beacon_task.turn_dir == 'right':
            t.p.wheels.lr = 0.4, 0.1
        elif self.beacon_task.turn_dir == 'left':
            t.p.wheels.lr = 0.1, 0.4
        else:
            t.p.wheels.lr = 0.4, 0.4

if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = Patio2()
    tttt.walk()
