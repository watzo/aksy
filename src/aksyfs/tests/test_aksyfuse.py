from unittest import TestCase, TestLoader
import logging

from aksyfs import aksyfuse
from aksyfs import common

from aksy.device import Devices
from aksy.test import testutil
from stat import S_ISDIR, S_ISREG, ST_MODE, ST_SIZE, S_IRUSR
import os, tempfile

log = logging.getLogger('aksy')

class TestStatInfo(TestCase):
    def test_set_owner(self):
        common.StatInfo.set_owner(1, 1)
        self.assertEquals(1, common.StatInfo.uid)
        self.assertEquals(1, common.StatInfo.gid)
        info = common.StatInfo(0, 1)
        self.assertEquals(1, info.st_uid)
        self.assertEquals(1, info.st_gid)

class TestDirStatInfo(TestCase):
    def test_stat_directory(self):
        info = common.DirStatInfo()
        self.assertTrue(S_ISDIR(info.st_mode))

class TestFileStatInfo(TestCase):
    def test_stat_file(self):
        info = common.FileStatInfo('test.akp', None)
        self.assertFalse(S_ISDIR(info.st_mode))
        self.assertEquals(16*1024, info.st_size)
        self.assertTrue(S_ISREG(info.st_mode))
        
class AksyFSTest(TestCase): #IGNORE:R0904
    def _assertdir(self, info):
        self.assertTrue(S_ISDIR(info.st_mode))
        
    def setUp(self):
        sampler = Devices.get_instance('mock_z48', 'mock', 
                                   debug=0)
        sampler.set_sample(testutil.get_test_resource('test.wav'))
        sampler.set_program(testutil.get_test_resource('221 Angel.akp'))
        self.fs = aksyfuse.AksyFS()
        self.fs.init_sampler(sampler)
        self.fs.getattr('/')
        self.fs.getattr('/disks')
        self.fs.getattr('/memory')
        
    def test_getattr(self):
        info = self.fs.getattr('/')
        self._assertdir(info)
    
    def test_getattr_unsupported(self):
        self.assertRaises(OSError, self.fs.getattr, '/test.doc')

    def test_getattr_memory(self):
        info = self.fs.getattr('/memory/Boo.wav')
        self.assertTrue(S_ISREG(info.st_mode))
        
    def test_readdir(self):
        self.fs.getattr('/')
        root = self.fs.readdir('/', 0)
        self.assert_dirlist(('memory', 'disks'), root)

    def test_readdir_memory(self):
        memory = list(self.fs.readdir('/memory', 0))
        self.assertEquals(102, len(memory))
        self.assertEquals('Boo.wav', memory[0].name)

    def test_getattr_memory_non_existing(self):
        self.assertRaises(OSError, self.fs.getattr, '/memory/subdir')

    def test_getattr_rootdisk(self):
        info = self.fs.getattr('/disks')
        self._assertdir(info)

    def test_readdir_rootdisk(self):
        children = self.fs.readdir('/disks', 0)
        self.assert_dirlist(('Samples disk', 'Cdrom',), children)

    def test_readdir_with_spaces(self):
        info  = self.fs.getattr('/disks/Cdrom')
        self.assert_dirlist(('Mellotron Samples',), self.fs.readdir('/disks/Cdrom', 0))
        
    def test_readdir_disk(self):
        info  = self.fs.getattr('/disks/Samples disk')
        self._assertdir(info)
        children = self.fs.readdir('/disks/Samples disk', 0)
        self.assert_dirlist(('Autoload', 'Songs'), children)

    def test_readdir_disk_nested(self):
        self.fs.getattr('/disks/Cdrom')
        info  = self.fs.getattr('/disks/Cdrom/Mellotron Samples')
        children  = self.fs.readdir('/disks/Cdrom/Mellotron Samples', 0)
        self.assert_dirlist(('Choir','A Sample.AKP','Sample.wav'), children)

    def assert_dirlist(self, expected, actual):
        actual = [entry.name for entry in actual]
        self.assertEquals(tuple(expected), tuple(actual))
            
    def test_mkdir_unsupported(self):
        self.assertRaises(OSError, self.fs.mkdir, '/memory/subdir', 'mode_ignored')

    def test_mkdir_readonly_fs(self):
        self.fs.getattr('/disks/Cdrom')
        self.assertRaises(OSError, self.fs.mkdir, '/disks/Cdrom/test', 'mode_ignored')
    
    def test_mkdir(self):
        self.fs.getattr('/disks/Samples disk')
        self.fs.getattr('/disks/Samples disk/Songs')
        self.assert_dirlist([], self.fs.readdir('/disks/Samples disk/Songs', 0))
        newdir = '/disks/Samples disk/Songs/test'
        self.fs.mkdir(newdir, 'mode_ignored')
        self.assert_dirlist(('test',), 
                          self.fs.readdir('/disks/Samples disk/Songs', 0))
        self.assertNotEquals(None, self.fs.getattr(newdir))

    def test_open_disk(self):
        self.fs.getattr('/disks/Cdrom')
        self.fs.getattr('/disks/Cdrom/Mellotron Samples')
        self.fs.getattr('/disks/Cdrom/Mellotron Samples/Choir')
        afile = aksyfuse.AksyFile('/disks/Cdrom/Mellotron Samples/Choir/Choir.AKP', S_IRUSR)
        afile.release('ignored')

    def test_read(self):
        afile = aksyfuse.AksyFile('/memory/Sample99.wav', os.O_RDONLY|S_IRUSR)
        try:
            read = afile.read(4, 0)
            self.assertEquals('RIFF', read)
        finally:
            afile.release('ignored')

    def test_mknod_write(self):
        path = '/memory/Sample100.wav'
        self.fs.mknod(path, 0, 'ignored')
        afile = aksyfuse.AksyFile('/memory/Sample100.wav', os.O_WRONLY|S_IRUSR)
        afile.write('abc', 0)
        afile.release('ignored')
        written = os.open(common._create_cache_path(path), os.O_RDONLY)
        try:
            self.assertEquals('abc', os.read(written, 3))
        finally:
            os.close(written)

    def test_rmdir(self):
        self.fs.getattr('/disks/Samples disk')
        self.fs.getattr('/disks/Samples disk/Songs')
        path = '/disks/Samples disk/Songs/test'
        self.fs.mkdir(path, 'ignored')
        songs = self.fs.get_parent(path)
        # simulate a refresh
        def refresh():
            songs.children = []
        songs.refresh = refresh
        self.fs.getattr(path)
        self.fs.rmdir(path)
        self.assertRaises(OSError, self.fs.getattr, path)
    
    def test_rmdir_memory(self):
        self.assertRaises(OSError, self.fs.rmdir, '/memory')
        
    def test_unlink(self):
        self.fs.getattr('/memory')
        path = '/memory/Boo.wav'
        self.fs.getattr(path)
        self.fs.unlink(path)
        self.assertRaises(OSError, self.fs.getattr, path)
    
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyfs.tests.test_aksyfuse')
