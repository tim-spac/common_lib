#!/usr/bin/env python
# coding: utf-8
#
# filename: common_lib/filetools/bufferedstorage.py
# author: Tim Wang
# date: Jan., 2014

"""the BufferedStorage class is a peer with file-write
"""

import codecs

from common_lib.utl.bufferedprocess import BufferedProcess

class BufferedStorage(BufferedProcess):
    """
    Based on file like storage (which support writelines methord),
    provide buffer for effectiveness optimization
    """

    def __init__(self, handle, fmtfunc=None):
        """provide an opened file handle for init
        """
        self.handle = handle
        self.fmtfunc = fmtfunc
        BufferedProcess.__init__(self, 
            process=lambda x: self.handle.writelines(map(self.fmtfunc, x))
            )


class BufferedFile(BufferedStorage):
    """
    Based on BufferedStorage
    open file with given name,
    close when destroy.
    """
    def __init__(self, filename):
        BufferedStorage.__init__(self, 
            handle=open(filename, 'at'), 
            fmtfunc=None)

    def __del__(self):
        BufferedStorage.__del__(self)
        self.handle.close()


class BufferedUFile(BufferedFile):
    """
    Based on BufferedFile, usage codecs to support unicode,
    with given name and charset, close when destroy.
    """
    def __init__(self, filename, coding="utf-8"):
        BufferedStorage.__init__(self, 
            handle=codecs.open(filename, 'a', coding), 
            fmtfunc=None)
