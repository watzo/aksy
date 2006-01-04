from unittest import TestCase, TestLoader
import logging, time

from aksyxusb import AkaiSampler
from aksy.device import Devices
from aksy.devices.akai import sysex_types

z48 = Devices.get_instance('z48', 'usb')
log = logging.getLogger('aksy')

TESTFOLDER_NAME = "test%s" % time.time()
class TestDisktools(TestCase):
    def selectFirstDisk(self):
        disks = z48.disktools.get_disklist()
        if len(disks) > 0:
            z48.disktools.select_disk(disks[0].handle)
        else:
            log.error("selectFirstDisk: no disks found")

    def selectFirstFolder(self):
        foldernames = z48.disktools.get_folder_names()
        if len(foldernames) > 0:
            z48.disktools.open_folder(foldernames[0])
        else:
            log.error('selectFirstFolder: no folder to select')

    def createSelectTestFolder(self):
        z48.disktools.create_folder(TESTFOLDER_NAME)
        z48.disktools.set_curr_folder(TESTFOLDER_NAME)

    def test_update_disklist(self):
        # this command works, but takes too long to execute
        # z48.disktools.update_disklist()
        pass

    def test_select_disk(self):
        for disk in z48.disktools.get_disklist():
            z48.disktools.select_disk(disk.handle)

    def test_test_disk(self):
        disks = z48.disktools.get_disklist()
        for disk in z48.disktools.get_disklist():
            z48.disktools.test_disk(disk.handle)

    def test_get_disklist(self):
        disks = z48.disktools.get_disklist()
        log.info('test_get_disklist: ' + repr(disks))
        self.assertEquals(z48.disktools.get_no_disks(), len(disks))

    def test_get_curr_path(self):
        self.selectFirstDisk()
        self.assertEquals('\\', z48.disktools.get_curr_path())

    def test_eject_disk(self):
        pass
        #z48.eject_disk()

    def test_get_no_folders(self):
        self.selectFirstDisk()

    def test_get_folder_names(self):
        self.selectFirstDisk()
        foldernames = z48.disktools.get_folder_names()
        log.debug('test_get_folder_names: ' + repr(foldernames))
        self.assertEquals(z48.disktools.get_no_folders(), len(foldernames))

    def test_set_curr_folder(self):
        self.selectFirstDisk()
        self.selectFirstFolder()

    def test_load_folder(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        z48.disktools.set_curr_path("..")
        z48.disktools.load_folder("test")

    def test_create_rename_delete_folder(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
        z48.disktools.create_folder(TESTFOLDER_NAME)
        z48.disktools.rename_folder(TESTFOLDER_NAME, TESTFOLDER_NAME + 'new')
        z48.disktools.delete_folder(TESTFOLDER_NAME + 'new')

    def test_get_no_files(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
        log.info("test_get_no_files: %i" % z48.disktools.get_no_files())

    def test_get_filenames(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
        files = z48.disktools.get_filenames()
        log.info("test_get_filenames: %s" % repr(files))
        self.assertEquals(z48.disktools.get_no_files(), len(files))

    def test_rename_file(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        z48.put("test.wav", AkaiSampler.DISK)
        z48.disktools.rename_file("test.wav", "test2.wav")

    def test_load_file(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        z48.load_file("test.wav")

    def test_load_file_and_deps(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        z48.load_file_and_deps("test2.wav")

    def test_delete_file(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        z48.delete_file("test2.wav")

    def test_save(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        handle = z48.sampletools.get_handle_by_name("test2")
        z48.save(handle, sysex_types.FILETYPE.SAMPLE, False, False)

    def test_save_all(self):
        self.selectFirstDisk()
        self.createSelectTestFolder()
        z48.save_all(sysex_types.FILETYPE.ALL, False)

def test_suite():
    testloader = TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.z48.tests.test_disktools')
    return suite
