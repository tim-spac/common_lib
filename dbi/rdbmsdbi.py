#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/dbi/rdbmsdbi.py
# author: Tim Wang
# date: Jan., 2014

"""provide RDBMS database interface, include:
    "LiteDBI" for SQLite3
    "MyDBI" for MySQL
    "MsDBI" for M$SQL
"""

import itertools
from inspect import isfunction, isclass

from common_lib.utl.bufferedprocess import BufferedProcess


def query(conn, sqlscript, rowfactory=None, *args, **kwgs):
    """execute sqlscript with args and kwgs by conn(ection),
        yield iter row throw the rowfactory processing
    """
    curr = conn.cursor()
    curr.execute(sqlscript, *args, **kwgs)
    fields = [f[0] for f in curr.description]
    
    if rowfactory is None:
        factory = None
    elif rowfactory == tuple:
        factory = lambda row: zip(fields, row)
    elif rowfactory == dict:
        factory = lambda row: dict(zip(fields, row))
    elif isfunction(rowfactory):
        factory = rowfactory
    elif isclass(rowfactory):
        factory = lambda row: rowfactory(**dict(zip(fields, row)))
    else:
        factory = None
    
    for row in curr:
        if factory: 
            yield factory(row)
        else:
            yield row

    curr.close()


class _Batch(BufferedProcess):
    """take a buffered batch execute sqlscript, 
        which automated flush/commit
    """
    def __init__(self, conn, sql):
        """define connection and sqlscript by init
        """
        self.conn = conn
        self.sql = sql
        self.curr = self.conn.cursor()
        BufferedProcess.__init__(self, process = self._doing)

    def _doing(self, data):
        """throw connection, usage sql script, process data batch.
        """
        curr = self.conn.cursor()
        curr.executemany(self.sql, data)
        self.conn.commit()
        curr.close()


class Transaction:
    """事务是数据库的一个原子操作，
        但一个事务可能涉及多个表的数据变化:
    """
    def __init__(self, conn, **sqlkwgs):
        """初始化定义数据库连接, 命名SQL-Script
        """
        self.conn = conn
        self.define = dict([
            (name, dict(SQL=sql, buffer=[]))
            for (name, sql) in sqlkwgs
            ])
    
    def append(self, domain, data):
        """向指定的域添加数据
        """
        if domain not in self.define:
            raise ValueError
        self.define[domain]["buffer"].append(data)
    
    def __call__(self):
        """执行一次事务需用命名参数赋值，
        其中参数名应与预先定义的SQL-Script命名相符，
        将其值批量提交给相应SQL-Script
        在实际使用过程中该方法应按需改写
        """
        curr = self.conn.cursor()
        try:
            for todo in self.define.values():
                data, todo["buffer"] = todo["buffer"], []
                curr.executemany(todo["SQL"], data)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
        finally:
            curr.close()


class _DBI:
    """abstract database interface
    """
    def __init__(self, **kwg):
        """init setting knowedges
        """
        self.setting = dict(kwg)
        self.conn = None

    def __enter__(self):
        """enter with statement
        """
        self.open()
        return self

    def __exit__(self, *args):
        """leave with statement
        """
        self.close()

    def open(self):
        """abstract open interface
            inherit, usage special driver make connection
        """
        pass

    def close(self):
        """close interface
        """
        self.conn.close()

    def batch(self, sql):
        """define a buffered batch
        """
        return _Batch(self.conn, sql)

    def query(self, sql, rowfactory=None, *args, **kwgs):
        """transfer current connection and arguments to "query" function
            which iter generate row result
        """
        return query(self.conn, sql, rowfactory, *args, **kwgs)

    def transaction(self, **sqlkwgs):
        return Transaction(self.conn, **sqlkwgs)

    def execute(self, sql, *args, **kwgs):
        """execute SQL script statement immediately
        """
        curr = self.conn.cursor()
        curr.execute(sql, *args, **kwgs)
        self.conn.commit()
        curr.close()

