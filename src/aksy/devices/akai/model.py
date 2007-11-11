"""aksy model

Offers a high level sampler API

"""
import os.path, logging
from aksyx import AkaiSampler
from aksy import fileutils


handlers = {}
LOG = logging.getLogger("aksy.model")

def register_handlers(tools):
    """Initialize the handlers, keyed on class
    definitions.
    """
    handlers.update(tools)

class SamplerException(Exception):
    """ Exception raised by the sampler
    """
    def __init(self, msg, code):
        Exception.__init__(self, msg)
        self.code = code

    def get_code(self):
        return self.code

class Container(object):
    def get_children(self):
        raise NotImplementedError()

    def get_child(self, name):
        for child in self.get_children():
            if child.get_name() == name:
                return child
        return None

class Disk(Container):
    def __init__(self, (handle, disk_type, format, scsi_id, writable, name)):
        self._handle = handle
        # type: 0=floppy; 1=hard disk; 2=CD ROM; 3=removable disk.
        self._disk_type = disk_type
        # format, where: 0=other; 1=MSDOS; 2=FAT32; 3=ISO9660; 4=S1000; 5=S3000; 6=EMU; 7=ROLAND, 
        # 8=CD-AUDIO, 100=EMPTY
        self._format = format
        self._scsi_id = scsi_id
        self._writable = writable
        self._name = name
        self.root = Folder("")

    def has_children(self):
        try:
            self.set_current()
            return self.root.has_children()
        except SamplerException:
            return False

    def get_handle(self):
        return self._handle

    def is_writable(self):
        return self._writable
    
    def set_current(self):
        handlers[Disk].select_disk(self.get_handle())

    def get_name(self):
        return self._name
    
    def get_short_name(self):
        return self.get_name()
    
    def get_size(self):
        return None

    def get_modified(self):
        return False
    
    def create_folder(self, name):
        self.root.create_folder(name)

    def get_children(self):
        self.set_current()
        return self.root.get_children()
    
    def refresh(self):
        self.root.refresh()
        
    def get_actions(self):
        return ('upload',)
    
def get_file_type(name):
    assert name is not None
    
    if fileutils.is_multi(name):
        return Multi, FileRef.MULTI
    if fileutils.is_program(name):
        return Program, FileRef.PROGRAM
    if fileutils.is_sample(name):
        return Sample, FileRef.SAMPLE
    if fileutils.is_song(name):
        return Song, FileRef.SONG
    
    msg = "No support for file type: %s", name
    LOG.exception(msg)
    raise NotImplementedError(msg)
    
class FileRef(object):
    FOLDER = 0
    MULTI = 1
    PROGRAM = 2
    SAMPLE = 3
    SONG = 4

    def __init__(self, path, size=None):
        """Initializes a file object - A multi, program or sample before it
        is loaded into memory
        """
        self.path = path
        self.size = size
        self.type = get_file_type(self.get_name())[1]

    def get_name(self):
        return os.path.basename(self.path)
    
    def get_short_name(self):
        """ Returns name without extension
        """
        return os.path.splitext(self.get_name())[0]

    def get_handle(self):
        """Returns handle for the file
        """
        return self.path

    def get_size(self):
        return self.size

    def get_modified(self):
        """Returns True if this file has been modified
        """
        return True

    def has_children(self):
        return False

    def copy(self, dest_path):
        """Copies a file
        """
        item = self.load()
        new_parent = Folder(dest_path)

        return new_parent.append_child(item)

    def load(self):
        """Load the file into memory
        """
        self.get_parent().set_current()
        handlers[Disk].load_file(self.get_name())
        return InMemoryFile.get_instance(self.get_name())

    def download(self, path):
        """download the file to host
        """
        LOG.info("download of file %s to %s" % (self.get_name(), repr(path)))
        # XXX: remove the reference to the sampler
        handlers[Disk].z48.transfertools.get(self.get_name(), path)

    def get_parent(self):
        return Folder(os.path.dirname(self.path))

    def delete(self):
        self.get_parent().set_current()
        handlers[Disk].delete(self.get_name())

    def rename(self, new_name):
        self.get_parent().set_current()
        handlers[Disk].rename_file(self.get_name(), new_name)
        self.path = os.path.join(os.path.dirname(self.path, new_name))

    def get_actions(self):
        return ('load', 'delete', 'download',)

