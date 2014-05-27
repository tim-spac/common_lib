#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/utl/__init__.py
# author: Tim Wang
# date: Jan., 2014


"""common_lib/utl
    is for utilities
"""

from functools import wraps

def cacheablefunction(func):
    _caches = {}
    @wraps(func)
    def wrap(*args):
        if args not in _caches:
            _caches[args] = func(*args)
        return _caches[args]
    return wrap


__all__ = [
    "bufferedprocess",
    "yamlutil",
    ]
