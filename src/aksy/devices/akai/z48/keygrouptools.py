
""" Python equivalent of akai section keygrouptools

Keygroup manipulation
"""

__author__ =  'Walco van Loon'
__version__=  '$Rev$'

from new import classobj

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Keygrouptools:
    def __init__(self, z48):
        self.z48 = z48
        self.set_curr_keygroup = classobj('Set_Curr_Keygroup', (aksy.devices.akai.sysex.Command,), {'__doc__':'Select Keygroup to be current <Data1> = Keygroup number (starting with 0)'})('_', '\x10\x01', 'set_curr_keygroup', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_curr_keygroup = classobj('Get_Curr_Keygroup', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Current Keygroup'})('_', '\x10\x02', 'get_curr_keygroup', (), None)
        self.get_group_id = classobj('Get_Group_Id', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Group ID'})('_', '\x13\x01', 'get_group_id', (), None)
        self.get_edit_mode = classobj('Get_Edit_Mode', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Keygroup Edit Mode <Reply1> = (0=SINGLE, 1=ALL, 2=ADD)'})('_', '\x13\x02', 'get_edit_mode', (), None)
        self.get_low_note = classobj('Get_Low_Note', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Low Note'})('_', '\x13\x04', 'get_low_note', (), None)
        self.get_high_note = classobj('Get_High_Note', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get High Note'})('_', '\x13\x05', 'get_high_note', (), None)
        self.get_mute_group = classobj('Get_Mute_Group', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Mute Group <Reply1> = (0=OFF, 1­64=value)'})('_', '\x13\x06', 'get_mute_group', (), None)
        self.get_fx_override = classobj('Get_Fx_Override', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get FX override <Reply1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)'})('_', '\x13\x07 ', 'get_fx_override', (), None)
        self.get_fx_send_level = classobj('Get_Fx_Send_Level', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get FX Send Level <Reply1> = level in 10×dB (-600­+60)'})('_', '\x13\x08', 'get_fx_send_level', (), None)
        self.get_zone_crossfade = classobj('Get_Zone_Crossfade', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Zone Crossfade <Reply1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)'})('_', '\x13\x09', 'get_zone_crossfade', (), None)
        self.get_crossfade_type = classobj('Get_Crossfade_Type', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)'})('_', '\x13\x0A', 'get_crossfade_type', (), None)
        self.get_polyphoy = classobj('Get_Polyphoy', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Polyphony'})('_', '\x13\x0E', 'get_polyphoy', (), None)
        self.get_zone_crossfade_ctrl_no = classobj('Get_Zone_Crossfade_Ctrl_No', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)'})('_', '\x13\x0F', 'get_zone_crossfade_ctrl_no', (), None)
        self.get_tune = classobj('Get_Tune', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Cents Tune'})('_', '\x13\x10', 'get_tune', (), None)
        self.get_level = classobj('Get_Level', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Keygroup Level (RT) <Reply> = value in 10×dB'})('_', '\x13\x11 ', 'get_level', (), None)
        self.get_play_trigger = classobj('Get_Play_Trigger', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Play Trigger <Reply> = (0=NOTE ON, 1=NOTE OFF)'})('_', '\x13\x18', 'get_play_trigger', (), None)
        self.get_player_trigger_velocity = classobj('Get_Player_Trigger_Velocity', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Play Trigger Velocity (0­129) <Reply> = (0=ON VEL, 1=OFF VEL, 2­129=0­127)'})('_', '\x13\x19', 'get_player_trigger_velocity', (), None)
        self.get_play_toggle_note = classobj('Get_Play_Toggle_Note', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Play Toggle Note <Reply> = (0=OFF, 1=ON)'})('_', '\x13\x1A ', 'get_play_toggle_note', (), None)
        self.get_filter = classobj('Get_Filter', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Filter <Data1> = Filter block (0=N'})('_', '\x13\x20', 'get_filter', (), None)
        self.get_filter_cutoff = classobj('Get_Filter_Cutoff', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Filter Cutoff Frequency. Data1= filter 0-3 reply: (0-100) BYTE'})('_', '\x13\x21', 'get_filter_cutoff', (), None)
        self.get_filter_resonance = classobj('Get_Filter_Resonance', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Filter Resonance (0-3) (0-60)'})('_', '\x13\x22', 'get_filter_resonance', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_filter_attenuation = classobj('Get_Filter_Attenuation', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Filter Attenuation (one setting for all filters) <Reply> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)'})('_', '\x13\x23', 'get_filter_attenuation', (), None)
        self.get_envelope_rate = classobj('Get_Envelope_Rate', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Rate1 <Data1> = Envelope (0=AMP, 1=FILTER, 2=AUX) 0­100) Get Envelope Rate 1 (for AMP = Attack)'})('_', '\x13\x30', 'get_envelope_rate', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level1 = classobj('Get_Envelope_Level1', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Level 1 (FILTER and AUX only)'})('_', '\x13\x31', 'get_envelope_level1', (), None)
        self.get_envelope_rate2 = classobj('Get_Envelope_Rate2', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Rate 2 (for AMP = Decay)'})('_', '\x13\x32', 'get_envelope_rate2', (), None)
        self.get_envelope_level2 = classobj('Get_Envelope_Level2', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Level 2 (for AMP = Sustain)'})('_', '\x13\x33', 'get_envelope_level2', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_rate3 = classobj('Get_Envelope_Rate3', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Rate 3 (for AMP = Release)'})('_', '\x13\x34', 'get_envelope_rate3', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level3 = classobj('Get_Envelope_Level3', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Level 3 (FILTER and AUX only)'})('_', '\x13\x35', 'get_envelope_level3', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_rate4 = classobj('Get_Envelope_Rate4', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Rate 4 (FILTER and AUX only)'})('_', '\x13\x36', 'get_envelope_rate4', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_level4 = classobj('Get_Envelope_Level4', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Level 4 (FILTER and AUX only)'})('_', '\x13\x37', 'get_envelope_level4', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_envelope_reference = classobj('Get_Envelope_Reference', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Envelope Reference (FILTER and AUX only)'})('_', '\x13\x42', 'get_envelope_reference', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_attack_hold = classobj('Get_Attack_Hold', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get Attack Hold <Reply> = (0=OFF, 1=ON) (AMP only)'})('_', '\x13\x43 ', 'get_attack_hold', (), None)
        self.get_lfo_rate = classobj('Get_Lfo_Rate', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Rate (0=LFO1, 1=LFO2)'})('_', '\x13\x50', 'get_lfo_rate', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_delay = classobj('Get_Lfo_Delay', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Delay (0=LFO1, 1=LFO2)'})('_', '\x13\x51 ', 'get_lfo_delay', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_depth = classobj('Get_Lfo_Depth', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Depth (0=LFO1, 1=LFO2)'})('_', '\x13\x52 ', 'get_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.get_lfo_waveform = classobj('Get_Lfo_Waveform', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Waveform <Reply> = waveform (0=LFO1, 1=LFO2)'})('_', '\x13\x53', 'get_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_phase = classobj('Get_Lfo_Phase', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Phase(0=LFO1, 1=LFO2)'})('_', '\x13\x54 ', 'get_lfo_phase', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_shift = classobj('Get_Lfo_Shift', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Shift(0=LFO1, 1=LFO2)'})('_', '\x13\x55', 'get_lfo_shift', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_midi_sync = classobj('Get_Lfo_Midi_Sync', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO MIDI Sync (0=LFO1, 1=LFO2) <Reply> = (0=OFF, 1=ON)'})('_', '\x13\x56', 'get_lfo_midi_sync', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_midi_clock_sync_div = classobj('Get_Midi_Clock_Sync_Div', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get MIDI Clock Sync Division <Reply> = value, where 0=8 cy/bt, 1=6cy/bt, 2=4cy/bt, 3=3cy/bt, 4=2cy/bt, 5=1cy/bt 6=2 bt/cy, 7=3bt/cy, ..., 68=64bt/cy'})('_', '\x13\x57', 'get_midi_clock_sync_div', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_retrigger = classobj('Get_Lfo_Retrigger', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO Re-trigger <Data1>0: LFO1 1: LF02 <Reply> = (0=OFF, 1=ON)'})('_', '\x13\x58 ', 'get_lfo_retrigger', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_lfo_sync = classobj('Get_Lfo_Sync', (aksy.devices.akai.sysex.Command,), {'__doc__':'Get LFO sync (i.e., all voices in program locked to same LFO)'})('_', '\x13\x59', 'get_lfo_sync', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_group_id = classobj('Set_Group_Id', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Group ID'})('_', '\x12\x01', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_edit_mode = classobj('Set_Edit_Mode', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Keygroup Edit Mode <Data2> = (0=SINGLE, 1=ALL, 2=ADD)'})('_', '\x12\x02', 'set_edit_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_low_note = classobj('Set_Low_Note', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Low Note'})('_', '\x12\x04', 'set_low_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_high_note = classobj('Set_High_Note', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set High Note'})('_', '\x12\x05', 'set_high_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_mute_group = classobj('Set_Mute_Group', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Mute Group <Data1> = (0=OFF, 1­64=value)'})('_', '\x12\x06', 'set_mute_group', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_fx_override = classobj('Set_Fx_Override', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set FX override <Data1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)'})('_', '\x12\x07', 'set_fx_override', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_fx_send_level = classobj('Set_Fx_Send_Level', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set FX Send Level <Data1> = level in 10×dB (-600­+60)'})('_', '\x12\x08', 'set_fx_send_level', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_zone_xfade = classobj('Set_Zone_Xfade', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Zone Crossfade <Data1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)'})('_', '\x12\x09', 'set_zone_xfade', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_xfade_type = classobj('Set_Xfade_Type', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)'})('_', '\x12\x0A', 'set_xfade_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_polyphony = classobj('Set_Polyphony', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Polyphony'})('_', '\x12\x0E', 'set_polyphony', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_zone_xfade_ctrl_no = classobj('Set_Zone_Xfade_Ctrl_No', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)'})('_', '\x12\x0F', 'set_zone_xfade_ctrl_no', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_tune = classobj('Set_Tune', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Cents Tune (0 ­ ±36)'})('_', '\x12\x10', 'set_tune', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_level = classobj('Set_Level', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Keygroup Level <Data1> = value in 10×dB'})('_', '\x12\x11', 'set_level', (aksy.devices.akai.sysex_types.SWORD,), None)
        self.set_play_trigger = classobj('Set_Play_Trigger', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Play Trigger <Data1> = (0=NOTE ON, 1=NOTE OFF)'})('_', '\x12\x18', 'set_play_trigger', (), None)
        self.set_play_trigger_vel = classobj('Set_Play_Trigger_Vel', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Play Trigger Velocity <Data1> = (0=ON VEL, 1=OFF VEL, 2­129=0­127)'})('_', '\x12\x19', 'set_play_trigger_vel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_toggle_note = classobj('Set_Play_Toggle_Note', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Play Toggle Note <Data1> = (0=OFF, 1=ON)'})('_', '\x12\x1A ', 'set_play_toggle_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_filter_mode = classobj('Set_Filter_Mode', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Filter Mode (0=NORMAL, 1=TRIPLE(1), 2=TRIPLE(2), 3=TRIPLE(3)), type'})('_', '\x12\x20', 'set_filter_mode', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_cutoff = classobj('Set_Filter_Cutoff', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Filter Cutoff Frequency'})('_', '\x12\x21', 'set_filter_cutoff', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_resonance = classobj('Set_Filter_Resonance', (aksy.devices.akai.sysex.Command,), {'__doc__':'Filter Resonance'})('_', '\x12\x22', 'set_filter_resonance', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_filter_atten = classobj('Set_Filter_Atten', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Filter Attenuation (one setting for all filters) <Data1> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)'})('_', '\x12\x23', 'set_filter_atten', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_env_rate1 = classobj('Set_Env_Rate1', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Rate 1 (for AMP = Attack)(0=AMP, 1=FILTER, 2=AUX)'})('_', '\x12\x30', 'set_env_rate1', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_level1 = classobj('Set_Env_Level1', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Level 1 (FILTER and AUX only)'})('_', '\x12\x31', 'set_env_level1', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_rate2 = classobj('Set_Env_Rate2', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Rate 2 (for AMP = Decay)'})('_', '\x12\x32', 'set_env_rate2', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_level2 = classobj('Set_Env_Level2', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Level 2 (for AMP = Sustain)'})('_', '\x12\x33', 'set_env_level2', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_rate3 = classobj('Set_Env_Rate3', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Rate 3 (for AMP = Release)'})('_', '\x12\x34', 'set_env_rate3', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_level3 = classobj('Set_Env_Level3', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Level 3 (FILTER and AUX only)'})('_', '\x12\x35', 'set_env_level3', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_rate4 = classobj('Set_Env_Rate4', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Rate 4 (FILTER and AUX only)'})('_', '\x12\x36', 'set_env_rate4', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_level4 = classobj('Set_Env_Level4', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Level 4 (FILTER and AUX only)'})('_', '\x12\x37', 'set_env_level4', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_env_ref = classobj('Set_Env_Ref', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Envelope Reference (FILTER and AUX only)'})('_', '\x12\x42', 'set_env_ref', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_attack_hold = classobj('Set_Attack_Hold', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set Attack Hold <Data1> = (0=OFF, 1=ON) (AMP only)'})('_', '\x12\x43', 'set_attack_hold', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_lfo_rate = classobj('Set_Lfo_Rate', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set LFO Rate (0: LFO1 1: LFO2), rate'})('_', '\x12\x50', 'set_lfo_rate', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_delay = classobj('Set_Lfo_Delay', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set LFO Delay <Data2> = delay'})('_', '\x12\x51', 'set_lfo_delay', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_depth = classobj('Set_Lfo_Depth', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set LFO Depth <Data2> = depth'})('_', '\x12\x52', 'set_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_waveform = classobj('Set_Lfo_Waveform', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set LFO Waveform <Data2> = waveform, (see Table 23)'})('_', '\x12\x53', 'set_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_lfo_phase = classobj('Set_Lfo_Phase', (aksy.devices.akai.sysex.Command,), {'__doc__':'Set LFO Phase'})('_', '\x12\x54', 'set_lfo_phase', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)

    def set_curr_keygroup(self, arg0):
        """Select Keygroup to be current <Data1> = Keygroup number (starting with 0)
        """
        return self.z48.execute(self.set_curr_keygroup, (arg0, ))

    def get_curr_keygroup(self):
        """Get Current Keygroup

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_curr_keygroup, ())

    def get_group_id(self):
        """Get Group ID

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_group_id, ())

    def get_edit_mode(self):
        """Get Keygroup Edit Mode <Reply1> = (0=SINGLE, 1=ALL, 2=ADD)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_edit_mode, ())

    def get_low_note(self):
        """Get Low Note

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_low_note, ())

    def get_high_note(self):
        """Get High Note

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_high_note, ())

    def get_mute_group(self):
        """Get Mute Group <Reply1> = (0=OFF, 1­64=value)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_mute_group, ())

    def get_fx_override(self):
        """Get FX override <Reply1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_fx_override, ())

    def get_fx_send_level(self):
        """Get FX Send Level <Reply1> = level in 10×dB (-600­+60)

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_fx_send_level, ())

    def get_zone_crossfade(self):
        """Get Zone Crossfade <Reply1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_zone_crossfade, ())

    def get_crossfade_type(self):
        """Get Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_crossfade_type, ())

    def get_polyphoy(self):
        """Get Polyphony

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_polyphoy, ())

    def get_zone_crossfade_ctrl_no(self):
        """Get Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_zone_crossfade_ctrl_no, ())

    def get_tune(self):
        """Get Cents Tune

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_tune, ())

    def get_level(self):
        """Get Keygroup Level (RT) <Reply> = value in 10×dB

        Returns:
            SWORD
        """
        return self.z48.execute(self.get_level, ())

    def get_play_trigger(self):
        """Get Play Trigger <Reply> = (0=NOTE ON, 1=NOTE OFF)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_play_trigger, ())

    def get_player_trigger_velocity(self):
        """Get Play Trigger Velocity (0­129) <Reply> = (0=ON VEL, 1=OFF VEL, 2­129=0­127)

        Returns:
            WORD
        """
        return self.z48.execute(self.get_player_trigger_velocity, ())

    def get_play_toggle_note(self):
        """Get Play Toggle Note <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_play_toggle_note, ())

    def get_filter(self):
        """Get Filter <Data1> = Filter block (0=N

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_filter, ())

    def get_filter_cutoff(self):
        """Get Filter Cutoff Frequency. Data1= filter 0-3 reply: (0-100) BYTE

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_filter_cutoff, ())

    def get_filter_resonance(self, arg0):
        """Get Filter Resonance (0-3) (0-60)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_filter_resonance, (arg0, ))

    def get_filter_attenuation(self):
        """Get Filter Attenuation (one setting for all filters) <Reply> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_filter_attenuation, ())

    def get_envelope_rate(self, arg0):
        """Get Envelope Rate1 <Data1> = Envelope (0=AMP, 1=FILTER, 2=AUX) 0­100) Get Envelope Rate 1 (for AMP = Attack)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_rate, (arg0, ))

    def get_envelope_level1(self):
        """Get Envelope Level 1 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_level1, ())

    def get_envelope_rate2(self):
        """Get Envelope Rate 2 (for AMP = Decay)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_rate2, ())

    def get_envelope_level2(self, arg0):
        """Get Envelope Level 2 (for AMP = Sustain)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_level2, (arg0, ))

    def get_envelope_rate3(self, arg0):
        """Get Envelope Rate 3 (for AMP = Release)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_rate3, (arg0, ))

    def get_envelope_level3(self, arg0):
        """Get Envelope Level 3 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_level3, (arg0, ))

    def get_envelope_rate4(self, arg0):
        """Get Envelope Rate 4 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_rate4, (arg0, ))

    def get_envelope_level4(self, arg0):
        """Get Envelope Level 4 (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_level4, (arg0, ))

    def get_envelope_reference(self, arg0):
        """Get Envelope Reference (FILTER and AUX only)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_envelope_reference, (arg0, ))

    def get_attack_hold(self):
        """Get Attack Hold <Reply> = (0=OFF, 1=ON) (AMP only)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_attack_hold, ())

    def get_lfo_rate(self, arg0):
        """Get LFO Rate (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_rate, (arg0, ))

    def get_lfo_delay(self, arg0):
        """Get LFO Delay (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_delay, (arg0, ))

    def get_lfo_depth(self, arg0, arg1):
        """Get LFO Depth (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_depth, (arg0, arg1, ))

    def get_lfo_waveform(self, arg0):
        """Get LFO Waveform <Reply> = waveform (0=LFO1, 1=LFO2)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_waveform, (arg0, ))

    def get_lfo_phase(self, arg0):
        """Get LFO Phase(0=LFO1, 1=LFO2)

        Returns:
            WORD
        """
        return self.z48.execute(self.get_lfo_phase, (arg0, ))

    def get_lfo_shift(self, arg0):
        """Get LFO Shift(0=LFO1, 1=LFO2)

        Returns:
            SBYTE
        """
        return self.z48.execute(self.get_lfo_shift, (arg0, ))

    def get_lfo_midi_sync(self, arg0):
        """Get LFO MIDI Sync (0=LFO1, 1=LFO2) <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_midi_sync, (arg0, ))

    def get_midi_clock_sync_div(self, arg0):
        """Get MIDI Clock Sync Division <Reply> = value, where 0=8 cy/bt, 1=6cy/bt, 2=4cy/bt, 3=3cy/bt, 4=2cy/bt, 5=1cy/bt 6=2 bt/cy, 7=3bt/cy, ..., 68=64bt/cy

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_midi_clock_sync_div, (arg0, ))

    def get_lfo_retrigger(self, arg0):
        """Get LFO Re-trigger <Data1>0: LFO1 1: LF02 <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_retrigger, (arg0, ))

    def get_lfo_sync(self, arg0):
        """Get LFO sync (i.e., all voices in program locked to same LFO)

        Returns:
            BYTE
        """
        return self.z48.execute(self.get_lfo_sync, (arg0, ))

    def set_group_id(self, arg0):
        """Set Group ID
        """
        return self.z48.execute(self.set_group_id, (arg0, ))

    def set_edit_mode(self, arg0):
        """Set Keygroup Edit Mode <Data2> = (0=SINGLE, 1=ALL, 2=ADD)
        """
        return self.z48.execute(self.set_edit_mode, (arg0, ))

    def set_low_note(self, arg0):
        """Set Low Note
        """
        return self.z48.execute(self.set_low_note, (arg0, ))

    def set_high_note(self, arg0):
        """Set High Note
        """
        return self.z48.execute(self.set_high_note, (arg0, ))

    def set_mute_group(self, arg0):
        """Set Mute Group <Data1> = (0=OFF, 1­64=value)
        """
        return self.z48.execute(self.set_mute_group, (arg0, ))

    def set_fx_override(self, arg0):
        """Set FX override <Data1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)
        """
        return self.z48.execute(self.set_fx_override, (arg0, ))

    def set_fx_send_level(self, arg0):
        """Set FX Send Level <Data1> = level in 10×dB (-600­+60)
        """
        return self.z48.execute(self.set_fx_send_level, (arg0, ))

    def set_zone_xfade(self, arg0):
        """Set Zone Crossfade <Data1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)
        """
        return self.z48.execute(self.set_zone_xfade, (arg0, ))

    def set_xfade_type(self, arg0):
        """Set Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)
        """
        return self.z48.execute(self.set_xfade_type, (arg0, ))

    def set_polyphony(self, arg0):
        """Set Polyphony
        """
        return self.z48.execute(self.set_polyphony, (arg0, ))

    def set_zone_xfade_ctrl_no(self, arg0):
        """Set Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)
        """
        return self.z48.execute(self.set_zone_xfade_ctrl_no, (arg0, ))

    def set_tune(self, arg0):
        """Set Cents Tune (0 ­ ±36)
        """
        return self.z48.execute(self.set_tune, (arg0, ))

    def set_level(self, arg0):
        """Set Keygroup Level <Data1> = value in 10×dB
        """
        return self.z48.execute(self.set_level, (arg0, ))

    def set_play_trigger(self):
        """Set Play Trigger <Data1> = (0=NOTE ON, 1=NOTE OFF)
        """
        return self.z48.execute(self.set_play_trigger, ())

    def set_play_trigger_vel(self, arg0):
        """Set Play Trigger Velocity <Data1> = (0=ON VEL, 1=OFF VEL, 2­129=0­127)
        """
        return self.z48.execute(self.set_play_trigger_vel, (arg0, ))

    def set_play_toggle_note(self, arg0):
        """Set Play Toggle Note <Data1> = (0=OFF, 1=ON)
        """
        return self.z48.execute(self.set_play_toggle_note, (arg0, ))

    def set_filter_mode(self, arg0, arg1):
        """Set Filter Mode (0=NORMAL, 1=TRIPLE(1), 2=TRIPLE(2), 3=TRIPLE(3)), type
        """
        return self.z48.execute(self.set_filter_mode, (arg0, arg1, ))

    def set_filter_cutoff(self, arg0, arg1):
        """Set Filter Cutoff Frequency
        """
        return self.z48.execute(self.set_filter_cutoff, (arg0, arg1, ))

    def set_filter_resonance(self, arg0, arg1):
        """Filter Resonance
        """
        return self.z48.execute(self.set_filter_resonance, (arg0, arg1, ))

    def set_filter_atten(self, arg0):
        """Set Filter Attenuation (one setting for all filters) <Data1> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)
        """
        return self.z48.execute(self.set_filter_atten, (arg0, ))

    def set_env_rate1(self, arg0, arg1):
        """Set Envelope Rate 1 (for AMP = Attack)(0=AMP, 1=FILTER, 2=AUX)
        """
        return self.z48.execute(self.set_env_rate1, (arg0, arg1, ))

    def set_env_level1(self, arg0, arg1):
        """Set Envelope Level 1 (FILTER and AUX only)
        """
        return self.z48.execute(self.set_env_level1, (arg0, arg1, ))

    def set_env_rate2(self, arg0, arg1):
        """Set Envelope Rate 2 (for AMP = Decay)
        """
        return self.z48.execute(self.set_env_rate2, (arg0, arg1, ))

    def set_env_level2(self, arg0, arg1):
        """Set Envelope Level 2 (for AMP = Sustain)
        """
        return self.z48.execute(self.set_env_level2, (arg0, arg1, ))

    def set_env_rate3(self, arg0, arg1):
        """Set Envelope Rate 3 (for AMP = Release)
        """
        return self.z48.execute(self.set_env_rate3, (arg0, arg1, ))

    def set_env_level3(self, arg0, arg1):
        """Set Envelope Level 3 (FILTER and AUX only)
        """
        return self.z48.execute(self.set_env_level3, (arg0, arg1, ))

    def set_env_rate4(self, arg0, arg1):
        """Set Envelope Rate 4 (FILTER and AUX only)
        """
        return self.z48.execute(self.set_env_rate4, (arg0, arg1, ))

    def set_env_level4(self, arg0, arg1):
        """Set Envelope Level 4 (FILTER and AUX only)
        """
        return self.z48.execute(self.set_env_level4, (arg0, arg1, ))

    def set_env_ref(self, arg0, arg1):
        """Set Envelope Reference (FILTER and AUX only)
        """
        return self.z48.execute(self.set_env_ref, (arg0, arg1, ))

    def set_attack_hold(self, arg0):
        """Set Attack Hold <Data1> = (0=OFF, 1=ON) (AMP only)
        """
        return self.z48.execute(self.set_attack_hold, (arg0, ))

    def set_lfo_rate(self, arg0, arg1):
        """Set LFO Rate (0: LFO1 1: LFO2), rate
        """
        return self.z48.execute(self.set_lfo_rate, (arg0, arg1, ))

    def set_lfo_delay(self, arg0, arg1):
        """Set LFO Delay <Data2> = delay
        """
        return self.z48.execute(self.set_lfo_delay, (arg0, arg1, ))

    def set_lfo_depth(self, arg0, arg1):
        """Set LFO Depth <Data2> = depth
        """
        return self.z48.execute(self.set_lfo_depth, (arg0, arg1, ))

    def set_lfo_waveform(self, arg0, arg1):
        """Set LFO Waveform <Data2> = waveform, (see Table 23)
        """
        return self.z48.execute(self.set_lfo_waveform, (arg0, arg1, ))

    def set_lfo_phase(self, arg0, arg1):
        """Set LFO Phase
        """
        return self.z48.execute(self.set_lfo_phase, (arg0, arg1, ))

