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
    >>> # z.get_disklist() 
    # [512, 1, 2, 256, 'Z48 & MPC4K']

    # it now says done!
    >>> z.select_disk(512) 
    >>> z.set_curr_folder('') 
    >>> z._execute('\x10\x0a\x00\xf0\x47\x5e\x20\x00\x00\x10\x20\x30\xf7')
    >>> z.get_no_subfolders() 
    >>> z.get_subfolder_names() 
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
