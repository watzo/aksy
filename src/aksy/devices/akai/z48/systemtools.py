
""" Python equivalent of akai section systemtools

Methods to manipulate system parameters
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex

class Systemtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x00', 'get_os_software_version', (), None)
          self.commands['\x04\x00'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x01', 'get_os_subversion', (), None)
          self.commands['\x04\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x04', 'get_sampler_model', (), None)
          self.commands['\x04\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x08', 'get_supported_filetypes', (), None)
          self.commands['\x04\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x10', 'get_perc_free_wave_mem', (), None)
          self.commands['\x04\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x11', 'get_perc_free_cpu_mem', (), None)
          self.commands['\x04\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x12', 'get_wave_mem_size', (), None)
          self.commands['\x04\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x13', 'get_free_wave_mem_size', (), None)
          self.commands['\x04\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x18', 'clear_sampler_mem', (), None)
          self.commands['\x04\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x19', 'purge_unused', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x04\x19'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x1A', 'tag_unused', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x04\x1A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x20', 'compact_wave_mem', (), None)
          self.commands['\x04\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x21', 'cancel_compact_wave_mem', (), None)
          self.commands['\x04\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x22 ', 'get_compact_wave_mem_progress', (), None)
          self.commands['\x04\x22 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x30 ', 'get_async_operation_state', (), None)
          self.commands['\x04\x30 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x04\x31 ', 'cancel_curr_async_operation', (), None)
          self.commands['\x04\x31 '] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x01', 'get_sampler_name', (), None)
          self.commands['\x07\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x02', 'get_scsi_id', (), None)
          self.commands['\x07\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x03', 'get_master_tune', (), None)
          self.commands['\x07\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x04', 'get_master_level', (), None)
          self.commands['\x07\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x05', 'get_midi_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x07\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x06', 'is_qlink_local_ctrl_enabled', (), None)
          self.commands['\x07\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x07', 'is_default_items_enabled', (), None)
          self.commands['\x07\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x08', 'get_midi_file_save_format', (), None)
          self.commands['\x07\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x09', 'get_cdr_write_speed', (), None)
          self.commands['\x07\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x0A', 'get_cdr_write_mode', (), None)
          self.commands['\x07\x0A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x10', 'is_front_panel_locked', (), None)
          self.commands['\x07\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x11', 'get_display_contrast', (), None)
          self.commands['\x07\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x12', 'get_note_display', (), None)
          self.commands['\x07\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x13', 'get_date_format', (), None)
          self.commands['\x07\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x14', 'get_time_format', (), None)
          self.commands['\x07\x14'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x18', 'get_waveform_view_scale', (), None)
          self.commands['\x07\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x19', 'get_waveform_view_type', (), None)
          self.commands['\x07\x19'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x1A', 'get_waveform_view_fill', (), None)
          self.commands['\x07\x1A'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x1B', 'get_item_sort_mode', (), None)
          self.commands['\x07\x1B'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x20', 'get_year', (), None)
          self.commands['\x07\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x21', 'get_month', (), None)
          self.commands['\x07\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x22', 'get_day', (), None)
          self.commands['\x07\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x23', 'get_day_of_week', (), None)
          self.commands['\x07\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x24', 'get_hours', (), None)
          self.commands['\x07\x24'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x25', 'get_mins', (), None)
          self.commands['\x07\x25'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x26', 'get_secs', (), None)
          self.commands['\x07\x26'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x30', 'get_system_clock', (), None)
          self.commands['\x07\x30'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x31', 'get_dig_sync', (), None)
          self.commands['\x07\x31'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x32', 'get_dig_format', (), None)
          self.commands['\x07\x32'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x33', 'get_adat_main_out', (), None)
          self.commands['\x07\x33'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x40', 'get_play_mode', (), None)
          self.commands['\x07\x40'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x41', 'get_prog_monitor_mode', (), None)
          self.commands['\x07\x41'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x42', 'get_sample_monitor_mode', (), None)
          self.commands['\x07\x42'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x48', 'get_play_key_note', (), None)
          self.commands['\x07\x48'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x49', 'get_play_key_velocity', (), None)
          self.commands['\x07\x49'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x4a', 'get_play_key_midi_channel', (), None)
          self.commands['\x07\x4a'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x4b', 'get_play_key_echo', (), None)
          self.commands['\x07\x4b'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x4c', 'get_prog_change_enable', (), None)
          self.commands['\x07\x4c'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x4d', 'get_autoload_enable', (), None)
          self.commands['\x07\x4d'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x50', 'get_global_pad_mode', (), None)
          self.commands['\x07\x50'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x51', 'get_pad_midi_channel', (), None)
          self.commands['\x07\x51'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x52', 'get_pad_sensitivity', (), None)
          self.commands['\x07\x52'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x53', 'get_def_note_assign', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x07\x53'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x07\x54', 'get_chrom_start_note', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x07\x54'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x01', 'set_sampler_name', (aksy.devices.akai.sysex.STRING,), None)
          self.commands['\x06\x01'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x02', 'set_scsi_id', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x02'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x03', 'set_master_tune', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x03'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x04', 'set_master_level', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x04'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x05', 'set_midi_out_thru', (), None)
          self.commands['\x06\x05'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x06', 'set_qlink_local_control', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x06\x06'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x07', 'set_create_default_items', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x06\x07'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x08', 'set_midi_file_save_format', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x08'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x09', 'set_cdr_write_speed', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x09'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x0a', 'set_cdr_write_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x0a'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x10', 'set_front_panel_lockout_state', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x10'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x11', 'set_display_contrast', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x11'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x12', 'set_note_display', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x12'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x13', 'set_date_display_format', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x13'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x14', 'set_time_display_format', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x14'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x18', 'set_waveform_view_scale', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x18'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x19', 'set_waveform_view_type', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x19'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x1a', 'set_waveform_view_fill', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x06\x1a'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x1b', 'set_item_sort_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x1b'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x20', 'set_year', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x20'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x21', 'set_month', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x21'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x22', 'set_day', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x22'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x23', 'set_day_of_week', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x23'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x24', 'set_hours', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x24'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x25', 'set_minutes', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x25'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x26', 'set_seconds', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x26'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x30', 'set_system_clock', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x30'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x31', 'set_digital_out_sync', (), None)
          self.commands['\x06\x31'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x32', 'set_digital_format', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x32'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x33', 'set_adat_main_out', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x33'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x40', 'set_play_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x40'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x41', 'set_program_monitor_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x41'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x42', 'set_sample_monitor_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x42'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x48', 'set_play_key_note', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x48'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x49', 'set_play_key_velocity', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x49'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x4a', 'set_play_key_midi_channel', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x4a'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x4b', 'set_play_key_echo', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x06\x4b'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x4c', 'set_program_change_enable', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x06\x4c'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x4d', 'set_autoload_enable', (aksy.devices.akai.sysex.BOOL,), None)
          self.commands['\x06\x4d'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x05\x50', 'set_global_pad_mode', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x05\x50'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x51', 'set_pad_midi_channel', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x51'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x52', 'set_pad_sensitivity', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x06\x52'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x53', 'set_default_note_assignment', (aksy.devices.akai.sysex.BYTE, aksy.devices.akai.sysex.BYTE), None)
          self.commands['\x06\x53'] = comm
          comm = aksy.devices.akai.sysex.Command('_', '\x06\x54', 'set_chromatic_start_note', (aksy.devices.akai.sysex.BYTE,), None)
          self.commands['\x06\x54'] = comm

     def get_os_software_version(self):
          """Get Operating System Software Version

          Returns:
               aksy.devices.akai.sysex.BYTE
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x00')
          return self.z48.execute(comm, ())

     def get_os_subversion(self):
          """Get the Sub-Version of the Operating System

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x01')
          return self.z48.execute(comm, ())

     def get_sampler_model(self):
          """Get Sampler Model

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x04')
          return self.z48.execute(comm, ())

     def get_supported_filetypes(self):
          """Get List of supported filetypes

          Returns:
               aksy.devices.akai.sysex.STRINGARRAY
          """
          comm = self.commands.get('\x04\x08')
          return self.z48.execute(comm, ())

     def get_perc_free_wave_mem(self):
          """Get the percentage free Wave memory

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x10')
          return self.z48.execute(comm, ())

     def get_perc_free_cpu_mem(self):
          """Get the percentage free CPU memory

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x11')
          return self.z48.execute(comm, ())

     def get_wave_mem_size(self):
          """Get the total number of kilobytes of Wave memory

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x04\x12')
          return self.z48.execute(comm, ())

     def get_free_wave_mem_size(self):
          """Get the number of kilobytes of free Wave memory

          Returns:
               aksy.devices.akai.sysex.DWORD
          """
          comm = self.commands.get('\x04\x13')
          return self.z48.execute(comm, ())

     def clear_sampler_mem(self):
          """Clear Sampler Memory (delete all items from memory)
          """
          comm = self.commands.get('\x04\x18')
          return self.z48.execute(comm, ())

     def purge_unused(self, arg0):
          """Purge Unused Items <Data1> = (0=SAMPLE, 1=PROGRAM)
          """
          comm = self.commands.get('\x04\x19')
          return self.z48.execute(comm, (arg0, ))

     def tag_unused(self, arg0):
          """Tag Unused Items <Data1> = (0=SAMPLE, 1=PROGRAM)
          """
          comm = self.commands.get('\x04\x1A')
          return self.z48.execute(comm, (arg0, ))

     def compact_wave_mem(self):
          """Start Compact Wave Memory
          """
          comm = self.commands.get('\x04\x20')
          return self.z48.execute(comm, ())

     def cancel_compact_wave_mem(self):
          """Cancel Compact Wave Memory
          """
          comm = self.commands.get('\x04\x21')
          return self.z48.execute(comm, ())

     def get_compact_wave_mem_progress(self):
          """Get Compact Wave Memory Progress (%)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x22 ')
          return self.z48.execute(comm, ())

     def get_async_operation_state(self):
          """Get State of Asynchronous Operation ERROR 'operation is pending' or DONE

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x04\x30 ')
          return self.z48.execute(comm, ())

     def cancel_curr_async_operation(self):
          """Cancel Current Asynchronous Operation
          """
          comm = self.commands.get('\x04\x31 ')
          return self.z48.execute(comm, ())

     def get_sampler_name(self):
          """Get Sampler Name

          Returns:
               aksy.devices.akai.sysex.STRING
          """
          comm = self.commands.get('\x07\x01')
          return self.z48.execute(comm, ())

     def get_scsi_id(self):
          """Get SCSI self ID

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x02')
          return self.z48.execute(comm, ())

     def get_master_tune(self):
          """Get Master Tune

          Returns:
               aksy.devices.akai.sysex.SWORD
          """
          comm = self.commands.get('\x07\x03')
          return self.z48.execute(comm, ())

     def get_master_level(self):
          """Get Master Level <Reply> = (-42 dB ­ 0dB in 6dB steps)(0=-42 dB, 1=-36dB, ..., 7=0dB)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x04')
          return self.z48.execute(comm, ())

     def get_midi_mode(self, arg0):
          """Get MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B) <Reply> = (0=OUT, 1=THRUA, 2=THRUB)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x05')
          return self.z48.execute(comm, (arg0, ))

     def is_qlink_local_ctrl_enabled(self):
          """Get Qlink Local Control <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x06')
          return self.z48.execute(comm, ())

     def is_default_items_enabled(self):
          """Get Create Default Items at Startup <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x07')
          return self.z48.execute(comm, ())

     def get_midi_file_save_format(self):
          """Get MIDI file save format

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x08')
          return self.z48.execute(comm, ())

     def get_cdr_write_speed(self):
          """Get CD-R write speed (0=×1, 1=×2, 2=×4, 3=×6, 4=×8, 5=×12, 6=×16, 7=MAX)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x09')
          return self.z48.execute(comm, ())

     def get_cdr_write_mode(self):
          """Get CD-R write mode <Reply> = (0=TEST+WRITE, 1=TEST ONLY, 2=WRITE ONLY)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x0A')
          return self.z48.execute(comm, ())

     def is_front_panel_locked(self):
          """Get Front panel lock-out state

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x10')
          return self.z48.execute(comm, ())

     def get_display_contrast(self):
          """Get Display Contrast

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x11')
          return self.z48.execute(comm, ())

     def get_note_display(self):
          """Get Note Display <Reply> = (0=NUMBER, 1=NAME)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x12')
          return self.z48.execute(comm, ())

     def get_date_format(self):
          """Get Date Display Format  <Reply> = (0=DDMMYY, 1=MMDDYY, 2=YYMMDD)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x13')
          return self.z48.execute(comm, ())

     def get_time_format(self):
          """Get Time Display Format <Reply> = (0=12HOUR, 1=24HOUR)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x14')
          return self.z48.execute(comm, ())

     def get_waveform_view_scale(self):
          """Get Waveform View Scale <Reply> = (0=LINEAR, 1=LOG)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x18')
          return self.z48.execute(comm, ())

     def get_waveform_view_type(self):
          """Get Waveform View Type <Reply> = (0=RECTIFIED, 1=BIPOLAR)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x19')
          return self.z48.execute(comm, ())

     def get_waveform_view_fill(self):
          """Get Waveform View Fill <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x1A')
          return self.z48.execute(comm, ())

     def get_item_sort_mode(self):
          """Get Item Sort Mode <Reply> = (0=ALPHABETIC, 1=MEMORY)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x1B')
          return self.z48.execute(comm, ())

     def get_year(self):
          """Get Year

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x20')
          return self.z48.execute(comm, ())

     def get_month(self):
          """Get Month

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x21')
          return self.z48.execute(comm, ())

     def get_day(self):
          """Get Day

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x22')
          return self.z48.execute(comm, ())

     def get_day_of_week(self):
          """Get Day of Week (0=SUN)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x23')
          return self.z48.execute(comm, ())

     def get_hours(self):
          """Get Hours

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x24')
          return self.z48.execute(comm, ())

     def get_mins(self):
          """Get Minutes

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x25')
          return self.z48.execute(comm, ())

     def get_secs(self):
          """Get Seconds

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x26')
          return self.z48.execute(comm, ())

     def get_system_clock(self):
          """Get System Clock <Reply> = (0=44·1kHz, 1=48kHz, 2=96kHz)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x30')
          return self.z48.execute(comm, ())

     def get_dig_sync(self):
          """Get Digital Out Sync (0=INTERNAL, 1=DIGITAL IN, 2=ADAT IN, 3=WORDCLOCK)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x31')
          return self.z48.execute(comm, ())

     def get_dig_format(self):
          """Get Digital Format <Reply> = (0=PRO, 1=CONSUMER)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x32')
          return self.z48.execute(comm, ())

     def get_adat_main_out(self):
          """Get ADAT Main Out <Reply> = (0=L/R, 1=1/2)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x33')
          return self.z48.execute(comm, ())

     def get_play_mode(self):
          """Get Play Mode (0=Multi, 1=Program; 2=Sample; 3=Muted), handle of item which is the active Play Item

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x40')
          return self.z48.execute(comm, ())

     def get_prog_monitor_mode(self):
          """Get Program Monitor Mode  (0=Multi, 1=Program(OMNI))

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x41')
          return self.z48.execute(comm, ())

     def get_sample_monitor_mode(self):
          """Get Sample Monitor Mode (0=Multi, 1=Program; 2=Sample(OMNI))

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x42')
          return self.z48.execute(comm, ())

     def get_play_key_note(self):
          """Get Play Key Note

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x48')
          return self.z48.execute(comm, ())

     def get_play_key_velocity(self):
          """Get Play Key Velocity

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x49')
          return self.z48.execute(comm, ())

     def get_play_key_midi_channel(self):
          """Get Play Key Midi Channel <Reply> = (1A=0, 2A=1, ..., 16B=31)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x4a')
          return self.z48.execute(comm, ())

     def get_play_key_echo(self):
          """Get Play Key Echo <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x07\x4b')
          return self.z48.execute(comm, ())

     def get_prog_change_enable(self):
          """Get Program Change Enable <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x07\x4c')
          return self.z48.execute(comm, ())

     def get_autoload_enable(self):
          """Get Autoload Enable <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.devices.akai.sysex.BOOL
          """
          comm = self.commands.get('\x07\x4d')
          return self.z48.execute(comm, ())

     def get_global_pad_mode(self):
          """Get Global Pad Mode <Reply> = (0=DEFAULT, 1=CHROMATIC)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x50')
          return self.z48.execute(comm, ())

     def get_pad_midi_channel(self):
          """Get MIDI Channel for MPC Pad

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x51')
          return self.z48.execute(comm, ())

     def get_pad_sensitivity(self):
          """Get Pad Sensitivity <Data1> = Pad <Reply> = Sensitivity (0­100 = 100%­200%)

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x52')
          return self.z48.execute(comm, ())

     def get_def_note_assign(self, arg0):
          """Get Default Note Assignment <Data1> = Pad

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x53')
          return self.z48.execute(comm, (arg0, ))

     def get_chrom_start_note(self, arg0):
          """Get Default Note Assignment <Data1> = Pad

          Returns:
               aksy.devices.akai.sysex.BYTE
          """
          comm = self.commands.get('\x07\x54')
          return self.z48.execute(comm, (arg0, ))

     def set_sampler_name(self, arg0):
          """Set Sampler Name
          """
          comm = self.commands.get('\x06\x01')
          return self.z48.execute(comm, (arg0, ))

     def set_scsi_id(self, arg0):
          """Set SCSI ID
          """
          comm = self.commands.get('\x06\x02')
          return self.z48.execute(comm, (arg0, ))

     def set_master_tune(self, arg0):
          """Set Master Tune
          """
          comm = self.commands.get('\x06\x03')
          return self.z48.execute(comm, (arg0, ))

     def set_master_level(self, arg0):
          """Set Master Level <Data1> = (-42dB ­ 0dB in 6dB * 7 steps)
          """
          comm = self.commands.get('\x06\x04')
          return self.z48.execute(comm, (arg0, ))

     def set_midi_out_thru(self):
          """Set MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B), <Data2> = (0=OUT, 1=THRUA, 2=THRUB)
          """
          comm = self.commands.get('\x06\x05')
          return self.z48.execute(comm, ())

     def set_qlink_local_control(self, arg0):
          """Set Qlink Local Control
          """
          comm = self.commands.get('\x06\x06')
          return self.z48.execute(comm, (arg0, ))

     def set_create_default_items(self, arg0):
          """Set Create Default Items at Startup
          """
          comm = self.commands.get('\x06\x07')
          return self.z48.execute(comm, (arg0, ))

     def set_midi_file_save_format(self, arg0):
          """Set MIDI file save format
          """
          comm = self.commands.get('\x06\x08')
          return self.z48.execute(comm, (arg0, ))

     def set_cdr_write_speed(self, arg0):
          """Set CD-R write speed <Data1> = (0=×1, 1=×2, 2=×4, 3=×6, 4=×8, 5=×12, 6=×16, 7=MAX)
          """
          comm = self.commands.get('\x06\x09')
          return self.z48.execute(comm, (arg0, ))

     def set_cdr_write_mode(self, arg0):
          """Set CD-R write mode <Data1> = (0=TEST+WRITE, 1=TEST ONLY, 2=WRITE ONLY)
          """
          comm = self.commands.get('\x06\x0a')
          return self.z48.execute(comm, (arg0, ))

     def set_front_panel_lockout_state(self, arg0):
          """Set Front panel lock-out state <Data1> = (0=NORMAL; 1=LOCKED)
          """
          comm = self.commands.get('\x06\x10')
          return self.z48.execute(comm, (arg0, ))

     def set_display_contrast(self, arg0):
          """  Set Display Contrast
          """
          comm = self.commands.get('\x06\x11')
          return self.z48.execute(comm, (arg0, ))

     def set_note_display(self, arg0):
          """Set Note Display <Data1> = (0=NUMBER, 1=NAME)
          """
          comm = self.commands.get('\x06\x12')
          return self.z48.execute(comm, (arg0, ))

     def set_date_display_format(self, arg0):
          """Set Date Display Format <Data1> = (0=DDMMYY, 1=MMDDYY, 2=YYMMDD)
          """
          comm = self.commands.get('\x06\x13')
          return self.z48.execute(comm, (arg0, ))

     def set_time_display_format(self, arg0):
          """Set Time Display Format <Data1> = (0=12HOUR, 1=24HOUR)
          """
          comm = self.commands.get('\x06\x14')
          return self.z48.execute(comm, (arg0, ))

     def set_waveform_view_scale(self, arg0):
          """Set Waveform View Scale <Data1> = (0=LINEAR, 1=LOG)
          """
          comm = self.commands.get('\x06\x18')
          return self.z48.execute(comm, (arg0, ))

     def set_waveform_view_type(self, arg0):
          """Set Waveform View Type <Data1> = (0=RECTIFIED, 1=BIPOLAR)
          """
          comm = self.commands.get('\x06\x19')
          return self.z48.execute(comm, (arg0, ))

     def set_waveform_view_fill(self, arg0):
          """Set Waveform View Fill <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x06\x1a')
          return self.z48.execute(comm, (arg0, ))

     def set_item_sort_mode(self, arg0):
          """Set Item Sort Mode <Data1> = (0=ALPHABETIC, 1=MEMORY)
          """
          comm = self.commands.get('\x06\x1b')
          return self.z48.execute(comm, (arg0, ))

     def set_year(self, arg0):
          """Set Year
          """
          comm = self.commands.get('\x06\x20')
          return self.z48.execute(comm, (arg0, ))

     def set_month(self, arg0):
          """Set Month
          """
          comm = self.commands.get('\x06\x21')
          return self.z48.execute(comm, (arg0, ))

     def set_day(self, arg0):
          """Set Day
          """
          comm = self.commands.get('\x06\x22')
          return self.z48.execute(comm, (arg0, ))

     def set_day_of_week(self, arg0):
          """Set Day of Week (0=SUN)
          """
          comm = self.commands.get('\x06\x23')
          return self.z48.execute(comm, (arg0, ))

     def set_hours(self, arg0):
          """Set Hours
          """
          comm = self.commands.get('\x06\x24')
          return self.z48.execute(comm, (arg0, ))

     def set_minutes(self, arg0):
          """Set Minutes
          """
          comm = self.commands.get('\x06\x25')
          return self.z48.execute(comm, (arg0, ))

     def set_seconds(self, arg0):
          """Set Seconds
          """
          comm = self.commands.get('\x06\x26')
          return self.z48.execute(comm, (arg0, ))

     def set_system_clock(self, arg0):
          """Set System Clock <Data1> = (0=44·1kHz, 1=48kHz, 2=96kHz)
          """
          comm = self.commands.get('\x06\x30')
          return self.z48.execute(comm, (arg0, ))

     def set_digital_out_sync(self):
          """Set Digital Out Sync <Data1> = (0=INTERNAL, 1=DIGITAL IN, 2=ADAT IN, 3=WORDCLOCK) BYTE
          """
          comm = self.commands.get('\x06\x31')
          return self.z48.execute(comm, ())

     def set_digital_format(self, arg0):
          """Set Digital Format <Data1> = (0=PRO, 1=CONSUMER)
          """
          comm = self.commands.get('\x06\x32')
          return self.z48.execute(comm, (arg0, ))

     def set_adat_main_out(self, arg0):
          """Set ADAT Main Out <Data1> = (0=L/R, 1=1/2)
          """
          comm = self.commands.get('\x06\x33')
          return self.z48.execute(comm, (arg0, ))

     def set_play_mode(self, arg0):
          """Set Play Mode <Data1> = (0=Multi, 1=Program; 2=Sample; 3=Muted) <Data2> = handle of item to become active Play Item
          """
          comm = self.commands.get('\x06\x40')
          return self.z48.execute(comm, (arg0, ))

     def set_program_monitor_mode(self, arg0):
          """Set Program Monitor Mode <Data1> = (0=Multi, 1=Program(OMNI))
          """
          comm = self.commands.get('\x06\x41')
          return self.z48.execute(comm, (arg0, ))

     def set_sample_monitor_mode(self, arg0):
          """Set Sample Monitor Mode <Data1> = (0=Multi, 1=Program; 2=Sample(OMNI))
          """
          comm = self.commands.get('\x06\x42')
          return self.z48.execute(comm, (arg0, ))

     def set_play_key_note(self, arg0):
          """Set Play Key Note
          """
          comm = self.commands.get('\x06\x48')
          return self.z48.execute(comm, (arg0, ))

     def set_play_key_velocity(self, arg0):
          """Set Play Key Velocity
          """
          comm = self.commands.get('\x06\x49')
          return self.z48.execute(comm, (arg0, ))

     def set_play_key_midi_channel(self, arg0):
          """Set Play Key Midi Channel <Data1> = (1A=0, 2A=1, ..., 16B=31)
          """
          comm = self.commands.get('\x06\x4a')
          return self.z48.execute(comm, (arg0, ))

     def set_play_key_echo(self, arg0):
          """Set Play Key Echo <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x06\x4b')
          return self.z48.execute(comm, (arg0, ))

     def set_program_change_enable(self, arg0):
          """Set Program Change Enable <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x06\x4c')
          return self.z48.execute(comm, (arg0, ))

     def set_autoload_enable(self, arg0):
          """Set Autoload Enable <Data1> = (0=OFF, 1=ON)
          """
          comm = self.commands.get('\x06\x4d')
          return self.z48.execute(comm, (arg0, ))

     def set_global_pad_mode(self, arg0):
          """Set Global Pad Mode <Data1> = (0=DEFAULT, 1=CHROMATIC)
          """
          comm = self.commands.get('\x05\x50')
          return self.z48.execute(comm, (arg0, ))

     def set_pad_midi_channel(self, arg0):
          """Set MIDI Channel
          """
          comm = self.commands.get('\x06\x51')
          return self.z48.execute(comm, (arg0, ))

     def set_pad_sensitivity(self, arg0, arg1):
          """Set Pad Sensitivity <Data1> = Pad <Data2> = Sensitivity (0­100 = 100%­200%)
          """
          comm = self.commands.get('\x06\x52')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_default_note_assignment(self, arg0, arg1):
          """Set Default Note Assignment <Data1> = Pad, <Data2> = Note
          """
          comm = self.commands.get('\x06\x53')
          return self.z48.execute(comm, (arg0, arg1, ))

     def set_chromatic_start_note(self, arg0):
          """Set Chromatic Start Note
          """
          comm = self.commands.get('\x06\x54')
          return self.z48.execute(comm, (arg0, ))

