#!/usr/bin/python

import fuse

from time import time

import stat
import os
import os.path
import errno
import logging

from aksy.device import Devices
from aksy.concurrent import transaction

from aksy.devices.akai import sampler as samplermod
from aksy import config
from aksyfs import common

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files')

MAX_FILE_SIZE_SAMPLE = 512 * 1024 * 1024 # 512 MB
MAX_FILE_SIZE_OTHER = 16 * 1024 # 16K
START_TIME = time()

LOG = logging.getLogger('aksy.aksyfs.aksyfuse')

class AksyFile(fuse.FuseFileInfo):
    @staticmethod
    def set_sampler(sampler):
        AksyFile.sampler = sampler
    
    @transaction()
    def __init__(self, path, flags, *mode):
        self.direct_io = True
        self.upload = bool(flags & os.O_WRONLY)
        self.name = os.path.basename(path)
        location = common._splitpath(path)[0]
        if location == "memory":
            self.location = samplermod.AkaiSampler.MEMORY
        elif location == "disks":
            self.location = samplermod.AkaiSampler.DISK
        else:
            raiseException(errno.ENOENT)

        self.path = common._create_cache_path(path)
        if not self.is_upload() and not common._cache_path_exists(path):
            AksyFile.sampler.transfertools.get(self.name, self.path, self.location)
        
        self.handle = os.open(self.path, flags, *mode)

    @transaction()
    def release(self, flags):
        if self.is_upload():
            try:
                AksyFile.sampler.transfertools.put(self.get_path(), None, self.get_location())
            except IOError, exc:
                # TODO: move to a method where we can raise exceptions
                LOG.exception( "Exception occurred: ", exc)
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

class AksyFS(common.AksyFS, fuse.Fuse): #IGNORE:R0904
    def __init__(self, *args, **kw):
        # todo postpone sampler init
        common.AksyFS().__init__()
        
        fuse.Fuse.__init__(self, *args, **kw)
        self.multithreaded = True
        cfg = config.get_config()
        self.sampler_type = cfg.get('sampler', 'type')
        self.connector = config.get_value(cfg, 'sampler', 'connector')
        self.file_class = AksyFile
        stat_home = os.stat(os.path.expanduser('~'))
        common.StatInfo.set_owner(stat_home[stat.ST_UID], stat_home[stat.ST_GID])

    def access(self, path, mode):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( "**access (" + path + ") (no-op)")
    
    @transaction()
    def readdir(self, path, offset):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( '*** readdir(%s, %s)', path, offset)
        folder = self.cache[path]
        for child in folder.get_children():
            yield fuse.Direntry(child.get_name())

    @transaction()
    def mknod(self, path, mode, dev):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( 'mknod(%s, %s, %s)', path, mode, dev)
        self.cache[path] = common.FileStatInfo(path, None)
        self.get_parent(path).refresh()

    def truncate(self, path, size):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( "truncate (%s, %s) (no-op)", path, size)
    
    @transaction()
    def statfs(self):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug( "statfs (metrics on memory contents only)")
        mem_total = self.sampler.systemtools.get_wave_mem_size()
        mem_free = self.sampler.systemtools.get_free_wave_mem_size()
        return FSStatInfo(mem_total, mem_free)

    def init_sampler(self, sampler):
        self.root = common.FSRoot(sampler)
        self.sampler = sampler
        self.cache = { '/': self.root }
        AksyFile.set_sampler(sampler)

    def main(self, sampler, *args, **kw):
        self.init_sampler(sampler)
        return fuse.Fuse.main(self, *args, **kw)
    
    def destroy(self):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('fsdestroy')
        self.sampler.close()
        

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

    fs.parser.add_option(mountopt="sampler_type", metavar="SAMPLER_TYPE", default=fs.sampler_type,
                         help="use SAMPLER_TYPE (z48/mpc4k/s56k|mock_z48) [default: %default]")
    fs.parser.add_option(mountopt="connector", metavar="CONNECTOR", default=fs.connector,
                         help="use CONNECTOR (usb|osc) [default: %default]")
    fs.parser.add_option(mountopt="sample_file", metavar="SAMPLE_FILE", 
                         help="The wave file to be served when any wave file is accessed on the filesystem (only valid with mock_z48)")
    fs.parser.add_option(mountopt="program_file", metavar="PROGRAM_FILE", 
                         help="The program to be served when any program is accessed on the filesystem (only valid with mock_z48")

    fs.parse(values=fs, errex=1)

    if fs.sampler_type == "mock_z48":
        sampler = Devices.get_instance('mock_z48', 'mock')
        sampler.set_sample(fs.sample_file)
        sampler.set_program(fs.program_file)
    else:
        sampler = Devices.get_instance(fs.sampler_type, fs.connector)
    try:
        #sampler.start_osc_server()
        fs.main(sampler)
    finally:
        #sampler.stop_osc_server()
        sampler.close()
