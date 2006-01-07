import sys, aksy, logging, os.path
from aksy.devices.akai.sysex import Request, Reply
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai.z48 import sysextools, disktools, programtools, sampletools, multitools
from aksy import model

log = logging.getLogger('aksy')
class Z48(Sampler):
    MEMORY = 1
    """
    >>> z = Z48()
    """
    def __init__(self, debug=1):
        self.disks = aksy.model.Storage('disk')
        self.memory = aksy.model.Memory('memory')
        self.sysextools = sysextools.Sysextools(self)
        self.disktools = disktools.Disktools(self)
        self.programtools = programtools.Programtools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.multitools = multitools.Multitools(self)
        model.register_handlers({model.Disk: self.disktools,
              model.File: self.disktools,
              model.Program: self.programtools,
              model.Sample: self.sampletools,
              model.Multi: self.multitools})

        rootfolder = model.Folder(("",))
        rootfolder.children.append(model.Folder(('', 'Autoload',)))
        rootfolder.children.append(model.Folder(('', 'Songs',)))
        mellotron_folder = model.Folder(('', 'Mellotron',))
        choir_folder = model.Folder(('', 'Choir',))
        choir_folder.children.extend(
            (model.File(('', 'Mellotron', 'Choir', 'Choir.AKM',)),
            model.File(('', 'Mellotron', 'Choir', 'Choir.AKP',)),
            model.File(('', 'Mellotron', 'Choir', 'Vox1.wav',)),))

        mellotron_folder.children.extend(
            (choir_folder,
            model.File(('', 'Mellotron', 'Sample.AKP',)),
            model.File(('', 'Mellotron', 'Sample.wav',)),))
        rootfolder.children.append(mellotron_folder)
        self.disks.set_children(rootfolder.get_children())
        self.memory.set_children(choir_folder.get_children())

    def get(self, filename, destpath):
        if self.debug > 0:
            log.debug("Transferring file %s to host" % filename)

    def put(self, path, remote_name, destination=MEMORY):
        if self.debug > 0:
            log.debug("Transferring file %s to sampler" % path)

    def execute(self, command, args, z48id=None, userref=None):
        # work with stored sessions later on
        log.debug("Executing command: %s " % command.name)
        request = Request(command, args)
        return None
