
""" Python equivalent of akai section systemtools

Methods to manipulate system parameters
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.sysex

class Systemtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          self.command_spec = aksy.sysex.CommandSpec('\x47\x5f\x00', aksy.sysex.CommandSpec.ID, aksy.sysex.CommandSpec.ARGS)
          comm = aksy.sysex.Command('\x04\x00', 'get_os_software_version', (), (aksy.sysex.BYTE, aksy.sysex.BYTE))
          self.commands['\x04\x00'] = comm
          comm = aksy.sysex.Command('\x04\x01', 'get_os_subversion', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x01'] = comm
          comm = aksy.sysex.Command('\x04\x04', 'get_sampler_model', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x04'] = comm
          comm = aksy.sysex.Command('\x04\x08', 'get_supported_filetypes', (), (aksy.sysex.STRING,))
          self.commands['\x04\x08'] = comm
          comm = aksy.sysex.Command('\x04\x10', 'get_perc_free_wave_mem', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x10'] = comm
          comm = aksy.sysex.Command('\x04\x11', 'get_perc_free_cpu_mem', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x11'] = comm
          comm = aksy.sysex.Command('\x04\x12', 'get_wave_mem_size', (), (aksy.sysex.DWORD,))
          self.commands['\x04\x12'] = comm
          comm = aksy.sysex.Command('\x04\x13', 'get_free_wave_mem_size', (), (aksy.sysex.DWORD,))
          self.commands['\x04\x13'] = comm
          comm = aksy.sysex.Command('\x04\x18', 'clear_sampler_mem', (), ())
          self.commands['\x04\x18'] = comm
          comm = aksy.sysex.Command('\x04\x19', 'purge_unused', (aksy.sysex.BYTE,), ())
          self.commands['\x04\x19'] = comm
          comm = aksy.sysex.Command('\x04\x1A', 'tag_unused', (aksy.sysex.BYTE,), ())
          self.commands['\x04\x1A'] = comm
          comm = aksy.sysex.Command('\x04\x20', 'compact_wave_mem', (), ())
          self.commands['\x04\x20'] = comm
          comm = aksy.sysex.Command('\x04\x21', 'cancel_compact_wave_mem', (), ())
          self.commands['\x04\x21'] = comm
          comm = aksy.sysex.Command('\x04\x22 ', 'get_compact_wave_mem_progress', (), (aksy.sysex.BYTE,))
          self.commands['\x04\x22 '] = comm
          comm = aksy.sysex.Command('\x04\x30 ', 'get_async_operation_state', (), ())
          self.commands['\x04\x30 '] = comm
          comm = aksy.sysex.Command('\x04\x31 ', 'cancel_curr_async_operation', (), ())
          self.commands['\x04\x31 '] = comm
          comm = aksy.sysex.Command('\x07\x01', 'get_sampler_name', (), (aksy.sysex.STRING,))
          self.commands['\x07\x01'] = comm
          comm = aksy.sysex.Command('\x07\x02', 'get_scsi_id', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x02'] = comm
          comm = aksy.sysex.Command('\x07\x03', 'get_master_tune', (), (aksy.sysex.SWORD,))
          self.commands['\x07\x03'] = comm
          comm = aksy.sysex.Command('\x07\x04', 'get_master_level', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x04'] = comm
          comm = aksy.sysex.Command('\x07\x05', 'get_midi_mode', (aksy.sysex.BYTE,), (aksy.sysex.BYTE,))
          self.commands['\x07\x05'] = comm
          comm = aksy.sysex.Command('\x07\x06', 'is_qlink_local_ctrl_enabled', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x06'] = comm
          comm = aksy.sysex.Command('\x07\x07', 'is_default_items_enabled', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x07'] = comm
          comm = aksy.sysex.Command('\x07\x08', 'get_midi_file_save_format', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x08'] = comm
          comm = aksy.sysex.Command('\x07\x09', 'get_cdr_write_speed', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x09'] = comm
          comm = aksy.sysex.Command('\x07\x0A', 'get_cdr_write_mode', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x0A'] = comm
          comm = aksy.sysex.Command('\x07\x10', 'is_front_panel_locked', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x10'] = comm
          comm = aksy.sysex.Command('\x07\x11', 'get_display_contrast', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x11'] = comm
          comm = aksy.sysex.Command('\x07\x12', 'get_note_display', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x12'] = comm
          comm = aksy.sysex.Command('\x07\x13', 'get_date_format', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x13'] = comm
          comm = aksy.sysex.Command('\x07\x14', 'get_time_format', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x14'] = comm
          comm = aksy.sysex.Command('\x07\x18', 'get_waveform_view_scale', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x18'] = comm
          comm = aksy.sysex.Command('\x07\x19', 'get_waveform_view_type', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x19'] = comm
          comm = aksy.sysex.Command('\x07\x1A', 'get_waveform_view_fill', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x1A'] = comm
          comm = aksy.sysex.Command('\x07\x1B', 'get_item_sort_mode', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x1B'] = comm
          comm = aksy.sysex.Command('\x07\x20', 'get_year', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x20'] = comm
          comm = aksy.sysex.Command('\x07\x21', 'get_month', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x21'] = comm
          comm = aksy.sysex.Command('\x07\x22', 'get_day', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x22'] = comm
          comm = aksy.sysex.Command('\x07\x23', 'get_day_of_week', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x23'] = comm
          comm = aksy.sysex.Command('\x07\x24', 'get_hours', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x24'] = comm
          comm = aksy.sysex.Command('\x07\x25', 'get_mins', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x25'] = comm
          comm = aksy.sysex.Command('\x07\x26', 'get_secs', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x26'] = comm
          comm = aksy.sysex.Command('\x07\x30', 'get_system_clock', (), (aksy.sysex.BYTE,))
          self.commands['\x07\x30'] = comm

     def get_os_software_version(self):
          """Get Operating System Software Version

          Returns:
               aksy.sysex.BYTE
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x00')
          return self.z48.execute(comm, ())

     def get_os_subversion(self):
          """Get the Sub-Version of the Operating System

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x01')
          return self.z48.execute(comm, ())

     def get_sampler_model(self):
          """Get Sampler Model

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x04')
          return self.z48.execute(comm, ())

     def get_supported_filetypes(self):
          """Get List of supported filetypes

          Returns:
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x04\x08')
          return self.z48.execute(comm, ())

     def get_perc_free_wave_mem(self):
          """Get the percentage free Wave memory

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x10')
          return self.z48.execute(comm, ())

     def get_perc_free_cpu_mem(self):
          """Get the percentage free CPU memory

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x11')
          return self.z48.execute(comm, ())

     def get_wave_mem_size(self):
          """Get the total number of kilobytes of Wave memory

          Returns:
               aksy.sysex.DWORD
          """
          comm = self.commands.get('\x04\x12')
          return self.z48.execute(comm, ())

     def get_free_wave_mem_size(self):
          """Get the number of kilobytes of free Wave memory

          Returns:
               aksy.sysex.DWORD
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
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x04\x22 ')
          return self.z48.execute(comm, ())

     def get_async_operation_state(self):
          """Get State of Asynchronous Operation ERROR 'operation is pending' or DONE
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
               aksy.sysex.STRING
          """
          comm = self.commands.get('\x07\x01')
          return self.z48.execute(comm, ())

     def get_scsi_id(self):
          """Get SCSI self ID

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x02')
          return self.z48.execute(comm, ())

     def get_master_tune(self):
          """Get Master Tune

          Returns:
               aksy.sysex.SWORD
          """
          comm = self.commands.get('\x07\x03')
          return self.z48.execute(comm, ())

     def get_master_level(self):
          """Get Master Level <Reply> = (-42 dB ­ 0dB in 6dB steps)(0=-42 dB, 1=-36dB, ..., 7=0dB)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x04')
          return self.z48.execute(comm, ())

     def get_midi_mode(self, arg0):
          """Get MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B) <Reply> = (0=OUT, 1=THRUA, 2=THRUB)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x05')
          return self.z48.execute(comm, (arg0, ))

     def is_qlink_local_ctrl_enabled(self):
          """Get Qlink Local Control <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x06')
          return self.z48.execute(comm, ())

     def is_default_items_enabled(self):
          """Get Create Default Items at Startup <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x07')
          return self.z48.execute(comm, ())

     def get_midi_file_save_format(self):
          """Get MIDI file save format

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x08')
          return self.z48.execute(comm, ())

     def get_cdr_write_speed(self):
          """Get CD-R write speed (0=×1, 1=×2, 2=×4, 3=×6, 4=×8, 5=×12, 6=×16, 7=MAX)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x09')
          return self.z48.execute(comm, ())

     def get_cdr_write_mode(self):
          """Get CD-R write mode <Reply> = (0=TEST+WRITE, 1=TEST ONLY, 2=WRITE ONLY)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x0A')
          return self.z48.execute(comm, ())

     def is_front_panel_locked(self):
          """Get Front panel lock-out state

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x10')
          return self.z48.execute(comm, ())

     def get_display_contrast(self):
          """Get Display Contrast

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x11')
          return self.z48.execute(comm, ())

     def get_note_display(self):
          """Get Note Display <Reply> = (0=NUMBER, 1=NAME)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x12')
          return self.z48.execute(comm, ())

     def get_date_format(self):
          """Get Date Display Format  <Reply> = (0=DDMMYY, 1=MMDDYY, 2=YYMMDD)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x13')
          return self.z48.execute(comm, ())

     def get_time_format(self):
          """Get Time Display Format <Reply> = (0=12HOUR, 1=24HOUR)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x14')
          return self.z48.execute(comm, ())

     def get_waveform_view_scale(self):
          """Get Waveform View Scale <Reply> = (0=LINEAR, 1=LOG)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x18')
          return self.z48.execute(comm, ())

     def get_waveform_view_type(self):
          """Get Waveform View Type <Reply> = (0=RECTIFIED, 1=BIPOLAR)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x19')
          return self.z48.execute(comm, ())

     def get_waveform_view_fill(self):
          """Get Waveform View Fill <Reply> = (0=OFF, 1=ON)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x1A')
          return self.z48.execute(comm, ())

     def get_item_sort_mode(self):
          """Get Item Sort Mode <Reply> = (0=ALPHABETIC, 1=MEMORY)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x1B')
          return self.z48.execute(comm, ())

     def get_year(self):
          """Get Year

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x20')
          return self.z48.execute(comm, ())

     def get_month(self):
          """Get Month

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x21')
          return self.z48.execute(comm, ())

     def get_day(self):
          """Get Day

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x22')
          return self.z48.execute(comm, ())

     def get_day_of_week(self):
          """Get Day of Week (0=SUN)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x23')
          return self.z48.execute(comm, ())

     def get_hours(self):
          """Get Hours

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x24')
          return self.z48.execute(comm, ())

     def get_mins(self):
          """Get Minutes

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x25')
          return self.z48.execute(comm, ())

     def get_secs(self):
          """Get Seconds

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x26')
          return self.z48.execute(comm, ())

     def get_system_clock(self):
          """Get System Clock <Reply> = (0=44·1kHz, 1=48kHz, 2=96kHz)

          Returns:
               aksy.sysex.BYTE
          """
          comm = self.commands.get('\x07\x30')
          return self.z48.execute(comm, ())

