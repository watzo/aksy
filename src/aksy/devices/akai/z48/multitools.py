
""" Python equivalent of akai section multitools

Methods to manipulate multis
"""

__author__ =  'Walco van Loon'
__version__=  '$Rev$'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Multitools:
    def __init__(self, z48):
        self.z48 = z48
        self.get_no_items_cmd = Command('_', '\x18\x01', 'get_no_items', (), None)
        self.get_handles_cmd = Command('_', '\x18\x02\x00', 'get_handles', (), None)
        self.get_names_cmd = Command('_', '\x18\x02\x01', 'get_names', (), None)
        self.get_handles_names_cmd = Command('_', '\x18\x02\x02', 'get_handles_names', (), None)
        self.get_handles_tagged_cmd = Command('_', '\x18\x02\x03', 'get_handles_tagged', (), None)
        self.set_curr_by_handle_cmd = Command('_', '\x18\x03', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_curr_by_name_cmd = Command('_', '\x18\x04', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.get_curr_handle_cmd = Command('_', '\x18\x05', 'get_curr_handle', (), None)
        self.get_curr_name_cmd = Command('_', '\x18\x06', 'get_curr_name', (), None)
        self.get_name_by_handle_cmd = Command('_', '\x18\x07', 'get_name_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_handle_by_name_cmd = Command('_', '\x18\x08', 'get_handle_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_all_cmd = Command('_', '\x18\x09', 'delete_all', (), None)
        self.delete_curr_cmd = Command('_', '\x18\x0A', 'delete_curr', (), None)
        self.delete_by_handle_cmd = Command('_', '\x18\x0B', 'delete_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.rename_curr_cmd = Command('_', '\x18\x0C', 'rename_curr', (aksy.devices.akai.sysex_types.STRING,), None)
        self.rename_by_handle_cmd = Command('_', '\x18\x0D', 'rename_by_handle', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.STRING), None)
        self.tag_cmd = Command('_', '\x18\x0E', 'tag', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_tag_bitmap_cmd = Command('_', '\x18\x0F', 'get_tag_bitmap', (), None)
        self.get_curr_modified_cmd = Command('_', '\x18\x10', 'get_curr_modified', (), None)
        self.get_modified_cmd = Command('_', '\x18\x11', 'get_modified', (), None)
        self.set_group_id_cmd = Command('_', '\x1A\x01', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_select_method_cmd = Command('_', '\x1A\x02', 'set_multi_select_method', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_select_channel_cmd = Command('_', '\x1A\x03', 'set_multi_select_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_tempo_cmd = Command('_', '\x1A\x04', 'set_multi_tempo', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_multi_program_no_cmd = Command('_', '\x1A\x08', 'set_multi_program_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_part_by_handle_cmd = Command('_', '\x1A\x09', 'set_multi_part_by_handle', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.DWORD), None)
        self.set_multi_part_by_name_cmd = Command('_', '\x1A\x0A', 'set_multi_part_by_name', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
        self.set_no_parts_cmd = Command('_', '\x1A\x0F', 'set_no_parts', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_part_midi_channel_cmd = Command('_', '\x1A\x10', 'set_part_midi_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_mute_cmd = Command('_', '\x1A\x11', 'set_part_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_part_solo_cmd = Command('_', '\x1A\x12', 'set_part_solo', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_part_level_cmd = Command('_', '\x1A\x13', 'set_part_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_part_output_cmd = Command('_', '\x1A\x14', 'set_part_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_pan_cmd = Command('_', '\x1A\x15', 'set_part_pan', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_fx_channel_cmd = Command('_', '\x1A\x16', 'set_part_fx_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_fx_send_level_cmd = Command('_', '\x1A\x17', 'set_part_fx_send_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_part_cents_tune_cmd = Command('_', '\x1A\x18', 'set_part_cents_tune', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_part_low_note_cmd = Command('_', '\x1A\x1A', 'set_part_low_note', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_high_note_cmd = Command('_', '\x1A\x1B', 'set_part_high_note', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_priority_cmd = Command('_', '\x1A\x1C', 'set_part_priority', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_program_no_cmd = Command('_', '\x1A\x1D', 'set_part_program_no', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_part_group_id_cmd = Command('_', '\x1A\x1F', 'set_part_group_id', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_eq_output_channel_cmd = Command('_', '\x1A\x30', 'set_eq_output_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.enable_eq_cmd = Command('_', '\x1A\x31', 'enable_eq', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_eq_low_gain_cmd = Command('_', '\x1A\x32', 'set_eq_low_gain', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_eq_low_freq_cmd = Command('_', '\x1A\x33', 'set_eq_low_freq', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_eq_mid_gain_cmd = Command('_', '\x1A\x34', 'set_eq_mid_gain', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_eq_mid_freq_cmd = Command('_', '\x1A\x35', 'set_eq_mid_freq', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_eq_high_gain_cmd = Command('_', '\x1A\x36', 'set_eq_high_gain', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_eq_high_freq_cmd = Command('_', '\x1A\x37', 'set_eq_high_freq', (aksy.devices.akai.sysex_types.WORD,), None)
        self.enable_midi_filter_cmd = Command('_', '\x1A\x40', 'enable_midi_filter', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_midi_filter_by_part_cmd = Command('_', '\x1A\x41', 'set_midi_filter_by_part', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_midi_filter_by_channel_cmd = Command('_', '\x1A\x42', 'set_midi_filter_by_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_fx_assign_type_cmd = Command('_', '\x1A\x50', 'set_fx_assign_type', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_target_cmd = Command('_', '\x1A\x51', 'set_target', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_destination_cmd = Command('_', '\x1A\x52', 'set_destination', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_change_type_cmd = Command('_', '\x1A\x53', 'set_change_type', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_scale_min_cmd = Command('_', '\x1A\x54', 'set_scale_min', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_scale_max_cmd = Command('_', '\x1A\x55', 'set_scale_max', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_midi_ctl_output_cmd = Command('_', '\x1A\x56', 'set_midi_ctl_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_midi_channel_output_cmd = Command('_', '\x1A\x57', 'set_midi_channel_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.get_group_id_cmd = Command('_', '\x1B\x01', 'get_group_id', (), None)
        self.get_multi_select_method_cmd = Command('_', '\x1B\x02', 'get_multi_select_method', (), None)
        self.get_multi_select_channel_cmd = Command('_', '\x1B\x03', 'get_multi_select_channel', (), None)
        self.get_multi_tempo_cmd = Command('_', '\x1B\x04', 'get_multi_tempo', (), None)
        self.get_multi_program_no_cmd = Command('_', '\x1B\x08', 'get_multi_program_no', (), None)
        self.get_multi_part_handle_cmd = Command('_', '\x1B\x09', 'get_multi_part_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_multi_part_name_cmd = Command('_', '\x1B\x0A', 'get_multi_part_name', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_no_parts_cmd = Command('_', '\x1B\x0F', 'get_no_parts', (), None)
        self.get_part_midi_channel_cmd = Command('_', '\x1B\x10', 'get_part_midi_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_mute_cmd = Command('_', '\x1B\x11', 'get_part_mute', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_solo_cmd = Command('_', '\x1B\x12', 'get_part_solo', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_level_cmd = Command('_', '\x1B\x13', 'get_part_level', (), None)
        self.get_part_output_cmd = Command('_', '\x1B\x14', 'get_part_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_pan_cmd = Command('_', '\x1B\x15', 'get_part_pan', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_fx_channel_cmd = Command('_', '\x1B\x16', 'get_part_fx_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_fx_send_level_cmd = Command('_', '\x1B\x17', 'get_part_fx_send_level', (), None)
        self.get_part_tune_cmd = Command('_', '\x1B\x18', 'get_part_tune', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_low_note_cmd = Command('_', '\x1B\x1A', 'get_part_low_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_high_note_cmd = Command('_', '\x1B\x1B', 'get_part_high_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_priority_cmd = Command('_', '\x1B\x1C', 'get_part_priority', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_prog_no_cmd = Command('_', '\x1B\x1D', 'get_part_prog_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_part_group_id_cmd = Command('_', '\x1B\x1F', 'get_part_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_eq_output_channel_cmd = Command('_', '\x1B\x30', 'get_eq_output_channel', (), None)
        self.is_eq_enabled_cmd = Command('_', '\x1B\x31', 'is_eq_enabled', (), None)
        self.get_eq_low_gain_cmd = Command('_', '\x1B\x32', 'get_eq_low_gain', (), None)
        self.get_eq_low_freq_cmd = Command('_', '\x1B\x33', 'get_eq_low_freq', (), None)
        self.get_eq_mid_gain_cmd = Command('_', '\x1B\x34', 'get_eq_mid_gain', (), None)
        self.get_eq_mid_freq_cmd = Command('_', '\x1B\x35', 'get_eq_mid_freq', (), None)
        self.get_eq_high_gain_cmd = Command('_', '\x1B\x36', 'get_eq_high_gain', (), None)
        self.get_eq_high_freq_cmd = Command('_', '\x1B\x37', 'get_eq_high_freq', (), None)
        self.is_midi_filter_enabled_cmd = Command('_', '\x1B\x40', 'is_midi_filter_enabled', (), None)
        self.get_midi_filter_by_part_cmd = Command('_', '\x1B\x41', 'get_midi_filter_by_part', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_midi_filter_by_channel_cmd = Command('_', '\x1B\x42', 'get_midi_filter_by_channel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_fx_assign_type_cmd = Command('_', '\x1B\x50', 'get_fx_assign_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_target_cmd = Command('_', '\x1B\x51', 'get_target', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_destination_cmd = Command('_', '\x1B\x52', 'get_destination', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_change_type_cmd = Command('_', '\x1B\x53', 'get_change_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_scale_min_cmd = Command('_', '\x1B\x54', 'get_scale_min', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_scale_max_cmd = Command('_', '\x1B\x55', 'get_scale_max', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_midi_ctl_output_cmd = Command('_', '\x1B\x56', 'get_midi_ctl_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_midi_channel_output_cmd = Command('_', '\x1B\x57', 'get_midi_channel_output', (aksy.devices.akai.sysex_types.BYTE,), None)

    def get_no_items(self):
        """Get number of items in memory

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_no_items_cmd, ())

    def get_handles(self):
        """Get handles <Data1>: 0=list of handles

        Returns:
            DWORD
        """
        return self.z48.execute(self.get_handles_cmd, ())

    def get_names(self):
        """Get names items: <Data1>; 1=list of names;

        Returns:
            STRINGARRAY
        """
        return self.z48.execute(self.get_names_cmd, ())

    def get_handles_names(self):
        """Get handles names: <Data1>; 2=list of handle+name

        Returns:
            HANDLENAMEARRAY
        """
        return self.z48.execute(self.get_handles_names_cmd, ())

    def get_handles_tagged(self):
        """Get handles tagged <Data1> ; 3=list of handle+modified/tagged name

        Returns:
            HANDLENAMEARRAY
        """
        return self.z48.execute(self.get_handles_tagged_cmd, ())

    def set_curr_by_handle(self, arg0):
        """Select by handle
        """
        return self.z48.execute(self.set_curr_by_handle_cmd, (arg0, ))

    def set_curr_by_name(self, arg0):
        """Select by name
        """
        return self.z48.execute(self.set_curr_by_name_cmd, (arg0, ))

    def get_curr_handle(self):
        """Get current handle

        Returns:
            DWORD
        """
        return self.z48.execute(self.get_curr_handle_cmd, ())

    def get_curr_name(self):
        """Get name of current item

        Returns:
            STRING
        """
        return self.z48.execute(self.get_curr_name_cmd, ())

    def get_name_by_handle(self, arg0):
        """Get item name from handle

        Returns:
            STRING
        """
        return self.z48.execute(self.get_name_by_handle_cmd, (arg0, ))

    def get_handle_by_name(self, arg0):
        """Get item handle from name

        Returns:
            DWORD
        """
        return self.z48.execute(self.get_handle_by_name_cmd, (arg0, ))

    def delete_all(self):
        """Delete ALL items from memory
        """
        return self.z48.execute(self.delete_all_cmd, ())

    def delete_curr(self):
        """Delete current item from memory
        """
        return self.z48.execute(self.delete_curr_cmd, ())

    def delete_by_handle(self, arg0):
        """Delete item represented by handle <Data1>
        """
        return self.z48.execute(self.delete_by_handle_cmd, (arg0, ))

    def rename_curr(self, arg0):
        """Rename current item
        """
        return self.z48.execute(self.rename_curr_cmd, (arg0, ))

    def rename_by_handle(self, arg0, arg1):
        """Rename item represented by handle <Data1>
        """
        return self.z48.execute(self.rename_by_handle_cmd, (arg0, arg1, ))

    def tag(self, arg0, arg1, arg2):
        """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) <Data3> = (0=CURRENT, 1=ALL)
        """
        return self.z48.execute(self.tag_cmd, (arg0, arg1, arg2, ))

    def get_tag_bitmap(self):
        """Get Tag Bitmap

        Returns:
            WORD
        """
        return self.z48.execute(self.get_tag_bitmap_cmd, ())

    def get_curr_modified(self):
        """Get name of current item with modified/tagged info.

        Returns:
            STRINGARRAY
        """
        return self.z48.execute(self.get_curr_modified_cmd, ())

    def get_modified(self):
        """Get modified state of current item

        Returns:
            BOOL
        """
        return self.z48.execute(self.get_modified_cmd, ())

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.z48.execute(self.set_group_id_cmd, (arg0, ))

    def set_multi_select_method(self, arg0):
        """Set Multi Select <Data1> = (0=OFF, 1=BANK, 2=PROG CHANGE)
        """
        return self.z48.execute(self.set_multi_select_method_cmd, (arg0, ))

    def set_multi_select_channel(self, arg0):
        """Set Multi Select Channel <Data1> = (1A=0, 2A=1, ..., 16B=31)
        """
        return self.z48.execute(self.set_multi_select_channel_cmd, (arg0, ))

    def set_multi_tempo(self, arg0):
        """Set Multi Tempo <Data1> = 10 bpm
        """
        return self.z48.execute(self.set_multi_tempo_cmd, (arg0, ))

    def set_multi_program_no(self, arg0):
        """Set Multi Program Number Data1: (0=OFF, 1=128)
        """
        return self.z48.execute(self.set_multi_program_no_cmd, (arg0, ))

    def set_multi_part_by_handle(self, arg0, arg1):
        """Set Multi Part by handle <Data1> = Part Number; <Data2> = Handle of program
        """
        return self.z48.execute(self.set_multi_part_by_handle_cmd, (arg0, arg1, ))

    def set_multi_part_by_name(self, arg0, arg1):
        """Set Multi Part by name
        """
        return self.z48.execute(self.set_multi_part_by_name_cmd, (arg0, arg1, ))

    def set_no_parts(self, arg0):
        """Set number of parts
        """
        return self.z48.execute(self.set_no_parts_cmd, (arg0, ))

    def set_part_midi_channel(self, arg0, arg1):
        """Set midi channel of part
        """
        return self.z48.execute(self.set_part_midi_channel_cmd, (arg0, arg1, ))

    def set_part_mute(self, arg0, arg1):
        """Set part mute
        """
        return self.z48.execute(self.set_part_mute_cmd, (arg0, arg1, ))

    def set_part_solo(self, arg0, arg1):
        """Set part solo
        """
        return self.z48.execute(self.set_part_solo_cmd, (arg0, arg1, ))

    def set_part_level(self, arg0, arg1):
        """Set part level
        """
        return self.z48.execute(self.set_part_level_cmd, (arg0, arg1, ))

    def set_part_output(self, arg0, arg1):
        """Set part output
        """
        return self.z48.execute(self.set_part_output_cmd, (arg0, arg1, ))

    def set_part_pan(self, arg0, arg1):
        """Set part pan
        """
        return self.z48.execute(self.set_part_pan_cmd, (arg0, arg1, ))

    def set_part_fx_channel(self, arg0, arg1):
        """Set part fx channel
        """
        return self.z48.execute(self.set_part_fx_channel_cmd, (arg0, arg1, ))

    def set_part_fx_send_level(self, arg0, arg1):
        """Set part fx send level
        """
        return self.z48.execute(self.set_part_fx_send_level_cmd, (arg0, arg1, ))

    def set_part_cents_tune(self, arg0, arg1):
        """Set part cents tune
        """
        return self.z48.execute(self.set_part_cents_tune_cmd, (arg0, arg1, ))

    def set_part_low_note(self, arg0, arg1):
        """Set part low note
        """
        return self.z48.execute(self.set_part_low_note_cmd, (arg0, arg1, ))

    def set_part_high_note(self, arg0, arg1):
        """Set part high note
        """
        return self.z48.execute(self.set_part_high_note_cmd, (arg0, arg1, ))

    def set_part_priority(self, arg0, arg1):
        """Set part priority
        """
        return self.z48.execute(self.set_part_priority_cmd, (arg0, arg1, ))

    def set_part_program_no(self, arg0, arg1):
        """Set part program number
        """
        return self.z48.execute(self.set_part_program_no_cmd, (arg0, arg1, ))

    def set_part_group_id(self, arg0, arg1):
        """Set part group id
        """
        return self.z48.execute(self.set_part_group_id_cmd, (arg0, arg1, ))

    def set_eq_output_channel(self, arg0):
        """Set EQ Output Channel
        """
        return self.z48.execute(self.set_eq_output_channel_cmd, (arg0, ))

    def enable_eq(self, arg0):
        """Enable EQ
        """
        return self.z48.execute(self.enable_eq_cmd, (arg0, ))

    def set_eq_low_gain(self, arg0):
        """Set EQ low gain
        """
        return self.z48.execute(self.set_eq_low_gain_cmd, (arg0, ))

    def set_eq_low_freq(self, arg0):
        """Set EQ low freq
        """
        return self.z48.execute(self.set_eq_low_freq_cmd, (arg0, ))

    def set_eq_mid_gain(self, arg0):
        """Set EQ mid gain
        """
        return self.z48.execute(self.set_eq_mid_gain_cmd, (arg0, ))

    def set_eq_mid_freq(self, arg0):
        """Set EQ mid freq
        """
        return self.z48.execute(self.set_eq_mid_freq_cmd, (arg0, ))

    def set_eq_high_gain(self, arg0):
        """Set EQ high gain
        """
        return self.z48.execute(self.set_eq_high_gain_cmd, (arg0, ))

    def set_eq_high_freq(self, arg0):
        """Set EQ high freq
        """
        return self.z48.execute(self.set_eq_high_freq_cmd, (arg0, ))

    def enable_midi_filter(self, arg0):
        """Enable midi filter
        """
        return self.z48.execute(self.enable_midi_filter_cmd, (arg0, ))

    def set_midi_filter_by_part(self, arg0, arg1, arg2):
        """Set midi filter by part
        """
        return self.z48.execute(self.set_midi_filter_by_part_cmd, (arg0, arg1, arg2, ))

    def set_midi_filter_by_channel(self, arg0, arg1, arg2):
        """Set midi filter by channel
        """
        return self.z48.execute(self.set_midi_filter_by_channel_cmd, (arg0, arg1, arg2, ))

    def set_fx_assign_type(self, arg0, arg1):
        """Set fx assign type (1: FX)
        """
        return self.z48.execute(self.set_fx_assign_type_cmd, (arg0, arg1, ))

    def set_target(self, arg0, arg1):
        """Set target (part/channel)
        """
        return self.z48.execute(self.set_target_cmd, (arg0, arg1, ))

    def set_destination(self, arg0, arg1):
        """Set destination
        """
        return self.z48.execute(self.set_destination_cmd, (arg0, arg1, ))

    def set_change_type(self, arg0, arg1):
        """Set Change type (0: replace, 1: offset)
        """
        return self.z48.execute(self.set_change_type_cmd, (arg0, arg1, ))

    def set_scale_min(self, arg0, arg1):
        """Set Scale minimum
        """
        return self.z48.execute(self.set_scale_min_cmd, (arg0, arg1, ))

    def set_scale_max(self, arg0, arg1):
        """Set Scale maximum
        """
        return self.z48.execute(self.set_scale_max_cmd, (arg0, arg1, ))

    def set_midi_ctl_output(self, arg0, arg1):
        """Set Midi controller output (0: off, 1-128)
        """
        return self.z48.execute(self.set_midi_ctl_output_cmd, (arg0, arg1, ))

    def set_midi_channel_output(self, arg0, arg1):
        """Set Midi channel output (0: off, 1-128)
        """
        return self.z48.execute(self.set_midi_channel_output_cmd, (arg0, arg1, ))

    def get_group_id(self):
        """Get Group ID

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_group_id_cmd, ())

    def get_multi_select_method(self):
        """Get Multi Select <Reply1> = (0=OFF, 1=BANK, 2=PROG CHANGE)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_multi_select_method_cmd, ())

    def get_multi_select_channel(self):
        """Get Multi Select Channel <Reply1> = (1A=0, 2A=1, ..., 16B=31)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_multi_select_channel_cmd, ())

    def get_multi_tempo(self):
        """Get Multi Tempo <Reply> = 10 bpm

        Returns:
            WORD
        """
        return self.z48.execute(self.get_multi_tempo_cmd, ())

    def get_multi_program_no(self):
        """Get Multi Program Number

        Returns:
            WORD
        """
        return self.z48.execute(self.get_multi_program_no_cmd, ())

    def get_multi_part_handle(self, arg0):
        """Get Multi Part handle. <Data1> = Part Number;<Reply> = Handle of program>

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_multi_part_handle_cmd, (arg0, ))

    def get_multi_part_name(self, arg0):
        """Get Multi Part name. <Data1> = Part Number; <Reply> = Name of part

        Returns:
            STRING
        """
        return self.z48.execute(self.get_multi_part_name_cmd, (arg0, ))

    def get_no_parts(self):
        """Get Number of Parts. <Reply> = new number of parts

        Returns:
            WORD
        """
        return self.z48.execute(self.get_no_parts_cmd, ())

    def get_part_midi_channel(self, arg0):
        """Get Part MIDI Channel, (Data1 = Part Number-1a) <Reply> = (1A=0, 2A=1, ..., 16B=31)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_midi_channel_cmd, (arg0, ))

    def get_part_mute(self, arg0):
        """Get Part Mute, <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_mute_cmd, (arg0, ))

    def get_part_solo(self, arg0):
        """Get Part Solo, <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_solo_cmd, (arg0, ))

    def get_part_level(self):
        """Get Part Level, <Reply> = PartLevel in 10 dB

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_part_level_cmd, ())

    def get_part_output(self, arg0):
        """Get Part Output, <Reply> = (Output: 0 = L/R; 1-4 = op1/2 op7/8; 5 = 14 = L, R, op1-op8)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_output_cmd, (arg0, ))

    def get_part_pan(self, arg0):
        """Get Part Pan/Balance, <Reply> = Pan/Bal (0-100 = L50-R50); centre=50

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_pan_cmd, (arg0, ))

    def get_part_fx_channel(self, arg0):
        """Get Part Effects Channel: Reply = (0=OFF, 1=FX1, 2=FX2, 3=RV3, 4=RV4)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_fx_channel_cmd, (arg0, ))

    def get_part_fx_send_level(self):
        """Get Part FX Send Level <Reply> = level in 10 dB

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_part_fx_send_level_cmd, ())

    def get_part_tune(self, arg0):
        """Get Part Cents Tune

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_part_tune_cmd, (arg0, ))

    def get_part_low_note(self, arg0):
        """Get Part Low Note

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_low_note_cmd, (arg0, ))

    def get_part_high_note(self, arg0):
        """Get Part High Note

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_high_note_cmd, (arg0, ))

    def get_part_priority(self, arg0):
        """Get Part Priority

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_priority_cmd, (arg0, ))

    def get_part_prog_no(self, arg0):
        """Get Part Program Number

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_prog_no_cmd, (arg0, ))

    def get_part_group_id(self, arg0):
        """Get Part Group ID

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_part_group_id_cmd, (arg0, ))

    def get_eq_output_channel(self):
        """Get EQ Output Channel

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_eq_output_channel_cmd, ())

    def is_eq_enabled(self):
        """Whether EQ is enabled

        Returns:
            BOOL
        """
        return self.z48.execute(self.is_eq_enabled_cmd, ())

    def get_eq_low_gain(self):
        """Get EQ low gain

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_eq_low_gain_cmd, ())

    def get_eq_low_freq(self):
        """Get EQ low freq

        Returns:
            WORD
        """
        return self.z48.execute(self.get_eq_low_freq_cmd, ())

    def get_eq_mid_gain(self):
        """Get EQ mid gain

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_eq_mid_gain_cmd, ())

    def get_eq_mid_freq(self):
        """Get EQ mid freq

        Returns:
            WORD
        """
        return self.z48.execute(self.get_eq_mid_freq_cmd, ())

    def get_eq_high_gain(self):
        """Get EQ high gain

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_eq_high_gain_cmd, ())

    def get_eq_high_freq(self):
        """Get EQ high freq

        Returns:
            WORD
        """
        return self.z48.execute(self.get_eq_high_freq_cmd, ())

    def is_midi_filter_enabled(self):
        """Whether the midi filter is enabled

        Returns:
            BOOL
        """
        return self.z48.execute(self.is_midi_filter_enabled_cmd, ())

    def get_midi_filter_by_part(self, arg0, arg1):
        """Get midi filter by part

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_midi_filter_by_part_cmd, (arg0, arg1, ))

    def get_midi_filter_by_channel(self, arg0, arg1):
        """Get midi filter by channel

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_midi_filter_by_channel_cmd, (arg0, arg1, ))

    def get_fx_assign_type(self, arg0):
        """Get fx assign type (1: FX)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_fx_assign_type_cmd, (arg0, ))

    def get_target(self, arg0):
        """Get target (part/channel)

        Returns:
            WORD
        """
        return self.z48.execute(self.get_target_cmd, (arg0, ))

    def get_destination(self, arg0):
        """Get destination

        Returns:
            WORD
        """
        return self.z48.execute(self.get_destination_cmd, (arg0, ))

    def get_change_type(self, arg0):
        """Get Change type (0: replace, 1: offset)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_change_type_cmd, (arg0, ))

    def get_scale_min(self, arg0):
        """Get Scale minimum

        Returns:
            SBYTE
        """
        return self.z48.execute(self.get_scale_min_cmd, (arg0, ))

    def get_scale_max(self, arg0):
        """Get Scale maximum

        Returns:
            SBYTE
        """
        return self.z48.execute(self.get_scale_max_cmd, (arg0, ))

    def get_midi_ctl_output(self, arg0):
        """Get Midi controller output (0: off, 1-128)

        Returns:
            WORD
        """
        return self.z48.execute(self.get_midi_ctl_output_cmd, (arg0, ))

    def get_midi_channel_output(self, arg0):
        """Get Midi channel output (0: off, 1-128)

        Returns:
            SBYTE
        """
        return self.z48.execute(self.get_midi_channel_output_cmd, (arg0, ))

