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
            return create_error_msg("Failed to execute command %s" %
decoded[0], e)

    """
        Override base class method.
    """
    def dispatch(self, message):
        address = message[0]
        section, cmd_name = self.parse_cmd_name(address)
        # skip address, typetag
        try:
            result = self.sampler.execute_by_cmd_name(section, cmd_name, message[2:])
        except AttributeError, e:
            raise DispatchException(e)

        if result is None:
            return None

        return create_response_msg(result)

    def parse_cmd_name(self, address):
        comps = address.split('/')
        if len(comps) != 3:
            raise DispatchException("Invalid address: '%s', should have two components" % address)
        return comps[1:3]
        
def create_response_msg(result):
    msg = OSCMessage()
    if not hasattr(result, '__iter__'):
        result = [result]

    for arg in result:
        msg.append(arg) 
    return msg.getBinary()

def create_error_msg(text, exception):
    msg = OSCMessage()
    msg.append(text)
    msg.append("Cause: " + str(exception))
    return msg.getBinary()
