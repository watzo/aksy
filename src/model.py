import re

RE_MULTI = re.compile("\.[aA][kK][mM]$")
RE_PROGRAM = re.compile("\.[aA][kK][pP]$")
RE_SAMPLE = re.compile("\.[wW][aA][vV]$")

modules = {} 
def init_tools(tools):
    modules.update(tools)

"""
try:
    modules
except NameError:
    raise Exception("Model not initialized properly")
"""

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
    def __init__(self, function, display_name, external_id=None):
        self.execute = function 
        self.display_name = display_name
        # The function to be executed before the function
        self.prolog = None
        # The function to be executed after the function
        self.epilog = None
        self.id = None

class File(object):
    FOLDER = 1
    MULTI = 2
    PROGRAM = 3
    SAMPLE = 4
    SONG = 5

    def __init__(self, path):
        """Initializes a file object - A multi, program or sample before it
        is loaded into memory
        """

        assert isinstance(path, tuple) 

        self.path = path

        if RE_MULTI.search(self.get_name()) is not None:
            self.type = self.MULTI
        elif RE_PROGRAM.search(self.get_name()) is not None:
            self.type = self.PROGRAM
        elif RE_SAMPLE.search(self.get_name()) is not None:
            self.type = self.SAMPLE
        else:
            #raise NotImplementedError("No support for file type: ", self.get_name()) 
            self.type = self.SAMPLE

    def get_name(self):
        return self.path[-1]

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
        # new_parent = Folder(dest_path)
        # add item to dest_path
    
    def load(self):
        """Load the file into memory 
        """
        self.get_parent().set_current()
        modules['disktools'].load_file(self.get_name())
        # XXX: self.path should reflect memory location
        if self.type == self.MULTI:
            return Multi(self.path)
        if self.type == self.PROGRAM:
            return Program(self.path)
        if self.type == self.SAMPLE:
            return Sample(self.path)

    def transfer(self, path):
        """Transfer the file to host 
        """
        print "Transfer of file %s to %s" % (self.get_name(), repr(path))
        modules['disktools'].get(self.get_name(), path)

    def get_children(self):
        """
        """
        raise NotImplementedError

    def get_parent(self):
        return Folder(self.path[:-1])

    def delete(self):
        """
        """
        modules['disktools'].delete_file(self.path)

    def rename(self, new_name):
        """
        """
        self.get_parent().set_current()
        modules['disktools'].rename_file(new_name)
        self.path = self.path[:-1] + (new_name,)

    def get_actions(self):
        """Returns the actions defined by this file type
        """
        return File.actions

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """
        raise NotImplementedError

#TODO: how to do this within the class definition... consider static method
File.actions = {"load": Action(File.load, "Load"), "delete": Action(File.delete, "Delete"), "transfer": Action(File.transfer, "Transfer"),}

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
            for subfolder in modules['disktools'].get_subfolder_names()]

        files = [ File(self.path + (name,)) for name in 
            modules['disktools'].get_filenames() ]

        self.children.extend(files)
        return self.children

    def has_children(self):
        return (len(self.children) > 0 or modules['disktools'].get_no_files() > 0 or
            modules['disktools'].get_no_subfolders() > 0)
        
    def get_name(self):
        return self.path[-1]

    def set_current(self):
        print "Current folder before set_current: %s" % modules['disktools'].get_curr_path()
        for item in self.path:
            modules['disktools'].set_curr_folder(item)
        print "Current folder after set_current: %s" % modules['disktools'].get_curr_path()

    def copy(self, dest_path, recursive=True):
        """Copies a folder, default is including all its children
        """
        # copy the folder
        # copy the children to the new path

    def rename(self, new_name):
        self.get_parent().set_current()
        modules['disktools'].rename_subfolder(self.get_name(), new_name)
        self.path = self.path[:-1] + (new_name,)

    def load(self):
        """
        """
        self.get_parent().set_current()
        modules['disktools'].load_folder(self.get_name())
        return self

    def delete(self):
        """
        """
        self.get_parent().set_current()
        modules['disktools'].delete_subfolder(self.get_name())
        # could be optimized by using dicts instead of lists
        for item in self.get_parent().get_children():
            if item.get_name() == self.get_name():
               del item
               break

    def create_subfolder(self, name):
        """
        """
        self.get_parent().set_current()
        modules['disktools'].create_subfolder(name)
        self.children.append(Folder(self.path + (name,)))

    def transfer(self, path):
        """Transfer the folder to host 
        """
        print "Transfer of folder not supported yet"

Folder.actions = {}
Folder.actions.update(File.actions)
Folder.actions.update({"transfer": Action(Folder.transfer, "Transfer"),})

class InMemoryFile(File):
    def __init__(self, path, handle=None):
        File.__init__(self, path) 
        self.handle = handle

    def get_size(self):
        return 'Unknown'

    def get_used_by(self):
        return None

    def get_handle(self):
        """Returns the handle
        XXX: Should be set on init
        """
        return modules[self.type].get_handle_by_name(self.get_name())

    def set_current(self):
        modules[self.type].set_current_by_name(self.get_name())

    def delete(self):
        print "InMemoryFile.delete() %s" % repr(modules[self.type])
        modules[self.type].get_no_items()
        self.set_current()
        modules[self.type].delete_current()

    def save(self, overwrite, dependents=False):
        modules['disktools'].save_file(self.get_handle(), self.type, overwrite, dependents) 

    def tranfer(self, dest_path):
        pass

    def rename(self, new_name):
        pass

InMemoryFile.actions = {"delete": Action(InMemoryFile.delete, "Delete"),
"transfer":Action(InMemoryFile.transfer, "Transfer"),}

class Multi(InMemoryFile):
    def get_used_by(self):
        return None

    def get_children(self):
        """Returns the programs used by this multi
        """

    def get_actions(self):
        """Returns the actions defined by this file type
        """
        return ("delete", "rename", "transfer")

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """

#TODO: possible inheritance issues, any subclass implementation
#will not be used
Multi.actions = {}
Multi.actions.update(InMemoryFile.actions)

class Program(InMemoryFile):
    def get_used_by(self):
        """Returns the multi(s) using this program
        """

    def get_children(self):
        """Returns the samples used by this program
        """

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """

Program.actions = {}
Program.actions.update(InMemoryFile.actions)

class Sample(InMemoryFile):
    def get_used_by(self):
        """Returns the pogram(s) using this file
        """
        return None

    def get_children(self):
        """Returns the samples used by this program
        """
        return None

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """

Sample.actions = {}
Sample.actions.update(InMemoryFile.actions)

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

    def get_children(self):
        return self._children    

    def set_children(self, item_list):
        self._children = item_list

class Memory(Storage):
    def __init__(self, z48, name):
        Storage.__init__(self, name)
        self.z48 = z48

    def get_children(self):
        if len(self._children) > 0:
            return self._children
        else:
            programs = [Program(name) for name in modules['programtools'].get_names()]
            multi = [Multi(name) for name in modules['multitools'].get_names()]
            sample = [Sample(name) for name in modules['sampletools'].get_names()]
            self._children.extend(programs)
            self._children.extend(multi)
            self._children.extend(sample)
