from aksyosc.osc import OSCMessage, decodeOSC
import socket

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
        return m.getBinary()
        
    def execute(self, command, args, request_id=0):
        b = OSCConnector.create_msg(command, args)
        return self._sendAndRcv(b)

    def _sendAndRcv(self, b):
        self.socket.sendall(b)

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
        for i in range(len(commands)+1):
            bundle.append(0)
   
        alt_req = OSCMessage()
        alt_req.setAddress('/altoperations')
        alt_req.append(handle)
        alt_req.append(index)
        bundle.append(alt_req.getBinary(), 'b')

        for cmd in commands:
            bundle.append(OSCConnector.create_msg(cmd, args), 'b')
        return bundle.message
    
    def execute_alt_request(self, handle, commands, args, index = None):
        b = OSCConnector.create_alt_req_msg(handle, commands, args, index)
        return self._sendAndRcv(b)
    
    def close(self):
        self.socket.shutdown(1)
