#!/usr/bin/python

import socket
from aksyosc.osc import OSCMessage, decodeOSC
from oscoptions import create_option_parser

def snd_recv(cmd):
    m = OSCMessage()
    m.setAddress(cmd)
    s.sendall(m.getBinary())
    print decodeOSC(s.recv(8192))

def show_banner():
    print "Aksyosc\n * Enter an osc address at the prompt,\
 e.g. '/systemtools/get_sampler_name'\n * Use 'quit' to exit"

if __name__ == "__main__":
    parser = create_option_parser()
    options = parser.parse_args()[0]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((options.address, options.port))
    show_banner()
    try:
        while 1:
            cmd = raw_input("aksyosc> ")
            if not cmd:
                continue
            if cmd == 'quit':
                break
            snd_recv(cmd)
    finally:
        s.shutdown(1)
