from aksyosc.osc import CallbackManager, decodeOSC, OSCMessage
import logging

LOG = logging.getLogger('aksyosc')

class DispatchException(Exception):
    pass

class SamplerCallbackManager(CallbackManager):
    def __init__(self, sampler):
        CallbackManager.__init__(self)
        self.sampler = sampler

    def handle(self, data, source = None):
        """Given OSC data, tries to call the callback with the
        right address."""
        try:
            decoded = decodeOSC(data)
            return self.dispatch(decoded)
        except DispatchException, e:
            LOG.error("Failed to execute command ", e)

    """
        Override base class method.
    """
    def dispatch(self, message):
        address = message[0]
        section, cmd_name = self.parse_cmd_name(address)
        # skip address, typetag
        result = self.sampler.execute_by_cmd_name(section, cmd_name, message[2:])
        msg = OSCMessage()
        if not hasattr(result, '__iter__'):
            result = [result]

        for arg in result:
            msg.append(arg) 
        return msg.getBinary()

    def parse_cmd_name(self, address):
        comps = address.split('/')
        if len(comps) != 3:
            raise DispatchException("Unknown address: %s, should have two components", address)
        return comps[1:3]
        
