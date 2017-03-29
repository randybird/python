import json
from tinydb import TinyDB, Query
from common.perf_case_result import PerfCaseResult


class PerfTestResult(object):
    def __init__(self, perfdb=None, name=None, id=None):
        if perfdb is not None:
            self.perfdb = perfdb
        elif name:
            self.perfdb = TinyDB(str(name) + '.json')
        elif id:
            self.perfdb = TinyDB(str(id) + '.json')

    def retrieve_result(self, name=None, Print=False):
        if name:
            result = self.perfdb.search(Query().name == name)
        else:
            result = self.perfdb.all()
        if Print:
            print result
        else:
            return result

    def retrieve_summary(self, name=None, value=None):
        if name:
            result = self.perfdb.search(Query().name == name)
        else:
            result = self.perfdb.all()
        summary = {}
        for r in result:
            if r['name'] not in summary:
                summary[r['name']] = PerfCaseResult(r['name'], r)
            else:
                case_result = summary[r['name']]
                case_result.append_result(r)
                summary[r['name']] = case_result
        final_summary = []
        for name, result in summary.iteritems():
            if value:
                result.calc(value)
            else:
                result.calc()
            final_summary.append(result.get_result())
        return final_summary
