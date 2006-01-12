import struct
import os.path
import sys

import sysextools, disktools
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai import sysex
from aksy import model

class S56K(Sampler):
    """S56K
    """
    def __init__(self, debug=1):
        Sampler.__init__(self, Sampler.S56K, debug)

        self.disktools = disktools.Disktools(self)
        self.sysextools = sysextools.Sysextools(self)

        model.register_handlers({model.Disk: self.disktools,
                        model.File: self.disktools})

        self.disks = model.Storage('disk')
        self.memory = model.Memory('memory')

        self.sysextools.enable_msg_notification(False)
        self.sysextools.enable_item_sync(False)
