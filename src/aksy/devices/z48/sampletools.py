
""" Python equivalent of akai section sampletools

Sample
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.sysex

class Sampletools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          self.command_spec = aksy.sysex.CommandSpec('\x47\x5f\x00', aksy.sysex.CommandSpec.ID, aksy.sysex.CommandSpec.ARGS)
          comm = aksy.sysex.Command('\x1C\x01', 'get_no_items', (), (aksy.sysex.BYTE,))
          self.commands['\x1C\x01'] = comm
          comm = aksy.sysex.Command('\x1C\x02\x00', 'get_handles', (), ())
          self.commands['\x1C\x02\x00'] = comm
          comm = aksy.sysex.Command('\x1C\x02\x01', 'get_names', (), ())
          self.commands['\x1C\x02\x01'] = comm
          comm = aksy.sysex.Command('\x1C\x02\x02', 'get_handles_names', (), ())
          self.commands['\x1C\x02\x02'] = comm
          comm = aksy.sysex.Command('\x1C\x02\x03', 'get_handles_modified', (aksy.sysex.BYTE,), ())
          self.commands['\x1C\x02\x03'] = comm
          comm = aksy.sysex.Command('\x1C\x03', 'set_current_by_handle', (aksy.sysex.DWORD,), ())
          self.commands['\x1C\x03'] = comm
          comm = aksy.sysex.Command('\x1C\x04', 'set_current_by_name', (aksy.sysex.STRING,), ())
          self.commands['\x1C\x04'] = comm
          comm = aksy.sysex.Command('\x1C\x05', 'get_current_handle', (), (aksy.sysex.DWORD,))
          self.commands['\x1C\x05'] = comm
          comm = aksy.sysex.Command('\x1C\x06', 'get_current_name', (), (aksy.sysex.STRING,))
          self.commands['\x1C\x06'] = comm
          comm = aksy.sysex.Command('\x1C\x07', 'get_name_by_handle', (aksy.sysex.DWORD,), (aksy.sysex.STRING,))
          self.commands['\x1C\x07'] = comm
          comm = aksy.sysex.Command('\x1C\x08', 'get_handle_by_name', (aksy.sysex.STRING,), (aksy.sysex.DWORD,))
          self.commands['\x1C\x08'] = comm
          comm = aksy.sysex.Command('\x1C\x09', 'delete_all', (), ())
          self.commands['\x1C\x09'] = comm
          comm = aksy.sysex.Command('\x1C\x0A', 'delete_current', (), ())
          self.commands['\x1C\x0A'] = comm
          comm = aksy.sysex.Command('\x1C\x0B', 'delete_by_handle', (aksy.sysex.DWORD,), ())
          self.commands['\x1C\x0B'] = comm
          comm = aksy.sysex.Command('\x1C\x0C', 'rename_current', (aksy.sysex.STRING,), ())
          self.commands['\x1C\x0C'] = comm
          comm = aksy.sysex.Command('\x1C\x0D', 'rename_by_handle', (aksy.sysex.DWORD, aksy.sysex.STRING), ())
          self.commands['\x1C\x0D'] = comm
          comm = aksy.sysex.Command('\x1C\x0E', 'set_tag_bit', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x1C\x0E'] = comm
          comm = aksy.sysex.Command('\x1C\x0F', 'get_tag_bitmap', (), ())
          self.commands['\x1C\x0F'] = comm
          comm = aksy.sysex.Command('\x1C\x10', 'get_curr_modified', (), (aksy.sysex.STRING,))
          self.commands['\x1C\x10'] = comm
          comm = aksy.sysex.Command('\x1C\x11 ', 'get_modified', (), (aksy.sysex.BYTE,))
          self.commands['\x1C\x11 '] = comm
          comm = aksy.sysex.Command('\x1C\x18', 'delete_tagged', (aksy.sysex.BYTE,), ())
          self.commands['\x1C\x18'] = comm
          comm = aksy.sysex.Command('\x1C\x40', 'play', (aksy.sysex.BYTE, aksy.sysex.BOOL), ())
          self.commands['\x1C\x40'] = comm
          comm = aksy.sysex.Command('\x1C\x41', 'stop', (), ())
          self.commands['\x1C\x41'] = comm
          comm = aksy.sysex.Command('\x1C\x42', 'play_until', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1C\x42'] = comm
          comm = aksy.sysex.Command('\x1C\x43 ', 'play_from', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1C\x43 '] = comm
          comm = aksy.sysex.Command('\x1C\x44', 'play_over', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1C\x44'] = comm
          comm = aksy.sysex.Command('\x1C\x45', 'play_loop', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x1C\x45'] = comm
          comm = aksy.sysex.Command('\x1C\x46', 'play_region', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x1C\x46'] = comm
          comm = aksy.sysex.Command('\x1C\x48', 'create_loop', (), ())
          self.commands['\x1C\x48'] = comm
          comm = aksy.sysex.Command('\x1C\x49', 'delete_loop', (aksy.sysex.BYTE,), ())
          self.commands['\x1C\x49'] = comm
          comm = aksy.sysex.Command('\x1C\x4A', 'create_region', (), ())
          self.commands['\x1C\x4A'] = comm
          comm = aksy.sysex.Command('\x1C\x4B', 'delete_region', (aksy.sysex.BYTE,), ())
          self.commands['\x1C\x4B'] = comm
          comm = aksy.sysex.Command('\x1F\x01', 'get_group_id', (), (aksy.sysex.BYTE,))
          self.commands['\x1F\x01'] = comm
          comm = aksy.sysex.Command('\x1F\x20', 'get_trim_start', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x20'] = comm
          comm = aksy.sysex.Command('\x1F\x21', 'get_trim_end', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x21'] = comm
          comm = aksy.sysex.Command('\x1F\x22', 'get_trim_length', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x22'] = comm
          comm = aksy.sysex.Command('\x1F\x24', 'get_orig_pitch', (), (aksy.sysex.BYTE,))
          self.commands['\x1F\x24'] = comm
          comm = aksy.sysex.Command('\x1F\x25', 'get_cents_tune', (), (aksy.sysex.SWORD,))
          self.commands['\x1F\x25'] = comm
          comm = aksy.sysex.Command('\x1F\x26', 'get_playback_mode', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x1F\x26'] = comm
          comm = aksy.sysex.Command('\x1F\x30', 'get_loop_start', (aksy.sysex.BYTE,), (aksy.sysex.QWORD,))
          self.commands['\x1F\x30'] = comm
          comm = aksy.sysex.Command('\x1F\x31', 'get_loop_end', (aksy.sysex.BYTE,), (aksy.sysex.QWORD,))
          self.commands['\x1F\x31'] = comm
          comm = aksy.sysex.Command('\x1F\x32', 'get_loop_length', (aksy.sysex.BYTE,), (aksy.sysex.QWORD,))
          self.commands['\x1F\x32'] = comm
          comm = aksy.sysex.Command('\x1F\x33', 'get_loop_lock', (aksy.sysex.BOOL,), (aksy.sysex.BYTE,))
          self.commands['\x1F\x33'] = comm
          comm = aksy.sysex.Command('\x1F\x34', 'get_loop_tune', (aksy.sysex.BYTE,), (aksy.sysex.SBYTE,))
          self.commands['\x1F\x34'] = comm
          comm = aksy.sysex.Command('\x1F\x35', 'get_loop_dir', (aksy.sysex.BOOL,), (aksy.sysex.BYTE,))
          self.commands['\x1F\x35'] = comm
          comm = aksy.sysex.Command('\x1F\x36', 'get_loop_type', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x1F\x36'] = comm
          comm = aksy.sysex.Command('\x1F\x37', 'get_no_loop_reps', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x1F\x37'] = comm
          comm = aksy.sysex.Command('\x1F\x38', 'get_no_loops', (), (aksy.sysex.BYTE,))
          self.commands['\x1F\x38'] = comm
          comm = aksy.sysex.Command('\x1F\x40', 'get_region_start', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x40'] = comm
          comm = aksy.sysex.Command('\x1F\x41', 'get_region_end', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x41'] = comm
          comm = aksy.sysex.Command('\x1F\x42', 'get_region_lenght', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x42'] = comm
          comm = aksy.sysex.Command('\x1F\x44', 'get_no_regions', (), (aksy.sysex.BYTE,))
          self.commands['\x1F\x44'] = comm
          comm = aksy.sysex.Command('\x1F\x50', 'get_sample_length', (), (aksy.sysex.QWORD,))
          self.commands['\x1F\x50'] = comm
          comm = aksy.sysex.Command('\x1F\x51', 'get_sample_rate', (), (aksy.sysex.DWORD,))
          self.commands['\x1F\x51'] = comm
          comm = aksy.sysex.Command('\x1F\x52', 'get_bit_depth', (), (aksy.sysex.BYTE,))
          self.commands['\x1F\x52'] = comm
          comm = aksy.sysex.Command('\x1F\x54', 'get_sample_type', (), (aksy.sysex.BOOL,))
          self.commands['\x1F\x54'] = comm
          comm = aksy.sysex.Command('\x1F\x55', 'get_no_channels', (), (aksy.sysex.BYTE,))
          self.commands['\x1F\x55'] = comm
          comm = aksy.sysex.Command('\x1E\x01', 'set_group_id', (aksy.sysex.BYTE,), ())
          self.commands['\x1E\x01'] = comm
          comm = aksy.sysex.Command('\x1E\x20', 'set_trim_start', (aksy.sysex.QWORD,), ())
          self.commands['\x1E\x20'] = comm
          comm = aksy.sysex.Command('\x1E\x21', 'set_trim_end', (aksy.sysex.QWORD,), ())
          self.commands['\x1E\x21'] = comm
          comm = aksy.sysex.Command('\x1E\x22', 'set_trim_length', (aksy.sysex.QWORD,), ())
          self.commands['\x1E\x22'] = comm
          comm = aksy.sysex.Command('\x1E\x24', 'set_orig_pitch', (aksy.sysex.BYTE,), ())
          self.commands['\x1E\x24'] = comm
          comm = aksy.sysex.Command('\x1E\x25', 'set_tune', (aksy.sysex.SWORD,), ())
          self.commands['\x1E\x25'] = comm
          comm = aksy.sysex.Command('\x1E\x26', 'set_playback_mode', (), ())
          self.commands['\x1E\x26'] = comm
          comm = aksy.sysex.Command('\x1E\x30', 'set_loop_start', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1E\x30'] = comm
          comm = aksy.sysex.Command('\x1E\x31', 'set_loop_end', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1E\x31'] = comm
          comm = aksy.sysex.Command('\x1E\x32', 'set_loop_length', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1E\x32'] = comm
          comm = aksy.sysex.Command('\x1E\x33', 'set_loop_lock', (aksy.sysex.BYTE, aksy.sysex.BOOL), ())
          self.commands['\x1E\x33'] = comm
          comm = aksy.sysex.Command('\x1E\x34', 'set_loop_tune', (aksy.sysex.BYTE, aksy.sysex.SBYTE), ())
          self.commands['\x1E\x34'] = comm
          comm = aksy.sysex.Command('\x1E\x35', 'set_loop_direction', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x1E\x35'] = comm
          comm = aksy.sysex.Command('\x1E\x36', 'set_loop_type', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x1E\x36'] = comm
          comm = aksy.sysex.Command('\x1E\x37', 'set_no_loop_repetitions', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x1E\x37'] = comm
          comm = aksy.sysex.Command('\x1E\x40', 'set_region_start', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1E\x40'] = comm
          comm = aksy.sysex.Command('\x1E\x41', 'set_region_end', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1E\x41'] = comm
          comm = aksy.sysex.Command('\x1E\x42', 'set_region_length', (aksy.sysex.BYTE, aksy.sysex.QWORD), ())
          self.commands['\x1E\x42'] = comm

     def get_no_items(self):
          """Get number of items in memory

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1C\x01')
          return self.z48.execute(comm, ())

     def get_handles(self):
          """Get Sample handles
          """
          comm = self.commands.get('\x1C\x02\x00')
          return self.z48.execute(comm, ())

     def get_names(self):
          """Get sample names
          """
          comm = self.commands.get('\x1C\x02\x01')
          return self.z48.execute(comm, ())

     def get_handles_names(self):
          """Get list of sample handles and names
          """
          comm = self.commands.get('\x1C\x02\x02')
          return self.z48.execute(comm, ())

     def get_handles_modified(self, arg0):
          """Get a list of modified/tagged samples
          """
          comm = self.commands.get('\x1C\x02\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_handle(self, arg0):
          """Select current item by handle
          """
          comm = self.commands.get('\x1C\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_current_by_name(self, arg0):
          """Select current item by name
          """
          comm = self.commands.get('\x1C\x04')
          return self.z48.execute(comm, (arg0, ))

     def get_current_handle(self):
          """Get handle of current item

          Returns:
               aksy.sysex.DWORD
          """
          comm = self.commands.get('\x1C\x05')
          return self.z48.execute(comm, ())

     def get_current_name(self):
          """Get name of current item

          Returns:
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x1C\x06')
          return self.z48.execute(comm, ())

     def get_name_by_handle(self, arg0):
          """Get item name from handle

          Returns:
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x1C\x07')
          return self.z48.execute(comm, (arg0, ))

     def get_handle_by_name(self, arg0):
          """Get item handle from name

          Returns:
               aksy.sysex.DWORD
          """
          comm = self.commands.get('\x1C\x08')
          return self.z48.execute(comm, (arg0, ))

     def delete_all(self):
          """Delete ALL items from memory
          """
          comm = self.commands.get('\x1C\x09')
          return self.z48.execute(comm, ())

     def delete_current(self):
          """Delete current item from memory
          """
          comm = self.commands.get('\x1C\x0A')
          return self.z48.execute(comm, ())

     def delete_by_handle(self, arg0):
          """Delete item represented by handle <Data1>
          """
          comm = self.commands.get('\x1C\x0B')
          return self.z48.execute(comm, (arg0, ))

     def rename_current(self, arg0):
          """Rename current item
          """
          comm = self.commands.get('\x1C\x0C')
          return self.z48.execute(comm, (arg0, ))

     def rename_by_handle(self, arg0, arg1):
          """Rename item represented by handle <Data1>
          """
          comm = self.commands.get('\x1C\x0D')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_tag_bit(self, arg0, arg1):
          """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) BYTE(0, 1) <Data3> = (0=CURRENT, 1=ALL)
          """
          comm = self.commands.get('\x1C\x0E')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_tag_bitmap(self):
          """Get Tag Bitmap
          """
          comm = self.commands.get('\x1C\x0F')
          return self.z48.execute(comm, ())

     def get_curr_modified(self):
          """Get name of current item with modified/tagged info

          Returns:
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x1C\x10')
          return self.z48.execute(comm, ())

     def get_modified(self):
          """Get modified state of current item.

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1C\x11 ')
          return self.z48.execute(comm, ())

     def delete_tagged(self, arg0):
          """Delete tagged items <Data1> = tag bit
          """
          comm = self.commands.get('\x1C\x18')
          return self.z48.execute(comm, (arg0, ))

     def play(self, arg0, arg1):
          """Start auditioning the current sample <Data1> = velocity <Data2> =(NO LOOPING, 1=LOOPING)
          """
          comm = self.commands.get('\x1C\x40')
          return self.z48.execute(comm, (arg0, arg1, ))

     def stop(self):
          """Stop playback of the current sample
          """
          comm = self.commands.get('\x1C\x41')
          return self.z48.execute(comm, ())

     def play_until(self, arg0, arg1):
          """Play To <Data1> = velocity, <Data2> = sample position
          """
          comm = self.commands.get('\x1C\x42')
          return self.z48.execute(comm, (arg0, arg1, ))

     def play_from(self, arg0, arg1):
          """Play From <Data1> = velocity, <Data2> = sample position
          """
          comm = self.commands.get('\x1C\x43 ')
          return self.z48.execute(comm, (arg0, arg1, ))

     def play_over(self, arg0, arg1):
          """Play Over <Data1> = velocity, <Data2> = sample position
          """
          comm = self.commands.get('\x1C\x44')
          return self.z48.execute(comm, (arg0, arg1, ))

     def play_loop(self, arg0, arg1):
          """Play Loop <Data1> = velocity, <Data2> = loop index
          """
          comm = self.commands.get('\x1C\x45')
          return self.z48.execute(comm, (arg0, arg1, ))

     def play_region(self, arg0, arg1):
          """Play Region <Data1> = velocity, <Data2> = region index
          """
          comm = self.commands.get('\x1C\x46')
          return self.z48.execute(comm, (arg0, arg1, ))

     def create_loop(self):
          """Create New Loop
          """
          comm = self.commands.get('\x1C\x48')
          return self.z48.execute(comm, ())

     def delete_loop(self, arg0):
          """Delete Loop <Data1> = index
          """
          comm = self.commands.get('\x1C\x49')
          return self.z48.execute(comm, (arg0, ))

     def create_region(self):
          """Create Region
          """
          comm = self.commands.get('\x1C\x4A')
          return self.z48.execute(comm, ())

     def delete_region(self, arg0):
          """Delete Region <Data1> = index
          """
          comm = self.commands.get('\x1C\x4B')
          return self.z48.execute(comm, (arg0, ))

     def get_group_id(self):
          """Get Group ID

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x01')
          return self.z48.execute(comm, ())

     def get_trim_start(self):
          """Get Trim Start

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x20')
          return self.z48.execute(comm, ())

     def get_trim_end(self):
          """Get Trim End

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x21')
          return self.z48.execute(comm, ())

     def get_trim_length(self):
          """Get Trim Length

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x22')
          return self.z48.execute(comm, ())

     def get_orig_pitch(self):
          """Get Original Pitch

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x24')
          return self.z48.execute(comm, ())

     def get_cents_tune(self):
          """Get Cents Tune (0 ­ ± 36 00)

          Returns:
               aksy.sysex.SWORD
          """
          comm = self.commands.get('\x1F\x25')
          return self.z48.execute(comm, ())

     def get_playback_mode(self, arg0):
          """Get Playback Mode, where <Data1> = (0=NO LOOPING, 1=LOOPING, 2=ONE SHOT)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x26')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_start(self, arg0):
          """Get Loop Start <Data1> = loop index

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x30')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_end(self, arg0):
          """Get Loop End <Data1> = loop index

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x31')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_length(self, arg0):
          """Get Loop Length <Data1> = loop index

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x32')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_lock(self, arg0):
          """Get Loop Lock <Data1> = (0=OFF, 1=ON)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x33')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_tune(self, arg0):
          """Get Loop Tune (0­±50)

          Returns:
               aksy.sysex.SBYTE
          """
          comm = self.commands.get('\x1F\x34')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_dir(self, arg0):
          """Get Loop Direction <Data1> = (0=FORWARDS, 1=ALTERNATING)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x35')
          return self.z48.execute(comm, (arg0, ))

     def get_loop_type(self, arg0):
          """Get Loop Type <Data1> = (0=LOOP IN REL, 1=LOOP UNTIL REL)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x36')
          return self.z48.execute(comm, (arg0, ))

     def get_no_loop_reps(self, arg0):
          """Get Number of Loop Repetitions

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x37')
          return self.z48.execute(comm, (arg0, ))

     def get_no_loops(self):
          """Get Number of Loops

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x38')
          return self.z48.execute(comm, ())

     def get_region_start(self):
          """Get Region Start <Data1> = Region Num (0-31), <Reply1> = start

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x40')
          return self.z48.execute(comm, ())

     def get_region_end(self):
          """Get Region End <Data1> = Region Num (0­31) <Reply1> = end

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x41')
          return self.z48.execute(comm, ())

     def get_region_lenght(self):
          """Get Region Length <Data1> = Region Num (0­31) <Reply1> = length

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x42')
          return self.z48.execute(comm, ())

     def get_no_regions(self):
          """Get Number of Regions

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x44')
          return self.z48.execute(comm, ())

     def get_sample_length(self):
          """Get Sample Length

          Returns:
               aksy.sysex.QWORD
          """
          comm = self.commands.get('\x1F\x50')
          return self.z48.execute(comm, ())

     def get_sample_rate(self):
          """Get Sample Rate [Hz]

          Returns:
               aksy.sysex.DWORD
          """
          comm = self.commands.get('\x1F\x51')
          return self.z48.execute(comm, ())

     def get_bit_depth(self):
          """Get Sample Bit-Depth [bits]

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x52')
          return self.z48.execute(comm, ())

     def get_sample_type(self):
          """Get Sample Type <Reply> = (0=RAM, 1=VIRTUAL)

          Returns:
               aksy.sysex.BOOL
          """
          comm = self.commands.get('\x1F\x54')
          return self.z48.execute(comm, ())

     def get_no_channels(self):
          """Get Number of Channels

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x1F\x55')
          return self.z48.execute(comm, ())

     def set_group_id(self, arg0):
          """Set Group ID
          """
          comm = self.commands.get('\x1E\x01')
          return self.z48.execute(comm, (arg0, ))

     def set_trim_start(self, arg0):
          """Set Trim Start
          """
          comm = self.commands.get('\x1E\x20')
          return self.z48.execute(comm, (arg0, ))

     def set_trim_end(self, arg0):
          """Set Trim End
          """
          comm = self.commands.get('\x1E\x21')
          return self.z48.execute(comm, (arg0, ))

     def set_trim_length(self, arg0):
          """Set Trim Length
          """
          comm = self.commands.get('\x1E\x22')
          return self.z48.execute(comm, (arg0, ))

     def set_orig_pitch(self, arg0):
          """Set Original Pitch
          """
          comm = self.commands.get('\x1E\x24')
          return self.z48.execute(comm, (arg0, ))

     def set_tune(self, arg0):
          """Set Cents Tune
          """
          comm = self.commands.get('\x1E\x25')
          return self.z48.execute(comm, (arg0, ))

     def set_playback_mode(self):
          """Set Playback Mode, where <Data1> = (0=NO LOOPING, 1=LOOPING, 2=ONE SHOT)
          """
          comm = self.commands.get('\x1E\x26')
          return self.z48.execute(comm, ())

     def set_loop_start(self, arg0, arg1):
          """Set Loop Start <Data1> = loop index
          """
          comm = self.commands.get('\x1E\x30')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_loop_end(self, arg0, arg1):
          """Set Loop End
          """
          comm = self.commands.get('\x1E\x31')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_loop_length(self, arg0, arg1):
          """Set Loop Length
          """
          comm = self.commands.get('\x1E\x32')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_loop_lock(self, arg0, arg1):
          """Set Loop Lock <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x1E\x33')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_loop_tune(self, arg0, arg1):
          """Set Loop Tune (0­±50)
          """
          comm = self.commands.get('\x1E\x34')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_loop_direction(self, arg0, arg1):
          """Set Loop Direction <Data1> = (0=FORWARDS, 1=ALTERNATING)
          """
          comm = self.commands.get('\x1E\x35')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_loop_type(self, arg0, arg1):
          """Set Loop Type <Data1> = (0=LOOP IN REL, 1=LOOP UNTIL REL)
          """
          comm = self.commands.get('\x1E\x36')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_no_loop_repetitions(self, arg0, arg1):
          """Set Number of Loop Repetitions (0=INFINITE)
          """
          comm = self.commands.get('\x1E\x37')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_region_start(self, arg0, arg1):
          """Set Region Start <Data1> = Region Num, <Data2> = start
          """
          comm = self.commands.get('\x1E\x40')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_region_end(self, arg0, arg1):
          """Set Region End <Data1> = Region Num <Data2> = end
          """
          comm = self.commands.get('\x1E\x41')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_region_length(self, arg0, arg1):
          """Set Region Length <Data1> = Region Num <Data2> = length
          """
          comm = self.commands.get('\x1E\x42')
          return self.z48.execute(comm, (arg0, arg1, ))

