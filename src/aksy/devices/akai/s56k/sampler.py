import logging

import sysextools, disktools, programtools, sampletools, multitools, songtools
from aksy.devices.akai.sampler import Sampler
#from aksy.devices.akai import sysex
from aksy.devices.akai import model

log = logging.getLogger("aksy")

class S56K(Sampler):
    """S56K
    """
    def __init__(self, connector):
        Sampler.__init__(self, connector)
        self.setup_tools()

        self.sysextools.enable_msg_notification(False)
        self.sysextools.enable_item_sync(False)
        
        self.setup_model()

    def setup_tools(self):
        self.disktools = disktools.Disktools(self.connector)
        self.programtools = programtools.Programtools(self.connector)
        self.sampletools = sampletools.Sampletools(self.connector)
        self.songtools = songtools.Songtools(self.connector)
        self.multitools = multitools.Multitools(self.connector)
        self.sysextools = sysextools.Sysextools(self.connector)

    def setup_model(self):
        model.register_handlers({model.Disk: self.disktools,
                        model.FileRef: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools, 
                        model.Song: self.songtools})
        
        self.disks = model.RootDisk('disks', self.disktools.get_disklist())
        self.memory = model.Memory('memory')

