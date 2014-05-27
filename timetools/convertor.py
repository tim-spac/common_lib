#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/timetools/convertor.py
# author: Tim Wang
# date: Dec., 2013

""" this module collect many convert tools to transfer :
    timestamp(unix-time), struct_time, datetime/time
"""

import time
import datetime as DT
import re

from common import TZ, DATETIMEBASE, MID_NIGHT
from common import ISODATETIME


DATETIME_REGX = re.compile(r"""
    (?P<year>[12]\d{3})
    [-,\.,/]?
    (?P<month>(0?\d|1[0-2]))
    [-,\.,/]?
    (?P<day>(0?[1-9]|[12]\d|3[0,1]))
    \s*
    (?P<hour>([0,1]\d|2[0-3]))
    :?
    (?P<minute>([0-5]?\d))
    :?
    (?P<second>([0-5]?\d))
    (?P<microsecond>\.\d*)?
    """, re.I|re.U|re.X)

print ISO_DATE_REGX.match("20140131 125332.020").groupdict()


def struce_time(var):
    """convert argument to time.struct_time
    """
    if isinstance(var, (float, int)):
        return time.localtime(var)
    elif isinstance(var, DT.datetime):
        return time.gmtime((var - DATETIMEBASE).total_seconds())
    elif isinstance(var, DT.date):
        return time.gmtime((DT.datetime(var.year, var.month, var.day)
                - DATETIMEBASE).total_seconds())


def timestamp(var):
    """convert argument to unix-timestamp
    """
    if isinstance(var, time.struct_time):
        return time.mktime(var)
    elif isinstance(var, DT.date):
        return (DT.datetime.combine(var, MID_NIGHT)
            - DATETIMEBASE).total_seconds() + TZ
    elif isinstance(var, DT.datetime):
        return (var - DATETIMEBASE).total_seconds() + TZ


def datetime(var):
    """convert argument to datetime.datetime
    """
    if isinstance(var, (float, int)):
        return DT.datetime.utcfromtimestamp(var - TZ)
    elif isinstance(var, time.struct_time):
        return DT.datetime.utcfromtimestamp(time.mktime(var) - TZ)
    elif isinstance(var, DT.date):
        return DT.datetime.combine(var, MID_NIGHT)


def date(var):
    """convert argument to datetime.date
    """
    if isinstance(var, (float, int)):
        return DT.datetime.utcfromtimestamp(var - TZ).date()
    elif isinstance(var, time.struct_time):
        return DT.date(var.tm_year, var.tm_mon, var.tm_mday)
    elif isinstance(var, DT.datetime):
        return DT.date()
    

def str(var, fmt=ISODATETIME):
    """convert argument to string
    """
    if isinstance(var, (int, float)):
        return time.strftime(fmt, time.localtime(var))
    elif isinstance(var, time.struct_time):
        return time.strftime(fmt, var)
    elif isinstance(var, (DT.date, DT.datetime)):
        return var.strftime(fmt)

