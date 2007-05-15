#!/usr/bin/python

from fuse import Fuse

from time import time

import stat
import os
import os.path
import errno

from aksy.device import Devices
from aksy import fileutils
from aksy.devices.akai import sampler, sysex_types

MAX_FILE_SIZE_SAMPLE = 512 * 1024 * 1024 # 512 MB
MAX_FILE_SIZE_OTHER = 16 * 1024 # 16K

EOF = '\x00' 

def stat_inode(mode, size, child_count, uid, gid, writable=False):
        
    info = [None] * 10
    info[stat.ST_DEV] = 0 # TODO: figure out whether required to provide unique value
    info[stat.ST_INO] = 0 # TODO: figure out whether required to provide unique value
    info[stat.ST_MODE] = mode|stat.S_IRUSR|stat.S_IRGRP
    if writable:
        info[stat.ST_MODE] = info[stat.ST_MODE]|stat.S_IWUSR
    info[stat.ST_SIZE] = size
    info[stat.ST_ATIME] = int(time())
    info[stat.ST_CTIME] = info[stat.ST_ATIME]
    info[stat.ST_MTIME] = info[stat.ST_ATIME]
    info[stat.ST_NLINK] = child_count
    info[stat.ST_UID] = uid
    info[stat.ST_GID] = gid
    return info

def stat_dir(uid, gid, child_count=1):
    return stat_inode(stat.S_IFDIR|stat.S_IEXEC, 4096L, child_count, uid, gid)

# TODO: provide real values for samples (other sizes can't be determined
def stat_file(uid, gid, path):
    if fileutils.is_sample(path):
        size = MAX_FILE_SIZE_SAMPLE
    else:
        size = MAX_FILE_SIZE_OTHER
    return stat_inode(stat.S_IFREG, size, 0, uid, gid)

class FSRoot(object):
    def __init__(self, sampler):
        self.sampler = sampler
    def get_children(self):
        return [self.sampler.memory, self.sampler.disks]

    def find_child(self, path):
        store_name, rel_path  = path.split('/', 2)[1:]
        for store in self.get_children():
            if store.get_name() == store_name:
                return store
        return None

    def get_dir(self, path):
        if path == '/':
            return self
        
        store_name, rel_path  = path.split('/', 2)[1:]
        store = self.find_child(path)
        if store is None:
            raiseException(errno.ENOENT)        
        
        if not hasattr(store, 'get_dir'):
            raiseException(errno.ENOENT)
        subdir = store.get_dir(rel_path)
        if subdir is None:
            raiseException(errno.ENOENT)
        
        return subdir
        
    def mkdir(self, path):
        store = self.find_child(path)
        print store
        if not hasattr(store, 'create_folder'):
            raiseException(errno.EINVAL)
        store.create_folder(path)
    
class AksyFS(Fuse):
    def __init__(self, z48, **args):
        self.flags = 0
        self.multithreaded = 0
        self.debug = True
        Fuse.__init__(self, [], direct_io=True)

        self.z48 = z48
        self.root = FSRoot(z48)
        self.cache = {}
        self.cache['/memory'] = z48.memory
        self.cache['/disks'] = z48.disks
        stat_home = os.stat(os.path.expanduser('~'))
        self.uid = stat_home[stat.ST_UID]
        self.gid = stat_home[stat.ST_GID]

    def stat_directory(self, path):
        if self.cache.get(path) is None:
            self.cache[path] = self.root.get_dir(path)
        return stat_dir(self.uid, self.gid)

    def get_parent(self, path):
        parent = os.path.dirname(path)
        return self.cache[parent]
        
    def stat_file(self, path):
        if not sampler.Sampler.is_filetype_supported(path):
            raiseException(errno.ENOENT)
        parent_dir = self.get_parent(path)
        file_name = os.path.basename(path)
        
        for child in parent_dir.get_children():
            if child.get_name() == file_name:
                return stat_file(self.uid, self.gid, path)
        
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
        print '*** mkdir', path, mode
        self.root.mkdir(path)

    def open(self, path, flags):
        print '*** open', path, flags
        # TODO
        #self.z48.get()
        #raiseUnsupportedOperationException()

    def read(self, path, length, offset):
        print '*** read', path, length, offset
        return 'abc-1' + EOF
        # TODO
        #raiseUnsupportedOperationException()

    def readlink(self, path):
        print '*** readlink', path
        raiseUnsupportedOperationException()

    def release(self, path, flags):
        print '*** release', path, flags
        #raiseUnsupportedOperationException()

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
        print '*** mknod ', path, mode, dev
        #TODO
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