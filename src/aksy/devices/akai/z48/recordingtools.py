
""" Python equivalent of akai section recordingtools

Methods to facilitate recording
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex

class Recordingtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x01', 'get_status', (), None)
          self.commands['\x30\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x02', 'get_progress', (), None)
          self.commands['\x30\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x03', 'get_max_rec_time', (), None)
          self.commands['\x30\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x10', 'arm', (), None)
          self.commands['\x30\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x11', 'start', (), None)
          self.commands['\x30\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x12', 'stop', (), None)
          self.commands['\x30\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x13', 'cancel', (), None)
          self.commands['\x30\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x20', 'start_playing', (), None)
          self.commands['\x30\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x21', 'stop_playing', (), None)
          self.commands['\x30\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x22', 'keep', (), None)
          self.commands['\x30\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x30\x23', 'delete', (), None)
          self.commands['\x30\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x01', 'set_input', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x32\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x02', 'set_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x32\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x03', 'enable_monitor', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x32\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x04', 'set_rec_time', (aksy.devices.akai.sysex.DWORD,), None)
          self.commands['\x32\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x05', 'set_orig_pitch', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x32\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x06', 'set_threshold', (aksy.devices.akai.sysex.SBYTE,), None)
          self.commands['\x32\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x07', 'set_trigger_src', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x32\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x08', 'set_bit_depth', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x32\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x09', 'set_prerec_time', (aksy.devices.akai.sysex.WORD,), None)
          self.commands['\x32\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x0A', 'set_dest', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x32\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x10', 'set_name', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x32\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x11', 'set_name_seed', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x32\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x12', 'set_autorec_mode', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x32\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x32\x13', 'set_autonormalize', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x32\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x01', 'get_input', (), None)
          self.commands['\x33\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x02', 'get_mode', (), None)
          self.commands['\x33\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x03', 'get_monitor', (), None)
          self.commands['\x33\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x04', 'get_rec_time', (), None)
          self.commands['\x33\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x05', 'get_pitch', (), None)
          self.commands['\x33\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x06', 'get_threshold', (), None)
          self.commands['\x33\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x07', 'get_trigger_src', (), None)
          self.commands['\x33\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x08', 'get_bit_depth', (), None)
          self.commands['\x33\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x09', 'get_prerec_time', (), None)
          self.commands['\x33\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x0A', 'get_dest', (), None)
          self.commands['\x33\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x10', 'get_name', (), None)
          self.commands['\x33\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x11', 'get_name_seed', (), None)
          self.commands['\x33\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x12', 'get_autorec_mode', (), None)
          self.commands['\x33\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x33\x13', 'get_autonormalize', (), None)
          self.commands['\x33\x13'] = comm

     def get_status(self):
          """Get Record Status

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x30\x01')
          return self.z48.execute(comm, ())

     def get_progress(self):
          """Get Record Progress

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x30\x02')
          return self.z48.execute(comm, ())

     def get_max_rec_time(self):
          """Get Maximum Record Time

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x30\x03')
          return self.z48.execute(comm, ())

     def arm(self):
          """Arm Recording
          """
          comm = self.commands.get('\x30\x10')
          return self.z48.execute(comm, ())

     def start(self):
          """Start Recording
          """
          comm = self.commands.get('\x30\x11')
          return self.z48.execute(comm, ())

     def stop(self):
          """Stop Recording
          """
          comm = self.commands.get('\x30\x12')
          return self.z48.execute(comm, ())

     def cancel(self):
          """Cancel Recording
          """
          comm = self.commands.get('\x30\x13')
          return self.z48.execute(comm, ())

     def start_playing(self):
          """Play Recorded Sample Start
          """
          comm = self.commands.get('\x30\x20')
          return self.z48.execute(comm, ())

     def stop_playing(self):
          """Play Recorded Sample Stop
          """
          comm = self.commands.get('\x30\x21')
          return self.z48.execute(comm, ())

     def keep(self):
          """Keep Recorded Sample. Sample with name assigned above, is added to the list of available samples.
          """
          comm = self.commands.get('\x30\x22')
          return self.z48.execute(comm, ())

     def delete(self):
          """Delete Recorded Sample
          """
          comm = self.commands.get('\x30\x23')
          return self.z48.execute(comm, ())

     def set_input(self, arg0):
          """Set Input <Data1> = (0=ANALOGUE, 1=DIGITAL, 2=MAIN OUT 3=ADAT1/2, 4=ADAT3/4, 5=ADAT5/6, 6=ADAT7/8)
          """
          comm = self.commands.get('\x32\x01')
          return self.z48.execute(comm, (arg0, ))

     def set_mode(self, arg0):
          """Set Record Mode <Data1> = (0=STEREO, 1=MONO L, 2=MONO R, 3=L/R MIX)
          """
          comm = self.commands.get('\x32\x02')
          return self.z48.execute(comm, (arg0, ))

     def enable_monitor(self, arg0):
          """Set Record Monitor
          """
          comm = self.commands.get('\x32\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_rec_time(self, arg0):
          """Set Record Time <Data1> = time in seconds. If <Data1> = 0, MANUAL mode is enabled.
          """
          comm = self.commands.get('\x32\x04')
          return self.z48.execute(comm, (arg0, ))

     def set_orig_pitch(self, arg0):
          """Set Original Pitch 
          """
          comm = self.commands.get('\x32\x05')
          return self.z48.execute(comm, (arg0, ))

     def set_threshold(self, arg0):
          """Set Threshold <Data1> = threshold in dB (-63,0)
          """
          comm = self.commands.get('\x32\x06')
          return self.z48.execute(comm, (arg0, ))

     def set_trigger_src(self, arg0):
          """Set Trigger Source (0=OFF, 1=AUDIO, 2=MIDI)
          """
          comm = self.commands.get('\x32\x07')
          return self.z48.execute(comm, (arg0, ))

     def set_bit_depth(self, arg0):
          """Set Bit Depth <Data1> = (0=16-bit, 1=24-bit)
          """
          comm = self.commands.get('\x32\x08')
          return self.z48.execute(comm, (arg0, ))

     def set_prerec_time(self, arg0):
          """Set Pre-recording Time <Data1> = time in ms
          """
          comm = self.commands.get('\x32\x09')
          return self.z48.execute(comm, (arg0, ))

     def set_dest(self, arg0):
          """Set Recording Detination <Data1> = (0=RAM, 1=DISK)
          """
          comm = self.commands.get('\x32\x0A')
          return self.z48.execute(comm, (arg0, ))

     def set_name(self, arg0):
          """Set Record Name
          """
          comm = self.commands.get('\x32\x10')
          return self.z48.execute(comm, (arg0, ))

     def set_name_seed(self, arg0):
          """Set Record Name Seed
          """
          comm = self.commands.get('\x32\x11')
          return self.z48.execute(comm, (arg0, ))

     def set_autorec_mode(self, arg0):
          """Set Auto-Record Mode <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x32\x12')
          return self.z48.execute(comm, (arg0, ))

     def set_autonormalize(self, arg0):
          """Set Auto-Normalise Mode <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x32\x13')
          return self.z48.execute(comm, (arg0, ))

     def get_input(self):
          """Get Input (0=ANALOGUE, 1=DIGITAL, 2=MAIN OUT, 3=ADAT1/2, 4=ADAT3/4, 5=ADAT5/6, 6=ADAT7/8)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x33\x01')
          return self.z48.execute(comm, ())

     def get_mode(self):
          """Get Record Mode (0=STEREO, 1=MONO L, 2=MONO R, 3=L/R MIX)
          """
          comm = self.commands.get('\x33\x02')
          return self.z48.execute(comm, ())

     def get_monitor(self):
          """Get Record Monitor <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x33\x03')
          return self.z48.execute(comm, ())

     def get_rec_time(self):
          """Get Record Time <Reply> = time in seconds.

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x33\x04')
          return self.z48.execute(comm, ())

     def get_pitch(self):
          """Get Original Pitch

          Returns:
               aksy.devices.akai.sysex.PAD BYTE
          """
          comm = self.commands.get('\x33\x05')
          return self.z48.execute(comm, ())

     def get_threshold(self):
          """Get Threshold <Reply> = threshold in dB -63,0

          Returns:
               aksy.devices.akai.sysex.SBYTE
          """
          comm = self.commands.get('\x33\x06')
          return self.z48.execute(comm, ())

     def get_trigger_src(self):
          """Get Trigger Source <Reply> = (0=OFF, 1=AUDIO, 2=MIDI)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x33\x07')
          return self.z48.execute(comm, ())

     def get_bit_depth(self):
          """Get Bit Depth <Reply> = (0=16-bit, 1=24-bit)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x33\x08')
          return self.z48.execute(comm, ())

     def get_prerec_time(self):
          """Get Pre-recording Time <Reply> = time in ms

          Returns:
               aksy.devices.akai.sysex.WORD
          """
          comm = self.commands.get('\x33\x09')
          return self.z48.execute(comm, ())

     def get_dest(self):
          """Get Recording Destination <Reply> = (0=RAM, 1=DISK)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x33\x0A')
          return self.z48.execute(comm, ())

     def get_name(self):
          """Get Record Name

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x33\x10')
          return self.z48.execute(comm, ())

     def get_name_seed(self):
          """Get Record Name Seed

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x33\x11')
          return self.z48.execute(comm, ())

     def get_autorec_mode(self):
          """Get Auto-Record Mode <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x33\x12')
          return self.z48.execute(comm, ())

     def get_autonormalize(self):
          """Get Auto-Normalise Mode <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x33\x13')
          return self.z48.execute(comm, ())

