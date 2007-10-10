from aksy.devices.akai import sysex

from aksyx import AkaiSampler

import os.path, logging

log = logging.getLogger("aksy")

class USBConnector(AkaiSampler):
    """ USB Connector for Akai Samplers.
    """
    def __init__(self, usb_product_id=0, debug=False):
        AkaiSampler.__init__(self, usb_product_id)
        
        #self.sysextools.enable_msg_notification(False)
        #self.sysextools.enable_item_sync(False)

        self.debug = debug

    def get(self, filename, destfile=None, source=AkaiSampler.MEMORY):
        """Gets a file from the sampler, overwriting destfile if it already exists.
        """
        if destfile is None:
            destfile = filename

        self._get(filename, destfile, source)

    def put(self, sourcepath, remote_name=None, destination=AkaiSampler.MEMORY):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        if remote_name is None:
            remote_name = os.path.basename(sourcepath)

        self._put(sourcepath, remote_name, destination)

    def execute(self, command, args, request_id=0):
        request = sysex.Request(command, args, request_id)
        result_bytes = self.execute_request(request)
        result = sysex.Reply(result_bytes, request.command)
        return result.get_return_value()

    def execute_request(self, request):
        """Execute a request on the sampler.
        Returns the byte response.
        """
        if self.debug:
            log.debug("Request:  %s\n" % repr(request))
        return self._execute(request.get_bytes())
        
        if self.debug:
            log.debug("Response: %s\n" % (sysex.byte_repr(result_bytes)))
        return result_bytes