
""" Python equivalent of akai section multifxtools

Multi FX
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Multifxtools:
    def __init__(self, z48):
        self.sampler = z48
        self.is_fxcard_installed_cmd = Command('_', '\x24\x01', 'multifxtools', 'is_fxcard_installed', (), None)
        self.get_no_channels_cmd = Command('_', '\x24\x10', 'multifxtools', 'get_no_channels', (), None)
        self.get_max_modules_cmd = Command('_', '\x24\x11', 'multifxtools', 'get_max_modules', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_no_cmd = Command('_', '\x24\x20', 'multifxtools', 'get_no', (), None)
        self.get_name_cmd = Command('_', '\x24\x21', 'multifxtools', 'get_name', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_id_cmd = Command('_', '\x24\x22', 'multifxtools', 'get_id', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_param_index_output_ctrl_cmd = Command('_', '\x24\x24', 'multifxtools', 'get_param_index_output_ctrl', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_number_of_parameters_cmd = Command('_', '\x24\x30', 'multifxtools', 'get_number_of_parameters', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_parameter_minimum_cmd = Command('_', '\x24\x31', 'multifxtools', 'get_parameter_minimum', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_parameter_maximum_cmd = Command('_', '\x24\x32', 'multifxtools', 'get_parameter_maximum', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_parameter_name_cmd = Command('_', '\x24\x33', 'multifxtools', 'get_parameter_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_parameter_units_cmd = Command('_', '\x24\x34', 'multifxtools', 'get_parameter_units', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_parameter_type_cmd = Command('_', '\x24\x35', 'multifxtools', 'get_parameter_type', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_display_template_cmd = Command('_', '\x24\x36', 'multifxtools', 'get_display_template', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_parameter_position_id_cmd = Command('_', '\x24\x38', 'multifxtools', 'get_parameter_position_id', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_number_of_parameter_groups_cmd = Command('_', '\x24\x40', 'multifxtools', 'get_number_of_parameter_groups', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_group_name_cmd = Command('_', '\x24\x41', 'multifxtools', 'get_group_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_group_index_of_parameter_cmd = Command('_', '\x24\x42', 'multifxtools', 'get_group_index_of_parameter', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_channel_mute_cmd = Command('_', '\x26\x20', 'multifxtools', 'set_channel_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_channel_input_cmd = Command('_', '\x26\x21', 'multifxtools', 'set_channel_input', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_channel_output_cmd = Command('_', '\x26\x22', 'multifxtools', 'set_channel_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_effect_by_name_cmd = Command('_', '\x26\x30', 'multifxtools', 'set_effect_by_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
        self.set_effect_by_index_cmd = Command('_', '\x26\x31', 'multifxtools', 'set_effect_by_index', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.enable_fx_module_cmd = Command('_', '\x26\x40', 'multifxtools', 'enable_fx_module', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_parameter_value_cmd = Command('_', '\x26\x50', 'multifxtools', 'set_parameter_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SDWORD), None)
        self.map_qlink_control_cmd = Command('_', '\x26\x52', 'multifxtools', 'map_qlink_control', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.is_channel_muted_cmd = Command('_', '\x27\x20', 'multifxtools', 'is_channel_muted', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_channel_input_cmd = Command('_', '\x27\x21', 'multifxtools', 'get_channel_input', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_channel_output_cmd = Command('_', '\x27\x22', 'multifxtools', 'get_channel_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_by_name_cmd = Command('_', '\x27\x30', 'multifxtools', 'get_by_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_by_index_cmd = Command('_', '\x27\x31', 'multifxtools', 'get_by_index', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.is_module_enabled_cmd = Command('_', '\x27\x40', 'multifxtools', 'is_module_enabled', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_param_value_cmd = Command('_', '\x27\x50', 'multifxtools', 'get_param_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_param_string_cmd = Command('_', '\x27\x51', 'multifxtools', 'get_param_string', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_param_qlinkctrl_cmd = Command('_', '\x27\x52', 'multifxtools', 'get_param_qlinkctrl', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_channel_mute_cmd = Command('_', '\x26\x20', 'multifxtools', 'set_channel_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_channel_input_cmd = Command('_', '\x26\x21', 'multifxtools', 'set_channel_input', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_channel_output_cmd = Command('_', '\x26\x22', 'multifxtools', 'set_channel_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_fx_by_name_cmd = Command('_', '\x26\x30', 'multifxtools', 'set_fx_by_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
        self.set_fx_by_id_cmd = Command('_', '\x26\x31', 'multifxtools', 'set_fx_by_id', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.enable_module_cmd = Command('_', '\x26\x40', 'multifxtools', 'enable_module', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_param_value_cmd = Command('_', '\x26\x50', 'multifxtools', 'set_param_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_param_qlinkctrl_cmd = Command('_', '\x26\x52', 'multifxtools', 'set_param_qlinkctrl', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)

    def is_fxcard_installed(self):
        """Get FX card installed

        Returns:
            BYTE
        """
        return self.sampler.execute(self.is_fxcard_installed_cmd, ())

    def get_no_channels(self):
        """Get Number of FX channels

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_channels_cmd, ())

    def get_max_modules(self, arg0):
        """Get Maximum Number of FX modules on given channel <Data1=channel>

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_max_modules_cmd, (arg0, ))

    def get_no(self):
        """Get Number of effects available

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_cmd, ())

    def get_name(self, arg0):
        """Get effect name <Data1> = index of effect

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_name_cmd, (arg0, ))

    def get_id(self, arg0):
        """Get Unique ID of effect <Data1> = index of effect

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_id_cmd, (arg0, ))

    def get_param_index_output_ctrl(self, arg0):
        """Get Parameter Index for Output Control <Data1> = index of effect

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_param_index_output_ctrl_cmd, (arg0, ))

    def get_number_of_parameters(self, arg0, arg1):
        """Get Number of Parameters (channel, module)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_number_of_parameters_cmd, (arg0, arg1, ))

    def get_parameter_minimum(self, arg0, arg1, arg2):
        """Get Parameter Minimum (channel, module, param)

        Returns:
            SDWORD
        """
        return self.sampler.execute(self.get_parameter_minimum_cmd, (arg0, arg1, arg2, ))

    def get_parameter_maximum(self, arg0, arg1, arg2):
        """Get Parameter Maximum (channel, module, param)

        Returns:
            SDWORD
        """
        return self.sampler.execute(self.get_parameter_maximum_cmd, (arg0, arg1, arg2, ))

    def get_parameter_name(self, arg0, arg1, arg2):
        """Get Parameter Name (channel, module, param)

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_parameter_name_cmd, (arg0, arg1, arg2, ))

    def get_parameter_units(self, arg0, arg1, arg2):
        """Get Parameter Units (channel, module, param)

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_parameter_units_cmd, (arg0, arg1, arg2, ))

    def get_parameter_type(self, arg0, arg1, arg2):
        """Get Parameter TYPE (channel, module, param)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_parameter_type_cmd, (arg0, arg1, arg2, ))

    def get_display_template(self, arg0, arg1, arg2):
        """Get Parameter Template (channel, module, param)

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_display_template_cmd, (arg0, arg1, arg2, ))

    def get_parameter_position_id(self, arg0, arg1, arg2):
        """Get Parameter Position ID (channel, module, param)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_parameter_position_id_cmd, (arg0, arg1, arg2, ))

    def get_number_of_parameter_groups(self, arg0, arg1):
        """Get Number of Parameter Groups (channel, module)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_number_of_parameter_groups_cmd, (arg0, arg1, ))

    def get_group_name(self, arg0, arg1, arg2):
        """Get Parameter Group name (channel, module, group index)

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_group_name_cmd, (arg0, arg1, arg2, ))

    def get_group_index_of_parameter(self, arg0, arg1, arg2):
        """Get Parameter Group Index (channel, module, param)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_group_index_of_parameter_cmd, (arg0, arg1, arg2, ))

    def set_channel_mute(self, arg0, arg1):
        """Set Mute (channel, mute status)
        """
        return self.sampler.execute(self.set_channel_mute_cmd, (arg0, arg1, ))

    def set_channel_input(self, arg0, arg1):
        """Set Channel Input (channel, input)
        """
        return self.sampler.execute(self.set_channel_input_cmd, (arg0, arg1, ))

    def set_channel_output(self, arg0, arg1):
        """Set Channel Output (channel, output)
        """
        return self.sampler.execute(self.set_channel_output_cmd, (arg0, arg1, ))

    def set_effect_by_name(self, arg0, arg1, arg2):
        """Set Effect on specified Channel (channel, module, effect)
        """
        return self.sampler.execute(self.set_effect_by_name_cmd, (arg0, arg1, arg2, ))

    def set_effect_by_index(self, arg0, arg1, arg2):
        """Set Effect on specified Channel (channel, module, effect)
        """
        return self.sampler.execute(self.set_effect_by_index_cmd, (arg0, arg1, arg2, ))

    def enable_fx_module(self, arg0, arg1, arg2):
        """Enable FX Module (channel, module, enabled)
        """
        return self.sampler.execute(self.enable_fx_module_cmd, (arg0, arg1, arg2, ))

    def set_parameter_value(self, arg0, arg1, arg2, arg3):
        """Set Parameter value (channel, module, param index, value)
        """
        return self.sampler.execute(self.set_parameter_value_cmd, (arg0, arg1, arg2, arg3, ))

    def map_qlink_control(self, arg0, arg1, arg2, arg3):
        """Maps QLink control to a Parameter (channel, module, param index, qlink no)
        """
        return self.sampler.execute(self.map_qlink_control_cmd, (arg0, arg1, arg2, arg3, ))

    def is_channel_muted(self, arg0):
        """Get Mute Status of Channel <Reply> = (0=ON, 1=MUTE)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.is_channel_muted_cmd, (arg0, ))

    def get_channel_input(self, arg0):
        """Get Channel Input <Reply> = input

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_channel_input_cmd, (arg0, ))

    def get_channel_output(self, arg0):
        """Get Channel Output <Reply> = output

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_channel_output_cmd, (arg0, ))

    def get_by_name(self, arg0, arg1):
        """Get effect in module on given channel (by name) <Data1> = channel; <Data2> = module; <Reply> = effect

        Returns:
            BYTE
            STRING
        """
        return self.sampler.execute(self.get_by_name_cmd, (arg0, arg1, ))

    def get_by_index(self, arg0, arg1):
        """Get effect in module on given channel (by index)<Data1> = channel; <Data2> = module; <Reply> = effect

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_by_index_cmd, (arg0, arg1, ))

    def is_module_enabled(self, arg0, arg1):
        """Get Enabled/Disabled State of FX module <Data1> = channel; <Data2> = module; (0=disabled, 1=enabled)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.is_module_enabled_cmd, (arg0, arg1, ))

    def get_param_value(self, arg0, arg1, arg2):
        """Get parameter value of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter

        Returns:
            SDWORD
        """
        return self.sampler.execute(self.get_param_value_cmd, (arg0, arg1, arg2, ))

    def get_param_string(self, arg0, arg1, arg2):
        """Get parameter string of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_param_string_cmd, (arg0, arg1, arg2, ))

    def get_param_qlinkctrl(self, arg0, arg1, arg2):
        """Get Qlink control used to control the parameter <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Reply> = Qlink control (0=NONE, 1-n = Qlink 1-n)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_param_qlinkctrl_cmd, (arg0, arg1, arg2, ))

    def set_channel_mute(self, arg0, arg1):
        """Set Mute Status of Channel <Data2> = (0=ON, 1=MUTE)
        """
        return self.sampler.execute(self.set_channel_mute_cmd, (arg0, arg1, ))

    def set_channel_input(self, arg0, arg1):
        """Set Channel Input <Data2> = input
        """
        return self.sampler.execute(self.set_channel_input_cmd, (arg0, arg1, ))

    def set_channel_output(self, arg0, arg1):
        """Set Channel Output <Data2> = output
        """
        return self.sampler.execute(self.set_channel_output_cmd, (arg0, arg1, ))

    def set_fx_by_name(self, arg0, arg1, arg2):
        """Set effect in module on given channel (by name) <Data1> = channel; <Data2> = module; <Data3> = effect.
        """
        return self.sampler.execute(self.set_fx_by_name_cmd, (arg0, arg1, arg2, ))

    def set_fx_by_id(self, arg0, arg1, arg2):
        """Set effect in module on given channel (by index)<Data1> = channel; <Data2> = module; <Data3> = effect
        """
        return self.sampler.execute(self.set_fx_by_id_cmd, (arg0, arg1, arg2, ))

    def enable_module(self, arg0, arg1, arg2):
        """Set State of FX module. (channel, module, enable
        """
        return self.sampler.execute(self.enable_module_cmd, (arg0, arg1, arg2, ))

    def set_param_value(self, arg0, arg1, arg2, arg3):
        """Set parameter value of given module in given channel. <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Data4> = parameter value
        """
        return self.sampler.execute(self.set_param_value_cmd, (arg0, arg1, arg2, arg3, ))

    def set_param_qlinkctrl(self, arg0, arg1, arg2, arg3):
        """Set Qlink control used to control the parameter <Data1> = channel; <Data2> = module; <Data3> = index of parameter to set <Data4> = Qlink control (0=NONE, 1-n = Qlink 1-n)
        """
        return self.sampler.execute(self.set_param_qlinkctrl_cmd, (arg0, arg1, arg2, arg3, ))

