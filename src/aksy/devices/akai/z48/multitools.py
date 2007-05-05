
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
        self.set_group_id_cmd = Command('_', '\x1A\x01', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_select_method_cmd = Command('_', '\x1A\x02', 'set_multi_select_method', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_select_channel_cmd = Command('_', '\x1A\x03', 'set_multi_select_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_tempo_cmd = Command('_', '\x1A\x04', 'set_multi_tempo', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_multi_program_no_cmd = Command('_', '\x1A\x08', 'set_multi_program_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_multi_part_by_handle_cmd = Command('_', '\x1A\x09', 'set_multi_part_by_handle', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.DWORD), None)

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

