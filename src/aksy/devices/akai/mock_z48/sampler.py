import logging, shutil

from aksy.devices.akai import sysex_types, model
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai.z48.sampler import Z48
from aksyx import AkaiSampler
from aksy import fileutils

log = logging.getLogger('aksy')

class MockConnector(object):
    def __init__(self):
        self.sample_file = ''
        self.program_file = ''
        
    def get(self, filename, destpath=None, source=AkaiSampler.MEMORY):
        log.debug("Transferring file %s to host from source %i" % (filename, source))
        try:
            if fileutils.is_sample(filename):
                shutil.copy(self.sample_file, destpath)
            elif fileutils.is_program(filename):
                shutil.copy(self.program_file, destpath)
        except IOError:
            raise model.SamplerException("Failed to get ", filename)

    def put(self, path, remote_name=None, destination=AkaiSampler.MEMORY):
        log.debug("Transferring file %s to sampler at remote_name %s (%i)" 
                  % (path, remote_name, destination))
    
    def execute(self, command, args, request_id=0):
        log.debug("execute(%s, %s)" % (repr(command), repr(args),))
        return None
    
    def close(self):
        log.debug("close()")
        
    
class MockZ48(Z48):
    def __init__(self, connector, debug=1): 
        # TODO: enable call to super class c'tor
        Sampler.__init__(self, connector)
        self.connector = connector
        self.debug = debug
        self.setup_tools()

        self._patch_disktools_get_disklist()
        
        self._patch_systemtools()
        
        self.programtools.get_handles_names = lambda : (1, 'program', 2, 'program 2')
        self.songtools.get_handles_names = lambda : (1, 'song',)
        self.multitools.get_handles_names = lambda : (1, 'multi', 2, 'multi 2')
        self.sampletools.get_handles_names = lambda : (1, 'sample', 2, 'sample 2')
        self.recordingtools.get_name = lambda : 'sample'
        
        self.setup_model()

        self._populate_fs()

        self._patch_rootdisk_getdir()

    def set_sample(self, sample):
	self.connector.sample_file = sample

    def set_program(self, program):
	self.connector.program_file = program

    def _populate_fs(self):
        mellotron_folder = model.Folder('Mellotron Samples')
        choir_folder = model.Folder('Choir')
        choir_folder.children.extend(
            (model.FileRef('Mellotron/Choir/Choir.AKM', 7102),
            model.FileRef('Mellotron/Choir/Choir.AKP', 7707),
            model.FileRef('Mellotron/Choir/Vox1.wav'),))

        mellotron_folder.children.extend(
            (choir_folder,
            model.FileRef('Mellotron Samples/A Sample.AKP'),
            model.FileRef('Mellotron Samples/Sample.wav'),))
        first_disk = self.disks.get_children()[0] 
        first_disk.root.children = [model.Folder('Autoload'),
             model.Folder('Songs')]
        self.disks.get_children()[1].root.children = [mellotron_folder]

        memory_items = [model.Sample("Boo", 1),
            model.Multi("Default", 2),]
        for i in range(0, 100):
            memory_items.append(model.Sample("Sample%i" %i, i))
        self.memory.set_children(memory_items)
        self.memory.get_children()[0].get_modified = lambda : True

    def _patch_disktools_get_disklist(self):
        def get_disklist(): 
            return [(256, 1, 0, 3, True, "Samples disk"),
                    (512, 1, 0, 3, False, "Cdrom")]
        
        self.disktools.get_disklist = get_disklist

    def _patch_systemtools(self):
        self.systemtools.get_free_wave_mem_size = lambda : 4
        self.systemtools.get_wave_mem_size = lambda : 16
        
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
        
    def close(self):
        pass
