#!/usr/bin/env python
# coding: utf-8
# 
# filename: common_lib/filetools/tgzutil.py
# author: Tim Wang
# date: Feb., 2014

""" this is utilities module for tar-gz file reader
"""


import tarfile
import os.path
import fnmatch


class TarFileReader:
    """tar-gz file reader
    """
    def __init__(self, filename, fnexp=None):
        """init with given tgz file name,
            fnexp: members' wildcard character
        """
        if os.path.isfile(filename):
            self.filename = filename
            self.fnexp = fnexp
            self.tar = tarfile.open(self.filename)
            self.files = [(member.path, member)
                for member in self.tar.getmembers()
                if member.isfile()
                ]
            self.files.sort()
        
    def __del__(self):
        """close tar file while instance destory
        """
        self.tar.close()
    
    def filter(self, fnexp=None):
        """return sorted member list with fnexp or predefined fnexp filter
        """
        return sorted(fnmatch.filter(
                [f[0] for f in self.files], 
                fnexp or self.fnexp or "*"
                ))
        
    def __getitem__(self, name):
        """get member's file-like handle by given name,
            just like dict operation.
        """
        mapper = dict(self.files)
        return self.tar.extractfile(mapper.get(name))

    def __iter__(self):
        """make the instance like a generator, 
            iterable on filted members' name
        """
        for name in self.filter():
            yield name

    def iter_items(self):
        """make the instance like a generator, 
            iterable on filted members' name and file-like handle
        """
        for name in self.filter():
            yield name, self[name]


class TarFileInput:
    """make tar-gz files like FileInput
    """
    def __init__(self, files, fnexp=None):
        self.files = files
        self.fnexp = fnexp
        self.current = dict(
                filename=None,
                subpath=None, 
                fileno=None, 
                lineno=0,
                isfirstline=None,
                )
    
    def tgzfile(self):
        """
        Return the name of the file currently being read.
        Before the first line has been read, returns None.
        """
        return self.current["filename"]
    
    def subpath(self):
        """
        Return the path of the file's member currently being read.
        Before the first line has been read, returns None.
        """
        return self.current["subpath"]
    
    def filename(self):
        """
        Return the path of the file/member currently being read.
        Before the first line has been read, returns None.
        """
        return os.path.join(
            self.current["filename"],
            self.current["subpath"],
            )
    
    def isfirstline(self):
        """
        Returns true the line just read is the first line of its file,
        otherwise returns false.
        """
        return not self.current["fileno"]
    
    def fileno(self):
        """
        Return the file number of the current file.
        """
        return self.current["fileno"]
    
    def lineno(self):
        """
        Return the cumulative line number of the line that has just been read.
        Before the first line has been read, returns 0. After the last line
        of the last file has been read, returns the line number of that line.
        """
        return self.current["lineno"]
    
    def __iter__(self):
        """
        line by line read on the tar-gzip files' members' content
        """
        for tgzfile in self.files:
            tz = TarFileReader(tgzfile, self.fnexp)
            self.current["filename"] = tgzfile
            for member in tz.filter():
                self.current["subpath"] = member
                self.current["isfirstline"] = True
                for i, ln in enumerate(tz[member].read().splitlines()):
                    self.current["fileno"] = i
                    self.current["lineno"] += 1
                    yield ln
