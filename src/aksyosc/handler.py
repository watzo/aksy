from aksyosc.osc import CallbackManager
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
            CallbackManager.handle(self, data, source)
        except DispatchException, e:
            LOG.error("Failed to execute command ", e)

    """
        Override base class method.
    """
    def dispatch(self, message):
        address = message[0]
        section, cmd_name = self.parse_cmd_name(address)
        # skip address, typetag
        self.sampler.execute_by_cmd_name(section, cmd_name, message[2:])

    def parse_cmd_name(self, address):
        comps = address.split('/')
        if len(comps) != 3:
            raise DispatchException("Unknown address: %s, should have two components", address)
        return comps[1:3]
        
