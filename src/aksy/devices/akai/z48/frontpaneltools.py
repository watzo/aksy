
""" Python equivalent of akai section frontpaneltools

Methods to manipulate the front panel
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

from aksy.devices.akai import base

class Frontpaneltools:
    def __init__(self, z48):
        self.sampler = z48
        self.mouseclick_at_screen_cmd = Command('_', '\x2C\x20', 'mouseclick_at_screen', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD), None)
        self.mousedoubleclick_at_screen_cmd = Command('_', '\x2C\x21', 'mousedoubleclick_at_screen', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD), None)
        self.keypress_hold_cmd = Command('_', '\x2C\x01', 'keypress_hold', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.keypress_release_cmd = Command('_', '\x2C\x02', 'keypress_release', (aksy.devices.akai.sysex_types.BYTE,), None)
        self.move_datawheel_cmd = Command('_', '\x2C\x03', 'move_datawheel', (aksy.devices.akai.sysex_types.SBYTE,), None)
        self.set_qlink_control_cmd = Command('_', '\x2C\x04', 'set_qlink_control', (aksy.devices.akai.sysex_types.BYTE, aksy.devices.akai.sysex_types.WORD), None)
        self.ascii_keypress_hold_cmd = Command('_', '\x2C\x10', 'ascii_keypress_hold', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD), None)
        self.ascii_keypress_release_cmd = Command('_', '\x2C\x11', 'ascii_keypress_release', (aksy.devices.akai.sysex_types.WORD, aksy.devices.akai.sysex_types.WORD), None)

    def mouseclick_at_screen(self, arg0, arg1):
        """Perform a mouse click
        """
        return self.sampler.execute(self.mouseclick_at_screen_cmd, (arg0, arg1, ))

    def mousedoubleclick_at_screen(self, arg0, arg1):
        """Perform a mouse double click
        """
        return self.sampler.execute(self.mousedoubleclick_at_screen_cmd, (arg0, arg1, ))

    def keypress_hold(self, arg0):
        """Perform key hold
        """
        return self.sampler.execute(self.keypress_hold_cmd, (arg0, ))

    def keypress_release(self, arg0):
        """Perform key release
        """
        return self.sampler.execute(self.keypress_release_cmd, (arg0, ))

    def move_datawheel(self, arg0):
        """Move datawheel
        """
        return self.sampler.execute(self.move_datawheel_cmd, (arg0, ))

    def set_qlink_control(self, arg0, arg1):
        """Set the value of a Q-link control
        """
        return self.sampler.execute(self.set_qlink_control_cmd, (arg0, arg1, ))

    def ascii_keypress_hold(self, arg0, arg1):
        """Perform ascii key hold
        """
        return self.sampler.execute(self.ascii_keypress_hold_cmd, (arg0, arg1, ))

    def ascii_keypress_release(self, arg0, arg1):
        """Perform ascii key release
        """
        return self.sampler.execute(self.ascii_keypress_release_cmd, (arg0, arg1, ))
