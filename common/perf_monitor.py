import uuid
from threading import Thread


class PerfMonitor(Thread):
    def __init__(self, id=None, name=None, monitor_type=None):
        super(PerfMonitor, self).__init__()
        self.monitor_id = uuid.uuid4() if id is None else id
        self.name = name if name is not None else self.monitor_id
        types = ('post_monitor', 'realtime_monitor', 'checkpoint_monitor')
        if monitor_type and monitor_type in types:
            self.monitor_type = monitor_type
        else:
            self.monitor_type = 'unknown'

    def run(self):
        pass

