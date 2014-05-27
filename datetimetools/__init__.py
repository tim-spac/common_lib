#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/datetimetools/__init__.py
# author: Tim Wang
# date: Jan., 2014

"""common_lib/datetimetools
    datetime convert/compute tools, include:
        convertor
        month
"""

__all__ = [
    "common", # define some CONSTs
    "timerange", # define TimeRange class
    ]


# convert tools
#    for :
#       timestamp, 
#       struct_time, 
#       datetime, 
#       date, 
#       string, 
from common_lib.datetimetools.dtconvertor import Convertor
DTC = Convertor()
