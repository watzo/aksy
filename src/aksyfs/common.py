from time import time

import stat
import os
import os.path
import errno
import logging

from aksy.device import Devices
from aksy import fileutils
from aksy.concurrent import transaction

from aksy.devices.akai import sampler as samplermod
from aksy.devices.akai import model
from aksy.config import get_config

MAX_FILE_SIZE_SAMPLE = 512 * 1024 * 1024 # 512 MB
MAX_FILE_SIZE_OTHER = 16 * 1024 # 16K
START_TIME = time()

LOG = logging.getLogger('aksy.aksyfs.common')

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
        if size is None:
            size = get_file_size(path)
        StatInfo.__init__(self, stat.S_IFREG|stat.S_IWUSR, size, writable)
        self.st_nlink = 0
        
def is_modified(stat_info):
    return stat_info.st_mtime > START_TIME

def _splitpath(path):
    return path.split('/', 2)[1:]

def _get_cache_path(path):
    return os.path.join(os.path.expanduser('~'), '.aksy/cache' + path)

def get_file_size(path):
    cache_path = _get_cache_path(path)
    if os.path.exists(cache_path):
        return os.lstat(cache_path).st_size
    
    if fileutils.is_sample(path):
        return MAX_FILE_SIZE_SAMPLE
    
    return MAX_FILE_SIZE_OTHER

def _cache_path_exists(path):
    return os.path.exists(_get_cache_path(path))

def _create_cache_path(path):
    cache_path = _get_cache_path(path)
    parent_dir = os.path.dirname(cache_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    return cache_path

class AksyFile(object):
    @staticmethod
    def set_sampler(sampler):
        AksyFile.sampler = sampler
    
    @staticmethod
    def parse_location(location):
        if location == "memory":
            return samplermod.AkaiSampler.MEMORY
        elif location == "disks":
            return samplermod.AkaiSampler.DISK
        else:
            raiseException(errno.ENOENT)
            
    @transaction()
    def __init__(self, path, flags, *mode):
        self.direct_io = True
        self.upload = bool(flags & os.O_WRONLY)
        self.name = os.path.basename(path)
        self.location = AksyFile.parse_location(_splitpath(path)[0])

        self.path = _create_cache_path(path)

        if not self.is_upload() or not _cache_path_exists(path):
            AksyFile.sampler.get(self.name, self.path, self.location)
        
        self.handle = os.open(self.path, flags, *mode)

    @transaction()
    def release(self, flags):
        if self.is_upload():
            try:
                AksyFile.sampler.transfertools.put(self.get_path(), None, self.get_location())
            except IOError, exc:
                # TODO: move to a method where we can raise exceptions
                LOG.exception( "Exception occurred: %s", repr(exc))
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

class FSRoot(model.Container):
    def __init__(self, sampler):
        self.sampler = sampler
        
    def is_writable(self):
        return False
    
    def get_children(self):
        return [self.sampler.memory, self.sampler.disks]

class AksyFS(object): #IGNORE:R0904
    def __init__(self, sampler=None):
        if sampler is not None:
            self.init_sampler(sampler)
        stat_home = os.stat(os.path.expanduser('~'))
        StatInfo.set_owner(stat_home[stat.ST_UID], stat_home[stat.ST_GID])

    @transaction()
    def open_for_read(self, path, mode):
        location = _splitpath(path)[0]
        name = os.path.basename(path)
        path = _create_cache_path(path)

        if location == "memory":
            location = samplermod.AkaiSampler.MEMORY
        elif location == "disks":
            location = samplermod.AkaiSampler.DISK
        else:
            raiseException(errno.ENOENT)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( "open(%s, %s)", path, mode)
        self.sampler.transfertools.get(name, path, location)

        return open(path, mode)

    @transaction()
    def open_for_write(self, path, mode):
        dest = AksyFile.parse_location(_splitpath(path)[0])
        name = os.path.basename(path)
        path = _create_cache_path(path)

        handle = open(path, mode)
        
        class UploadingFileWrapper:
            def __init__(self, fd, sampler):
                self.sampler = sampler
                self.file = fd
                
            def __getattr__(self, attr):
                return getattr(self.file, attr)
            
            def close(self):
                self.file.close()
                self.sampler.transfertools.put(path, name, dest)

        return UploadingFileWrapper(handle, self.sampler)
        
    def fetch_parent_folder(self, path):
        return self.get_parent(path).get_child(os.path.basename(path))

    @transaction()
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

    @transaction()
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
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( 'getattr(%s)', path)
        if fileutils.is_dirpath(path):
            return self.stat_directory(path)
        else:
            return self.stat_file(path)

    @transaction()
    def listdir(self, path):
        folder = self.cache.get(path, None)
        if folder is None:
            raiseException(errno.ENOENT)
        for child in folder.get_children():
            yield child.get_name()

    @transaction()
    def mkdir(self, path, mode='unused'):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('mkdir(%s, %s)', path, mode)
        folder = self.get_parent(path)
        if not folder.is_writable():
            raiseException(errno.EROFS)
        if not hasattr(folder, 'create_folder'):
            raiseUnsupportedOperationException()
        
        child = folder.create_folder(os.path.basename(path))
        self.cache[path] = child

    @transaction()
    def rename(self, old_path, new_path):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('rename(%s, %s)', old_path, new_path)
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

    @transaction()
    def rmdir(self, path):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('rmdir(%s)', path)
        folder = self.cache[path]
        if hasattr(folder, 'delete'):
            folder.delete()
            del self.cache[path]
            self.get_parent(path).refresh()
            return

        raiseException(errno.EPERM)

    @transaction()
    def unlink(self, path):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('unlink(%s)', path)
        file_obj = self.get_file(path)
        file_obj.delete()
        try:
            os.remove(_create_cache_path(path))
        except OSError:
            # file not cached
            pass 
        
        self.get_parent(path).refresh()

    def init_sampler(self, sampler):
        self.root = FSRoot(sampler)
        self.sampler = sampler
        self.cache = { '/': self.root }
        AksyFile.set_sampler(sampler)

def raiseUnsupportedOperationException():
    raiseException(errno.ENOSYS)

def raiseException(err):
    raise OSError(err, 'Exception occurred')
