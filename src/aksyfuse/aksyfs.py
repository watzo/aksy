#!/usr/bin/python

import fuse

from time import time

import stat
import os, sys
import os.path
import errno

from aksy.device import Devices
from aksy import fileutils, model
from aksy.concurrent import transaction

from aksy.devices.akai import sampler as samplermod

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files')

MAX_FILE_SIZE_SAMPLE = 512 * 1024 * 1024 # 512 MB
MAX_FILE_SIZE_OTHER = 16 * 1024 # 16K
START_TIME = time()

class StatInfo(object):
    @staticmethod
    def set_owner(uid, gid):
        StatInfo.uid = uid
        StatInfo.gid = gid
        
    def __init__(self, mode, size, writable=False):
        self.st_dev = 0 # TODO: figure out whether required to provide unique value
        self.st_ino = 0 # TODO: figure out whether required to provide unique value
        self.st_mode = mode|stat.S_IRUSR|stat.S_IRGRP
        if writable:
            self.st_mode |= stat.S_IWUSR

        self.st_size = size
        self.st_atime = int(time())
        self.st_ctime = self.st_atime
        if is_modified:
            self.st_mtime = int(time())
        else:
            self.st_mtime = self.st_atime
        self.st_uid = StatInfo.uid
        self.st_gid = StatInfo.gid

class DirStatInfo(StatInfo):   
    def __init__(self, writable=False, child_count=1):
        StatInfo.__init__(self, stat.S_IFDIR|stat.S_IEXEC, 4096L)
        self.st_nlink = child_count

class FileStatInfo(StatInfo):
    def __init__(self, path, size, writable=False):
        cache_path = _get_cache_path(path)
        if size is None:
            if os.path.exists(cache_path):
                size = os.lstat(cache_path).st_size
            elif fileutils.is_sample(path):
                size = MAX_FILE_SIZE_SAMPLE
            else:
                size = MAX_FILE_SIZE_OTHER
        StatInfo.__init__(self, stat.S_IFREG|stat.S_IWUSR, size, writable)
        self.st_nlink = 0
        
def is_modified(stat_info):
    return stat_info.st_mtime > START_TIME

def _splitpath(path):
    return path.split('/', 2)[1:]

def _get_cache_path(path):
    return os.path.expanduser('~/.aksy/cache' + path)

def _cache_path_exists(path):
    return os.path.exists(_get_cache_path(path))

