from aksy.devices.akai import sysex

from aksyx import AkaiSampler

import logging

LOG = logging.getLogger("aksy.devices.akai.connector")

class USBConnector(AkaiSampler):
    """ USB Connector for Akai Samplers.
    """
    def __init__(self, device_id):
        AkaiSampler.__init__(self, getattr(USBConnector, device_id.upper()))
        
        #self.sysextools.enable_msg_notification(False)
        #self.sysextools.enable_item_sync(False)

    def execute(self, command, args):
        request = sysex.Request(command, args)
        result_bytes = self.execute_request(request)
        result = sysex.Reply(result_bytes, request.command)
        return result.get_return_value()

    def execute_alt_request(self, handle, commands, args, index = None):
        result_bytes = self.execute_request(sysex.AlternativeRequest(handle, commands, args, index))
        result = sysex.Reply(result_bytes, commands[0], True)
        return result.get_return_value()

    def execute_request(self, request):
        """Execute a request on the sampler.
        Returns the byte response.
        """
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("Request: %s", repr(request))

        result_bytes = self._execute(request.get_bytes())
        
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("Response: %s", (sysex.byte_repr(result_bytes)))
        return result_bytes
