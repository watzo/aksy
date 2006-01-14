import sys, aksy, logging, os.path
from aksy.devices.akai.sysex import Request, Reply
from aksy.devices.akai.z48.sampler import Z48
from aksy import model

log = logging.getLogger('aksy')
class MockZ48(Z48):
    def __init__(self, debug=1):
        self.setupTools()
        self.setupModel()

    def get(self, filename, destpath):
        if self.debug > 0:
            log.debug("Transferring file %s to host" % filename)

    def put(self, path, remote_name, destination=Z48.MEMORY):
        if self.debug > 0:
            log.debug("Transferring file %s to sampler" % path)

    def execute(self, command, args, request_id=0):
        # work with stored sessions later on
        log.debug("Executing command: %s " % command.name)
        request = Request(command, args)
        return None
