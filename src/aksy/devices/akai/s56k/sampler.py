import struct
import os.path
import sys

import sysextools, disktools, programtools, sampletools, multitools, songtools
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai import sysex
from aksy.devices.akai import model

class S56K(Sampler):
    """S56K
    """
    def __init__(self, debug=1):
        Sampler.__init__(self, Sampler.S56K, debug)
        # TODO: remove duplication

        self.disktools = disktools.Disktools(self)
        self.sysextools = sysextools.Sysextools(self)
        self.programtools = programtools.Programtools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.songtools = songtools.Songtools(self)
        self.multitools = multitools.Multitools(self)

        model.register_handlers({model.Disk: self.disktools,
                        model.FileRef: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools, 
                        model.Song: self.songtools})
        
        self.sysextools.enable_msg_notification(False)
        self.sysextools.enable_item_sync(False)
        
        self.disks = model.RootDisk('disks', self.disktools.get_disklist())
        self.memory = model.Memory('memory')

