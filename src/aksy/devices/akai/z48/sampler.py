import logging

import sysextools, disktools, programtools, multitools, songtools, multifxtools
import sampletools, systemtools, recordingtools, keygrouptools, zonetools, frontpaneltools
from aksy.devices.akai.sampler import Sampler
from aksy import model

log = logging.getLogger("aksy")

class Z48(Sampler):
    """Z48
    """
    def __init__(self, connector):
        Sampler.__init__(self, connector)
        self.setup_tools()

        self.sysextools.enable_msg_notification(False)
        self.sysextools.enable_item_sync(False)
        
        self.setup_model()

    def setup_tools(self):
        self.disktools = disktools.Disktools(self)
        self.programtools = programtools.Programtools(self)
        self.keygrouptools = keygrouptools.Keygrouptools(self)
        self.zonetools = zonetools.Zonetools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.songtools = songtools.Songtools(self)
        self.multitools = multitools.Multitools(self)
        self.multifxtools = multifxtools.Multifxtools(self)
        self.systemtools = systemtools.Systemtools(self)
        self.sysextools = sysextools.Sysextools(self)
        self.recordingtools = recordingtools.Recordingtools(self)
        self.frontpaneltools = frontpaneltools.Frontpaneltools(self)

    def setup_model(self):
        model.register_handlers({model.Disk: self.disktools,
                        model.FileRef: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools,
                        model.Song: self.songtools})

        self.disks = model.RootDisk('disks', self.disktools.get_disklist())
        self.memory = model.Memory('memory')
