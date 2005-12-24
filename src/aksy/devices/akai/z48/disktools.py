
""" Disktools

Methods to manipulate the samplers filesystem
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex

class Disktools:
     def __init__(self, z48):
          self.z48 = z48
          self.update_disklist_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x01', 'update_disklist', (), None,
              userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.select_disk_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x02', 'select_disk', (aksy.devices.akai.sysex_types.WORD,), None,
              userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.test_disk_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x03', 'test_disk', (aksy.devices.akai.sysex_types.WORD,), None)
          self.get_no_disks_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x04', 'get_no_disks', (), None)
          self.get_disklist_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x05', 'get_disklist', (),
              (aksy.devices.akai.sysex_types.DISKLIST,), userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.get_curr_path_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x09', 'get_curr_path', (), None)
          self.eject_disk_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x0D', 'eject_disk', (aksy.devices.akai.sysex_types.WORD,), None)
          self.get_no_folders_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x10', 'get_no_folders', (), None)
          self.get_folder_names_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x12', 'get_folder_names', (),
              (aksy.devices.akai.sysex_types.STRINGARRAY,), userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.open_folder_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x13', 'open_folder', (aksy.devices.akai.sysex_types.STRING,), None)
          self.load_folder_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x15', 'load_folder', (aksy.devices.akai.sysex_types.STRING,),
              None, userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.create_folder_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x16', 'create_folder', (aksy.devices.akai.sysex_types.STRING,), None)
          self.del_folder_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x17', 'delete_folder', (aksy.devices.akai.sysex_types.STRING,), None)
          self.rename_folder_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x18', 'rename_folder', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), None)
          self.get_no_files_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x20', 'get_no_files', (),
              (aksy.devices.akai.sysex_types.WORD,), userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.get_filenames_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x22', 'get_filenames', (),
              (aksy.devices.akai.sysex_types.STRINGARRAY,), userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.rename_file_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x28', 'rename_file', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), None)
          self.delete_file_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x29', 'delete_file', (aksy.devices.akai.sysex_types.STRING,), None,
              userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.load_file_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x2A', 'load_file', (aksy.devices.akai.sysex_types.STRING,), None,
               userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.load_file_and_deps_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x20\x2B', 'load_file_and_deps', (aksy.devices.akai.sysex_types.STRING,), None,
               userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.save_cmd = aksy.devices.akai.sysex.Command('\x5e', '\x10\x2C', 'save',
              (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.FILETYPE, aksy.devices.akai.sysex_types.BOOL,
               aksy.devices.akai.sysex_types.BOOL), None,
               userref_type=aksy.devices.akai.sysex_types.S56K_USERREF)
          self.save_all_cmd = aksy.devices.akai.sysex.Command('\x5f', '\x20\x2D', 'save_all', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL, aksy.devices.akai.sysex_types.BOOL), None,
             userref_type=aksy.devices.akai.sysex_types.USERREF)

     def update_disklist(self):
          """Update the list of disks connected
          """
          return self.z48.execute(self.update_disklist_cmd, ())

     def select_disk(self, arg0):
          """Select Disk <Data1> = Disk Handle
          """
          return self.z48.execute(self.select_disk_cmd, (arg0, ))

     def test_disk(self, arg0):
          """Test if the disk is valid <Data1> = Disk Handle
          """
          return self.z48.execute(self.test_disk_cmd, (arg0, ))

     def get_no_disks(self):
          """Get the number of disks connected

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          return self.z48.execute(self.get_no_disks_cmd, ())

     def get_disklist(self):
          """Get list of all connected disks

          Returns:
              a list of aksy.devices.akai.sysex_types.DiskInfo objects
          """
          return self.z48.execute(self.get_disklist_cmd, ())

     def get_curr_path(self):
          """Get current path of current disk

          Returns:
               aksy.devices.akai.sysex_types.STRING
          """
          return self.z48.execute(self.get_curr_path_cmd, ())

     def eject_disk(self, arg0):
          """Eject Disk <Data1> = Disk Handle
          """
          return self.z48.execute(self.eject_disk_cmd, (arg0, ))

     def get_no_folders(self):
          """Get number of sub-folders in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.WORD
          """
          return self.z48.execute(self.get_no_folders_cmd, ())

     def get_folder_names(self):
          """Get the names of all of the sub-folders in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.STRINGARRAY
          """
          return self.z48.execute(self.get_folder_names_cmd, ())

     def open_folder(self, arg0):
          """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)
          """
          return self.z48.execute(self.open_folder_cmd, (arg0, ))

     def load_folder(self, arg0):
          """Load Folder: the selected folder, and all its contents (including folders)
          """
          return self.z48.execute(self.load_folder_cmd, (arg0, ))

     def create_folder(self, arg0):
          """Create Folder: Creates a folder in the currently selected folder.
          """
          return self.z48.execute(self.create_folder_cmd, (arg0, ))

     def delete_folder(self, arg0):
          """Delete Folder.
          """
          return self.z48.execute(self.del_folder_cmd, (arg0, ))

     def rename_folder(self, arg0, arg1):
          """Rename Folder: <Data1> = name of folder to rename
          """
          return self.z48.execute(self.rename_folder_cmd, (arg0, arg1, ))

     def get_no_files(self):
          """Get number of files in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.WORD
          """
          return self.z48.execute(self.get_no_files_cmd, ())

     def get_filenames(self):
          """Get the names of all of the files in the current folder.

          Returns:
               aksy.devices.akai.sysex_types.STRINGARRAY
          """
          return self.z48.execute(self.get_filenames_cmd, ())

     def rename_file(self, arg0, arg1):
          """Rename File
          """
          return self.z48.execute(self.rename_file_cmd, (arg0, arg1, ))

     def delete_file(self, arg0):
          """Delete File <Data1> = name of file to delete.
          """
          return self.z48.execute(self.delete_file_cmd, (arg0, ))

     def load_file(self, arg0):
          """Load File <Data1> = name of file to load.
          """
          return self.z48.execute(self.load_file_cmd, (arg0, ))

     def load_file_and_deps(self, arg0):
          """Load File <Data1> = name of file to load. Will load the dependents as well
          """
          return self.z48.execute(self.load_file_and_deps_cmd, (arg0, ))

     def save(self, arg0, arg1, arg2, arg3):
          """Save Memory Item to Disk
          <Data1> = Handle of Memory Item
          <Data2> = Type = (1=Multi; 2=Program; 3=Sample; 4=SMF)
          <Data3> = (0=Skip if file exists; 1=Overwrite existing files)
          <Data4> = (0=Don't save children; 1=Save Children)
          """
          return self.z48.execute(self.save_cmd, (arg0, arg1, arg2, arg3, ))

     def save_all(self, arg0, arg1, arg2):
          """Save All Memory Items to Disk
          <Data1> = Type = (0=All; 1=Multi; 2=Program; 3=Sample; 4=SMF)
          <Data2> = (0=Skip if file exists; 1=Overwrite existing files)
          <Data4> = (0=Don't save children; 1=Save Children)
          """
          return self.z48.execute(self.save_all_cmd, (arg0, arg1, arg2))