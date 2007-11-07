from unittest import TestCase, TestLoader
import logging, time, os.path, os

from aksyx import AkaiSampler
from aksy.device import Devices
from aksy.devices.akai import sysex_types

TESTDIR = os.path.abspath(os.path.split(__file__)[0])
TESTFOLDER_NAME = "test%s" % time.time()
AKSY_RUN_SLOW_TESTS =  bool(os.environ.get("AKSY_RUN_SLOW_TESTS", False))
LOG = logging.getLogger('aksy')

z48 = Devices.get_instance('mock_z48', 'mock')

class TestDisktools(TestCase):
    def setUp(self):
        self.selectFirstDisk()
        z48.disktools.create_folder(TESTFOLDER_NAME)
        
    def tearDown(self):
        z48.disktools.open_folder("")
        z48.disktools.delete(TESTFOLDER_NAME)
        
    def selectFirstDisk(self):
        disks = z48.disktools.get_disklist()
        if len(disks) > 0:
            z48.disktools.select_disk(disks[0][0])
        else:
            LOG.error("selectFirstDisk: no disks found")

    def selectFirstFolder(self):
        foldernames = z48.disktools.get_folder_names()
        if len(foldernames) > 0:
            z48.disktools.open_folder(foldernames[0])
        else:
            LOG.error('selectFirstFolder: no folder to select')

    def selectTestFolder(self):
        z48.disktools.open_folder(TESTFOLDER_NAME)

    def test_update_disklist(self):
        if AKSY_RUN_SLOW_TESTS: 
            z48.disktools.update_disklist()

    def test_select_disk(self):
        for disk in z48.disktools.get_disklist():
            z48.disktools.select_disk(disk[0])

    def test_test_disk(self):
        disks = z48.disktools.get_disklist()
        for disk in z48.disktools.get_disklist():
            z48.disktools.test_disk(disk[0])

    def test_get_disklist(self):
        disks = z48.disktools.get_disklist()
        LOG.info('test_get_disklist: ' + repr(disks))
        self.assertEquals(z48.disktools.get_no_disks(), len(disks))

    def test_get_curr_path(self):
        self.selectFirstDisk()
        self.assertEquals('\\', z48.disktools.get_curr_path())

    def test_eject_disk(self):
        for disk in z48.disktools.get_disklist():
            z48.disktools.eject_disk(disk[0])

    def test_folder_listings(self):
        foldernames = z48.disktools.get_folder_names()
        LOG.debug('test_get_folder_names: ' + repr(foldernames))
        self.assertEquals(z48.disktools.get_no_folders(), len(foldernames))

    def test_load_folder(self):
        self.selectTestFolder()
        z48.disktools.open_folder("..")
        z48.disktools.load_folder(TESTFOLDER_NAME)
        
    def test_create_rename_delete(self):
        self.selectTestFolder()
        z48.disktools.open_folder("..")
        z48.disktools.rename_folder(TESTFOLDER_NAME, TESTFOLDER_NAME + 'new')
        z48.disktools.delete(TESTFOLDER_NAME + 'new')

    def test_get_no_files(self):
        self.selectFirstFolder()
        LOG.info("test_get_no_files: %i" % z48.disktools.get_no_files())

    def test_get_filenames(self):
        self.selectFirstFolder()
        files = z48.disktools.get_filenames()
        LOG.info("test_get_filenames: %s" % repr(files))
        self.assertEquals(z48.disktools.get_no_files(), len(files))

    def test_rename_delete_file(self):
        self.selectTestFolder()
        z48.put(os.path.join(TESTDIR, "test.wav"), destination=AkaiSampler.DISK)
        z48.disktools.rename_file("test.wav", "test2.wav")
        z48.disktools.delete("test2.wav")

    def test_load_file_and_deps(self):
        self.selectTestFolder()
        z48.put(os.path.join(TESTDIR, "test.wav"), destination=AkaiSampler.DISK)
        z48.disktools.load_file_and_deps("test.wav")

    def test_load_save(self):
        self.selectTestFolder()
        z48.put(os.path.join(TESTDIR, "test.wav"), destination=AkaiSampler.DISK)
        z48.disktools.load_file("test.wav")

        handle = z48.sampletools.get_handle_by_name("test")
        z48.disktools.save(handle, sysex_types.FILETYPE.SAMPLE, True, False)

    def test_save_all(self):
        self.selectTestFolder()
        if AKSY_RUN_SLOW_TESTS:
            z48.disktools.save_all(sysex_types.FILETYPE.ALL, False, False)

def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('tests.aksy.devices.akai.z48.ftests.test_disktools')
