"""aksy model

Offers a high level sampler API

"""
import re, os.path, sys, logging
from aksyx import AkaiSampler

RE_MULTI = re.compile("\.[aA][kK][mM]$")
RE_PROGRAM = re.compile("\.[aA][kK][pP]$")
RE_SAMPLE = re.compile("\.[wW][aA][vV]$")
RE_SONG = re.compile("\.[mM][iI][dD]$")

handlers = {}
log = logging.getLogger("aksy")

def register_handlers(tools):
    """Initialize the handlers, keyed on class
    definitions.
    """
    handlers.update(tools)

class Disk(object):
    def __init__(self, disk_info):
        self.info = disk_info
        self.root = Folder("")

    def has_children(self):
        self.set_current()
        if self.info.format != 8:
            return self.root.has_children()
        return False

    def get_handle(self):
        return self.info.handle

    def set_current(self):
        if self.info.format != 8: # ejected disk!
            handlers[Disk].select_disk(self.get_handle())
        return None

    def get_name(self):
        return self.info.name
    def get_short_name(self):
        return self.get_name()
    
    def get_size(self):
        return None

    def get_used_by(self):
        return None

    def get_modified(self):
        return None

    def get_children(self):
        self.set_current()
        return self.root.get_children()
    
    def get_actions(self):
        return ('upload',)
    
def get_file_type(name):
        if RE_MULTI.search(name) is not None:
            return FileRef.MULTI
        if RE_PROGRAM.search(name) is not None:
            return FileRef.PROGRAM
        if RE_SAMPLE.search(name) is not None:
            return FileRef.SAMPLE
        
        log.error("No support for file type: ", name)
        return FileRef.SAMPLE
    
class FileRef(object):
    FOLDER = 0
    MULTI = 1
    PROGRAM = 2
    SAMPLE = 3
    SONG = 4

    def __init__(self, path):
        """Initializes a file object - A multi, program or sample before it
        is loaded into memory
        """

        assert isinstance(path, tuple) or isinstance(path, list)

        log.debug(repr(path))
        self.path = path
        self.type = get_file_type(self.get_name())

    def get_name(self):
        return self.path[-1]
    
    def get_short_name(self):
        """ Returns name without extension
        """
        return os.path.splitext(self.get_name())[0]

    def get_handle(self):
        """Returns a unique handle for the file
        """
        return self.path

    def get_size(self):
        return 'Unknown'

    def get_modified(self):
        """Returns True if this file has been modified
        """
        return None

    def get_used_by(self):
        """Returns the parent using this file
        """
        return None

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
        # XXX: self.path should reflect memory location
        if self.type == self.MULTI:
            return Multi(self.get_name())
        if self.type == self.PROGRAM:
            return Program(self.get_name())
        if self.type == self.SAMPLE:
            return Sample(self.get_name())
        else:
            sys.stderr.writelines("Not a supported type %i\n" %self.type)
            return Sample(self.get_name())

    def download(self, path):
        """download the file to host
        """
        log.info("download of file %s to %s" % (self.get_name(), repr(path)))
        # XXX: remove the reference to the sampler
        handlers[Disk].z48.get(self.get_name(), path)

    def get_children(self):
        """
        """
        return []

    def get_parent(self):
        return Folder(self.path[:-1])

    def delete(self):
        """
        """
        self.get_parent().set_current()
        handlers[Disk].delete_file(self.get_name())

    def rename(self, new_name):
        """
        """
        self.get_parent().set_current()
        handlers[Disk].rename_file(self.get_name(), new_name)
        self.path = self.path[:-1] + (new_name,)

    def get_actions(self):
        return ('load', 'delete', 'download',)

