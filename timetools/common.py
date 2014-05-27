#!/usr/bin/env python
# coding: utf-8
# 
# filename: common_lib/timetools/common.py
# author: Tim Wang
# date: Dec., 2013

""" datetime/time tools collection
"""

import datetime
import time


TZ = time.timezone
TIMESTAMP = time.time()
NOW = datetime.datetime.now()
TODAY = datetime.date.today()

DT_MICROSECOND = datetime.timedelta(microseconds=1)
DT_SECOND = datetime.timedelta(seconds=1)
DT_MINUTE = 60 * DT_SECOND
DT_HOUR = 60 * DT_MINUTE
DT_DAY = datetime.timedelta(days=1)
MID_NIGHT = datetime.time(0, 0, 0)
DATETIMEBASE = datetime.datetime(1970, 1, 1)

ISODATE = "%Y-%m-%d"
ISOTIME = "%H:%M:%S"
ISODATETIME = ISODATE+' '+ISOTIME
CMPDATE = "%Y%m%d"
CMPTIME = "%H%M%S"
CMPDATETIME = CMPDATE+CMPTIME


def date2datetime(var):
    """convert the date var to datetime"""
    return datetime.datetime.combine(var, MID_NIGHT)
