
""" Python equivalent of akai section zonetools

Manipulate the zones of a keygroup
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.sysex

class Zonetools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          self.command_spec = aksy.sysex.CommandSpec('\x47\x5f\x00', aksy.sysex.CommandSpec.ID, aksy.sysex.CommandSpec.ARGS)
          comm = aksy.sysex.Command('\x0F\x01', 'get_sample', (aksy.sysex.BYTE,), (aksy.sysex.STRING,))
          self.commands['\x0F\x01'] = comm
          comm = aksy.sysex.Command('\x0F\x02', 'get_level', (aksy.sysex.BYTE,), (aksy.sysex.LEVEL,))
          self.commands['\x0F\x02'] = comm
          comm = aksy.sysex.Command('\x0F\x03', 'get_pan', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x0F\x03'] = comm
          comm = aksy.sysex.Command('\x0F\x04', 'get_output', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x0F\x04'] = comm
          comm = aksy.sysex.Command('\x0F\x05', 'get_filter', (aksy.sysex.Get Zone Filter (0 ­ ±100),), (aksy.sysex.SBYTE,))
          self.commands['\x0F\x05'] = comm
          comm = aksy.sysex.Command('\x0F\x06', 'get_tune', (), (aksy.sysex.SBYTE,))
          self.commands['\x0F\x06'] = comm
          comm = aksy.sysex.Command('\x0F\x07', 'get_keyboard_track', (aksy.sysex.BYTE,), (aksy.sysex.BOOL,))
          self.commands['\x0F\x07'] = comm
          comm = aksy.sysex.Command('\x0F\x08', 'get_playback', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x0F\x08'] = comm
          comm = aksy.sysex.Command('\x0F\x09', 'get_mod_start', (aksy.sysex.Get Zone ModStart(0 ­ ± 99 99), aksy.sysex.BYTE), (aksy.sysex.SWORD,))
          self.commands['\x0F\x09'] = comm
          comm = aksy.sysex.Command('\x0F\x0A', 'get_low_velocity', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x0F\x0A'] = comm
          comm = aksy.sysex.Command('\x0F\x0B', 'get_high_velocity', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x0F\x0B'] = comm
          comm = aksy.sysex.Command('\x0F\x0C', 'get_mute', (aksy.sysex.BYTE,), (aksy.sysex.BOOL,))
          self.commands['\x0F\x0C'] = comm
          comm = aksy.sysex.Command('\x0F\x0D', 'get_solo', (aksy.sysex.BYTE,), (aksy.sysex.BOOL,))
          self.commands['\x0F\x0D'] = comm
          comm = aksy.sysex.Command('\x0E\x01', 'set_sample', (aksy.sysex.BYTE, aksy.sysex.STRING), ())
          self.commands['\x0E\x01'] = comm
          comm = aksy.sysex.Command('\x0E\x02', 'set_level', (aksy.sysex.BYTE, aksy.sysex.SWORD), ())
          self.commands['\x0E\x02'] = comm
          comm = aksy.sysex.Command('\x0E\x03', 'set_pan', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x03'] = comm
          comm = aksy.sysex.Command('\x0E\x04', 'set_output', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x04'] = comm
          comm = aksy.sysex.Command('\x0E\x05', 'set_filter', (aksy.sysex.BYTE, aksy.sysex.SBYTE), ())
          self.commands['\x0E\x05'] = comm
          comm = aksy.sysex.Command('\x0E\x06', 'set_tune', (aksy.sysex.BYTE, aksy.sysex.SWORD), ())
          self.commands['\x0E\x06'] = comm
          comm = aksy.sysex.Command('\x0E\x07', 'set_keyboard_track', (aksy.sysex.BYTE, aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x07'] = comm
          comm = aksy.sysex.Command('\x0E\x08', 'set_playback', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x08'] = comm
          comm = aksy.sysex.Command('\x0E\x09', 'set_modstart', (aksy.sysex.BYTE, aksy.sysex.SWORD), ())
          self.commands['\x0E\x09'] = comm
          comm = aksy.sysex.Command('\x0E\x0A', 'set_low_vel', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x0A'] = comm
          comm = aksy.sysex.Command('\x0E\x0B', 'set_high_vel', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x0B'] = comm
          comm = aksy.sysex.Command('\x0E\x0C', 'set_mute', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x0C'] = comm
          comm = aksy.sysex.Command('\x0E\x0D', 'set_solo', (aksy.sysex.BYTE, aksy.sysex.BYTE), ())
          self.commands['\x0E\x0D'] = comm

     def get_sample(self, arg0):
          """Get Zone Sample (Data1=zone number 1-4)

          Returns:
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x0F\x01')
          return self.z48.execute(comm, (arg0, ))

     def get_level(self, arg0):
          """Get Zone Level <Reply> = level in 10×dB

          Returns:
               aksy.sysex.LEVEL
          """
          comm = self.commands.get('\x0F\x02')
          return self.z48.execute(comm, (arg0, ))

     def get_pan(self, arg0):
          """Get Zone Pan (0-100)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x0F\x03')
          return self.z48.execute(comm, (arg0, ))

     def get_output(self, arg0):
          """Get Zone Output(0-15)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x0F\x04')
          return self.z48.execute(comm, (arg0, ))

     def get_filter(self, arg0):
          """

          Returns:
               aksy.sysex.SBYTE
          """
          comm = self.commands.get('\x0F\x05')
          return self.z48.execute(comm, (arg0, ))

     def get_tune(self):
          """Get Zone Cents Tune(0 ­ ±3600)

          Returns:
               aksy.sysex.SBYTE
          """
          comm = self.commands.get('\x0F\x06')
          return self.z48.execute(comm, ())

     def get_keyboard_track(self, arg0):
          """Get Zone Keyboard Track

          Returns:
               aksy.sysex.BOOL
          """
          comm = self.commands.get('\x0F\x07')
          return self.z48.execute(comm, (arg0, ))

     def get_playback(self, arg0):
          """Get Zone Playback

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x0F\x08')
          return self.z48.execute(comm, (arg0, ))

     def get_mod_start(self, arg0, arg1):
          """

          Returns:
               aksy.sysex.SWORD
          """
          comm = self.commands.get('\x0F\x09')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_low_velocity(self, arg0):
          """Get Zone Low Velocity

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x0F\x0A')
          return self.z48.execute(comm, (arg0, ))

     def get_high_velocity(self, arg0):
          """Get Zone High Velocity

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x0F\x0B')
          return self.z48.execute(comm, (arg0, ))

     def get_mute(self, arg0):
          """Get Zone Mute

          Returns:
               aksy.sysex.BOOL
          """
          comm = self.commands.get('\x0F\x0C')
          return self.z48.execute(comm, (arg0, ))

     def get_solo(self, arg0):
          """Get Zone Solo

          Returns:
               aksy.sysex.BOOL
          """
          comm = self.commands.get('\x0F\x0D')
          return self.z48.execute(comm, (arg0, ))

     def set_sample(self, arg0, arg1):
          """Set Zone Sample <Data2...0> = name of sample to assign to zone. (0, 1­4)
          """
          comm = self.commands.get('\x0E\x01')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_level(self, arg0, arg1):
          """Set Zone Level <Data1> = Zone number, <Data2> = level in 10xdB (0, 1­4)
          """
          comm = self.commands.get('\x0E\x02')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_pan(self, arg0, arg1):
          """Set Zone Pan/Balance <Data2> = Pan/Bal where (0­100 = L50­R50);
          """
          comm = self.commands.get('\x0E\x03')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_output(self, arg0, arg1):
          """Set Zone Output <Data2> = output, where 0=MULTI, 1 = L/R; 2­5 = op1/2­op7/8; 6­15 = L, R, op1-op8
          """
          comm = self.commands.get('\x0E\x04')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_filter(self, arg0, arg1):
          """Set Zone Filter
          """
          comm = self.commands.get('\x0E\x05')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_tune(self, arg0, arg1):
          """Set Zone Cents Tune
          """
          comm = self.commands.get('\x0E\x06')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_keyboard_track(self, arg0, arg1, arg2):
          """Set Zone Keyboard Track <Data2> =  
          """
          comm = self.commands.get('\x0E\x07')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def set_playback(self, arg0, arg1):
          """Set Zone Playback <Data2> = mode, where 0=NO LOOPING, 1=ONE SHOT 2=LOOP IN REL, 3=LOOP UNTIL REL, 4=LIRRETRIG, 5=PLAYRETRIG, 6=AS SAMPLE
          """
          comm = self.commands.get('\x0E\x08')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_modstart(self, arg0, arg1):
          """Set Zone ModStart
          """
          comm = self.commands.get('\x0E\x09')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_low_vel(self, arg0, arg1):
          """Set Zone Low Velocity
          """
          comm = self.commands.get('\x0E\x0A')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_high_vel(self, arg0, arg1):
          """Set Zone High Velocity
          """
          comm = self.commands.get('\x0E\x0B')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_mute(self, arg0, arg1):
          """Set Zone Mute <Data2> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x0E\x0C')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_solo(self, arg0, arg1):
          """Set Zone Solo <Data2> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x0E\x0D')
          return self.z48.execute(comm, (arg0, arg1, ))

