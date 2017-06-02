import logging

import tool
import tortoise as t
from beacon_detect import BeaconDetectionTask
from turning import Turning
from wall_following_task_indoor import PlanterWallFollower

t.update_config(TORTOISE_WALK_PERIOD=0.1)
logging.getLogger('tortoise.p').setLevel(logging.WARN)


class Patio2(t.Task):
    logger = logging.getLogger('tortoise.patio2')

    def __init__(self):
        super(Patio2, self).__init__()
        self.beacon_task = BeaconDetectionTask()
        self.step_manager = tool.StepManager()
        self.turning_task = Turning()
        self.wall_following_task = PlanterWallFollower()

    def step(self):
        if self.step_manager.need_step():
            self.step_manager.step()
            return

        if not self.beacon_task.done:
            self.beacon_task.step()
            print 'Area: {:9.1f}, direction: {:8s}'.format(
                self.beacon_task.beacon_area, self.beacon_task.turn_dir)

            self.set_speeds_from_beacon_flag(self.beacon_task.turn_dir)
        elif tool.run_n_time_flag(self, 'asdfaw'):
            print 'First turning'
            self.turning_task.reset(-110)
            self.step_manager.add_blocking(
                self.turning_task.step,
                lambda: not self.turning_task.finish_flag
            )
        elif not self.wall_following_task.done:
            self.wall_following_task.step()
        elif tool.run_n_time_flag(self, 'asfawefoijwj'):
            print 'Second turning'
            self.turning_task.reset(-110)
            self.step_manager.add_blocking(
                self.turning_task.step,
                lambda: not self.turning_task.finish_flag
            )
            def reset_beacon_step():
                self.beacon_task.done = False
            self.step_manager.add(reset_beacon_step)
        elif not self.beacon_task.done:
            self.beacon_task.step()
            print 'Area: {:9.1f}, direction: {:8s}'.format(
                self.beacon_task.beacon_area, self.beacon_task.turn_dir)

            self.set_speeds_from_beacon_flag(self.beacon_task.turn_dir)
        elif tool.run_n_time_flag(self, 'yogokut'):
            print 'Second turning'
            self.turning_task.reset(-200)
            self.step_manager.add_blocking(
                self.turning_task.step,
                lambda: not self.turning_task.finish_flag
            )

            def reset_beacon_step():
                self.beacon_task.done = False
            self.step_manager.add(reset_beacon_step)
        elif not self.beacon_task.done:
            self.beacon_task.step()
            print 'Area: {:9.1f}, direction: {:8s}'.format(
                self.beacon_task.beacon_area, self.beacon_task.turn_dir)

            self.set_speeds_from_beacon_flag(self.beacon_task.turn_dir)




    def set_speeds_from_beacon_flag(self, flag):
        if flag == 'right':
            t.p.wheels.lr = 0.4, 0.1
        elif flag == 'left':
            t.p.wheels.lr = 0.1, 0.4
        else:
            t.p.wheels.lr = 0.4, 0.4

if __name__ == '__main__':
    tttt = t.Tortoise()
    tttt.task = Patio2()
    tttt.walk()
