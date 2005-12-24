from unittest import TestCase, TestLoader
import logging

from aksy.device import Devices

z48 = Devices.get_instance('z48', 'usb')
log = logging.getLogger('aksy')

class TestDisktools(TestCase):
    def selectFirstDisk(self):
        disks = z48.disktools.get_disklist()
        if len(disks) > 0:
            z48.disktools.select_disk(disks[0].handle)
        else:
            log.error("selectFirstDisk: no disks found")

    def selectFirstFolder(self):
        foldernames = z48.disktools.get_subfolder_names()
        if len(foldernames) > 0:
            z48.disktools.set_curr_folder(foldernames[0])
        else:
            log.error('selectFirstFolder: no folder to select')

    def test_update_disklist(self):
        # z48.disktools.update_disklist()
        # ra
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

    def test_get_no_subfolders(self):
        self.selectFirstDisk()

    def test_get_subfolder_names(self):
        self.selectFirstDisk()
        foldernames = z48.disktools.get_subfolder_names()
        log.debug('test_get_subfolder_names' + repr(foldernames))
        self.assertEquals(z48.disktools.get_no_subfolders(), len(foldernames))

    def test_set_curr_folder(self):
        self.selectFirstDisk()
        self.selectFirstFolder()

    def test_load_folder(self):
        pass # z48.disktools.load_folder()

    def test_create_rename_del_subfolder(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
        z48.disktools.create_subfolder('test')
        z48.disktools.rename_subfolder('test', 'testnew')
        z48.disktools.del_subfolder('testnew')

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

    """
    def test_rename_file(self):
        z48.rename_file()

    def test_delete_file(self):
        z48.delete_file()

    def test_load_file(self):
        z48.load_file()

    def test_load_file_and_deps(self):
        z48.load_file_and_deps("test")

    def test_save(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
		handle = z48.programtools.get_handle_by_name("test")
        z48.save(handle, False ,False)

    def test_save_all(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
        z48.save_all(0, False)
    """

def test_suite():
    testloader = TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.z48.tests.test_disktools')
    return suite
