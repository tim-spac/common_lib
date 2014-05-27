#!/usr/bin/env python
# coding: utf-8
#
# filename: kvdbi.py
# date: Mar., 2014
# author: Tim Wang

"""This module is for Key-Value database interface
"""

import os
import glob
import bsddb
import shelve
import itertools


class KvStorageBase(shelve.BsdDbShelf):
    """this is Key-Value storage Base
    """
    def __init__(self, dbname, keytype=str):
        self.dbname = dbname
        self.keytype = int if keytype == int else str
        _open = bsddb.rnopen if self.keytype == int else bsddb.hashopen
        self.dbhandle = _open(dbname, 'c')
        shelve.BsdDbShelf.__init__(self, self.dbhandle)
        
    def __del__(self):
        """when instance destory, sync and close automated
        """
        shelve.BsdDbShelf.sync(self)
        self.dbhandle.close()
    
    def itervaluesfilter(self, filterfunc=None):
        """provide a filter function,
            find object in storage, if filter(obj) is True
        """
        for obj in itertools.ifilter(filterfunc, self.itervalues()):
            yield obj
    
    def scan(self, **kwgs):
        """scan in stored dict-objects for match kwgs
        """
        filterfunc = None if not kwgs else lambda obj: all([
                obj.get(k) == v for (k, v) in dict(kwgs).iteritems()
                ])
        return self.itervaluesfilter(filterfunc)

    def put(self, obj_key, obj):
        """usage put methord to storage key-value
        """
        self.__setitem__(obj_key, obj)

    def get(self, obj_key, failobj=None):
        """usage get methord to get key-value
        """
        if obj_key in self.keys():
            return self.__getitem__(obj_key)
        else:
            return failobj

    def clear(self):
        self.dbhandle.clear()


class KvStorage(KvStorageBase):
    """extend KvStorageBase, support for indexes
    """
    def __init__(self, dbname, keytype=str):
        KvStorageBase.__init__(self, dbname, keytype)
        self.indexes = {}
        basenamelength = len(self.dbname)
        foundindexfiles = [(name[basenamelength:-4], name)
            for name in glob.glob(self.dbname + ".*.idx")]
        for indexname, indexfile in foundindexfiles:
            self.indexes[indexname] = KvStorageBase(indexfile, keytype=str)

    def makeindex(self, attribname):
        """按指定的属性名称创建/重建索引
            索引按repr(属性值)聚合key集合
            保存在按特定规则命名的KvStorageBase文件中
        """
        indexfile = "%s.%s.idx" % (self.dbname, attribname)
        try:
            os.remove(indexfile)
        except:
            pass
        self.indexes[attribname] = KvStorageBase(indexfile, keytype=str)
        index = {}
        for obj_key, obj in self.iteritems():
            index.setdefault(obj.get(attribname), set()).add(obj_key)
        for attr, keyset in index.items():
            self.indexes[attribname][repr(attr)] = keyset

    def makemixindex(self, *attribnames):
        """按指定的属性名称创建/重建索引
            索引按repr(属性值)聚合key集合
            保存在按特定规则命名的KvStorageBase文件中
        """
        attribname = '-'.join(attribnames)
        indexfile = "%s.%s.idx" % (self.dbname, attribname)
        try:
            os.remove(indexfile)
        except:
            pass
        self.indexes[attribname] = KvStorageBase(indexfile, keytype=str)
        index = {}
        for obj_key, obj in self.iteritems():
            idxkey = tuple([obj.get(attr) for attr in attribnames])
            index.setdefault(idxkey, set()).add(obj_key)
        for attr, keyset in index.items():
            self.indexes[attribname][repr(attr)] = keyset

    def finditemswithindex(self, indexname, *tobefind):
        """find objects by exists attribute index
        """
        if len(tobefind) == 1:
            indexkey = repr(tobefind)
        else:
            indexkey = repr(tuple(tobefind))
        foundedkeys = self.indexes.get(indexname, {}).get(indexkey)
        for obj_key in foundedkeys:
            yield obj_key, self[obj_key]

    def scan(self, **kwgs):
        """组织attr-rule参数，若attr存在于self.indexes, 则优先索引查询
            否则按传统方式进行scan
        """
        scankwgs = dict(kwgs)
        indexusage = {}
        for attr in itertools.ifilter(lambda attr: attr in scankwgs, self.indexes):
            rule = scankwgs[attr]
            indexusage[attr] = self.indexes[attr].get(
                    repr(scankwgs.pop(attr)), 
                    set()
                    )
        if indexusage:
            return itertools.ifilter(
                lambda obj: all([
                        obj.get(k) == v for (k, v) in scankwgs.iteritems()
                        ]),
                (self.get(obj_key)
                    for obj_key in reduce(lambda x, y: x & y, indexusage.values()))
                )
        else:
            filterfunc = None if not scankwgs else lambda obj: all([
                    obj.get(k) == v for (k, v) in scankwgs.iteritems()
                    ])
            return self.itervaluesfilter(filterfunc)


def groupby(iterable, *args):
    """按给定参数(属性名称，或属性名称元组)
        对iterable中的字典对象进行分组
    """
    collector = {}
    attr, args = args[0], args[1:]
    for obj in iterable:
        if isinstance(attr, tuple):
            collector.setdefault(
                repr(tuple(itertools.imap(obj.get, attr))),
                []).append(obj)
        else:
            collector.setdefault(
                repr(obj.get(attr)),
                []).append(obj)
    if args:
        for attr, subiter in collector.items():
            collector[attr] = groupby(subiter, *args)
    return collector


def showcollector(collector, prefix='\t', level=0):
    for k, subcollector in collector.items():
        print prefix*level, eval(k)
        if isinstance(subcollector, dict):
            showcollector(subcollector, prefix, level+1)
        else:
            for obj in subcollector:
                print prefix*(level+1), obj


def tester():
    storage = KvStorage("tester.db")
    
    storage.put("M$SQLSERVER:BILL", dict(
        host='10.156.70.7',
        user='sa',
        password='',
        database='master',
        charset='gb18030',
        ))
    storage.put("M$SQLSERVER:CDR", dict(
        host='10.156.70.7',
        user='sa',
        password='',
        database='boss_cdr',
        charset='gb18030',
        ))
    storage["MySQLSERVER:BILL"] = dict(
        host='192.168.11.59',
        user='root',
        passwd='111111',
        db='bill_cdr',
        charset='utf-8',
        )
    
    storage.makeindex("charset")
    storage.makeindex("database")
    
    grouped = groupby(
        storage.itervalues(), 
        'charset', 
        'database')
    showcollector(grouped)
    print "="*32
    
    grouped = groupby(
        storage.itervalues(), 
        ('charset', 'user'),
        'database')
    showcollector(grouped)
    print "="*32
    
    print "charset: utf-8:"
    for obj in storage.scan(charset='utf-8'):
        print obj
    print "="*32
    
    print "charset: gb18030:"
    for obj in storage.scan(charset='gb18030'):
        print obj
    print "="*32
    
    print "password: :"
    for obj in storage.scan(password=''):
        print obj
    print "="*32
    
    import re
    print "scan key by regex:"
    key_patt = re.compile(r"^.*\:BILL$", re.I|re.U|re.X)
    for obj_key in itertools.ifilter(
            lambda obj_key: key_patt.match(obj_key), 
            storage):
        print obj_key, storage.get(obj_key)
    print "="*32


if __name__ == "__main__":
    tester()
