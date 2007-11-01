from aksyosc.osc import OSCMessage, decodeOSC
import socket, logging

LOG = logging.getLogger("aksy.osc.connector")

class OSCConnector:
    """ Execute commands using OSC
    """
    def __init__(self, host, port, timeout=30.0):
        socket.setdefaulttimeout(timeout)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((host, port,))

    @staticmethod
    def create_msg(command, args):
        m = OSCMessage()
        m.setAddress("/" + command.section + "/" + command.name)
        for arg in args:
            m.append(arg)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("Created message: %s, args(%s)", decodeOSC(m.getBinary()), repr(args))
        return m.getBinary()
        
    def execute(self, command, args):
        b = OSCConnector.create_msg(command, args)
        resp = self._sendAndRcv(b)
        # HACK: mimic the behaviour of TypedComposite
        if len(resp) == 1 and command.reply_spec is None:
            return resp[0]
            
        return resp

    def _sendAndRcv(self, b):
        self.socket.sendall(b)
        # TODO: use "streaming" decoder to allocate buffer 
        data = self.socket.recv(8192)
        resp_msg = decodeOSC(data)
        if resp_msg[0] == '/sampler/error':
            raise Exception("Remote execution failed, Server cause: " + resp_msg[3])
        return resp_msg[2:]
    
    @staticmethod
    def create_alt_req_msg(handle, commands, args, index):
        bundle = OSCMessage()
        bundle.setAddress("")
        bundle.append('#bundle')
        bundle.append(0)
        bundle.append(0)
   
        alt_req = OSCMessage()
        alt_req.setAddress('/altoperations')
        alt_req.append(handle)
        alt_req.append(index)
        bundle.append(alt_req.getBinary(), 'b')

        args = list(args)
        
        for cmd in commands:
            if len(cmd.arg_types) > 0:
                arg = args.pop(0)
            else:
                arg = []
                
            bundle.append(OSCConnector.create_msg(cmd, arg), 'b')
        return bundle.message
    
    def execute_alt_request(self, handle, commands, args, index = None):
        b = OSCConnector.create_alt_req_msg(handle, commands, args, index)
        return self._sendAndRcv(b)
    
    def close(self):
        self.socket.shutdown(1)
