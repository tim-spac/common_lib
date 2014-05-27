#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/datetimetools/common.py
# author: Tim Wang
# date: Jan., 2014

"""define some CONSTs about datetime
"""

import time
import datetime

DT_DATEBASE = datetime.date(1970, 1, 1)
DT_MIDNIGHT = datetime.time(0, 0, 0)

def datetime2date(dtvar):
    """datetime.datetime to datetime.date
    """
    return dtvar.date()

def date2datetime(dtvar):
    """datetime.date to datetime.datetime
    """
    return datetime.datetime.combine(dtvar, DT_MIDNIGHT)

DATETIMEBASE = date2datetime(DT_DATEBASE)

DT_DAY = datetime.timedelta(days=1)
DT_SECOND = datetime.timedelta(seconds=1)
DT_HOUR = 3600 * DT_SECOND

TZ = time.timezone

FMT_ISO_DATETIME = "%Y-%m-%d %H:%M:%S"

