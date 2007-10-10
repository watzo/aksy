
""" Python equivalent of akai section keygrouptools

Keygroup manipulation
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Keygrouptools:
    def __init__(self, z48):
        self.sampler = z48
        self.set_curr_keygroup_cmd = Command('_', '\x10\x01', 'keygrouptools', 'set_curr_keygroup', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_curr_keygroup_cmd = Command('_', '\x10\x02', 'keygrouptools', 'get_curr_keygroup', (), None)
        self.get_group_id_cmd = Command('_', '\x13\x01', 'keygrouptools', 'get_group_id', (), None)
        self.get_edit_mode_cmd = Command('_', '\x13\x02', 'keygrouptools', 'get_edit_mode', (), None)
        self.get_low_note_cmd = Command('_', '\x13\x04', 'keygrouptools', 'get_low_note', (), None)
        self.get_high_note_cmd = Command('_', '\x13\x05', 'keygrouptools', 'get_high_note', (), None)
        self.get_mute_group_cmd = Command('_', '\x13\x06', 'keygrouptools', 'get_mute_group', (), None)
        self.get_fx_override_cmd = Command('_', '\x13\x07', 'keygrouptools', 'get_fx_override', (), None)
        self.get_fx_send_level_cmd = Command('_', '\x13\x08', 'keygrouptools', 'get_fx_send_level', (), None)
        self.get_zone_xfade_cmd = Command('_', '\x13\x09', 'keygrouptools', 'get_zone_xfade', (), None)
        self.get_zone_xfade_type_cmd = Command('_', '\x13\x0A', 'keygrouptools', 'get_zone_xfade_type', (), None)
        self.get_polyphony_cmd = Command('_', '\x13\x0E', 'keygrouptools', 'get_polyphony', (), None)
        self.get_zone_xfade_ctrl_no_cmd = Command('_', '\x13\x0F', 'keygrouptools', 'get_zone_xfade_ctrl_no', (), None)
        self.get_tune_cmd = Command('_', '\x13\x10', 'keygrouptools', 'get_tune', (), None)
        self.get_level_cmd = Command('_', '\x13\x11', 'keygrouptools', 'get_level', (), None)
        self.get_play_trigger_cmd = Command('_', '\x13\x18', 'keygrouptools', 'get_play_trigger', (), None)
        self.get_play_trigger_velocity_cmd = Command('_', '\x13\x19', 'keygrouptools', 'get_play_trigger_velocity', (), None)
        self.get_play_toggle_note_cmd = Command('_', '\x13\x1A', 'keygrouptools', 'get_play_toggle_note', (), None)
        self.get_filter_cmd = Command('_', '\x13\x20', 'keygrouptools', 'get_filter', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_filter_cutoff_cmd = Command('_', '\x13\x21', 'keygrouptools', 'get_filter_cutoff', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_filter_resonance_cmd = Command('_', '\x13\x22', 'keygrouptools', 'get_filter_resonance', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_filter_attenuation_cmd = Command('_', '\x13\x23', 'keygrouptools', 'get_filter_attenuation', (), None)
        self.get_envelope_rate1_cmd = Command('_', '\x13\x30', 'keygrouptools', 'get_envelope_rate1', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level1_cmd = Command('_', '\x13\x31', 'keygrouptools', 'get_envelope_level1', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_rate2_cmd = Command('_', '\x13\x32', 'keygrouptools', 'get_envelope_rate2', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level2_cmd = Command('_', '\x13\x33', 'keygrouptools', 'get_envelope_level2', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_rate3_cmd = Command('_', '\x13\x34', 'keygrouptools', 'get_envelope_rate3', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level3_cmd = Command('_', '\x13\x35', 'keygrouptools', 'get_envelope_level3', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_rate4_cmd = Command('_', '\x13\x36', 'keygrouptools', 'get_envelope_rate4', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level4_cmd = Command('_', '\x13\x37', 'keygrouptools', 'get_envelope_level4', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_reference_cmd = Command('_', '\x13\x42', 'keygrouptools', 'get_envelope_reference', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_attack_hold_cmd = Command('_', '\x13\x43', 'keygrouptools', 'get_attack_hold', (), None)
        self.get_lfo_rate_cmd = Command('_', '\x13\x50', 'keygrouptools', 'get_lfo_rate', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_delay_cmd = Command('_', '\x13\x51', 'keygrouptools', 'get_lfo_delay', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_depth_cmd = Command('_', '\x13\x52', 'keygrouptools', 'get_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_lfo_waveform_cmd = Command('_', '\x13\x53', 'keygrouptools', 'get_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_phase_cmd = Command('_', '\x13\x54', 'keygrouptools', 'get_lfo_phase', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_shift_cmd = Command('_', '\x13\x55', 'keygrouptools', 'get_lfo_shift', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_midi_sync_cmd = Command('_', '\x13\x56', 'keygrouptools', 'get_lfo_midi_sync', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_midi_clock_sync_div_cmd = Command('_', '\x13\x57', 'keygrouptools', 'get_midi_clock_sync_div', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_retrigger_cmd = Command('_', '\x13\x58', 'keygrouptools', 'get_lfo_retrigger', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_sync_cmd = Command('_', '\x13\x59', 'keygrouptools', 'get_lfo_sync', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_group_id_cmd = Command('_', '\x12\x01', 'keygrouptools', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_edit_mode_cmd = Command('_', '\x12\x02', 'keygrouptools', 'set_edit_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_low_note_cmd = Command('_', '\x12\x04', 'keygrouptools', 'set_low_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_high_note_cmd = Command('_', '\x12\x05', 'keygrouptools', 'set_high_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_mute_group_cmd = Command('_', '\x12\x06', 'keygrouptools', 'set_mute_group', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_fx_override_cmd = Command('_', '\x12\x07', 'keygrouptools', 'set_fx_override', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_fx_send_level_cmd = Command('_', '\x12\x08', 'keygrouptools', 'set_fx_send_level', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_zone_xfade_cmd = Command('_', '\x12\x09', 'keygrouptools', 'set_zone_xfade', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_zone_xfade_type_cmd = Command('_', '\x12\x0A', 'keygrouptools', 'set_zone_xfade_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_polyphony_cmd = Command('_', '\x12\x0E', 'keygrouptools', 'set_polyphony', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_zone_xfade_ctrl_no_cmd = Command('_', '\x12\x0F', 'keygrouptools', 'set_zone_xfade_ctrl_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_tune_cmd = Command('_', '\x12\x10', 'keygrouptools', 'set_tune', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_level_cmd = Command('_', '\x12\x11', 'keygrouptools', 'set_level', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_play_trigger_cmd = Command('_', '\x12\x18', 'keygrouptools', 'set_play_trigger', (), None)
        self.set_play_trigger_vel_cmd = Command('_', '\x12\x19', 'keygrouptools', 'set_play_trigger_vel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_toggle_note_cmd = Command('_', '\x12\x1A', 'keygrouptools', 'set_play_toggle_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_filter_cmd = Command('_', '\x12\x20', 'keygrouptools', 'set_filter', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_cutoff_cmd = Command('_', '\x12\x21', 'keygrouptools', 'set_filter_cutoff', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_resonance_cmd = Command('_', '\x12\x22', 'keygrouptools', 'set_filter_resonance', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_atten_cmd = Command('_', '\x12\x23', 'keygrouptools', 'set_filter_atten', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_envelope_rate1_cmd = Command('_', '\x12\x30', 'keygrouptools', 'set_envelope_rate1', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_level1_cmd = Command('_', '\x12\x31', 'keygrouptools', 'set_envelope_level1', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_rate2_cmd = Command('_', '\x12\x32', 'keygrouptools', 'set_envelope_rate2', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_level2_cmd = Command('_', '\x12\x33', 'keygrouptools', 'set_envelope_level2', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_rate3_cmd = Command('_', '\x12\x34', 'keygrouptools', 'set_envelope_rate3', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_level3_cmd = Command('_', '\x12\x35', 'keygrouptools', 'set_envelope_level3', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_rate4_cmd = Command('_', '\x12\x36', 'keygrouptools', 'set_envelope_rate4', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_level4_cmd = Command('_', '\x12\x37', 'keygrouptools', 'set_envelope_level4', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_envelope_reference_cmd = Command('_', '\x12\x42', 'keygrouptools', 'set_envelope_reference', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_attack_hold_cmd = Command('_', '\x12\x43', 'keygrouptools', 'set_attack_hold', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_lfo_rate_cmd = Command('_', '\x12\x50', 'keygrouptools', 'set_lfo_rate', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_delay_cmd = Command('_', '\x12\x51', 'keygrouptools', 'set_lfo_delay', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_depth_cmd = Command('_', '\x12\x52', 'keygrouptools', 'set_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_waveform_cmd = Command('_', '\x12\x53', 'keygrouptools', 'set_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_phase_cmd = Command('_', '\x12\x54', 'keygrouptools', 'set_lfo_phase', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_lfo_shift_cmd = Command('_', '\x12\x55', 'keygrouptools', 'set_lfo_shift', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.SBYTE), None)
        self.set_lfo_midi_sync_cmd = Command('_', '\x12\x56', 'keygrouptools', 'set_lfo_midi_sync', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BOOL), None)
        self.set_midi_clock_sync_div_cmd = Command('_', '\x12\x57', 'keygrouptools', 'set_midi_clock_sync_div', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_retrigger_cmd = Command('_', '\x12\x58', 'keygrouptools', 'set_lfo_retrigger', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.set_lfo_sync_cmd = Command('_', '\x12\x59', 'keygrouptools', 'set_lfo_sync', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)

    def set_curr_keygroup(self, arg0):
        """Select Keygroup to be current <Data1> = Keygroup number (starting with 0)
        """
        return self.sampler.execute(self.set_curr_keygroup_cmd, (arg0, ))

    def get_curr_keygroup(self):
        """Get Current Keygroup

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_curr_keygroup_cmd, ())

    def get_group_id(self):
        """Get Group ID

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_group_id_cmd, ())

    def get_edit_mode(self):
        """Get Keygroup Edit Mode <Reply1> = (0=SINGLE, 1=ALL, 2=ADD)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_edit_mode_cmd, ())

    def get_low_note(self):
        """Get Low Note

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_low_note_cmd, ())

    def get_high_note(self):
        """Get High Note

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_high_note_cmd, ())

    def get_mute_group(self):
        """Get Mute Group <Reply1> = (0=OFF, 1-64=value)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_mute_group_cmd, ())

    def get_fx_override(self):
        """Get FX override <Reply1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_fx_override_cmd, ())

    def get_fx_send_level(self):
        """Get FX Send Level <Reply1> = level in 10 dB (-600 +60)

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_fx_send_level_cmd, ())

    def get_zone_xfade(self):
        """Get Zone Crossfade <Reply1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_zone_xfade_cmd, ())

    def get_zone_xfade_type(self):
        """Get Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_zone_xfade_type_cmd, ())

    def get_polyphony(self):
        """Get Polyphony

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_polyphony_cmd, ())

    def get_zone_xfade_ctrl_no(self):
        """Get Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_zone_xfade_ctrl_no_cmd, ())

    def get_tune(self):
        """Get Cents Tune

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_tune_cmd, ())

    def get_level(self):
        """Get Keygroup Level (RT) <Reply> = value in 10 dB

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_level_cmd, ())

    def get_play_trigger(self):
        """Get Play Trigger <Reply> = (0=NOTE ON, 1=NOTE OFF)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_play_trigger_cmd, ())

    def get_play_trigger_velocity(self):
        """Get Play Trigger Velocity (0 129) <Reply> = (0=ON VEL, 1=OFF VEL, 2-129=0-127)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_play_trigger_velocity_cmd, ())

    def get_play_toggle_note(self):
        """Get Play Toggle Note <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_play_toggle_note_cmd, ())

    def get_filter(self, arg0):
        """Get Filter <Data1> = Filter block

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_filter_cmd, (arg0, ))

    def get_filter_cutoff(self, arg0):
        """Get Filter Cutoff Frequency. Data1= filter 0-3 reply: (0-100)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_filter_cutoff_cmd, (arg0, ))

    def get_filter_resonance(self, arg0):
        """Get Filter Resonance (0-3) (0-60)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_filter_resonance_cmd, (arg0, ))

    def get_filter_attenuation(self):
        """Get Filter Attenuation (one setting for all filters) <Reply> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_filter_attenuation_cmd, ())

    def get_envelope_rate1(self, arg0):
        """Get Envelope Rate1 <Data1> = Envelope (0=AMP, 1=FILTER, 2=AUX) 0-100) Get Envelope Rate 1 (for AMP = Attack)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_rate1_cmd, (arg0, ))

    def get_envelope_level1(self, arg0):
        """Get Envelope Level 1 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_level1_cmd, (arg0, ))

    def get_envelope_rate2(self, arg0):
        """Get Envelope Rate 2 (for AMP = Decay)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_rate2_cmd, (arg0, ))

    def get_envelope_level2(self, arg0):
        """Get Envelope Level 2 (for AMP = Sustain)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_level2_cmd, (arg0, ))

    def get_envelope_rate3(self, arg0):
        """Get Envelope Rate 3 (for AMP = Release)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_rate3_cmd, (arg0, ))

    def get_envelope_level3(self, arg0):
        """Get Envelope Level 3 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_level3_cmd, (arg0, ))

    def get_envelope_rate4(self, arg0):
        """Get Envelope Rate 4 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_rate4_cmd, (arg0, ))

    def get_envelope_level4(self, arg0):
        """Get Envelope Level 4 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_level4_cmd, (arg0, ))

    def get_envelope_reference(self, arg0):
        """Get Envelope Reference (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_envelope_reference_cmd, (arg0, ))

    def get_attack_hold(self):
        """Get Attack Hold <Reply> = (0=OFF, 1=ON) (AMP only)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_attack_hold_cmd, ())

    def get_lfo_rate(self, arg0):
        """Get LFO Rate (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_rate_cmd, (arg0, ))

    def get_lfo_delay(self, arg0):
        """Get LFO Delay (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_delay_cmd, (arg0, ))

    def get_lfo_depth(self, arg0, arg1):
        """Get LFO Depth (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_depth_cmd, (arg0, arg1, ))

    def get_lfo_waveform(self, arg0):
        """Get LFO Waveform <Reply> = waveform (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_waveform_cmd, (arg0, ))

    def get_lfo_phase(self, arg0):
        """Get LFO Phase(0=LFO1, 1=LFO2)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_lfo_phase_cmd, (arg0, ))

    def get_lfo_shift(self, arg0):
        """Get LFO Shift(0=LFO1, 1=LFO2)

        Returns:
            SBYTE
        """
        return self.sampler.execute(self.get_lfo_shift_cmd, (arg0, ))

    def get_lfo_midi_sync(self, arg0):
        """Get LFO MIDI Sync (0=LFO1, 1=LFO2) <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_midi_sync_cmd, (arg0, ))

    def get_midi_clock_sync_div(self, arg0):
        """Get MIDI Clock Sync Division <Reply> = value, where 0=8 cy/bt, 1=6cy/bt, 2=4cy/bt, 3=3cy/bt, 4=2cy/bt, 5=1cy/bt 6=2 bt/cy, 7=3bt/cy, ..., 68=64bt/cy

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_clock_sync_div_cmd, (arg0, ))

    def get_lfo_retrigger(self, arg0):
        """Get LFO Re-trigger <Data1>0: LFO1 1: LF02 <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_retrigger_cmd, (arg0, ))

    def get_lfo_sync(self, arg0):
        """Get LFO sync (i.e., all voices in program locked to same LFO)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_lfo_sync_cmd, (arg0, ))

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.sampler.execute(self.set_group_id_cmd, (arg0, ))

    def set_edit_mode(self, arg0):
        """Set Keygroup Edit Mode <Data2> = (0=SINGLE, 1=ALL, 2=ADD)
        """
        return self.sampler.execute(self.set_edit_mode_cmd, (arg0, ))

    def set_low_note(self, arg0):
        """Set Low Note
        """
        return self.sampler.execute(self.set_low_note_cmd, (arg0, ))

    def set_high_note(self, arg0):
        """Set High Note
        """
        return self.sampler.execute(self.set_high_note_cmd, (arg0, ))

    def set_mute_group(self, arg0):
        """Set Mute Group <Data1> = (0=OFF, 1-64=value)
        """
        return self.sampler.execute(self.set_mute_group_cmd, (arg0, ))

    def set_fx_override(self, arg0):
        """Set FX override <Data1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)
        """
        return self.sampler.execute(self.set_fx_override_cmd, (arg0, ))

    def set_fx_send_level(self, arg0):
        """Set FX Send Level <Data1> = level in 10 dB (-600 +60)
        """
        return self.sampler.execute(self.set_fx_send_level_cmd, (arg0, ))

    def set_zone_xfade(self, arg0):
        """Set Zone Crossfade <Data1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)
        """
        return self.sampler.execute(self.set_zone_xfade_cmd, (arg0, ))

    def set_zone_xfade_type(self, arg0):
        """Set Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)
        """
        return self.sampler.execute(self.set_zone_xfade_type_cmd, (arg0, ))

    def set_polyphony(self, arg0):
        """Set Polyphony
        """
        return self.sampler.execute(self.set_polyphony_cmd, (arg0, ))

    def set_zone_xfade_ctrl_no(self, arg0):
        """Set Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)
        """
        return self.sampler.execute(self.set_zone_xfade_ctrl_no_cmd, (arg0, ))

    def set_tune(self, arg0):
        """Set Cents Tune (0 +- 36)
        """
        return self.sampler.execute(self.set_tune_cmd, (arg0, ))

    def set_level(self, arg0):
        """Set Keygroup Level <Data1> = value in 10 dB
        """
        return self.sampler.execute(self.set_level_cmd, (arg0, ))

    def set_play_trigger(self):
        """Set Play Trigger <Data1> = (0=NOTE ON, 1=NOTE OFF)
        """
        return self.sampler.execute(self.set_play_trigger_cmd, ())

    def set_play_trigger_vel(self, arg0):
        """Set Play Trigger Velocity <Data1> = (0=ON VEL, 1=OFF VEL, 2-129=0-127)
        """
        return self.sampler.execute(self.set_play_trigger_vel_cmd, (arg0, ))

    def set_play_toggle_note(self, arg0):
        """Set Play Toggle Note <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_play_toggle_note_cmd, (arg0, ))

    def set_filter(self, arg0, arg1):
        """Set Filter Mode (0=NORMAL, 1=TRIPLE(1), 2=TRIPLE(2), 3=TRIPLE(3)), type
        """
        return self.sampler.execute(self.set_filter_cmd, (arg0, arg1, ))

    def set_filter_cutoff(self, arg0, arg1):
        """Set Filter Cutoff Frequency
        """
        return self.sampler.execute(self.set_filter_cutoff_cmd, (arg0, arg1, ))

    def set_filter_resonance(self, arg0, arg1):
        """Filter Resonance
        """
        return self.sampler.execute(self.set_filter_resonance_cmd, (arg0, arg1, ))

    def set_filter_atten(self, arg0):
        """Set Filter Attenuation (one setting for all filters) <Data1> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)
        """
        return self.sampler.execute(self.set_filter_atten_cmd, (arg0, ))

    def set_envelope_rate1(self, arg0, arg1):
        """Set Envelope Rate 1 (for AMP = Attack)(0=AMP, 1=FILTER, 2=AUX)
        """
        return self.sampler.execute(self.set_envelope_rate1_cmd, (arg0, arg1, ))

    def set_envelope_level1(self, arg0, arg1):
        """Set Envelope Level 1 (FILTER and AUX only)
        """
        return self.sampler.execute(self.set_envelope_level1_cmd, (arg0, arg1, ))

    def set_envelope_rate2(self, arg0, arg1):
        """Set Envelope Rate 2 (for AMP = Decay)
        """
        return self.sampler.execute(self.set_envelope_rate2_cmd, (arg0, arg1, ))

    def set_envelope_level2(self, arg0, arg1):
        """Set Envelope Level 2 (for AMP = Sustain)
        """
        return self.sampler.execute(self.set_envelope_level2_cmd, (arg0, arg1, ))

    def set_envelope_rate3(self, arg0, arg1):
        """Set Envelope Rate 3 (for AMP = Release)
        """
        return self.sampler.execute(self.set_envelope_rate3_cmd, (arg0, arg1, ))

    def set_envelope_level3(self, arg0, arg1):
        """Set Envelope Level 3 (FILTER and AUX only)
        """
        return self.sampler.execute(self.set_envelope_level3_cmd, (arg0, arg1, ))

    def set_envelope_rate4(self, arg0, arg1):
        """Set Envelope Rate 4 (FILTER and AUX only)
        """
        return self.sampler.execute(self.set_envelope_rate4_cmd, (arg0, arg1, ))

    def set_envelope_level4(self, arg0, arg1):
        """Set Envelope Level 4 (FILTER and AUX only)
        """
        return self.sampler.execute(self.set_envelope_level4_cmd, (arg0, arg1, ))

    def set_envelope_reference(self, arg0, arg1):
        """Set Envelope Reference (FILTER and AUX only)
        """
        return self.sampler.execute(self.set_envelope_reference_cmd, (arg0, arg1, ))

    def set_attack_hold(self, arg0):
        """Set Attack Hold <Data1> = (0=OFF, 1=ON) (AMP only)
        """
        return self.sampler.execute(self.set_attack_hold_cmd, (arg0, ))

    def set_lfo_rate(self, arg0, arg1):
        """Set LFO Rate (0: LFO1 1: LFO2), rate
        """
        return self.sampler.execute(self.set_lfo_rate_cmd, (arg0, arg1, ))

    def set_lfo_delay(self, arg0, arg1):
        """Set LFO Delay <Data2> = delay
        """
        return self.sampler.execute(self.set_lfo_delay_cmd, (arg0, arg1, ))

    def set_lfo_depth(self, arg0, arg1):
        """Set LFO Depth <Data2> = depth
        """
        return self.sampler.execute(self.set_lfo_depth_cmd, (arg0, arg1, ))

    def set_lfo_waveform(self, arg0, arg1):
        """Set LFO Waveform <Data2> = waveform, (see Table 23)
        """
        return self.sampler.execute(self.set_lfo_waveform_cmd, (arg0, arg1, ))

    def set_lfo_phase(self, arg0, arg1):
        """Set LFO Phase
        """
        return self.sampler.execute(self.set_lfo_phase_cmd, (arg0, arg1, ))

    def set_lfo_shift(self, arg0, arg1):
        """Set LFO Shift
        """
        return self.sampler.execute(self.set_lfo_shift_cmd, (arg0, arg1, ))

    def set_lfo_midi_sync(self, arg0, arg1):
        """Set LFO Midi Sync
        """
        return self.sampler.execute(self.set_lfo_midi_sync_cmd, (arg0, arg1, ))

    def set_midi_clock_sync_div(self, arg0, arg1):
        """Set LFO Midi Clock Sync Division
        """
        return self.sampler.execute(self.set_midi_clock_sync_div_cmd, (arg0, arg1, ))

    def set_lfo_retrigger(self, arg0, arg1):
        """Set LFO Retrigger
        """
        return self.sampler.execute(self.set_lfo_retrigger_cmd, (arg0, arg1, ))

    def set_lfo_sync(self, arg0, arg1):
        """Set LFO Sync
        """
        return self.sampler.execute(self.set_lfo_sync_cmd, (arg0, arg1, ))

