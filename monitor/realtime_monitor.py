from common.perf_monitor import PerfMonitor


class RealTimeMonitor(PerfMonitor):
    def __init__(self, interval=10, output=None):
        super(RealTimeMonitor, self).__init__()
        self.interval = interval
        self.daemon = True
        self.output = output

    def run(self):
        pass
