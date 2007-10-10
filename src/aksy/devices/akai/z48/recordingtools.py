
""" Python equivalent of akai section recordingtools

Methods to facilitate recording
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Recordingtools:
    def __init__(self, z48):
        self.sampler = z48
        self.get_status_cmd = Command('_', '\x30\x01', 'recordingtools', 'get_status', (), None)
        self.get_progress_cmd = Command('_', '\x30\x02', 'recordingtools', 'get_progress', (), None)
        self.get_max_rec_time_cmd = Command('_', '\x30\x03', 'recordingtools', 'get_max_rec_time', (), None)
        self.arm_cmd = Command('_', '\x30\x10', 'recordingtools', 'arm', (), None)
        self.start_cmd = Command('_', '\x30\x11', 'recordingtools', 'start', (), None)
        self.stop_cmd = Command('_', '\x30\x12', 'recordingtools', 'stop', (), None)
        self.cancel_cmd = Command('_', '\x30\x13', 'recordingtools', 'cancel', (), None)
        self.start_playing_cmd = Command('_', '\x30\x20', 'recordingtools', 'start_playing', (), None)
        self.stop_playing_cmd = Command('_', '\x30\x21', 'recordingtools', 'stop_playing', (), None)
        self.keep_cmd = Command('_', '\x30\x22', 'recordingtools', 'keep', (), None)
        self.delete_cmd = Command('_', '\x30\x23', 'recordingtools', 'delete', (), None)
        self.set_input_cmd = Command('_', '\x32\x01', 'recordingtools', 'set_input', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_mode_cmd = Command('_', '\x32\x02', 'recordingtools', 'set_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.enable_monitor_cmd = Command('_', '\x32\x03', 'recordingtools', 'enable_monitor', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_rec_time_cmd = Command('_', '\x32\x04', 'recordingtools', 'set_rec_time', (aksy.devices.akai.sysex_types.DWORD,), None)
        self.set_orig_pitch_cmd = Command('_', '\x32\x05', 'recordingtools', 'set_orig_pitch', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_threshold_cmd = Command('_', '\x32\x06', 'recordingtools', 'set_threshold', (aksy.devices.akai.sysex_types.SBYTE,), None)
        self.set_trigger_src_cmd = Command('_', '\x32\x07', 'recordingtools', 'set_trigger_src', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_bit_depth_cmd = Command('_', '\x32\x08', 'recordingtools', 'set_bit_depth', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_prerec_time_cmd = Command('_', '\x32\x09', 'recordingtools', 'set_prerec_time', (aksy.devices.akai.sysex_types.WORD,), None)
        self.set_dest_cmd = Command('_', '\x32\x0A', 'recordingtools', 'set_dest', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_name_cmd = Command('_', '\x32\x10', 'recordingtools', 'set_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.set_name_seed_cmd = Command('_', '\x32\x11', 'recordingtools', 'set_name_seed', (aksy.devices.akai.sysex_types.STRING,), None)
        self.set_autorec_mode_cmd = Command('_', '\x32\x12', 'recordingtools', 'set_autorec_mode', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_autonormalize_cmd = Command('_', '\x32\x13', 'recordingtools', 'set_autonormalize', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.get_input_cmd = Command('_', '\x33\x01', 'recordingtools', 'get_input', (), None)
        self.get_mode_cmd = Command('_', '\x33\x02', 'recordingtools', 'get_mode', (), None)
        self.get_monitor_cmd = Command('_', '\x33\x03', 'recordingtools', 'get_monitor', (), None)
        self.get_rec_time_cmd = Command('_', '\x33\x04', 'recordingtools', 'get_rec_time', (), None)
        self.get_pitch_cmd = Command('_', '\x33\x05', 'recordingtools', 'get_pitch', (), None)
        self.get_threshold_cmd = Command('_', '\x33\x06', 'recordingtools', 'get_threshold', (), None)
        self.get_trigger_src_cmd = Command('_', '\x33\x07', 'recordingtools', 'get_trigger_src', (), None)
        self.get_bit_depth_cmd = Command('_', '\x33\x08', 'recordingtools', 'get_bit_depth', (), None)
        self.get_prerec_time_cmd = Command('_', '\x33\x09', 'recordingtools', 'get_prerec_time', (), None)
        self.get_dest_cmd = Command('_', '\x33\x0A', 'recordingtools', 'get_dest', (), None)
        self.get_name_cmd = Command('_', '\x33\x10', 'recordingtools', 'get_name', (), None)
        self.get_name_seed_cmd = Command('_', '\x33\x11', 'recordingtools', 'get_name_seed', (), None)
        self.get_autorec_mode_cmd = Command('_', '\x33\x12', 'recordingtools', 'get_autorec_mode', (), None)
        self.get_autonormalize_cmd = Command('_', '\x33\x13', 'recordingtools', 'get_autonormalize', (), None)

    def get_status(self):
        """Get Record Status

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_status_cmd, ())

    def get_progress(self):
        """Get Record Progress

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_progress_cmd, ())

    def get_max_rec_time(self):
        """Get Maximum Record Time

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_max_rec_time_cmd, ())

    def arm(self):
        """Arm Recording
        """
        return self.sampler.execute(self.arm_cmd, ())

    def start(self):
        """Start Recording
        """
        return self.sampler.execute(self.start_cmd, ())

    def stop(self):
        """Stop Recording
        """
        return self.sampler.execute(self.stop_cmd, ())

    def cancel(self):
        """Cancel Recording
        """
        return self.sampler.execute(self.cancel_cmd, ())

    def start_playing(self):
        """Play Recorded Sample Start
        """
        return self.sampler.execute(self.start_playing_cmd, ())

    def stop_playing(self):
        """Play Recorded Sample Stop
        """
        return self.sampler.execute(self.stop_playing_cmd, ())

    def keep(self):
        """Keep Recorded Sample. Sample with name assigned above, is added to the list of available samples.
        """
        return self.sampler.execute(self.keep_cmd, ())

    def delete(self):
        """Delete Recorded Sample
        """
        return self.sampler.execute(self.delete_cmd, ())

    def set_input(self, arg0):
        """Set Input <Data1> = (0=ANALOGUE, 1=DIGITAL, 2=MAIN OUT 3=ADAT1/2, 4=ADAT3/4, 5=ADAT5/6, 6=ADAT7/8)
        """
        return self.sampler.execute(self.set_input_cmd, (arg0, ))

    def set_mode(self, arg0):
        """Set Record Mode <Data1> = (0=STEREO, 1=MONO L, 2=MONO R, 3=L/R MIX)
        """
        return self.sampler.execute(self.set_mode_cmd, (arg0, ))

    def enable_monitor(self, arg0):
        """Set Record Monitor
        """
        return self.sampler.execute(self.enable_monitor_cmd, (arg0, ))

    def set_rec_time(self, arg0):
        """Set Record Time <Data1> = time in seconds. If <Data1> = 0, MANUAL mode is enabled.
        """
        return self.sampler.execute(self.set_rec_time_cmd, (arg0, ))

    def set_orig_pitch(self, arg0):
        """Set Original Pitch
        """
        return self.sampler.execute(self.set_orig_pitch_cmd, (arg0, ))

    def set_threshold(self, arg0):
        """Set Threshold <Data1> = threshold in dB (-63,0)
        """
        return self.sampler.execute(self.set_threshold_cmd, (arg0, ))

    def set_trigger_src(self, arg0):
        """Set Trigger Source (0=OFF, 1=AUDIO, 2=MIDI)
        """
        return self.sampler.execute(self.set_trigger_src_cmd, (arg0, ))

    def set_bit_depth(self, arg0):
        """Set Bit Depth <Data1> = (0=16-bit, 1=24-bit)
        """
        return self.sampler.execute(self.set_bit_depth_cmd, (arg0, ))

    def set_prerec_time(self, arg0):
        """Set Pre-recording Time <Data1> = time in ms
        """
        return self.sampler.execute(self.set_prerec_time_cmd, (arg0, ))

    def set_dest(self, arg0):
        """Set Recording Detination <Data1> = (0=RAM, 1=DISK) Note: seems to be unsupported
        """
        return self.sampler.execute(self.set_dest_cmd, (arg0, ))

    def set_name(self, arg0):
        """Set Record Name
        """
        return self.sampler.execute(self.set_name_cmd, (arg0, ))

    def set_name_seed(self, arg0):
        """Set Record Name Seed
        """
        return self.sampler.execute(self.set_name_seed_cmd, (arg0, ))

    def set_autorec_mode(self, arg0):
        """Set Auto-Record Mode <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_autorec_mode_cmd, (arg0, ))

    def set_autonormalize(self, arg0):
        """Set Auto-Normalise Mode <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_autonormalize_cmd, (arg0, ))

    def get_input(self):
        """Get Input (0=ANALOGUE, 1=DIGITAL, 2=MAIN OUT, 3=ADAT1/2, 4=ADAT3/4, 5=ADAT5/6, 6=ADAT7/8)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_input_cmd, ())

    def get_mode(self):
        """Get Record Mode (0=STEREO, 1=MONO L, 2=MONO R, 3=L/R MIX)
        """
        return self.sampler.execute(self.get_mode_cmd, ())

    def get_monitor(self):
        """Get Record Monitor <Reply> = (0=OFF, 1=ON)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_monitor_cmd, ())

    def get_rec_time(self):
        """Get Record Time <Reply> = time in seconds.

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_rec_time_cmd, ())

    def get_pitch(self):
        """Get Original Pitch

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pitch_cmd, ())

    def get_threshold(self):
        """Get Threshold <Reply> = threshold in dB -63,0

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_threshold_cmd, ())

    def get_trigger_src(self):
        """Get Trigger Source <Reply> = (0=OFF, 1=AUDIO, 2=MIDI)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_trigger_src_cmd, ())

    def get_bit_depth(self):
        """Get Bit Depth <Reply> = (0=16-bit, 1=24-bit)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_bit_depth_cmd, ())

    def get_prerec_time(self):
        """Get Pre-recording Time <Reply> = time in ms

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_prerec_time_cmd, ())

    def get_dest(self):
        """Get Recording Destination <Reply> = (0=RAM, 1=DISK) Note: seems to be unsupported

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_dest_cmd, ())

    def get_name(self):
        """Get Record Name

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_name_cmd, ())

    def get_name_seed(self):
        """Get Record Name Seed

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_name_seed_cmd, ())

    def get_autorec_mode(self):
        """Get Auto-Record Mode <Reply> = (0=OFF, 1=ON)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_autorec_mode_cmd, ())

    def get_autonormalize(self):
        """Get Auto-Normalise Mode <Reply> = (0=OFF, 1=ON)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_autonormalize_cmd, ())

