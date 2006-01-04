
""" Python equivalent of akai section songtools

Song
"""

__author__ =  'Walco van Loon'
__version__=  "$Rev$"

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Songtools:
    def __init__(self, z48):
        self.z48 = z48
        self.get_no_items_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x01', 'get_no_items', (), None)
        self.get_handles_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x02\x00', 'get_handles', (), None)
        self.get_names_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x02\x01', 'get_names', (), None)
        self.get_handles_names_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x02\x02', 'get_handles_names', (), None)
        self.get_handles_modified_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x02\x03', 'get_handles_modified', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_current_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x03', 'set_current_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_current_by_name_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x04', 'set_current_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.get_current_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x05', 'get_current_handle', (), None)
        self.get_current_name_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x06', 'get_current_name', (), None)
        self.get_name_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x07', 'get_name_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_handle_by_name_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x08', 'get_handle_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_all_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x09', 'delete_all', (), None)
        self.delete_current_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x0A', 'delete_current', (), None)
        self.delete_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x0B', 'delete_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.rename_current_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x0C', 'rename_current', (aksy.devices.akai.sysex_types.STRING,), None)
        self.rename_by_handle_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x0D', 'rename_by_handle', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.STRING), None)
        self.set_tag_bit_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x0E', 'set_tag_bit', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_tag_bitmap_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x0F', 'get_tag_bitmap', (), None)
        self.get_curr_modified_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'get_curr_modified', (), None)
        self.get_modified_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x11 ', 'get_modified', (), None)
        self.delete_tagged_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x18', 'delete_tagged', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.play_song_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x40', 'play_song', (), None)
        self.pause_song_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x41', 'pause_song', (), None)
        self.stop_song_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x42', 'stop_song', (), None)
        self.set_group_id_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x01', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_from_bar_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'set_from_bar', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_to_bar_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'set_to_bar', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_tempo_mode_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x12', 'set_tempo_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_manual_tempo_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x13', 'set_manual_tempo', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_midi_output_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x18', 'set_midi_output', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.get_group_id_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x01', 'get_group_id', (), None)
        self.get_from_bar_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x10', 'get_from_bar', (), None)
        self.get_to_bar_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x11', 'get_to_bar', (), None)
        self.get_tempo_mode_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x12', 'get_tempo_mode', (), None)
        self.get_manual_tempo_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x13', 'get_manual_tempo', (), None)
        self.get_midi_output_port_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x18', 'get_midi_output_port', (), None)
        self.get_time_signature_beat_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x20', 'get_time_signature_beat', (), None)
        self.get_time_sig_beat_no_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x21', 'get_time_sig_beat_no', (), None)
        self.get_curr_beat_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x22', 'get_curr_beat', (), None)
        self.get_curr_bar_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x23', 'get_curr_bar', (), None)
        self.get_curr_tempo_cmd = aksy.devices.akai.sysex.Command('_', '\x28\x24', 'get_curr_tempo', (), None)

    def get_no_items(self):
        """Get number of items in memory

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_no_items_cmd, ())

    def get_handles(self):
        """Get Sample handles
        """
        return self.z48.execute(self.get_handles_cmd, ())

    def get_names(self):
        """Get sample names

        Returns:
            aksy.devices.akai.sysex_types.STRINGARRAY
        """
        return self.z48.execute(self.get_names_cmd, ())

    def get_handles_names(self):
        """Get list of sample handles and names

        Returns:
            aksy.devices.akai.sysex_types.HANDLENAMEARRAY
        """
        return self.z48.execute(self.get_handles_names_cmd, ())

    def get_handles_modified(self, arg0):
        """Get a list of modified/tagged samples
        """
        return self.z48.execute(self.get_handles_modified_cmd, (arg0, ))

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

    def set_tag_bit(self, arg0, arg1):
        """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) BYTE(0, 1) <Data3> = (0=CURRENT, 1=ALL)
        """
        return self.z48.execute(self.set_tag_bit_cmd, (arg0, arg1, ))

    def get_tag_bitmap(self):
        """Get Tag Bitmap
        """
        return self.z48.execute(self.get_tag_bitmap_cmd, ())

    def get_curr_modified(self):
        """Get name of current item with modified/tagged info

        Returns:
            aksy.devices.akai.sysex_types.STRINGARRAY
        """
        return self.z48.execute(self.get_curr_modified_cmd, ())

    def get_modified(self):
        """Get modified state of current item.

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_modified_cmd, ())

    def delete_tagged(self, arg0):
        """Delete tagged items <Data1> = tag bit
        """
        return self.z48.execute(self.delete_tagged_cmd, (arg0, ))

    def play_song(self):
        """Play Song
        """
        return self.z48.execute(self.play_song_cmd, ())

    def pause_song(self):
        """Pause Song
        """
        return self.z48.execute(self.pause_song_cmd, ())

    def stop_song(self):
        """Stop Song
        """
        return self.z48.execute(self.stop_song_cmd, ())

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.z48.execute(self.set_group_id_cmd, (arg0, ))

    def set_from_bar(self, arg0):
        """Set From Bar
        """
        return self.z48.execute(self.set_from_bar_cmd, (arg0, ))

    def set_to_bar(self, arg0):
        """Set To Bar
        """
        return self.z48.execute(self.set_to_bar_cmd, (arg0, ))

    def set_tempo_mode(self, arg0):
        """Set Tempo Mode <Data1> = (0=FILE, 1=MANUAL, 2=MULTI)
        """
        return self.z48.execute(self.set_tempo_mode_cmd, (arg0, ))

    def set_manual_tempo(self, arg0):
        """Set Manual Tempo <Data1> = (tempo×10)bpm
        """
        return self.z48.execute(self.set_manual_tempo_cmd, (arg0, ))

    def set_midi_output(self, arg0):
        """Set MIDI output port <Data1> = (0=NONE, 1=MIDI A, 2=MIDI B)
        """
        return self.z48.execute(self.set_midi_output_cmd, (arg0, ))

    def get_group_id(self):
        """Get Group ID

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_group_id_cmd, ())

    def get_from_bar(self):
        """Get From Bar

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_from_bar_cmd, ())

    def get_to_bar(self):
        """Get To Bar

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_to_bar_cmd, ())

    def get_tempo_mode(self):
        """Get Tempo Mode <Reply> = (0=FILE, 1=MANUAL, 2=MULTI)

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_tempo_mode_cmd, ())

    def get_manual_tempo(self):
        """Get Manual Tempo

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_manual_tempo_cmd, ())

    def get_midi_output_port(self):
        """Get MIDI output port <Reply> = (0=NONE, 1=MIDI A, 2=MIDI B

        Returns:
            aksy.devices.akai.sysex_types.BOOL
        """
        return self.z48.execute(self.get_midi_output_port_cmd, ())

    def get_time_signature_beat(self):
        """Get (Time Signature) Beat Value

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_time_signature_beat_cmd, ())

    def get_time_sig_beat_no(self):
        """Get (Time Signature) Beats-per-Bar

        Returns:
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.z48.execute(self.get_time_sig_beat_no_cmd, ())

    def get_curr_beat(self):
        """Get Current Beat

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_curr_beat_cmd, ())

    def get_curr_bar(self):
        """Get Current Bar

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_curr_bar_cmd, ())

    def get_curr_tempo(self):
        """Get Current Tempo <Reply> = (tempo×10)bpm

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.z48.execute(self.get_curr_tempo_cmd, ())

