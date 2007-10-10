
""" Python equivalent of akai section sysextools

Methods to manipulate sysex parameters
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Sysextools:
    def __init__(self, z48):
        self.sampler = z48
        self.query_cmd = Command('_', '\x00\x00', 'sysextools', 'query', (), None)
        self.enable_msg_notification_cmd = Command('_', '\x00\x01', 'sysextools', 'enable_msg_notification', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.enable_item_sync_cmd = Command('_', '\x00\x03', 'sysextools', 'enable_item_sync', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.enable_checksum_verification_cmd = Command('_', '\x00\x04', 'sysextools', 'enable_checksum_verification', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.enable_screen_updates_cmd = Command('_', '\x00\x05', 'sysextools', 'enable_screen_updates', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.echo_cmd = Command('_', '\x00\x06', 'sysextools', 'echo', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), None)
        self.enable_heartbeat_cmd = Command('_', '\x00\x07', 'sysextools', 'enable_heartbeat', (), None)
        self.enable_playback_sync_cmd = Command('_', '\x00\x08', 'sysextools', 'enable_playback_sync', (aksy.devices.akai.sysex_types.BOOL,), None)
        self.get_sysex_buffersize_cmd = Command('_', '\x00\x10', 'sysextools', 'get_sysex_buffersize', (), None)

    def query(self):
        """Query device, returns device ID
        """
        return self.sampler.execute(self.query_cmd, ())

    def enable_msg_notification(self, arg0):
        """Enable/disable 'OK' messages. Use with care!
        """
        return self.sampler.execute(self.enable_msg_notification_cmd, (arg0, ))

    def enable_item_sync(self, arg0):
        """Enable sync between sysex item and front panel
        """
        return self.sampler.execute(self.enable_item_sync_cmd, (arg0, ))

    def enable_checksum_verification(self, arg0):
        """Enable sysex msg checksum verifcation
        """
        return self.sampler.execute(self.enable_checksum_verification_cmd, (arg0, ))

    def enable_screen_updates(self, arg0):
        """Enable screen updates during sysex processing
        """
        return self.sampler.execute(self.enable_screen_updates_cmd, (arg0, ))

    def echo(self, arg0, arg1, arg2, arg3):
        """Echo the specified bytes

        Returns:
            FOUR_BYTES
        """
        return self.sampler.execute(self.echo_cmd, (arg0, arg1, arg2, arg3, ))

    def enable_heartbeat(self):
        """Enable sending of empty sysex 'still alive' msgs
        """
        return self.sampler.execute(self.enable_heartbeat_cmd, ())

    def enable_playback_sync(self, arg0):
        """Enable sync between sysex playback item and front panel
        """
        return self.sampler.execute(self.enable_playback_sync_cmd, (arg0, ))

    def get_sysex_buffersize(self):
        """Retrieves the sysex buffer size

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_sysex_buffersize_cmd, ())

