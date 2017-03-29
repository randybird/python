import json
import sys


class PerfCaseResult(object):
    def __init__(self, name, raw):
        self.name = name
        self.average = None
        self.maximum = None
        self.minimum = None
        self.invocations = 0
        if isinstance(raw, list):
            self.raw = raw
        else:
            self.raw = [raw]

    def append_result(self, result):
        self.raw.append(result)

    def calc(self, value='duration'):
        sum_value = 0
        max_value = 0
        min_value = sys.float_info.max
        self.invocations = len(self.raw)
        for case in self.raw:
            number = case[value]
            sum_value += number
            if number < min_value:
                min_value = number
            if number > max_value:
                max_value = number
        self.maximum = max_value
        self.minimum = min_value
        self.average = sum_value * 1.0 / self.invocations

    def get_result(self):
        result = {
            'name': self.name,
            'invocations': self.invocations,
            'average': self.average,
            'maximum': self.maximum,
            'minimum': self.minimum
        }
        return result
