
""" Python equivalent of akai section sampletools

Sample
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Sampletools:
    def __init__(self, z48):
        self.sampler = z48
        self.get_no_items_cmd = Command('_', '\x1C\x01', 'sampletools', 'get_no_items', (), None)
        self.get_handles_cmd = Command('_', '\x1C\x02\x00', 'sampletools', 'get_handles', (), None)
        self.get_names_cmd = Command('_', '\x1C\x02\x01', 'sampletools', 'get_names', (), None)
        self.get_handles_names_cmd = Command('_', '\x1C\x02\x02', 'sampletools', 'get_handles_names', (), None)
        self.get_handles_modified_cmd = Command('_', '\x1C\x02\x03', 'sampletools', 'get_handles_modified', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_curr_by_handle_cmd = Command('_', '\x1C\x03', 'sampletools', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_curr_by_name_cmd = Command('_', '\x1C\x04', 'sampletools', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.get_curr_handle_cmd = Command('_', '\x1C\x05', 'sampletools', 'get_curr_handle', (), None)
        self.get_curr_name_cmd = Command('_', '\x1C\x06', 'sampletools', 'get_curr_name', (), None)
        self.get_name_by_handle_cmd = Command('_', '\x1C\x07', 'sampletools', 'get_name_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.get_handle_by_name_cmd = Command('_', '\x1C\x08', 'sampletools', 'get_handle_by_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.delete_all_cmd = Command('_', '\x1C\x09', 'sampletools', 'delete_all', (), None)
        self.delete_curr_cmd = Command('_', '\x1C\x0A', 'sampletools', 'delete_curr', (), None)
        self.delete_by_handle_cmd = Command('_', '\x1C\x0B', 'sampletools', 'delete_by_handle', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.rename_curr_cmd = Command('_', '\x1C\x0C', 'sampletools', 'rename_curr', (aksy.devices.akai.sysex_types.STRING,), None)
        self.rename_by_handle_cmd = Command('_', '\x1C\x0D', 'sampletools', 'rename_by_handle', (aksy.devices.akai.sysex_types.DWORD, aksy.devices.akai.sysex_types.STRING), None)
        self.set_tag_bit_cmd = Command('_', '\x1C\x0E', 'sampletools', 'set_tag_bit', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_tag_bitmap_cmd = Command('_', '\x1C\x0F', 'sampletools', 'get_tag_bitmap', (), None)
        self.get_curr_modified_cmd = Command('_', '\x1C\x10', 'sampletools', 'get_curr_modified', (), None)
        self.get_modified_cmd = Command('_', '\x1C\x11', 'sampletools', 'get_modified', (), None)
        self.delete_tagged_cmd = Command('_', '\x1C\x18', 'sampletools', 'delete_tagged', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.play_cmd = Command('_', '\x1C\x40', 'sampletools', 'play', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.stop_cmd = Command('_', '\x1C\x41', 'sampletools', 'stop', (), None)
        self.play_until_cmd = Command('_', '\x1C\x42', 'sampletools', 'play_until', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.play_from_cmd = Command('_', '\x1C\x43', 'sampletools', 'play_from', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.play_over_cmd = Command('_', '\x1C\x44', 'sampletools', 'play_over', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.play_loop_cmd = Command('_', '\x1C\x45', 'sampletools', 'play_loop', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.play_region_cmd = Command('_', '\x1C\x46', 'sampletools', 'play_region', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.create_loop_cmd = Command('_', '\x1C\x48', 'sampletools', 'create_loop', (), None)
        self.delete_loop_cmd = Command('_', '\x1C\x49', 'sampletools', 'delete_loop', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.create_region_cmd = Command('_', '\x1C\x4A', 'sampletools', 'create_region', (), None)
        self.delete_region_cmd = Command('_', '\x1C\x4B', 'sampletools', 'delete_region', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_group_id_cmd = Command('_', '\x1F\x01', 'sampletools', 'get_group_id', (), None)
        self.get_trim_start_cmd = Command('_', '\x1F\x20', 'sampletools', 'get_trim_start', (), None)
        self.get_trim_end_cmd = Command('_', '\x1F\x21', 'sampletools', 'get_trim_end', (), None)
        self.get_trim_length_cmd = Command('_', '\x1F\x22', 'sampletools', 'get_trim_length', (), None)
        self.get_orig_pitch_cmd = Command('_', '\x1F\x24', 'sampletools', 'get_orig_pitch', (), None)
        self.get_cents_tune_cmd = Command('_', '\x1F\x25', 'sampletools', 'get_cents_tune', (), None)
        self.get_playback_mode_cmd = Command('_', '\x1F\x26', 'sampletools', 'get_playback_mode', (), None)
        self.get_loop_start_cmd = Command('_', '\x1F\x30', 'sampletools', 'get_loop_start', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_loop_end_cmd = Command('_', '\x1F\x31', 'sampletools', 'get_loop_end', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_loop_length_cmd = Command('_', '\x1F\x32', 'sampletools', 'get_loop_length', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_loop_lock_cmd = Command('_', '\x1F\x33', 'sampletools', 'get_loop_lock', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.get_loop_tune_cmd = Command('_', '\x1F\x34', 'sampletools', 'get_loop_tune', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_loop_dir_cmd = Command('_', '\x1F\x35', 'sampletools', 'get_loop_dir', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.get_loop_type_cmd = Command('_', '\x1F\x36', 'sampletools', 'get_loop_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_no_loop_reps_cmd = Command('_', '\x1F\x37', 'sampletools', 'get_no_loop_reps', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_no_loops_cmd = Command('_', '\x1F\x38', 'sampletools', 'get_no_loops', (), None)
        self.get_region_start_cmd = Command('_', '\x1F\x40', 'sampletools', 'get_region_start', (), None)
        self.get_region_end_cmd = Command('_', '\x1F\x41', 'sampletools', 'get_region_end', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_region_length_cmd = Command('_', '\x1F\x42', 'sampletools', 'get_region_length', (), None)
        self.get_no_regions_cmd = Command('_', '\x1F\x44', 'sampletools', 'get_no_regions', (), None)
        self.get_sample_length_cmd = Command('_', '\x1F\x50', 'sampletools', 'get_sample_length', (), None)
        self.get_sample_rate_cmd = Command('_', '\x1F\x51', 'sampletools', 'get_sample_rate', (), None)
        self.get_bit_depth_cmd = Command('_', '\x1F\x52', 'sampletools', 'get_bit_depth', (), None)
        self.get_sample_type_cmd = Command('_', '\x1F\x54', 'sampletools', 'get_sample_type', (), None)
        self.get_no_channels_cmd = Command('_', '\x1F\x55', 'sampletools', 'get_no_channels', (), None)
        self.set_group_id_cmd = Command('_', '\x1E\x01', 'sampletools', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_trim_start_cmd = Command('_', '\x1E\x20', 'sampletools', 'set_trim_start', (aksy.devices.akai.sysex_types.QWORD,), None)
        self.set_trim_end_cmd = Command('_', '\x1E\x21', 'sampletools', 'set_trim_end', (aksy.devices.akai.sysex_types.QWORD,), None)
        self.set_trim_length_cmd = Command('_', '\x1E\x22', 'sampletools', 'set_trim_length', (aksy.devices.akai.sysex_types.QWORD,), None)
        self.set_orig_pitch_cmd = Command('_', '\x1E\x24', 'sampletools', 'set_orig_pitch', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_tune_cmd = Command('_', '\x1E\x25', 'sampletools', 'set_tune', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_playback_mode_cmd = Command('_', '\x1E\x26', 'sampletools', 'set_playback_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_loop_start_cmd = Command('_', '\x1E\x30', 'sampletools', 'set_loop_start', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.set_loop_end_cmd = Command('_', '\x1E\x31', 'sampletools', 'set_loop_end', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.set_loop_length_cmd = Command('_', '\x1E\x32', 'sampletools', 'set_loop_length', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.set_loop_lock_cmd = Command('_', '\x1E\x33', 'sampletools', 'set_loop_lock', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_loop_tune_cmd = Command('_', '\x1E\x34', 'sampletools', 'set_loop_tune', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_loop_direction_cmd = Command('_', '\x1E\x35', 'sampletools', 'set_loop_direction', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_loop_type_cmd = Command('_', '\x1E\x36', 'sampletools', 'set_loop_type', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_no_loop_reps_cmd = Command('_', '\x1E\x37', 'sampletools', 'set_no_loop_reps', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_region_start_cmd = Command('_', '\x1E\x40', 'sampletools', 'set_region_start', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.set_region_end_cmd = Command('_', '\x1E\x41', 'sampletools', 'set_region_end', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)
        self.set_region_length_cmd = Command('_', '\x1E\x42', 'sampletools', 'set_region_length', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.QWORD), None)

    def get_no_items(self):
        """Get number of items in memory

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_handles(self):
        """Get Sample handles
        """
        return self.sampler.execute(self.get_handles_cmd, ())

    def get_names(self):
        """Get sample names

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_names_cmd, ())

    def get_handles_names(self):
        """Get list of sample handles and names

        Returns:
            HANDLENAMEARRAY
        """
        return self.sampler.execute(self.get_handles_names_cmd, ())

    def get_handles_modified(self, arg0):
        """Get a list of modified/tagged samples

        Returns:
            HANDLENAMEARRAY
        """
        return self.sampler.execute(self.get_handles_modified_cmd, (arg0, ))

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

    def set_tag_bit(self, arg0, arg1):
        """Set Tag Bit <Data1> = bit to set, <Data2> = (0=OFF, 1=ON) BYTE(0, 1) <Data3> = (0=CURRENT, 1=ALL)
        """
        return self.sampler.execute(self.set_tag_bit_cmd, (arg0, arg1, ))

    def get_tag_bitmap(self):
        """Get Tag Bitmap
        """
        return self.sampler.execute(self.get_tag_bitmap_cmd, ())

    def get_curr_modified(self):
        """Get name of current item with modified/tagged info

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_curr_modified_cmd, ())

    def get_modified(self):
        """Get modified state of current item.

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_modified_cmd, ())

    def delete_tagged(self, arg0):
        """Delete tagged items <Data1> = tag bit
        """
        return self.sampler.execute(self.delete_tagged_cmd, (arg0, ))

    def play(self, arg0, arg1):
        """Start auditioning the current sample <Data1> = velocity <Data2> =(NO LOOPING, 1=LOOPING)
        """
        return self.sampler.execute(self.play_cmd, (arg0, arg1, ))

    def stop(self):
        """Stop playback of the current sample
        """
        return self.sampler.execute(self.stop_cmd, ())

    def play_until(self, arg0, arg1):
        """Play To <Data1> = velocity, <Data2> = sample position
        """
        return self.sampler.execute(self.play_until_cmd, (arg0, arg1, ))

    def play_from(self, arg0, arg1):
        """Play From <Data1> = velocity, <Data2> = sample position
        """
        return self.sampler.execute(self.play_from_cmd, (arg0, arg1, ))

    def play_over(self, arg0, arg1):
        """Play Over <Data1> = velocity, <Data2> = sample position
        """
        return self.sampler.execute(self.play_over_cmd, (arg0, arg1, ))

    def play_loop(self, arg0, arg1):
        """Play Loop <Data1> = velocity, <Data2> = loop index
        """
        return self.sampler.execute(self.play_loop_cmd, (arg0, arg1, ))

    def play_region(self, arg0, arg1):
        """Play Region <Data1> = velocity, <Data2> = region index
        """
        return self.sampler.execute(self.play_region_cmd, (arg0, arg1, ))

    def create_loop(self):
        """Create New Loop
        """
        return self.sampler.execute(self.create_loop_cmd, ())

    def delete_loop(self, arg0):
        """Delete Loop <Data1> = index
        """
        return self.sampler.execute(self.delete_loop_cmd, (arg0, ))

    def create_region(self):
        """Create Region
        """
        return self.sampler.execute(self.create_region_cmd, ())

    def delete_region(self, arg0):
        """Delete Region <Data1> = index
        """
        return self.sampler.execute(self.delete_region_cmd, (arg0, ))

    def get_group_id(self):
        """Get Group ID

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_group_id_cmd, ())

    def get_trim_start(self):
        """Get Trim Start

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_trim_start_cmd, ())

    def get_trim_end(self):
        """Get Trim End

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_trim_end_cmd, ())

    def get_trim_length(self):
        """Get Trim Length

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_trim_length_cmd, ())

    def get_orig_pitch(self):
        """Get Original Pitch

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_orig_pitch_cmd, ())

    def get_cents_tune(self):
        """Get Cents Tune (+-3600)

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_cents_tune_cmd, ())

    def get_playback_mode(self):
        """Get Playback Mode, where <Data1> = (0=NO LOOPING, 1=LOOPING, 2=ONE SHOT)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_playback_mode_cmd, ())

    def get_loop_start(self, arg0):
        """Get Loop Start <Data1> = loop index

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_loop_start_cmd, (arg0, ))

    def get_loop_end(self, arg0):
        """Get Loop End <Data1> = loop index

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_loop_end_cmd, (arg0, ))

    def get_loop_length(self, arg0):
        """Get Loop Length <Data1> = loop index

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_loop_length_cmd, (arg0, ))

    def get_loop_lock(self, arg0):
        """Get Loop Lock <Data1> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_loop_lock_cmd, (arg0, ))

    def get_loop_tune(self, arg0):
        """Get Loop Tune (+-50)

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_loop_tune_cmd, (arg0, ))

    def get_loop_dir(self, arg0):
        """Get Loop Direction <Data1> = (0=FORWARDS, 1=ALTERNATING)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_loop_dir_cmd, (arg0, ))

    def get_loop_type(self, arg0):
        """Get Loop Type <Data1> = (0=LOOP IN REL, 1=LOOP UNTIL REL)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_loop_type_cmd, (arg0, ))

    def get_no_loop_reps(self, arg0):
        """Get Number of Loop Repetitions

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_loop_reps_cmd, (arg0, ))

    def get_no_loops(self):
        """Get Number of Loops

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_loops_cmd, ())

    def get_region_start(self):
        """Get Region Start <Data1> = Region Num (0-31), <Reply1> = start

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_region_start_cmd, ())

    def get_region_end(self, arg0):
        """Get Region End <Data1> = Region Num (0-31) <Reply1> = end

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_region_end_cmd, (arg0, ))

    def get_region_length(self):
        """Get Region Length <Data1> = Region Num (0-31) <Reply1> = length BYTE

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_region_length_cmd, ())

    def get_no_regions(self):
        """Get Number of Regions

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_regions_cmd, ())

    def get_sample_length(self):
        """Get Sample Length

        Returns:
            QWORD
        """
        return self.sampler.execute(self.get_sample_length_cmd, ())

    def get_sample_rate(self):
        """Get Sample Rate [Hz]

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_sample_rate_cmd, ())

    def get_bit_depth(self):
        """Get Sample Bit-Depth [bits]

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_bit_depth_cmd, ())

    def get_sample_type(self):
        """Get Sample Type <Reply> = (0=RAM, 1=VIRTUAL)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_sample_type_cmd, ())

    def get_no_channels(self):
        """Get Number of Channels

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_no_channels_cmd, ())

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.sampler.execute(self.set_group_id_cmd, (arg0, ))

    def set_trim_start(self, arg0):
        """Set Trim Start
        """
        return self.sampler.execute(self.set_trim_start_cmd, (arg0, ))

    def set_trim_end(self, arg0):
        """Set Trim End
        """
        return self.sampler.execute(self.set_trim_end_cmd, (arg0, ))

    def set_trim_length(self, arg0):
        """Set Trim Length
        """
        return self.sampler.execute(self.set_trim_length_cmd, (arg0, ))

    def set_orig_pitch(self, arg0):
        """Set Original Pitch
        """
        return self.sampler.execute(self.set_orig_pitch_cmd, (arg0, ))

    def set_tune(self, arg0):
        """Set Cents Tune
        """
        return self.sampler.execute(self.set_tune_cmd, (arg0, ))

    def set_playback_mode(self, arg0):
        """Set Playback Mode, where arg0= (0=NO LOOPING, 1=LOOPING, 2=ONE SHOT)
        """
        return self.sampler.execute(self.set_playback_mode_cmd, (arg0, ))

    def set_loop_start(self, arg0, arg1):
        """Set Loop Start <Data1> = loop index
        """
        return self.sampler.execute(self.set_loop_start_cmd, (arg0, arg1, ))

    def set_loop_end(self, arg0, arg1):
        """Set Loop End
        """
        return self.sampler.execute(self.set_loop_end_cmd, (arg0, arg1, ))

    def set_loop_length(self, arg0, arg1):
        """Set Loop Length
        """
        return self.sampler.execute(self.set_loop_length_cmd, (arg0, arg1, ))

    def set_loop_lock(self, arg0, arg1):
        """Set Loop Lock <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_loop_lock_cmd, (arg0, arg1, ))

    def set_loop_tune(self, arg0, arg1):
        """Set Loop Tune (0-50)
        """
        return self.sampler.execute(self.set_loop_tune_cmd, (arg0, arg1, ))

    def set_loop_direction(self, arg0, arg1):
        """Set Loop Direction <Data1> = (0=FORWARDS, 1=ALTERNATING)
        """
        return self.sampler.execute(self.set_loop_direction_cmd, (arg0, arg1, ))

    def set_loop_type(self, arg0, arg1):
        """Set Loop Type <Data1> = (0=LOOP IN REL, 1=LOOP UNTIL REL)
        """
        return self.sampler.execute(self.set_loop_type_cmd, (arg0, arg1, ))

    def set_no_loop_reps(self, arg0):
        """Set Number of Loop Repetitions (0=INFINITE)
        """
        return self.sampler.execute(self.set_no_loop_reps_cmd, (arg0, ))

    def set_region_start(self, arg0, arg1):
        """Set Region Start <Data1> = Region Num, <Data2> = start
        """
        return self.sampler.execute(self.set_region_start_cmd, (arg0, arg1, ))

    def set_region_end(self, arg0, arg1):
        """Set Region End <Data1> = Region Num <Data2> = end
        """
        return self.sampler.execute(self.set_region_end_cmd, (arg0, arg1, ))

    def set_region_length(self, arg0, arg1):
        """Set Region Length <Data1> = Region Num <Data2> = length
        """
        return self.sampler.execute(self.set_region_length_cmd, (arg0, arg1, ))

