from aksyxusb import Z48Sampler
from sysex import Request, Reply 
import disktools
import struct
import sys

class Z48(Z48Sampler):
    """Models a Z4 or Z8 sampler.

    You can use it like this:
    >>> z = Z48()
    >>> z.init_usb()
    >>> z.get_no_disks()
    1
    >>> z.close_usb()
    """

    def __init__(self):
        Z48Sampler.__init__(self)
        Z48.__dict__.update(disktools.__dict__)

    """
    def __new__(cls):
        print cls.__name__
        if not Z48.__dict__.has_key(cls.__name__):
           Z48.__dict[cls.__name__] =  Z48Sampler.__new__(cls)

        return Z48.__dict__.get(cls.__name__) 

    """
    def execute(self, command):
        request = Request(command)
        print request.get_bytes()
        result_bytes = self._execute('\x10\x08\x00' + request.get_bytes())
        print "Python: len: %i data: %s" %(len(result_bytes), repr(struct.unpack(str(len(result_bytes)) + 'b', result_bytes)))
        result = Reply(result_bytes)
        return result.parse()
