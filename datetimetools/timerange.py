#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/datetimetools/timerange.py
# author: Tim Wang
# date: Jan., 2014

"""TimeRange class is an object 
    include two important attribute: bgntime/endtime
    which mark start/ended time point,
    it's base of "CDR", "Conference".. and so on.
"""

from math import ceil
from copy import deepcopy


BEFORE, PREOVER, SUPEROVER, EQURE, SUBOVER, POSTOVER, AFTER = range(-3, 7)


class TimeRange(object):
    """a time range from start to ended
    """
    def __init__(self, bgntime, endtime, **kwg):
        """init start/ended time point and extend attributes
        """
        self.__dict__ = dict(
                **kwg
                )
        self.bgntime = bgntime
        self.endtime = endtime

    def duration(self):
        """duration of start / ended
        """
        return (self.endtime - self.bgntime).total_seconds()

    def minutes(self, keeper=0):
        """minutes of start / ended, keeper keeps bits after float point
        """
        _minutes = round(self.duration()/60, 2)
        if keeper == 0:
            return int(ceil(_minutes))
        elif keeper == 1:
            return .1 * ceil(int(10 * _minutes))
        else:
            return _minutes

    def __cmp__(self, another):
        """compare with another's bgntime/endtime
        """
        return cmp((self.bgntime, self.endtime), 
            (another.bgntime, another.endtime))

    def broken(self, timepoint):
        """split by a time point
        """
        if timepoint <= self.bgntime:
            return None, self
        elif self.endtime <= timepoint:
            return self, None
        else:
            tr0 = deepcopy(self)
            tr0.endtime = timepoint
            tr1 = deepcopy(self)
            tr1.bgntime = timepoint
            return tr0, tr1

    def cross_cmp(self, another):
        """compare with another, check cross statue
        """
        if self.bgntime == another.bgntime \
                and another.endtime == self.endtime:
            statue = EQURE
        
        elif another.endtime <= self.bgntime:
            statue = BEFORE
        elif self.endtime <= another.bgntime:
            statue = AFTER
            
        elif another.bgntime <= self.bgntime \
                and self.endtime <= another.endtime:
            statue = SUPEROVER
        elif self.bgntime <= another.bgntime \
                and another.endtime <= self.endtime:
            statue = SUBOVER
        
        elif another.bgntime < self.bgntime:
            statue = PREOVER
        elif self.endtime < another.endtime:
            statue = POSTOVER
        return statue