#!/usr/bin/env python
# coding: utf-8
#
# author: Tim Wang
# date: May, 2014
# filename: common_lib/utl/streambase.py

from itertools import imap as map


class StreamBasePipe:
    
    def __init__(self, process=None, ostream=None):
        self.istreams = []
        self.ostream = ostream
        if not process:
            self._process = lambda x: x
        else:
            self._process = process
        self._buff = []
        
    def append(self, obj):
        output = self.ostream or self._buff
        output.append(self._process(obj))

    def extend(self, iter):
        output = self.ostream or self._buff
        output.extend(map(self._process, iter))
    
    def __rshift__(self, another):
        if self not in another.istreams:
            another.istreams.append(self)
        return another
    
    def __lshift__(self, obj):
        self.append(obj)
    
    def __iter__(self):
        if self._buff:
            buff, self._buff = self._buff, []
            for data in buff:
                yield data
        for istream in self.istreams:
            for obj in istream:
                yield self._process(obj)
        

def tester():
    generator1 = StreamBasePipe(process=str)
    generator2 = StreamBasePipe()
    pfactory = StreamBasePipe(process=lambda x: '%03d'%int(x))
    collector = StreamBasePipe()

    generator1 >> pfactory >> collector
    generator2 >> collector
    
    generator1.extend(xrange(100))
    generator2.extend(xrange(1000,1200))

    for data in collector :
        print "collector:%r" % data


if __name__ == "__main__":
    tester()