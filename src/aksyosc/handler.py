from aksyosc.osc import CallbackManager, decodeOSC, OSCMessage
from aksy.devices.akai.base import SamplerException
import logging

LOG = logging.getLogger('aksy.osc')

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
        if address == "#bundle":
            return self.dispatch_alt_request(message[2:])
            
        section, cmd_name = self.parse_cmd_name(address)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('dispatch(%s %s)', section, cmd_name)
        
        # skip address, typetag
        try:
            result = self.sampler.execute_by_cmd_name(section, cmd_name, message[2:])
            return create_response_msg(address, result)
        except AttributeError, e:
            raise DispatchException(e)
        except Exception, e:
            return create_error_msg('Execution failed', e)

    def parse_cmd_name(self, address):
        comps = address.split('/')
        if len(comps) != 3:
            raise DispatchException("Invalid address: '%s', should have two components" % address)
        return comps[1:3]
    
    def dispatch_alt_request(self, messages):
        LOG.debug("dispatch_alt_request(%s)", repr(messages))
        alt_request = messages.pop(0)
        alt_address = alt_request[0]

        try:
            handle = alt_request[2]
            index = alt_request[3]
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.debug('dispatch_alt_request for handle, index(%s, %s)', handle, index)
            cmds = []
            args = []
            for msg in messages:
                address = msg[0]
                args.append(msg[2:])
                section, cmd_name = self.parse_cmd_name(address)
                cmds.append(self.sampler.get_cmd_by_name(section, cmd_name))
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.debug('adding cmd to dispatch: %s %s', section, cmd_name)
            # skip address, typetag
            result = self.sampler.execute_alt_request(handle, cmds, args, index)
            return create_response_msg(alt_address, result)
        except AttributeError, e:
            raise DispatchException(e)
        except Exception, e:
            return create_error_msg('Alternative Request execution failed', e)
        
def create_response_msg(address, result):
    msg = OSCMessage()
    msg.setAddress(address)
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
