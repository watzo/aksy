import sys, aksy
from aksy.devices.akai.sysex import Request, Reply
from aksy.devices.akai.z48 import disktools, programtools, sampletools, multitools
from aksy import model

class Sampler:
    MEMORY = 1
    """
    >>> z = MockZ48()
    >>> z.init()
    """
    def __init__(self, debug=0):
        print "INIT MOCK"
        self.debug = debug
        #self.command_spec = CommandSpec(
        #    r'\x47\x5f\x00', CommandSpec.ID, CommandSpec.ARGS)
        self.disks = aksy.model.Storage('disk')
        self.memory = aksy.model.Memory('memory')
        self.disktools = disktools.Disktools(self)
        self.programtools = programtools.Programtools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.multitools = multitools.Multitools(self)
        model.register_handlers({model.Disk: self.disktools,
              model.File: self.disktools,
              model.Program: self.programtools,
              model.Sample: self.sampletools,
              model.Multi: self.multitools})


    def init(self):
        if self.debug > 0:
            print "Init sampler"
            # Setup some items

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
            print "Transferring file %s to host" % filename

    def put(self, path, remote_name, destination=MEMORY):
        if self.debug > 0:
            print "Transferring file %s to sampler" % path

    def execute(self, command, args, z48id=None, userref=None):
        # work with stored sessions later on
        if self.debug > 0:
            print "Executing command: %s " % command.name
        request = Request(command, args)
        return None

    def close(self):
        if self.debug > 0:
            print "Close sampler"

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
