from collections import deque


def run_n_time_flag(self, distinct_name, time=1):
    """
    >>> class Something(object):
    ...     def hello(self):
    ...         print '#'*10,
    ...         if run_n_time_flag(self, 'one',time=5):
    ...             print 'executed',
    ...         print 'something'

    >>> s = Something()

    >>> for i in range(20):
    ...     s.hello()

    """
    if getattr(self, '_execute_record', None) is None:
        setattr(self, '_execute_record', {})

    rec = getattr(self, '_execute_record')

    if rec.get(distinct_name, None) is None:
        rec[distinct_name] = time

    if rec[distinct_name] > 0:
        rec[distinct_name] -= 1
        return True
    else:
        return False


class StepManager(object):
    def __init__(self):
        self.task = None

    def add(self, task):
        if callable(task):
            self.task = task

    def remove(self):
        self.task = None

    def need_step(self):
        return True if self.task is not None else False

    def step(self):
        return self.task()


if __name__ == '__main__':
    class TestStepManager(object):
        def __init__(self):
            self.stepm = StepManager()
            self.executed_count = 0

        def step(self):
            if self.stepm.need_step():
                self.stepm.step()
                self.stepm.remove()
                return

            print 'raw running'
            if self.executed_count == 5:
                def other_fun():
                    print 'other fun run'
                self.stepm.add(other_fun)

            self.executed_count += 1

    t = TestStepManager()
    for i in range(10):
        t.step()


