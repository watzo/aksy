
""" Python equivalent of akai section multi_main

Multi Main
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import sysex

class MultiMain:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = sysex.Command('\x18','\x01', 'get_no_items', (), (sysex.BYTE,))
          self.commands[('\x18', '\x01')] = comm
          comm = sysex.Command('\x18','\x02\x00', 'get_multi_handles', (), (sysex.DWORD,))
          self.commands[('\x18', '\x02\x00')] = comm
          comm = sysex.Command('\x18','\x02\x01', 'get_multi_names', (), (sysex.STRING,))
          self.commands[('\x18', '\x02\x01')] = comm
          comm = sysex.Command('\x18','\x02\x02', 'get_multi_handles_names', (), (sysex.DWORD, sysex.STRING))
          self.commands[('\x18', '\x02\x02')] = comm
          comm = sysex.Command('\x18','\x02\x03', 'get_multi_handles_tagged', (), (sysex.DWORD, sysex.STRING))
          self.commands[('\x18', '\x02\x03')] = comm
          comm = sysex.Command('\x18','\x03', 'set_curr_multi', (sysex.DWORD,), ())
          self.commands[('\x18', '\x03')] = comm
          comm = sysex.Command('\x18','\x04', 'set_multi_by_name', (sysex.STRING,), ())
          self.commands[('\x18', '\x04')] = comm
          comm = sysex.Command('\x18','\x05', 'get_curr_multi_handle', (), (sysex.DWORD,))
          self.commands[('\x18', '\x05')] = comm
          comm = sysex.Command('\x18','\x06', 'get_curr_multi_name', (), (sysex.STRING,))
          self.commands[('\x18', '\x06')] = comm
          comm = sysex.Command('\x18','\x07', 'get_name_by_handle', (sysex.DWORD,), (sysex.STRING,))
          self.commands[('\x18', '\x07')] = comm
          comm = sysex.Command('\x18','\x08', 'get_handle_by_name', (sysex.STRING,), (sysex.DWORD,))
          self.commands[('\x18', '\x08')] = comm
          comm = sysex.Command('\x18','\x09', 'delete_all', (), ())
          self.commands[('\x18', '\x09')] = comm
          comm = sysex.Command('\x18','\x0A', 'delete_curr_multi', (), ())
          self.commands[('\x18', '\x0A')] = comm
          comm = sysex.Command('\x18','\x0B', 'delete_by_handle', (sysex.DWORD,), ())
          self.commands[('\x18', '\x0B')] = comm
          comm = sysex.Command('\x18','\x0C', 'rename_curr_multi', (sysex.STRING,), ())
          self.commands[('\x18', '\x0C')] = comm
          comm = sysex.Command('\x18','\x0D', 'rename_by_handle', (sysex.DWORD, sysex.STRING), ())
          self.commands[('\x18', '\x0D')] = comm
          comm = sysex.Command('\x18','\x0E', 'set_tag_bitmap', (sysex.BYTE, sysex.BYTE, sysex.BYTE), ())
          self.commands[('\x18', '\x0E')] = comm
          comm = sysex.Command('\x18','\x0F', 'get_tag_bitmap', (), (sysex.WORD,))
          self.commands[('\x18', '\x0F')] = comm
          comm = sysex.Command('\x18','\x10', 'get_curr_modified', (), (sysex.STRING,))
          self.commands[('\x18', '\x10')] = comm

     def get_no_items(self):
          """Get number of items in memory

          Returns:
               sysex.BYTE
          """
          comm =  self.commands.get(('\x18','\x01'))
          return self.z48.execute(comm, ())

     def get_multi_handles(self):
          """Get handles <Data1>: 0=list of handles

          Returns:
               sysex.DWORD
          """
          comm =  self.commands.get(('\x18','\x02\x00'))
          return self.z48.execute(comm, ())

     def get_multi_names(self):
          """Get names items: <Data1>; 1=list of names; 

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x02\x01'))
          return self.z48.execute(comm, ())

     def get_multi_handles_names(self):
          """Get handles names: <Data1>; 2=list of handle+name

          Returns:
               sysex.DWORD
               sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x02\x02'))
          return self.z48.execute(comm, ())

     def get_multi_handles_tagged(self):
          """Get handles tagged <Data1> ; 3=list of handle+modified/tagged name 

          Returns:
               sysex.DWORD
               sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x02\x03'))
          return self.z48.execute(comm, ())

     def set_curr_multi(self, arg0):
          """Select by handle
          """
          comm =  self.commands.get(('\x18','\x03'))
          return self.z48.execute(comm, (arg0, ))

     def set_multi_by_name(self, arg0):
          """Select by name
          """
          comm =  self.commands.get(('\x18','\x04'))
          return self.z48.execute(comm, (arg0, ))

     def get_curr_multi_handle(self):
          """Get current handle 

          Returns:
               sysex.DWORD
          """
          comm =  self.commands.get(('\x18','\x05'))
          return self.z48.execute(comm, ())

     def get_curr_multi_name(self):
          """Get name of current item

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x06'))
          return self.z48.execute(comm, ())

     def get_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x07'))
          return self.z48.execute(comm, (arg0, ))

     def get_handle_by_name(self, arg0):
          """Get item handle from name

          Returns:
               sysex.DWORD
          """
          comm =  self.commands.get(('\x18','\x08'))
          return self.z48.execute(comm, (arg0, ))

     def delete_all(self):
          """Delete ALL items from memory
          """
          comm =  self.commands.get(('\x18','\x09'))
          return self.z48.execute(comm, ())

     def delete_curr_multi(self):
          """Delete current item from memory
          """
          comm =  self.commands.get(('\x18','\x0A'))
          return self.z48.execute(comm, ())

     def delete_by_handle(self, arg0):
          """Delete item represented by handle <Data1>
          """
          comm =  self.commands.get(('\x18','\x0B'))
          return self.z48.execute(comm, (arg0, ))

     def rename_curr_multi(self, arg0):
          """Rename current item
          """
          comm =  self.commands.get(('\x18','\x0C'))
          return self.z48.execute(comm, (arg0, ))

     def rename_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>
          """
          comm =  self.commands.get(('\x18','\x0D'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_tag_bitmap(self, arg0, arg1, arg2):
          """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) <Data3> = (0=CURRENT, 1=ALL)
          """
          comm =  self.commands.get(('\x18','\x0E'))
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def get_tag_bitmap(self):
          """Get Tag Bitmap

          Returns:
               sysex.WORD
          """
          comm =  self.commands.get(('\x18','\x0F'))
          return self.z48.execute(comm, ())

     def get_curr_modified(self):
          """Get name of current item with modified/tagged info.

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x10'))
          return self.z48.execute(comm, ())

