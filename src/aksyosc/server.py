import asyncore, socket, time
from handler import SamplerCallbackManager
from aksy.device import Devices

class Envelope:
    def __init__(self, address, message):
        self.address = address
        self.message = message
    def get_message(self):
        return self.message
    def get_address(self):
        return self.address

class OSCServer(asyncore.dispatcher):
    def __init__(self, address, port, callbackManager):
        self._address = address
        self._port = port
        self._callbackMgr = callbackManager
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((address, port))
        self.response = None 
        print '%s started at %s\n\tLocal addr: %s\n' % (
           self.__class__.__name__, time.ctime(time.time()),
           address)

    def writeable(self):
        return self.response is not None

    def handle_write (self):
        if (self.writeable()):
            self.sendto(self.response.get_message(), 0, 
                self.response.get_address())
            self.response = None

    def handle_read(self):
        data, address = self.recvfrom(8192)
        self.response = Envelope(address, self._callbackMgr.handle(data))

    def handle_connect(self):
        pass

if __name__ == "__main__":
    z48 = Devices.get_instance('mock_z48', None)
    OSCServer('localhost', 8888,  SamplerCallbackManager(z48))
    asyncore.loop()

