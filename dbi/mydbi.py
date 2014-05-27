#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/dbi/mydbi.py
# author: Tim Wang
# date: Jan., 2014

"""provide RDBMS database interface
    "MyDBI" for MySQL
"""

import MySQLdb

from common_lib.dbi.rdbmsdbi import _DBI


class MyDBI(_DBI):
    """for "MySQL" RDBMS Interface
    """
    def open(self):
        self.conn = MySQLdb.connect(
            host = self.setting.get('host', 'localhost'),
            user = self.setting.get('user', 'sa'),
            passwd = self.setting.get('passwd', ''),
            db = self.setting.get('db', 'mysql'),
            charset = self.setting.get('charset', 'utf-8'),
            )
