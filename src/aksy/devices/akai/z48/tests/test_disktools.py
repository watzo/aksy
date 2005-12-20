from unittest import TestCase, TestLoader

from aksy.device import Devices

logfile = open('test_disktools.log', 'w')

def log(method_name, msg):
    logfile.writelines("%s: %s" %(method_name, msg))

#TODO: timings

class TestDisktools(TestCase):
    def setUp(self):
		if not hasattr(self, 'z48'):
	        self.z48 = Devices.get_instance('akai', 'usb')

    def selectFirstDisk(self):
        disks = self.z48.disktools.get_disklist()
        if len(disks) > 0:
            self.z48.disktools.select_disk(disks[0].handle)
        else:
            log("selectFirstDisk", "no disks found")

    def selectFirstFolder(self):
        foldernames = self.z48.disktools.get_subfolder_names()
        if len(foldernames) > 0:
            self.z48.disktools.set_curr_folder(foldernames[0])
        else:
            log('selectFirstFolder', 'no folder to select')
            
    def test_update_disklist(self):
        self.z48.disktools.update_disklist()

    def test_select_disk(self):
        for disk in self.z48.get_disklist():
            self.z48.disktools.select_disk(disk.handle)

    def test_test_disk(self):
        disks = self.z48.get_disklist()
        for disk in self.z48.get_disklist():
            self.z48.disktools.test_disk(disk.handle)

    def test_get_disklist(self):
        disks = self.z48.disktools.get_disklist()
        log('test_get_disklist', repr(disks))
        self.assertEquals(self.z48.disktools.get_no_disks(), len(disks))

    def test_get_curr_path(self):
        self.selectFirstDisk()
        self.assertEquals('\\', self.z48.disktools.get_curr_path())

    def test_eject_disk(self):
        pass
        #self.z48.eject_disk()

    def test_get_no_subfolders(self):
        self.selectFirstDisk()

    def test_get_subfolder_names(self):
        self.selectFirstDisk()
        foldernames = self.z48.disktools.get_subfolder_names()
        log('test_get_subfolder_names', repr(foldernames))
        self.assertEquals(self.z48.disktools.get_no_subfolders(), len(foldernames))

    def test_set_curr_folder(self):
        self.selectFirstDisk()
        self.selectFirstFolder()

    def test_load_folder(self):
        pass # self.z48.disktools.load_folder()

    def test_create_rename_del_subfolder(self):
        self.z48.disktools.create_subfolder('test')
        self.z48.disktools.rename_subfolder('test', 'testnew')
        self.z48.disktools.del_subfolder('testnew')

    """
    def test_get_no_files(self):
        self.z48.get_no_files()

    def test_get_filenames(self):
        self.z48.get_filenames()

    def test_rename_file(self):
        self.z48.rename_file()

    def test_delete_file(self):
        self.z48.delete_file()

    def test_load_file(self):
        self.z48.load_file()

    def test_load_file_and_deps(self):
        self.z48.load_file_and_deps("test")

    def test_save(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
		handle = self.z48.programtools.get_handle_by_name("test")
        self.z48.save(handle, False ,False)

    def test_save_all(self):
        self.selectFirstDisk()
        self.selectFirstFolder()
        self.z48.save_all(0, False)
    """

def test_suite():
    testloader = TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.z48.tests.test_disktools')
    return suite
