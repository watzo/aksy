"""aksy model

Offers a high level API, should eventually be abstracting the midi jargon of
different devices, but at the moment it is using Akai conventions

"""
import re, os.path, sys, logging

RE_MULTI = re.compile("\.[aA][kK][mM]$")
RE_PROGRAM = re.compile("\.[aA][kK][pP]$")
RE_SAMPLE = re.compile("\.[wW][aA][vV]$")

handlers = {} 
log = logging.getLogger("aksy")

def register_handlers(tools):
    """Initialize the handlers, keyed on class
    definitions.
    """
    handlers.update(tools)

class Disk(object):
    def __init__(self, (handle, disktype, fstype, disk_id, writable, name)):
        self.handle = handle
        self.disktype = disktype
        self.fstype = fstype
        self.disk_id = disk_id
        self.writable = writable
        self.name = name

    def get_name(self):
        return self.name

class Action:
    """Wraps an action for a file, adapting an interface action to
    a function call
    """ 
    def __init__(self, function_name, display_name, id=None):
        self.function_name = function_name
        self.display_name = display_name
        # The function to be executed before the function
        self.prolog = None
        # The function to be executed after the function
        self.epilog = None
        self.id = id

class File(object):
    FOLDER = 0
    MULTI = 1
    PROGRAM = 2
    SAMPLE = 3
    SONG = 4

    def __init__(self, path):
        """Initializes a file object - A multi, program or sample before it
        is loaded into memory
        """

        assert isinstance(path, tuple) 

        log.debug(repr(path))
        self.path = path

        if RE_MULTI.search(self.get_name()) is not None:
            self.type = self.MULTI
        elif RE_PROGRAM.search(self.get_name()) is not None:
            self.type = self.PROGRAM
        elif RE_SAMPLE.search(self.get_name()) is not None:
            self.type = self.SAMPLE
        else:
            #raise NotImplementedError("No support for file type: ", self.get_name()) 
            log.warn("No support for file type: ", self.get_name())
            self.type = self.SAMPLE

    def get_name(self):
        return self.path[-1]

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

    def transfer(self, path):
        """Transfer the file to host 
        """
        log.info("Transfer of file %s to %s" % (self.get_name(), repr(path)))
        # XXX: remove the reference to the sampler
        handlers[Disk].z48.get(self.get_name(), path)

    def get_children(self):
        """
        """
        raise NotImplementedError

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
        return File.actions

File.actions = [Action("load", "Load"), Action("delete", "Delete"), Action("transfer", "Transfer"),]

class Folder(File):
    def __init__(self, path):
        """ TODO: find a nice solution for the primitive folder selection
        """
        self.path = path
        self.type = File.FOLDER
        self.children = []

    def get_children(self):
        """Gets the children of this folder
        or returns a cached version when already retrieved.
        """
        self.set_current()
        if len(self.children) > 0:
            return self.children

        self.children = [Folder(self.path + (subfolder,))
            for subfolder in handlers[Disk].get_subfolder_names()]

        files = [ File(self.path + (name,)) for name in 
            handlers[Disk].get_filenames() ]

        self.children.extend(files)
        return self.children

    def has_children(self):
        return (len(self.children) > 0 or handlers[Disk].get_no_files() > 0 or
            handlers[Disk].get_no_subfolders() > 0)
        
    def get_name(self):
        return self.path[-1]

    def set_current(self):
        log.debug("Current folder before set_current: %s" % handlers[Disk].get_curr_path())
        for item in self.path:
            handlers[Disk].set_curr_folder(item)
        log.debug("Current folder after set_current: %s" % handlers[Disk].get_curr_path())

    def copy(self, dest_path, recursive=True):
        """Copies a folder, default is including all its children
        """
        # copy the folder
        # copy the children to the new path

    def rename(self, new_name):
        self.get_parent().set_current()
        handlers[Disk].rename_subfolder(self.get_name(), new_name)
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
        handlers[Disk].delete_subfolder(self.get_name())
        # could be optimized by using dicts instead of lists
        for item in self.get_parent().get_children():
            if item.get_name() == self.get_name():
               del item
               break

    def create_subfolder(self, name):
        """
        """
        self.get_parent().set_current()
        handlers[Disk].create_subfolder(name)
        folder = Folder(self.path + (name,))
        self.children.append(folder)
        return folder

    def append_child(self, item):
        """Adds a child item to this folder
        Returns the added item
        """
        self.set_current()
        handlers[Disk].save(item.get_handle(), item.type, True, False)
        item = File(self.path + (name,))
        self.children.append(item)
        return item

    def transfer(self, path):
        """Transfer the folder to host 
        """
        self.get_parent().set_current()
        path = os.path.join(path, self.get_name())
        log.info("Transfer to dir: %s" % repr(path))
        if not os.path.exists(path):
            os.makedirs(path)
            for item in self.get_children():
                log.debug("Transfer to dir: %s" % repr(path))
                item.transfer(os.path.join(path, item.get_name()))

