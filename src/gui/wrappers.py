import re

RE_MULTI = re.compile("\.[aA][kK][mM]$")
RE_PROGRAM = re.compile("\.[aA][kK][pP]$")
RE_SAMPLE = re.compile("\.[wW][aA][vV]$")

    # TODO: move these objects to their respective 
    # modules once the generated classes become
    # stable; the passing in of section refs can
    # then be removed.
class Disk(object):
    def __init__(self, (handle, disktype, fstype, disk_id, writable, name)):
        self.handle = handle
        self.disktype = disktype
        self.fstype = fstype
        self.disk_id = disk_id
        self.writable = writable
        self.name = name

class Action:
    """Wraps an action for a file, adapting an interface action to
    a function call
    """ 
    def __init__(self, function, display_name, external_id=None):
        self.execute = function 
        self.display_name = display_name
        self.external_id = external_id

    def set_external_id(self, external_id):
        self.external_id = external_id

class Folder(object):
    def __init__(self, disktools, path):
        """ TODO: find a nice solution for the primitive folder selection
        Consider extending File
        """
        self.disktools = disktools
        self.path = path
        self.name = path[-1]

        print "Initializing folder %s" % repr(path)

    def get_children(self):
        """
        """
        self.set_current()
        children = [Folder(self.disktools, self.path + [subfolder])
            for subfolder in self.disktools.get_subfolder_names()]

        # TODO: check this! this currently does not work
        files = [ File(self.disktools, name) for name in 
            self.disktools.get_filenames() ]

        children.extend(files)
        return children

    def set_current(self):
        for item in self.path:
            self.disktools.set_curr_folder(item)

    def load(self):
        """
        """

    def delete(self):
        """
        """

    def create_subfolder(self):
        """
        """

Folder.actions = {"folder_load": Action(Folder.load, "Load"),
        "folder_delete": Action(Folder.delete, "Delete"), "folder_rename": Action(Folder.rename, "Rename")}

class File(object):
    MULTI = 0
    PROGRAM = 1
    SAMPLE = 2

    def __init__(self, disktools, path):
        """Initializes a file object - A multi, program or sample before it
        is loaded into memory
        """
        self.disktools = disktools
        self.path = path
        self.name = path[-1]
        if RE_MULTI.search(name) is not None:
            self.type = self.MULTI
            # self.module = multi_main
        elif RE_PROGRAM.search(name) is not None:
            self.type = self.PROGRAM
            # self.module = program_main
        elif RE_SAMPLE.search(name) is not None:
            self.type = self.SAMPLE
            # self.module = sample_main
        else:
            raise NotImplementedError("No support for file type: ", name) 

    def get_modified(self):
        """Returns True if this program has has been modified
        """

    def get_used_by(self):
        """Returns the parent using this file
        """

    def load(self):
        """Load the file into memory 
        """
        parent_folder = Folder(self.disktools, self.path[:-1])
        parent_folder.set_current()
        self.disktools.load_file(self.name)

        if self.type == self.MULTI:
            return Multi(self.module, self.name)
        if self.type == self.PROGRAM:
            return Program(self.module, self.name)
        if self.type == self.SAMPLE:
            return Sample(self.module, self.name)

    def get_children(self):
        """
        """
        raise NotImplementedError

    def delete(self):
        """
        """
        self.disktools.delete_file(self.path)

    def rename(self, new_name):
        """
        """
        self.disktools.rename_file(self.path, new_name)

    def get_actions(self):
        """Returns the actions defined by this file type
        """
        return File.actions

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """
        raise NotImplementedError

#TODO: how to do this within the class definition...
File.actions = {"load": Action(File.load, "Load"),
        "delete": Action(File.delete, "Delete"), "rename": Action(File.rename, "Rename")}


class Multi(File):
    def __init__(self, multi_main, name=None):
        """
        """
        
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
Multi.actions.update(File.actions)

class Program(File):
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
Program.actions.update(File.actions)

class Sample(File):
    def get_used_by(self):
        """Returns the pogram(s) using this file
        """

    def get_children(self):
        """Returns the samples used by this program
        """
        return None

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """

Sample.actions = {}
Sample.actions.update(File.actions)
