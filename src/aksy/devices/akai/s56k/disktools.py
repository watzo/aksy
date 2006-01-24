
""" Python equivalent of akai section disktools

Methods to manipulate the samplers filesystem
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Disktools:
    def __init__(self, s56k):
        self.s56k = s56k
        self.update_disklist_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x01', 'update_disklist', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.select_disk_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x02', 'select_disk', (aksy.devices.akai.sysex_types.WORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.test_disk_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x03', 'test_disk', (aksy.devices.akai.sysex_types.WORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_disks_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x04', 'get_no_disks', (), (aksy.devices.akai.sysex_types.BYTE,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_disklist_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x05', 'get_disklist', (), (aksy.devices.akai.sysex_types.DISKLIST,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_path_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x09', 'get_curr_path', (), (aksy.devices.akai.sysex_types.STRING,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.eject_disk_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x0D', 'eject_disk', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_subfolders_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x10', 'get_no_subfolders', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_subfolder_names_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x12', 'get_subfolder_names', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.open_folder_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x13', 'open_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.load_folder_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x15', 'load_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.create_subfolder_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x16', 'create_subfolder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_subfolder_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x17', 'delete_subfolder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.rename_subfolder_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x18', 'rename_subfolder', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_files_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x20', 'get_no_files', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_filenames_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x22', 'get_filenames', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.rename_file_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x28', 'rename_file', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_file_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x29', 'delete_file', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.load_file_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x2A', 'load_file', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.load_file_and_deps_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x2B', 'load_file_and_deps', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.save_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x2C', 'save', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.save_all_cmd = aksy.devices.akai.sysex.Command('^', '\x10\x2D', 'save_all', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), (), aksy.devices.akai.sysex_types.S56K_USERREF)

    def update_disklist(self):
        """Update the list of disks connected
        """
        return self.s56k.execute(self.update_disklist_cmd, ())

    def select_disk(self, arg0):
        """Select Disk <Data1> = Disk Handle
        """
        return self.s56k.execute(self.select_disk_cmd, (arg0, ))

    def test_disk(self, arg0):
        """Test if the disk is valid <Data1> = Disk Handle
        """
        return self.s56k.execute(self.test_disk_cmd, (arg0, ))

    def get_no_disks(self):
        """Get the number of disks connected

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.s56k.execute(self.get_no_disks_cmd, ())

    def get_disklist(self):
        """Get list of all connected disks

        Returns:
            aksy.devices.akai.sysex_types.DISKLIST
        """
        return self.s56k.execute(self.get_disklist_cmd, ())

    def get_curr_path(self):
        """Get current path of current disk

        Returns:
            aksy.devices.akai.sysex_types.STRING
        """
        return self.s56k.execute(self.get_curr_path_cmd, ())

    def eject_disk(self, arg0):
        """Eject Disk <Data1> = Disk Handle
        """
        return self.s56k.execute(self.eject_disk_cmd, (arg0, ))

    def get_no_subfolders(self):
        """Get number of sub-folders in the current folder.

        Returns:
            aksy.devices.akai.sysex_types.CWORD
        """
        return self.s56k.execute(self.get_no_subfolders_cmd, ())

    def get_subfolder_names(self):
        """Get the names of all of the sub-folders in the current folder.

        Returns:
            aksy.devices.akai.sysex_types.STRINGARRAY
        """
        return self.s56k.execute(self.get_subfolder_names_cmd, ())

    def open_folder(self, arg0):
        """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)
        """
        return self.s56k.execute(self.open_folder_cmd, (arg0, ))

    def load_folder(self, arg0):
        """Load Folder: the selected folder, and all its contents (including subfolders)
        """
        return self.s56k.execute(self.load_folder_cmd, (arg0, ))

    def create_subfolder(self, arg0):
        """Create Folder: Creates a sub-folder in the currently selected folder.
        """
        return self.s56k.execute(self.create_subfolder_cmd, (arg0, ))

    def delete_subfolder(self, arg0):
        """Delete Sub-Folder.
        """
        return self.s56k.execute(self.delete_subfolder_cmd, (arg0, ))

    def rename_subfolder(self, arg0, arg1):
        """Rename Folder: <Data1> = name of folder to rename
        """
        return self.s56k.execute(self.rename_subfolder_cmd, (arg0, arg1, ))

    def get_no_files(self):
        """Get number of files in the current folder.

        Returns:
            aksy.devices.akai.sysex_types.CWORD
        """
        return self.s56k.execute(self.get_no_files_cmd, ())

    def get_filenames(self):
        """Get the names of all of the files in the current folder.

        Returns:
            aksy.devices.akai.sysex_types.STRINGARRAY
        """
        return self.s56k.execute(self.get_filenames_cmd, ())

    def rename_file(self, arg0, arg1):
        """Rename File
        """
        return self.s56k.execute(self.rename_file_cmd, (arg0, arg1, ))

    def delete_file(self, arg0):
        """Delete File. <Data1> = name of file to delete.
        """
        return self.s56k.execute(self.delete_file_cmd, (arg0, ))

    def load_file(self, arg0):
        """Load File <Data1> = name of file to load.
        """
        return self.s56k.execute(self.load_file_cmd, (arg0, ))

    def load_file_and_deps(self, arg0):
        """Load File <Data1> = name of file to load. Will load the dependents as well
        """
        return self.s56k.execute(self.load_file_and_deps_cmd, (arg0, ))

    def save(self, arg0, arg1, arg2, arg3):
        """Save Memory Item to Disk <Data1> = Handle of Memory Item <Data2> = Type = (1=Multi; 2=Program; 3=Sample; 4=SMF) <Data3> = (0=Skip if file exists; 1=Overwrite existing files) <Data4> = (0=Don't save children; 1=Save Children)
        """
        return self.s56k.execute(self.save_cmd, (arg0, arg1, arg2, arg3, ))

    def save_all(self, arg0, arg1):
        """Save All Memory Items to Disk <Data1> = Type = (0=All; 1=Multi; 2=Program; 3=Sample; 4=SMF) <Data2> = (0=Skip if file exists; 1=Overwrite existing files)
        """
        return self.s56k.execute(self.save_all_cmd, (arg0, arg1, ))

