from aksyosc.osc import CallbackManager, decodeOSC, OSCMessage

from aksy.concurrent import transaction

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
        right address, and returns the result"""
        decoded = decodeOSC(data)
        return self.dispatch(decoded)

    @transaction()
    def dispatch(self, message):
        """
            Overrides base class method to return the result of the dispatch.
        """
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('dispatch(%s)', repr(message))

        address = message[0]
            
        # skip address, typetag
        try:
            if address == "#bundle":
                return self.dispatch_alt_request(message[2:])
            else:
                return self.dispatch_command(address, message)
        except AttributeError, e:
            LOG.exception("OSC message %s could not be dispatched", repr(message))
            return create_error_msg("Failed to execute command %s" % address, e)
        except Exception, e:
            LOG.exception("Dispatch of %s failed", repr(message))
            return create_error_msg('Execution failed', e)

    def parse_cmd_name(self, address):
        comps = address.split('/')
        if len(comps) != 3:
            raise DispatchException("Invalid address: '%s', should have two components" % address)
        return comps[1:3]
    
    def dispatch_command(self, address, message):
        section, cmd_name = self.parse_cmd_name(address)
        result = self.sampler.execute_by_cmd_name(section, cmd_name, message[2:])
        return create_response_msg(address, result)

    def dispatch_alt_request(self, messages):
        alt_request = messages.pop(0)
        alt_address = alt_request[0]

        handle = alt_request[2]
        index = alt_request[3]

        cmds = []
        args = []
        for msg in messages:
            address = msg[0]
            args.append(msg[2:])
            section, cmd_name = self.parse_cmd_name(address)
            cmds.append(self.sampler.get_cmd_by_name(section, cmd_name))

        result = self.sampler.execute_alt_request(handle, cmds, args, index)
        return create_response_msg(alt_address, result)
        
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
