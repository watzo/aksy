
""" Python equivalent of akai section programtools

Methods to manipulate in-memory programs
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Programtools:
    def __init__(self, s56k):
        self.sampler = s56k
        self.create_empty_cmd = Command('^', '\x0a\x02', 'programtools', 'create_empty', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.create_new_cmd = Command('^', '\x0a\x03', 'programtools', 'create_new', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_name_cmd = Command('^', '\x0a\x05', 'programtools', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_handle_cmd = Command('^', '\x0a\x06', 'programtools', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.WORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_all_cmd = Command('^', '\x0a\x07', 'programtools', 'delete_all', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_curr_cmd = Command('^', '\x0a\x08', 'programtools', 'delete_curr', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.rename_curr_cmd = Command('^', '\x0a\x09', 'programtools', 'rename_curr', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_program_no_cmd = Command('^', '\x0a\x0A', 'programtools', 'set_program_no', (aksy.devices.akai.sysex_types.BOOL,aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.add_keygroups_cmd = Command('^', '\x0a\x0B', 'programtools', 'add_keygroups', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_keygroup_cmd = Command('^', '\x0a\x0C', 'programtools', 'delete_keygroup', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_keygroup_xfade_cmd = Command('^', '\x0a\x0D', 'programtools', 'set_keygroup_xfade', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_items_cmd = Command('^', '\x0a\x10', 'programtools', 'get_no_items', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_program_no_cmd = Command('^', '\x0a\x11', 'programtools', 'get_program_no', (), (aksy.devices.akai.sysex_types.BOOL,aksy.devices.akai.sysex_types.BYTE), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_index_cmd = Command('^', '\x0a\x12', 'programtools', 'get_index', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_name_cmd = Command('^', '\x0a\x13', 'programtools', 'get_name', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_keygroups_cmd = Command('^', '\x0a\x14', 'programtools', 'get_no_keygroups', (), (aksy.devices.akai.sysex_types.BYTE), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_keygroup_xfade_cmd = Command('^', '\x0a\x15', 'programtools', 'get_keygroup_xfade', (), (aksy.devices.akai.sysex_types.BOOL), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_program_numbers_cmd = Command('^', '\x0a\x18', 'programtools', 'get_program_numbers', (), (aksy.devices.akai.sysex_types.BOOL,aksy.devices.akai.sysex_types.BYTE), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_names_cmd = Command('^', '\x0a\x19', 'programtools', 'get_names', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        
        self.set_loudness_cmd = Command('^', '\x0a\x20', 'programtools', 'set_loudness', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_velocity_sens_cmd = Command('^', '\x0a\x21', 'programtools', 'set_velocity_sens', (aksy.devices.akai.sysex_types.SBYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_amp_modulation_source_cmd = Command('^', '\x0a\x22', 'programtools', 'set_amp_modulation_source', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_amp_modulation_value_cmd = Command('^', '\x0a\x23', 'programtools', 'set_amp_modulation_value', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_pan_modulation_source_cmd = Command('^', '\x0a\x24', 'programtools', 'set_pan_modulation_source', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_pan_modulation_value_cmd = Command('^', '\x0a\x25', 'programtools', 'set_pan_modulation_value', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_loudness_cmd = Command('^', '\x0a\x28', 'programtools', 'get_loudness', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_velocity_sens_cmd = Command('^', '\x0a\x29', 'programtools', 'get_velocity_sens', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_amp_modulation_source_cmd = Command('^', '\x0a\x2A', 'programtools', 'get_amp_modulation_source', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_amp_modulation_value_cmd = Command('^', '\x0a\x2B', 'programtools', 'get_amp_modulation_value', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_pan_modulation_source_cmd = Command('^', '\x0a\x2C', 'programtools', 'get_pan_modulation_source', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_pan_modulation_value_cmd = Command('^', '\x0a\x2D', 'programtools', 'get_pan_modulation_value', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_semitone_tune_cmd = Command('^', '\x0a\x30', 'programtools', 'set_semitone_tune', (aksy.devices.akai.sysex_types.SBYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_fine_tune_cmd = Command('^', '\x0a\x31', 'programtools', 'set_fine_tune', (aksy.devices.akai.sysex_types.SBYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_tune_template_cmd = Command('^', '\x0a\x32', 'programtools', 'set_tune_template', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_user_tune_template_cmd = Command('^', '\x0a\x33', 'programtools', 'set_user_tune_template', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_key_cmd = Command('^', '\x0a\x34', 'programtools', 'set_key', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_semitone_tune_cmd = Command('^', '\x0a\x38', 'programtools', 'get_semitone_tune', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_fine_tune_cmd = Command('^', '\x0a\x39', 'programtools', 'get_fine_tune', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_tune_template_cmd = Command('^', '\x0a\x3A', 'programtools', 'get_tune_template', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_user_tune_template_cmd = Command('^', '\x0a\x3B', 'programtools', 'get_user_tune_template', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_key_cmd = Command('^', '\x0a\x3C', 'programtools', 'get_key', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_pitch_bend_up_cmd = Command('^', '\x0a\x40', 'programtools', 'set_pitch_bend_up', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_pitch_bend_down_cmd = Command('^', '\x0a\x41', 'programtools', 'set_pitch_bend_down', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_bend_mode_cmd = Command('^', '\x0a\x42', 'programtools', 'set_bend_mode', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_aftertouch_value_cmd = Command('^', '\x0a\x43', 'programtools', 'set_aftertouch_value', (aksy.devices.akai.sysex_types.SBYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_legato_setting_cmd = Command('^', '\x0a\x44', 'programtools', 'set_legato_setting', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_portamento_enabled_cmd = Command('^', '\x0a\x45', 'programtools', 'set_portamento_enabled', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_portamento_mode_cmd = Command('^', '\x0a\x46', 'programtools', 'set_portamento_mode', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_portamento_time_cmd = Command('^', '\x0a\x47', 'programtools', 'set_portamento_time', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_pitch_bend_up_cmd = Command('^', '\x0a\x48', 'programtools', 'get_pitch_bend_up', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_pitch_bend_down_cmd = Command('^', '\x0a\x49', 'programtools', 'get_pitch_bend_down', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_bend_mode_cmd = Command('^', '\x0a\x4A', 'programtools', 'get_bend_mode', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_aftertouch_value_cmd = Command('^', '\x0a\x4B', 'programtools', 'get_aftertouch_value', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_legato_setting_cmd = Command('^', '\x0a\x4C', 'programtools', 'get_legato_setting', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_portamento_enabled_cmd = Command('^', '\x0a\x4D', 'programtools', 'get_portamento_enabled', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_portamento_mode_cmd = Command('^', '\x0a\x4E', 'programtools', 'get_portamento_mode', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_portamento_time_cmd = Command('^', '\x0a\x4F', 'programtools', 'get_portamento_time', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_lfo_rate_cmd = Command('^', '\x0a\x50', 'programtools', 'set_lfo_rate', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_lfo_delay_cmd = Command('^', '\x0a\x51', 'programtools', 'set_lfo_delay', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_lfo_depth_cmd = Command('^', '\x0a\x52', 'programtools', 'set_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_lfo_waveform_cmd = Command('^', '\x0a\x53', 'programtools', 'set_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_lfo_sync_cmd = Command('^', '\x0a\x54', 'programtools', 'set_lfo_sync', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_lfo_retrigger_cmd = Command('^', '\x0a\x55', 'programtools', 'set_lfo_retrigger', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_rate_modulation_source_cmd = Command('^', '\x0a\x56', 'programtools', 'set_rate_modulation_source', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_lfo_sync_cmd = Command('^', '\x0a\x64', 'programtools', 'get_lfo_sync', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_lfo_retrigger_cmd = Command('^', '\x0a\x65', 'programtools', 'get_lfo_retrigger', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_rate_modulation_source_cmd = Command('^', '\x0a\x66', 'programtools', 'get_rate_modulation_source', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_rate_modulation_value_cmd = Command('^', '\x0a\x67', 'programtools', 'get_rate_modulation_value', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_delay_modulation_source_cmd = Command('^', '\x0a\x68', 'programtools', 'get_delay_modulation_source', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_delay_modulation_value_cmd = Command('^', '\x0a\x69', 'programtools', 'get_delay_modulation_value', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_depth_modulation_source_cmd = Command('^', '\x0a\x6A', 'programtools', 'get_depth_modulation_source', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_depth_modulation_value_cmd = Command('^', '\x0a\x6B', 'programtools', 'get_depth_modulation_value', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_modwheel_cmd = Command('^', '\x0a\x6C', 'programtools', 'get_modwheel', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_aftertouch_cmd = Command('^', '\x0a\x6D', 'programtools', 'get_aftertouch', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_midi_clock_sync_enabled_cmd = Command('^', '\x0a\x6E', 'programtools', 'get_midi_clock_sync_enabled', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_midi_clock_sync_division_cmd = Command('^', '\x0a\x6F', 'programtools', 'get_midi_clock_sync_division', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_pitch_modulation_source_cmd = Command('^', '\x0a\x70', 'programtools', 'set_pitch_modulation_source', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_filter_modulation_source_cmd = Command('^', '\x0a\x72', 'programtools', 'set_filter_modulation_source', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_pitch_modulation_source_cmd = Command('^', '\x0a\x74', 'programtools', 'get_pitch_modulation_source', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_filter_modulation_source_cmd = Command('^', '\x0a\x76', 'programtools', 'get_filter_modulation_source', (aksy.devices.akai.sysex_types.BYTE,), (), aksy.devices.akai.sysex_types.S56K_USERREF)

    def create_empty(self, arg0):
        """Create Program: <Data1> = Name
        """
        return self.sampler.execute(self.create_empty_cmd, (arg0, ))

    def create_new(self, arg0, arg1):
        """Create Program with keygroups. <Data1> = Name
        """
        return self.sampler.execute(self.create_new_cmd, (arg0, arg1, ))

    def set_curr_by_name(self, arg0):
        """Select Program (by name) to be current: <Data1> = Name
        """
        return self.sampler.execute(self.set_curr_by_name_cmd, (arg0, ))

    def set_curr_by_handle(self, arg0):
        """Select Program (by index) to be current: <Data1> = handle.
        """
        return self.sampler.execute(self.set_curr_by_handle_cmd, (arg0, ))

    def delete_all(self):
        """Delete ALL programs from memory
        """
        return self.sampler.execute(self.delete_all_cmd, ())

    def delete_curr(self):
        """Delete the currently selected Program from memory
        """
        return self.sampler.execute(self.delete_curr_cmd, ())

    def rename_curr(self, arg0):
        """Rename currently selected Program: <Data1> = Name
        """
        return self.sampler.execute(self.rename_curr_cmd, (arg0, ))

    def set_program_no(self, arg0, arg1=0):  # arg1 is optional if arg=0?
        """Set Program Number. <Data1>=1).
        """
        return self.sampler.execute(self.set_program_no_cmd, (arg0, arg1))

    def add_keygroups(self, arg0):
        """Add Keygroups to Program <Data1> = Number of Keygroups to add.
        """
        return self.sampler.execute(self.add_keygroups_cmd, (arg0, ))

    def delete_keygroup(self, arg0):
        """Delete Keygroup from Program: <Data1> = Number of the keygroup to delete. (zero-based)
        """
        return self.sampler.execute(self.delete_keygroup_cmd, (arg0, ))

    def set_keygroup_xfade(self, arg0, arg1):
        """Set Keygroup Crossfade <Data1>: 0=OFF; 1=ON
        """
        return self.sampler.execute(self.set_keygroup_xfade_cmd, (arg0, arg1, ))

    def get_no_items(self):
        """Get Number of Programs in memory

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_program_no(self):
        """Get Current Programs Program Number

        Returns:
            BOOL
            BYTE
        """
        return self.sampler.execute(self.get_program_no_cmd, ())

    def get_index(self):
        """Get Current Program Index (i.e., its position in memory)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_index_cmd, ())

    def get_name(self):
        """Get Current Program Name

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_name_cmd, ())

    def get_no_keygroups(self):
        """Get Number of Keygroups in Current Program

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_keygroups_cmd, ())

    def get_keygroup_xfade(self):
        """Get Keygroup Crossfade

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_keygroup_xfade_cmd, ())

    def get_program_numbers(self):
        """Get the Program Numbers of all the Programs in memory

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_program_numbers_cmd, ())

    def get_names(self):
        """Get the names of all of the Programs in memory

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_names_cmd, ())

    def set_loudness(self, arg0):
        """Set Loudness. <Data1> = loudness value.
        """
        return self.sampler.execute(self.set_loudness_cmd, (arg0, ))

    def set_velocity_sens(self, arg0):
        """Set Velocity Sensitivity. Values range from 100 to +100, <Data1> = absolute value.
        """
        return self.sampler.execute(self.set_velocity_sens_cmd, (arg0, ))

    def set_amp_modulation_source(self, arg0):
        """Set Amp Mod Source. <Data1> = Modulation Source. (see Table 15)
        """
        return self.sampler.execute(self.set_amp_modulation_source_cmd, (arg0, ))

    def set_amp_modulation_value(self, arg0, arg1):
        """Set Amp Mod Value. <Data1> = Amp Mod (1 or 2)
        """
        return self.sampler.execute(self.set_amp_modulation_value_cmd, (arg0, arg1, ))

    def set_pan_modulation_source(self, arg0, arg1):
        """Set Pan Mod Source. <Data1> = Modulation Source. (see Table 15)
        """
        return self.sampler.execute(self.set_pan_modulation_source_cmd, (arg0, arg1, ))

    def set_pan_modulation_value(self):
        """Set Pan Mod Value. <Data1>0-100
        """
        return self.sampler.execute(self.set_pan_modulation_value_cmd, ())

    def get_loudness(self):
        """Get Loudness.

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_loudness_cmd, ())

    def get_velocity_sens(self):
        """Get Velocity Sensitivity.

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_velocity_sens_cmd, ())

    def get_amp_modulation_source(self):
        """Get Amp Mod Source. <Data1> = Amp Mod (1 or 2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_amp_modulation_source_cmd, ())

    def get_amp_modulation_value(self):
        """Get Amp Mod Value. <Data1> = Amp Mod (1 or 2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_amp_modulation_value_cmd, ())

    def get_pan_modulation_source(self):
        """Get Pan Mod Source. <Data1> = Pan Mod (1, 2 or 3)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pan_modulation_source_cmd, ())

    def get_pan_modulation_value(self):
        """Get Pan Mod Value. <Data1> = Pan Mod (1, 2 or 3)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pan_modulation_value_cmd, ())

    def set_semitone_tune(self, arg0):
        """Semitone Tune
        """
        return self.sampler.execute(self.set_semitone_tune_cmd, (arg0, ))

    def set_fine_tune(self, arg0):
        """Fine Tune.
        """
        return self.sampler.execute(self.set_fine_tune_cmd, (arg0, ))

    def set_tune_template(self, arg0):
        """Tune Template, where <Data1> = template. 0=USER, 1=EVEN-TEMPERED, 2=ORCHESTRAL, 3=WERKMEISTER, 4=1/5 MEANTONE, 5=1/4 MEANTONE, 6=JUST, 7=ARABIAN.
        """
        return self.sampler.execute(self.set_tune_template_cmd, (arg0, ))

    def set_user_tune_template(self, arg0):
        """Set User Tune Template. All the values are sent one after the other starting at C. The format of each value is the same as for Item &31{49}. (i.e., 24 data bytes are representing all 12 notes.)
        """
        return self.sampler.execute(self.set_user_tune_template_cmd, (arg0, ))

    def set_key(self, arg0):
        """Set Key = <Data1> where: 0=C, 1=C#, 2=D, 3=Eb, 4=E, 5=F, 6=F#, 7=G, 8=G#, 9=A, 10=Bb, 11=B
        """
        return self.sampler.execute(self.set_key_cmd, (arg0, ))

    def get_semitone_tune(self):
        """Get Semitone Tune.

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_semitone_tune_cmd, ())

    def get_fine_tune(self):
        """Get Fine Tune.

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_fine_tune_cmd, ())

    def get_tune_template(self):
        """Get Tune Template.

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_tune_template_cmd, ())

    def get_user_tune_template(self):
        """Get User Tune Template.

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_user_tune_template_cmd, ())

    def get_key(self):
        """Get Key.

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_key_cmd, ())

    def set_pitch_bend_up(self, arg0):
        """Set Pitch Bend Up. <Data1> = semitones
        """
        return self.sampler.execute(self.set_pitch_bend_up_cmd, (arg0, ))

    def set_pitch_bend_down(self, arg0):
        """Set Pitch Bend Down. <Data1> = semitones
        """
        return self.sampler.execute(self.set_pitch_bend_down_cmd, (arg0, ))

    def set_bend_mode(self, arg0):
        """Set Bend Mode. <Data1> = mode, where 0=NORMAL, 1=HELD
        """
        return self.sampler.execute(self.set_bend_mode_cmd, (arg0, ))

    def set_aftertouch_value(self, arg0):
        """Set Aftertouch Value.
        """
        return self.sampler.execute(self.set_aftertouch_value_cmd, (arg0, ))

    def set_legato_setting(self, arg0):
        """Set Legato Setting <Data1> = mode, where 0=OFF, 1=ON
        """
        return self.sampler.execute(self.set_legato_setting_cmd, (arg0, ))

    def set_portamento_enabled(self, arg0):
        """Set Portamento Enable <Data1> = mode, where 0=OFF, 1=ON
        """
        return self.sampler.execute(self.set_portamento_enabled_cmd, (arg0, ))

    def set_portamento_mode(self, arg0):
        """Set Portamento Mode <Data1> = mode, where 0=TIME, 1=RATE
        """
        return self.sampler.execute(self.set_portamento_mode_cmd, (arg0, ))

    def set_portamento_time(self, arg0):
        """Set Portamento Time
        """
        return self.sampler.execute(self.set_portamento_time_cmd, (arg0, ))

    def get_pitch_bend_up(self):
        """Get Pitch Bend Up

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pitch_bend_up_cmd, ())

    def get_pitch_bend_down(self):
        """Get Pitch Bend Down

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pitch_bend_down_cmd, ())

    def get_bend_mode(self):
        """Get Bend Mode

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_bend_mode_cmd, ())

    def get_aftertouch_value(self):
        """Get Aftertouch Value

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_aftertouch_value_cmd, ())

    def get_legato_setting(self):
        """Get Legato Setting

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_legato_setting_cmd, ())

    def get_portamento_enabled(self):
        """Get Portamento Enable

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_portamento_enabled_cmd, ())

    def get_portamento_mode(self):
        """Get Portamento Mode

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_portamento_mode_cmd, ())

    def get_portamento_time(self):
        """Get Portamento Time

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_portamento_time_cmd, ())

    def set_lfo_rate(self, arg0, arg1):
        """Set LFO Rate. <Data1> = rate
        """
        return self.sampler.execute(self.set_lfo_rate_cmd, (arg0, arg1, ))

    def set_lfo_delay(self, arg0, arg1):
        """Set LFO Delay. <Data1> = delay
        """
        return self.sampler.execute(self.set_lfo_delay_cmd, (arg0, arg1, ))

    def set_lfo_depth(self, arg0, arg1):
        """Set LFO Depth. <Data1> = depth
        """
        return self.sampler.execute(self.set_lfo_depth_cmd, (arg0, arg1, ))

    def set_lfo_waveform(self, arg0, arg1):
        """Set LFO Waveform. <Data1> = waveform, where: 0=SINE, 1=TRIANGLE, 2=SQUARE, 3=SQUARE+, 4=SQUARE, 5=SAW BI, 6=SAW UP, 7=SAW DOWN, 8=RANDOM
        """
        return self.sampler.execute(self.set_lfo_waveform_cmd, (arg0, arg1, ))

    def set_lfo_sync(self, arg0, arg1):
        """Set LFO Sync. <Data1> = (0=OFF, 1=ON). (LFO1 only)
        """
        return self.sampler.execute(self.set_lfo_sync_cmd, (arg0, arg1, ))

    def set_lfo_retrigger(self, arg0, arg1):
        """Set LFO Re-trigger. <Data1> = (0=OFF, 1=ON). (LFO2 only)
        """
        return self.sampler.execute(self.set_lfo_retrigger_cmd, (arg0, arg1, ))

    def set_rate_modulation_source(self, arg0, arg1):
        """Set Rate Mod Source <Data1> = Modulation Source. (see Table 15)
        """
        return self.sampler.execute(self.set_rate_modulation_source_cmd, (arg0, arg1, ))

    def get_lfo_sync(self, arg0):
        """Get LFO Sync (LFO1 only)
        """
        return self.sampler.execute(self.get_lfo_sync_cmd, (arg0, ))

    def get_lfo_retrigger(self, arg0):
        """Get LFO Re-trigger (LFO2 only)
        """
        return self.sampler.execute(self.get_lfo_retrigger_cmd, (arg0, ))

    def get_rate_modulation_source(self, arg0):
        """Get Rate Mod Source

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_rate_modulation_source_cmd, (arg0, ))

    def get_rate_modulation_value(self, arg0):
        """Get Rate Mod Value

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_rate_modulation_value_cmd, (arg0, ))

    def get_delay_modulation_source(self, arg0):
        """Get Delay Mod Source

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_delay_modulation_source_cmd, (arg0, ))

    def get_delay_modulation_value(self, arg0):
        """Get Delay Mod Value

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_delay_modulation_value_cmd, (arg0, ))

    def get_depth_modulation_source(self, arg0):
        """Get Depth Mod Source

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_depth_modulation_source_cmd, (arg0, ))

    def get_depth_modulation_value(self, arg0):
        """Get Depth Mod Value

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_depth_modulation_value_cmd, (arg0, ))

    def get_modwheel(self, arg0):
        """Get Modwheel (LFO1 only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_modwheel_cmd, (arg0, ))

    def get_aftertouch(self, arg0):
        """Get Aftertouch (LFO1 only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_aftertouch_cmd, (arg0, ))

    def get_midi_clock_sync_enabled(self):
        """Get MIDI Clock Sync Enable (LFO2 only)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_midi_clock_sync_enabled_cmd, ())

    def get_midi_clock_sync_division(self, arg0):
        """Get MIDI Clock Sync Division (LFO2 only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_clock_sync_division_cmd, (arg0, ))

    def set_pitch_modulation_source(self, arg0, arg1):
        """Set Pitch Mod Source. <Data1> = Modulation Source. (see Table 15)
        """
        return self.sampler.execute(self.set_pitch_modulation_source_cmd, (arg0, arg1, ))

    def set_filter_modulation_source(self, arg0, arg1):
        """Set Filter Mod Input Source. <Data1> = Modulation Source. (see Table 15)
        """
        return self.sampler.execute(self.set_filter_modulation_source_cmd, (arg0, arg1, ))

    def get_pitch_modulation_source(self, arg0):
        """Get Pitch Mod Source. <Data1> = Pitch Mod (1 or 2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pitch_modulation_source_cmd, (arg0, ))

    def get_filter_modulation_source(self, arg0):
        """Get Filter Mod Input Source. <Data1> = Mod Input (1, 2 or 3)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_filter_modulation_source_cmd, (arg0, ))

    def get_handles_names(self):
        """Get list of program handles and names

        Returns:
            HANDLENAMEARRAY
        """
        handle_names = []
        names = self.get_names()
        for i in range(len(names)):
            handle_names.extend([i, names[i]])
        return handle_names

