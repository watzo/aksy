
""" Python equivalent of akai section program_main

Program Main
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import sysex
def get_no_programs(z48):
     """Get number of items in memory

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x01 '))
     return z48.execute(comm, ())

def program_get_handles(z48):
     """Get list of info for all items: 0=list of handles;

     Returns:
          sysex.DWORD     
     """
     comm =  z48.commands.get(('\x14','\x02\x00'))
     return z48.execute(comm, ())

def program_get_names(z48):
     """Get list of info for all items: 1=list of names

     Returns:
          sysex.STRING     
     """
     comm =  z48.commands.get(('\x14','\x02\x01'))
     return z48.execute(comm, ())

def program_get_handles_names(z48):
     """Get list of info for all items: 2=list of handle+name;

     Returns:
          sysex.DWORD
          sysex.STRING     
     """
     comm =  z48.commands.get(('\x14','\x02\x02'))
     return z48.execute(comm, ())

def program_get_modified(z48):
     """Get list of info for all items: 3=list of handle+modified/tagged name

     Returns:
          sysex.DWORD
          sysex.STRING     
     """
     comm =  z48.commands.get(('\x14','\x02\x03'))
     return z48.execute(comm, ())

def curr_program_select_by_handle(z48, arg0):
     """Select current item by handle

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x03'))
     return z48.execute(comm, (arg0, ))

def curr_program_select_by_name(z48, arg0):
     """Select current item by name

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x04'))
     return z48.execute(comm, (arg0, ))

def curr_program_get_handle(z48):
     """Get handle of current item NA

     Returns:
          sysex.DWORD     
     """
     comm =  z48.commands.get(('\x14','\x05'))
     return z48.execute(comm, ())

def curr_program_get_name(z48):
     """Get name of current item

     Returns:
          sysex.STRING     
     """
     comm =  z48.commands.get(('\x14','\x06'))
     return z48.execute(comm, ())

def program_get_item_name_by_handle(z48, arg0):
     """Get item name from handle

     Returns:
          sysex.STRING     
     """
     comm =  z48.commands.get(('\x14','\x07'))
     return z48.execute(comm, (arg0, ))

def program_get_item_handle_from_name(z48):
     """Get item handle from name

     Returns:
          sysex.DWORD     
     """
     comm =  z48.commands.get(('\x14','\x08'))
     return z48.execute(comm, ())

def delete_all_programs(z48):
     """Delete ALL items from memory

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x09'))
     return z48.execute(comm, ())

def curr_program_delete(z48):
     """Delete current item from memory

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x0A'))
     return z48.execute(comm, ())

def delete_program_by_handle(z48):
     """Delete item represented by handle <Data1> DWORD

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x0B'))
     return z48.execute(comm, ())

def curr_program_rename(z48):
     """Rename current item STRING

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x0C'))
     return z48.execute(comm, ())

def rename_program_by_handle(z48):
     """Rename item represented by handle <Data1> DWORD

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x0D'))
     return z48.execute(comm, ())

def tag_program(z48, arg0):
     """Set Tag Bit <Data1> = bit to set(0-7), <Data2> = (0=OFF, 1=ON), Data3> = (0=CURRENT, 1=ALL)

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x0E'))
     return z48.execute(comm, (arg0, ))

def program_get_tag_bitmap(z48):
     """Get Tag Bitmap

     Returns:
          sysex.WORD     
     """
     comm =  z48.commands.get(('\x14','\x0F'))
     return z48.execute(comm, ())

def curr_program_get_mod_tagged(z48):
     """Get name of current item with modified/tagged info.

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x10'))
     return z48.execute(comm, ())

def curr_program_get_modified(z48):
     """Get modified state of current item.  NA

     Returns:
          sysex.BYTE     
     """
     comm =  z48.commands.get(('\x14','\x11'))
     return z48.execute(comm, ())

def delete_tagged_programs(z48):
     """BYTE(0 ­ 7)

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x18'))
     return z48.execute(comm, ())

