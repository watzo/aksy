
""" Python equivalent of akai section disktools

These commands have been sniffed from ak.Sys output

Methods to manipulate the samplers filesystem
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import sysex

class DiskTools:
    def __init__(self, z48):
        self.z48= z48

        # Registers commands locally
        self.commands = {}
        comm = sysex.Command('\x10','\x01', 'update_disklist', (), ())
        self.commands[('\x10', '\x01')] = comm
        comm = sysex.Command('\x10','\x02', 'select_disk', (sysex.WORD,), ())
        self.commands[('\x10', '\x02')] = comm
        comm = sysex.Command('\x10','\x03', 'test_disk', (sysex.WORD,), ())
        self.commands[('\x10', '\x03')] = comm
        comm = sysex.Command('\x10','\x04', 'get_no_disks', (), (sysex.BYTE,))
        self.commands[('\x10', '\x04')] = comm
        comm = sysex.Command('\x10','\x05', 'get_disklist', (), (sysex.WORD, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.STRING))
        self.commands[('\x10', '\x05')] = comm
        comm = sysex.Command('\x10','\x09', 'get_curr_path', (), (sysex.STRING,))
        self.commands[('\x10', '\x09')] = comm
        comm = sysex.Command('\x10','\x0D', 'eject_disk', (sysex.WORD,), ())
        self.commands[('\x10', '\x0D')] = comm
        comm = sysex.Command('\x10','\x10', 'get_no_subfolders', (), (sysex.PAD, sysex.WORD))
        self.commands[('\x10', '\x10')] = comm
        comm = sysex.Command('\x10','\x12', 'get_subfolder_names', (), (sysex.STRING,))
        self.commands[('\x10', '\x12')] = comm
        comm = sysex.Command('\x10','\x13', 'set_curr_folder', (sysex.STRING,), ())
        self.commands[('\x10', '\x13')] = comm
        comm = sysex.Command('\x10','\x15', 'load_folder', (sysex.STRING,), ())
        self.commands[('\x10', '\x15')] = comm
        comm = sysex.Command('\x10','\x16', 'create_subfolder', (sysex.STRING,), ())
        self.commands[('\x10', '\x16')] = comm
        comm = sysex.Command('\x10','\x17', 'del_subfolder', (sysex.STRING,), ())
        self.commands[('\x10', '\x17')] = comm
        comm = sysex.Command('\x10','\x18', 'rename_subfolder', (sysex.STRING,), ())
        self.commands[('\x10', '\x18')] = comm
        comm = sysex.Command('\x10','\x20', 'get_no_files', (), (sysex.WORD,))
        self.commands[('\x10', '\x20')] = comm
        comm = sysex.Command('\x10','\x22', 'get_filenames', (), (sysex.STRING,))
        self.commands[('\x10', '\x22')] = comm
        comm = sysex.Command('\x10','\x28', 'rename_file', (sysex.STRING,), ())
        self.commands[('\x10', '\x28')] = comm
        comm = sysex.Command('\x10','\x29', 'delete_file', (sysex.STRING,), ())
        self.commands[('\x10', '\x29')] = comm
        comm = sysex.Command('\x10','\x2A', 'load_file', (sysex.STRING,), ())
        self.commands[('\x10', '\x2A')] = comm

    def update_disklist(z48):
     """Update the list of disks connected

     Returns:
               
     """
     comm =  commands.get(('\x10','\x01'))
     return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def select_disk(arg0):
         """Select Disk <Data1> = Disk Handle

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x02'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def test_disk(z48, arg0):
         """Test if the disk is valid <Data1> = Disk Handle

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x03'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def get_no_disks():
         """Get the number of disks connected

         Returns:
              sysex.PAD
              sysex.BYTE     
         """
         comm =  commands.get(('\x10','\x04'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def get_disklist():
         """Get list of all connected disks

         Returns:
              sysex.WORD
              sysex.BYTE
              sysex.BYTE
              sysex.BYTE
              sysex.BYTE
              sysex.STRING     
         """
         comm =  commands.get(('\x10','\x05'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def get_curr_path():
         """Get current path of current disk

         Returns:
              sysex.STRING     
         """
         comm =  commands.get(('\x10','\x09'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def eject_disk(arg0):
         """Eject Disk <Data1> = Disk Handle

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x0D'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def get_no_subfolders():
         """Get number of sub-folders in the current folder.

         Returns:
              sysex.PAD
              sysex.WORD     
         """
         comm =  commands.get(('\x10','\x10'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def get_subfolder_names():
         """Get the names of all of the sub-folders in the current folder.

         Returns:
              sysex.STRING     
         """
         comm =  commands.get(('\x10','\x12'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def set_curr_folder(arg0):
         """Open Folder. This sets the current folder to be the requested one. (If <Data1> = 0, the root folder will be selected.)

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x13'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def load_folder(arg0):
         """Load Folder: the selected folder, and all its contents (including sub- 

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x15'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def create_subfolder(arg0):
         """Create Folder: Creates a sub-folder in the currently selected folder.

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x16'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def del_subfolder(arg0):
         """Delete Sub-Folder.

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x17'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def rename_subfolder(arg0):
         """Rename Folder: <Data1> = name of folder to rename

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x18'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def get_no_files():
         """Get number of files in the current folder.

         Returns:
              sysex.WORD     
         """
         comm =  commands.get(('\x10','\x20'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def get_filenames():
         """Get the names of all of the files in the current folder.

         Returns:
              sysex.STRING     
         """
         comm =  commands.get(('\x10','\x22'))
         return z48.execute(comm, (), sysex.AKSYS_Z48_ID)

    def rename_file(arg0):
         """ Rename File 

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x28'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def delete_file(arg0):
         """Delete File. <Data1> = name of file to delete.

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x29'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

    def load_file(arg0):
         """Load File <Data1> = name of file to load.

         Returns:
                   
         """
         comm =  commands.get(('\x10','\x2A'))
         return z48.execute(comm, (arg0, ), sysex.AKSYS_Z48_ID)

