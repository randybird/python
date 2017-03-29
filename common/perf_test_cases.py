from threading import Thread

from perf import timer


class PerfTestCases(Thread):
    def __init__(self, target, thinktime, iterations, pacingtime, event, args, kwargs):
        super(PerfTestCases, self).__init__(target=target, args=args)
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.thinktime = thinktime
        self.iterations = iterations
        self.pacingtime = pacingtime
        self.event = event

    def run(self):
        index = 1
        while True:
            if isinstance(self._target, list):
                for case in self._target:
                    timer.constant_time(self.thinktime)
                    case(*self._args[case], **self._kwargs[case])
            else:
                self._target(*self._args, **self._kwargs)
            timer.constant_time(self.pacingtime)
            # self.event.wait(1)
            if index == self.iterations:
                break
            else:
                index += 1
            print 'event is ' + str(self.event.is_set())
            if self.event.is_set():
                print 'event is ' + str(self.event.is_set())
                break
                # logic to gracefully exit
