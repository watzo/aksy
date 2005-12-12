from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai import sysex
from aksy import model

import struct
import os.path
import sys

class S56K(Sampler):
    """S56K
    """
    def __init__(self, debug=1):
        Sampler.__init__(self, Sampler.S56K, debug)
        import sysextools, disktools

        self.disktools = disktools.Disktools(self)
        self.sysextools = sysextools.Sysextools(self)

        model.register_handlers({model.Disk: self.disktools,
                        model.File: self.disktools})

        self.disks = model.Storage('disk')
        self.memory = model.Memory('memory')

        try:
            # this command sometimes doesn't yield a response
            self.sysextools.enable_msg_notification(False)
        except Exception, e:
            print e
        self.sysextools.enable_item_sync(False)

    def get(self, filename, destfile=None, source=Sampler.MEMORY):
        """Gets a file from the sampler, overwriting destfile if it already exists.
        """
        if source == AkaiSampler.MEMORY:
            self._get_by_handle(filename, destfile);
        else:
            self.get(filename, destfile, source)