class Folder(FileRef, Container):
    def __init__(self, path):
        self.path = path
        self.type = FileRef.FOLDER
        self.children = []
        self.writable = True

    def set_writable(self, writable):
        self.writable = writable
        
    def is_writable(self):
        return self.writable
    
    def refresh(self):
        del self.children[:]

    def get_actions(self):
        return ('load', 'delete', 'download',)

    def get_children(self):
        """Gets the children of this folder
        or returns a cached version when already retrieved.
        """
        if len(self.children) > 0:
            return self.children

        self.set_current()
        folder_names = handlers[Disk].get_folder_names()
        if folder_names:
            self.children = [Folder(os.path.join(self.path, folder_name))
                for folder_name in folder_names if fileutils.is_valid_name(folder_name)]

        file_names_sizes = handlers[Disk].get_filenames()
        if file_names_sizes:
            self.children.extend(self.get_filename_sizes(file_names_sizes))
        return self.children

    def get_filename_sizes(self, names_sizes):
        for i in range(0, len(names_sizes), 2):
            name, size = names_sizes[i], names_sizes[i+1]
            if fileutils.is_file(name):
                yield FileRef(os.path.join(self.path, name), size)

    def get_child(self, name):
        for child in self.get_children():
            if child.get_name() == name:
                return child
        return None
    
    def has_children(self):
        return (len(self.children) > 0 or handlers[Disk].get_no_files() > 0 or
            handlers[Disk].get_no_folders() > 0)

    def get_name(self):
        return os.path.basename(self.path)

    def set_current(self):
        handlers[Disk].open_folder('')
        path = self.path.replace('/', '\\')
        handlers[Disk].open_folder(path)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("set_current to: %s" % path)

    def copy(self, dest_path, recursive=True):
        """Copies a folder, default is including all its children
        """
        # copy the folder
        # copy the children to the new path

    def rename(self, new_name):
        self.get_parent().set_current()
        handlers[Disk].rename_folder(self.get_name(), new_name)
        self.path = self.path.replace(self.get_name(), new_name)

    def load(self):
        self.get_parent().set_current()
        handlers[Disk].load_folder(self.get_name())
        LOG.debug("Loading folder children %s" % repr (self.get_children()))
        return [item for item in self.get_children()]

    def create_folder(self, name):
        self.get_parent().set_current()
        handlers[Disk].create_folder(name)
        folder = Folder(os.path.join(self.path, name))
        self.children.append(folder)
        return folder

    def upload(self, path):
        self.set_current()
        name = os.path.basename(path)
        handlers[Disk].z48.put(path, name, destination=AkaiSampler.DISK)
        item = FileRef(self.path + (name,))
        self.children.append(item)
        return item

    def append_child(self, item):
        """Adds a child item to this folder
        Returns the added item
        """
        self.set_current()
        handlers[Disk].save(item.get_handle(), item.type, True, False)
        item = FileRef(self.path + (item.name,))
        self.children.append(item)
        return item

    def download(self, path):
        """download the folder to host
        """
        self.get_parent().set_current()
        path = os.path.join(path, self.get_name())
        LOG.info("download to dir: %s" % repr(path))
        if not os.path.exists(path):
            os.makedirs(path)
            for item in self.get_children():
                LOG.debug("download to dir: %s" % repr(path))
                item.download(os.path.join(path, item.get_name()))

