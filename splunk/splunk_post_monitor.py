import ast
import json
import time

import splunklib.results as results
from common.perf_monitor import PerfMonitor
from common.result_server import SplunkResultServer


class SplunkPostMonitor(PerfMonitor):
    def __init__(self, splunk, queries, starttime=None, endtime=None, result_server=None, name=None, id=None, monitor_type=None):
        super(SplunkPostMonitor, self).__init__(id=id, name=name, monitor_type=monitor_type)
        self.endtime = endtime
        self.starttime = starttime
        self.monitor_type = monitor_type if monitor_type is not None else 'post_monitor'
        self.splunk = splunk
        self.result_server = SplunkResultServer() if result_server is None else result_server
        self.queries = queries

    def run(self):
        kwargs = {"exec_mode": "normal",
                  "adhoc_search_level": "smart",
                  "status_buckets": "300",
                  "max_time": "0",
                  "earliest_time": self.starttime,
                  "latest_time": self.endtime}
        print kwargs
        for query in self.queries:
            job = self.splunk.jobs.create(query, **kwargs)
            while True:
                while not job.is_ready():
                    pass
                if job['isDone'] == '1':
                    break
            print 'eventcount=' + str(job['eventCount'])
            kwargs_getresult = {"count": 0}
            # job_results = job.get_results(**kwargs_getresult)
            hec_data = {}
            lines = ""
            for event in results.ResultsReader(job.results(**kwargs_getresult)):
                try:
                    json.loads(event['_raw'])
                    event_body = ast.literal_eval(event['_raw'])
                except ValueError:
                    event_body = {'log': event['_raw']}

                event_body['uuid'] = str(self.monitor_id)
                event_body['test_id'] = str(self.monitor_id)
                # self.logger.info("event = %s", event)
                # hec_data['event'] = json.loads(json.dumps(event['_raw']))
                hec_data['event'] = json.dumps(event_body)
                hec_data['source'] = str(self.monitor_id) + '_' + event['source']
                hec_data['host'] = event['host']
                hec_data['sourcetype'] = event['sourcetype']
                hec_data['time'] = time.mktime(time.strptime(event['_time'][:-6], "%Y-%m-%dT%H:%M:%S.%f"))
                lines += json.dumps(hec_data)
                if len(lines) > 900*1024:
                    self.result_server.receive_data(lines)
                    lines = ""
            self.result_server.receive_data(lines)
                # hec_send(self.result_server.url, self.result_server.hec_token, hec_data)
