
""" Python equivalent of akai section systemtools

Methods to manipulate system parameters
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.sysex

class Systemtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          self.command_spec = aksy.sysex.CommandSpec('\x47\x5f\x00', aksy.sysex.CommandSpec.ID, aksy.sysex.CommandSpec.ARGS)
          comm = aksy.sysex.Command('\x04\x00', 'get_os_software_version', (), (aksy.sysex.2BYTES,))
          self.commands['\x04\x00'] = comm
          comm = aksy.sysex.Command('\x04\x01', 'get_os_subversion', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x01'] = comm
          comm = aksy.sysex.Command('\x04\x04', 'get_sampler_model', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x04'] = comm
          comm = aksy.sysex.Command('\x04\x08', 'get_supported_filetypes', (), (aksy.sysex.STRING,))
          self.commands['\x04\x08'] = comm
          comm = aksy.sysex.Command('\x04\x10', 'get_perc_free_wave_mem', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x10'] = comm
          comm = aksy.sysex.Command('\x04\x11', 'get_perc_free_cpu_mem', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x11'] = comm
          comm = aksy.sysex.Command('\x04\x12', 'get_wave_mem_size', (), (aksy.sysex.DWORD,))
          self.commands['\x04\x12'] = comm
          comm = aksy.sysex.Command('\x04\x13', 'get_free_wave_mem_size', (), (aksy.sysex.DWORD,))
          self.commands['\x04\x13'] = comm
          comm = aksy.sysex.Command('\x04\x18', 'clear_sampler_mem', (), ())
          self.commands['\x04\x18'] = comm
          comm = aksy.sysex.Command('\x04\x19', 'purge_unused', (aksy.sysex.BYTE,), ())
          self.commands['\x04\x19'] = comm
          comm = aksy.sysex.Command('\x04\x1A', 'tag_unused', (aksy.sysex.BYTE,), ())
          self.commands['\x04\x1A'] = comm
          comm = aksy.sysex.Command('\x04\x20', 'compact_wave_mem', (), ())
          self.commands['\x04\x20'] = comm
          comm = aksy.sysex.Command('\x04\x21', 'cancel_compact_wave_mem', (), ())
          self.commands['\x04\x21'] = comm
          comm = aksy.sysex.Command('\x04\x22 ', 'get_compact_wave_mem_progress', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x22 '] = comm
          comm = aksy.sysex.Command('\x04\x30 ', 'get_async_operation_state', (), ())
          self.commands['\x04\x30 '] = comm
          comm = aksy.sysex.Command('\x04\x31 ', 'cancel_curr_async_operation', (), ())
          self.commands['\x04\x31 '] = comm
          comm = aksy.sysex.Command('\x07\x05', 'Get MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B) <Reply> = (0=OUT, 1=THRUA, 2=THRUB)', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x05'] = comm

     def get_os_software_version(self):
          """Get Operating System Software Version

          Returns:
               aksy.sysex.2BYTES
          """
          comm = self.commands.get('\x04\x00')
          return self.z48.execute(comm, ())

     def get_os_subversion(self):
          """Get the Sub-Version of the Operating System

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x01')
          return self.z48.execute(comm, ())

     def get_sampler_model(self):
          """Get Sampler Model

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x04')
          return self.z48.execute(comm, ())

     def get_supported_filetypes(self):
          """Get List of supported filetypes

          Returns:
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x04\x08')
          return self.z48.execute(comm, ())

     def get_perc_free_wave_mem(self):
          """Get the percentage free Wave memory

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x10')
          return self.z48.execute(comm, ())

     def get_perc_free_cpu_mem(self):
          """Get the percentage free CPU memory

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x11')
          return self.z48.execute(comm, ())

     def get_wave_mem_size(self):
          """Get the total number of kilobytes of Wave memory

          Returns:
               aksy.sysex.DWORD
          """
          comm = self.commands.get('\x04\x12')
          return self.z48.execute(comm, ())

     def get_free_wave_mem_size(self):
          """Get the number of kilobytes of free Wave memory

          Returns:
               aksy.sysex.DWORD
          """
          comm = self.commands.get('\x04\x13')
          return self.z48.execute(comm, ())

     def clear_sampler_mem(self):
          """Clear Sampler Memory (delete all items from memory)
          """
          comm = self.commands.get('\x04\x18')
          return self.z48.execute(comm, ())

     def purge_unused(self, arg0):
          """Purge Unused Items <Data1> = (0=SAMPLE, 1=PROGRAM)
          """
          comm = self.commands.get('\x04\x19')
          return self.z48.execute(comm, (arg0, ))

     def tag_unused(self, arg0):
          """Tag Unused Items <Data1> = (0=SAMPLE, 1=PROGRAM)
          """
          comm = self.commands.get('\x04\x1A')
          return self.z48.execute(comm, (arg0, ))

     def compact_wave_mem(self):
          """Start Compact Wave Memory
          """
          comm = self.commands.get('\x04\x20')
          return self.z48.execute(comm, ())

     def cancel_compact_wave_mem(self):
          """Cancel Compact Wave Memory
          """
          comm = self.commands.get('\x04\x21')
          return self.z48.execute(comm, ())

     def get_compact_wave_mem_progress(self):
          """Get Compact Wave Memory Progress (%)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x22 ')
          return self.z48.execute(comm, ())

     def get_async_operation_state(self):
          """Get State of Asynchronous Operation ERROR 'operation is pending' or DONE
          """
          comm = self.commands.get('\x04\x30 ')
          return self.z48.execute(comm, ())

     def cancel_curr_async_operation(self):
          """Cancel Current Asynchronous Operation
          """
          comm = self.commands.get('\x04\x31 ')
          return self.z48.execute(comm, ())

     def Get MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B) <Reply> = (0=OUT, 1=THRUA, 2=THRUB)(self):
          """BYTE

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x05')
          return self.z48.execute(comm, ())

