
""" Python equivalent of akai section program_main

Program Main
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import sysex

class ProgramMain:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = sysex.Command('\x14','\x01', 'get_no_items', (), ())
          self.commands[('\x14', '\x01')] = comm
          comm = sysex.Command('\x14','\x02\x00', 'get_handles', (), (sysex.DWORD,))
          self.commands[('\x14', '\x02\x00')] = comm
          comm = sysex.Command('\x14','\x02\x01', 'get_names', (), (sysex.STRING,))
          self.commands[('\x14', '\x02\x01')] = comm
          comm = sysex.Command('\x14','\x02\x02', 'get_handles_names', (), (sysex.DWORD, sysex.STRING))
          self.commands[('\x14', '\x02\x02')] = comm
          comm = sysex.Command('\x14','\x02\x03', 'get_modified', (), (sysex.DWORD, sysex.STRING))
          self.commands[('\x14', '\x02\x03')] = comm
          comm = sysex.Command('\x14','\x03', 'set_current_by_handle', (sysex.DWORD,), ())
          self.commands[('\x14', '\x03')] = comm
          comm = sysex.Command('\x14','\x04', 'set_current_by_name', (sysex.STRING,), ())
          self.commands[('\x14', '\x04')] = comm
          comm = sysex.Command('\x14','\x05', 'get_current_handle', (), (sysex.DWORD,))
          self.commands[('\x14', '\x05')] = comm
          comm = sysex.Command('\x14','\x06', 'get_current_name', (), (sysex.STRING,))
          self.commands[('\x14', '\x06')] = comm
          comm = sysex.Command('\x14','\x07', 'get_name_by_handle', (sysex.DWORD,), (sysex.STRING,))
          self.commands[('\x14', '\x07')] = comm
          comm = sysex.Command('\x14','\x08', 'get_handle_by_name', (sysex.STRING,), (sysex.DWORD,))
          self.commands[('\x14', '\x08')] = comm
          comm = sysex.Command('\x14','\x09', 'delete_all', (), ())
          self.commands[('\x14', '\x09')] = comm
          comm = sysex.Command('\x14','\x0A', 'delete_current', (), ())
          self.commands[('\x14', '\x0A')] = comm
          comm = sysex.Command('\x14','\x0B', 'delete_by_handle', (sysex.DWORD,), ())
          self.commands[('\x14', '\x0B')] = comm
          comm = sysex.Command('\x14','\x0C', 'rename_current', (sysex.STRING,), ())
          self.commands[('\x14', '\x0C')] = comm
          comm = sysex.Command('\x14','\x0D', 'rename_by_handle', (sysex.DWORD, sysex.STRING), ())
          self.commands[('\x14', '\x0D')] = comm
          comm = sysex.Command('\x14','\x0E', 'tag', (sysex.BYTE, sysex.BYTE), ())
          self.commands[('\x14', '\x0E')] = comm
          comm = sysex.Command('\x14','\x0F', 'get_tag_bitmap', (), (sysex.WORD,))
          self.commands[('\x14', '\x0F')] = comm
          comm = sysex.Command('\x14','\x10', 'get_modified', (), ())
          self.commands[('\x14', '\x10')] = comm
          comm = sysex.Command('\x14','\x11', 'get_modified', (), (sysex.BYTE,))
          self.commands[('\x14', '\x11')] = comm
          comm = sysex.Command('\x14','\x18', 'delete_tagged', (sysex.BYTE,), ())
          self.commands[('\x14', '\x18')] = comm
          comm = sysex.Command('\x14','\x40', 'create_new', (sysex.WORD, sysex.STRING), ())
          self.commands[('\x14', '\x40')] = comm
          comm = sysex.Command('\x14','\x41', 'add_keygroups_to_current', (sysex.BYTE,), ())
          self.commands[('\x14', '\x41')] = comm

     def get_no_items(self):
          """Get number of items in memory
          """
          comm =  self.commands.get(('\x14','\x01'))
          return self.z48.execute(comm, ())

     def get_handles(self):
          """Get list of info for all items: 0=list of handles;

          Returns:
               sysex.DWORD
          """
          comm =  self.commands.get(('\x14','\x02\x00'))
          return self.z48.execute(comm, ())

     def get_names(self):
          """Get list of info for all items: 1=list of names

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x14','\x02\x01'))
          return self.z48.execute(comm, ())

     def get_handles_names(self):
          """Get list of info for all items: 2=list of handle+name;

          Returns:
               sysex.DWORD
               sysex.STRING
          """
          comm =  self.commands.get(('\x14','\x02\x02'))
          return self.z48.execute(comm, ())

     def get_modified(self):
          """Get list of info for all items: 3=list of handle+modified/tagged name

          Returns:
               sysex.DWORD
               sysex.STRING
          """
          comm =  self.commands.get(('\x14','\x02\x03'))
          return self.z48.execute(comm, ())

     def set_current_by_handle(self, arg0):
          """Select current item by handle
          """
          comm =  self.commands.get(('\x14','\x03'))
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_name(self, arg0):
          """Select current item by name
          """
          comm =  self.commands.get(('\x14','\x04'))
          return self.z48.execute(comm, (arg0, ))

     def get_current_handle(self):
          """Get handle of current item

          Returns:
               sysex.DWORD
          """
          comm =  self.commands.get(('\x14','\x05'))
          return self.z48.execute(comm, ())

     def get_current_name(self):
          """Get name of current item

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x14','\x06'))
          return self.z48.execute(comm, ())

     def get_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               sysex.STRING
          """
          comm =  self.commands.get(('\x14','\x07'))
          return self.z48.execute(comm, (arg0, ))

     def get_handle_by_name(self, arg0):
          """Get item handle from name

          Returns:
               sysex.DWORD
          """
          comm =  self.commands.get(('\x14','\x08'))
          return self.z48.execute(comm, (arg0, ))

     def delete_all(self):
          """Delete ALL items from memory
          """
          comm =  self.commands.get(('\x14','\x09'))
          return self.z48.execute(comm, ())

     def delete_current(self):
          """Delete current item from memory
          """
          comm =  self.commands.get(('\x14','\x0A'))
          return self.z48.execute(comm, ())

     def delete_by_handle(self, arg0):
          """Delete item represented by handle <Data1>
          """
          comm =  self.commands.get(('\x14','\x0B'))
          return self.z48.execute(comm, (arg0, ))

     def rename_current(self, arg0):
          """Rename current item
          """
          comm =  self.commands.get(('\x14','\x0C'))
          return self.z48.execute(comm, (arg0, ))

     def rename_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>
          """
          comm =  self.commands.get(('\x14','\x0D'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def tag(self, arg0, arg1):
          """Set Tag Bit <Data1> = bit to set(0-7), <Data2> = (0=OFF, 1=ON), Data3> = (0=CURRENT, 1=ALL)
          """
          comm =  self.commands.get(('\x14','\x0E'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_tag_bitmap(self):
          """Get Tag Bitmap

          Returns:
               sysex.WORD
          """
          comm =  self.commands.get(('\x14','\x0F'))
          return self.z48.execute(comm, ())

     def get_modified(self):
          """Get name of current item with modified/tagged info.
          """
          comm =  self.commands.get(('\x14','\x10'))
          return self.z48.execute(comm, ())

     def get_modified(self):
          """Get modified state of current item.

          Returns:
               sysex.BYTE
          """
          comm =  self.commands.get(('\x14','\x11'))
          return self.z48.execute(comm, ())

     def delete_tagged(self, arg0):
          """Delete tagged items <Data1> = tag bit
          """
          comm =  self.commands.get(('\x14','\x18'))
          return self.z48.execute(comm, (arg0, ))

     def create_new(self, arg0, arg1):
          """Create New Program <Data1> = number of keygroups;<Data2> = name.
          """
          comm =  self.commands.get(('\x14','\x40'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def add_keygroups_to_current(self, arg0):
          """Add Keygroups to Program <Data1> = number of keygroups to add
          """
          comm =  self.commands.get(('\x14','\x41'))
          return self.z48.execute(comm, (arg0, ))

