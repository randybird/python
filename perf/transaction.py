import time

import functools
from tinydb import TinyDB
from common.perf_monitor import PerfMonitor


# def transaction(name=None, perftest=None, block=None):
#     def real_transaction(f):
#         def wrapper(*args, **kwargs):
#             start_time = time.time()
#             f(*args, **kwargs)
#             end_time = time.time()
#             duration = end_time - start_time
#             if perftest:
#                 db = perftest.perfdb
#                 db.insert({'time': end_time, 'name': name, 'duration': duration})
#             else:
#                 print name + "_duration: " + str(duration)
#             if block:
#                 if isinstance(block, PerfMonitor):
#                     block.start()
#                     block.join()
#         return wrapper
#     return real_transaction


# reference but not used any more

# def transaction(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         name = kwargs.pop('name', None)
#         perftest = kwargs.pop('perftest', None)
#         block = kwargs.pop('block', None)
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         duration = end_time - start_time
#         if perftest:
#             db = perftest.perfdb
#             db.insert({'time': end_time, 'name': name, 'duration': duration})
#         else:
#             print name + "_duration: " + str(duration)
#         if block:
#             if isinstance(block, PerfMonitor):
#                 block.start()
#                 block.join()
#         return result
#     return decorated


def transaction(func=None, name=None, perftest=None, block=None):
    if func is None:
        return functools.partial(transaction, name=name, perftest=perftest, block=block)

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        if 'name' in kwargs:
            name = kwargs.pop('name', None)
        else:
            name = func.__name__
        if 'perftest' in kwargs:
            perftest = kwargs.pop('perftest', None)
        if 'block' in kwargs:
            # if block is True:
            block = kwargs.pop('block', None)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        if perftest:
            db = perftest.perfdb
            db.insert({'time': end_time, 'name': name, 'duration': duration})
        else:
            print name + "_duration: " + str(duration)
        if block:
            if isinstance(block, PerfMonitor):
                block.start()
                block.join()
        return result

    return decorated
    # def real_trans(func):
    #     # @functools.wraps(func)
    #     def decorated(name=name, perftest=perftest, block=block, *args, **kwargs):
    #         if 'name' in kwargs:
    #             name = kwargs.pop('name', None)
    #         if 'perftest' in kwargs:
    #             perftest = kwargs.pop('perftest', None)
    #         if block is True:
    #             block = kwargs.pop('block', None)
    #         start_time = time.time()
    #         result = func(*args, **kwargs)
    #         end_time = time.time()
    #         duration = end_time - start_time
    #         if perftest:
    #             db = perftest.perfdb
    #             db.insert({'time': end_time, 'name': name, 'duration': duration})
    #         else:
    #             print name + "_duration: " + str(duration)
    #         if block:
    #             if isinstance(block, PerfMonitor):
    #                 block.start()
    #                 block.join()
    #         return result
    #     return decorated
    # return real_trans


#
# _empty = object()  # sentinel value used to control testing
#
#
def dump_ne(expected=None):
    def real_trans(f):
        def decorated(expected=expected, *args, **kwargs):
            print expected
            if expected is None:
                print "None None None"
            # expected = kwargs.pop('expected', None)
            result = f(*args, **kwargs)
            # only print when the result didn't equal expected
            # if expected is not None and expected != result:
            #     print('FAIL: func={}, args={}, kwargs={}'.format(func.__name__, args, kwargs))
            return result

        return decorated

    return real_trans