class Folder(FileRef):
    def __init__(self, path):
        """ TODO: find a nice solution for the primitive folder selection
        """
        self.path = path
        self.type = FileRef.FOLDER
        self.children = []

    def refresh(self):
        del self.children[:]

    def get_actions(self):
        return ('load', 'delete', 'download',)
        
    def get_children(self):
        """Gets the children of this folder
        or returns a cached version when already retrieved.
        """
        self.set_current()
        if len(self.children) > 0:
            return self.children

        folder_names = handlers[Disk].get_folder_names()
        if folder_names:
            self.children = [Folder(self.path + (subfolder,))
                for subfolder in folder_names]

        file_names = handlers[Disk].get_filenames()
        if file_names:
            files = [ FileRef((self.path + name,)) for name in
                file_names]
            self.children.extend(files)
        return self.children

    def has_children(self):

        return (len(self.children) > 0 or handlers[Disk].get_no_files() > 0 or
            handlers[Disk].get_no_folders() > 0)

    def get_name(self):
        return self.path[-1]

    def set_current(self):
        log.debug("Current folder before set_current: %s" % handlers[Disk].get_curr_path())
        for item in self.path:
            handlers[Disk].open_folder(item)
        log.debug("Current folder after set_current: %s" % handlers[Disk].get_curr_path())

    def copy(self, dest_path, recursive=True):
        """Copies a folder, default is including all its children
        """
        # copy the folder
        # copy the children to the new path

    def rename(self, new_name):
        self.get_parent().set_current()
        handlers[Disk].rename_folder(self.get_name(), new_name)
        self.path = self.path[:-1] + (new_name,)

    def load(self):
        """
        """
        self.get_parent().set_current()
        handlers[Disk].load_folder(self.get_name())
        log.debug("Loading folder children %s" % repr (self.get_children()))
        return [item for item in self.get_children()]

    def delete(self):
        """
        """
        self.get_parent().set_current()
        handlers[Disk].delete_folder(self.get_name())
        # could be optimized by using dicts instead of lists
        for item in self.get_parent().get_children():
            if item.get_name() == self.get_name():
               del item
               break

    def create_folder(self, name):
        """
        """
        self.get_parent().set_current()
        handlers[Disk].create_folder(name)
        folder = Folder(self.path + (name,))
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
        log.info("download to dir: %s" % repr(path))
        if not os.path.exists(path):
            os.makedirs(path)
            for item in self.get_children():
                log.debug("download to dir: %s" % repr(path))
                item.download(os.path.join(path, item.get_name()))

class InMemoryFile(FileRef):
    def get_instance(name):
        type = get_file_type(name)
        if type == FileRef.MULTI:
            return Multi(name)
        if type == FileRef.PROGRAM:
            return Program(name)
        if type == FileRef.SAMPLE:
            return Sample(name)
        if type == FileRef.SONG:
            return Song(name)
        log.error("Unknown file type: %s" % repr(name))
        return InMemoryFile(name)

    get_instance = staticmethod(get_instance)

    def __cmp__(self, item):
        return cmp(self.get_short_name(), item.get_short_name())
    
    def __init__(self, name):
        self.name = name
        FileRef.__init__(self, (name,))

    def get_actions(self):
        return ('delete', 'download',)
    
    def get_size(self):
        return 'Unknown'

    def get_used_by(self):
        return None

    def get_name(self):
        return self.name

    def get_handle(self):
        """Returns the handle
        """
        return handlers[self.__class__].get_handle_by_name(self.get_name())

    def set_current(self):
        handlers[self.__class__].set_curr_by_name(self.get_name())

    def delete(self):
        log.info("InMemoryFile.delete() %s" % repr(self.get_name()))
        handlers[self.__class__].get_no_items()
        self.set_current()
        handlers[self.__class__].delete_curr()

    def save(self, overwrite, children=False):
        handlers[Disk].save_file(self.get_handle(), self.type, overwrite, children)

    def download(self, dest_path):
        pass

    def rename(self, new_name):
        self.set_current()
        handlers[self.__class__].rename_curr(new_name)

class Multi(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = FileRef.MULTI

class Program(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = FileRef.PROGRAM

class Sample(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = FileRef.SAMPLE

    def get_size(self):
        handlers[Sample].get_sample_length()
    def get_used_by(self):
        return None

class Song(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = FileRef.SONG

    def get_size(self):
        raise NotImplementedError()
    
    def get_used_by(self):
        return None

class Storage:
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

class Memory(Storage):
    def __init__(self, name):
        Storage.__init__(self, name)

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
        return (
            (handlers.has_key(Program) and handlers[Program].get_no_items() > 0) or
            (handlers.has_key(Sample) and handlers[Sample].get_no_items() > 0) or
            (handlers.has_key(Multi) and handlers[Multi].get_no_items() > 0) )


    def get_children(self):
        if len(self.children) > 0:
            return self.children
        programs = []
        multis = []
        samples = []
        songs = []
        
        pnames = handlers[Program].get_names()
        if pnames is not None:
            programs = [Program(name) for name in pnames ]
        mnames = handlers[Multi].get_names()
        if mnames is not None:
            multis = [Multi(name) for name in mnames ]
        snames = handlers[Sample].get_names()
        if snames is not None:
            samples = [Sample(name) for name in snames ]
        
        self.children.extend(programs)
        self.children.extend(multis)
        self.children.extend(samples)
        self.children.extend(songs)
        
        return self.children
