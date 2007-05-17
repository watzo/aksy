from unittest import TestCase, TestLoader
import logging

from aksyfuse import aksyfs
from aksy.device import Devices
from stat import S_ISDIR, S_ISREG, ST_MODE, ST_SIZE, S_IRUSR, S_IRGRP
import os, errno, tempfile

z48 = Devices.get_instance('mock_z48', None)
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

class AksyFSTest(TestCase):
    def _assertdir(self, info):
        self.assertTrue(S_ISDIR(info[ST_MODE]))
        
    def setUp(self):
        self.fs = aksyfs.AksyFS(z48)
        
    def test_getattr(self):
        info = self.fs.getattr('/')
        self.assertTrue(S_ISDIR(info[ST_MODE]))
    
    def test_getattr_unsupported(self):
        self.assertRaises(OSError, self.fs.getattr, '/test.doc')
        
    def test_getdir(self):
        self.fs.getattr('/')
        root = self.fs.getdir('/')
        self.assertEquals([('memory', 0), ('disks', 0)], root)
    
    def test_getdir_memory(self):
        self.fs.getattr('/memory')
        memory = self.fs.getdir('/memory')
        self.assertEquals(102, len(memory))
        self.assertEquals(('Boo.wav', 0), memory[0])
        
    def test_getattr_memory(self):
        self.fs.getattr('/memory')
        info = self.fs.getattr('/memory/Boo.wav')
        self.assertTrue(S_ISREG(info[ST_MODE]))

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

    def test_mkdir_readonly_fs(self):
        self.assertRaises(IOError, self.fs.mkdir, '/disks/Cdrom/test', 'mode_ignored')
    
    def test_mkdir(self):
        self.fs.getattr('/disks/Samples disk/Songs')
        self.assertEquals([], self.fs.getdir('/disks/Samples disk/Songs'))
        self.fs.mkdir('/disks/Samples disk/Songs/test', 'mode_ignored')
        self.assertEquals([('/disks/Samples disk/Songs/test', 0)], self.fs.getdir('/disks/Samples disk/Songs'))

    def test_open(self):
        self.assertRaises(OSError, self.fs.open, '/memory/Sample99.wav', S_IRUSR)

        try:
            self.fs.open('/disks/Cdrom/Mellotron/Choir/Choir.AKP', S_IRUSR)
            self.fail()
        except OSError, (exc):
            self.assertEquals(errno.ENOENT, exc.errno)
            self.assertTrue(
                exc.filename.endswith('.aksy/cache/Cdrom/Mellotron/Choir/Choir.AKP'))

    def test_release(self):
        # should not throw
        self.fs.release('/non-existent', 'ignored')
    
    def test_read(self):
        tmp_file = self._prep_file()
        try:
            read = self.fs.read('file', 3, 0)
            self.assertEquals('abc', read)
        finally:
            os.close(tmp_file)

    def _prep_file(self):
        tmp_file = tempfile.mkstemp('test')[0]
        os.write(tmp_file, 'abc')
        self.fs.root.file_cache['file'] = tmp_file
        return tmp_file

def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyfuse.tests.test_aksyfs')
