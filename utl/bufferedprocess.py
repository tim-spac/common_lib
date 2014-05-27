#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/utl/bufferedprocess.py
# author: Tim Wang
# date: Jan., 2014

"""define a abstract class for make a buffer, and batch process
"""

class BufferedProcess:
    """make a buffer, automated process when full or exit
    """
    MAXSIZE = 8192
    
    def __init__(self, process):
        """define process methord by init
        """
        self.process = process
        self.buff = []
    
    def __del__(self):
        """auto flush when instance destory
        """
        self.flush()
    
    def __enter__(self):
        """support with .. statement -- enter
        """
        self.buff = []
        return self
    
    def __exit__(self, *args):
        """support with .. statement -- leave
        """
        self.flush()
    
    def append(self, obj):
        """append object/data to buffer, waiting for process
        """
        self.buff.append(obj)
        if len(self.buff) >= self.MAXSIZE:
            self.flush()
    
    def __lshift__(self, obj):
        """support operator "<<" to append
        """
        self.append(obj)
    
    def flush(self):
        """process with buffer, and clean it
        """
        if self.buff:
            data, self.buff = self.buff, []
            self.process(data)
