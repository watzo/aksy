from aksyxusb import Z48Sampler
from sysex import Request, Reply 
import sysex
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
    >>> z.get_disklist() 
    [512, 1, 2, 0, 1, 'Z48 & MPC4K']
    >>> z._clear()

    # it now says done!
    >>> z.select_disk(512) 
    >>> z.set_curr_folder('') 
    >>> z.set_curr_folder('AUTOLOAD') 
    # should read approx. 99123 bytes
    >>> z.get('Ride 1.wav', '/home/walco/dev/aksy' ) 

    # the number can differ ofcourse...
    >>> z.get_no_subfolders() 
    21
    >>> #z.get_subfolder_names() 
    >>> z.close_usb()
    """

    def __init__(self):
        Z48Sampler.__init__(self)
        Z48.__dict__.update(disktools.__dict__)
        self.commands = {}
        self.register_disktools()

    def init(self):
        """Initializes the connection with the sampler
        """
        Z48Sampler.init_usb(self)

    def reset(self):
        """Initializes the connection with the sampler
        """
        result_bytes = self._execute('\x30')
        print 'bytes: %s' % result_bytes

    def close(self):
        """Closes the connection with the sampler
        """
        Z48Sampler.close_usb(self)

    def get(self, filename, destpath):
        # fix this call
        Z48Sampler._get(self, sysex._to_byte_string(sysex.STRING, filename), destpath + '/' + filename)
    def execute(self, command, args):
        request = Request(command, args)
        sys.stderr.writelines("Request: %s\n" % repr(request))
        
        result_bytes = self._execute('\x10' + struct.pack('b', len(request.get_bytes())) + '\x00' + request.get_bytes())
        sys.stderr.writelines("Length of reply: %i\n" % len(result_bytes))
        result = Reply(result_bytes, command.reply_spec)
        sys.stderr.writelines("Reply: %s\n" % repr(result))
        return result.parse()

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
