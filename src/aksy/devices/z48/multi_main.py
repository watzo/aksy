
""" Python equivalent of akai section multi_main

Multi Main
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.z48.sysex

class MultiMain:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.sysex.Command('\x18','\x01', 'get_no_items', (), (aksy.sysex.BYTE,))
          self.commands[('\x18', '\x01')] = comm
          comm = aksy.sysex.Command('\x18','\x02\x00', 'get_handles', (), (aksy.sysex.DWORD,))
          self.commands[('\x18', '\x02\x00')] = comm
          comm = aksy.sysex.Command('\x18','\x02\x01', 'get_names', (), (aksy.sysex.STRING,))
          self.commands[('\x18', '\x02\x01')] = comm
          comm = aksy.sysex.Command('\x18','\x02\x02', 'get_handles_names', (), (aksy.sysex.DWORD, aksy.sysex.STRING))
          self.commands[('\x18', '\x02\x02')] = comm
          comm = aksy.sysex.Command('\x18','\x02\x03', 'get_handles_tagged', (), (aksy.sysex.DWORD, aksy.sysex.STRING))
          self.commands[('\x18', '\x02\x03')] = comm
          comm = aksy.sysex.Command('\x18','\x03', 'set_current_by_handle', (aksy.sysex.DWORD,), ())
          self.commands[('\x18', '\x03')] = comm
          comm = aksy.sysex.Command('\x18','\x04', 'set_current_by_name', (aksy.sysex.STRING,), ())
          self.commands[('\x18', '\x04')] = comm
          comm = aksy.sysex.Command('\x18','\x05', 'get_current_handle', (), (aksy.sysex.DWORD,))
          self.commands[('\x18', '\x05')] = comm
          comm = aksy.sysex.Command('\x18','\x06', 'get_current_name', (), (aksy.sysex.STRING,))
          self.commands[('\x18', '\x06')] = comm
          comm = aksy.sysex.Command('\x18','\x07', 'get_name_by_handle', (aksy.sysex.DWORD,), (aksy.sysex.STRING,))
          self.commands[('\x18', '\x07')] = comm
          comm = aksy.sysex.Command('\x18','\x08', 'get_handle_by_name', (aksy.sysex.STRING,), (aksy.sysex.DWORD,))
          self.commands[('\x18', '\x08')] = comm
          comm = aksy.sysex.Command('\x18','\x09', 'delete_all', (), ())
          self.commands[('\x18', '\x09')] = comm
          comm = aksy.sysex.Command('\x18','\x0A', 'delete_current', (), ())
          self.commands[('\x18', '\x0A')] = comm
          comm = aksy.sysex.Command('\x18','\x0B', 'delete_by_handle', (aksy.sysex.DWORD,), ())
          self.commands[('\x18', '\x0B')] = comm
          comm = aksy.sysex.Command('\x18','\x0C', 'rename_current', (aksy.sysex.STRING,), ())
          self.commands[('\x18', '\x0C')] = comm
          comm = aksy.sysex.Command('\x18','\x0D', 'rename_by_handle', (aksy.sysex.DWORD, aksy.sysex.STRING), ())
          self.commands[('\x18', '\x0D')] = comm
          comm = aksy.sysex.Command('\x18','\x0E', 'tag', (aksy.sysex.BYTE, aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands[('\x18', '\x0E')] = comm
          comm = aksy.sysex.Command('\x18','\x0F', 'get_tag_bitmap', (), (aksy.sysex.WORD,))
          self.commands[('\x18', '\x0F')] = comm
          comm = aksy.sysex.Command('\x18','\x10', 'get_current_modified', (), (aksy.sysex.STRING,))
          self.commands[('\x18', '\x10')] = comm

     def get_no_items(self):
          """Get number of items in memory

          Returns:
               aksy.sysex.BYTE
          """
          comm =  self.commands.get(('\x18','\x01'))
          return self.z48.execute(comm, ())

     def get_handles(self):
          """Get handles <Data1>: 0=list of handles

          Returns:
               aksy.sysex.DWORD
          """
          comm =  self.commands.get(('\x18','\x02\x00'))
          return self.z48.execute(comm, ())

     def get_names(self):
          """Get names items: <Data1>; 1=list of names; 

          Returns:
               aksy.sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x02\x01'))
          return self.z48.execute(comm, ())

     def get_handles_names(self):
          """Get handles names: <Data1>; 2=list of handle+name

          Returns:
               aksy.sysex.DWORD
               aksy.sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x02\x02'))
          return self.z48.execute(comm, ())

     def get_handles_tagged(self):
          """Get handles tagged <Data1> ; 3=list of handle+modified/tagged name 

          Returns:
               aksy.sysex.DWORD
               aksy.sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x02\x03'))
          return self.z48.execute(comm, ())

     def set_current_by_handle(self, arg0):
          """Select by handle
          """
          comm =  self.commands.get(('\x18','\x03'))
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_name(self, arg0):
          """Select by name
          """
          comm =  self.commands.get(('\x18','\x04'))
          return self.z48.execute(comm, (arg0, ))

     def get_current_handle(self):
          """Get current handle 

          Returns:
               aksy.sysex.DWORD
          """
          comm =  self.commands.get(('\x18','\x05'))
          return self.z48.execute(comm, ())

     def get_current_name(self):
          """Get name of current item

          Returns:
               aksy.sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x06'))
          return self.z48.execute(comm, ())

     def get_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               aksy.sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x07'))
          return self.z48.execute(comm, (arg0, ))

     def get_handle_by_name(self, arg0):
          """Get item handle from name

          Returns:
               aksy.sysex.DWORD
          """
          comm =  self.commands.get(('\x18','\x08'))
          return self.z48.execute(comm, (arg0, ))

     def delete_all(self):
          """Delete ALL items from memory
          """
          comm =  self.commands.get(('\x18','\x09'))
          return self.z48.execute(comm, ())

     def delete_current(self):
          """Delete current item from memory
          """
          comm =  self.commands.get(('\x18','\x0A'))
          return self.z48.execute(comm, ())

     def delete_by_handle(self, arg0):
          """Delete item represented by handle <Data1>
          """
          comm =  self.commands.get(('\x18','\x0B'))
          return self.z48.execute(comm, (arg0, ))

     def rename_current(self, arg0):
          """Rename current item
          """
          comm =  self.commands.get(('\x18','\x0C'))
          return self.z48.execute(comm, (arg0, ))

     def rename_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>
          """
          comm =  self.commands.get(('\x18','\x0D'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def tag(self, arg0, arg1, arg2):
          """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) <Data3> = (0=CURRENT, 1=ALL)
          """
          comm =  self.commands.get(('\x18','\x0E'))
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def get_tag_bitmap(self):
          """Get Tag Bitmap

          Returns:
               aksy.sysex.WORD
          """
          comm =  self.commands.get(('\x18','\x0F'))
          return self.z48.execute(comm, ())

     def get_current_modified(self):
          """Get name of current item with modified/tagged info.

          Returns:
               aksy.sysex.STRING
          """
          comm =  self.commands.get(('\x18','\x10'))
          return self.z48.execute(comm, ())

