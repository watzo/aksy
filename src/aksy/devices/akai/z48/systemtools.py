
""" Python equivalent of akai section systemtools

Methods to manipulate system parameters
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Systemtools:
    def __init__(self, z48):
        self.sampler = z48
        self.get_os_software_version_cmd = Command('_', '\x04\x00', 'systemtools', 'get_os_software_version', (), None)
        self.get_os_subversion_cmd = Command('_', '\x04\x01', 'systemtools', 'get_os_subversion', (), None)
        self.get_sampler_model_cmd = Command('_', '\x04\x04', 'systemtools', 'get_sampler_model', (), None)
        self.get_supported_filetypes_cmd = Command('_', '\x04\x08', 'systemtools', 'get_supported_filetypes', (), None)
        self.get_perc_free_wave_mem_cmd = Command('_', '\x04\x10', 'systemtools', 'get_perc_free_wave_mem', (), None)
        self.get_perc_free_cpu_mem_cmd = Command('_', '\x04\x11', 'systemtools', 'get_perc_free_cpu_mem', (), None)
        self.get_wave_mem_size_cmd = Command('_', '\x04\x12', 'systemtools', 'get_wave_mem_size', (), None)
        self.get_free_wave_mem_size_cmd = Command('_', '\x04\x13', 'systemtools', 'get_free_wave_mem_size', (), None)
        self.clear_sampler_mem_cmd = Command('_', '\x04\x18', 'systemtools', 'clear_sampler_mem', (), None)
        self.purge_unused_cmd = Command('_', '\x04\x19', 'systemtools', 'purge_unused', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.tag_unused_cmd = Command('_', '\x04\x1A', 'systemtools', 'tag_unused', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.compact_wave_mem_cmd = Command('_', '\x04\x20', 'systemtools', 'compact_wave_mem', (), None)
        self.cancel_compact_wave_mem_cmd = Command('_', '\x04\x21', 'systemtools', 'cancel_compact_wave_mem', (), None)
        self.get_compact_wave_mem_progress_cmd = Command('_', '\x04\x22', 'systemtools', 'get_compact_wave_mem_progress', (), None)
        self.get_async_operation_state_cmd = Command('_', '\x04\x30', 'systemtools', 'get_async_operation_state', (), None)
        self.cancel_curr_async_operation_cmd = Command('_', '\x04\x31', 'systemtools', 'cancel_curr_async_operation', (), None)
        self.get_sampler_name_cmd = Command('_', '\x07\x01', 'systemtools', 'get_sampler_name', (), None)
        self.get_scsi_id_cmd = Command('_', '\x07\x02', 'systemtools', 'get_scsi_id', (), None)
        self.get_master_tune_cmd = Command('_', '\x07\x03', 'systemtools', 'get_master_tune', (), None)
        self.get_master_level_cmd = Command('_', '\x07\x04', 'systemtools', 'get_master_level', (), None)
        self.get_midi_mode_cmd = Command('_', '\x07\x05', 'systemtools', 'get_midi_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.is_qlink_local_ctrl_enabled_cmd = Command('_', '\x07\x06', 'systemtools', 'is_qlink_local_ctrl_enabled', (), None)
        self.is_default_items_enabled_cmd = Command('_', '\x07\x07', 'systemtools', 'is_default_items_enabled', (), None)
        self.get_midi_file_save_format_cmd = Command('_', '\x07\x08', 'systemtools', 'get_midi_file_save_format', (), None)
        self.get_cdr_write_speed_cmd = Command('_', '\x07\x09', 'systemtools', 'get_cdr_write_speed', (), None)
        self.get_cdr_write_mode_cmd = Command('_', '\x07\x0A', 'systemtools', 'get_cdr_write_mode', (), None)
        self.is_front_panel_locked_cmd = Command('_', '\x07\x10', 'systemtools', 'is_front_panel_locked', (), None)
        self.get_display_contrast_cmd = Command('_', '\x07\x11', 'systemtools', 'get_display_contrast', (), None)
        self.get_note_display_cmd = Command('_', '\x07\x12', 'systemtools', 'get_note_display', (), None)
        self.get_date_format_cmd = Command('_', '\x07\x13', 'systemtools', 'get_date_format', (), None)
        self.get_time_format_cmd = Command('_', '\x07\x14', 'systemtools', 'get_time_format', (), None)
        self.get_waveform_view_scale_cmd = Command('_', '\x07\x18', 'systemtools', 'get_waveform_view_scale', (), None)
        self.get_waveform_view_type_cmd = Command('_', '\x07\x19', 'systemtools', 'get_waveform_view_type', (), None)
        self.get_waveform_view_fill_cmd = Command('_', '\x07\x1A', 'systemtools', 'get_waveform_view_fill', (), None)
        self.get_item_sort_mode_cmd = Command('_', '\x07\x1B', 'systemtools', 'get_item_sort_mode', (), None)
        self.get_year_cmd = Command('_', '\x07\x20', 'systemtools', 'get_year', (), None)
        self.get_month_cmd = Command('_', '\x07\x21', 'systemtools', 'get_month', (), None)
        self.get_day_cmd = Command('_', '\x07\x22', 'systemtools', 'get_day', (), None)
        self.get_day_of_week_cmd = Command('_', '\x07\x23', 'systemtools', 'get_day_of_week', (), None)
        self.get_hours_cmd = Command('_', '\x07\x24', 'systemtools', 'get_hours', (), None)
        self.get_mins_cmd = Command('_', '\x07\x25', 'systemtools', 'get_mins', (), None)
        self.get_secs_cmd = Command('_', '\x07\x26', 'systemtools', 'get_secs', (), None)
        self.get_system_clock_cmd = Command('_', '\x07\x30', 'systemtools', 'get_system_clock', (), None)
        self.get_dig_sync_cmd = Command('_', '\x07\x31', 'systemtools', 'get_dig_sync', (), None)
        self.get_dig_format_cmd = Command('_', '\x07\x32', 'systemtools', 'get_dig_format', (), None)
        self.get_adat_main_out_cmd = Command('_', '\x07\x33', 'systemtools', 'get_adat_main_out', (), None)
        self.get_play_mode_cmd = Command('_', '\x07\x40', 'systemtools', 'get_play_mode', (), None)
        self.get_prog_monitor_mode_cmd = Command('_', '\x07\x41', 'systemtools', 'get_prog_monitor_mode', (), None)
        self.get_sample_monitor_mode_cmd = Command('_', '\x07\x42', 'systemtools', 'get_sample_monitor_mode', (), None)
        self.get_play_key_note_cmd = Command('_', '\x07\x48', 'systemtools', 'get_play_key_note', (), None)
        self.get_play_key_velocity_cmd = Command('_', '\x07\x49', 'systemtools', 'get_play_key_velocity', (), None)
        self.get_play_key_midi_channel_cmd = Command('_', '\x07\x4a', 'systemtools', 'get_play_key_midi_channel', (), None)
        self.get_play_key_echo_cmd = Command('_', '\x07\x4b', 'systemtools', 'get_play_key_echo', (), None)
        self.get_prog_change_enable_cmd = Command('_', '\x07\x4c', 'systemtools', 'get_prog_change_enable', (), None)
        self.get_autoload_enable_cmd = Command('_', '\x07\x4d', 'systemtools', 'get_autoload_enable', (), None)
        self.get_global_pad_mode_cmd = Command('_', '\x07\x50', 'systemtools', 'get_global_pad_mode', (), None)
        self.get_pad_midi_channel_cmd = Command('_', '\x07\x51', 'systemtools', 'get_pad_midi_channel', (), None)
        self.get_pad_sensitivity_cmd = Command('_', '\x07\x52', 'systemtools', 'get_pad_sensitivity', (), None)
        self.get_def_note_assign_cmd = Command('_', '\x07\x53', 'systemtools', 'get_def_note_assign', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.get_chrom_start_note_cmd = Command('_', '\x07\x54', 'systemtools', 'get_chrom_start_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_sampler_name_cmd = Command('_', '\x06\x01', 'systemtools', 'set_sampler_name', (aksy.devices.akai.sysex_types.STRING,), None)
        self.set_scsi_id_cmd = Command('_', '\x06\x02', 'systemtools', 'set_scsi_id', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_master_tune_cmd = Command('_', '\x06\x03', 'systemtools', 'set_master_tune', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_master_level_cmd = Command('_', '\x06\x04', 'systemtools', 'set_master_level', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_midi_out_thru_cmd = Command('_', '\x06\x05', 'systemtools', 'set_midi_out_thru', (), None)
        self.set_qlink_local_control_cmd = Command('_', '\x06\x06', 'systemtools', 'set_qlink_local_control', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_create_default_items_cmd = Command('_', '\x06\x07', 'systemtools', 'set_create_default_items', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_midi_file_save_format_cmd = Command('_', '\x06\x08', 'systemtools', 'set_midi_file_save_format', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_cdr_write_speed_cmd = Command('_', '\x06\x09', 'systemtools', 'set_cdr_write_speed', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_cdr_write_mode_cmd = Command('_', '\x06\x0a', 'systemtools', 'set_cdr_write_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_front_panel_lockout_state_cmd = Command('_', '\x06\x10', 'systemtools', 'set_front_panel_lockout_state', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_display_contrast_cmd = Command('_', '\x06\x11', 'systemtools', 'set_display_contrast', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_note_display_cmd = Command('_', '\x06\x12', 'systemtools', 'set_note_display', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_date_display_format_cmd = Command('_', '\x06\x13', 'systemtools', 'set_date_display_format', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_time_display_format_cmd = Command('_', '\x06\x14', 'systemtools', 'set_time_display_format', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_waveform_view_scale_cmd = Command('_', '\x06\x18', 'systemtools', 'set_waveform_view_scale', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_waveform_view_type_cmd = Command('_', '\x06\x19', 'systemtools', 'set_waveform_view_type', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_waveform_view_fill_cmd = Command('_', '\x06\x1a', 'systemtools', 'set_waveform_view_fill', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_item_sort_mode_cmd = Command('_', '\x06\x1b', 'systemtools', 'set_item_sort_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_year_cmd = Command('_', '\x06\x20', 'systemtools', 'set_year', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_month_cmd = Command('_', '\x06\x21', 'systemtools', 'set_month', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_day_cmd = Command('_', '\x06\x22', 'systemtools', 'set_day', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_day_of_week_cmd = Command('_', '\x06\x23', 'systemtools', 'set_day_of_week', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_hours_cmd = Command('_', '\x06\x24', 'systemtools', 'set_hours', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_minutes_cmd = Command('_', '\x06\x25', 'systemtools', 'set_minutes', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_seconds_cmd = Command('_', '\x06\x26', 'systemtools', 'set_seconds', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_system_clock_cmd = Command('_', '\x06\x30', 'systemtools', 'set_system_clock', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_digital_out_sync_cmd = Command('_', '\x06\x31', 'systemtools', 'set_digital_out_sync', (), None)
        self.set_digital_format_cmd = Command('_', '\x06\x32', 'systemtools', 'set_digital_format', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_adat_main_out_cmd = Command('_', '\x06\x33', 'systemtools', 'set_adat_main_out', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_mode_cmd = Command('_', '\x06\x40', 'systemtools', 'set_play_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_program_monitor_mode_cmd = Command('_', '\x06\x41', 'systemtools', 'set_program_monitor_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_sample_monitor_mode_cmd = Command('_', '\x06\x42', 'systemtools', 'set_sample_monitor_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_key_note_cmd = Command('_', '\x06\x48', 'systemtools', 'set_play_key_note', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_key_velocity_cmd = Command('_', '\x06\x49', 'systemtools', 'set_play_key_velocity', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_key_midi_channel_cmd = Command('_', '\x06\x4a', 'systemtools', 'set_play_key_midi_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_play_key_echo_cmd = Command('_', '\x06\x4b', 'systemtools', 'set_play_key_echo', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_program_change_enable_cmd = Command('_', '\x06\x4c', 'systemtools', 'set_program_change_enable', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_autoload_enable_cmd = Command('_', '\x06\x4d', 'systemtools', 'set_autoload_enable', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.set_global_pad_mode_cmd = Command('_', '\x05\x50', 'systemtools', 'set_global_pad_mode', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_pad_midi_channel_cmd = Command('_', '\x06\x51', 'systemtools', 'set_pad_midi_channel', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.set_pad_sensitivity_cmd = Command('_', '\x06\x52', 'systemtools', 'set_pad_sensitivity', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_default_note_assignment_cmd = Command('_', '\x06\x53', 'systemtools', 'set_default_note_assignment', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.set_chromatic_start_note_cmd = Command('_', '\x06\x54', 'systemtools', 'set_chromatic_start_note', (aksy.devices.akai.sysex_types.BYTE,), None)

    def get_os_software_version(self):
        """Get Operating System Software Version

        Returns:
            BYTE
            BYTE
        """
        return self.sampler.execute(self.get_os_software_version_cmd, ())

    def get_os_subversion(self):
        """Get the Sub-Version of the Operating System

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_os_subversion_cmd, ())

    def get_sampler_model(self):
        """Get Sampler Model  (0=Z4, 1=Z8, 2=MPC4000)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_sampler_model_cmd, ())

    def get_supported_filetypes(self):
        """Get List of supported filetypes [returns DONE message]

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_supported_filetypes_cmd, ())

    def get_perc_free_wave_mem(self):
        """Get the percentage free Wave memory

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_perc_free_wave_mem_cmd, ())

    def get_perc_free_cpu_mem(self):
        """Get the percentage free CPU memory

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_perc_free_cpu_mem_cmd, ())

    def get_wave_mem_size(self):
        """Get the total number of kilobytes of Wave memory

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_wave_mem_size_cmd, ())

    def get_free_wave_mem_size(self):
        """Get the number of kilobytes of free Wave memory

        Returns:
            DWORD
        """
        return self.sampler.execute(self.get_free_wave_mem_size_cmd, ())

    def clear_sampler_mem(self):
        """Clear Sampler Memory (delete all items from memory)
        """
        return self.sampler.execute(self.clear_sampler_mem_cmd, ())

    def purge_unused(self, arg0):
        """Purge Unused Items <Data1> = (0=SAMPLE, 1=PROGRAM)
        """
        return self.sampler.execute(self.purge_unused_cmd, (arg0, ))

    def tag_unused(self, arg0):
        """Tag Unused Items <Data1> = (0=SAMPLE, 1=PROGRAM)
        """
        return self.sampler.execute(self.tag_unused_cmd, (arg0, ))

    def compact_wave_mem(self):
        """Start Compact Wave Memory
        """
        return self.sampler.execute(self.compact_wave_mem_cmd, ())

    def cancel_compact_wave_mem(self):
        """Cancel Compact Wave Memory
        """
        return self.sampler.execute(self.cancel_compact_wave_mem_cmd, ())

    def get_compact_wave_mem_progress(self):
        """Get Compact Wave Memory Progress (%)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_compact_wave_mem_progress_cmd, ())

    def get_async_operation_state(self):
        """Get State of Asynchronous Operation ERROR 'operation is pending' or DONE

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_async_operation_state_cmd, ())

    def cancel_curr_async_operation(self):
        """Cancel Current Asynchronous Operation
        """
        return self.sampler.execute(self.cancel_curr_async_operation_cmd, ())

    def get_sampler_name(self):
        """Get Sampler Name

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_sampler_name_cmd, ())

    def get_scsi_id(self):
        """Get SCSI self ID

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_scsi_id_cmd, ())

    def get_master_tune(self):
        """Get Master Tune

        Returns:
            SWORD
        """
        return self.sampler.execute(self.get_master_tune_cmd, ())

    def get_master_level(self):
        """Get Master Level <Reply> = (-42 dB - 0dB in 6dB steps)(0=-42 dB, 1=-36dB, ..., 7=0dB)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_master_level_cmd, ())

    def get_midi_mode(self, arg0):
        """Get MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B) <Reply> = (0=OUT, 1=THRUA, 2=THRUB)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_mode_cmd, (arg0, ))

    def is_qlink_local_ctrl_enabled(self):
        """Get Qlink Local Control <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.is_qlink_local_ctrl_enabled_cmd, ())

    def is_default_items_enabled(self):
        """Get Create Default Items at Startup <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.is_default_items_enabled_cmd, ())

    def get_midi_file_save_format(self):
        """Get MIDI file save format

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_midi_file_save_format_cmd, ())

    def get_cdr_write_speed(self):
        """Get CD-R write speed (0=*1, 1=*2, 2=*4, 3=*6, 4=*8, 5=*12, 6=*16, 7=MAX)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_cdr_write_speed_cmd, ())

    def get_cdr_write_mode(self):
        """Get CD-R write mode <Reply> = (0=TEST+WRITE, 1=TEST ONLY, 2=WRITE ONLY)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_cdr_write_mode_cmd, ())

    def is_front_panel_locked(self):
        """Get Front panel lock-out state

        Returns:
            BYTE
        """
        return self.sampler.execute(self.is_front_panel_locked_cmd, ())

    def get_display_contrast(self):
        """Get Display Contrast

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_display_contrast_cmd, ())

    def get_note_display(self):
        """Get Note Display <Reply> = (0=NUMBER, 1=NAME)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_note_display_cmd, ())

    def get_date_format(self):
        """Get Date Display Format  <Reply> = (0=DDMMYY, 1=MMDDYY, 2=YYMMDD)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_date_format_cmd, ())

    def get_time_format(self):
        """Get Time Display Format <Reply> = (0=12HOUR, 1=24HOUR)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_time_format_cmd, ())

    def get_waveform_view_scale(self):
        """Get Waveform View Scale <Reply> = (0=LINEAR, 1=LOG)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_waveform_view_scale_cmd, ())

    def get_waveform_view_type(self):
        """Get Waveform View Type <Reply> = (0=RECTIFIED, 1=BIPOLAR)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_waveform_view_type_cmd, ())

    def get_waveform_view_fill(self):
        """Get Waveform View Fill <Reply> = (0=OFF, 1=ON)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_waveform_view_fill_cmd, ())

    def get_item_sort_mode(self):
        """Get Item Sort Mode <Reply> = (0=ALPHABETIC, 1=MEMORY)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_item_sort_mode_cmd, ())

    def get_year(self):
        """Get Year

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_year_cmd, ())

    def get_month(self):
        """Get Month

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_month_cmd, ())

    def get_day(self):
        """Get Day

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_day_cmd, ())

    def get_day_of_week(self):
        """Get Day of Week (0=SUN)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_day_of_week_cmd, ())

    def get_hours(self):
        """Get Hours

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_hours_cmd, ())

    def get_mins(self):
        """Get Minutes

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_mins_cmd, ())

    def get_secs(self):
        """Get Seconds

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_secs_cmd, ())

    def get_system_clock(self):
        """Get System Clock <Reply> = (0=44.1kHz, 1=48kHz, 2=96kHz)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_system_clock_cmd, ())

    def get_dig_sync(self):
        """Get Digital Out Sync (0=INTERNAL, 1=DIGITAL IN, 2=ADAT IN, 3=WORDCLOCK)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_dig_sync_cmd, ())

    def get_dig_format(self):
        """Get Digital Format <Reply> = (0=PRO, 1=CONSUMER)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_dig_format_cmd, ())

    def get_adat_main_out(self):
        """Get ADAT Main Out <Reply> = (0=L/R, 1=1/2)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_adat_main_out_cmd, ())

    def get_play_mode(self):
        """Get Play Mode (0=Multi, 1=Program; 2=Sample; 3=Muted), handle of item which is the active Play Item

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_play_mode_cmd, ())

    def get_prog_monitor_mode(self):
        """Get Program Monitor Mode  (0=Multi, 1=Program(OMNI))

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_prog_monitor_mode_cmd, ())

    def get_sample_monitor_mode(self):
        """Get Sample Monitor Mode (0=Multi, 1=Program; 2=Sample(OMNI))

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_sample_monitor_mode_cmd, ())

    def get_play_key_note(self):
        """Get Play Key Note

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_play_key_note_cmd, ())

    def get_play_key_velocity(self):
        """Get Play Key Velocity

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_play_key_velocity_cmd, ())

    def get_play_key_midi_channel(self):
        """Get Play Key Midi Channel <Reply> = (1A=0, 2A=1, ..., 16B=31)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_play_key_midi_channel_cmd, ())

    def get_play_key_echo(self):
        """Get Play Key Echo <Reply> = (0=OFF, 1=ON)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_play_key_echo_cmd, ())

    def get_prog_change_enable(self):
        """Get Program Change Enable <Reply> = (0=OFF, 1=ON)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_prog_change_enable_cmd, ())

    def get_autoload_enable(self):
        """Get Autoload Enable <Reply> = (0=OFF, 1=ON)

        Returns:
            BOOL
        """
        return self.sampler.execute(self.get_autoload_enable_cmd, ())

    def get_global_pad_mode(self):
        """Get Global Pad Mode <Reply> = (0=DEFAULT, 1=CHROMATIC)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_global_pad_mode_cmd, ())

    def get_pad_midi_channel(self):
        """Get MIDI Channel for MPC Pad

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pad_midi_channel_cmd, ())

    def get_pad_sensitivity(self):
        """Get Pad Sensitivity <Data1> = Pad <Reply> = Sensitivity (0-100 = 100%-200%)

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_pad_sensitivity_cmd, ())

    def get_def_note_assign(self, arg0):
        """Get Default Note Assignment <Data1> = Pad

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_def_note_assign_cmd, (arg0, ))

    def get_chrom_start_note(self, arg0):
        """Get Default Note Assignment <Data1> = Pad

        Returns:
            BYTE
        """
        return self.sampler.execute(self.get_chrom_start_note_cmd, (arg0, ))

    def set_sampler_name(self, arg0):
        """Set Sampler Name
        """
        return self.sampler.execute(self.set_sampler_name_cmd, (arg0, ))

    def set_scsi_id(self, arg0):
        """Set SCSI ID
        """
        return self.sampler.execute(self.set_scsi_id_cmd, (arg0, ))

    def set_master_tune(self, arg0):
        """Set Master Tune
        """
        return self.sampler.execute(self.set_master_tune_cmd, (arg0, ))

    def set_master_level(self, arg0):
        """Set Master Level <Data1> = (-42dB - 0dB in 6dB * 7 steps)
        """
        return self.sampler.execute(self.set_master_level_cmd, (arg0, ))

    def set_midi_out_thru(self):
        """Set MIDI OUT/THRU <Data1> = MIDI port (0=A, 1=B), <Data2> = (0=OUT, 1=THRUA, 2=THRUB)
        """
        return self.sampler.execute(self.set_midi_out_thru_cmd, ())

    def set_qlink_local_control(self, arg0):
        """Set Qlink Local Control
        """
        return self.sampler.execute(self.set_qlink_local_control_cmd, (arg0, ))

    def set_create_default_items(self, arg0):
        """Set Create Default Items at Startup
        """
        return self.sampler.execute(self.set_create_default_items_cmd, (arg0, ))

    def set_midi_file_save_format(self, arg0):
        """Set MIDI file save format
        """
        return self.sampler.execute(self.set_midi_file_save_format_cmd, (arg0, ))

    def set_cdr_write_speed(self, arg0):
        """Set CD-R write speed <Data1> = (0=*1, 1=*2, 2=*4, 3=*6, 4=*8, 5=*12, 6=*16, 7=MAX)
        """
        return self.sampler.execute(self.set_cdr_write_speed_cmd, (arg0, ))

    def set_cdr_write_mode(self, arg0):
        """Set CD-R write mode <Data1> = (0=TEST+WRITE, 1=TEST ONLY, 2=WRITE ONLY)
        """
        return self.sampler.execute(self.set_cdr_write_mode_cmd, (arg0, ))

    def set_front_panel_lockout_state(self, arg0):
        """Set Front panel lock-out state <Data1> = (0=NORMAL; 1=LOCKED)
        """
        return self.sampler.execute(self.set_front_panel_lockout_state_cmd, (arg0, ))

    def set_display_contrast(self, arg0):
        """  Set Display Contrast
        """
        return self.sampler.execute(self.set_display_contrast_cmd, (arg0, ))

    def set_note_display(self, arg0):
        """Set Note Display <Data1> = (0=NUMBER, 1=NAME)
        """
        return self.sampler.execute(self.set_note_display_cmd, (arg0, ))

    def set_date_display_format(self, arg0):
        """Set Date Display Format <Data1> = (0=DDMMYY, 1=MMDDYY, 2=YYMMDD)
        """
        return self.sampler.execute(self.set_date_display_format_cmd, (arg0, ))

    def set_time_display_format(self, arg0):
        """Set Time Display Format <Data1> = (0=12HOUR, 1=24HOUR)
        """
        return self.sampler.execute(self.set_time_display_format_cmd, (arg0, ))

    def set_waveform_view_scale(self, arg0):
        """Set Waveform View Scale <Data1> = (0=LINEAR, 1=LOG)
        """
        return self.sampler.execute(self.set_waveform_view_scale_cmd, (arg0, ))

    def set_waveform_view_type(self, arg0):
        """Set Waveform View Type <Data1> = (0=RECTIFIED, 1=BIPOLAR)
        """
        return self.sampler.execute(self.set_waveform_view_type_cmd, (arg0, ))

    def set_waveform_view_fill(self, arg0):
        """Set Waveform View Fill <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_waveform_view_fill_cmd, (arg0, ))

    def set_item_sort_mode(self, arg0):
        """Set Item Sort Mode <Data1> = (0=ALPHABETIC, 1=MEMORY)
        """
        return self.sampler.execute(self.set_item_sort_mode_cmd, (arg0, ))

    def set_year(self, arg0):
        """Set Year
        """
        return self.sampler.execute(self.set_year_cmd, (arg0, ))

    def set_month(self, arg0):
        """Set Month
        """
        return self.sampler.execute(self.set_month_cmd, (arg0, ))

    def set_day(self, arg0):
        """Set Day
        """
        return self.sampler.execute(self.set_day_cmd, (arg0, ))

    def set_day_of_week(self, arg0):
        """Set Day of Week (0=SUN)
        """
        return self.sampler.execute(self.set_day_of_week_cmd, (arg0, ))

    def set_hours(self, arg0):
        """Set Hours
        """
        return self.sampler.execute(self.set_hours_cmd, (arg0, ))

    def set_minutes(self, arg0):
        """Set Minutes
        """
        return self.sampler.execute(self.set_minutes_cmd, (arg0, ))

    def set_seconds(self, arg0):
        """Set Seconds
        """
        return self.sampler.execute(self.set_seconds_cmd, (arg0, ))

    def set_system_clock(self, arg0):
        """Set System Clock <Data1> = (0=44.1kHz, 1=48kHz, 2=96kHz)
        """
        return self.sampler.execute(self.set_system_clock_cmd, (arg0, ))

    def set_digital_out_sync(self):
        """Set Digital Out Sync <Data1> = (0=INTERNAL, 1=DIGITAL IN, 2=ADAT IN, 3=WORDCLOCK) BYTE
        """
        return self.sampler.execute(self.set_digital_out_sync_cmd, ())

    def set_digital_format(self, arg0):
        """Set Digital Format <Data1> = (0=PRO, 1=CONSUMER)
        """
        return self.sampler.execute(self.set_digital_format_cmd, (arg0, ))

    def set_adat_main_out(self, arg0):
        """Set ADAT Main Out <Data1> = (0=L/R, 1=1/2)
        """
        return self.sampler.execute(self.set_adat_main_out_cmd, (arg0, ))

    def set_play_mode(self, arg0):
        """Set Play Mode <Data1> = (0=Multi, 1=Program; 2=Sample; 3=Muted) <Data2> = handle of item to become active Play Item
        """
        return self.sampler.execute(self.set_play_mode_cmd, (arg0, ))

    def set_program_monitor_mode(self, arg0):
        """Set Program Monitor Mode <Data1> = (0=Multi, 1=Program(OMNI))
        """
        return self.sampler.execute(self.set_program_monitor_mode_cmd, (arg0, ))

    def set_sample_monitor_mode(self, arg0):
        """Set Sample Monitor Mode <Data1> = (0=Multi, 1=Program; 2=Sample(OMNI))
        """
        return self.sampler.execute(self.set_sample_monitor_mode_cmd, (arg0, ))

    def set_play_key_note(self, arg0):
        """Set Play Key Note
        """
        return self.sampler.execute(self.set_play_key_note_cmd, (arg0, ))

    def set_play_key_velocity(self, arg0):
        """Set Play Key Velocity
        """
        return self.sampler.execute(self.set_play_key_velocity_cmd, (arg0, ))

    def set_play_key_midi_channel(self, arg0):
        """Set Play Key Midi Channel <Data1> = (1A=0, 2A=1, ..., 16B=31)
        """
        return self.sampler.execute(self.set_play_key_midi_channel_cmd, (arg0, ))

    def set_play_key_echo(self, arg0):
        """Set Play Key Echo <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_play_key_echo_cmd, (arg0, ))

    def set_program_change_enable(self, arg0):
        """Set Program Change Enable <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_program_change_enable_cmd, (arg0, ))

    def set_autoload_enable(self, arg0):
        """Set Autoload Enable <Data1> = (0=OFF, 1=ON)
        """
        return self.sampler.execute(self.set_autoload_enable_cmd, (arg0, ))

    def set_global_pad_mode(self, arg0):
        """Set Global Pad Mode <Data1> = (0=DEFAULT, 1=CHROMATIC)
        """
        return self.sampler.execute(self.set_global_pad_mode_cmd, (arg0, ))

    def set_pad_midi_channel(self, arg0):
        """Set MIDI Channel
        """
        return self.sampler.execute(self.set_pad_midi_channel_cmd, (arg0, ))

    def set_pad_sensitivity(self, arg0, arg1):
        """Set Pad Sensitivity <Data1> = Pad <Data2> = Sensitivity (0-100 = 100%-200%)
        """
        return self.sampler.execute(self.set_pad_sensitivity_cmd, (arg0, arg1, ))

    def set_default_note_assignment(self, arg0, arg1):
        """Set Default Note Assignment <Data1> = Pad, <Data2> = Note
        """
        return self.sampler.execute(self.set_default_note_assignment_cmd, (arg0, arg1, ))

    def set_chromatic_start_note(self, arg0):
        """Set Chromatic Start Note
        """
        return self.sampler.execute(self.set_chromatic_start_note_cmd, (arg0, ))

