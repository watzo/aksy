
""" Python equivalent of akai section programtools

Methods to manipulate sampler programs
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Programtools:
    def __init__(self, z48):
        self.sampler = z48
        self.get_no_items_cmd = Command('_', '\x14\x01', 'programtools', 'get_no_items', (), None)
        self.get_handles_cmd = Command('_', '\x14\x02\x00', 'programtools', 'get_handles', (), None)
        self.get_names_cmd = Command('_', '\x14\x02\x01', 'programtools', 'get_names', (), None)
        self.get_handles_names_cmd = Command('_', '\x14\x02\x02', 'programtools', 'get_handles_names', (), None)
        self.get_modified_cmd = Command('_', '\x14\x02\x03', 'programtools', 'get_modified', (), None)
        self.set_curr_by_handle_cmd = Command('_', '\x14\x03', 'programtools', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_curr_by_name_cmd = Command('_', '\x14\x04', 'programtools', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.get_curr_handle_cmd = Command('_', '\x14\x05', 'programtools', 'get_curr_handle', (), None)
        self.get_curr_name_cmd = Command('_', '\x14\x06', 'programtools', 'get_curr_name', (), None)
        self.get_name_by_handle_cmd = Command('_', '\x14\x07', 'programtools', 'get_name_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_handle_by_name_cmd = Command('_', '\x14\x08', 'programtools', 'get_handle_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_all_cmd = Command('_', '\x14\x09', 'programtools', 'delete_all', (), None)
        self.delete_curr_cmd = Command('_', '\x14\x0A', 'programtools', 'delete_curr', (), None)
        self.delete_by_handle_cmd = Command('_', '\x14\x0B', 'programtools', 'delete_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.rename_curr_cmd = Command('_', '\x14\x0C', 'programtools', 'rename_curr', (aksy.devices.akai.sysex_types.STRING,), None)
        self.rename_by_handle_cmd = Command('_', '\x14\x0D', 'programtools', 'rename_by_handle', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.STRING), None)
        self.tag_cmd = Command('_', '\x14\x0E', 'programtools', 'tag', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_tag_bitmap_cmd = Command('_', '\x14\x0F', 'programtools', 'get_tag_bitmap', (), None)
        self.get_modified_name_cmd = Command('_', '\x14\x10', 'programtools', 'get_modified_name', (), None)
        self.get_modified_state_cmd = Command('_', '\x14\x11', 'programtools', 'get_modified_state', (), None)
        self.delete_tagged_cmd = Command('_', '\x14\x18', 'programtools', 'delete_tagged', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.create_new_cmd = Command('_', '\x14\x40', 'programtools', 'create_new', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.STRING), None)
        self.add_keygroups_cmd = Command('_', '\x14\x41', 'programtools', 'add_keygroups', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.delete_keygroup_cmd = Command('_', '\x14\x42', 'programtools', 'delete_keygroup', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.delete_blank_keygroups_cmd = Command('_', '\x14\x43', 'programtools', 'delete_blank_keygroups', (), None)
        self.arrange_keygroups_cmd = Command('_', '\x14\x44', 'programtools', 'arrange_keygroups', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.copy_keygroup_cmd = Command('_', '\x14\x45', 'programtools', 'copy_keygroup', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.copy_cmd = Command('_', '\x14\x48', 'programtools', 'copy', (aksy.devices.akai.sysex_types.STRING,), None)
        self.merge_programs_cmd = Command('_', '\x14\x49', 'programtools', 'merge_programs', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.DWORD), None)
        self.add_keygroup_sample_cmd = Command('_', '\x14\x4A', 'programtools', 'add_keygroup_sample', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL, aksy.devices.akai.sysex_types.STRING), None)
        self.copy_temperament_to_user_cmd = Command('_', '\x14\x50', 'programtools', 'copy_temperament_to_user', (), None)
        self.get_no_modulation_connections_cmd = Command('_', '\x14\x54', 'programtools', 'get_no_modulation_connections', (), None)
        self.get_no_modulation_sources_cmd = Command('_', '\x14\x55', 'programtools', 'get_no_modulation_sources', (), None)
        self.get_no_modulation_destinations_cmd = Command('_', '\x14\x56', 'programtools', 'get_no_modulation_destinations', (), None)
        self.get_name_modulation_source_cmd = Command('_', '\x14\x57', 'programtools', 'get_name_modulation_source', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_name_modulation_dest_cmd = Command('_', '\x14\x58', 'programtools', 'get_name_modulation_dest', (aksy.devices.akai.sysex_types.WORD,), None)
        self.get_group_id_cmd = Command('_', '\x17\x01', 'programtools', 'get_group_id', (), None)
        self.get_type_cmd = Command('_', '\x17\x03', 'programtools', 'get_type', (), None)
        self.get_genre_cmd = Command('_', '\x17\x04', 'programtools', 'get_genre', (), None)
        self.get_program_no_cmd = Command('_', '\x17\x08', 'programtools', 'get_program_no', (), None)
        self.get_no_keygroups_cmd = Command('_', '\x17\x09', 'programtools', 'get_no_keygroups', (), None)
        self.get_keygroup_xfade_cmd = Command('_', '\x17\x0A', 'programtools', 'get_keygroup_xfade', (), None)
        self.get_keygroup_xfade_type_cmd = Command('_', '\x17\x0B', 'programtools', 'get_keygroup_xfade_type', (), None)
        self.get_level_cmd = Command('_', '\x17\x0C', 'programtools', 'get_level', (), None)
        self.get_polyphony_cmd = Command('_', '\x17\x10', 'programtools', 'get_polyphony', (), None)
        self.get_reassignment_method_cmd = Command('_', '\x17\x11', 'programtools', 'get_reassignment_method', (), None)
        self.get_softpedal_loudness_reduction_cmd = Command('_', '\x17\x12', 'programtools', 'get_softpedal_loudness_reduction', (), None)
        self.get_softpedal_attack_stretch_cmd = Command('_', '\x17\x13', 'programtools', 'get_softpedal_attack_stretch', (), None)
        self.get_softpedal_filter_close_cmd = Command('_', '\x17\x14', 'programtools', 'get_softpedal_filter_close', (), None)
        self.get_midi_transpose_cmd = Command('_', '\x17\x15', 'programtools', 'get_midi_transpose', (), None)
        self.get_mpc_pad_assignment_cmd = Command('_', '\x17\x18', 'programtools', 'get_mpc_pad_assignment', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_modulation_connection_cmd = Command('_', '\x17\x20', 'programtools', 'get_modulation_connection', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.get_modulation_source_type_cmd = Command('_', '\x17\x21', 'programtools', 'get_modulation_source_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_modulation_destination_type_cmd = Command('_', '\x17\x22', 'programtools', 'get_modulation_destination_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_modulation_level_cmd = Command('_', '\x17\x23', 'programtools', 'get_modulation_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.get_midi_controller_number_cmd = Command('_', '\x17\x24', 'programtools', 'get_midi_controller_number', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_edit_keygroup_cmd = Command('_', '\x17\x25', 'programtools', 'get_edit_keygroup', (), None)
        self.get_modulation_level_edit_keygroup_cmd = Command('_', '\x17\x26', 'programtools', 'get_modulation_level_edit_keygroup', (), None)
        self.get_tune_cmd = Command('_', '\x17\x30', 'programtools', 'get_tune', (), None)
        self.get_temperament_template_cmd = Command('_', '\x17\x31', 'programtools', 'get_temperament_template', (), None)
        self.get_program_temperament_cmd = Command('_', '\x17\x32', 'programtools', 'get_program_temperament', (), None)
        self.get_key_cmd = Command('_', '\x17\x33', 'programtools', 'get_key', (), None)
        self.get_user_temperament_note_cmd = Command('_', '\x17\x34', 'programtools', 'get_user_temperament_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_pitchbend_up_cmd = Command('_', '\x17\x40', 'programtools', 'get_pitchbend_up', (), None)
        self.get_pitchbend_down_cmd = Command('_', '\x17\x41', 'programtools', 'get_pitchbend_down', (), None)
        self.get_pitchbend_mode_cmd = Command('_', '\x17\x42', 'programtools', 'get_pitchbend_mode', (), None)
        self.get_aftertouch_value_cmd = Command('_', '\x17\x43', 'programtools', 'get_aftertouch_value', (), None)
        self.get_legato_cmd = Command('_', '\x17\x44', 'programtools', 'get_legato', (), None)
        self.get_portamento_enabled_cmd = Command('_', '\x17\x45', 'programtools', 'get_portamento_enabled', (), None)
        self.get_portamento_mode_cmd = Command('_', '\x17\x46', 'programtools', 'get_portamento_mode', (), None)
        self.get_portamento_time_cmd = Command('_', '\x17\x47', 'programtools', 'get_portamento_time', (), None)
        self.get_glissando_mode_cmd = Command('_', '\x17\x48', 'programtools', 'get_glissando_mode', (), None)
        self.get_aftertouch_mode_cmd = Command('_', '\x17\x49', 'programtools', 'get_aftertouch_mode', (), None)
        self.set_group_id_cmd = Command('_', '\x16\x01', 'programtools', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_type_cmd = Command('_', '\x16\x03', 'programtools', 'set_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_genre_cmd = Command('_', '\x16\x04', 'programtools', 'set_genre', (aksy.devices.akai.sysex_types.STRING,), None)
        self.set_program_no_cmd = Command('_', '\x16\x08', 'programtools', 'set_program_no', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_no_keygroups_cmd = Command('_', '\x16\x09', 'programtools', 'set_no_keygroups', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_keygroup_xfade_cmd = Command('_', '\x16\x0A', 'programtools', 'set_keygroup_xfade', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_keygroup_xfade_type_cmd = Command('_', '\x16\x0B', 'programtools', 'set_keygroup_xfade_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_level_cmd = Command('_', '\x16\x0C', 'programtools', 'set_level', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_polyphony_cmd = Command('_', '\x16\x10', 'programtools', 'set_polyphony', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_reassignment_method_cmd = Command('_', '\x16\x11', 'programtools', 'set_reassignment_method', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_softpedal_loudness_reduction_cmd = Command('_', '\x16\x12', 'programtools', 'set_softpedal_loudness_reduction', (), None)
        self.set_softpedal_attack_stretch_cmd = Command('_', '\x16\x13', 'programtools', 'set_softpedal_attack_stretch', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_softpedal_filter_close_cmd = Command('_', '\x16\x14', 'programtools', 'set_softpedal_filter_close', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_midi_transpose_cmd = Command('_', '\x16\x15', 'programtools', 'set_midi_transpose', (aksy.devices.akai.sysex_types.SBYTE,), None)
        self.set_mpc_pad_assignment_cmd = Command('_', '\x16\x18', 'programtools', 'set_mpc_pad_assignment', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_modulation_connection_cmd = Command('_', '\x16\x20', 'programtools', 'set_modulation_connection', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_modulation_source_cmd = Command('_', '\x16\x21', 'programtools', 'set_modulation_source', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_modulation_destination_cmd = Command('_', '\x16\x22', 'programtools', 'set_modulation_destination', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_modulation_level_cmd = Command('_', '\x16\x23', 'programtools', 'set_modulation_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_midi_ctrl_no_cmd = Command('_', '\x16\x24', 'programtools', 'set_midi_ctrl_no', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_edit_keygroup_cmd = Command('_', '\x16\x25', 'programtools', 'set_edit_keygroup', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_edit_kegyroup_modulation_level_cmd = Command('_', '\x16\x26', 'programtools', 'set_edit_kegyroup_modulation_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_tune_cmd = Command('_', '\x16\x30', 'programtools', 'set_tune', (aksy.devices.akai.sysex_types.TUNE,), None)
        self.set_temperament_template_cmd = Command('_', '\x16\x31', 'programtools', 'set_temperament_template', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_program_temperament_cmd = Command('_', '\x16\x32', 'programtools', 'set_program_temperament', (aksy.devices.akai.sysex_types.SBYTE,), None)
        self.set_key_cmd = Command('_', '\x16\x33', 'programtools', 'set_key', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_user_temperament_note_cmd = Command('_', '\x16\x34', 'programtools', 'set_user_temperament_note', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_pitchbend_up_cmd = Command('_', '\x16\x40', 'programtools', 'set_pitchbend_up', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_pitchbend_down_cmd = Command('_', '\x16\x41', 'programtools', 'set_pitchbend_down', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_pitchbend_mode_cmd = Command('_', '\x16\x42', 'programtools', 'set_pitchbend_mode', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_aftertouch_value_cmd = Command('_', '\x16\x43', 'programtools', 'set_aftertouch_value', (aksy.devices.akai.sysex_types.SBYTE,), None)
        self.set_legato_cmd = Command('_', '\x16\x44', 'programtools', 'set_legato', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_portamento_enabled_cmd = Command('_', '\x16\x45', 'programtools', 'set_portamento_enabled', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_portamento_mode_cmd = Command('_', '\x16\x46', 'programtools', 'set_portamento_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_portamento_time_cmd = Command('_', '\x16\x47', 'programtools', 'set_portamento_time', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_glissando_mode_cmd = Command('_', '\x16\x48', 'programtools', 'set_glissando_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_aftertouch_mode_cmd = Command('_', '\x16\x49', 'programtools', 'set_aftertouch_mode', (aksy.devices.akai.sysex_types.BYTE,), None)

    def get_no_items(self):
        """Get number of items in memory
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_handles(self):
        """Get list of info for all items: 0=list of handles;

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_handles_cmd, ())

    def get_names(self):
        """Get list of info for all items: 1=list of names

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_names_cmd, ())

    def get_handles_names(self):
        """Get list of info for all items: 2=list of handle+name;

        Returns:
            HANDLENAMEARRAY
        """
        return self.sampler.execute(self.get_handles_names_cmd, ())

    def get_modified(self):
        """Get list of info for all items: 3=list of handle+modified/tagged name

        Returns:
            HANDLENAMEARRAY
        """
        return self.sampler.execute(self.get_modified_cmd, ())

    def set_curr_by_handle(self, arg0):
        """Select current item by handle
        """
        return self.sampler.execute(self.set_curr_by_handle_cmd, (arg0, ))

    def set_curr_by_name(self, arg0):
        """Select current item by name
        """
        return self.sampler.execute(self.set_curr_by_name_cmd, (arg0, ))

    def get_curr_handle(self):
        """Get handle of current item

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

    def tag(self, arg0, arg1):
        """Set Tag Bit <Data1> = bit to set(0-7), <Data2> = (0=OFF, 1=ON), Data3> = (0=CURRENT, 1=ALL)
        """
        return self.sampler.execute(self.tag_cmd, (arg0, arg1, ))

    def get_tag_bitmap(self):
        """Get Tag Bitmap

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_tag_bitmap_cmd, ())

    def get_modified_name(self):
        """Get name of current item with modified/tagged info.
        """
        return self.sampler.execute(self.get_modified_name_cmd, ())

    def get_modified_state(self):
        """Get modified state of current item.

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_modified_state_cmd, ())

    def delete_tagged(self, arg0):
        """Delete tagged items <Data1> = tag bit
        """
        return self.sampler.execute(self.delete_tagged_cmd, (arg0, ))

    def create_new(self, arg0, arg1):
        """Create New Program <Data1> = number of keygroups;<Data2> = name.
        """
        return self.sampler.execute(self.create_new_cmd, (arg0, arg1, ))

    def add_keygroups(self, arg0):
        """Add Keygroups to Program <Data1> = number of keygroups to add
        """
        return self.sampler.execute(self.add_keygroups_cmd, (arg0, ))

    def delete_keygroup(self, arg0):
        """Delete Keygroup (keygroup index)
        """
        return self.sampler.execute(self.delete_keygroup_cmd, (arg0, ))

    def delete_blank_keygroups(self):
        """Delete Blank Keygroups
        """
        return self.sampler.execute(self.delete_blank_keygroups_cmd, ())

    def arrange_keygroups(self, arg0):
        """Arrange Keygroups (note 0:orig 1:low 2:high)
        """
        return self.sampler.execute(self.arrange_keygroups_cmd, (arg0, ))

    def copy_keygroup(self, arg0):
        """Copy Keygroup (keygroup  index)
        """
        return self.sampler.execute(self.copy_keygroup_cmd, (arg0, ))

    def copy(self, arg0):
        """Copy Program (program name)
        """
        return self.sampler.execute(self.copy_cmd, (arg0, ))

    def merge_programs(self, arg0, arg1):
        """Merge Programs (program handle1, handle2)
        """
        return self.sampler.execute(self.merge_programs_cmd, (arg0, arg1, ))

    def add_keygroup_sample(self, arg0, arg1, arg2, arg3, arg4):
        """Add Keygroup Sample (low note, high note, zone, keytrack, sample name)
        """
        return self.sampler.execute(self.add_keygroup_sample_cmd, (arg0, arg1, arg2, arg3, arg4, ))

    def copy_temperament_to_user(self):
        """Copies Program Temperament to User Temperament
        """
        return self.sampler.execute(self.copy_temperament_to_user_cmd, ())

    def get_no_modulation_connections(self):
        """Get number of Modulation Connections

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_modulation_connections_cmd, ())

    def get_no_modulation_sources(self):
        """Get number of Modulation Sources

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_modulation_sources_cmd, ())

    def get_no_modulation_destinations(self):
        """Get number of Modulation Destinations

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_modulation_destinations_cmd, ())

    def get_name_modulation_source(self, arg0):
        """Get Name of Modulation Source (source index)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_name_modulation_source_cmd, (arg0, ))

    def get_name_modulation_dest(self, arg0):
        """Get Name of Modulation Destination (dest index)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_name_modulation_dest_cmd, (arg0, ))

    def get_group_id(self):
        """Get Group ID

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_group_id_cmd, ())

    def get_type(self):
        """Get Program Type <Reply> = (0=KEYGROUP, 1=DRUM)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_type_cmd, ())

    def get_genre(self):
        """Get Genre

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_genre_cmd, ())

    def get_program_no(self):
        """Get Program Number <Reply1> = (0=OFF, 1=128)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_program_no_cmd, ())

    def get_no_keygroups(self):
        """Get Number of keygroups

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_keygroups_cmd, ())

    def get_keygroup_xfade(self):
        """Get Keygroup Crossfade <Reply1> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_keygroup_xfade_cmd, ())

    def get_keygroup_xfade_type(self):
        """Get Keygroup Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_keygroup_xfade_type_cmd, ())

    def get_level(self):
        """Get Program Level <Reply1> = level in 10 dB

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_level_cmd, ())

    def get_polyphony(self):
        """Get Polyphony

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_polyphony_cmd, ())

    def get_reassignment_method(self):
        """Get Reassignment <Reply1> = (0=QUIETEST, 1=OLDEST)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_reassignment_method_cmd, ())

    def get_softpedal_loudness_reduction(self):
        """Soft Pedal Loudness Reduction

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_softpedal_loudness_reduction_cmd, ())

    def get_softpedal_attack_stretch(self):
        """Soft Pedal Attack Stretch

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_softpedal_attack_stretch_cmd, ())

    def get_softpedal_filter_close(self):
        """Soft Pedal Filter Close

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_softpedal_filter_close_cmd, ())

    def get_midi_transpose(self):
        """Get midi transpose

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_midi_transpose_cmd, ())

    def get_mpc_pad_assignment(self, arg0):
        """Get the midi pad assignment (pad index)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_mpc_pad_assignment_cmd, (arg0, ))

    def get_modulation_connection(self, arg0, arg1):
        """Get the modulation connection(pin number, keygroup for level - note 0 or 'all' is not supported)

        Returns:
            WORD
            WORD
            SBYTE
        """
        return self.sampler.execute(self.get_modulation_connection_cmd, (arg0, arg1, ))

    def get_modulation_source_type(self, arg0):
        """Get the modulation source type (pin number)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_modulation_source_type_cmd, (arg0, ))

    def get_modulation_destination_type(self, arg0):
        """Get the modulation dest type (pin number)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_modulation_destination_type_cmd, (arg0, ))

    def get_modulation_level(self, arg0, arg1):
        """Get the modulation level (pin number, keygroup number - note 0 or 'all' is not supported)

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_modulation_level_cmd, (arg0, arg1, ))

    def get_midi_controller_number(self, arg0):
        """Get the midi controller number (pin number - only available if source=CTRL)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_controller_number_cmd, (arg0, ))

    def get_edit_keygroup(self):
        """Get edit keygroup

        Returns:
            BYTE
            WORD
        """
        return self.sampler.execute(self.get_edit_keygroup_cmd, ())

    def get_modulation_level_edit_keygroup(self):
        """Get Modulation Level of Edit Keygroup

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_modulation_level_edit_keygroup_cmd, ())

    def get_tune(self):
        """Get Cents Tune

        Returns:
            TUNE
        """
        return self.sampler.execute(self.get_tune_cmd, ())

    def get_temperament_template(self):
        """Get Temperament Template, where <Reply1> = template (see Table 22)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_temperament_template_cmd, ())

    def get_program_temperament(self):
        """Get Program Temperament

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_program_temperament_cmd, ())

    def get_key(self):
        """Get Key

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_key_cmd, ())

    def get_user_temperament_note(self, arg0):
        """Get User Temperament Note

        Returns:
            TUNE
        """
        return self.sampler.execute(self.get_user_temperament_note_cmd, (arg0, ))

    def get_pitchbend_up(self):
        """Get Pitch Bend Up

        Returns:
            BYT
        """
        return self.sampler.execute(self.get_pitchbend_up_cmd, ())

    def get_pitchbend_down(self):
        """Get Pitch Bend down

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pitchbend_down_cmd, ())

    def get_pitchbend_mode(self):
        """Get Pitch Bend Mode (normal, held)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pitchbend_mode_cmd, ())

    def get_aftertouch_value(self):
        """Get Aftertouch Value

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_aftertouch_value_cmd, ())

    def get_legato(self):
        """Get Legato Setting (off, pitch, loop

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_legato_cmd, ())

    def get_portamento_enabled(self):
        """Get Portamento Enabled

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_portamento_enabled_cmd, ())

    def get_portamento_mode(self):
        """Get portamento mode (time, rate)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_portamento_mode_cmd, ())

    def get_portamento_time(self):
        """Get portamento time

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_portamento_time_cmd, ())

    def get_glissando_mode(self):
        """Get Glissando Mode

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_glissando_mode_cmd, ())

    def get_aftertouch_mode(self):
        """Get Aftertouch Type

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_aftertouch_mode_cmd, ())

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.sampler.execute(self.set_group_id_cmd, (arg0, ))

    def set_type(self, arg0):
        """Set Program Type <Data1> = (0=KEYGROUP, 1=DRUM)
        """
        return self.sampler.execute(self.set_type_cmd, (arg0, ))

    def set_genre(self, arg0):
        """Set Genre
        """
        return self.sampler.execute(self.set_genre_cmd, (arg0, ))

    def set_program_no(self, arg0):
        """Set Program Number <Data1> = (0=OFF, 1=128)
        """
        return self.sampler.execute(self.set_program_no_cmd, (arg0, ))

    def set_no_keygroups(self, arg0):
        """Set Number of keygroups
        """
        return self.sampler.execute(self.set_no_keygroups_cmd, (arg0, ))

    def set_keygroup_xfade(self, arg0):
        """Set Keygroup Crossfade <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_keygroup_xfade_cmd, (arg0, ))

    def set_keygroup_xfade_type(self, arg0):
        """Set Keygroup Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)
        """
        return self.sampler.execute(self.set_keygroup_xfade_type_cmd, (arg0, ))

    def set_level(self, arg0):
        """Set Program Level <Data1> = level in 10dB (-600 +60)
        """
        return self.sampler.execute(self.set_level_cmd, (arg0, ))

    def set_polyphony(self, arg0):
        """Set Polyphony
        """
        return self.sampler.execute(self.set_polyphony_cmd, (arg0, ))

    def set_reassignment_method(self, arg0):
        """Set Reassignment <Data1> = (0=QUIETEST, 1=OLDEST)
        """
        return self.sampler.execute(self.set_reassignment_method_cmd, (arg0, ))

    def set_softpedal_loudness_reduction(self):
        """Soft Pedal Loudness Reduction
        """
        return self.sampler.execute(self.set_softpedal_loudness_reduction_cmd, ())

    def set_softpedal_attack_stretch(self, arg0):
        """Soft Pedal Attack Stretch
        """
        return self.sampler.execute(self.set_softpedal_attack_stretch_cmd, (arg0, ))

    def set_softpedal_filter_close(self, arg0):
        """Soft Pedal Filter Close
        """
        return self.sampler.execute(self.set_softpedal_filter_close_cmd, (arg0, ))

    def set_midi_transpose(self, arg0):
        """Midi Transpose (-36 +36)
        """
        return self.sampler.execute(self.set_midi_transpose_cmd, (arg0, ))

    def set_mpc_pad_assignment(self, arg0, arg1):
        """MPC pad assignment <Data1> = pad, <Data2> = note
        """
        return self.sampler.execute(self.set_mpc_pad_assignment_cmd, (arg0, arg1, ))

    def set_modulation_connection(self, arg0, arg1, arg2, arg3, arg4):
        """Set Modulation Connection <Data1> = connection (pin) number;<Data2> = keygroup number (0=ALL, 1-128=KEYGROUP) <Data3> = source (see Table 24); <Data4> = destination (see Table 25); <Data5> = level.  If Source or Destination is zero, the connection will be cleared.
        """
        return self.sampler.execute(self.set_modulation_connection_cmd, (arg0, arg1, arg2, arg3, arg4, ))

    def set_modulation_source(self, arg0, arg1):
        """Set Modulation Source (see Table 24)
        """
        return self.sampler.execute(self.set_modulation_source_cmd, (arg0, arg1, ))

    def set_modulation_destination(self, arg0, arg1):
        """Set Modulation Destination (see Table 25)
        """
        return self.sampler.execute(self.set_modulation_destination_cmd, (arg0, arg1, ))

    def set_modulation_level(self, arg0, arg1, arg2):
        """Set Modulation Level <Data1> = pin number; <Data2> = (0=ALL, 1-128=KEYGROUP); <Data3> = level
        """
        return self.sampler.execute(self.set_modulation_level_cmd, (arg0, arg1, arg2, ))

    def set_midi_ctrl_no(self, arg0, arg1):
        """Set MIDI controller number (only used if Source = CTRL)
        """
        return self.sampler.execute(self.set_midi_ctrl_no_cmd, (arg0, arg1, ))

    def set_edit_keygroup(self, arg0, arg1):
        """Set Edit Keygroup (used to edit level) <Data2> = Edit Keygroup
        """
        return self.sampler.execute(self.set_edit_keygroup_cmd, (arg0, arg1, ))

    def set_edit_kegyroup_modulation_level(self, arg0, arg1):
        """Set Modulation Level of Edit Keygroup
        """
        return self.sampler.execute(self.set_edit_kegyroup_modulation_level_cmd, (arg0, arg1, ))

    def set_tune(self, arg0):
        """Set Cents Tune
        """
        return self.sampler.execute(self.set_tune_cmd, (arg0, ))

    def set_temperament_template(self, arg0):
        """Set Temperament Template, where <Data1> = template (see Table 22)
        """
        return self.sampler.execute(self.set_temperament_template_cmd, (arg0, ))

    def set_program_temperament(self, arg0):
        """Set Program Temperament 0=C, 1=C#, 2=D, 3=Eb, 4=E, 5=F, 6=F#, 7=G, 8=G#, 9=A, 10=Bb, 11=B
        """
        return self.sampler.execute(self.set_program_temperament_cmd, (arg0, ))

    def set_key(self, arg0):
        """Set Key 0=C, 1=C#, 2=D, 3=Eb, 4=E, 5=F, 6=F#, 7=G, 8=G#, 9=A, 10=Bb, 11=B
        """
        return self.sampler.execute(self.set_key_cmd, (arg0, ))

    def set_user_temperament_note(self, arg0, arg1):
        """Set User Temperament Note (note, cents)
        """
        return self.sampler.execute(self.set_user_temperament_note_cmd, (arg0, arg1, ))

    def set_pitchbend_up(self, arg0):
        """Set pitchbend up (semitones)
        """
        return self.sampler.execute(self.set_pitchbend_up_cmd, (arg0, ))

    def set_pitchbend_down(self, arg0):
        """Set pitchbend down (semitones)
        """
        return self.sampler.execute(self.set_pitchbend_down_cmd, (arg0, ))

    def set_pitchbend_mode(self, arg0):
        """Set bend mode (held=true)
        """
        return self.sampler.execute(self.set_pitchbend_mode_cmd, (arg0, ))

    def set_aftertouch_value(self, arg0):
        """Set aftertouch value
        """
        return self.sampler.execute(self.set_aftertouch_value_cmd, (arg0, ))

    def set_legato(self, arg0):
        """Set legato setting (off, pitch, loop)
        """
        return self.sampler.execute(self.set_legato_cmd, (arg0, ))

    def set_portamento_enabled(self, arg0):
        """Enable portamento
        """
        return self.sampler.execute(self.set_portamento_enabled_cmd, (arg0, ))

    def set_portamento_mode(self, arg0):
        """Set portamento mode (time, rate)
        """
        return self.sampler.execute(self.set_portamento_mode_cmd, (arg0, ))

    def set_portamento_time(self, arg0):
        """Set portamento time
        """
        return self.sampler.execute(self.set_portamento_time_cmd, (arg0, ))

    def set_glissando_mode(self, arg0):
        """Set glissando mode (portamento, glissando)
        """
        return self.sampler.execute(self.set_glissando_mode_cmd, (arg0, ))

    def set_aftertouch_mode(self, arg0):
        """Set aftertouch (channel, poly)
        """
        return self.sampler.execute(self.set_aftertouch_mode_cmd, (arg0, ))

