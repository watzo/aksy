import logging

import sysextools, disktools, programtools, multitools, sampletools, systemtools, recordingtools
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai import sysex
from aksy import model

log = logging.getLogger("aksy")

class Z48(Sampler):
    """Z48
    """
    def __init__(self, debug=1, usb_product_id=Sampler.Z48):
        Sampler.__init__(self, usb_product_id, debug)
        # not fool proof for multiple disks
        #disk = model.Disk(self.disktools.get_disklist())
        #self.disktools.select_disk(disk.handle)
        #rootfolder = model.Folder(("",))
        #folders = rootfolder.get_children()
        #disks.set_children(folders)

        self.disktools = disktools.Disktools(self)
        self.programtools = programtools.Programtools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.multitools = multitools.Multitools(self)
        self.systemtools = systemtools.Systemtools(self)
        self.sysextools = sysextools.Sysextools(self)
        self.recordingtools = recordingtools.Recordingtools(self)

        model.register_handlers({model.Disk: self.disktools,
                        model.File: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools})

        self.disks = model.Storage('disk')
        self.memory = model.Memory('memory')

        self.sysextools.enable_msg_notification(False)
        self.sysextools.enable_item_sync(False)

class MPC4K(Z48):
    def __init__(self, debug=1):
        Z48.__init__(self, debug=1, usb_product_id=Sampler.MPC4K)