class InMemoryFile(File):
    def get_instance(name):
        if self.type == File.MULTI:
            return Multi(name)
        elif self.type == File.PROGRAM:
            return Multi(name)
        elif self.type == File.SAMPLE:
            return Multi(name)
        elif self.type == File.SONG:
            return Song(name)
        else:
            log.debug("Unknown file type:", repr(name))
            return InMemoryFile(name)

    get_instance = staticmethod(get_instance)

    def __init__(self, name, handle=None):
        self.name = name
        self.handle = handle
        File.__init__(self, (name,))

    def get_size(self):
        return 'Unknown'

    def get_used_by(self):
        return None

    def get_name(self):
        return self.name
    
    def get_handle(self):
        """Returns the handle
        XXX: Should be set on init
        """
        self.set_current()
        return handlers[self.__class__].get_current_handle()
        # return handlers[self.__class__].get_handle_by_name(self.get_name())

    def set_current(self):
        handlers[self.__class__].set_current_by_name(self.get_name())

    def delete(self):
        log.info("InMemoryFile.delete() %s" % repr(self.get_name()))
        handlers[self.__class__].get_no_items()
        self.set_current()
        handlers[self.__class__].delete_current()

    def save(self, overwrite, children=False):
        handlers[Disk].save_file(self.get_handle(), self.type, overwrite, children) 

    def set_current(self):
        handlers[self.__class__].set_current_by_name(self.get_name())
    
    def transfer(self, dest_path):
        pass

    def rename(self, new_name):
        self.set_current()
        handlers[self.__class__].rename(new_name)
            
class Multi(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = File.MULTI

    def get_used_by(self):
        return None

    def get_children(self):
        """Returns the programs used by this multi
        """

class Program(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = File.PROGRAM

    def get_used_by(self):
        """Returns the multi(s) using this program
        """

    def get_children(self):
        """Returns the samples used by this program
        """

class Sample(InMemoryFile):
    def __init__(self, name):
        InMemoryFile.__init__(self, name)
        self.type = File.SAMPLE

    def get_size(self):
        self.handlers[Sample].get_sample_length()
    def get_used_by(self):
        """Returns the pogram(s) using this file
        """
        return None

    def get_children(self):
        """Returns the samples used by this program
        """
        return None

class Storage:
    def __init__(self, name):
        self.name = name
        self.path = name
        self.actions = None 
        self.type = File.FOLDER
        self._children = []
    
    def has_children(self):
        return (len(self._children) > 0)

    def get_name(self):
        return self.name

    def get_handle(self):
        return self.name

    def get_children(self):
        return self._children    

    def set_children(self, item_list):
        self._children = item_list

    def get_actions(self):
        # maybe implement an info action?
        return ()

class Memory(Storage):
    def __init__(self, name):
        Storage.__init__(self, name)

    def upload(self, path):
        if name == '':
            raise ValueError
        name = os.path.basename(path)
        self.handlers[Disk].z48.put(path, name)
        item = InMemoryFile.get_instance(name)
        self.append_child(item)

    def append_child(self, item):
        self.children.append(item)
        return item

    def has_children(self):
        if len(self._children) > 0:
            return True
        else:
            return (
                handlers[Program].get_no_items() > 0 or
                handlers[Sample].get_no_items() > 0 or
                handlers[Multi].get_no_items() > 0)

    def get_children(self):
        if len(self._children) > 0:
            return self._children
        else:
            pnames = handlers[Program].get_names()
            if not isinstance(pnames, tuple):
                pnames = (pnames,)
            programs = [Program(name) for name in pnames ]
            mnames = handlers[Multi].get_names()
            if not isinstance(mnames, tuple):
                mnames = (mnames,)
            multis = [Multi(name) for name in mnames ]
            snames = handlers[Sample].get_names()
            if not isinstance(snames, tuple):
                snames = (snames,)

            samples = [Sample(name) for name in snames ]
            self._children.extend(programs)
            self._children.extend(multis)
            self._children.extend(samples)
            return self._children
