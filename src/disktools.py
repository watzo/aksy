
""" Python equivalent of akai section disktools

Methods to manipulate the samplers filesystem
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import sysex
def update_disklist(z48):
     """Update the list of disks connected

     Returns:
               
     """
     comm =  z48.get(('\x20','\x01'))
     return z48.execute(comm, ())

def select_disk(z48, arg):
     """Select Disk <Data1> = Disk Handle

     Returns:
               
     """
     comm =  z48.get(('\x20','\x02'))
     return z48.execute(comm, (arg, ))

def test_disk(z48, arg):
     """Test if the disk is valid <Data1> = Disk Handle

     Returns:
               
     """
     comm =  z48.get(('\x20','\x03'))
     return z48.execute(comm, (arg, ))

def get_no_disks(z48):
     """Get the number of disks connected

     Returns:
               
     """
     comm =  z48.get(('\x20','\x04'))
     return z48.execute(comm, ())

def get_disklist(z48):
     """Get list of all connected disks

     Returns:
          sysex.WORD
          sysex.BYTE
          sysex.BYTE
          sysex.BYTE
          sysex.BYTE
          sysex.STRING     
     """
     comm =  z48.get(('\x20','\x05'))
     return z48.execute(comm, ())

def get_curr_path(z48):
     """Get current path of current disk

     Returns:
          sysex.STRING     
     """
     comm =  z48.get(('\x20','\x09'))
     return z48.execute(comm, ())

def eject_disk(z48, arg):
     """Eject Disk <Data1> = Disk Handle

     Returns:
               
     """
     comm =  z48.get(('\x20','\x0D'))
     return z48.execute(comm, (arg, ))

def get_no_subfolders(z48):
     """Get number of sub-folders in the current folder.

     Returns:
               
     """
     comm =  z48.get(('\x20','\x10'))
     return z48.execute(comm, ())

def get_subfolder_names(z48):
     """Get the names of all of the sub-folders in the current folder.

     Returns:
          sysex.STRING     
     """
     comm =  z48.get(('\x20','\x12'))
     return z48.execute(comm, ())

def set_curr_folder(z48, arg):
     """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)

     Returns:
               
     """
     comm =  z48.get(('\x20','\x13'))
     return z48.execute(comm, (arg, ))

def load_folder(z48, arg):
     """Load Folder: the selected folder, and all its contents (including sub- 

     Returns:
               
     """
     comm =  z48.get(('\x20','\x15'))
     return z48.execute(comm, (arg, ))

def create_subfolder(z48, arg):
     """Create Folder: Creates a sub-folder in the currently selected folder.

     Returns:
               
     """
     comm =  z48.get(('\x20','\x16'))
     return z48.execute(comm, (arg, ))

def del_subfolder(z48, arg):
     """Delete Sub-Folder.

     Returns:
               
     """
     comm =  z48.get(('\x20','\x17'))
     return z48.execute(comm, (arg, ))

def rename_subfolder(z48, arg1, arg2):
     """Rename Folder: <Data1> = name of folder to rename

     Returns:
               
     """
     comm =  z48.get(('\x20','\x18'))
     return z48.execute(comm, (arg1, arg2, ))

def get_no_files(z48):
     """Get number of files in the current folder.

     Returns:
               
     """
     comm =  z48.get(('\x20','\x20'))
     return z48.execute(comm, ())

def get_filenames(z48):
     """Get the names of all of the files in the current folder.

     Returns:
          sysex.STRING     
     """
     comm =  z48.get(('\x20','\x22'))
     return z48.execute(comm, ())

def rename_file(z48, arg1, arg2):
     """ Rename File 

     Returns:
               
     """
     comm =  z48.get(('\x20','\x28'))
     return z48.execute(comm, (arg1, arg2, ))

def delete_file(z48, arg):
     """Delete File. <Data1> = name of file to delete.

     Returns:
               
     """
     comm =  z48.get(('\x20','\x29'))
     return z48.execute(comm, (arg, ))

def load_file(z48, arg):
     """Load File <Data1> = name of file to load.

     Returns:
               
     """
     comm =  z48.get(('\x20','\x2A'))
     return z48.execute(comm, (arg, ))

def register_disktools(z48)
     comm =  z48.get(('\x20','\x01'), sysex.Command('\x20','\x01', 'update_disklist', (None,None), ()))
     z48.commands[('\x20', '\x01')] = comm
     comm =  z48.get(('\x20','\x02'), sysex.Command('\x20','\x02', 'select_disk', (sysex.WORD,None), ()))
     z48.commands[('\x20', '\x02')] = comm
     comm =  z48.get(('\x20','\x03'), sysex.Command('\x20','\x03', 'test_disk', (sysex.WORD,None), ()))
     z48.commands[('\x20', '\x03')] = comm
     comm =  z48.get(('\x20','\x04'), sysex.Command('\x20','\x04', 'get_no_disks', (None,None), ()))
     z48.commands[('\x20', '\x04')] = comm
     comm =  z48.get(('\x20','\x05'), sysex.Command('\x20','\x05', 'get_disklist', (None,None), (sysex.WORD, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.STRING)))
     z48.commands[('\x20', '\x05')] = comm
     comm =  z48.get(('\x20','\x09'), sysex.Command('\x20','\x09', 'get_curr_path', (None,None), (sysex.STRING)))
     z48.commands[('\x20', '\x09')] = comm
     comm =  z48.get(('\x20','\x0D'), sysex.Command('\x20','\x0D', 'eject_disk', (sysex.WORD,None), ()))
     z48.commands[('\x20', '\x0D')] = comm
     comm =  z48.get(('\x20','\x10'), sysex.Command('\x20','\x10', 'get_no_subfolders', (None,None), ()))
     z48.commands[('\x20', '\x10')] = comm
     comm =  z48.get(('\x20','\x12'), sysex.Command('\x20','\x12', 'get_subfolder_names', (None,None), (sysex.STRING)))
     z48.commands[('\x20', '\x12')] = comm
     comm =  z48.get(('\x20','\x13'), sysex.Command('\x20','\x13', 'set_curr_folder', (sysex.STRING,None), ()))
     z48.commands[('\x20', '\x13')] = comm
     comm =  z48.get(('\x20','\x15'), sysex.Command('\x20','\x15', 'load_folder', (sysex.STRING,None), ()))
     z48.commands[('\x20', '\x15')] = comm
     comm =  z48.get(('\x20','\x16'), sysex.Command('\x20','\x16', 'create_subfolder', (sysex.STRING,None), ()))
     z48.commands[('\x20', '\x16')] = comm
     comm =  z48.get(('\x20','\x17'), sysex.Command('\x20','\x17', 'del_subfolder', (sysex.STRING,None), ()))
     z48.commands[('\x20', '\x17')] = comm
     comm =  z48.get(('\x20','\x18'), sysex.Command('\x20','\x18', 'rename_subfolder', (sysex.STRING,sysex.STRING), ()))
     z48.commands[('\x20', '\x18')] = comm
     comm =  z48.get(('\x20','\x20'), sysex.Command('\x20','\x20', 'get_no_files', (None,None), ()))
     z48.commands[('\x20', '\x20')] = comm
     comm =  z48.get(('\x20','\x22'), sysex.Command('\x20','\x22', 'get_filenames', (None,None), (sysex.STRING)))
     z48.commands[('\x20', '\x22')] = comm
     comm =  z48.get(('\x20','\x28'), sysex.Command('\x20','\x28', 'rename_file', (sysex.STRING,sysex.STRING), ()))
     z48.commands[('\x20', '\x28')] = comm
     comm =  z48.get(('\x20','\x29'), sysex.Command('\x20','\x29', 'delete_file', (sysex.STRING,None), ()))
     z48.commands[('\x20', '\x29')] = comm
     comm =  z48.get(('\x20','\x2A'), sysex.Command('\x20','\x2A', 'load_file', (sysex.STRING,None), ()))
     z48.commands[('\x20', '\x2A')] = comm