def _create_cache_path(path):
    cache_path = _get_cache_path(path)
    parent_dir = os.path.dirname(cache_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    return cache_path

class AksyFile(fuse.FuseFileInfo):
    @staticmethod
    def set_sampler(sampler):
        AksyFile.sampler = sampler
    
    @transaction(samplermod.Sampler.lock)
    def __init__(self, path, flags, *mode):
        self.direct_io = True
        self.upload = bool(flags & os.O_WRONLY)
        self.name = os.path.basename(path)
        location = _splitpath(path)[0]
        if location == "memory":
            self.location = samplermod.AkaiSampler.MEMORY
        elif location == "disks":
            self.location = samplermod.AkaiSampler.DISK
        else:
            raiseException(errno.ENOENT)

        self.path = _create_cache_path(path)

        if not self.is_upload() or not _cache_path_exists(path):
            AksyFile.sampler.get(self.name, self.path, self.location)
        
        self.handle = os.open(self.path, flags, *mode)

    @transaction(samplermod.Sampler.lock)        
    def release(self, flags):
        if self.is_upload():
            try:
                AksyFile.sampler.put(self.get_path(), None, self.get_location())
            except IOError, exc:
                # TODO: move to a method where we can raise exceptions
                print "Exception occurred: ", repr(exc)
        os.close(self.handle)

    def write(self, buf, offset):
        os.lseek(self.handle, offset, 0)
        return os.write(self.handle, buf)

    def read(self, length, offset):
        os.lseek(self.handle, offset, 0)
        return os.read(self.handle, length)

    def get_name(self):
        return self.name
    
    def get_path(self):
        return self.path
    
    def is_upload(self):
        return self.upload

    def get_handle(self):
        return self.handle
    
    def get_location(self):
        return self.location

class FSStatInfo(fuse.StatVfs):
    def __init__(self, mem_total, mem_free):
        fuse.StatVfs.__init__(self)
        self.f_bsize = 1024
        self.f_frsize = 1024
        self.f_blocks = mem_total
        self.f_bfree = mem_free
        self.f_bavail = mem_free

class FSRoot(model.Container):
    def __init__(self, sampler):
        self.sampler = sampler
        
    def is_writable(self):
        return False
    
    def get_children(self):
        return [self.sampler.memory, self.sampler.disks]

class AksyFS(fuse.Fuse): #IGNORE:R0904
    def __init__(self, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)
        self.multithreaded = True
        self.fuse_args.setmod('foreground')
        self.sampler_id = 'mock_z48'
        self.file_class = AksyFile
        stat_home = os.stat(os.path.expanduser('~'))
        StatInfo.set_owner(stat_home[stat.ST_UID], stat_home[stat.ST_GID])

    def access(self, path, mode):
        print "**access " + path
        pass
    
    def fetch_parent_folder(self, path):
        return self.get_parent(path).get_child(os.path.basename(path))

    @transaction(samplermod.Sampler.lock)
    def stat_directory(self, path):
        folder = self.cache.get(path)
        if folder is None:
            folder = self.fetch_parent_folder(path)
            if folder is None:
                raiseException(errno.ENOENT)
            self.cache[path] = folder
        return DirStatInfo(folder.is_writable())

    def get_parent(self, path):
        parent = os.path.dirname(path)
        return self.cache[parent]
        
    def get_file(self, path):
        if not samplermod.Sampler.is_filetype_supported(path):
            raiseException(errno.ENOENT)

        parent_dir = self.get_parent(path)
        file_name = os.path.basename(path)
        
        for child in parent_dir.get_children():
            if child.get_name() == file_name:
                return child
        return None

    @transaction(samplermod.Sampler.lock)
    def stat_file(self, path):
        cached = self.cache.get(path, None)
        if cached is not None:
            return cached
        if _cache_path_exists(path):
            return os.lstat(_create_cache_path(path))
        
        file_obj = self.get_file(path)
        if file_obj is None:
            raiseException(errno.ENOENT)
        else:
            return FileStatInfo(path, file_obj.get_size(), False)

    def getattr(self, path):
        print '*** getattr', path
        if fileutils.is_dirpath(path):
            return self.stat_directory(path)
        else:
            return self.stat_file(path)

    @transaction(samplermod.Sampler.lock)
    def readdir(self, path, offset):
        print '*** readdir', path, offset
        folder = self.cache[path]
        for child in folder.get_children():
            yield fuse.Direntry(child.get_name())

    @transaction(samplermod.Sampler.lock)
    def mkdir(self, path, mode):
        print '*** mkdir', path, mode
        folder = self.get_parent(path)
        if not folder.is_writable():
            raiseException(errno.EROFS)
        if not hasattr(folder, 'create_folder'):
            raiseUnsupportedOperationException()
        
        child = folder.create_folder(os.path.basename(path))
        self.cache[path] = child

    @transaction(samplermod.Sampler.lock)
    def rename(self, old_path, new_path):
        print '*** rename', old_path, new_path
        new_dir = os.path.dirname(new_path)
        if os.path.dirname(old_path) != new_dir:
            file_obj = self.get_file(old_path)
            if hasattr(file_obj, 'save'):
                folder = self.cache[new_dir]
                folder.set_current()
                file_obj.save(False, False)
            elif hasattr(file_obj, 'load'):
                file_obj.load()
            else:
                raiseUnsupportedOperationException() 
            return
                
        new_name = os.path.basename(new_path)
        if fileutils.is_dirpath(old_path):
            folder = self.cache[old_path]
            folder.rename(new_name)
            self.cache[new_path] = folder
            del self.cache[old_path]
        else: 
            file_obj = self.get_file(old_path)
            file_obj.rename(new_name)

    @transaction(samplermod.Sampler.lock)
    def rmdir(self, path):
        print '*** rmdir', path
        folder = self.cache[path]
        if hasattr(folder, 'delete'):
            folder.delete()
            del self.cache[path]
            self.get_parent(path).refresh()
            return

        raiseException(errno.EPERM)

    @transaction(samplermod.Sampler.lock)
    def unlink(self, path):
        print '*** unlink', path
        file_obj = self.get_file(path)
        file_obj.delete()
        self.get_parent(path).refresh()

    @transaction(samplermod.Sampler.lock)
    def mknod(self, path, mode, dev):
        print '*** mknod ', path, mode, dev
        self.cache[path] = FileStatInfo(path, None)
        self.get_parent(path).refresh()

    def truncate(self, path, size): #IGNORE:W0212
        print "*** truncate ", path, size
        pass
    
    def statfs(self):
        print "*** statfs (metrics on memory contents only)"
        mem_total = self.sampler.systemtools.get_wave_mem_size()
        mem_free = self.sampler.systemtools.get_free_wave_mem_size()
        return FSStatInfo(mem_total, mem_free)

    def init_sampler(self, sampler):
        self.root = FSRoot(sampler)
        self.sampler = sampler
        self.cache = { '/': self.root }
        AksyFile.set_sampler(sampler)

    def main(self, sampler, *args, **kw):
        self.init_sampler(sampler)
        return fuse.Fuse.main(self, *args, **kw)

def raiseUnsupportedOperationException():
    raiseException(errno.ENOSYS)

def raiseException(err):
    raise OSError(err, 'Exception occurred')

def main():
    usage = """
Aksyfs: mount your sampler as a filesystem

""" + fuse.Fuse.fusage

    fs = AksyFS(version="%prog " + fuse.__version__,
                 usage=usage,
                 dash_s_do='setsingle')

    fs.parser.add_option(mountopt="sampler_id", metavar="SAMPLER_ID", default='mock_z48',
                         help="mount SAMPLER_ID [default: %default]")
    fs.parse(values=fs, errex=1)

    if fs.sampler_id == "mock_z48":
        script_dir = os.path.abspath(os.path.split(__file__)[0])
        src_dir = os.path.dirname(script_dir)
        sampler = Devices.get_instance('mock_z48', None, 
                              debug=1, 
                              sampleFile=os.path.join(src_dir, 'aksy/test/test.wav'))
    else:
        sampler = Devices.get_instance(fs.sampler_id, 'usb')
    try:
        sampler.start_osc_server()
        fs.main(sampler)
    finally:
        sampler.stop_osc_server()
        sampler.close()

if __name__ == '__main__':
    main()
