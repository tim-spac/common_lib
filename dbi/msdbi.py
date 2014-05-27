#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/dbi/msdbi.py
# author: Tim Wang
# date: Jan., 2014

"""provide RDBMS database interface
    "MsDBI" for MsSQL
"""

import pymssql

from common_lib.dbi.rdbmsdbi import _DBI


class MsDBI(_DBI):
    """for "M$SQL" RDBMS Interface
    """
    def open(self):
        self.conn = pymssql.connect(
            host = self.setting.get('host', 'localhost'),
            user = self.setting.get('user', 'sa'),
            password = self.setting.get('password', ''),
            database = self.setting.get('database', 'master'),
            charset = self.setting.get('charset', 'gbk'),
            )


