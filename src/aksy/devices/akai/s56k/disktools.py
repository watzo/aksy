
""" Python equivalent of akai section disktools

Methods to manipulate the samplers filesystem
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Disktools:
     def __init__(self, s56k):
          self.s56k = s56k
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x01', 'update_disklist', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x02', 'select_disk', (aksy.devices.akai.sysex_types.WORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x03', 'test_disk', (aksy.devices.akai.sysex_types.WORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x04', 'get_no_disks', (), (aksy.devices.akai.sysex_types.BYTE,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x05', 'get_disklist', (), (aksy.devices.akai.sysex_types.DISKLIST,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x09', 'get_curr_path', (), (aksy.devices.akai.sysex_types.STRING,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x0D', 'eject_disk', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x0D'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x10', 'get_no_subfolders', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x12', 'get_subfolder_names', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x13', 'set_curr_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x15', 'load_folder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x15'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x16', 'create_subfolder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x16'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x17', 'delete_subfolder', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x17'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x18', 'rename_subfolder', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x20', 'get_no_files', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x22', 'get_filenames', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x28', 'rename_file', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x28'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x29', 'delete_file', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x29'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x2A', 'load_file', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x2A'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x2B', 'load_file_and_deps', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x2B'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x2C', 'save', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x2C'] = comm
          comm = aksy.devices.akai.sysex.Command('^', '\x10\x2D', 'save_all', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), (), aksy.devices.akai.sysex_types.S56K_USERREF)
          self.commands['\x10\x2D'] = comm

     def update_disklist(self):
          """Update the list of disks connected
          """
          comm = self.commands.get('\x10\x01')
          return self.s56k.execute(comm, ())

     def select_disk(self, arg0):
          """Select Disk <Data1> = Disk Handle
          """
          comm = self.commands.get('\x10\x02')
          return self.s56k.execute(comm, (arg0, ))

     def test_disk(self, arg0):
          """Test if the disk is valid <Data1> = Disk Handle
          """
          comm = self.commands.get('\x10\x03')
          return self.s56k.execute(comm, (arg0, ))

     def get_no_disks(self):
          """Get the number of disks connected

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x10\x04')
          return self.s56k.execute(comm, ())

     def get_disklist(self):
          """Get list of all connected disks

          Returns:
               aksy.devices.akai.sysex_types.DISKLIST
          """
          comm = self.commands.get('\x10\x05')
          return self.s56k.execute(comm, ())

     def get_curr_path(self):
          """Get current path of current disk

          Returns:
               aksy.devices.akai.sysex_types.STRING
          """
          comm = self.commands.get('\x10\x09')
          return self.s56k.execute(comm, ())

     def eject_disk(self, arg0):
          """Eject Disk <Data1> = Disk Handle
          """
          comm = self.commands.get('\x10\x0D')
          return self.s56k.execute(comm, (arg0, ))

     def get_no_subfolders(self):
          """Get number of sub-folders in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.CWORD
          """
          comm = self.commands.get('\x10\x10')
          return self.s56k.execute(comm, ())

     def get_subfolder_names(self):
          """Get the names of all of the sub-folders in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.STRINGARRAY
          """
          comm = self.commands.get('\x10\x12')
          return self.s56k.execute(comm, ())

     def set_curr_folder(self, arg0):
          """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)
          """
          comm = self.commands.get('\x10\x13')
          return self.s56k.execute(comm, (arg0, ))

     def load_folder(self, arg0):
          """Load Folder: the selected folder, and all its contents (including subfolders)
          """
          comm = self.commands.get('\x10\x15')
          return self.s56k.execute(comm, (arg0, ))

     def create_subfolder(self, arg0):
          """Create Folder: Creates a sub-folder in the currently selected folder.
          """
          comm = self.commands.get('\x10\x16')
          return self.s56k.execute(comm, (arg0, ))

     def delete_subfolder(self, arg0):
          """Delete Sub-Folder.
          """
          comm = self.commands.get('\x10\x17')
          return self.s56k.execute(comm, (arg0, ))

     def rename_subfolder(self, arg0, arg1):
          """Rename Folder: <Data1> = name of folder to rename
          """
          comm = self.commands.get('\x10\x18')
          return self.s56k.execute(comm, (arg0, arg1, ))

     def get_no_files(self):
          """Get number of files in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.CWORD
          """
          comm = self.commands.get('\x10\x20')
          return self.s56k.execute(comm, ())

     def get_filenames(self):
          """Get the names of all of the files in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.STRINGARRAY
          """
          comm = self.commands.get('\x10\x22')
          return self.s56k.execute(comm, ())

     def rename_file(self, arg0, arg1):
          """Rename File
          """
          comm = self.commands.get('\x10\x28')
          return self.s56k.execute(comm, (arg0, arg1, ))

     def delete_file(self, arg0):
          """Delete File. <Data1> = name of file to delete.
          """
          comm = self.commands.get('\x10\x29')
          return self.s56k.execute(comm, (arg0, ))

     def load_file(self, arg0):
          """Load File <Data1> = name of file to load.
          """
          comm = self.commands.get('\x10\x2A')
          return self.s56k.execute(comm, (arg0, ))

     def load_file_and_deps(self, arg0):
          """Load File <Data1> = name of file to load. Will load the dependents as well
          """
          comm = self.commands.get('\x10\x2B')
          return self.s56k.execute(comm, (arg0, ))

     def save(self, arg0, arg1, arg2, arg3):
          """Save Memory Item to Disk <Data1> = Handle of Memory Item <Data2> = Type = (1=Multi; 2=Program; 3=Sample; 4=SMF) <Data3> = (0=Skip if file exists; 1=Overwrite existing files) <Data4> = (0=Don't save children; 1=Save Children)
          """
          comm = self.commands.get('\x10\x2C')
          return self.s56k.execute(comm, (arg0, arg1, arg2, arg3, ))

     def save_all(self, arg0, arg1):
          """Save All Memory Items to Disk <Data1> = Type = (0=All; 1=Multi; 2=Program; 3=Sample; 4=SMF) <Data2> = (0=Skip if file exists; 1=Overwrite existing files)
          """
          comm = self.commands.get('\x10\x2D')
          return self.s56k.execute(comm, (arg0, arg1, ))

