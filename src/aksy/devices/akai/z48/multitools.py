
""" Python equivalent of akai section multitools

Methods to manipulate multis
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Multitools:
    def __init__(self, z48):
        self.sampler = z48
        self.get_no_items_cmd = Command('_', '\x18\x01', 'multitools', 'get_no_items', (), None)
        self.get_handles_cmd = Command('_', '\x18\x02\x00', 'multitools', 'get_handles', (), None)
        self.get_names_cmd = Command('_', '\x18\x02\x01', 'multitools', 'get_names', (), None)
        self.get_handles_names_cmd = Command('_', '\x18\x02\x02', 'multitools', 'get_handles_names', (), None)
        self.get_handles_tagged_cmd = Command('_', '\x18\x02\x03', 'multitools', 'get_handles_tagged', (), None)
        self.set_curr_by_handle_cmd = Command('_', '\x18\x03', 'multitools', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_curr_by_name_cmd = Command('_', '\x18\x04', 'multitools', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.get_curr_handle_cmd = Command('_', '\x18\x05', 'multitools', 'get_curr_handle', (), None)
        self.get_curr_name_cmd = Command('_', '\x18\x06', 'multitools', 'get_curr_name', (), None)
        self.get_name_by_handle_cmd = Command('_', '\x18\x07', 'multitools', 'get_name_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_handle_by_name_cmd = Command('_', '\x18\x08', 'multitools', 'get_handle_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_all_cmd = Command('_', '\x18\x09', 'multitools', 'delete_all', (), None)
        self.delete_curr_cmd = Command('_', '\x18\x0A', 'multitools', 'delete_curr', (), None)
        self.delete_by_handle_cmd = Command('_', '\x18\x0B', 'multitools', 'delete_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.rename_curr_cmd = Command('_', '\x18\x0C', 'multitools', 'rename_curr', (aksy.devices.akai.sysex_types.STRING,), None)
        self.rename_by_handle_cmd = Command('_', '\x18\x0D', 'multitools', 'rename_by_handle', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.STRING), None)
        self.tag_cmd = Command('_', '\x18\x0E', 'multitools', 'tag', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_tag_bitmap_cmd = Command('_', '\x18\x0F', 'multitools', 'get_tag_bitmap', (), None)
        self.get_curr_modified_cmd = Command('_', '\x18\x10', 'multitools', 'get_curr_modified', (), None)
        self.get_modified_cmd = Command('_', '\x18\x11', 'multitools', 'get_modified', (), None)
        self.delete_tagged_cmd = Command('_', '\x18\x18', 'multitools', 'delete_tagged', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.create_new_cmd = Command('_', '\x18\x40', 'multitools', 'create_new', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.STRING), None)
        self.copy_cmd = Command('_', '\x18\x41', 'multitools', 'copy', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_part_cmd = Command('_', '\x18\x42', 'multitools', 'delete_part', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.delete_unused_parts_cmd = Command('_', '\x18\x43', 'multitools', 'delete_unused_parts', (), None)
        self.arrange_parts_cmd = Command('_', '\x18\x44', 'multitools', 'arrange_parts', (), None)
        self.set_group_id_cmd = Command('_', '\x1A\x01', 'multitools', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_select_method_cmd = Command('_', '\x1A\x02', 'multitools', 'set_multi_select_method', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_select_channel_cmd = Command('_', '\x1A\x03', 'multitools', 'set_multi_select_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_tempo_cmd = Command('_', '\x1A\x04', 'multitools', 'set_multi_tempo', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_multi_program_no_cmd = Command('_', '\x1A\x08', 'multitools', 'set_multi_program_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_part_by_handle_cmd = Command('_', '\x1A\x09', 'multitools', 'set_multi_part_by_handle', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.DWORD), None)
        self.set_multi_part_name_cmd = Command('_', '\x1A\x0A', 'multitools', 'set_multi_part_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
        self.set_no_parts_cmd = Command('_', '\x1A\x0F', 'multitools', 'set_no_parts', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_part_midi_channel_cmd = Command('_', '\x1A\x10', 'multitools', 'set_part_midi_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_mute_cmd = Command('_', '\x1A\x11', 'multitools', 'set_part_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_part_solo_cmd = Command('_', '\x1A\x12', 'multitools', 'set_part_solo', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_part_level_cmd = Command('_', '\x1A\x13', 'multitools', 'set_part_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_part_output_cmd = Command('_', '\x1A\x14', 'multitools', 'set_part_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_pan_cmd = Command('_', '\x1A\x15', 'multitools', 'set_part_pan', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_fx_channel_cmd = Command('_', '\x1A\x16', 'multitools', 'set_part_fx_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_fx_send_level_cmd = Command('_', '\x1A\x17', 'multitools', 'set_part_fx_send_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_part_cents_tune_cmd = Command('_', '\x1A\x18', 'multitools', 'set_part_cents_tune', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_part_low_note_cmd = Command('_', '\x1A\x1A', 'multitools', 'set_part_low_note', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_high_note_cmd = Command('_', '\x1A\x1B', 'multitools', 'set_part_high_note', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_priority_cmd = Command('_', '\x1A\x1C', 'multitools', 'set_part_priority', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_program_no_cmd = Command('_', '\x1A\x1D', 'multitools', 'set_part_program_no', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_group_id_cmd = Command('_', '\x1A\x1F', 'multitools', 'set_part_group_id', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_eq_output_channel_cmd = Command('_', '\x1A\x30', 'multitools', 'set_eq_output_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.enable_eq_cmd = Command('_', '\x1A\x31', 'multitools', 'enable_eq', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_eq_low_gain_cmd = Command('_', '\x1A\x33', 'multitools', 'set_eq_low_gain', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_eq_low_freq_cmd = Command('_', '\x1A\x32', 'multitools', 'set_eq_low_freq', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_eq_mid_gain_cmd = Command('_', '\x1A\x34', 'multitools', 'set_eq_mid_gain', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_eq_mid_freq_cmd = Command('_', '\x1A\x34', 'multitools', 'set_eq_mid_freq', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_eq_high_gain_cmd = Command('_', '\x1A\x37', 'multitools', 'set_eq_high_gain', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_eq_high_freq_cmd = Command('_', '\x1A\x36', 'multitools', 'set_eq_high_freq', (aksy.devices.akai.sysex_types.WORD,), None)
        self.enable_midi_filter_cmd = Command('_', '\x1A\x40', 'multitools', 'enable_midi_filter', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_midi_filter_by_part_cmd = Command('_', '\x1A\x41', 'multitools', 'set_midi_filter_by_part', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_midi_filter_by_channel_cmd = Command('_', '\x1A\x42', 'multitools', 'set_midi_filter_by_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_fx_assign_type_cmd = Command('_', '\x1A\x50', 'multitools', 'set_fx_assign_type', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_target_cmd = Command('_', '\x1A\x51', 'multitools', 'set_target', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_destination_cmd = Command('_', '\x1A\x52', 'multitools', 'set_destination', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_change_type_cmd = Command('_', '\x1A\x53', 'multitools', 'set_change_type', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_scale_min_cmd = Command('_', '\x1A\x54', 'multitools', 'set_scale_min', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_scale_max_cmd = Command('_', '\x1A\x55', 'multitools', 'set_scale_max', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_midi_ctl_output_cmd = Command('_', '\x1A\x56', 'multitools', 'set_midi_ctl_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_midi_channel_output_cmd = Command('_', '\x1A\x57', 'multitools', 'set_midi_channel_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.get_group_id_cmd = Command('_', '\x1B\x01', 'multitools', 'get_group_id', (), None)
        self.get_multi_select_method_cmd = Command('_', '\x1B\x02', 'multitools', 'get_multi_select_method', (), None)
        self.get_multi_select_channel_cmd = Command('_', '\x1B\x03', 'multitools', 'get_multi_select_channel', (), None)
        self.get_multi_tempo_cmd = Command('_', '\x1B\x04', 'multitools', 'get_multi_tempo', (), None)
        self.get_multi_program_no_cmd = Command('_', '\x1B\x08', 'multitools', 'get_multi_program_no', (), None)
        self.get_multi_part_handle_cmd = Command('_', '\x1B\x09', 'multitools', 'get_multi_part_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_multi_part_name_cmd = Command('_', '\x1B\x0A', 'multitools', 'get_multi_part_name', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_no_parts_cmd = Command('_', '\x1B\x0F', 'multitools', 'get_no_parts', (), None)
        self.get_part_midi_channel_cmd = Command('_', '\x1B\x10', 'multitools', 'get_part_midi_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_mute_cmd = Command('_', '\x1B\x11', 'multitools', 'get_part_mute', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_solo_cmd = Command('_', '\x1B\x12', 'multitools', 'get_part_solo', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_level_cmd = Command('_', '\x1B\x13', 'multitools', 'get_part_level', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_output_cmd = Command('_', '\x1B\x14', 'multitools', 'get_part_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_pan_cmd = Command('_', '\x1B\x15', 'multitools', 'get_part_pan', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_fx_channel_cmd = Command('_', '\x1B\x16', 'multitools', 'get_part_fx_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_fx_send_level_cmd = Command('_', '\x1B\x17', 'multitools', 'get_part_fx_send_level', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_tune_cmd = Command('_', '\x1B\x18', 'multitools', 'get_part_tune', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_low_note_cmd = Command('_', '\x1B\x1A', 'multitools', 'get_part_low_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_high_note_cmd = Command('_', '\x1B\x1B', 'multitools', 'get_part_high_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_priority_cmd = Command('_', '\x1B\x1C', 'multitools', 'get_part_priority', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_prog_no_cmd = Command('_', '\x1B\x1D', 'multitools', 'get_part_prog_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_group_id_cmd = Command('_', '\x1B\x1F', 'multitools', 'get_part_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_eq_output_channel_cmd = Command('_', '\x1B\x30', 'multitools', 'get_eq_output_channel', (), None)
        self.is_eq_enabled_cmd = Command('_', '\x1B\x31', 'multitools', 'is_eq_enabled', (), None)
        self.get_eq_low_gain_cmd = Command('_', '\x1B\x33', 'multitools', 'get_eq_low_gain', (), None)
        self.get_eq_low_freq_cmd = Command('_', '\x1B\x32', 'multitools', 'get_eq_low_freq', (), None)
        self.get_eq_mid_gain_cmd = Command('_', '\x1B\x35', 'multitools', 'get_eq_mid_gain', (), None)
        self.get_eq_mid_freq_cmd = Command('_', '\x1B\x34', 'multitools', 'get_eq_mid_freq', (), None)
        self.get_eq_high_gain_cmd = Command('_', '\x1B\x37', 'multitools', 'get_eq_high_gain', (), None)
        self.get_eq_high_freq_cmd = Command('_', '\x1B\x36', 'multitools', 'get_eq_high_freq', (), None)
        self.is_midi_filter_enabled_cmd = Command('_', '\x1B\x40', 'multitools', 'is_midi_filter_enabled', (), None)
        self.get_midi_filter_by_part_cmd = Command('_', '\x1B\x41', 'multitools', 'get_midi_filter_by_part', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_midi_filter_by_channel_cmd = Command('_', '\x1B\x42', 'multitools', 'get_midi_filter_by_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_fx_assign_type_cmd = Command('_', '\x1B\x50', 'multitools', 'get_fx_assign_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_target_cmd = Command('_', '\x1B\x51', 'multitools', 'get_target', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_destination_cmd = Command('_', '\x1B\x52', 'multitools', 'get_destination', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_change_type_cmd = Command('_', '\x1B\x53', 'multitools', 'get_change_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_scale_min_cmd = Command('_', '\x1B\x54', 'multitools', 'get_scale_min', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_scale_max_cmd = Command('_', '\x1B\x55', 'multitools', 'get_scale_max', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_midi_ctl_output_cmd = Command('_', '\x1B\x56', 'multitools', 'get_midi_ctl_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_midi_channel_output_cmd = Command('_', '\x1B\x57', 'multitools', 'get_midi_channel_output', (aksy.devices.akai.sysex_types.BYTE,), None)

    def get_no_items(self):
        """Get number of items in memory

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_handles(self):
        """Get handles <Data1>: 0=list of handles

        Returns:
            DWORDARRAY
        """
        return self.sampler.execute(self.get_handles_cmd, ())

    def get_names(self):
        """Get names items: <Data1>; 1=list of names;

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_names_cmd, ())

    def get_handles_names(self):
        """Get handles names: <Data1>; 2=list of handle+name

        Returns:
            HANDLENAMEARRAY
        """
        return self.sampler.execute(self.get_handles_names_cmd, ())

    def get_handles_tagged(self):
        """Get handles tagged <Data1> ; 3=list of handle+modified/tagged name

        Returns:
            HANDLENAMEARRAY
        """
        return self.sampler.execute(self.get_handles_tagged_cmd, ())

    def set_curr_by_handle(self, arg0):
        """Select by handle
        """
        return self.sampler.execute(self.set_curr_by_handle_cmd, (arg0, ))

    def set_curr_by_name(self, arg0):
        """Select by name
        """
        return self.sampler.execute(self.set_curr_by_name_cmd, (arg0, ))

    def get_curr_handle(self):
        """Get current handle

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_curr_handle_cmd, ())

    def get_curr_name(self):
        """Get name of current item

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_curr_name_cmd, ())

    def get_name_by_handle(self, arg0):
        """Get item name from handle

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_name_by_handle_cmd, (arg0, ))

    def get_handle_by_name(self, arg0):
        """Get item handle from name

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_handle_by_name_cmd, (arg0, ))

    def delete_all(self):
        """Delete ALL items from memory
        """
        return self.sampler.execute(self.delete_all_cmd, ())

    def delete_curr(self):
        """Delete current item from memory
        """
        return self.sampler.execute(self.delete_curr_cmd, ())

    def delete_by_handle(self, arg0):
        """Delete item represented by handle <Data1>
        """
        return self.sampler.execute(self.delete_by_handle_cmd, (arg0, ))

    def rename_curr(self, arg0):
        """Rename current item
        """
        return self.sampler.execute(self.rename_curr_cmd, (arg0, ))

    def rename_by_handle(self, arg0, arg1):
        """Rename item represented by handle <Data1>
        """
        return self.sampler.execute(self.rename_by_handle_cmd, (arg0, arg1, ))

    def tag(self, arg0, arg1, arg2):
        """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) <Data3> = (0=CURRENT, 1=ALL)
        """
        return self.sampler.execute(self.tag_cmd, (arg0, arg1, arg2, ))

    def get_tag_bitmap(self):
        """Get Tag Bitmap

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_tag_bitmap_cmd, ())

    def get_curr_modified(self):
        """Get name of current item with modified/tagged info.

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_curr_modified_cmd, ())

    def get_modified(self):
        """Get modified state of current item

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_modified_cmd, ())

    def delete_tagged(self, arg0):
        """Delete tagged items <Data1> = tag bit
        """
        return self.sampler.execute(self.delete_tagged_cmd, (arg0, ))

    def create_new(self, arg0, arg1):
        """Create a new Multi
        """
        return self.sampler.execute(self.create_new_cmd, (arg0, arg1, ))

    def copy(self, arg0):
        """Copy a Multi
        """
        return self.sampler.execute(self.copy_cmd, (arg0, ))

    def delete_part(self, arg0):
        """Delete a specific part
        """
        return self.sampler.execute(self.delete_part_cmd, (arg0, ))

    def delete_unused_parts(self):
        """Delete unused parts
        """
        return self.sampler.execute(self.delete_unused_parts_cmd, ())

    def arrange_parts(self):
        """Arrange parts (sort by MIDI channel)
        """
        return self.sampler.execute(self.arrange_parts_cmd, ())

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.sampler.execute(self.set_group_id_cmd, (arg0, ))

    def set_multi_select_method(self, arg0):
        """Set Multi Select <Data1> = (0=OFF, 1=BANK, 2=PROG CHANGE)
        """
        return self.sampler.execute(self.set_multi_select_method_cmd, (arg0, ))

    def set_multi_select_channel(self, arg0):
        """Set Multi Select Channel <Data1> = (1A=0, 2A=1, ..., 16B=31)
        """
        return self.sampler.execute(self.set_multi_select_channel_cmd, (arg0, ))

    def set_multi_tempo(self, arg0):
        """Set Multi Tempo <Data1> = 10 bpm
        """
        return self.sampler.execute(self.set_multi_tempo_cmd, (arg0, ))

    def set_multi_program_no(self, arg0):
        """Set Multi Program Number Data1: (0=OFF, 1=128)
        """
        return self.sampler.execute(self.set_multi_program_no_cmd, (arg0, ))

    def set_multi_part_by_handle(self, arg0, arg1):
        """Set Multi Part by handle <Data1> = Part Number; <Data2> = Handle of program
        """
        return self.sampler.execute(self.set_multi_part_by_handle_cmd, (arg0, arg1, ))

    def set_multi_part_name(self, arg0, arg1):
        """Set Multi Part by name
        """
        return self.sampler.execute(self.set_multi_part_name_cmd, (arg0, arg1, ))

    def set_no_parts(self, arg0):
        """Set number of parts
        """
        return self.sampler.execute(self.set_no_parts_cmd, (arg0, ))

    def set_part_midi_channel(self, arg0, arg1):
        """Set midi channel of part
        """
        return self.sampler.execute(self.set_part_midi_channel_cmd, (arg0, arg1, ))

    def set_part_mute(self, arg0, arg1):
        """Set part mute
        """
        return self.sampler.execute(self.set_part_mute_cmd, (arg0, arg1, ))

    def set_part_solo(self, arg0, arg1):
        """Set part solo
        """
        return self.sampler.execute(self.set_part_solo_cmd, (arg0, arg1, ))

    def set_part_level(self, arg0, arg1):
        """Set part level
        """
        return self.sampler.execute(self.set_part_level_cmd, (arg0, arg1, ))

    def set_part_output(self, arg0, arg1):
        """Set part output
        """
        return self.sampler.execute(self.set_part_output_cmd, (arg0, arg1, ))

    def set_part_pan(self, arg0, arg1):
        """Set part pan
        """
        return self.sampler.execute(self.set_part_pan_cmd, (arg0, arg1, ))

    def set_part_fx_channel(self, arg0, arg1):
        """Set part fx channel
        """
        return self.sampler.execute(self.set_part_fx_channel_cmd, (arg0, arg1, ))

    def set_part_fx_send_level(self, arg0, arg1):
        """Set part fx send level
        """
        return self.sampler.execute(self.set_part_fx_send_level_cmd, (arg0, arg1, ))

    def set_part_cents_tune(self, arg0, arg1):
        """Set part cents tune
        """
        return self.sampler.execute(self.set_part_cents_tune_cmd, (arg0, arg1, ))

    def set_part_low_note(self, arg0, arg1):
        """Set part low note
        """
        return self.sampler.execute(self.set_part_low_note_cmd, (arg0, arg1, ))

    def set_part_high_note(self, arg0, arg1):
        """Set part high note
        """
        return self.sampler.execute(self.set_part_high_note_cmd, (arg0, arg1, ))

    def set_part_priority(self, arg0, arg1):
        """Set part priority
        """
        return self.sampler.execute(self.set_part_priority_cmd, (arg0, arg1, ))

    def set_part_program_no(self, arg0, arg1):
        """Set part program number
        """
        return self.sampler.execute(self.set_part_program_no_cmd, (arg0, arg1, ))

    def set_part_group_id(self, arg0, arg1):
        """Set part group id
        """
        return self.sampler.execute(self.set_part_group_id_cmd, (arg0, arg1, ))

    def set_eq_output_channel(self, arg0):
        """Set EQ Output Channel
        """
        return self.sampler.execute(self.set_eq_output_channel_cmd, (arg0, ))

    def enable_eq(self, arg0):
        """Enable EQ
        """
        return self.sampler.execute(self.enable_eq_cmd, (arg0, ))

    def set_eq_low_gain(self, arg0):
        """Set EQ low gain
        """
        return self.sampler.execute(self.set_eq_low_gain_cmd, (arg0, ))

    def set_eq_low_freq(self, arg0):
        """Set EQ low freq
        """
        return self.sampler.execute(self.set_eq_low_freq_cmd, (arg0, ))

    def set_eq_mid_gain(self, arg0):
        """Set EQ mid gain
        """
        return self.sampler.execute(self.set_eq_mid_gain_cmd, (arg0, ))

    def set_eq_mid_freq(self, arg0):
        """Set EQ mid freq
        """
        return self.sampler.execute(self.set_eq_mid_freq_cmd, (arg0, ))

    def set_eq_high_gain(self, arg0):
        """Set EQ high gain
        """
        return self.sampler.execute(self.set_eq_high_gain_cmd, (arg0, ))

    def set_eq_high_freq(self, arg0):
        """Set EQ high freq
        """
        return self.sampler.execute(self.set_eq_high_freq_cmd, (arg0, ))

    def enable_midi_filter(self, arg0):
        """Enable midi filter
        """
        return self.sampler.execute(self.enable_midi_filter_cmd, (arg0, ))

    def set_midi_filter_by_part(self, arg0, arg1, arg2):
        """Set midi filter by part
        """
        return self.sampler.execute(self.set_midi_filter_by_part_cmd, (arg0, arg1, arg2, ))

    def set_midi_filter_by_channel(self, arg0, arg1, arg2):
        """Set midi filter by channel
        """
        return self.sampler.execute(self.set_midi_filter_by_channel_cmd, (arg0, arg1, arg2, ))

    def set_fx_assign_type(self, arg0, arg1):
        """Set fx assign type (1: FX)
        """
        return self.sampler.execute(self.set_fx_assign_type_cmd, (arg0, arg1, ))

    def set_target(self, arg0, arg1):
        """Set target (part/channel)
        """
        return self.sampler.execute(self.set_target_cmd, (arg0, arg1, ))

    def set_destination(self, arg0, arg1):
        """Set destination
        """
        return self.sampler.execute(self.set_destination_cmd, (arg0, arg1, ))

    def set_change_type(self, arg0, arg1):
        """Set Change type (0: replace, 1: offset)
        """
        return self.sampler.execute(self.set_change_type_cmd, (arg0, arg1, ))

    def set_scale_min(self, arg0, arg1):
        """Set Scale minimum
        """
        return self.sampler.execute(self.set_scale_min_cmd, (arg0, arg1, ))

    def set_scale_max(self, arg0, arg1):
        """Set Scale maximum
        """
        return self.sampler.execute(self.set_scale_max_cmd, (arg0, arg1, ))

    def set_midi_ctl_output(self, arg0, arg1):
        """Set Midi controller output (0: off, 1-128)
        """
        return self.sampler.execute(self.set_midi_ctl_output_cmd, (arg0, arg1, ))

    def set_midi_channel_output(self, arg0, arg1):
        """Set Midi channel output (0: off, 1-128)
        """
        return self.sampler.execute(self.set_midi_channel_output_cmd, (arg0, arg1, ))

    def get_group_id(self):
        """Get Group ID

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_group_id_cmd, ())

    def get_multi_select_method(self):
        """Get Multi Select <Reply1> = (0=OFF, 1=BANK, 2=PROG CHANGE)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_multi_select_method_cmd, ())

    def get_multi_select_channel(self):
        """Get Multi Select Channel <Reply1> = (1A=0, 2A=1, ..., 16B=31)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_multi_select_channel_cmd, ())

    def get_multi_tempo(self):
        """Get Multi Tempo <Reply> = 10 bpm

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_multi_tempo_cmd, ())

    def get_multi_program_no(self):
        """Get Multi Program Number

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_multi_program_no_cmd, ())

    def get_multi_part_handle(self, arg0):
        """Get Multi Part handle. <Data1> = Part Number;<Reply> = Handle of program>

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_multi_part_handle_cmd, (arg0, ))

    def get_multi_part_name(self, arg0):
        """Get Multi Part name. <Data1> = Part Number; <Reply> = Name of part

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_multi_part_name_cmd, (arg0, ))

    def get_no_parts(self):
        """Get Number of Parts. <Reply> = new number of parts

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_parts_cmd, ())

    def get_part_midi_channel(self, arg0):
        """Get Part MIDI Channel, (Data1 = Part Number-1a) <Reply> = (1A=0, 2A=1, ..., 16B=31)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_midi_channel_cmd, (arg0, ))

    def get_part_mute(self, arg0):
        """Get Part Mute, <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_mute_cmd, (arg0, ))

    def get_part_solo(self, arg0):
        """Get Part Solo, <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_solo_cmd, (arg0, ))

    def get_part_level(self, arg0):
        """Get Part Level, <Reply> = PartLevel in 10 dB

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_part_level_cmd, (arg0, ))

    def get_part_output(self, arg0):
        """Get Part Output, <Reply> = (Output: 0 = L/R; 1-4 = op1/2 op7/8; 5 = 14 = L, R, op1-op8)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_output_cmd, (arg0, ))

    def get_part_pan(self, arg0):
        """Get Part Pan/Balance, <Reply> = Pan/Bal (0-100 = L50-R50); centre=50

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_pan_cmd, (arg0, ))

    def get_part_fx_channel(self, arg0):
        """Get Part Effects Channel: Reply = (0=OFF, 1=FX1, 2=FX2, 3=RV3, 4=RV4)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_fx_channel_cmd, (arg0, ))

    def get_part_fx_send_level(self, arg0):
        """Get Part FX Send Level <Reply> = level in 10 dB

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_part_fx_send_level_cmd, (arg0, ))

    def get_part_tune(self, arg0):
        """Get Part Cents Tune

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_part_tune_cmd, (arg0, ))

    def get_part_low_note(self, arg0):
        """Get Part Low Note

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_low_note_cmd, (arg0, ))

    def get_part_high_note(self, arg0):
        """Get Part High Note

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_high_note_cmd, (arg0, ))

    def get_part_priority(self, arg0):
        """Get Part Priority

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_priority_cmd, (arg0, ))

    def get_part_prog_no(self, arg0):
        """Get Part Program Number

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_prog_no_cmd, (arg0, ))

    def get_part_group_id(self, arg0):
        """Get Part Group ID

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_part_group_id_cmd, (arg0, ))

    def get_eq_output_channel(self):
        """Get EQ Output Channel

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_eq_output_channel_cmd, ())

    def is_eq_enabled(self):
        """Whether EQ is enabled

        Returns:
            BOOL
        """
        return self.sampler.execute(self.is_eq_enabled_cmd, ())

    def get_eq_low_gain(self):
        """Get EQ low gain

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_eq_low_gain_cmd, ())

    def get_eq_low_freq(self):
        """Get EQ low freq

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_eq_low_freq_cmd, ())

    def get_eq_mid_gain(self):
        """Get EQ mid gain

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_eq_mid_gain_cmd, ())

    def get_eq_mid_freq(self):
        """Get EQ mid freq

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_eq_mid_freq_cmd, ())

    def get_eq_high_gain(self):
        """Get EQ high gain

        Returns:
            SWOR
        """
        return self.sampler.execute(self.get_eq_high_gain_cmd, ())

    def get_eq_high_freq(self):
        """Get EQ high freq

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_eq_high_freq_cmd, ())

    def is_midi_filter_enabled(self):
        """Whether the midi filter is enabled

        Returns:
            BOOL
        """
        return self.sampler.execute(self.is_midi_filter_enabled_cmd, ())

    def get_midi_filter_by_part(self, arg0, arg1):
        """Get midi filter by part

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_filter_by_part_cmd, (arg0, arg1, ))

    def get_midi_filter_by_channel(self, arg0, arg1):
        """Get midi filter by channel

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_filter_by_channel_cmd, (arg0, arg1, ))

    def get_fx_assign_type(self, arg0):
        """Get fx assign type (1: FX)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_fx_assign_type_cmd, (arg0, ))

    def get_target(self, arg0):
        """Get target (part/channel)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_target_cmd, (arg0, ))

    def get_destination(self, arg0):
        """Get destination

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_destination_cmd, (arg0, ))

    def get_change_type(self, arg0):
        """Get Change type (0: replace, 1: offset)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_change_type_cmd, (arg0, ))

    def get_scale_min(self, arg0):
        """Get Scale minimum

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_scale_min_cmd, (arg0, ))

    def get_scale_max(self, arg0):
        """Get Scale maximum

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_scale_max_cmd, (arg0, ))

    def get_midi_ctl_output(self, arg0):
        """Get Midi controller output (0: off, 1-128)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_midi_ctl_output_cmd, (arg0, ))

    def get_midi_channel_output(self, arg0):
        """Get Midi channel output (0: off, 1-128)

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_midi_channel_output_cmd, (arg0, ))

