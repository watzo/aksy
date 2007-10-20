from aksyosc.osc import OSCMessage, decodeOSC
import socket

class OSCConnector:
    """ Execute commands using OSC
    """
    def __init__(self, host, port, timeout=30.0):
    	socket.setdefaulttimeout(timeout)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((host, port,))

    def execute(self, command, args, request_id=0):
        m = OSCMessage()
        m.setAddress("/" + command.section + "/" + command.name)
        for arg in args:
            m.append(arg)
        self.socket.sendall(m.getBinary())

        data = self.socket.recv(8192)
        resp_msg = decodeOSC(data)
        if resp_msg[0] == '/sampler/error':
            raise Exception("Remote execution failed, Server cause: " + resp_msg[3])
        return resp_msg[2:]

    def close(self):
        self.socket.shutdown(1)
