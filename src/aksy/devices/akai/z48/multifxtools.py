
""" Python equivalent of akai section multifxtools

Multi FX
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Multifxtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x01', 'is_fxcard_installed', (), None)
          self.commands['\x24\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x10', 'get_no_channels', (), None)
          self.commands['\x24\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x11', 'get_max_modules', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x24\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x20', 'get_no', (), None)
          self.commands['\x24\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x21', 'get_name', (aksy.devices.akai.sysex_types.WORD,), None)
          self.commands['\x24\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x22', 'get_id', (aksy.devices.akai.sysex_types.WORD,), None)
          self.commands['\x24\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x24\x24', 'get_param_index_output_ctrl', (aksy.devices.akai.sysex_types.WORD,), None)
          self.commands['\x24\x24'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x20', 'is_channel_muted', (), None)
          self.commands['\x27\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x21', 'get_channel_input', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x27\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x22', 'get_channel_output', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x27\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x30', 'get_by_name', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x27\x30'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x31', 'get_by_index', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x27\x31'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x40', 'is_module_enabled', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x27\x40'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x50', 'get_param_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x27\x50'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x51', 'get_param_string', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x27\x51'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x27\x52', 'get_param_qlinkctrl', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x27\x52'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x20', 'set_channel_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x26\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x21', 'set_channel_input', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x26\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x22', 'set_channel_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x26\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x30', 'set_fx_by_id', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
          self.commands['\x26\x30'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x31', 'set_fx_by_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
          self.commands['\x26\x31'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x40', 'enable_module', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTES, aksy.devices.akai.sysex_types.DWORD), None)
          self.commands['\x26\x40'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x50', 'set_param_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x26\x50'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x26\x52', 'set_param_qlinkctrl', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x26\x52'] = comm

     def is_fxcard_installed(self):
          """Get FX card installed

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x24\x01')
          return self.z48.execute(comm, ())

     def get_no_channels(self):
          """Get Number of FX channels

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x24\x10')
          return self.z48.execute(comm, ())

     def get_max_modules(self, arg0):
          """Get Maximum Number of FX modules on given channel <Data1=channel>

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x24\x11')
          return self.z48.execute(comm, (arg0, ))

     def get_no(self):
          """Get Number of effects available

          Returns:
               aksy.devices.akai.sysex_types.WORD
          """
          comm = self.commands.get('\x24\x20')
          return self.z48.execute(comm, ())

     def get_name(self, arg0):
          """Get effect name <Data1> = index of effect

          Returns:
               aksy.devices.akai.sysex_types.STRING
          """
          comm = self.commands.get('\x24\x21')
          return self.z48.execute(comm, (arg0, ))

     def get_id(self, arg0):
          """Get Unique ID of effect <Data1> = index of effect

          Returns:
               aksy.devices.akai.sysex_types.DWORD
          """
          comm = self.commands.get('\x24\x22')
          return self.z48.execute(comm, (arg0, ))

     def get_param_index_output_ctrl(self, arg0):
          """Get Parameter Index for Output Control <Data1> = index of effect

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x24\x24')
          return self.z48.execute(comm, (arg0, ))

     def is_channel_muted(self):
          """Get Mute Status of Channel <Reply> = (0=ON, 1=MUTE) BYTE

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x27\x20')
          return self.z48.execute(comm, ())

     def get_channel_input(self, arg0):
          """Get Channel Input <Reply> = input

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x27\x21')
          return self.z48.execute(comm, (arg0, ))

     def get_channel_output(self, arg0):
          """Get Channel Output <Reply> = output

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x27\x22')
          return self.z48.execute(comm, (arg0, ))

     def get_by_name(self, arg0):
          """Get effect in module on given channel (by name) <Data1> = channel; <Data2> = module; <Reply> = effect

          Returns:
               aksy.devices.akai.sysex_types.BYTE
               aksy.devices.akai.sysex_types.STRING
          """
          comm = self.commands.get('\x27\x30')
          return self.z48.execute(comm, (arg0, ))

     def get_by_index(self, arg0, arg1):
          """Get effect in module on given channel (by index)<Data1> = channel; <Data2> = module; <Reply> = effect

          Returns:
               aksy.devices.akai.sysex_types.WORD
          """
          comm = self.commands.get('\x27\x31')
          return self.z48.execute(comm, (arg0, arg1, ))

     def is_module_enabled(self, arg0, arg1):
          """Get Enabled/Disabled State of FX module <Data1> = channel; <Data2> = module; (0=disabled, 1=enabled)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x27\x40')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_param_value(self, arg0, arg1):
          """Get parameter value of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter

          Returns:
               aksy.devices.akai.sysex_types.SDWORD
          """
          comm = self.commands.get('\x27\x50')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_param_string(self, arg0, arg1, arg2):
          """Get parameter string of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter

          Returns:
               aksy.devices.akai.sysex_types.STRING
          """
          comm = self.commands.get('\x27\x51')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def get_param_qlinkctrl(self, arg0, arg1, arg2):
          """Get Qlink control used to control the parameter <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Reply> = Qlink control (0=NONE, 1要 = Qlink 1要)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x27\x52')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def set_channel_mute(self, arg0, arg1):
          """Set Mute Status of Channel <Data2> = (0=ON, 1=MUTE)
          """
          comm = self.commands.get('\x26\x20')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_channel_input(self, arg0, arg1):
          """Set Channel Input <Data2> = input
          """
          comm = self.commands.get('\x26\x21')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_channel_output(self, arg0, arg1):
          """Set Channel Output <Data2> = output
          """
          comm = self.commands.get('\x26\x22')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_fx_by_id(self, arg0, arg1, arg2):
          """Set effect in module on given channel (by name) <Data1> = channel; <Data2> = module; <Data3> = effect.
          """
          comm = self.commands.get('\x26\x30')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def set_fx_by_name(self, arg0, arg1, arg2):
          """Set effect in module on given channel (by index)<Data1> = channel; <Data2> = module; <Data3> = effect
          """
          comm = self.commands.get('\x26\x31')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def enable_module(self, arg0, arg1, arg2):
          """Set Enabled/Disabled State of FX module. <Data1> = channel; <Data2> = module; <Data3> =0 (disable) or 1 (enable) parameter values
          """
          comm = self.commands.get('\x26\x40')
          return self.z48.execute(comm, (arg0, arg1, arg2, ))

     def set_param_value(self, arg0, arg1, arg2, arg3):
          """Set parameter value of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Data4> = parameter value
          """
          comm = self.commands.get('\x26\x50')
          return self.z48.execute(comm, (arg0, arg1, arg2, arg3, ))

     def set_param_qlinkctrl(self, arg0, arg1, arg2, arg3):
          """Set Qlink control used to control the parameter <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Data4> = Qlink control (0=NONE, 1要 = Qlink 1要)
          """
          comm = self.commands.get('\x26\x52')
          return self.z48.execute(comm, (arg0, arg1, arg2, arg3, ))

