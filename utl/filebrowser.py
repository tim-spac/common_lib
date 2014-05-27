#!/usr/bin/env python
# coding: utf-8
#
# author: Tim Wang
# date: May, 2014
# filename: filebrowser.py

import os
import fnmatch
import itertools


def iterfiles(path, filenameexp="*.*"):
    """walk on the given path, yield iter file 
        if the filename match the filenameexp
    """
    for home, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, filenameexp):
            yield os.path.join(home, filename)


def relpath(path1, path2):
    ''' return a relative path from path1 equivalent to path path2.
    '''
    pathabspart = lambda p: os.path.abspath(p).split(os.path.sep)
    common = []
    ps1 = pathabspart(path1)
    ps2 = pathabspart(path2)
    for (p1, p2) in itertools.izip(ps1, ps2):
        if p1==p2:
            common.append(p1)
        else:
            break
    return (
            os.path.sep.join(common), 
            os.path.join(*ps1[len(common):]), 
            os.path.join(*ps2[len(common):])
            )


def iterfiletester():
    found = []
    for filename in iterfiles("/home/tim/Projects", "*.py"):
        found.append(filename)
    print relpath(found[0], found[-1])


if __name__ == "__main__":
    iterfiletester()