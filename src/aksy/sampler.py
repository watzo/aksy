import sys, aksy
import imp

import aksy.mock_z48.sampler
import aksy.z48.sampler

class Sampler:
    """Defines a generic sampler.

    >>> z48 = Sampler.get_instance('z48')
    """
    def get_instance(sampler_name, *args, **kwargs):
        sampler_mod_name = 'sampler'
        file, path, desc = imp.find_module('aksy')
        if file is not None: file.close()
        file, path, desc = imp.find_module(sampler_name, sys.path.append(path))
        if file is not None: file.close()
        package = imp.load_module('aksy.' + sampler_name, file, path, desc)
        if file is not None: file.close()
        file, path, desc = imp.find_module(sampler_mod_name)
        sampler_module = imp.load_module('aksy' + '.' + sampler_name + '.' + sampler_mod_name, file, path, desc)
        if file is not None: file.close()

        return sampler_module.SamplerImpl(1)

    get_instance = staticmethod(get_instance)

    def __init__(self):
        raise NotImplementedError

    def init(self):
        """Initializes the connection with the sampler
        """
        raise NotImplementedError

    def close(self):
        """Closes the connection with the sampler
        """
        raise NotImplementedError

    def get(self, filename, destpath):
        """Gets a file from the sampler, overwriting it if it already exists.
        """
        raise NotImplementedError

    def put(self, path, remote_name):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        raise NotImplementedError

    def execute(self, command, args, sampler_id=None, extra_id=None):
        """Execute a command on the sampler
        """
        raise NotImplementedError

class Command:
    """Defines a command which can be executed on the sampler
    """

class Request:
    """Maps a command to a command sequence
    """

class Reply:
    """Maps the command reply sequence to aksy types
    """

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
