import sys, aksy, logging, os.path
from aksy.devices.akai.sysex import Request, Reply
from aksy.devices.akai import sysex_types
from aksy.devices.akai.z48.sampler import Z48
from aksy import model

log = logging.getLogger('aksy')
class MockZ48(Z48):
    def __init__(self, debug=1):
        self.debug = debug
        self.setupTools()
        def get_disklist(): return []
        self.disktools.get_disklist = get_disklist
        self.setupModel()

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
        disks = [model.Disk(info) for info in
            sysex_types.DiskInfo((256, 1, 0, 3, True, "Samples disk")),
            sysex_types.DiskInfo((512, 1, 0, 3, False, "Cdrom"))]
        disks[0].root.children = [model.Folder(('', 'Autoload',)),
             model.Folder(('', 'Songs',))]
        disks[1].root.children = [mellotron_folder]

        self.disks.set_children(disks)
        self.memory.set_children((
            model.Sample("Boo.wav"),
            model.Multi("Default.akm"),))

    def get(self, filename, destpath=None):
        if self.debug > 0:
            log.debug("Transferring file %s to host" % filename)

    def put(self, path, remote_name=None, destination=Z48.MEMORY):
        if self.debug > 0:
            log.debug("Transferring file %s to sampler" % path)

    def execute(self, command, args, request_id=0):
        # work with stored sessions later on
        log.debug("Executing command: %s " % command.name)
        request = Request(command, args)
        return None
