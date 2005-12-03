
""" Python equivalent of akai section keygrouptools

Keygroup manipulation
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Keygrouptools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x01', 'get_group_id', (), None)
          self.commands['\x13\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x02', 'get_edit_mode', (), None)
          self.commands['\x13\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x04', 'get_low_note', (), None)
          self.commands['\x13\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x05', 'get_high_note', (), None)
          self.commands['\x13\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x06', 'get_mute_group', (), None)
          self.commands['\x13\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x07 ', 'get_FX_override', (), None)
          self.commands['\x13\x07 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x08', 'get_FX_send_level', (), None)
          self.commands['\x13\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x09', 'get_zone_crossfade', (), None)
          self.commands['\x13\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x0A', 'get_crossfade_type', (), None)
          self.commands['\x13\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x0E', 'get_polyphoy', (), None)
          self.commands['\x13\x0E'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x0F', 'get_zone_crossfade_ctrl_no', (), None)
          self.commands['\x13\x0F'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x10', 'get_tune', (), None)
          self.commands['\x13\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x11 ', 'get_keygroup_level', (), None)
          self.commands['\x13\x11 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x18', 'get_play_trigger', (), None)
          self.commands['\x13\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x19', 'get_player_trigger_velocity', (), None)
          self.commands['\x13\x19'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x1A ', 'get_play_toggle_note', (), None)
          self.commands['\x13\x1A '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x20', 'get_filter', (), None)
          self.commands['\x13\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x21', 'get_filter_cutoff', (), None)
          self.commands['\x13\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x22', 'get_filter_resonance', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x23', 'get_filter_attenuation', (), None)
          self.commands['\x13\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x30', 'get_envelope_rate', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x30'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x31', 'get_envelope_level1', (), None)
          self.commands['\x13\x31'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x32', 'get_envelope_rate2', (), None)
          self.commands['\x13\x32'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x33', 'get_envelope_level2', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x33'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x34', 'get_envelope_rate3', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x34'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x35', 'get_envelope_level3', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x35'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x36', 'get_envelope_rate4', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x36'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x37', 'get_envelope_level4', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x37'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x42', 'get_envelope_reference', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x42'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x43 ', 'get_attack_hold', (), None)
          self.commands['\x13\x43 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x50', 'get_lfo_rate', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x50'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x51 ', 'get_lfo_delay', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x51 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x52 ', 'get_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x13\x52 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x53', 'get_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x53'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x54 ', 'get_lfo_phase', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x54 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x55', 'get_LFO_shift', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x55'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x56', 'get_LFO_midi_sync', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x56'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x57', 'get_midi_clock_sync_div', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x57'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x58 ', 'get_LFO_retrigger', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x58 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x13\x59', 'get_LFO_sync', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x13\x59'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x01', 'set_group_id', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x02', 'set_edit_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x04', 'set_low_note', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x05', 'set_high_note', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x06', 'set_mute_group', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x07', 'set_fx_override', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x08', 'set_fx_send_level', (aksy.devices.akai.sysex_types.SWORD,), None)
          self.commands['\x12\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x09', 'set_zone_xfade', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x0A', 'set_xfade_type', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x0E', 'set_polyphony', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x0E'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x0F', 'set_zone_xfade_ctrl_no', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x0F'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x10', 'set_tune', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x11', 'set_keygroup_level', (aksy.devices.akai.sysex_types.SWORD,), None)
          self.commands['\x12\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x18', 'set_play_trigger', (), None)
          self.commands['\x12\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x19', 'set_play_trigger_vel', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x19'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x1A ', 'set_play_toggle_note', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x1A '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x20', 'set_filter_mode', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x21', 'set_filter_cutoff', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x22', 'set_filter_resonance', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x23', 'set_filter_atten', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x30', 'set_env_rate1', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x30'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x31', 'set_env_level1', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x31'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x32', 'set_env_rate2', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x32'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x33', 'set_env_level2', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x33'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x34', 'set_env_rate3', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x34'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x35', 'set_env_level3', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x35'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x36', 'set_env_rate4', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x36'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x37', 'set_env_level4', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x37'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x42', 'set_env_ref', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x42'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x43', 'set_attack_hold', (aksy.devices.akai.sysex_types.BYTE,), None)
          self.commands['\x12\x43'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x50', 'set_lfo_rate', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x50'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x51', 'set_lfo_delay', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x51'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x52', 'set_lfo_depth', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x52'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x53', 'set_lfo_waveform', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x53'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x12\x54', 'set_lfo_phase', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
          self.commands['\x12\x54'] = comm

     def get_group_id(self):
          """Get Group ID

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x01')
          return self.z48.execute(comm, ())

     def get_edit_mode(self):
          """Get Keygroup Edit Mode <Reply1> = (0=SINGLE, 1=ALL, 2=ADD)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x02')
          return self.z48.execute(comm, ())

     def get_low_note(self):
          """Get Low Note

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x04')
          return self.z48.execute(comm, ())

     def get_high_note(self):
          """Get High Note

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x05')
          return self.z48.execute(comm, ())

     def get_mute_group(self):
          """Get Mute Group <Reply1> = (0=OFF, 1­64=value)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x06')
          return self.z48.execute(comm, ())

     def get_FX_override(self):
          """Get FX override <Reply1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x07 ')
          return self.z48.execute(comm, ())

     def get_FX_send_level(self):
          """Get FX Send Level <Reply1> = level in 10×dB (-600­+60)

          Returns:
               aksy.devices.akai.sysex_types.SWORD
          """
          comm = self.commands.get('\x13\x08')
          return self.z48.execute(comm, ())

     def get_zone_crossfade(self):
          """Get Zone Crossfade <Reply1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x09')
          return self.z48.execute(comm, ())

     def get_crossfade_type(self):
          """Get Crossfade type <Reply1> = (0=LIN, 1=EXP, 2=LOG)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x0A')
          return self.z48.execute(comm, ())

     def get_polyphoy(self):
          """Get Polyphony

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x0E')
          return self.z48.execute(comm, ())

     def get_zone_crossfade_ctrl_no(self):
          """Get Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x0F')
          return self.z48.execute(comm, ())

     def get_tune(self):
          """Get Cents Tune

          Returns:
               aksy.devices.akai.sysex_types.SBYTE
          """
          comm = self.commands.get('\x13\x10')
          return self.z48.execute(comm, ())

     def get_keygroup_level(self):
          """Get Keygroup Level (RT) <Reply> = value in 10×dB

          Returns:
               aksy.devices.akai.sysex_types.SWORD
          """
          comm = self.commands.get('\x13\x11 ')
          return self.z48.execute(comm, ())

     def get_play_trigger(self):
          """Get Play Trigger <Reply> = (0=NOTE ON, 1=NOTE OFF)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x18')
          return self.z48.execute(comm, ())

     def get_player_trigger_velocity(self):
          """Get Play Trigger Velocity (0­129) <Reply> = (0=ON VEL, 1=OFF VEL, 2­129=0­127)

          Returns:
               aksy.devices.akai.sysex_types.WORD
          """
          comm = self.commands.get('\x13\x19')
          return self.z48.execute(comm, ())

     def get_play_toggle_note(self):
          """Get Play Toggle Note <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x1A ')
          return self.z48.execute(comm, ())

     def get_filter(self):
          """Get Filter <Data1> = Filter block (0=N

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x20')
          return self.z48.execute(comm, ())

     def get_filter_cutoff(self):
          """Get Filter Cutoff Frequency. Data1= filter 0-3 reply: (0-100) BYTE

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x21')
          return self.z48.execute(comm, ())

     def get_filter_resonance(self, arg0):
          """Get Filter Resonance (0-3) (0-60)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x22')
          return self.z48.execute(comm, (arg0, ))

     def get_filter_attenuation(self):
          """Get Filter Attenuation (one setting for all filters) <Reply> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x23')
          return self.z48.execute(comm, ())

     def get_envelope_rate(self, arg0):
          """Get Envelope Rate1 <Data1> = Envelope (0=AMP, 1=FILTER, 2=AUX) 0­100) Get Envelope Rate 1 (for AMP = Attack)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x30')
          return self.z48.execute(comm, (arg0, ))

     def get_envelope_level1(self):
          """Get Envelope Level 1 (FILTER and AUX only)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x31')
          return self.z48.execute(comm, ())

     def get_envelope_rate2(self):
          """Get Envelope Rate 2 (for AMP = Decay)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x32')
          return self.z48.execute(comm, ())

     def get_envelope_level2(self, arg0):
          """Get Envelope Level 2 (for AMP = Sustain)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x33')
          return self.z48.execute(comm, (arg0, ))

     def get_envelope_rate3(self, arg0):
          """Get Envelope Rate 3 (for AMP = Release)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x34')
          return self.z48.execute(comm, (arg0, ))

     def get_envelope_level3(self, arg0):
          """Get Envelope Level 3 (FILTER and AUX only)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x35')
          return self.z48.execute(comm, (arg0, ))

     def get_envelope_rate4(self, arg0):
          """Get Envelope Rate 4 (FILTER and AUX only)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x36')
          return self.z48.execute(comm, (arg0, ))

     def get_envelope_level4(self, arg0):
          """Get Envelope Level 4 (FILTER and AUX only)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x37')
          return self.z48.execute(comm, (arg0, ))

     def get_envelope_reference(self, arg0):
          """Get Envelope Reference (FILTER and AUX only)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x42')
          return self.z48.execute(comm, (arg0, ))

     def get_attack_hold(self):
          """Get Attack Hold <Reply> = (0=OFF, 1=ON) (AMP only)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x43 ')
          return self.z48.execute(comm, ())

     def get_lfo_rate(self, arg0):
          """Get LFO Rate (0=LFO1, 1=LFO2)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x50')
          return self.z48.execute(comm, (arg0, ))

     def get_lfo_delay(self, arg0):
          """Get LFO Delay (0=LFO1, 1=LFO2)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x51 ')
          return self.z48.execute(comm, (arg0, ))

     def get_lfo_depth(self, arg0, arg1):
          """Get LFO Depth (0=LFO1, 1=LFO2)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x52 ')
          return self.z48.execute(comm, (arg0, arg1, ))

     def get_lfo_waveform(self, arg0):
          """Get LFO Waveform <Reply> = waveform (0=LFO1, 1=LFO2)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x53')
          return self.z48.execute(comm, (arg0, ))

     def get_lfo_phase(self, arg0):
          """Get LFO Phase(0=LFO1, 1=LFO2)

          Returns:
               aksy.devices.akai.sysex_types.WORD
          """
          comm = self.commands.get('\x13\x54 ')
          return self.z48.execute(comm, (arg0, ))

     def get_LFO_shift(self, arg0):
          """Get LFO Shift(0=LFO1, 1=LFO2)

          Returns:
               aksy.devices.akai.sysex_types.SBYTE
          """
          comm = self.commands.get('\x13\x55')
          return self.z48.execute(comm, (arg0, ))

     def get_LFO_midi_sync(self, arg0):
          """Get LFO MIDI Sync (0=LFO1, 1=LFO2) <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x56')
          return self.z48.execute(comm, (arg0, ))

     def get_midi_clock_sync_div(self, arg0):
          """Get MIDI Clock Sync Division <Reply> = value, where 0=8 cy/bt, 1=6cy/bt, 2=4cy/bt, 3=3cy/bt, 4=2cy/bt, 5=1cy/bt 6=2 bt/cy, 7=3bt/cy, ..., 68=64bt/cy

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x57')
          return self.z48.execute(comm, (arg0, ))

     def get_LFO_retrigger(self, arg0):
          """Get LFO Re-trigger <Data1>0: LFO1 1: LF02 <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x58 ')
          return self.z48.execute(comm, (arg0, ))

     def get_LFO_sync(self, arg0):
          """Get LFO sync (i.e., all voices in program locked to same LFO)

          Returns:
               aksy.devices.akai.sysex_types.BYTE
          """
          comm = self.commands.get('\x13\x59')
          return self.z48.execute(comm, (arg0, ))

     def set_group_id(self, arg0):
          """Set Group ID
          """
          comm = self.commands.get('\x12\x01')
          return self.z48.execute(comm, (arg0, ))

     def set_edit_mode(self, arg0):
          """Set Keygroup Edit Mode <Data2> = (0=SINGLE, 1=ALL, 2=ADD)
          """
          comm = self.commands.get('\x12\x02')
          return self.z48.execute(comm, (arg0, ))

     def set_low_note(self, arg0):
          """Set Low Note
          """
          comm = self.commands.get('\x12\x04')
          return self.z48.execute(comm, (arg0, ))

     def set_high_note(self, arg0):
          """Set High Note
          """
          comm = self.commands.get('\x12\x05')
          return self.z48.execute(comm, (arg0, ))

     def set_mute_group(self, arg0):
          """Set Mute Group <Data1> = (0=OFF, 1­64=value)
          """
          comm = self.commands.get('\x12\x06')
          return self.z48.execute(comm, (arg0, ))

     def set_fx_override(self, arg0):
          """Set FX override <Data1> = (0=OFF, 1=A, 2=B, 3=C, 4=D, 5=AB, 6=CD, 7=MULTI)
          """
          comm = self.commands.get('\x12\x07')
          return self.z48.execute(comm, (arg0, ))

     def set_fx_send_level(self, arg0):
          """Set FX Send Level <Data1> = level in 10×dB (-600­+60)
          """
          comm = self.commands.get('\x12\x08')
          return self.z48.execute(comm, (arg0, ))

     def set_zone_xfade(self, arg0):
          """Set Zone Crossfade <Data1> = (0=OFF, 1=VELOCITY, 2=REAL-TIME)
          """
          comm = self.commands.get('\x12\x09')
          return self.z48.execute(comm, (arg0, ))

     def set_xfade_type(self, arg0):
          """Set Crossfade type <Data1> = (0=LIN, 1=EXP, 2=LOG)
          """
          comm = self.commands.get('\x12\x0A')
          return self.z48.execute(comm, (arg0, ))

     def set_polyphony(self, arg0):
          """Set Polyphony
          """
          comm = self.commands.get('\x12\x0E')
          return self.z48.execute(comm, (arg0, ))

     def set_zone_xfade_ctrl_no(self, arg0):
          """Set Zone Crossfade Source Controller Number (only used when Zone Crossfade Source is MIDI CTRL)
          """
          comm = self.commands.get('\x12\x0F')
          return self.z48.execute(comm, (arg0, ))

     def set_tune(self, arg0):
          """Set Cents Tune (0 ­ ±3600)
          """
          comm = self.commands.get('\x12\x10')
          return self.z48.execute(comm, (arg0, ))

     def set_keygroup_level(self, arg0):
          """Set Keygroup Level <Data1> = value in 10×dB
          """
          comm = self.commands.get('\x12\x11')
          return self.z48.execute(comm, (arg0, ))

     def set_play_trigger(self):
          """Set Play Trigger <Data1> = (0=NOTE ON, 1=NOTE OFF)
          """
          comm = self.commands.get('\x12\x18')
          return self.z48.execute(comm, ())

     def set_play_trigger_vel(self, arg0):
          """Set Play Trigger Velocity <Data1> = (0=ON VEL, 1=OFF VEL, 2­129=0­127)
          """
          comm = self.commands.get('\x12\x19')
          return self.z48.execute(comm, (arg0, ))

     def set_play_toggle_note(self, arg0):
          """Set Play Toggle Note <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x12\x1A ')
          return self.z48.execute(comm, (arg0, ))

     def set_filter_mode(self, arg0, arg1):
          """Set Filter Mode (0=NORMAL, 1=TRIPLE(1), 2=TRIPLE(2), 3=TRIPLE(3)), type
          """
          comm = self.commands.get('\x12\x20')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_filter_cutoff(self, arg0, arg1):
          """Set Filter Cutoff Frequency
          """
          comm = self.commands.get('\x12\x21')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_filter_resonance(self, arg0, arg1):
          """Filter Resonance
          """
          comm = self.commands.get('\x12\x22')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_filter_atten(self, arg0):
          """Set Filter Attenuation (one setting for all filters) <Data1> = (0, 1, 2, 3, 4, 5 = 0dB, 6dB, 12dB, 18dB, 24dB, 30dB)
          """
          comm = self.commands.get('\x12\x23')
          return self.z48.execute(comm, (arg0, ))

     def set_env_rate1(self, arg0, arg1):
          """Set Envelope Rate 1 (for AMP = Attack)(0=AMP, 1=FILTER, 2=AUX)
          """
          comm = self.commands.get('\x12\x30')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_level1(self, arg0, arg1):
          """Set Envelope Level 1 (FILTER and AUX only)
          """
          comm = self.commands.get('\x12\x31')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_rate2(self, arg0, arg1):
          """Set Envelope Rate 2 (for AMP = Decay)
          """
          comm = self.commands.get('\x12\x32')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_level2(self, arg0, arg1):
          """Set Envelope Level 2 (for AMP = Sustain)
          """
          comm = self.commands.get('\x12\x33')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_rate3(self, arg0, arg1):
          """Set Envelope Rate 3 (for AMP = Release)
          """
          comm = self.commands.get('\x12\x34')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_level3(self, arg0, arg1):
          """Set Envelope Level 3 (FILTER and AUX only)
          """
          comm = self.commands.get('\x12\x35')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_rate4(self, arg0, arg1):
          """Set Envelope Rate 4 (FILTER and AUX only)
          """
          comm = self.commands.get('\x12\x36')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_level4(self, arg0, arg1):
          """Set Envelope Level 4 (FILTER and AUX only)
          """
          comm = self.commands.get('\x12\x37')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_env_ref(self, arg0, arg1):
          """Set Envelope Reference (FILTER and AUX only)
          """
          comm = self.commands.get('\x12\x42')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_attack_hold(self, arg0):
          """Set Attack Hold <Data1> = (0=OFF, 1=ON) (AMP only)
          """
          comm = self.commands.get('\x12\x43')
          return self.z48.execute(comm, (arg0, ))

     def set_lfo_rate(self, arg0, arg1):
          """Set LFO Rate (0: LFO1 1: LFO2), rate
          """
          comm = self.commands.get('\x12\x50')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_lfo_delay(self, arg0, arg1):
          """Set LFO Delay <Data2> = delay
          """
          comm = self.commands.get('\x12\x51')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_lfo_depth(self, arg0, arg1):
          """Set LFO Depth <Data2> = depth
          """
          comm = self.commands.get('\x12\x52')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_lfo_waveform(self, arg0, arg1):
          """Set LFO Waveform <Data2> = waveform, (see Table 23)
          """
          comm = self.commands.get('\x12\x53')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_lfo_phase(self, arg0, arg1):
          """Set LFO Phase
          """
          comm = self.commands.get('\x12\x54')
          return self.z48.execute(comm, (arg0, arg1, ))

