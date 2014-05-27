#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/dbi/litedbi.py
# author: Tim Wang
# date: Jan., 2014

"""provide RDBMS database interface
    "LiteDBI" for SQLite3
"""

import decimal
import sqlite3

from common_lib.dbi.rdbmsdbi import _DBI


DEC = decimal.Decimal

def adapt_decimal(d):
    return str(d)

def convert_decimal(s):
    return DEC(s)

# Register the adapter
sqlite3.register_adapter(DEC, adapt_decimal)

# Register the converter
sqlite3.register_converter("decimal", convert_decimal)


class LiteDBI(_DBI):
    """for "SQLite3" RDBMS Interface
    """
    def open(self):
        self.conn = sqlite3.connect(
            database = self.setting.get('database', ':memory:'),
            )
    
    def execute(self, sql, *args, **kwgs):
        self.conn.executescript(sql, *args, **kwgs)
        self.conn.commit()

