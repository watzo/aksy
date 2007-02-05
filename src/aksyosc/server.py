import asyncore, socket, time
from osc import OSCMessage
from handler import SamplerCallbackManager
from aksy.device import Devices

class OSCServer(asyncore.dispatcher):
    def __init__(self, address, port, callbackManager):
        self._address = address
        self._port = port
        self._callbackMgr = callbackManager
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((address, port))
        self.response = ''
        print '%s started at %s\n\tLocal addr: %s\n' % (
           self.__class__.__name__, time.ctime(time.time()),
           address)

    def writeable(self):
        return len(self.response) > 0

    def handle_write (self):
        if (self.writeable()):
            self.sendto(self.response, 0, self.address)
            self.response = ''

    def handle_read(self):
        data, self.address = self.recvfrom(8192)
        self.response = self._callbackMgr.handle(data)

    def handle_connect(self):
        pass

if __name__ == "__main__":
    z48 = Devices.get_instance('mock_z48', None)
    OSCServer('localhost', 8888,  SamplerCallbackManager(z48))
    asyncore.loop()

