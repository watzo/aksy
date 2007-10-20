from aksyosc.osc import CallbackManager, decodeOSC, OSCMessage
from aksy.devices.akai.base import SamplerException
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

    def dispatch(self, message):
        """
            Overrides base class method.
        """
 
        address = message[0]
        section, cmd_name = self.parse_cmd_name(address)
        LOG.debug('dispatch(%s %s)' % (section, cmd_name))
        
        # skip address, typetag
        try:
            result = self.sampler.execute_by_cmd_name(section, cmd_name, message[2:])
        except AttributeError, e:
            raise DispatchException(e)
        except Exception, e:
            return create_error_msg('Execution failed', e)

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
    msg.setAddress('/sampler/error')
    msg.append(text)
    msg.append(str(exception))
    return msg.getBinary()
