
""" Python equivalent of akai section disktools

Methods to manipulate the sampler's filesystem
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Disktools:
    def __init__(self, s56k):
        self.sampler = s56k
        self.update_disklist_cmd = Command('^', '\x10\x01', 'disktools', 'update_disklist', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.select_disk_cmd = Command('^', '\x10\x02', 'disktools', 'select_disk', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.test_disk_cmd = Command('^', '\x10\x03', 'disktools', 'test_disk', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_disks_cmd = Command('^', '\x10\x04', 'disktools', 'get_no_disks', (), (aksy.devices.akai.sysex_types.BYTE,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_disklist_cmd = Command('^', '\x10\x05', 'disktools', 'get_disklist', (), (aksy.devices.akai.sysex_types.S56KDISKLIST,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_path_cmd = Command('^', '\x10\x09', 'disktools', 'get_curr_path', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.eject_disk_cmd = Command('^', '\x10\x0D', 'disktools', 'eject_disk', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_folders_cmd = Command('^', '\x10\x10', 'disktools', 'get_no_folders', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_folder_names_cmd = Command('^', '\x10\x12', 'disktools', 'get_folder_names', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.open_folder_cmd = Command('^', '\x10\x13', 'disktools', 'open_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.close_folder_cmd = Command('^', '\x10\x14', 'disktools', 'close_folder', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.load_folder_cmd = Command('^', '\x10\x15', 'disktools', 'load_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.create_folder_cmd = Command('^', '\x10\x16', 'disktools', 'create_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_folder_cmd = Command('^', '\x10\x17', 'disktools', 'delete_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.rename_folder_cmd = Command('^', '\x10\x18', 'disktools', 'rename_folder', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_files_cmd = Command('^', '\x10\x20', 'disktools', 'get_no_files', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_filenames_cmd = Command('^', '\x10\x22', 'disktools', 'get_filenames', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.rename_file_cmd = Command('^', '\x10\x28', 'disktools', 'rename_file', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_file_cmd = Command('^', '\x10\x29', 'disktools', 'delete_file', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.load_file_cmd = Command('^', '\x10\x2A', 'disktools', 'load_file', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.load_file_and_deps_cmd = Command('^', '\x10\x2B', 'disktools', 'load_file_and_deps', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.save_cmd = Command('^', '\x10\x2C', 'disktools', 'save', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.save_all_cmd = Command('^', '\x10\x2D', 'disktools', 'save_all', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), (), aksy.devices.akai.sysex_types.S56K_USERREF)

    def update_disklist(self):
        """Update the list of disks connected
        """
        return self.sampler.execute(self.update_disklist_cmd, ())

    def select_disk(self, arg0):
        """Select Disk <Data1> = Disk Handle
        """
        return self.sampler.execute(self.select_disk_cmd, (arg0, ))

    def test_disk(self, arg0):
        """Test if the disk is valid <Data1> = Disk Handle
        """
        return self.sampler.execute(self.test_disk_cmd, (arg0, ))

    def get_no_disks(self):
        """Get the number of disks connected

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_disks_cmd, ())

    def get_disklist(self):
        """Get list of all connected disks

        Returns:
            DISKLIST
        """
        return self.sampler.execute(self.get_disklist_cmd, ())

    def get_curr_path(self):
        """Get current path of current disk

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_curr_path_cmd, ())

    def eject_disk(self, arg0):
        """Eject Disk <Data1> = Disk Handle
        """
        return self.sampler.execute(self.eject_disk_cmd, (arg0, ))

    def get_no_folders(self):
        """Get number of sub-folders in the current folder.

        Returns:
            CWORD
        """
        return self.sampler.execute(self.get_no_folders_cmd, ())

    def get_folder_names(self):
        """Get the names of all of the sub-folders in the current folder.

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_folder_names_cmd, ())

    def open_folder(self, arg0):
        """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)
        """
        return self.sampler.execute(self.open_folder_cmd, (arg0, ))

    def close_folder(self):
        """Move up one level in the folder hierarchy. If this is used on a root folder, an ERROR confirmation message will be returned.
        """
        return self.sampler.execute(self.close_folder_cmd, ())

    def load_folder(self, arg0):
        """Load Folder: the selected folder, and all its contents (including subfolders)
        """
        return self.sampler.execute(self.load_folder_cmd, (arg0, ))

    def create_folder(self, arg0):
        """Create Folder: Creates a sub-folder in the currently selected folder.
        """
        return self.sampler.execute(self.create_folder_cmd, (arg0, ))

    def delete_folder(self, arg0):
        """Delete Sub-Folder.
        """
        return self.sampler.execute(self.delete_folder_cmd, (arg0, ))

    def rename_folder(self, arg0, arg1):
        """Rename Folder: <Data1> = name of folder to rename
        """
        return self.sampler.execute(self.rename_folder_cmd, (arg0, arg1, ))

    def get_no_files(self):
        """Get number of files in the current folder.

        Returns:
            CWORD
        """
        return self.sampler.execute(self.get_no_files_cmd, ())

    def get_filenames(self):
        """Get the names of all of the files in the current folder.

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_filenames_cmd, ())

    def rename_file(self, arg0, arg1):
        """Rename File
        """
        return self.sampler.execute(self.rename_file_cmd, (arg0, arg1, ))

    def delete_file(self, arg0):
        """Delete File. <Data1> = name of file to delete.
        """
        return self.sampler.execute(self.delete_file_cmd, (arg0, ))

    def load_file(self, arg0):
        """Load File <Data1> = name of file to load.
        """
        return self.sampler.execute(self.load_file_cmd, (arg0, ))

    def load_file_and_deps(self, arg0):
        """Load File <Data1> = name of file to load. Will load the dependents as well
        """
        return self.sampler.execute(self.load_file_and_deps_cmd, (arg0, ))

    def save(self, arg0, arg1, arg2, arg3):
        """Save Memory Item to Disk <Data1> = Handle of Memory Item <Data2> = Type = (1=Multi; 2=Program; 3=Sample; 4=SMF) <Data3> = (0=Skip if file exists; 1=Overwrite existing files) <Data4> = (0=Don't save children; 1=Save Children)
        """
        return self.sampler.execute(self.save_cmd, (arg0, arg1, arg2, arg3, ))

    def save_all(self, arg0, arg1):
        """Save All Memory Items to Disk <Data1> = Type = (0=All; 1=Multi; 2=Program; 3=Sample; 4=SMF) <Data2> = (0=Skip if file exists; 1=Overwrite existing files)
        """
        return self.sampler.execute(self.save_all_cmd, (arg0, arg1, ))

