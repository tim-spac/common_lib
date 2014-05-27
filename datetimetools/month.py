#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/datetimetools/month.py
# author: Tim Wang
# date: Jan., 2014

"""month module's Month class is for compute period
    month1stday return the 1st. day of the month which include given day
"""
import datetime

from common_lib.datetimetools.common import DT_DAY


def month1stday(dtvar):
    """return the datetime's month's datetime start point
    """
    return datetime.date(dtvar.year, dtvar.month, 1)

    
class Month(object):
    """given any a day in the month, generate days in the month,
        and adjust by given number goto another month
    """
    def __init__(self, innerdt=datetime.date.today(), fmt="%B %Y"):
        """innerdt is a day during the month,
            "fmt" define the output date str format (by datetime fmt)
        """
        self.days = []
        self.fmt = fmt
        self._initdays(month1stday(innerdt))
        
    def _initdays(self, firstday):
        """init self's days by month's first day
        """
        mn = firstday.month
        self.days = [dt for dt in 
            (firstday + d * DT_DAY for d in xrange(31))
            if dt.month == mn]
    
    def adjust(self, adjustment):
        """adjust month
        """
        dt = self.days[0]
        ym = dt.year * 12 + (dt.month - 1)
        ym = ym + adjustment
        year, month = ym / 12, (ym % 12) + 1
        self._initdays(datetime.date(year, month, 1))
    
    def __str__(self, fmt=None):
        """string
        """
        return self.days[0].strftime(fmt or self.fmt)

    def daterange(self):
        """return self's first day and last day
        """
        return (self.days[0], self.days[-1])

    def strdaterange(self, fmt=None):
        """return self.daterange's string
        """
        return "%s ~ %s" % (
            self.days[0].strftime(fmt or self.fmt), 
            self.days[-1].strftime(fmt or self.fmt)
            )
