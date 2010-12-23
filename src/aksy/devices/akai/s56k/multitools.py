
""" Python equivalent of akai section multitools

Methods to manipulate in-memory multis
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Multitools:
    def __init__(self, s56k):
        self.sampler = s56k
        self.rename_cmd = Command('^', '\x0c\x30', 'multitools', 'rename', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_items_cmd = Command('^', '\x0c\x40', 'multitools', 'get_no_items', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_handle_cmd = Command('^', '\x0c\x42', 'multitools', 'get_curr_handle', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_name_cmd = Command('^', '\x0c\x43', 'multitools', 'get_curr_name', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_names_cmd = Command('^', '\x0c\x51', 'multitools', 'get_names', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_handle_cmd = Command('^', '\x0c\x06', 'multitools', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_name_cmd = Command('^', '\x0c\x05', 'multitools', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_all_cmd = Command('^', '\x0c\x07', 'multitools', 'delete_all', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_curr_cmd = Command('^', '\x0c\x08', 'multitools', 'delete_curr', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)

    def rename(self):
        """Rename multi
        """
        return self.sampler.execute(self.rename_cmd, ())

    def get_no_items(self):
        """Get Number of Multis in Memory

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_curr_handle(self):
        """Current Multi Index (i.e., its position in memory)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_curr_handle_cmd, ())

    def get_curr_name(self):
        """Get Current Multi Name

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_curr_name_cmd, ())

    def get_names(self):
        """Get the Names of All Multis in memory

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_names_cmd, ())

    def set_curr_by_handle(self, arg0):
        """Select by handle
        """
        return self.sampler.execute(self.set_curr_by_handle_cmd, (arg0, ))

    def set_curr_by_name(self, arg0):
        """Select by name
        """
        return self.sampler.execute(self.set_curr_by_name_cmd, (arg0, ))

    def delete_all(self):
        """Delete ALL items from memory
        """
        return self.sampler.execute(self.delete_all_cmd, ())

    def delete_curr(self):
        """Delete current item from memory
        """
        return self.sampler.execute(self.delete_curr_cmd, ())

    def get_handles_names(self):
        """Get list of multi handles and names

        Returns:
            HANDLENAMEARRAY
        """
        handle_names = []
        names = self.get_names()
        for i in range(len(names)):
            handle_names.extend([i, names[i]])
        return handle_names

