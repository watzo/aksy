from aksyxusb import Z48Sampler
from aksy.devices.z48.sampler import Sampler as Z48
import sys,time, aksy

class Sampler:
    MEMORY = 1
    """
    >>> z = MockZ48()
    >>> z.init()
    """
    def __init__(self, debug=0):
        #Z48.__init__(self)
        print "INIT MOCK"
        self.debug = debug
        self.disks = aksy.model.Storage('disks') 
        self.memory = aksy.model.Memory('mem')
        self.disktools = aksy.devices.z48.disktools.Disktools(self) 
        self.programtools = aksy.devices.z48.program_main.ProgramMain(self) 
        self.sampletools = aksy.devices.z48.sample_main.SampleMain(self) 
        self.multitools = aksy.devices.z48.multi_main.MultiMain(self) 
        model.register_handlers({model.Disk: self.disktools,
              model.File: self.disktools,
              model.Program: self.programtools,
              model.Sample: self.sampletools,
              model.Multi: self.multitools})


    def init(self):
        if self.debug > 0:
            print "Init sampler"

    def get(self, filename, destpath):
        if self.debug > 0:
            print "Transferring file %s to host" % filename

    def put(self, path, remote_name, destination=MEMORY):
        if self.debug > 0:
            print "Transferring file %s to sampler" % path
        
    def execute(self, command, args, z48id=None, userref=None):
        if self.debug > 0:
            print "Executing command: %s " % command.name
        if len(command.reply_spec) > 0:
            return (1,)  
        else:
            return None

    def close(self):
        if self.debug > 0:
            print "Close sampler"

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
