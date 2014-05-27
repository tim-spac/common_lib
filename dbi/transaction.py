#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/dbi/transaction.py
# date: Mar., 2014
# author: Tim Wang


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
