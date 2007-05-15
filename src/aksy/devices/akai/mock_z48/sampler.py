import logging
from aksy.devices.akai import sysex_types
from aksy.devices.akai.z48.sampler import Z48
from aksy import model

log = logging.getLogger('aksy')
class MockZ48(Z48):
    def __init__(self, debug=1):
        self.debug = debug
        self.setup_tools()
        def get_disklist(): return [sysex_types.DiskInfo((256, 1, 0, 3, True, "Samples disk")),
            sysex_types.DiskInfo((512, 1, 0, 3, False, "Cdrom"))]
        
        self.disktools.get_disklist = get_disklist
        self.setup_model()

        mellotron_folder = model.Folder(('', 'Mellotron',))
        choir_folder = model.Folder(('', 'Choir',))
        choir_folder.children.extend(
            (model.FileRef(('', 'Mellotron', 'Choir', 'Choir.AKM',)),
            model.FileRef(('', 'Mellotron', 'Choir', 'Choir.AKP',)),
            model.FileRef(('', 'Mellotron', 'Choir', 'Vox1.wav',)),))

        mellotron_folder.children.extend(
            (choir_folder,
            model.FileRef(('', 'Mellotron', 'Sample.AKP',)),
            model.FileRef(('', 'Mellotron', 'Sample.wav',)),))
        first_disk = self.disks.get_children()[0] 
        first_disk.root.children = [model.Folder(('', 'Autoload',)),
             model.Folder(('', 'Songs',))]
        self.disks.get_children()[1].root.children = [mellotron_folder]
        
        def get_subdir(obj, path):
            for c in obj.get_children():
                if c.get_name() == path:
                    return c

        def get_dir(path):
            segments = path.split('/')
            folder = self.disks
            while segments and folder is not None:
                print segments
                folder = get_subdir(folder, segments.pop(0))
            print folder
            return folder


        self.disks.get_dir = get_dir
           
        memory_items = [model.Sample("Boo.wav"),
            model.Multi("Default.akm"),]
        for i in range(0, 100):
            memory_items.append(model.Sample("Sample%i.wav" %i))
        self.memory.set_children(memory_items)

    def get(self, filename, destpath=None):
        if self.debug > 0:
            log.debug("Transferring file %s to host" % filename)

    def put(self, path, remote_name=None, destination=Z48.MEMORY):
        if self.debug > 0:
            log.debug("Transferring file %s to sampler" % path)

    def execute(self, command, args, request_id=0):
        # work with stored sessions later on
        log.debug("Executing command: %s " % command.name)
        return None
