
""" Python equivalent of akai section songtools

Methods to manipulate in-memory songs
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Songtools:
    def __init__(self, s56k):
        self.sampler = s56k
        self.rename_cmd = Command('^', '\x16\x09', 'rename', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_items_cmd = Command('^', '\x16\x10', 'get_no_items', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_handle_cmd = Command('^', '\x16\x13', 'get_curr_handle', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_name_cmd = Command('^', '\x16\x14', 'get_curr_name', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_names_cmd = Command('^', '\x16\x12', 'get_names', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_handle_cmd = Command('^', '\x16\x06', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.WORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_name_cmd = Command('^', '\x16\x05', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_all_cmd = Command('^', '\x16\x07', 'delete_all', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_curr_cmd = Command('^', '\x16\x08', 'delete_curr', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)

    def rename(self):
        """Rename Song
        """
        return self.sampler.execute(self.rename_cmd, ())

    def get_no_items(self):
        """Get Number of Songs in Memory

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_curr_handle(self):
        """Current Song Index (i.e., its position in memory)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_curr_handle_cmd, ())

    def get_curr_name(self):
        """Get Current Song Name

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_curr_name_cmd, ())

    def get_names(self):
        """Get the Names of All Songs in memory

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

