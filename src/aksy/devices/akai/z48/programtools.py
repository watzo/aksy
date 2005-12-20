
""" Python equivalent of akai section programtools

Methods to manipulate sampler programs
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Programtools:
    def __init__(self, z48):
        self.z48 = z48
        self.get_no_items_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x01', 'get_no_items', (), None)
        self.get_handles_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x02\x00', 'get_handles', (), None)
        self.get_names_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x02\x01', 'get_names', (), None)
        self.get_handles_names_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x02\x02', 'get_handles_names', (), None)
        self.get_modified_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x02\x03', 'get_modified', (), None)
        self.set_current_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x03', 'set_current_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_current_by_name_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x04', 'set_current_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.get_current_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x05', 'get_current_handle', (), None)
        self.get_current_name_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x06', 'get_current_name', (), None)
        self.get_name_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x07', 'get_name_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_handle_by_name_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x08', 'get_handle_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_all_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x09', 'delete_all', (), None)
        self.delete_current_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x0A', 'delete_current', (), None)
        self.delete_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x0B', 'delete_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.rename_current_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x0C', 'rename_current', (aksy.devices.akai.sysex_types.STRING,), None)
        self.rename_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x0D', 'rename_by_handle', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.STRING), None)
        self.tag_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x0E', 'tag', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_tag_bitmap_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x0F', 'get_tag_bitmap', (), None)
        self.get_modified_name_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x10', 'get_modified_name', (), None)
        self.get_modified_state_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x11', 'get_modified_state', (), None)
        self.delete_tagged_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x18', 'delete_tagged', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.create_new_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x40', 'create_new', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.STRING), None)
        self.add_keygroups_to_current_cmd = aksy.devices.akai.sysex.Command('_', '\x14\x41', 'add_keygroups_to_current', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_group_id_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x01', 'get_group_id', (), None)
        self.get_type_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x03', 'get_type', (), None)
        self.get_genre_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x04', 'get_genre', (), None)
        self.get_program_no_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x08', 'get_program_no', (), None)
        self.get_no_keygroups_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x09', 'get_no_keygroups', (), None)
        self.get_keygroup_xfade_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x0A', 'get_keygroup_xfade', (), None)
        self.get_keygroup_xfade_type_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x0B', 'get_keygroup_xfade_type', (), None)
        self.get_level_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x0C', 'get_level', (), None)
        self.get_polyphony_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x10', 'get_polyphony', (), None)
        self.get_reassignment_method_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x11', 'get_reassignment_method', (), None)
        self.get_softpedal_loudness_reduction_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x12', 'get_softpedal_loudness_reduction', (), None)
        self.get_softpedal_attack_stretch_cmd = aksy.devices.akai.sysex.Command('_', '\x17\x13', 'get_softpedal_attack_stretch', (), None)
        self.set_group_id_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x01', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_type_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x03', 'set_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_genre_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x04', 'set_genre', (aksy.devices.akai.sysex_types.STRING,), None)
        self.set_program_no_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x08', 'set_program_no', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_no_keygroups_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x09', 'set_no_keygroups', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_keygroup_xfade_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x0A', 'set_keygroup_xfade', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_keygroup_xfade_type_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x0B', 'set_keygroup_xfade_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_level_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x0C', 'set_level', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_polyphony_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x10', 'set_polyphony', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_reassignment_method_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x11', 'set_reassignment_method', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_softpedal_loudness_reduction_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x12', 'set_softpedal_loudness_reduction', (), None)
        self.set_softpedal_attack_stretch_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x13', 'set_softpedal_attack_stretch', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_softpedal_filter_close_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x14', 'set_softpedal_filter_close', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_midi_transpose_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x15', 'set_midi_transpose', (aksy.devices.akai.sysex_types.SBYTE,), None)
        self.set_mpc_pad_assignment_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x18', 'set_mpc_pad_assignment', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_modulation_conn_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x20', 'set_modulation_conn', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_modulation_src_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x21', 'set_modulation_src', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_modulation_dest_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x22', 'set_modulation_dest', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_modulation_level_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x23', 'set_modulation_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_midi_ctrl_no_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x24', 'set_midi_ctrl_no', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_edit_keygroup_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x25', 'set_edit_keygroup', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_edit_kegyroup_modulation_level_cmd = aksy.devices.akai.sysex.Command('_', '\x16\x26', 'set_edit_kegyroup_modulation_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)

    def get_no_items(self):
        """Get number of items in memory
        """
        return self.z48.execute(self.get_no_items_cmd, ())

    def get_handles(self):
        """Get list of info for all items: 0=list of handles;

        Returns:
            aksy.devices.akai.sysex_types.DWORD
        """
        return self.z48.execute(self.get_handles_cmd, ())

    def get_names(self):
        """Get list of info for all items: 1=list of names

        Returns:
            aksy.devices.akai.sysex_types.STRINGARRAY
        """
        return self.z48.execute(self.get_names_cmd, ())

    def get_handles_names(self):
        """Get list of info for all items: 2=list of handle+name;

        Returns:
            aksy.devices.akai.sysex_types.HANDLENAMEARRAY
        """
        return self.z48.execute(self.get_handles_names_cmd, ())

    def get_modified(self):
        """Get list of info for all items: 3=list of handle+modified/tagged name

        Returns:
            aksy.devices.akai.sysex_types.HANDLENAMEARRAY
        """
        return self.z48.execute(self.get_modified_cmd, ())

    def set_current_by_handle(self, arg0):
        """Select current item by handle
        """
        return self.z48.execute(self.set_current_by_handle_cmd, (arg0, ))

    def set_current_by_name(self, arg0):
        """Select current item by name
        """
        return self.z48.execute(self.set_current_by_name_cmd, (arg0, ))

    def get_current_handle(self):
        """Get handle of current item

        Returns:
            aksy.devices.akai.sysex_types.DWORD
        """
        return self.z48.execute(self.get_current_handle_cmd, ())

    def get_current_name(self):
        """Get name of current item

        Returns:
            aksy.devices.akai.sysex_types.STRING
        """
        return self.z48.execute(self.get_current_name_cmd, ())

    def get_name_by_handle(self, arg0):
        """Get item name from handle

        Returns:
            aksy.devices.akai.sysex_types.STRING
        """
        return self.z48.execute(self.get_name_by_handle_cmd, (arg0, ))

    def get_handle_by_name(self, arg0):
        """Get item handle from name

        Returns:
            aksy.devices.akai.sysex_types.DWORD
        """
        return self.z48.execute(self.get_handle_by_name_cmd, (arg0, ))

    def delete_all(self):
        """Delete ALL items from memory
        """
        return self.z48.execute(self.delete_all_cmd, ())

    def delete_current(self):
        """Delete current item from memory
        """
        return self.z48.execute(self.delete_current_cmd, ())

    def delete_by_handle(self, arg0):
        """Delete item represented by handle <Data1>
        """
        return self.z48.execute(self.delete_by_handle_cmd, (arg0, ))

    def rename_current(self, arg0):
        """Rename current item
        """
        return self.z48.execute(self.rename_current_cmd, (arg0, ))

    def rename_by_handle(self, arg0, arg1):
        """Rename item represented by handle <Data1>
        """
        return self.z48.execute(self.rename_by_handle_cmd, (arg0, arg1, ))

    def tag(self, arg0, arg1):
        """Set Tag Bit <Data1> = bit to set(0-7), <Data2> = (0=OFF, 1=ON), Data3> = (0=CURRENT, 1=ALL)
        """
        return self.z48.execute(self.tag_cmd, (arg0, arg1, ))

    def get_tag_bitmap(self):
        """Get Tag Bitmap

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_tag_bitmap_cmd, ())

    def get_modified_name(self):
        """Get name of current item with modified/tagged info.
        """
        return self.z48.execute(self.get_modified_name_cmd, ())

    def get_modified_state(self):
        """Get modified state of current item.

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_modified_state_cmd, ())

    def delete_tagged(self, arg0):
        """Delete tagged items <Data1> = tag bit
        """
        return self.z48.execute(self.delete_tagged_cmd, (arg0, ))

    def create_new(self, arg0, arg1):
        """Create New Program <Data1> = number of keygroups;<Data2> = name.
        """
        return self.z48.execute(self.create_new_cmd, (arg0, arg1, ))

    def add_keygroups_to_current(self, arg0):
        """Add Keygroups to Program <Data1> = number of keygroups to add
        """
        return self.z48.execute(self.add_keygroups_to_current_cmd, (arg0, ))

    def get_group_id(self):
        """Get Group ID

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_group_id_cmd, ())

    def get_type(self):
        """Get Program Type <Reply> = (0=KEYGROUP, 1=DRUM)

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_type_cmd, ())

    def get_genre(self):
        """Get Genre

        Returns:
            aksy.devices.akai.sysex_types.STRING
        """
        return self.z48.execute(self.get_genre_cmd, ())

    def get_program_no(self):
        """Get Program Number <Reply1> = (0=OFF, 1­128)

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_program_no_cmd, ())

    def get_no_keygroups(self):
        """Get Number of keygroups

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_no_keygroups_cmd, ())

    def get_keygroup_xfade(self):
        """Get Keygroup Crossfade <Reply1> = (0=OFF, 1=ON)

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_keygroup_xfade_cmd, ())

    def get_keygroup_xfade_type(self):
        """Get Keygroup Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_keygroup_xfade_type_cmd, ())

    def get_level(self):
        """Get Program Level <Reply1> = level in 10×dB

        Returns:
            aksy.devices.akai.sysex_types.SWORD
        """
        return self.z48.execute(self.get_level_cmd, ())

    def get_polyphony(self):
        """Get Polyphony

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_polyphony_cmd, ())

    def get_reassignment_method(self):
        """Get Reassignment <Reply1> = (0=QUIETEST, 1=OLDEST)

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_reassignment_method_cmd, ())

    def get_softpedal_loudness_reduction(self):
        """Soft Pedal Loudness Reduction

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_softpedal_loudness_reduction_cmd, ())

    def get_softpedal_attack_stretch(self):
        """Soft Pedal Attack Stretch

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_softpedal_attack_stretch_cmd, ())

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.z48.execute(self.set_group_id_cmd, (arg0, ))

    def set_type(self, arg0):
        """Set Program Type <Data1> = (0=KEYGROUP, 1=DRUM)
        """
        return self.z48.execute(self.set_type_cmd, (arg0, ))

    def set_genre(self, arg0):
        """Set Genre
        """
        return self.z48.execute(self.set_genre_cmd, (arg0, ))

    def set_program_no(self, arg0):
        """Set Program Number <Data1> = (0=OFF, 1­128)
        """
        return self.z48.execute(self.set_program_no_cmd, (arg0, ))

    def set_no_keygroups(self, arg0):
        """Set Number of keygroups
        """
        return self.z48.execute(self.set_no_keygroups_cmd, (arg0, ))

    def set_keygroup_xfade(self, arg0):
        """Set Keygroup Crossfade <Data1> = (0=OFF, 1=ON)
        """
        return self.z48.execute(self.set_keygroup_xfade_cmd, (arg0, ))

    def set_keygroup_xfade_type(self, arg0):
        """Set Keygroup Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)
        """
        return self.z48.execute(self.set_keygroup_xfade_type_cmd, (arg0, ))

    def set_level(self, arg0):
        """Set Program Level <Data1> = level in 10×dB (-600 ­ +60)
        """
        return self.z48.execute(self.set_level_cmd, (arg0, ))

    def set_polyphony(self, arg0):
        """Set Polyphony
        """
        return self.z48.execute(self.set_polyphony_cmd, (arg0, ))

    def set_reassignment_method(self, arg0):
        """Set Reassignment <Data1> = (0=QUIETEST, 1=OLDEST)
        """
        return self.z48.execute(self.set_reassignment_method_cmd, (arg0, ))

    def set_softpedal_loudness_reduction(self):
        """Soft Pedal Loudness Reduction
        """
        return self.z48.execute(self.set_softpedal_loudness_reduction_cmd, ())

    def set_softpedal_attack_stretch(self, arg0):
        """Soft Pedal Attack Stretch
        """
        return self.z48.execute(self.set_softpedal_attack_stretch_cmd, (arg0, ))

    def set_softpedal_filter_close(self, arg0):
        """Soft Pedal Filter Close
        """
        return self.z48.execute(self.set_softpedal_filter_close_cmd, (arg0, ))

    def set_midi_transpose(self, arg0):
        """Midi Transpose (-36 ­ +36)
        """
        return self.z48.execute(self.set_midi_transpose_cmd, (arg0, ))

    def set_mpc_pad_assignment(self, arg0, arg1):
        """MPC pad assignment <Data1> = pad, <Data2> = note
        """
        return self.z48.execute(self.set_mpc_pad_assignment_cmd, (arg0, arg1, ))

    def set_modulation_conn(self, arg0, arg1, arg2, arg3, arg4):
        """Set Modulation Connection <Data1> = connection (pin) number;<Data2> = keygroup number (0=ALL, 1­128=KEYGROUP) <Data3> = source (see Table 24); <Data4> = destination (see Table 25); <Data5> = level.  If Source or Destination is zero, the connection will be cleared.
        """
        return self.z48.execute(self.set_modulation_conn_cmd, (arg0, arg1, arg2, arg3, arg4, ))

    def set_modulation_src(self, arg0, arg1):
        """Set Modulation Source (see Table 24)
        """
        return self.z48.execute(self.set_modulation_src_cmd, (arg0, arg1, ))

    def set_modulation_dest(self, arg0, arg1):
        """Set Modulation Destination (see Table 25)
        """
        return self.z48.execute(self.set_modulation_dest_cmd, (arg0, arg1, ))

    def set_modulation_level(self, arg0, arg1, arg2):
        """Set Modulation Level <Data1> = pin number; <Data2> = (0=ALL, 1­128=KEYGROUP); <Data3> = level
        """
        return self.z48.execute(self.set_modulation_level_cmd, (arg0, arg1, arg2, ))

    def set_midi_ctrl_no(self, arg0, arg1):
        """Set MIDI controller number (only used if Source = CTRL)
        """
        return self.z48.execute(self.set_midi_ctrl_no_cmd, (arg0, arg1, ))

    def set_edit_keygroup(self, arg0, arg1):
        """Set Edit Keygroup (used to edit level) <Data2> = Edit Keygroup
        """
        return self.z48.execute(self.set_edit_keygroup_cmd, (arg0, arg1, ))

    def set_edit_kegyroup_modulation_level(self, arg0, arg1):
        """Set Modulation Level of Edit Keygroup
        """
        return self.z48.execute(self.set_edit_kegyroup_modulation_level_cmd, (arg0, arg1, ))

