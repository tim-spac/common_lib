#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/dbi/__init__.py
# author: Tim Wang
# date: Jan., 2014

"""database interface
        provide "LiteDBI", "MyDBI", "MsDBI"
        and "BsdStorage" dict-like file storage
"""

import bsddb
import shelve


class BsdStorage(shelve.BsdDbShelf):
    """storage Key-Value by shelve-bsddb.
        it provide a dict-like storage
    """
    def __init__(self, dbname, keytype):
        self.dbname = dbname
        self.keytype = int if keytype == int else str
        _open = bsddb.rnopen if self.keytype == int else bsddb.hashopen
        self.dbhandle = _open(dbname, 'c')
        shelve.BsdDbShelf.__init__(self, self.dbhandle)
        indexfile = self.dbname+".idx"
        if os.path.isfile(indexfile):
            self._indexes = shelve.BsdDbShelf(bsddb.hashopen(indexfile, 'c'))
        else:
            self._indexes = {}
        
    def __del__(self):
        shelve.BsdDbShelf.sync(self)
        self.dbhandle.close()
        if self._indexes and isinstance(self._indexes, dict):
            indexfile = bsddb.hashopen(self.dbname+".idx", 'c')
            for indexname, indexes in self._indexes.items():
                indexfile[indexname] = indexes

    def __enter__(self):
        return self

    def __exit__(self, *args):
        shelve.BsdDbShelf.sync(self)

    def scanitems(self, filterfunc=None):
        """provide a filter function,
            find object in storage, if filter(obj) is True
        """
        for obj_key, obj in itertools.ifilter(filterfunc, self.iteritems()):
            yield obj_key, obj

    def makeindex(self, indexname, attribname):
        index = {}
        for obj_key, obj in self.iteritems():
            index.setdefault(repr(obj.get(attribname)), set()).add(obj_key)
        self._indexes[indexname] = index

    def findindex(self, indexname, attribvalue):
        return self._indexes.get(indexname, {}).get(repr(attribvalue), set())
    

try:
    from common_lib.dbi.litedbi import LiteDBI
except:
    pass

try:
    from common_lib.dbi.msdbi import MsDBI
except:
    pass

try:
    from common_lib.dbi.mydbi import MyDBI
except:
    pass

try:
    from common_lib.dbi.kvdbi import KvStorage
except:
    pass


def getdbibyconfig(**kwgs):
    setting = dict(kwgs)
    driver = setting.pop("driver")
    if driver in ("MsSQL", "M$SQL"):
        try:
            from common_lib.dbi.msdbi import MsDBI
            return MsDBI(**setting)
        except:
            pass

    elif driver == "MySQL":
        try:
            from common_lib.dbi.mydbi import MyDBI
            return MyDBI(**setting)
        except:
            pass

    elif driver == "SQLite":
        try:
            from common_lib.dbi.litedbi import LiteDBI
            return LiteDBI(**setting)
        except:
            pass

    