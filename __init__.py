#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/__init__.py
# author: Tim Wang
# date: Jan., 2014


"""common_lib
    is a common lib for python scripts.
"""

__all__ = [
    'readconfig', # read config from INI/YAML file
    "datetimetools", # date/time convert/compute tools
    "dbi", # database interface
    "filetools", # file/path tools
    "net", # net work tools
    "utl", # common utilities
    ]


class DictObj(dict):
    """ make a dict like object, which can access by attribute """
    def __getattr__(self, k):
        return self[k]
    def __setattr__(self, k, val):
        self[k] = val
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, **kwg):
        self.__dict__.update(dict(kwg))
    def __repr__(self):
        return '%s(%r)' % (
            self.__class__.__name__,
            self.items(),
            )


def dictobjtester():
    a = DictObj(name="Tim Wang")
    b = DictObj(mobile="13501104004")
    a.update(b)
    import cPickle as pickle
    c = pickle.loads(pickle.dumps(a))
    c.mobile = "(86)%s" % c.mobile
    print "%r" % c
    


if __name__ == "__main__":
   dictobjtester()
