from unittest import TestCase, TestLoader
import logging

from aksy.device import Devices
from tests.aksy.util import testutil
from aksyfs import ftpd, common
from stat import S_ISDIR, S_ISREG, ST_MODE, ST_SIZE, S_IRUSR
import os, tempfile

log = logging.getLogger('aksy')

class AksyFtpFSTest(TestCase): #IGNORE:R0904
    def _assertdir(self, info):
        self.assertTrue(S_ISDIR(info.st_mode))
        
    def setUp(self):
        sampler = Devices.get_instance('mock_z48', 'mock', debug=0)
        sampler.set_sample(testutil.get_test_resource('test.wav'))
        sampler.set_program(testutil.get_test_resource('221 Angel.akp'))
        self.fs = ftpd.AksyFtpFS(sampler)
        self.fs.getattr('/')
        self.fs.getattr('/disks')
        self.fs.getattr('/memory')
        
    def test_translate(self):
        self.assertEqual('/disks/Z48/!@#$%.wav', 
                          self.fs.translate('/disks/Z48/!@#$%.wav'))

    def test_getattr(self):
        info = self.fs.getattr('/')
        self._assertdir(info)
    
    def test_getattr_unsupported(self):
        self.assertRaises(OSError, self.fs.getattr, '/test.doc')

    def test_getattr_memory(self):
        info = self.fs.getattr('/memory/Boo.wav')
        self.assertTrue(S_ISREG(info.st_mode))
        
    def test_listdir(self):
        self.fs.getattr('/')
        root = self.fs.listdir('/')
        self.assert_dirlist(('memory', 'disks'), root)

    def test_listdir_memory(self):
        memory = list(self.fs.listdir('/memory'))
        self.assertEqual(102, len(memory))
        self.assertEqual('Boo.wav', memory[0])

    def test_getattr_memory_non_existing(self):
        self.assertRaises(OSError, self.fs.getattr, '/memory/subdir')

    def test_getattr_rootdisk(self):
        info = self.fs.getattr('/disks')
        self._assertdir(info)

    def test_listdir_rootdisk(self):
        children = self.fs.listdir('/disks')
        self.assert_dirlist(('Samples disk', 'Cdrom',), children)

    def test_listdir_with_spaces(self):
        info  = self.fs.getattr('/disks/Cdrom')
        self.assert_dirlist(('Mellotron Samples',), self.fs.listdir('/disks/Cdrom'))
        
    def test_listdir_disk(self):
        info  = self.fs.getattr('/disks/Samples disk')
        self._assertdir(info)
        children = self.fs.listdir('/disks/Samples disk')
        self.assert_dirlist(('Autoload', 'Songs'), children)

    def test_listdir_disk_nested(self):
        self.fs.getattr('/disks/Cdrom')
        info  = self.fs.getattr('/disks/Cdrom/Mellotron Samples')
        children  = self.fs.listdir('/disks/Cdrom/Mellotron Samples')
        self.assert_dirlist(('Choir','A Sample.AKP','Sample.wav'), children)

    def assert_dirlist(self, expected, actual):
        self.assertEqual(tuple(expected), tuple(actual))
            
    def test_mkdir_unsupported(self):
        self.assertRaises(OSError, self.fs.mkdir, '/memory/subdir')

    def test_mkdir_readonly_fs(self):
        self.fs.getattr('/disks/Cdrom')
        self.assertRaises(OSError, self.fs.mkdir, '/disks/Cdrom/test')
    
    def test_mkdir(self):
        self.fs.getattr('/disks/Samples disk')
        self.fs.getattr('/disks/Samples disk/Songs')
        self.assert_dirlist([], self.fs.listdir('/disks/Samples disk/Songs'))
        newdir = '/disks/Samples disk/Songs/test'
        self.fs.mkdir(newdir)
        self.assert_dirlist(('test',), 
                          self.fs.listdir('/disks/Samples disk/Songs'))
        self.assertNotEqual(None, self.fs.getattr(newdir))

    def test_open_disk(self):
        self.fs.getattr('/disks/Cdrom')
        self.fs.getattr('/disks/Cdrom/Mellotron Samples')
        self.fs.getattr('/disks/Cdrom/Mellotron Samples/Choir')
        f = self.fs.open('/disks/Cdrom/Mellotron Samples/Choir/Choir.AKP', 'rb')
        f.close()

    def test_read(self):
        f = self.fs.open('/memory/Sample100.wav', 'rb')
        try:
            read = f.read(4)
            self.assertEqual('RIFF', read)
        finally:
            f.close()

    def test_mknod_write(self):
        path = '/memory/Sample100.wav'
        f = self.fs.open('/memory/Sample100.wav', 'wb')
        f.write('abc')
        f.close()
        written = os.open(common._create_cache_path(path), os.O_RDONLY)
        try:
            self.assertEqual('abc', os.read(written, 3))
        finally:
            os.close(written)

    def test_rmdir(self):
        self.fs.getattr('/disks/Samples disk')
        self.fs.getattr('/disks/Samples disk/Songs')
        path = '/disks/Samples disk/Songs/test'
        self.fs.mkdir(path)
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
        
    def test_remove(self):
        self.fs.getattr('/memory')
        path = '/memory/Boo.wav'
        self.fs.getattr(path)
        self.fs.remove(path)
        self.assertRaises(OSError, self.fs.getattr, path)
    
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('tests.aksyfs.tests.test_ftpd')
