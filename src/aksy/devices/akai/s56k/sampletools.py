
""" Python equivalent of akai section sampletools

Methods to manipulate in-memory samples
"""

__author__ =  'Walco van Loon'
__version__ =  '0.2'
__credits__ = ["Mike Goins"]

from aksy.devices.akai.sysex import Command

import aksy.devices.akai.sysex_types

class Sampletools:
    def __init__(self, s56k):
        self.sampler = s56k
        self.set_curr_by_name_cmd   = Command('^', '\x0e\x05', 'sampletools', 'set_curr_by_name', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.set_curr_by_handle_cmd = Command('^', '\x0e\x06', 'sampletools', 'set_curr_by_handle', (aksy.devices.akai.sysex_types.CWORD,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_all_cmd         = Command('^', '\x0e\x07', 'sampletools', 'delete_all', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.delete_curr_cmd        = Command('^', '\x0e\x08', 'sampletools', 'delete_curr', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.rename_curr_cmd        = Command('^', '\x0e\x09', 'sampletools', 'rename', (aksy.devices.akai.sysex_types.STRING,), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.play_cmd               = Command('^', '\x0e\x0a', 'sampletools', 'play', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.stop_cmd               = Command('^', '\x0e\x0b', 'sampletools', 'stop', (), (), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_no_items_cmd       = Command('^', '\x0e\x10', 'sampletools', 'get_no_items', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_name_by_handle_cmd = Command('^', '\x0e\x11', 'sampletools', 'get_name_by_handle', (aksy.devices.akai.sysex_types.CWORD,), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_names_cmd          = Command('^', '\x0e\x12', 'sampletools', 'get_names', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_handle_cmd    = Command('^', '\x0e\x13', 'sampletools', 'get_curr_handle', (), (aksy.devices.akai.sysex_types.CWORD,), aksy.devices.akai.sysex_types.S56K_USERREF)
        self.get_curr_name_cmd      = Command('^', '\x0e\x14', 'sampletools', 'get_curr_name', (), (aksy.devices.akai.sysex_types.STRINGARRAY,), aksy.devices.akai.sysex_types.S56K_USERREF)
        

    def set_curr_by_name(self, arg0):
        """Select current item by name
        """
        return self.sampler.execute(self.set_curr_by_name_cmd, (arg0, ))

    def set_curr_by_handle(self, arg0):
        """Select current item by handle
        """
        return self.sampler.execute(self.set_curr_by_handle_cmd, (arg0, ))

    def delete_all(self):
        """Delete ALL items from memory
        """
        return self.sampler.execute(self.delete_all_cmd, ())

    def delete_curr(self):
        """Delete current item from memory
        """
        return self.sampler.execute(self.delete_curr_cmd, ())

    def rename(self):
        """Rename Sample
        """
        return self.sampler.execute(self.rename_curr_cmd, ())

    def play(self, arg0=127, arg1=0):
        """Start auditioning the current sample
        """
        return self.sampler.execute(self.play_cmd, ())

    def stop(self):
        """Stop playback of the current sample
        """
        return self.sampler.execute(self.stop_cmd, ())

    def get_no_items(self):
        """Get Number of Samples in Memory

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_no_items_cmd, ())

    def get_name_by_handle(self, arg0):
        """Get item name from handle

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_name_by_handle_cmd, (arg0, ))

    def get_names(self):
        """Get the Names of All Samples in memory

        Returns:
            STRINGARRAY
        """
        return self.sampler.execute(self.get_names_cmd, ())

    def get_curr_handle(self):
        """Current Sample Index (i.e., its position in memory)

        Returns:
            WORD
        """
        return self.sampler.execute(self.get_curr_handle_cmd, ())

    def get_curr_name(self):
        """Get Current Sample Name

        Returns:
            STRING
        """
        return self.sampler.execute(self.get_curr_name_cmd, ())


    def get_handles_names(self):
        """Get list of sample handles and names

        Returns:
            HANDLENAMEARRAY
        """
        handle_names = []
        names = self.get_names()
        for i in range(len(names)):
            handle_names.extend([i, names[i]])
        return handle_names

    def get_handle_by_name(self, arg0):
        """Get item handle from name

        Returns:
            DWORD
        """
        self.sampler.execute(self.set_curr_by_name_cmd, (arg0, ))
        return self.sampler.execute(self.get_curr_handle_cmd, ())

