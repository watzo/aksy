
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
     comm =  sysex.Command('\x20','\x01', (None,None), (), ())
     return z48.execute(comm)

def select_disk(z48, arg):
     """Select Disk <Data1> = Disk Handle

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x02', (sysex.WORD,None), (arg), ())
     return z48.execute(comm)

def test_disk(z48, arg):
     """Test if the disk is valid <Data1> = Disk Handle

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x03', (sysex.WORD,None), (arg), ())
     return z48.execute(comm)

def get_no_disks(z48):
     """Get the number of disks connected

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x04', (None,None), (), ())
     return z48.execute(comm)

def get_disklist(z48):
     """Get list of all connected disks

     Returns:
          sysex.WORD
          sysex.BYTE
          sysex.BYTE
          sysex.WORD
          sysex.STRING     
     """
     comm =  sysex.Command('\x20','\x05', (None,None), (), (sysex.WORD, sysex.BYTE, sysex.BYTE, sysex.WORD, sysex.STRING))
     return z48.execute(comm)

def get_curr_path(z48):
     """Get current path of current disk

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x09', (None,None), (), ())
     return z48.execute(comm)

def eject_disk(z48, arg):
     """Eject Disk <Data1> = Disk Handle

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x0D', (sysex.WORD,None), (arg), ())
     return z48.execute(comm)

def get_no_subfolders(z48):
     """Get number of sub-folders in the current folder.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x10', (None,None), (), ())
     return z48.execute(comm)

def get_subfolder_names(z48):
     """Get the names of all of the sub-folders in the current folder.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x12', (None,None), (), ())
     return z48.execute(comm)

def set_curr_folder(z48, arg):
     """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x13', (sysex.STRING,None), (arg), ())
     return z48.execute(comm)

def load_folder(z48, arg):
     """Load Folder: the selected folder, and all its contents (including sub- 

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x15', (sysex.STRING,None), (arg), ())
     return z48.execute(comm)

def create_subfolder(z48, arg):
     """Create Folder: Creates a sub-folder in the currently selected folder.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x16', (sysex.STRING,None), (arg), ())
     return z48.execute(comm)

def del_subfolder(z48, arg):
     """Delete Sub-Folder.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x17', (sysex.STRING,None), (arg), ())
     return z48.execute(comm)

def rename_subfolder(z48, arg1, arg2):
     """Rename Folder: <Data1> = name of folder to rename

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x18', (sysex.STRING,sysex.STRING), (arg1, arg2), ())
     return z48.execute(comm)

def get_no_files(z48):
     """Get number of files in the current folder.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x20', (None,None), (), ())
     return z48.execute(comm)

def get_filenames(z48):
     """Get the names of all of the files in the current folder.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x22', (None,None), (), ())
     return z48.execute(comm)

def rename_file(z48, arg1, arg2):
     """ Rename File 

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x28', (sysex.STRING,sysex.STRING), (arg1, arg2), ())
     return z48.execute(comm)

def delete_file(z48, arg):
     """Delete File. <Data1> = name of file to delete.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x29', (sysex.STRING,None), (arg), ())
     return z48.execute(comm)

def load_file(z48, arg):
     """Load File <Data1> = name of file to load.

     Returns:
               
     """
     comm =  sysex.Command('\x20','\x2A', (sysex.STRING,None), (arg), ())
     return z48.execute(comm)

