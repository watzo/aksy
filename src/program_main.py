
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
          comm = sysex.Command('\x14','\x01 ', 'get_no_programs', (), ())
          self.commands[('\x14', '\x01 ')] = comm
          comm = sysex.Command('\x14','\x02\x00', 'program_get_handles', (), (sysex.DWORD,))
          self.commands[('\x14', '\x02\x00')] = comm
          comm = sysex.Command('\x14','\x02\x01', 'program_get_names', (), (sysex.STRING,))
          self.commands[('\x14', '\x02\x01')] = comm
          comm = sysex.Command('\x14','\x02\x02', 'program_get_handles_names', (), (sysex.DWORD, sysex.STRING))
          self.commands[('\x14', '\x02\x02')] = comm
          comm = sysex.Command('\x14','\x02\x03', 'program_get_modified', (), (sysex.DWORD, sysex.STRING))
          self.commands[('\x14', '\x02\x03')] = comm
          comm = sysex.Command('\x14','\x03', 'curr_program_select_by_handle', (sysex.DWORD,), ())
          self.commands[('\x14', '\x03')] = comm
          comm = sysex.Command('\x14','\x04', 'curr_program_select_by_name', (sysex.STRING,), ())
          self.commands[('\x14', '\x04')] = comm
          comm = sysex.Command('\x14','\x05', 'curr_program_get_handle', (), (sysex.DWORD,))
          self.commands[('\x14', '\x05')] = comm
          comm = sysex.Command('\x14','\x06', 'curr_program_get_name', (), (sysex.STRING,))
          self.commands[('\x14', '\x06')] = comm
          comm = sysex.Command('\x14','\x07', 'program_get_item_name_by_handle', (sysex.DWORD,), (sysex.STRING,))
          self.commands[('\x14', '\x07')] = comm
          comm = sysex.Command('\x14','\x08', 'program_get_item_handle_from_name', (sysex.STRING,), (sysex.DWORD,))
          self.commands[('\x14', '\x08')] = comm
          comm = sysex.Command('\x14','\x09', 'delete_all_programs', (), ())
          self.commands[('\x14', '\x09')] = comm
          comm = sysex.Command('\x14','\x0A', 'curr_program_delete', (), ())
          self.commands[('\x14', '\x0A')] = comm
          comm = sysex.Command('\x14','\x0B', 'delete_program_by_handle', (sysex.DWORD,), ())
          self.commands[('\x14', '\x0B')] = comm
          comm = sysex.Command('\x14','\x0C', 'curr_program_rename', (sysex.STRING,), ())
          self.commands[('\x14', '\x0C')] = comm
          comm = sysex.Command('\x14','\x0D', 'rename_program_by_handle', (sysex.DWORD, sysex.STRING), ())
          self.commands[('\x14', '\x0D')] = comm
          comm = sysex.Command('\x14','\x0E', 'tag_program', (sysex.BYTE, sysex.BYTE), ())
          self.commands[('\x14', '\x0E')] = comm
          comm = sysex.Command('\x14','\x0F', 'program_get_tag_bitmap', (), (sysex.WORD,))
          self.commands[('\x14', '\x0F')] = comm
          comm = sysex.Command('\x14','\x10', 'curr_program_get_mod_tagged', (), ())
          self.commands[('\x14', '\x10')] = comm
          comm = sysex.Command('\x14','\x11', 'curr_program_get_modified', (), (sysex.BYTE,))
          self.commands[('\x14', '\x11')] = comm
          comm = sysex.Command('\x14','\x18', 'delete_tagged_programs', (sysex.BYTE,), ())
          self.commands[('\x14', '\x18')] = comm
          comm = sysex.Command('\x14','\x40', 'create_program', (sysex.WORD, sysex.STRING), ())
          self.commands[('\x14', '\x40')] = comm
          comm = sysex.Command('\x14','\x41', 'curr_program_add_keygroups', (sysex.BYTE,), ())
          self.commands[('\x14', '\x41')] = comm

     def get_no_programs(self):
          """Get number of items in memory

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x01 '))
          return self.z48.execute(comm, ())

     def program_get_handles(self):
          """Get list of info for all items: 0=list of handles;

          Returns:
               sysex.DWORD     
          """
          comm =  self.commands.get(('\x14','\x02\x00'))
          return self.z48.execute(comm, ())

     def program_get_names(self):
          """Get list of info for all items: 1=list of names

          Returns:
               sysex.STRING     
          """
          comm =  self.commands.get(('\x14','\x02\x01'))
          return self.z48.execute(comm, ())

     def program_get_handles_names(self):
          """Get list of info for all items: 2=list of handle+name;

          Returns:
               sysex.DWORD
               sysex.STRING     
          """
          comm =  self.commands.get(('\x14','\x02\x02'))
          return self.z48.execute(comm, ())

     def program_get_modified(self):
          """Get list of info for all items: 3=list of handle+modified/tagged name

          Returns:
               sysex.DWORD
               sysex.STRING     
          """
          comm =  self.commands.get(('\x14','\x02\x03'))
          return self.z48.execute(comm, ())

     def curr_program_select_by_handle(self, arg0):
          """Select current item by handle

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x03'))
          return self.z48.execute(comm, (arg0, ))

     def curr_program_select_by_name(self, arg0):
          """Select current item by name

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x04'))
          return self.z48.execute(comm, (arg0, ))

     def curr_program_get_handle(self):
          """Get handle of current item

          Returns:
               sysex.DWORD     
          """
          comm =  self.commands.get(('\x14','\x05'))
          return self.z48.execute(comm, ())

     def curr_program_get_name(self):
          """Get name of current item

          Returns:
               sysex.STRING     
          """
          comm =  self.commands.get(('\x14','\x06'))
          return self.z48.execute(comm, ())

     def program_get_item_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               sysex.STRING     
          """
          comm =  self.commands.get(('\x14','\x07'))
          return self.z48.execute(comm, (arg0, ))

     def program_get_item_handle_from_name(self, arg0):
          """Get item handle from name

          Returns:
               sysex.DWORD     
          """
          comm =  self.commands.get(('\x14','\x08'))
          return self.z48.execute(comm, (arg0, ))

     def delete_all_programs(self):
          """Delete ALL items from memory

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x09'))
          return self.z48.execute(comm, ())

     def curr_program_delete(self):
          """Delete current item from memory

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x0A'))
          return self.z48.execute(comm, ())

     def delete_program_by_handle(self, arg0):
          """Delete item represented by handle <Data1>

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x0B'))
          return self.z48.execute(comm, (arg0, ))

     def curr_program_rename(self, arg0):
          """Rename current item

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x0C'))
          return self.z48.execute(comm, (arg0, ))

     def rename_program_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x0D'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def tag_program(self, arg0, arg1):
          """Set Tag Bit <Data1> = bit to set(0-7), <Data2> = (0=OFF, 1=ON), Data3> = (0=CURRENT, 1=ALL)

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x0E'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def program_get_tag_bitmap(self):
          """Get Tag Bitmap

          Returns:
               sysex.WORD     
          """
          comm =  self.commands.get(('\x14','\x0F'))
          return self.z48.execute(comm, ())

     def curr_program_get_mod_tagged(self):
          """Get name of current item with modified/tagged info.

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x10'))
          return self.z48.execute(comm, ())

     def curr_program_get_modified(self):
          """Get modified state of current item.

          Returns:
               sysex.BYTE     
          """
          comm =  self.commands.get(('\x14','\x11'))
          return self.z48.execute(comm, ())

     def delete_tagged_programs(self, arg0):
          """Delete tagged items <Data1> = tag bit

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x18'))
          return self.z48.execute(comm, (arg0, ))

     def create_program(self, arg0, arg1):
          """Create New Program <Data1> = number of keygroups;<Data2> = name.

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x40'))
          return self.z48.execute(comm, (arg0, arg1, ))

     def curr_program_add_keygroups(self, arg0):
          """Add Keygroups to Program <Data1> = number of keygroups to add

          Returns:
                    
          """
          comm =  self.commands.get(('\x14','\x41'))
          return self.z48.execute(comm, (arg0, ))

