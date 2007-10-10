from aksyosc.osc import OSCMessage, decodeOSC
import socket

class OSCConnector:
    """ Execute commands using OSC
    """
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((host, port,))

    def execute(self, command, args, request_id=0):
        m = OSCMessage()
        m.setAddress("/" + command.section + "/" + command.name)
        for arg in args:
            m.append(arg)
        self.socket.sendall(m.getBinary()) 
        return decodeOSC(self.socket.recv(8192))[2:]

    # TODO: delegate to AksyFS filehandler
    # or add osc api for get/put of files on same system
    def get(self, filename, destfile, source):
        raise NotImplementedError
    
    # TODO: delegate to AksyFS filehandler
    # or add osc api for get/put of files on same system
    def put(self, sourcepath, remote_name, destination):
        raise NotImplementedError
        
    def close(self):
        self.socket.shutdown(1)
