
""" Python equivalent of akai section disktools

Methods to manipulate the samplers filesystem
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import sysex
def update_disklist(z48):
     """ Update the list of disks connected
     """
     comm =  sysex.Command('\x20','\x01',update_disklist,(None,None),())
     return z48.execute(comm)

def select_disk(z48, arg):
     """ Select Disk <Data1> = Disk Handle
     """
     comm =  sysex.Command('\x20','\x02',select_disk,(sysex.WORD,None),(arg))
     return z48.execute(comm)

def test_disk(z48, arg):
     """ Test if the disk is valid <Data1> = Disk Handle
     """
     comm =  sysex.Command('\x20','\x03',test_disk,(sysex.WORD,None),(arg))
     return z48.execute(comm)

def get_no_disks(z48):
     """ Get the number of disks connected
     """
     comm =  sysex.Command('\x20','\x04',get_no_disks,(None,None),())
     return z48.execute(comm)

def get_disklist(z48):
     """ Get list of all connected disks
     """
     comm =  sysex.Command('\x20','\x05',get_disklist,(None,None),())
     return z48.execute(comm)

def get_curr_path(z48):
     """ Get current path of current disk
     """
     comm =  sysex.Command('\x20','\x09',get_curr_path,(None,None),())
     return z48.execute(comm)

def eject_disk(z48, arg):
     """ Eject Disk <Data1> = Disk Handle
     """
     comm =  sysex.Command('\x20','\x0D',eject_disk,(sysex.WORD,None),(arg))
     return z48.execute(comm)

def get_no_subfolders(z48):
     """ Get number of sub-folders in the current folder.
     """
     comm =  sysex.Command('\x20','\x10',get_no_subfolders,(None,None),())
     return z48.execute(comm)

def get_subfolder_names(z48):
     """ Get the names of all of the sub-folders in the current folder.
     """
     comm =  sysex.Command('\x20','\x12',get_subfolder_names,(None,None),())
     return z48.execute(comm)

def set_curr_folder(z48, arg):
     """ Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)
     """
     comm =  sysex.Command('\x20','\x13',set_curr_folder,(sysex.STRING,None),(arg))
     return z48.execute(comm)

def load_folder(z48, arg):
     """ Load Folder: the selected folder, and all its contents (including sub- 
     """
     comm =  sysex.Command('\x20','\x15',load_folder,(sysex.STRING,None),(arg))
     return z48.execute(comm)

def create_subfolder(z48, arg):
     """ Create Folder: Creates a sub-folder in the currently selected folder.
     """
     comm =  sysex.Command('\x20','\x16',create_subfolder,(sysex.STRING,None),(arg))
     return z48.execute(comm)

def del_subfolder(z48, arg):
     """ Delete Sub-Folder.
     """
     comm =  sysex.Command('\x20','\x17',del_subfolder,(sysex.STRING,None),(arg))
     return z48.execute(comm)

def rename_subfolder(z48, arg1, arg2):
     """ Rename Folder: <Data1> = name of folder to rename
     """
     comm =  sysex.Command('\x20','\x18',rename_subfolder,(sysex.STRING,sysex.STRING),(arg1, arg2))
     return z48.execute(comm)

def get_no_files(z48):
     """ Get number of files in the current folder.
     """
     comm =  sysex.Command('\x20','\x20',get_no_files,(None,None),())
     return z48.execute(comm)

def get_filenames(z48):
     """ Get the names of all of the files in the current folder.
     """
     comm =  sysex.Command('\x20','\x22',get_filenames,(None,None),())
     return z48.execute(comm)

def rename_file(z48, arg1, arg2):
     """  Rename File 
     """
     comm =  sysex.Command('\x20','\x28',rename_file,(sysex.STRING,sysex.STRING),(arg1, arg2))
     return z48.execute(comm)

def delete_file(z48, arg):
     """ Delete File. <Data1> = name of file to delete.
     """
     comm =  sysex.Command('\x20','\x29',delete_file,(sysex.STRING,None),(arg))
     return z48.execute(comm)

def load_file(z48, arg):
     """ Load File <Data1> = name of file to load.
     """
     comm =  sysex.Command('\x20','\x2A',load_file,(sysex.STRING,None),(arg))
     return z48.execute(comm)

