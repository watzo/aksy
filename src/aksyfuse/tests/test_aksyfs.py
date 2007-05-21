from unittest import TestCase, TestLoader
import logging

from aksyfuse import aksyfs
from aksy.device import Devices
from aksy.test import testutil
from stat import S_ISDIR, S_ISREG, ST_MODE, ST_SIZE, S_IRUSR
import os, errno, tempfile

log = logging.getLogger('aksy')

class TestModuleTest(TestCase):
    def test_stat_directory(self):
        info = aksyfs.stat_dir(1000, 1000)
        self.assertTrue(S_ISDIR(info[ST_MODE]))
        self.assertEquals(len(os.stat('/')), len(info))

    def test_stat_file(self):
        info = aksyfs.stat_file(1000, 1000, 'test.akp')
        self.assertFalse(S_ISDIR(info[ST_MODE]))
        self.assertEquals(len(os.stat('/')), len(info))
        self.assertEquals(16*1024, info[ST_SIZE])

class AksyFSTest(TestCase): #IGNORE:R0904
    def _assertdir(self, info):
        self.assertTrue(S_ISDIR(info[ST_MODE]))
        
    def setUp(self):
        z48 = Devices.get_instance('mock_z48', None, 
                                   debug=0, 
                                   sampleFile=testutil.get_test_resource('test.wav'))
        self.fs = aksyfs.AksyFS(z48)
        
    def test_getattr(self):
        info = self.fs.getattr('/')
        self.assertTrue(S_ISDIR(info[ST_MODE]))
    
    def test_getattr_unsupported(self):
        self.assertRaises(OSError, self.fs.getattr, '/test.doc')

    def test_getattr_memory(self):
        self.fs.getattr('/memory')
        info = self.fs.getattr('/memory/Boo.wav')
        self.assertTrue(S_ISREG(info[ST_MODE]))
        
    def test_getdir(self):
        self.fs.getattr('/')
        root = self.fs.getdir('/')
        self.assertEquals([('memory', 0), ('disks', 0)], root)

    def test_getdir_memory(self):
        self.fs.getattr('/memory')
        memory = self.fs.getdir('/memory')
        self.assertEquals(102, len(memory))
        self.assertEquals(('Boo.wav', 0), memory[0])

    def test_getattr_memory_non_existing(self):
        self.assertRaises(OSError, self.fs.getattr, '/memory/subdir')

    def test_getattr_rootdisk(self):
        info = self.fs.getattr('/disks')
        self._assertdir(info)

    def test_getdir_rootdisk(self):
        self.fs.getattr('/disks')
        children = self.fs.getdir('/disks')
        self.assertEquals([('Samples disk', 0), ('Cdrom', 0)], children)

    def test_getdir_disk(self):
        info  = self.fs.getattr('/disks/Samples disk')
        self._assertdir(info)
        children = self.fs.getdir('/disks/Samples disk')
        self.assertEquals([('Autoload', 0), ('Songs', 0)], children)

        info  = self.fs.getattr('/disks/Cdrom/Mellotron')
        children  = self.fs.getdir('/disks/Cdrom/Mellotron')
        self.assertEquals([('Choir', 0), ('Sample.AKP', 0), ('Sample.wav', 0)], 
                          children)

    def test_mkdir_unsupported(self):
        self.assertRaises(OSError, self.fs.mkdir, '/memory/subdir', 'mode_ignored')

    def not_test_mkdir_readonly_fs(self):
        self.assertRaises(IOError, self.fs.mkdir, '/disks/Cdrom/test', 'mode_ignored')
    
    def test_mkdir(self):
        self.fs.getattr('/disks/Samples disk/Songs')
        self.assertEquals([], self.fs.getdir('/disks/Samples disk/Songs'))
        newdir = '/disks/Samples disk/Songs/test'
        self.fs.mkdir(newdir, 'mode_ignored')
        self.assertEquals([('test', 0)], 
                          self.fs.getdir('/disks/Samples disk/Songs'))
        self.assertNotEquals(None, self.fs.getattr(newdir))


    def test_open_memory(self):
        path = '/memory/Sample99.wav'
        try:
            self.fs.open(path, S_IRUSR)
            info = self.fs.root.file_cache[path]
            self.assertEquals(os.stat(testutil.get_test_resource('test.wav'))[ST_SIZE], 
                              os.fstat(info.get_handle())[ST_SIZE])
        finally:
            self.fs.release(path, 'ignored')
            self.assertEquals(None, self.fs.root.file_cache.get(path, None))


    def test_open_disk(self):
        self.fs.open('/disks/Cdrom/Mellotron/Choir/Choir.AKP', S_IRUSR)
        self.fs.release('/disks/Cdrom/Mellotron/Choir/Choir.AKP', 'ignored')

    def test_release(self):
        # should not throw
        self.fs.release('/non-existent', 'ignored')

    def test_read(self):
        tmp_file = self._prep_file()
        try:
            read = self.fs.read('file', 10, 0)
            self.assertEquals('abc' + aksyfs.EOF, read)
        finally:
            os.close(tmp_file)

    def test_mknod_write(self):
        path = '/memory/Sample100.wav'
        self.fs.mknod(path, 0, 'ignored')
        self.fs.open('/memory/Sample100.wav', S_IRUSR)
        self.fs.write(path, 'abc', 0)
        self.fs.release(path, 'ignored')
        written = os.open(aksyfs._create_cache_path(path), os.O_RDONLY)
        try:
            self.assertEquals('abc', os.read(written, 3))
        finally:
            os.close(written)

    def test_rmdir(self):
        self.fs.getattr('/disks/Samples disk/Songs')
        path = '/disks/Samples disk/Songs/test'
        self.fs.mkdir(path, 'ignored')
        self.fs.getattr(path)
        self.fs.rmdir(path)
        # TODO: fix mock delete()
        # self.assertRaises(OSError, self.fs.getattr, path)
    
    def test_unlink(self):
        self.fs.getattr('/memory')
        path = '/memory/Boo.wav'
        self.fs.getattr(path)
        self.fs.unlink(path)
        self.assertRaises(OSError, self.fs.getattr, path)
    
    def _prep_file(self):
        tmp_file = tempfile.mkstemp('aksy_test')[0]
        os.write(tmp_file, 'abc')
        self.fs.root.file_cache['file'] = aksyfs.FileInfo('/memory/sample.wav', 
                                                          False, handle=tmp_file)
        return tmp_file

def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyfuse.tests.test_aksyfs')
