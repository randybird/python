
import copy
import types
from threading import Event
from common.perf_test_cases import PerfTestCases


def check_kwargs(kwargs):
    if 'perftest' not in kwargs:
        kwargs['pertest'] = None
    if 'block' not in kwargs:
        kwargs['block'] = None
    return kwargs


class PerfTestScenario(object):
    def __init__(self, iteration=1, concurrency=1, timeout=None):
        self.iteration = iteration
        self.concurrency = concurrency
        self.timeout = timeout
        self.testcases = []
        self.testcases_names = []
        self.args = {}
        self.kwargs = {}
        self.rampuptime = 10
        self.thinktime = 100
        self.pacingtime = 200

    def set_iteration(self, count):
        self.iteration = count
        return self

    def set_concurrency(self, count):
        self.concurrency = count
        return self

    def set_timeout(self, minutes):
        self.timeout = minutes
        return self

    def add_testcase(self, testcase, *args, **kwargs):
        if isinstance(testcase, types.ModuleType):
            kwargs = check_kwargs(kwargs)
            # all_attrs = dir(testcase)
            r = open(getattr(testcase, '__file__')[0:-1])
            t = ast.parse(r.read())
            # inspect = ast.dump(t)
            for e in t.body:
                if type(e) is ast.FunctionDef:
                    decorator_list = e.decorator_list
                    func_name = e.name
                    a = getattr(testcase, func_name)
                    for d in decorator_list:
                        if type(d) is ast.Call:
                            for keyword in d.keywords:
                                if keyword.arg == 'block' and keyword.value.id == 'True':
                                    if 'block' not in kwargs:
                                        print "ERROR: block is not set correctly"
                                        return
                                    if callable(a) and isinstance(a, types.FunctionType) and func_name != 'transaction':
                                        self.testcases.append(a)
                                        self.args[a] = args
                                        self.kwargs[a] = kwargs
                                        break
                                else:
                                    break
                    if a not in self.testcases:
                        self.testcases.append(a)
                        self.args[a] = args
                        temp_kwargs = copy.copy(kwargs)
                        temp_kwargs['block'] = None
                        self.kwargs[a] = temp_kwargs
        elif callable(testcase):
            self.testcases.append(testcase)
            self.args[testcase] = args
            kwargs = check_kwargs(kwargs)
            self.kwargs[testcase] = kwargs
        return self

    def start(self):
        test_workers = []
        event = Event()
        for x in range(self.concurrency):
            test_worker = PerfTestCases(self.testcases, self.thinktime, self.iteration,
                                        self.pacingtime, event, self.args, self.kwargs)
            test_workers.append(test_worker)
        for test_worker in test_workers:
            test_worker.start()
        for worker in test_workers:
            worker.join(self.timeout)
            worker.event.set()
        for worker in test_workers:
            worker.join()
