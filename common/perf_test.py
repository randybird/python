import json
import os
import socket
import uuid
import time
from datetime import datetime

from splunklib import client
from tinydb.storages import MemoryStorage

from common.perf_test_result import PerfTestResult
from result_server import SplunkResultServer
from splunk.splunk_checkpoint_monitor import SplunkCheckpointMonitor
from tinydb import TinyDB, Query

from splunk.splunk_post_monitor import SplunkPostMonitor


def get_default_result_server():
    return SplunkResultServer()


class PerfTest(object):
    def __init__(self, name=None):
        self.id = str(uuid.uuid4())
        self.name = name if name is not None else self.id
        self.result_server = None
        self.post_monitor = None
        self.starttime = time.time()
        self.endtime = None
        self.collection_starttime = None
        self.collection_endtime = None
        self.perfdb = TinyDB(storage=MemoryStorage)
        # self.perfdb.purge()
        self.result = PerfTestResult(perfdb=self.perfdb)
        self.context = None
        self.host = socket.gethostname()

    def set_post_monitor(self, monitor=None):
        self.post_monitor = monitor

    def set_result_server(self, splunk_result_server=None):
        self.result_server = splunk_result_server if splunk_result_server is not None else get_default_result_server()

    def set_collection_time(self, start, end):
        self.collection_starttime = start
        self.collection_endtime = end
        print 'set collection_start: ' + str(self.collection_starttime)
        print 'set collection_end: ' + str(self.collection_endtime)

    def set_context(self, perf_context):
        self.context = perf_context

    def create_checkpoint_monitor(self, splunk, spl):
        return SplunkCheckpointMonitor(start_time=time.time(), splunk=splunk, interval=300, parent=self, spl=spl)

    def create_post_monitor(self, splunk, queries):
        return SplunkPostMonitor(id=self.id, splunk=splunk, queries=queries)

    def get_summary_result(self):
        if self.endtime is None:
            self.endtime = time.time()
        duration = self.endtime - self.starttime
        perf_result = self.result.retrieve_summary()
        if self.context:
            result = self.context.get_context()
        else:
            result = {}
        result['test_metrics'] = perf_result
        result['duration'] = duration
        return result

    def populate_result(self, data, source=None, host=None, sourcetype=None, index=None):
        data['uuid'] = str(self.id)
        data['test_id'] = str(self.id)
        print data
        hec_data = {'event': data}
        if source:
            hec_data['source'] = source
        hec_data['host'] = self.host if host is None else host
        if sourcetype:
            hec_data['sourcetype'] = sourcetype
        if index:
            hec_data['index'] = index
        hec_data['time'] = time.time()
        if self.result_server:
            self.result_server.receive_data(json.dumps(hec_data))
        self.cleanup()
        print 'collection_start: ' + str(self.collection_starttime)
        print 'collection_end: ' + str(self.collection_endtime)
        if self.post_monitor is not None:
            if self.post_monitor.starttime is None:
                self.post_monitor.starttime = self.collection_starttime if self.collection_starttime is not None else self.starttime
            if self.post_monitor.endtime is None:
                self.post_monitor.endtime = self.collection_endtime if self.collection_endtime is not None else self.endtime
            self.post_monitor.start()
            self.post_monitor.join()

    def cleanup(self):
        fname = self.name + ".json"
        if os.path.isfile(fname):
            os.remove(fname)
