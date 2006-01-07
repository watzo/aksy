
""" Python equivalent of akai section multifxtools

Multi FX
"""

__author__ =  'Walco van Loon'
__version__=  '$Rev$'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Multifxtools:
    def __init__(self, z48):
        self.z48 = z48
        self.is_fxcard_installed_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x01', 'is_fxcard_installed', (), None)
        self.get_no_channels_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x10', 'get_no_channels', (), None)
        self.get_max_modules_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x11', 'get_max_modules', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_no_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x20', 'get_no', (), None)
        self.get_name_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x21', 'get_name', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_id_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x22', 'get_id', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_param_index_output_ctrl_cmd = aksy.devices.akai.sysex.Command('_', '\x24\x24', 'get_param_index_output_ctrl', (aksy.devices.akai.sysex_types.WORD,), None)
        self.is_channel_muted_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x20', 'is_channel_muted', (), None)
        self.get_channel_input_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x21', 'get_channel_input', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_channel_output_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x22', 'get_channel_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_by_name_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x30', 'get_by_name', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_by_index_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x31', 'get_by_index', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.is_module_enabled_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x40', 'is_module_enabled', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_param_value_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x50', 'get_param_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_param_string_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x51', 'get_param_string', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_param_qlinkctrl_cmd = aksy.devices.akai.sysex.Command('_', '\x27\x52', 'get_param_qlinkctrl', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_channel_mute_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x20', 'set_channel_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_channel_input_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x21', 'set_channel_input', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_channel_output_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x22', 'set_channel_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_fx_by_id_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x30', 'set_fx_by_id', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
        self.set_fx_by_name_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x31', 'set_fx_by_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.enable_module_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x40', 'enable_module', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_param_value_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x50', 'set_param_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_param_qlinkctrl_cmd = aksy.devices.akai.sysex.Command('_', '\x26\x52', 'set_param_qlinkctrl', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)

    def is_fxcard_installed(self):
        """Get FX card installed

        Returns:
            BYTE
        """
        return self.z48.execute(self.is_fxcard_installed_cmd, ())

    def get_no_channels(self):
        """Get Number of FX channels

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_no_channels_cmd, ())

    def get_max_modules(self, arg0):
        """Get Maximum Number of FX modules on given channel <Data1=channel>

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_max_modules_cmd, (arg0, ))

    def get_no(self):
        """Get Number of effects available

        Returns:
            WORD
        """
        return self.z48.execute(self.get_no_cmd, ())

    def get_name(self, arg0):
        """Get effect name <Data1> = index of effect

        Returns:
            STRING
        """
        return self.z48.execute(self.get_name_cmd, (arg0, ))

    def get_id(self, arg0):
        """Get Unique ID of effect <Data1> = index of effect

        Returns:
            DWORD
        """
        return self.z48.execute(self.get_id_cmd, (arg0, ))

    def get_param_index_output_ctrl(self, arg0):
        """Get Parameter Index for Output Control <Data1> = index of effect

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_param_index_output_ctrl_cmd, (arg0, ))

    def is_channel_muted(self):
        """Get Mute Status of Channel <Reply> = (0=ON, 1=MUTE) BYTE

        Returns:
            BOOL
        """
        return self.z48.execute(self.is_channel_muted_cmd, ())

    def get_channel_input(self, arg0):
        """Get Channel Input <Reply> = input

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_channel_input_cmd, (arg0, ))

    def get_channel_output(self, arg0):
        """Get Channel Output <Reply> = output

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_channel_output_cmd, (arg0, ))

    def get_by_name(self, arg0):
        """Get effect in module on given channel (by name) <Data1> = channel; <Data2> = module; <Reply> = effect

        Returns:
            BYTE
            STRING
        """
        return self.z48.execute(self.get_by_name_cmd, (arg0, ))

    def get_by_index(self, arg0, arg1):
        """Get effect in module on given channel (by index)<Data1> = channel; <Data2> = module; <Reply> = effect

        Returns:
            WORD
        """
        return self.z48.execute(self.get_by_index_cmd, (arg0, arg1, ))

    def is_module_enabled(self, arg0, arg1):
        """Get Enabled/Disabled State of FX module <Data1> = channel; <Data2> = module; (0=disabled, 1=enabled)

        Returns:
            BYTE
        """
        return self.z48.execute(self.is_module_enabled_cmd, (arg0, arg1, ))

    def get_param_value(self, arg0, arg1):
        """Get parameter value of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter

        Returns:
            SDWORD
        """
        return self.z48.execute(self.get_param_value_cmd, (arg0, arg1, ))

    def get_param_string(self, arg0, arg1, arg2):
        """Get parameter string of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter

        Returns:
            STRING
        """
        return self.z48.execute(self.get_param_string_cmd, (arg0, arg1, arg2, ))

    def get_param_qlinkctrl(self, arg0, arg1, arg2):
        """Get Qlink control used to control the parameter <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Reply> = Qlink control (0=NONE, 1要 = Qlink 1要)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_param_qlinkctrl_cmd, (arg0, arg1, arg2, ))

    def set_channel_mute(self, arg0, arg1):
        """Set Mute Status of Channel <Data2> = (0=ON, 1=MUTE)
        """
        return self.z48.execute(self.set_channel_mute_cmd, (arg0, arg1, ))

    def set_channel_input(self, arg0, arg1):
        """Set Channel Input <Data2> = input
        """
        return self.z48.execute(self.set_channel_input_cmd, (arg0, arg1, ))

    def set_channel_output(self, arg0, arg1):
        """Set Channel Output <Data2> = output
        """
        return self.z48.execute(self.set_channel_output_cmd, (arg0, arg1, ))

    def set_fx_by_id(self, arg0, arg1, arg2):
        """Set effect in module on given channel (by name) <Data1> = channel; <Data2> = module; <Data3> = effect.
        """
        return self.z48.execute(self.set_fx_by_id_cmd, (arg0, arg1, arg2, ))

    def set_fx_by_name(self, arg0, arg1, arg2):
        """Set effect in module on given channel (by index)<Data1> = channel; <Data2> = module; <Data3> = effect
        """
        return self.z48.execute(self.set_fx_by_name_cmd, (arg0, arg1, arg2, ))

    def enable_module(self, arg0, arg1, arg2):
        """Set State of FX module. (channel, module, enable) 
        """
        return self.z48.execute(self.enable_module_cmd, (arg0, arg1, arg2, ))

    def set_param_value(self, arg0, arg1, arg2, arg3):
        """Set parameter value of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Data4> = parameter value
        """
        return self.z48.execute(self.set_param_value_cmd, (arg0, arg1, arg2, arg3, ))

    def set_param_qlinkctrl(self, arg0, arg1, arg2, arg3):
        """Set Qlink control used to control the parameter <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Data4> = Qlink control (0=NONE, 1要 = Qlink 1要)
        """
        return self.z48.execute(self.set_param_qlinkctrl_cmd, (arg0, arg1, arg2, arg3, ))

