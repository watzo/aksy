
"""
filebatch.py

class FileBatch describes a list of filenames with full path info
"""

import os
from glob import *

import filex, filenamer

class FileBatch:
    def __init__(self, filelist=[], dir="", mask="*.*"):
        self.data = filelist
        if dir != "":
            self.appendDir(dir, mask)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
        except:
            raise IndexError

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise IndexError

    def __delitem__(self, key):
        try:
            del self.data[key]
        except:
            raise IndexError

    def appendDir(self, dir, mask="*.*"):
        flist = glob(filex.pathjoin(dir, mask))
        self.data = self.data + flist

    def removeDir(self, dir, mask="*.*"):
        flist = glob(filex.pathjoin(dir, mask))
        for x in flist:
            if x in self.data:
                self.data.remove(x)

    def reset(self):
        self.data = []

    def allNewNames(self):
        """get new unique filenames for all files"""
        for i in xrange(0, len(self.data)):
            self.data[i] = filenamer.uniqueFilename(self.data[i])
        

"""
fb = FileBatch(dir="c:\\it", mask="*.it")
fb.appendDir("c:\\audio")
print fb.data
fb.removeDir("c:\\it")
print fb.data
"""

#fb = FileBatch(dir="c:\\it", mask="*.it")
#fb.allNewNames()
#print fb.data




        