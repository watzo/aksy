
""" Python equivalent of akai section programtools

Methods to manipulate sampler programs
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex

class Programtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x01', 'get_no_items', (), None)
          self.commands['\x14\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x02\x00', 'get_handles', (), None)
          self.commands['\x14\x02\x00'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x02\x01', 'get_names', (), None)
          self.commands['\x14\x02\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x02\x02', 'get_handles_names', (), (aksy.devices.akai.sysex.HANDLENAMEARRAY,))
          self.commands['\x14\x02\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x02\x03', 'get_modified', (), None)
          self.commands['\x14\x02\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x03', 'set_current_by_handle', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x14\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x04', 'set_current_by_name', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x14\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x05', 'get_current_handle', (), None)
          self.commands['\x14\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x06', 'get_current_name', (), None)
          self.commands['\x14\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x07', 'get_name_by_handle', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x14\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x08', 'get_handle_by_name', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x14\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x09', 'delete_all', (), None)
          self.commands['\x14\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x0A', 'delete_current', (), None)
          self.commands['\x14\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x0B', 'delete_by_handle', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x14\x0B'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x0C', 'rename_current', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x14\x0C'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x0D', 'rename_by_handle', (aksy.devices.akai.sysex.DWORD, aksy.devices.akai.sysex.STRING), None)
          self.commands['\x14\x0D'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x0E', 'tag', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x14\x0E'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x0F', 'get_tag_bitmap', (), None)
          self.commands['\x14\x0F'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x10', 'get_modified_name', (), None)
          self.commands['\x14\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x11', 'get_modified_state', (), None)
          self.commands['\x14\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x18', 'delete_tagged', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x14\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x40', 'create_new', (aksy.devices.akai.sysex.WORD, aksy.devices.akai.sysex.STRING), None)
          self.commands['\x14\x40'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x14\x41', 'add_keygroups_to_current', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x14\x41'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x01', 'get_group_id', (), None)
          self.commands['\x17\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x03', 'get_type', (), None)
          self.commands['\x17\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x04', 'get_genre', (), None)
          self.commands['\x17\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x08', 'get_program_no', (), None)
          self.commands['\x17\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x09', 'get_no_keygroups', (), None)
          self.commands['\x17\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x0A', 'get_keygroup_xfade', (), None)
          self.commands['\x17\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x0B', 'get_keygroup_xfade_type', (), None)
          self.commands['\x17\x0B'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x0C', 'get_level', (), None)
          self.commands['\x17\x0C'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x10', 'get_polyphony', (), None)
          self.commands['\x17\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x11', 'get_reassignment_method', (), None)
          self.commands['\x17\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x12', 'get_softpedal_loudness_reduction', (), None)
          self.commands['\x17\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x17\x13', 'get_softpedal_attack_stretch', (), None)
          self.commands['\x17\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x01', 'set_group_id', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x03', 'set_type', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x04', 'set_genre', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x16\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x08', 'set_program_no', (aksy.devices.akai.sysex.WORD,), None)
          self.commands['\x16\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x09', 'set_no_keygroups', (aksy.devices.akai.sysex.WORD,), None)
          self.commands['\x16\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x0A', 'set_keygroup_xfade', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x0B', 'set_keygroup_xfade_type', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x0B'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x0C', 'set_level', (aksy.devices.akai.sysex.SWORD,), None)
          self.commands['\x16\x0C'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x10', 'set_polyphony', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x11', 'set_reassignment_method', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x12', 'set_softpedal_loudness_reduction', (), None)
          self.commands['\x16\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x13', 'set_softpedal_attack_stretch', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x14', 'set_softpedal_filter_close', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x16\x14'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x15', 'set_midi_transpose', (aksy.devices.akai.sysex.SBYTE,), None)
          self.commands['\x16\x15'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x18', 'set_mpc_pad_assignment', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x16\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x20', 'set_modulation_conn', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.WORD, aksy.devices.akai.sysex.WORD, aksy.devices.akai.sysex.WORD, aksy.devices.akai.sysex.SBYTE), None)
          self.commands['\x16\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x21', 'set_modulation_src', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.WORD), None)
          self.commands['\x16\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x22', 'set_modulation_dest', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.WORD), None)
          self.commands['\x16\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x23', 'set_modulation_level', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.WORD, aksy.devices.akai.sysex.SBYTE), None)
          self.commands['\x16\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x24', 'set_midi_ctrl_no', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x16\x24'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x25', 'set_edit_keygroup', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.WORD), None)
          self.commands['\x16\x25'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x16\x26', 'set_edit_kegyroup_modulation_level', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x16\x26'] = comm

     def get_no_items(self):
          """Get number of items in memory
          """
          comm = self.commands.get('\x14\x01')
          return self.z48.execute(comm, ())

     def get_handles(self):
          """Get list of info for all items: 0=list of handles;

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x14\x02\x00')
          return self.z48.execute(comm, ())

     def get_names(self):
          """Get list of info for all items: 1=list of names

          Returns:
               aksy.devices.akai.sysex.STRINGARRAY
          """
          comm = self.commands.get('\x14\x02\x01')
          return self.z48.execute(comm, ())

     def get_handles_names(self):
          """Get list of info for all items: 2=list of handle+name;

          Returns:
               aksy.devices.akai.sysex.HANDLENAMEARRAY
          """
          comm = self.commands.get('\x14\x02\x02')
          return self.z48.execute(comm, ())

     def get_modified(self):
          """Get list of info for all items: 3=list of handle+modified/tagged name

          Returns:
               aksy.devices.akai.sysex.HANDLENAMEARRAY
          """
          comm = self.commands.get('\x14\x02\x03')
          return self.z48.execute(comm, ())

     def set_current_by_handle(self, arg0):
          """Select current item by handle
          """
          comm = self.commands.get('\x14\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_name(self, arg0):
          """Select current item by name
          """
          comm = self.commands.get('\x14\x04')
          return self.z48.execute(comm, (arg0, ))

     def get_current_handle(self):
          """Get handle of current item

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x14\x05')
          return self.z48.execute(comm, ())

     def get_current_name(self):
          """Get name of current item

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x14\x06')
          return self.z48.execute(comm, ())

     def get_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x14\x07')
          return self.z48.execute(comm, (arg0, ))

     def get_handle_by_name(self, arg0):
          """Get item handle from name

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x14\x08')
          return self.z48.execute(comm, (arg0, ))

     def delete_all(self):
          """Delete ALL items from memory
          """
          comm = self.commands.get('\x14\x09')
          return self.z48.execute(comm, ())

     def delete_current(self):
          """Delete current item from memory
          """
          comm = self.commands.get('\x14\x0A')
          return self.z48.execute(comm, ())

     def delete_by_handle(self, arg0):
          """Delete item represented by handle <Data1>
          """
          comm = self.commands.get('\x14\x0B')
          return self.z48.execute(comm, (arg0, ))

     def rename_current(self, arg0):
          """Rename current item
          """
          comm = self.commands.get('\x14\x0C')
          return self.z48.execute(comm, (arg0, ))

     def rename_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>
          """
          comm = self.commands.get('\x14\x0D')
          return self.z48.execute(comm, (arg0, arg1, ))

     def tag(self, arg0, arg1):
          """Set Tag Bit <Data1> = bit to set(0-7), <Data2> = (0=OFF, 1=ON), Data3> = (0=CURRENT, 1=ALL)
          """
          comm = self.commands.get('\x14\x0E')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_tag_bitmap(self):
          """Get Tag Bitmap

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x14\x0F')
          return self.z48.execute(comm, ())

     def get_modified_name(self):
          """Get name of current item with modified/tagged info.
          """
          comm = self.commands.get('\x14\x10')
          return self.z48.execute(comm, ())

     def get_modified_state(self):
          """Get modified state of current item.

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x14\x11')
          return self.z48.execute(comm, ())

     def delete_tagged(self, arg0):
          """Delete tagged items <Data1> = tag bit
          """
          comm = self.commands.get('\x14\x18')
          return self.z48.execute(comm, (arg0, ))

     def create_new(self, arg0, arg1):
          """Create New Program <Data1> = number of keygroups;<Data2> = name.
          """
          comm = self.commands.get('\x14\x40')
          return self.z48.execute(comm, (arg0, arg1, ))

     def add_keygroups_to_current(self, arg0):
          """Add Keygroups to Program <Data1> = number of keygroups to add
          """
          comm = self.commands.get('\x14\x41')
          return self.z48.execute(comm, (arg0, ))

     def get_group_id(self):
          """Get Group ID

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x01')
          return self.z48.execute(comm, ())

     def get_type(self):
          """Get Program Type <Reply> = (0=KEYGROUP, 1=DRUM)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x03')
          return self.z48.execute(comm, ())

     def get_genre(self):
          """Get Genre

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x17\x04')
          return self.z48.execute(comm, ())

     def get_program_no(self):
          """Get Program Number <Reply1> = (0=OFF, 1­128)

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x17\x08')
          return self.z48.execute(comm, ())

     def get_no_keygroups(self):
          """Get Number of keygroups

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x17\x09')
          return self.z48.execute(comm, ())

     def get_keygroup_xfade(self):
          """Get Keygroup Crossfade <Reply1> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x0A')
          return self.z48.execute(comm, ())

     def get_keygroup_xfade_type(self):
          """Get Keygroup Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x0B')
          return self.z48.execute(comm, ())

     def get_level(self):
          """Get Program Level <Reply1> = level in 10×dB

          Returns:
               aksy.devices.akai.sysex.SWORD
          """
          comm = self.commands.get('\x17\x0C')
          return self.z48.execute(comm, ())

     def get_polyphony(self):
          """Get Polyphony

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x10')
          return self.z48.execute(comm, ())

     def get_reassignment_method(self):
          """Get Reassignment <Reply1> = (0=QUIETEST, 1=OLDEST)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x11')
          return self.z48.execute(comm, ())

     def get_softpedal_loudness_reduction(self):
          """Soft Pedal Loudness Reduction

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x12')
          return self.z48.execute(comm, ())

     def get_softpedal_attack_stretch(self):
          """Soft Pedal Attack Stretch

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x17\x13')
          return self.z48.execute(comm, ())

     def set_group_id(self, arg0):
          """Set Group ID
          """
          comm = self.commands.get('\x16\x01')
          return self.z48.execute(comm, (arg0, ))

     def set_type(self, arg0):
          """Set Program Type <Data1> = (0=KEYGROUP, 1=DRUM)
          """
          comm = self.commands.get('\x16\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_genre(self, arg0):
          """Set Genre
          """
          comm = self.commands.get('\x16\x04')
          return self.z48.execute(comm, (arg0, ))

     def set_program_no(self, arg0):
          """Set Program Number <Data1> = (0=OFF, 1­128)
          """
          comm = self.commands.get('\x16\x08')
          return self.z48.execute(comm, (arg0, ))

     def set_no_keygroups(self, arg0):
          """Set Number of keygroups
          """
          comm = self.commands.get('\x16\x09')
          return self.z48.execute(comm, (arg0, ))

     def set_keygroup_xfade(self, arg0):
          """Set Keygroup Crossfade <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x16\x0A')
          return self.z48.execute(comm, (arg0, ))

     def set_keygroup_xfade_type(self, arg0):
          """Set Keygroup Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)
          """
          comm = self.commands.get('\x16\x0B')
          return self.z48.execute(comm, (arg0, ))

     def set_level(self, arg0):
          """Set Program Level <Data1> = level in 10×dB (-600 ­ +60)
          """
          comm = self.commands.get('\x16\x0C')
          return self.z48.execute(comm, (arg0, ))

     def set_polyphony(self, arg0):
          """Set Polyphony
          """
          comm = self.commands.get('\x16\x10')
          return self.z48.execute(comm, (arg0, ))

     def set_reassignment_method(self, arg0):
          """Set Reassignment <Data1> = (0=QUIETEST, 1=OLDEST)
          """
          comm = self.commands.get('\x16\x11')
          return self.z48.execute(comm, (arg0, ))

     def set_softpedal_loudness_reduction(self):
          """Soft Pedal Loudness Reduction
          """
          comm = self.commands.get('\x16\x12')
          return self.z48.execute(comm, ())

     def set_softpedal_attack_stretch(self, arg0):
          """Soft Pedal Attack Stretch
          """
          comm = self.commands.get('\x16\x13')
          return self.z48.execute(comm, (arg0, ))

     def set_softpedal_filter_close(self, arg0):
          """Soft Pedal Filter Close
          """
          comm = self.commands.get('\x16\x14')
          return self.z48.execute(comm, (arg0, ))

     def set_midi_transpose(self, arg0):
          """Midi Transpose (-36 ­ +36)
          """
          comm = self.commands.get('\x16\x15')
          return self.z48.execute(comm, (arg0, ))

     def set_mpc_pad_assignment(self, arg0, arg1):
          """MPC pad assignment <Data1> = pad, <Data2> = note
          """
          comm = self.commands.get('\x16\x18')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_modulation_conn(self, arg0, arg1, arg2, arg3, arg4):
          """Set Modulation Connection <Data1> = connection (pin) number;<Data2> = keygroup number (0=ALL, 1­128=KEYGROUP) <Data3> = source (see Table 24); <Data4> = destination (see Table 25); <Data5> = level.  If Source or Destination is zero, the connection will be cleared.
          """
          comm = self.commands.get('\x16\x20')
          return self.z48.execute(comm, (arg0, arg1, arg2, arg3, arg4, ))

     def set_modulation_src(self, arg0, arg1):
          """Set Modulation Source (see Table 24)
          """
          comm = self.commands.get('\x16\x21')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_modulation_dest(self, arg0, arg1):
          """Set Modulation Destination (see Table 25)
          """
          comm = self.commands.get('\x16\x22')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_modulation_level(self, arg0, arg1, arg2):
          """Set Modulation Level <Data1> = pin number; <Data2> = (0=ALL, 1­128=KEYGROUP); <Data3> = level
          """
          comm = self.commands.get('\x16\x23')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def set_midi_ctrl_no(self, arg0, arg1):
          """Set MIDI controller number (only used if Source = CTRL)
          """
          comm = self.commands.get('\x16\x24')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_edit_keygroup(self, arg0, arg1):
          """Set Edit Keygroup (used to edit level) <Data2> = Edit Keygroup
          """
          comm = self.commands.get('\x16\x25')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_edit_kegyroup_modulation_level(self, arg0, arg1):
          """Set Modulation Level of Edit Keygroup
          """
          comm = self.commands.get('\x16\x26')
          return self.z48.execute(comm, (arg0, arg1, ))

