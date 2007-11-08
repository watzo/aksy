import logging

import sysextools, disktools, programtools, multitools, songtools, multifxtools
import sampletools, systemtools, recordingtools, keygrouptools, zonetools, frontpaneltools
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai import model

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
        self.disktools = disktools.Disktools(self.connector)
        self.programtools = programtools.Programtools(self.connector)
        self.keygrouptools = keygrouptools.Keygrouptools(self.connector)
        self.zonetools = zonetools.Zonetools(self.connector)
        self.sampletools = sampletools.Sampletools(self.connector)
        self.songtools = songtools.Songtools(self.connector)
        self.multitools = multitools.Multitools(self.connector)
        self.multifxtools = multifxtools.Multifxtools(self.connector)
        self.systemtools = systemtools.Systemtools(self.connector)
        self.sysextools = sysextools.Sysextools(self.connector)
        self.recordingtools = recordingtools.Recordingtools(self.connector)
        self.frontpaneltools = frontpaneltools.Frontpaneltools(self.connector)

    def setup_model(self):
        model.register_handlers({model.Disk: self.disktools,
                        model.FileRef: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools,
                        model.Song: self.songtools})

        self.disks = model.RootDisk('disks', self.disktools.get_disklist())
        self.memory = model.Memory('memory')
