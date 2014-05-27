#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/datetimetools/convertor.py
# author: Tim Wang
# date: Jan., 2014

"""通过识别提供的参数的类型，实现的各种"日期时间"数据格式的转换工具
    日期时间的数据格式包括:
        timestamp (unix time, seconds from 1970-1-1 0:00:00),
        time.struct_time (C 语言中的时间结构)
        datetime.datetime
        datetime.date
"""

import re

from common_lib.datetimetools.common import *


DATETIMEITEMSERIAL = ('year', 'month', 'day', 
    'hour', 'minute', 'second', 'microsecond')
COMPACTIONDTPATT = re.compile(r"""
    (?P<date>
        (?P<year>\d{4})
        \D?
        (?P<month>\d{2})
        \D?
        (?P<day>\d{2})
    )
    \D?
    (?P<time>
        (?P<hour>\d{2})
        \D?
        (?P<minute>\d{2})
        \D?
        (?P<second>\d{2})
        (\.(?P<microsecond>\d+))?
    )?
    """, re.I|re.U|re.X)


def regxdatetime(strdt):
    """usage regex parser string to struct_time
    """
    dtitems = COMPACTIONDTPATT.match(strdt).groupdict()
    if not dtitems["time"]:
        dtitems.update(dict(hour=0, minute=0, second=0))
    return datetime.datetime(*[int(dtitems.get(item, 0))
        for item in DATETIMEITEMSERIAL[:-1]])
    


class Convertor:
    """this a convert tools for convert var betwee:
        datetime, date, timestamp(unix-time), struct_time and string
    """
    def __init__(self,
            defaultfmt=FMT_ISO_DATETIME, 
            tmzone=TZ):
        """set the default string datetime format
            and system local time zone
        """
        self.fmt = defaultfmt
        self.tmzone = tmzone
        self.srcfmt = self.fmt

    def setsrcfmt(self, fmt="%Y-%m-%d %H:%M:%S"):
        """set convert string format to be converted"""
        self.srcfmt = fmt

    def timestamp(self, obj=None):
        """return unix timestamp"""
        if obj is None:
            return time.time()
        elif isinstance(obj, datetime.datetime):
            return (obj - DATETIMEBASE).total_seconds() + self.tmzone
        elif isinstance(obj, datetime.date):
            dt = datetime.datetime(obj.year, obj.month, obj.day)
            return (dt - DATETIMEBASE).total_seconds() + self.tmzone
        elif isinstance(obj, time.struct_time):
            return time.mktime(obj)
        elif isinstance(obj, (int, float)):
            return obj
        elif isinstance(obj, str):
            return time.mktime(regxdatetime(obj).timetuple())

    def datetime(self, obj=None):
        """return datetime instance"""
        if obj is None:
            return datetime.datetime.now()
        elif isinstance(obj, datetime.datetime):
            return obj
        elif isinstance(obj, datetime.date):
            return datetime.datetime(obj.year, obj.month, obj.day)
        elif isinstance(obj, time.struct_time):
            return datetime.datetime(year=obj.tm_year,
                    month=obj.tm_mon,
                    day=obj.tm_mday,
                    hour=obj.tm_hour,
                    minute=obj.tm_min,
                    second=obj.tm_sec)
        elif isinstance(obj, (int, float)):
            tm = time.gmtime(obj-self.tmzone)
            return datetime.datetime(year=tm.tm_year,
                    month=tm.tm_mon,
                    day=tm.tm_mday,
                    hour=tm.tm_hour,
                    minute=tm.tm_min,
                    second=tm.tm_sec)
        elif isinstance(obj, str):
            return regxdatetime(obj)

    def date(self, obj=None):
        """return datetime instance"""
        if obj is None:
            return datetime.date.today()
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return datetime.date(obj.year, obj.month, obj.day)
        elif isinstance(obj, time.struct_time):
            return datetime.date(year=obj.tm_year,
                    month=obj.tm_mon,
                    day=obj.tm_mday)
        elif isinstance(obj, (int, float)):
            tm = time.gmtime(obj-self.tmzone)
            return datetime.date(year=tm.tm_year,
                    month=tm.tm_mon,
                    day=tm.tm_mday)
        elif isinstance(obj, str):
            return regxdatetime(obj).date()

    def struct_time(self, obj=None):
        """return a local time.struct_time"""
        if obj is None:
            return time.gmtime(time.time()-self.tmzone)
        elif isinstance(obj, datetime.datetime):
            tm = (obj - DATETIMEBASE).total_seconds()
            return time.gmtime(tm)
        elif isinstance(obj, datetime.date):
            tm = (datetime.datetime(obj.year, obj.month, obj.day) 
                    - DATETIMEBASE).total_seconds()
            return time.gmtime(tm)
        elif isinstance(obj, time.struct_time):
            return obj
        elif isinstance(obj, (int, float)):
            return time.gmtime(obj-self.tmzone)
        elif isinstance(obj, str):
            return regxdatetime(obj).timetuple()

    def str(self, obj=None):
        """return formated string"""
        if obj is None:
            return datetime.datetime.now().strftime(self.fmt)
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.strftime(self.fmt)
        elif isinstance(obj, time.struct_time):
            return time.strftime(self.fmt, obj)
        elif isinstance(obj, (int, float)):
            return time.strftime(self.fmt, time.localtime(obj))
        elif isinstance(obj, str):
            return regxdatetime(obj).strftime(self.fmt)

