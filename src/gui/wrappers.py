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

class Folder(object):
    def __init__(self, disktools, path):
        """ TODO: find a nice solution for the primitive folder selection
        """
        self.disktools = disktools
        self.path = path

        print "Initializing folder %s" % repr(path)
        self.set_current()

    def get_children(self):
        """
        """
        children = []
        for subfolder in self.disktools.get_subfolder_names():
            children.append(Folder(self.disktools, self.path + [subfolder]))

        # TODO: check this! this currently does not work
        # Should stay a 'string item' unless loaded
        files = [ File(self.disktools, name) for name in 
            self.disktools.get_filenames() ]

        children.extend(files)
        return children

    def set_current(self):
        for item in self.path:
            self.disktools.set_curr_folder(item)

class File(object):

    def __init__(self, module, name=None):
        """Initializes a file object - should not be called directly, use 
        getInstance instead.
        """
        self.module = module
        self.name = name

    def getInstance(module, name=None):
        """Initializes a program from a  name
        """
        if RE_MULTI.search(name) is not None:
            return Multi(module, name)
        elif RE_PROGRAM.search(name) is not None:
            return Program(module, name)
        elif RE_SAMPLE.search(name) is not None:
            return Sample(module, name)
        else:
            raise NotImplementedError("No support for file type: ", name) 

    def get_modified(self):
        """Returns True if this program has has been modified
        """

    def get_used_by(self):
        """Returns the parent using this file
        """

    def get_children(self):
        """
        """
        raise NotImplementedError

    def get_children(self):
        """
        """
        raise NotImplementedError

    def delete(self):
        """
        """
        raise NotImplementedError

    def rename(self, new_name):
        """
        """
        raise NotImplementedError

    def get_actions(self):
        """Returns the actions defined by this file type
        """
        raise NotImplementedError

    def get_list_repr(self):
        """Returns a representation of the file for display
        in a list
        """
        raise NotImplementedError


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
