import sys, aksy
from aksy.devices import config
import imp

class Devices:
    """
    >>> Devices.get_instance('z48', 'usb')
    1
    >>> Devices.get_instance('mock_z48', None)
    """

    _devices = config.devices 
    def get_instance(name, type=None, *args, **kwargs):
        module_name, klass = Devices._devices[(name, type)]
        mod = __import__(module_name)
        components = module_name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        if not hasattr(mod, klass):
            raise Exception('Device %s not found' %name)
        return getattr(mod, klass)(*args, **kwargs)
    
    get_instance = staticmethod(get_instance)

class Device:
    """Defines a generic device.

    """

    def discover(self):
        """
        """

    def get_vendor_id(self):
        raise NotImplementedError

    def get_system_objects(self):
        """Returns the system objects contained by this device
        """
        raise NotImplementedError

    def init(self):
        """Initializes the device
        """
        raise NotImplementedError

    def close(self):
        """Closes the device
        """
        raise NotImplementedError

    def execute(self, command, args, device_id=None, extra_id=None):
        """Execute a command on the device
        """
        raise NotImplementedError

class Command:
    """Defines a command which can be executed on the device
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