def create_program(z48, arg0):
     """Create New Program <Data1> = number of keygroups;<Data2> = name.

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x40'))
     return z48.execute(comm, (arg0, ))

def curr_program_add_keygroups(z48, arg0):
     """Add Keygroups to Program <Data1> = number of keygroups to add

     Returns:
               
     """
     comm =  z48.commands.get(('\x14','\x41'))
     return z48.execute(comm, (arg0, ))

def register_program_main(z48):
     comm = sysex.Command('\x14','\x01 ', 'get_no_programs', (), ())
     z48.commands[('\x14', '\x01 ')] = comm
     comm = sysex.Command('\x14','\x02\x00', 'program_get_handles', (), (sysex.DWORD,))
     z48.commands[('\x14', '\x02\x00')] = comm
     comm = sysex.Command('\x14','\x02\x01', 'program_get_names', (), (sysex.STRING,))
     z48.commands[('\x14', '\x02\x01')] = comm
     comm = sysex.Command('\x14','\x02\x02', 'program_get_handles_names', (), (sysex.DWORD, sysex.STRING))
     z48.commands[('\x14', '\x02\x02')] = comm
     comm = sysex.Command('\x14','\x02\x03', 'program_get_modified', (), (sysex.DWORD, sysex.STRING))
     z48.commands[('\x14', '\x02\x03')] = comm
     comm = sysex.Command('\x14','\x03', 'curr_program_select_by_handle', (sysex.DWORD,), ())
     z48.commands[('\x14', '\x03')] = comm
     comm = sysex.Command('\x14','\x04', 'curr_program_select_by_name', (sysex.STRING,), ())
     z48.commands[('\x14', '\x04')] = comm
     comm = sysex.Command('\x14','\x05', 'curr_program_get_handle', (), (sysex.DWORD,))
     z48.commands[('\x14', '\x05')] = comm
     comm = sysex.Command('\x14','\x06', 'curr_program_get_name', (), (sysex.STRING,))
     z48.commands[('\x14', '\x06')] = comm
     comm = sysex.Command('\x14','\x07', 'program_get_item_name_by_handle', (sysex.DWORD,), (sysex.STRING,))
     z48.commands[('\x14', '\x07')] = comm
     comm = sysex.Command('\x14','\x08', 'program_get_item_handle_from_name', (), (sysex.DWORD,))
     z48.commands[('\x14', '\x08')] = comm
     comm = sysex.Command('\x14','\x09', 'delete_all_programs', (), ())
     z48.commands[('\x14', '\x09')] = comm
     comm = sysex.Command('\x14','\x0A', 'curr_program_delete', (), ())
     z48.commands[('\x14', '\x0A')] = comm
     comm = sysex.Command('\x14','\x0B', 'delete_program_by_handle', (), ())
     z48.commands[('\x14', '\x0B')] = comm
     comm = sysex.Command('\x14','\x0C', 'curr_program_rename', (), ())
     z48.commands[('\x14', '\x0C')] = comm
     comm = sysex.Command('\x14','\x0D', 'rename_program_by_handle', (), ())
     z48.commands[('\x14', '\x0D')] = comm
     comm = sysex.Command('\x14','\x0E', 'tag_program', (sysex.BYTE,), ())
     z48.commands[('\x14', '\x0E')] = comm
     comm = sysex.Command('\x14','\x0F', 'program_get_tag_bitmap', (), (sysex.WORD,))
     z48.commands[('\x14', '\x0F')] = comm
     comm = sysex.Command('\x14','\x10', 'curr_program_get_mod_tagged', (), ())
     z48.commands[('\x14', '\x10')] = comm
     comm = sysex.Command('\x14','\x11', 'curr_program_get_modified', (), (sysex.BYTE,))
     z48.commands[('\x14', '\x11')] = comm
     comm = sysex.Command('\x14','\x18', 'delete_tagged_programs', (), ())
     z48.commands[('\x14', '\x18')] = comm
     comm = sysex.Command('\x14','\x40', 'create_program', (sysex.WORD,), ())
     z48.commands[('\x14', '\x40')] = comm
     comm = sysex.Command('\x14','\x41', 'curr_program_add_keygroups', (sysex.BYTE,), ())
     z48.commands[('\x14', '\x41')] = comm
