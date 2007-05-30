import logging, shutil

from aksy.devices.akai import sysex_types
from aksy.devices.akai.z48.sampler import Z48
from aksy import model, fileutils
import errno
log = logging.getLogger('aksy')

class MockZ48(Z48):
    def __init__(self, debug=1, sampleFile=None):
        self.debug = debug
        self.sampleFile = sampleFile
        self.setup_tools()

        self._patch_disktools_get_disklist()
        
        self._patch_systemtools()

        self.setup_model()

        self._populate_fs()

        self._patch_rootdisk_getdir()

    def get(self, filename, destpath=None, source=Z48.MEMORY):
        if self.debug > 0:
            log.debug("Transferring file %s to host from source %i" % (filename, source)) 
        if fileutils.is_sample(destpath):
            if self.sampleFile is not None:
                shutil.copy(self.sampleFile, destpath)
            else:
                raise IOError(errno.ENOENT, "File not found", destpath)

    def put(self, path, remote_name=None, destination=Z48.MEMORY):
        if self.debug > 0:
            log.debug("Transferring file %s to sampler" % path)

    def execute(self, command, args, request_id=0):
        # TODO: work with stored sessions
        log.debug("Executing command: %s " % command.name)
        return None

    def _populate_fs(self):
        mellotron_folder = model.Folder('Mellotron Samples')
        choir_folder = model.Folder('Choir')
        choir_folder.children.extend(
            (model.FileRef('Mellotron/Choir/Choir.AKM'),
            model.FileRef('Mellotron/Choir/Choir.AKP'),
            model.FileRef('Mellotron/Choir/Vox1.wav'),))

        mellotron_folder.children.extend(
            (choir_folder,
            model.FileRef('Mellotron Samples/A Sample.AKP'),
            model.FileRef('Mellotron Samples/Sample.wav'),))
        first_disk = self.disks.get_children()[0] 
        first_disk.root.children = [model.Folder('Autoload'),
             model.Folder('Songs')]
        self.disks.get_children()[1].root.children = [mellotron_folder]

        memory_items = [model.Sample("Boo"),
            model.Multi("Default"),]
        for i in range(0, 100):
            memory_items.append(model.Sample("Sample%i" %i))
        self.memory.set_children(memory_items)
        print self.memory.get_children()[0]
        self.memory.get_children()[0].get_modified = lambda : True

    def _patch_disktools_get_disklist(self):
        def get_disklist(): 
            return [sysex_types.DiskInfo((256, 1, 0, 3, True, "Samples disk")),
                    sysex_types.DiskInfo((512, 1, 0, 3, False, "Cdrom"))]
        
        self.disktools.get_disklist = get_disklist

    def _patch_systemtools(self):
        def get_free_mem():
            return 4

        def get_total_mem():
            return 16
        self.systemtools.get_free_wave_mem_size = get_free_mem
        self.systemtools.get_wave_mem_size = get_total_mem
        
    def _patch_rootdisk_getdir(self):
        def get_subdir(obj, path):
            for child in obj.get_children():
                if child.get_name() == path:
                    return child

        def get_dir(path):
            segments = path.split('/')
            folder = self.disks
            while segments and folder is not None:
                folder = get_subdir(folder, segments.pop(0))
            return folder

        self.disks.get_dir = get_dir