class InMemoryFile(FileRef):
    @staticmethod
    def get_instance(name):
        clazz = get_file_type(name)[0]
        base_name = os.path.splitext(name)[0]
        handle = handlers[clazz].get_handle_by_name(base_name)
        return clazz(base_name, handle)

    def __cmp__(self, item):
        return cmp(self.get_short_name(), item.get_short_name())
    
    def __init__(self, name, handle):
        self.name = name
        self.handle = handle
        FileRef.__init__(self, (name,))

    def get_actions(self):
        return ('delete', 'download', 'copy')
    
    def get_name(self):
        return self.name
    
    def get_short_name(self):
        """ Returns name without extension
        """
        return os.path.splitext(self.get_name())[0]

    def get_handle(self):
        """Returns the handle
        """
        return self.handle

    def get_modified(self):
        self.set_current()
        return handlers[self.__class__].get_modified()
    
    def set_current(self):
        handlers[self.__class__].set_curr_by_name(self.get_short_name())

    def delete(self):
        LOG.info("InMemoryFile.delete() %s" % repr(self.get_name()))
        handlers[self.__class__].get_no_items()
        self.set_current()
        handlers[self.__class__].delete_curr()

    def save(self, overwrite, children=False):
        handlers[Disk].save(self.get_handle(), self.type, 
                                 overwrite, children)

    def download(self, dest_path):
        pass
    
    def copy(self, new_name):
        handlers[self.__class__].copy(new_name)

    def rename(self, new_name):
        self.set_current()
        handlers[self.__class__].rename_curr(new_name)

class Multi(InMemoryFile):
    def __init__(self, name, handle):
        InMemoryFile.__init__(self, name, handle)
        self.type = FileRef.MULTI

    def get_name(self):
        return InMemoryFile.get_name(self) + ".akm"

class Program(InMemoryFile):
    def __init__(self, name, handle):
        InMemoryFile.__init__(self, name, handle)
        self.type = FileRef.PROGRAM
    def get_name(self):
        return InMemoryFile.get_name(self) + ".akp"

class Sample(InMemoryFile):
    def __init__(self, name, handle):
        InMemoryFile.__init__(self, name, handle)
        self.type = FileRef.SAMPLE

    def get_name(self):
        return InMemoryFile.get_name(self) + ".wav"

    def copy(self, name):
        raise NotImplementedError("Copy not implemented for samples")
    
    def get_size(self):
        self.set_current()
        handlers[Sample].get_sample_length()
        
class Song(InMemoryFile):
    def __init__(self, name, handle):
        InMemoryFile.__init__(self, name, handle)
        self.type = FileRef.SONG

    def get_name(self):
        return InMemoryFile.get_name(self) + ".mid"
    
class Storage(Container):
    def __init__(self, name):
        self.name = name
        self.path = name
        self.actions = None
        self.type = FileRef.FOLDER
        self.children = []

    def refresh(self):
        del self.children[:]
        
    def has_children(self):
        return (len(self.children) > 0)

    def get_name(self):
        return self.name

    def get_short_name(self):
        return self.get_name()

    def get_handle(self):
        return self.name

    def get_children(self):
        return self.children

    def set_children(self, item_list):
        self.children = item_list

    def get_actions(self):
        # maybe implement an info action?
        return ()

class RootDisk(Storage):
    def __init__(self, name, disk_list):
        Storage.__init__(self, name)
        self.set_children([Disk(disk) for disk 
            in disk_list])

    def is_writable(self):
        return False

class Memory(Storage):
    def __init__(self, name):
        Storage.__init__(self, name)

    def is_writable(self):
        return True
    
    def get_actions(self):
        return ('upload',)
    
    def upload(self, path):
        name = os.path.basename(path)
        handlers[Disk].z48.put(path, name)
        item = InMemoryFile.get_instance(name)
        self.append_child(item)

    def append_child(self, item):
        self.children.append(item)
        return item

    def has_children(self):
        if len(self.children) > 0:
            return True
        return (handlers[Program].get_no_items() > 0 or
             handlers[Sample].get_no_items() > 0 or
             handlers[Song].get_no_items() > 0 or
             handlers[Multi].get_no_items() > 0)

    def get_children(self):
        if len(self.children) > 0:
            return self.children
        
        self.children.extend(self.get_handles_names(Program))
        self.children.extend(self.get_handles_names(Multi))
        self.children.extend(self.get_handles_names(Sample))
        self.children.extend(self.get_handles_names(Song))

        return self.children
    
    def get_handles_names(self, clz):
        handles_names = handlers[clz].get_handles_names()
        for i in range(0, len(handles_names), 2):
            handle, name = handles_names[i], handles_names[i+1]
            yield clz(name, handle)


