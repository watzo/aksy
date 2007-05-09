#!/usr/bin/python

from fuse import Fuse

from time import time

from stat import *
import os
import os.path
import errno

from aksy.device import Devices
from aksy import fileutils, model
from aksy.devices.akai.sampler import Sampler

    
def stat_inode(mode, size, child_count, uid, gid, writable=False):
        
    info = [None] * 10
    info[ST_DEV] = 0 # TODO: figure out whether required to provide unique value
    info[ST_INO] = 0 # TODO: figure out whether required to provide unique value
    info[ST_MODE] = mode|S_IRUSR|S_IRGRP
    if writable:
        info[ST_MODE] = info[ST_MODE]|S_IWUSR
    info[ST_SIZE] = size
    info[ST_ATIME] = int(time())
    info[ST_CTIME] = info[ST_ATIME]
    info[ST_MTIME] = info[ST_ATIME]
    info[ST_NLINK] = child_count

    info[ST_UID] = uid
    info[ST_GID] = gid
    return info

def stat_dir(uid, gid, child_count=1):
    return stat_inode(S_IFDIR|S_IEXEC, 4096L, child_count, uid, gid)

def stat_file(uid, gid):
    return stat_inode(S_IFREG, 0L, 0, uid, gid)

class FSRoot(object):
    def __init__(self, z48):
        self.z48 = z48
    def get_children(self):
        return [self.z48.memory, self.z48.disks]

    def get_dir(self, path):
        if path == '/':
            return self
        
        store_name, rel_path  = path.split('/', 2)[1:]
        for child in self.get_children():
            if child.get_name() == store_name:
                if child.get_dir(rel_path) is None:
                    raiseException(errno.ENOENT)
                folder = model.Folder(rel_path)
                folder.set_current()
                return folder
        
        raiseException(errno.ENOENT)

class DiskNode(model.Disk):
    def list_children(self):
        pass
    
class AksyFS(Fuse):
    def __init__(self, z48, **args):
        self.flags = 0
        self.multithreaded = 0
        #self.debug = True
        Fuse.__init__(self, [], **args)

        self.z48 = z48
        self.root = FSRoot(z48)
        self.cache = {}
        self.cache['/memory'] = z48.memory
        self.cache['/disks'] = z48.disks
        stat_home = os.stat(os.path.expanduser('~'))
        self.uid = stat_home[ST_UID]
        self.gid = stat_home[ST_GID]

    def find_file(self, path):
        parent = os.path.dirname(path)
        dir = self.find_directory(parent)
        return dir
        
    def find_directory(self, path):
        return self.cache[path]
    
    def stat_directory(self, path):
        if self.cache.get(path) is None:
            self.cache[path] = self.root.get_dir(path)
        
        return stat_dir(self.uid, self.gid)

    def stat_file(self, path):
        if not Sampler.is_filetype_supported(path):
            raiseException(errno.ENOENT)
        parent = os.path.dirname(path)
        parent_dir = self.cache[parent]
        file_name = os.path.basename(path)
        
        for child in parent_dir.get_children():
            if child.get_name() == file_name:
                return stat_file(self.uid, self.gid)
        
        raiseException(errno.ENOENT)

    def getattr(self, path):
        print '*** getattr', path
        if fileutils.is_dirpath(path):
            return self.stat_directory(path)
        else:
            return self.stat_file(path)

    def getdir(self, path):
        print '*** getdir', path
        dir = self.cache[path]
        return [(child.get_name(), 0) for child in dir.get_children()]

    def fsync(self, path, isFsyncFile):
        print '*** fsync', path, isFsyncFile
        # TODO
        raiseUnsupportedOperationException()

    def link(self, targetPath, linkPath):
        print '*** link', targetPath, linkPath
        raiseUnsupportedOperationException()

    def mkdir(self, path, mode):
        print '*** mkdir', path, oct(mode)
        # TODO
        raiseUnsupportedOperationException()

    def open(self, path, flags):
        print '*** open', path, flags
        # TODO
        raiseUnsupportedOperationException()

    def read(self, path, length, offset):
        print '*** read', path, length, offset
        # TODO
        raiseUnsupportedOperationException()

    def readlink(self, path):
        print '*** readlink', path
        raiseUnsupportedOperationException()

    def release(self, path, flags):
        print '*** release', path, flags
        raiseUnsupportedOperationException()

    def rename(self, oldPath, newPath):
        print '*** rename', oldPath, newPath
        raiseUnsupportedOperationException()

    def rmdir(self, path):
        print '*** rmdir', path
        raiseUnsupportedOperationException()

    def statfs(self):
        print '*** statfs'
        raiseUnsupportedOperationException()

    def symlink(self, targetPath, linkPath):
        print '*** symlink', targetPath, linkPath
        raiseUnsupportedOperationException()

    def unlink(self, path):
        print '*** unlink', path
        # TODO
        raiseUnsupportedOperationException()

    def utime(self, path, times):
        print '*** utime', path, times
        raiseUnsupportedOperationException()

    def write(self, path, buf, offset):
        print '*** write', path, buf, offset
        # TODO
        raiseUnsupportedOperationException()

    def truncate(self, path, size):
        raiseUnsupportedOperationException()

    def mythread(self):
        raiseUnsupportedOperationException()

    def chmod(self, path, mode):
        raiseUnsupportedOperationException()

    def chown(self, path, uid, gid):
        raiseUnsupportedOperationException()

    def mknod(self, path, mode, dev):
        raiseUnsupportedOperationException()

def raiseUnsupportedOperationException():
    raiseException(errno.ENOSYS)

def raiseException(err):
    e = OSError()
    e.errno = err
    raise e

if __name__ == '__main__':
    z48 = Devices.get_instance('mock_z48', None)
    fs = AksyFS(z48)
    fs.mountpoint = '/tmp/aksy'
    fs.main()