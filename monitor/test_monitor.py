from monitor.realtime_monitor import RealTimeMonitor


class TestMonitor(RealTimeMonitor):
    def __init__(self, interval=None, output=None):
        super(TestMonitor, self).__init__(interval, output)

    def test(self):
        print self.interval
