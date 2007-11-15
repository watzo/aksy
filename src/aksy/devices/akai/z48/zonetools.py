
""" Python equivalent of akai section zonetools

Manipulate the zones of a keygroup
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Zonetools:
    def __init__(self, z48):
        self.sampler = z48
        self.get_sample_cmd = Command('_', '\x0F\x01', 'zonetools', 'get_sample', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_level_cmd = Command('_', '\x0F\x02', 'zonetools', 'get_level', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_pan_cmd = Command('_', '\x0F\x03', 'zonetools', 'get_pan', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_output_cmd = Command('_', '\x0F\x04', 'zonetools', 'get_output', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_filter_cmd = Command('_', '\x0F\x05', 'zonetools', 'get_filter', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_tune_cmd = Command('_', '\x0F\x06', 'zonetools', 'get_tune', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_keyboard_track_cmd = Command('_', '\x0F\x07', 'zonetools', 'get_keyboard_track', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_playback_cmd = Command('_', '\x0F\x08', 'zonetools', 'get_playback', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_mod_start_cmd = Command('_', '\x0F\x09', 'zonetools', 'get_mod_start', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_low_velocity_cmd = Command('_', '\x0F\x0A', 'zonetools', 'get_low_velocity', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_high_velocity_cmd = Command('_', '\x0F\x0B', 'zonetools', 'get_high_velocity', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_mute_cmd = Command('_', '\x0F\x0C', 'zonetools', 'get_mute', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_solo_cmd = Command('_', '\x0F\x0D', 'zonetools', 'get_solo', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_sample_cmd = Command('_', '\x0E\x01', 'zonetools', 'set_sample', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.STRING), None)
        self.set_level_cmd = Command('_', '\x0E\x02', 'zonetools', 'set_level', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_pan_cmd = Command('_', '\x0E\x03', 'zonetools', 'set_pan', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_output_cmd = Command('_', '\x0E\x04', 'zonetools', 'set_output', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_cmd = Command('_', '\x0E\x05', 'zonetools', 'set_filter', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_tune_cmd = Command('_', '\x0E\x06', 'zonetools', 'set_tune', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_keyboard_track_cmd = Command('_', '\x0E\x07', 'zonetools', 'set_keyboard_track', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_playback_cmd = Command('_', '\x0E\x08', 'zonetools', 'set_playback', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_mod_start_cmd = Command('_', '\x0E\x09', 'zonetools', 'set_mod_start', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SWORD), None)
        self.set_low_vel_cmd = Command('_', '\x0E\x0A', 'zonetools', 'set_low_vel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_high_vel_cmd = Command('_', '\x0E\x0B', 'zonetools', 'set_high_vel', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_mute_cmd = Command('_', '\x0E\x0C', 'zonetools', 'set_mute', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_solo_cmd = Command('_', '\x0E\x0D', 'zonetools', 'set_solo', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)

    def get_sample(self, arg0):
        """Get Zone Sample (Data1=zone number 1-4)

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_sample_cmd, (arg0, ))

    def get_level(self, arg0):
        """Get Zone Level <Reply> = level in 10 dB

        Returns:
            LEVEL
        """
        return self.sampler.execute(self.get_level_cmd, (arg0, ))

    def get_pan(self, arg0):
        """Get Zone Pan (0-100)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pan_cmd, (arg0, ))

    def get_output(self, arg0):
        """Get Zone Output(0-15)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_output_cmd, (arg0, ))

    def get_filter(self, arg0):
        """Get Zone Filter (0 +-100)

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_filter_cmd, (arg0, ))

    def get_tune(self, arg0):
        """Get Zone Cents Tune(0 +-3600)

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_tune_cmd, (arg0, ))

    def get_keyboard_track(self, arg0):
        """Get Zone Keyboard Track

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_keyboard_track_cmd, (arg0, ))

    def get_playback(self, arg0):
        """Get Zone Playback

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_playback_cmd, (arg0, ))

    def get_mod_start(self, arg0):
        """Get Zone ModStart(0 +- 9999)

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_mod_start_cmd, (arg0, ))

    def get_low_velocity(self, arg0):
        """Get Zone Low Velocity

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_low_velocity_cmd, (arg0, ))

    def get_high_velocity(self, arg0):
        """Get Zone High Velocity

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_high_velocity_cmd, (arg0, ))

    def get_mute(self, arg0):
        """Get Zone Mute

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_mute_cmd, (arg0, ))

    def get_solo(self, arg0):
        """Get Zone Solo

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_solo_cmd, (arg0, ))

    def set_sample(self, arg0, arg1):
        """Set Zone Sample <Data2...0> = name of sample to assign to zone. (0, 1-4)
        """
        return self.sampler.execute(self.set_sample_cmd, (arg0, arg1, ))

    def set_level(self, arg0, arg1):
        """Set Zone Level <Data1> = Zone number, <Data2> = level in 10xdB (0, 1-4)
        """
        return self.sampler.execute(self.set_level_cmd, (arg0, arg1, ))

    def set_pan(self, arg0, arg1):
        """Set Zone Pan/Balance <Data2> = Pan/Bal where (0-100 = L50-R50);
        """
        return self.sampler.execute(self.set_pan_cmd, (arg0, arg1, ))

    def set_output(self, arg0, arg1):
        """Set Zone Output <Data2> = output, where 0=MULTI, 1 = L/R; 2-5 = op1/2;op7/8; 6-15 = L, R, op1-op8
        """
        return self.sampler.execute(self.set_output_cmd, (arg0, arg1, ))

    def set_filter(self, arg0, arg1):
        """Set Zone Filter
        """
        return self.sampler.execute(self.set_filter_cmd, (arg0, arg1, ))

    def set_tune(self, arg0, arg1):
        """Set Zone Cents Tune
        """
        return self.sampler.execute(self.set_tune_cmd, (arg0, arg1, ))

    def set_keyboard_track(self, arg0, arg1):
        """Set Zone Keyboard Track
        """
        return self.sampler.execute(self.set_keyboard_track_cmd, (arg0, arg1, ))

    def set_playback(self, arg0, arg1):
        """Set Zone Playback <Data2> = mode, where 0=NO LOOPING, 1=ONE SHOT 2=LOOP IN REL, 3=LOOP UNTIL REL, 4=LIRRETRIG, 5=PLAYRETRIG, 6=AS SAMPLE
        """
        return self.sampler.execute(self.set_playback_cmd, (arg0, arg1, ))

    def set_mod_start(self, arg0, arg1):
        """Set Zone ModStart
        """
        return self.sampler.execute(self.set_mod_start_cmd, (arg0, arg1, ))

    def set_low_vel(self, arg0, arg1):
        """Set Zone Low Velocity
        """
        return self.sampler.execute(self.set_low_vel_cmd, (arg0, arg1, ))

    def set_high_vel(self, arg0, arg1):
        """Set Zone High Velocity
        """
        return self.sampler.execute(self.set_high_vel_cmd, (arg0, arg1, ))

    def set_mute(self, arg0, arg1):
        """Set Zone Mute <Data2> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_mute_cmd, (arg0, arg1, ))

    def set_solo(self, arg0, arg1):
        """Set Zone Solo <Data2> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_solo_cmd, (arg0, arg1, ))

