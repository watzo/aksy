from aksyxusb import AkaiSampler
from aksy.devices.akai import sysex
from aksy.devices.akai.sysex import Request, Reply
import disktools, programtools, multitools, sampletools, systemtools, recordingtools
from aksy import model
import struct
import sys,time

class Sampler(AkaiSampler):
    """Models a Z4 or Z8 sampler.

    You can use it like this:
    >>> z = Sampler()
    >>> z.init()
    >>> z.disktools.get_disklist() 
    (512, 1, 2, 0, 1, 'Z48 & MPC4K')

    >>> z.select_disk(256) 
    >>> z.set_curr_folder('') 
    >>> # z.create_subfolder('AUTOLOAD') 
    >>> z.set_curr_folder('AUTOLOAD') 

    >>> # z.get('Ride 1.wav', '/home/walco/dev/aksy' ) 
    >>> # z.put('/home/walco/dev/aksy/Ride 1.wav', 'Ride 1 copy.wav')

    # the number can differ of course...
    >>> # z.get_no_subfolders() 
    21
    >>> # z.get_filenames() 

    >>> z.get_subfolder_names() 
    ()
    >>> z.close_usb()
    """
    MEMORY = 0
    DISK = 1

    def __init__(self, confirmation_msgs=False, debug=1, id=0):
        self.id = id
        self.debug = debug
        sys.stderr.writelines("Sampler: %s\n" %repr(self))
        self.disktools = disktools.Disktools(self)
        self.programtools = programtools.Programtools(self)
        self.sampletools = sampletools.Sampletools(self)
        self.multitools = multitools.Multitools(self)
        self.systemtools = systemtools.Systemtools(self)
        self.recordingtools = recordingtools.Recordingtools(self)
        # self.command_spec = CommandSpec('\x47\x5f\x00', CommandSpec.ID, CommandSpec.ARGS)
        model.register_handlers({model.Disk: self.disktools,
                        model.File: self.disktools,
                        model.Program: self.programtools,
                        model.Sample: self.sampletools,
                        model.Multi: self.multitools})

        self.disks = model.Storage('disk')
        self.memory = model.Memory('memory')
        AkaiSampler.__init__(self)

    def init(self):
        """Initializes the connection with the sampler
        """
        AkaiSampler.init_usb(self)

        # disable checksums (not enabled per default)
        # msg = "\xf0\x47\x5f\x00\x04\x00\xf7";
        # result_bytes = self._execute('\x10' + struct.pack('B', len(msg) + '\x00' + msg)
        # disable confirmation
        msg = "\xf0\x47\x5f\x00\x00\x01\x00\xf7";
        self._execute('\x10' + struct.pack('B', len(msg)) + '\x00' + msg)
        # disable sync
        # msg = "\xf0\x47\x5f\x00\x00\x03\x00\xf7";
        # result_bytes = self._execute('\x10' + struct.pack('B', len(msg)) + '\x00' + msg)
        # not fool proof for multiple disks
        #disk = model.Disk(self.disktools.get_disklist())
        #self.disktools.select_disk(disk.handle)
        #rootfolder = model.Folder(("",))
        #folders = rootfolder.get_children()
        #disks.set_children(folders)

    def close(self):
        """Closes the connection with the sampler
        """
        AkaiSampler.close_usb(self)

    def get(self, filename, destpath, source=MEMORY):
        """Gets a file from the sampler, overwriting it if it already exists.
        """
        if source == self.DISK:
            AkaiSampler._get(self, sysex.STRING.encode(filename), destpath)
        if source == self.MEMORY:
            print filename[:-4]
            if filename.lower().endswith('akp'):
                handle = self.programtools.get_handle_by_name(filename[:-4])
            elif filename.lower().endswith('wav'):
                handle = self.sampletools.get_handle_by_name(filename[:-4])
            elif filename.lower().endswith('akm'):
                handle = self.multitools.get_handle_by_name(filename[:-4])
            elif filename.lower().endswith('mid'):
                handle = self.songtools.get_handle_by_name(filename[:-4])
            else:
                raise Exception("%s has an unknown extension.", filename)
                
            AkaiSampler._get(self, sysex.DWORD.encode(handle), destpath)
        else:
            raise Exception("Unknown source: %s", source)

    def put(self, path, remote_name, destination=MEMORY):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        AkaiSampler._put(self, path, sysex.STRING.encode(remote_name), destination)

    def execute(self, command, args, userref=None):
        """Executes a command on the sampler
        TODO: calculate the deviceid byte together with the userref count
        """
        request = Request(command, args)
        if self.debug:
            sys.stderr.writelines("Request: %s\n" % repr(request))
        result_bytes = self._execute('\x10' + struct.pack('B', len(request.get_bytes())) + '\x00' + request.get_bytes())
        if self.debug:
            sys.stderr.writelines("Length of reply: %i\n" % len(result_bytes))
        result = Reply(result_bytes, command)
        if self.debug:
            sys.stderr.writelines("Reply: %s\n" % repr(result))
        return result.parse()

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
