#!/usr/bin/python

import asyncore, socket
from aksyosc.osc import OSCMessage

class OSCClient(asyncore.dispatcher):
    def __init__(self, host, port, message):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect( (host, port) )
        self.message = message 

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print self.recv(8192)

    def writable(self):
        return (len(self.message) > 0)

    def handle_write(self):
        self.send(self.message)
        self.message = ''

if __name__ == "__main__":
    m = OSCMessage()
    m.setAddress("/systemtools/get_sampler_name")
    c = OSCClient('localhost', 8888, m.getBinary())

    asyncore.loop()
