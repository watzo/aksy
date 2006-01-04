
""" Python equivalent of akai section sysextools

Methods to manipulate sysex parameters
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.devices.akai.sysex,aksy.devices.akai.sysex_types

class Sysextools:
    def __init__(self, s56k):
        self.s56k = s56k
        self.query_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x00', 'query', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.enable_msg_notification_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x01', 'enable_msg_notification', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.enable_item_sync_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x03', 'enable_item_sync', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.enable_checksum_verification_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x04', 'enable_checksum_verification', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.enable_screen_updates_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x05', 'enable_screen_updates', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.echo_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x06', 'echo', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.BYTE), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.enable_heartbeat_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x07', 'enable_heartbeat', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.enable_playback_sync_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x08', 'enable_playback_sync', (aksy.devices.akai.sysex_types.BOOL,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_sysex_buffersize_cmd = aksy.devices.akai.sysex.Command('^', '\x00\x10', 'get_sysex_buffersize', (), (aksy.devices.akai.sysex_types.WORD,), aksy.devices.akai.sysex_types.S56K_USERREF)

    def query(self):
        """Query device, returns device ID
        """
        return self.s56k.execute(self.query_cmd, ())

    def enable_msg_notification(self, arg0):
        """Enable/disable 'OK' messages. Use with care!
        """
        return self.s56k.execute(self.enable_msg_notification_cmd, (arg0, ))

    def enable_item_sync(self, arg0):
        """Enable sync between sysex item and front panel
        """
        return self.s56k.execute(self.enable_item_sync_cmd, (arg0, ))

    def enable_checksum_verification(self, arg0):
        """Enable sysex msg checksum verifcation
        """
        return self.s56k.execute(self.enable_checksum_verification_cmd, (arg0, ))

    def enable_screen_updates(self, arg0):
        """Enable screen updates during sysex processing
        """
        return self.s56k.execute(self.enable_screen_updates_cmd, (arg0, ))

    def echo(self, arg0, arg1, arg2, arg3):
        """Echo the specified bytes

        Returns:
            aksy.devices.akai.sysex_types.BYTE
            aksy.devices.akai.sysex_types.BYTE
            aksy.devices.akai.sysex_types.BYTE
            aksy.devices.akai.sysex_types.BYTE
        """
        return self.s56k.execute(self.echo_cmd, (arg0, arg1, arg2, arg3, ))

    def enable_heartbeat(self):
        """Enable sending of empty sysex 'still alive' msgs
        """
        return self.s56k.execute(self.enable_heartbeat_cmd, ())

    def enable_playback_sync(self, arg0):
        """Enable sync between sysex playback item and front panel
        """
        return self.s56k.execute(self.enable_playback_sync_cmd, (arg0, ))

    def get_sysex_buffersize(self):
        """Retrieves the sysex buffer size

        Returns:
            aksy.devices.akai.sysex_types.WORD
        """
        return self.s56k.execute(self.get_sysex_buffersize_cmd, ())

