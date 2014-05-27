#!/usr/bin/env python
# coding: utf-8
#
# filename: tester.py
# author: Tim Wang
# date: Dec., 2013

from timetools.common import TIMESTAMP
from timetools import convertor 


def tester():
    """ 测试程序
    """
    now = TIMESTAMP
    tsn = convertor.struce_time(now)
    print tsn
    tsm = convertor.timestamp(tsn)
    print convertor.date(tsn)
    print tsm
    dtr = convertor.datetime(now)
    print convertor.datetime(tsn)
    print dtr
    print convertor.timestamp(dtr)
    print convertor.struce_time(dtr)


if __name__ == "__main__":
    tester()
