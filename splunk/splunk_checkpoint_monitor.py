from splunklib import results
from time import time, sleep

from common.perf_monitor import PerfMonitor


class SplunkCheckpointMonitor(PerfMonitor):
    def __init__(self, start_time, splunk, spl, parent=None, result_server=None, name=None, monitor_type=None,
                 timeout=7200, interval=300):
        super(SplunkCheckpointMonitor, self).__init__(name, monitor_type)
        self.start_time = start_time
        self.monitor_type = 'checkpoint_monitor'
        self.splunk = splunk
        self.spl = spl
        self.test_start = None
        self.test_end = time()
        self.parent = parent
        self.timeout = timeout
        self.interval = interval

    def run(self):
        beginning = self.start_time
        while True:
            sleep(self.interval)
            if time() - self.start_time > self.timeout:
                print 'timeout is met, the monitor stopped'
                if self.parent:
                    self.parent.set_collection_time(self.test_start, self.test_end)
                self.return_checkpoint()
                break
            if time() - self.interval > self.start_time:
                beginning = '-'+str(self.interval+30)+'s'
            kwargs = {"exec_mode": "normal",
                      "adhoc_search_level": "smart",
                      "status_buckets": "300",
                      "max_time": "0",
                      "earliest_time": beginning,
                      "latest_time": 'now'}
            if self.test_start:
                sort_option = '| sort - _time'
            else:
                sort_option = '| sort _time'
            job = self.splunk.jobs.create(self.spl + sort_option, **kwargs)
            while True:
                while not job.is_ready():
                    pass
                if job['isDone'] == '1':
                    break
            kwargs_options = {"count": 1}
            if int(job['eventCount']) > 0:
                for result in results.ResultsReader(job.results(**kwargs_options)):
                    if self.test_start is None:
                        self.test_start = result['_time']
                    else:
                        self.test_end = result['_time']
            elif self.test_start:
                if self.parent:
                    self.parent.set_collection_time(self.test_start, self.test_end)
                self.return_checkpoint()
                break
            print 'start_time='+str(self.test_start)+', end_time='+str(self.test_end)

    def return_checkpoint(self):
        output = {
            'start_time': self.test_start,
            'end_time': self.test_end
        }
        return output
