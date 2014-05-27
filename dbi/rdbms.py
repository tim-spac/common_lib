#!/usr/bin/env python
# coding: utf-8
#
# author: Tim Wang
# date: May, 2014
# filename: common_lib/dbi/rdbms.py
# varsion: 3.0.0

""" common_lib/dbi/rdbms.py is an abstract database interface liberary
"""

class Query:
    
    def __init__(self, conn, sqlscript, rowfactory):
        self.curr = conn.cursor()
        self.sql = sqlscript
        self._rowfactory = rowfactory
        self.fields = None
    
    def rowfactory(self, row):
        if not self._rowfactory:
            return row
        
        row_tuple = zip(self.fields, row)
        if self._rowfacotry == tuple:
            return row_tuple
        
        row_dict = dict(row_tuple)
        if self._rowfacotry == dict:
            return row_dict
        
        return self._rowfactory(**row_dict)
        
    def __call__(self, *args, **kwgs):
        self.curr.execute(self.sql, *args, **kwgs)
        self.fields = [f[0] for f in curr.descriptions]

    def __iter__(self):
        for row in self.curr:
            yield self.rowfactory(row)
            

class _DBI:
    """abstract database interface"""
    def __init__(self, **kwgs):
        self.setting = dict(kwgs)
        self.conn = None
    
    def open(self):
        """make connection to RDBMS server with special setting, 
            store connection instance with self.conn
        """
        pass

    def close(self):
        """close connection with RDBMS server
        """
        pass
    
    def query(self, sqlscript, rowfactory=None):
        return Query(self.conn, sqlscript, rowfactory=rowfactory)

    def batch(self, sql):
        return Batch(self.conn, sql)

    def execute(self, sqlscript):
        self.conn.execute(sqlscript)
        self.conn.commit()
