from aksyxusb import AkaiSampler
import aksyxusb

from aksy.devices.akai import sysex
from aksy.devices.akai.sysex import Request, Reply
from aksy import model
import struct
import os.path
import sys

class Sampler(AkaiSampler):
    """Models an Akai sampler.

    You can use it like this:
    >>> z = Sampler(0x5f)
    >>> z.disktools.get_disklist()
    (512, 1, 2, 0, 1, 'Z48 & MPC4K')

    >>> z.disktools.select_disk(256)
    >>> z.disktools.set_curr_folder('')
    >>> # z.create_subfolder('AUTOLOAD')
    >>> z.disktools.set_curr_folder('AUTOLOAD')

    >>> # z.get('Ride 1.wav', '/home/walco/dev/aksy' )
    >>> # z.put('/home/walco/dev/aksy/Ride 1.wav', 'Ride 1 copy.wav')

    # the number can differ of course...
    >>> # z.disktools.get_no_subfolders()
    21
    >>> # z.disktools.get_filenames()

    >>> z.disktools.get_subfolder_names()
    ()
    """
    def __init__(self, usb_product_id, debug=1):
        self.debug = debug
        AkaiSampler.__init__(self, usb_product_id)
        # not fool proof for multiple disks
        #disk = model.Disk(self.disktools.get_disklist())
        #self.disktools.select_disk(disk.handle)
        #rootfolder = model.Folder(("",))
        #folders = rootfolder.get_children()
        #disks.set_children(folders)
        # XXX: move to seperate S56k Sampler class
        if self.sysex_id == 0x5e:
            from s56k import sysextools, disktools
            # programtools, multitools, sampletools, systemtools, recordingtools
        elif self.sysex_id == 0x5f:
            from aksy.devices.akai.z48 import sysextools, disktools, programtools, multitools, sampletools, systemtools, recordingtools

        self.disktools = disktools.Disktools(self)
        self.programtools = programtools.Programtools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.multitools = multitools.Multitools(self)
        self.systemtools = systemtools.Systemtools(self)
        self.sysextools = sysextools.Sysextools(self)
        self.recordingtools = recordingtools.Recordingtools(self)

        model.register_handlers({model.Disk: self.disktools,
                        model.File: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools})

        self.disks = model.Storage('disk')
        self.memory = model.Memory('memory')

        try:
            # this command sometimes doesn't yield a response
            self.sysextools.enable_msg_notification(False)
        except Exception, e:
            print e
        self.sysextools.enable_item_sync(False)

    def get(self, filename, destfile=None, source=aksyxusb.MEMORY):
        """Gets a file from the sampler, overwriting destfile if it already exists.
        """
        if destfile is None:
            destfile = filename

        self._get(filename, destfile, source)

    def put(self, sourcepath, remote_name=None, destination=aksyxusb.MEMORY):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        if remote_name is None:
            remote_name = os.path.basename(sourcepath)

        self._put(sourcepath, remote_name, destination)

    def execute(self, command, args, request_id=0):
        """Executes a command on the sampler
        """
        request = Request(command, args, request_id)
        if self.debug:
            sys.stderr.writelines("Request: %s, id %i\n" % (repr(request), request_id))
        result_bytes = self._execute('\x10' + struct.pack('B', len(request.get_bytes())) + '\x00' + request.get_bytes())
        if self.debug:
            sys.stderr.writelines("Reply %s\n" % sysex.byte_repr(result_bytes))
        result = Reply(result_bytes, command)
        return result.get_return_value()

if __name__ == "__main__":
    import doctest
    doctest.testmod(sys.modules[__name__])