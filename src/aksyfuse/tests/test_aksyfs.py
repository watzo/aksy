from unittest import TestCase, TestLoader
from aksyfuse import aksyfs
from aksy.device import Devices
from stat import S_ISDIR, S_ISREG, ST_MODE
import os

z48 = Devices.get_instance('mock_z48', None)

class TestModuleTest(TestCase):
    def test_stat_directory(self):
        info = aksyfs.stat_dir(1000, 1000)
        self.assertTrue(S_ISDIR(info[ST_MODE]))
        self.assertEquals(len(os.stat('/')), len(info))

    def test_stat_file(self):
        info = aksyfs.stat_file(1000, 1000)
        self.assertFalse(S_ISDIR(info[ST_MODE]))
        self.assertEquals(len(os.stat('/')), len(info))

class AksyFSTest(TestCase):
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
        
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyfuse.tests.test_aksyfs')
