
""" Python equivalent of akai section songtools

Song
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex

class Songtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x01', 'get_no_items', (), None)
          self.commands['\x28\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x02\x00', 'get_handles', (), None)
          self.commands['\x28\x02\x00'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x02\x01', 'get_names', (), None)
          self.commands['\x28\x02\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x02\x02', 'get_handles_names', (), None)
          self.commands['\x28\x02\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x02\x03', 'get_handles_modified', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x28\x02\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x03', 'set_current_by_handle', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x28\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x04', 'set_current_by_name', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x28\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x05', 'get_current_handle', (), None)
          self.commands['\x28\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x06', 'get_current_name', (), None)
          self.commands['\x28\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x07', 'get_name_by_handle', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x28\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x08', 'get_handle_by_name', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x28\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x09', 'delete_all', (), None)
          self.commands['\x28\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x0A', 'delete_current', (), None)
          self.commands['\x28\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x0B', 'delete_by_handle', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x28\x0B'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x0C', 'rename_current', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x28\x0C'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x0D', 'rename_by_handle', (aksy.devices.akai.sysex.DWORD, aksy.devices.akai.sysex.STRING), None)
          self.commands['\x28\x0D'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x0E', 'set_tag_bit', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x28\x0E'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x0F', 'get_tag_bitmap', (), None)
          self.commands['\x28\x0F'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'get_curr_modified', (), None)
          self.commands['\x28\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x11 ', 'get_modified', (), None)
          self.commands['\x28\x11 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x18', 'delete_tagged', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x28\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x40', 'play_song', (), None)
          self.commands['\x28\x40'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x41', 'pause_song', (), None)
          self.commands['\x28\x41'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x42', 'stop_song', (), None)
          self.commands['\x28\x42'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x01', 'set_group_id', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x28\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'set_from_bar', (aksy.devices.akai.sysex.WORD,), None)
          self.commands['\x28\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'set_to_bar', (aksy.devices.akai.sysex.WORD,), None)
          self.commands['\x28\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x12', 'set_tempo_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x28\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x13', 'set_manual_tempo', (aksy.devices.akai.sysex.WORD,), None)
          self.commands['\x28\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x18', 'set_midi_output', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x28\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x01', 'get_group_id', (), None)
          self.commands['\x28\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'get_from_bar', (), None)
          self.commands['\x28\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x11', 'get_to_bar', (), None)
          self.commands['\x28\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x12', 'get_tempo_mode', (), None)
          self.commands['\x28\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x13', 'get_manual_tempo', (), None)
          self.commands['\x28\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x18', 'get_midi_output_port', (), None)
          self.commands['\x28\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x20', 'get_time_signature_beat', (), None)
          self.commands['\x28\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x21', 'get_time_sig_beat_no', (), None)
          self.commands['\x28\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x22', 'get_curr_beat', (), None)
          self.commands['\x28\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x23', 'get_curr_bar', (), None)
          self.commands['\x28\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x28\x24', 'get_curr_tempo', (), None)
          self.commands['\x28\x24'] = comm

     def get_no_items(self):
          """Get number of items in memory

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x28\x01')
          return self.z48.execute(comm, ())

     def get_handles(self):
          """Get Sample handles
          """
          comm = self.commands.get('\x28\x02\x00')
          return self.z48.execute(comm, ())

     def get_names(self):
          """Get sample names

          Returns:
               aksy.devices.akai.sysex.STRINGARRAY
          """
          comm = self.commands.get('\x28\x02\x01')
          return self.z48.execute(comm, ())

     def get_handles_names(self):
          """Get list of sample handles and names

          Returns:
               aksy.devices.akai.sysex.HANDLENAMEARRAY
          """
          comm = self.commands.get('\x28\x02\x02')
          return self.z48.execute(comm, ())

     def get_handles_modified(self, arg0):
          """Get a list of modified/tagged samples
          """
          comm = self.commands.get('\x28\x02\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_handle(self, arg0):
          """Select current item by handle
          """
          comm = self.commands.get('\x28\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_name(self, arg0):
          """Select current item by name
          """
          comm = self.commands.get('\x28\x04')
          return self.z48.execute(comm, (arg0, ))

     def get_current_handle(self):
          """Get handle of current item

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x28\x05')
          return self.z48.execute(comm, ())

     def get_current_name(self):
          """Get name of current item

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x28\x06')
          return self.z48.execute(comm, ())

     def get_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x28\x07')
          return self.z48.execute(comm, (arg0, ))

     def get_handle_by_name(self, arg0):
          """Get item handle from name

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x28\x08')
          return self.z48.execute(comm, (arg0, ))

     def delete_all(self):
          """Delete ALL items from memory
          """
          comm = self.commands.get('\x28\x09')
          return self.z48.execute(comm, ())

     def delete_current(self):
          """Delete current item from memory
          """
          comm = self.commands.get('\x28\x0A')
          return self.z48.execute(comm, ())

     def delete_by_handle(self, arg0):
          """Delete item represented by handle <Data1>
          """
          comm = self.commands.get('\x28\x0B')
          return self.z48.execute(comm, (arg0, ))

     def rename_current(self, arg0):
          """Rename current item
          """
          comm = self.commands.get('\x28\x0C')
          return self.z48.execute(comm, (arg0, ))

     def rename_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>
          """
          comm = self.commands.get('\x28\x0D')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_tag_bit(self, arg0, arg1):
          """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) BYTE(0, 1) <Data3> = (0=CURRENT, 1=ALL)
          """
          comm = self.commands.get('\x28\x0E')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_tag_bitmap(self):
          """Get Tag Bitmap
          """
          comm = self.commands.get('\x28\x0F')
          return self.z48.execute(comm, ())

     def get_curr_modified(self):
          """Get name of current item with modified/tagged info

          Returns:
               aksy.devices.akai.sysex.STRINGARRAY
          """
          comm = self.commands.get('\x28\x10')
          return self.z48.execute(comm, ())

     def get_modified(self):
          """Get modified state of current item.

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x28\x11 ')
          return self.z48.execute(comm, ())

     def delete_tagged(self, arg0):
          """Delete tagged items <Data1> = tag bit
          """
          comm = self.commands.get('\x28\x18')
          return self.z48.execute(comm, (arg0, ))

     def play_song(self):
          """Play Song
          """
          comm = self.commands.get('\x28\x40')
          return self.z48.execute(comm, ())

     def pause_song(self):
          """Pause Song
          """
          comm = self.commands.get('\x28\x41')
          return self.z48.execute(comm, ())

     def stop_song(self):
          """Stop Song
          """
          comm = self.commands.get('\x28\x42')
          return self.z48.execute(comm, ())

     def set_group_id(self, arg0):
          """Set Group ID
          """
          comm = self.commands.get('\x28\x01')
          return self.z48.execute(comm, (arg0, ))

     def set_from_bar(self, arg0):
          """Set From Bar
          """
          comm = self.commands.get('\x28\x10')
          return self.z48.execute(comm, (arg0, ))

     def set_to_bar(self, arg0):
          """Set To Bar
          """
          comm = self.commands.get('\x28\x10')
          return self.z48.execute(comm, (arg0, ))

     def set_tempo_mode(self, arg0):
          """Set Tempo Mode <Data1> = (0=FILE, 1=MANUAL, 2=MULTI)
          """
          comm = self.commands.get('\x28\x12')
          return self.z48.execute(comm, (arg0, ))

     def set_manual_tempo(self, arg0):
          """Set Manual Tempo <Data1> = (tempo×10)bpm
          """
          comm = self.commands.get('\x28\x13')
          return self.z48.execute(comm, (arg0, ))

     def set_midi_output(self, arg0):
          """Set MIDI output port <Data1> = (0=NONE, 1=MIDI A, 2=MIDI B)
          """
          comm = self.commands.get('\x28\x18')
          return self.z48.execute(comm, (arg0, ))

     def get_group_id(self):
          """Get Group ID

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x28\x01')
          return self.z48.execute(comm, ())

     def get_from_bar(self):
          """Get From Bar

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x28\x10')
          return self.z48.execute(comm, ())

     def get_to_bar(self):
          """Get To Bar

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x28\x11')
          return self.z48.execute(comm, ())

     def get_tempo_mode(self):
          """Get Tempo Mode <Reply> = (0=FILE, 1=MANUAL, 2=MULTI)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x28\x12')
          return self.z48.execute(comm, ())

     def get_manual_tempo(self):
          """Get Manual Tempo

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x28\x13')
          return self.z48.execute(comm, ())

     def get_midi_output_port(self):
          """Get MIDI output port <Reply> = (0=NONE, 1=MIDI A, 2=MIDI B

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x28\x18')
          return self.z48.execute(comm, ())

     def get_time_signature_beat(self):
          """Get (Time Signature) Beat Value

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x28\x20')
          return self.z48.execute(comm, ())

     def get_time_sig_beat_no(self):
          """Get (Time Signature) Beats-per-Bar

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x28\x21')
          return self.z48.execute(comm, ())

     def get_curr_beat(self):
          """Get Current Beat

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x28\x22')
          return self.z48.execute(comm, ())

     def get_curr_bar(self):
          """Get Current Bar

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x28\x23')
          return self.z48.execute(comm, ())

     def get_curr_tempo(self):
          """Get Current Tempo <Reply> = (tempo×10)bpm

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x28\x24')
          return self.z48.execute(comm, ())

