from aksyx import Z48Sampler
from sysex import Request, Reply 
import disktools
import struct
import sys

class Z48(Z48Sampler,object):
    def __init__(self):
        Z48Sampler.__init__(self)
        Z48.__dict__.update(disktools.__dict__)

    def __new__(cls):
        print cls.__name__
        if not Z48.__dict__.has_key(cls.__name__):
           Z48.__dict[cls.__name__] =  Z48Sampler.__new__(cls)

        return Z48.__dict__.get(cls.__name__) 

    def execute(self, command):
        request = Request(command)
        print request.get_bytes()
        result_bytes = self._execute('\x10\x08\x00' + request.get_bytes())
        print "Python: %s " % result_bytes
        result = Reply(result_bytes)
        return result
