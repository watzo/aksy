import asynchat, asyncore, socket, time
import osc
from handler import SamplerCallbackManager

"""
OSCServer 
"""
class OSCChannel(asynchat.async_chat):
    COMMAND = 0
    DATA = 1

    def __init__(self, server, conn, addr):
        asynchat.async_chat.__init__(self, conn)
        self.__server = server
        self.__conn = conn
        self.__addr = addr
        self.__line = []
        self.__state = self.COMMAND
        self.__peer = conn.getpeername()
        print 'Peer:', repr(self.__peer)

class OSCServer(asyncore.dispatcher):
     def __init__(self, address, port, callbackManager):
        self._address = address
        self._port = port
        self._callbackMgr = callbackManager
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((address, port))
        print '%s started at %s\n\tLocal addr: %s\n' % (
            self.__class__.__name__, time.ctime(time.time()),
            address)

     def handle_write (self):
        pass

     def handle_read(self):
        data = self.recv(8192)
        self._callbackMgr.handle(data)

     def handle_connect(self):
        pass


if __name__ == "__main__":
    z48 = Devices.get_instance('z48', 'usb')
    OSCServer('localhost', 8888,  SamplerCallbackManager(z48))
    asyncore.loop()

