#!/usr/bin/python
import asyncore, socket, time

from aksyosc.handler import SamplerCallbackManager
from aksyosc.oscoptions import create_option_parser

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
        print '%s started at addr: %s:%i\n' % (
           self.__class__.__name__, address, port)

    def handle_connect(self):
        pass
        
    def writable(self):
        return self.response is not None

    def handle_write(self):
        self.sendto(self.response.get_message(), 0, self.response.get_address())
        self.response = None

    def handle_read(self):
        data, address = self.recvfrom(8192)
        resp_data = self._callbackMgr.handle(data)
        self.response = Envelope(address, resp_data)
    
if __name__ == "__main__":
    parser = create_option_parser()
    options = parser.parse_args()[0]
    from aksy.device import Devices
    z48 = Devices.get_instance('mock_z48', None)
    server = OSCServer(options.address, options.port,  SamplerCallbackManager(z48))
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        asyncore.close_all()
