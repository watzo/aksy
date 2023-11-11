#!/usr/bin/python
#
# Open SoundControl for Python
# Copyright (C) 2002 Daniel Holth, Clinton McChesney
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact 
# Daniel Holth <dholth@stetson.edu> or visit
# http://www.stetson.edu/~ProctoLogic/
#
# Changelog:
# 15 Nov. 2001:
#   Removed dependency on Python 2.0 features.
#   - dwh
# 13 Feb. 2002:
#   Added a generic callback handler.
#   - dwh

# 31 Oct. 2007:
#   * Added support for optional OSC types (True, False, Nil, Arrays).
#     (For tests, see tests/test_osc.py)
#   * Throw exceptions for various error cases.
#   * Remove unused code

import struct
import math
import sys
import types


def hexDump(bytes):
    """Useful utility; prints the string in hexadecimal"""
    for i in range(len(bytes)):
        sys.stdout.write("%2x " % (ord(bytes[i])))
        if (i+1) % 8 == 0:
            print(repr(bytes[i-7:i+1]))

    if(len(bytes) % 8 != 0):
        print("".rjust(11), repr(bytes[i-7:i+1]))

def string_encodeable(str):
    return str.find('\x00') == -1

class OSCMessage:
    """Builds typetagged OSC messages."""
    def __init__(self):
        self.address  = ""
        self.typetags = ","
        self.message  = ""

    def setAddress(self, address):
        self.address = address

    def append(self, argument, typehint = None):
        """Appends data to the message,
        updating the typetags based on
        the argument's type.
        If the argument is a blob (counted string)
        pass in 'b' as typehint."""

        if typehint == 'b':
            binary = OSCBlob(argument)
        elif hasattr(argument, "__iter__"):
            binary = OSCArray(argument)
        else:
            binary = OSCArgument(argument)

        self.typetags = self.typetags + binary[0]
        self._rawAppend(binary[1])

    def _rawAppend(self, data):
        self.message = self.message + data

    def getBinary(self):
        """Returns the binary message (so far) with typetags."""
        address  = OSCArgument(self.address)[1]
        typetags = OSCArgument(self.typetags)[1]
        return address + typetags + self.message

    def __repr__(self):
        return self.getBinary()

def readString(data):
    length   = data.find("\0")
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    return (data[0:length], data[nextData:])

def readArrayStart(data):
    return ([], data)

def readBlob(data):
    length  = struct.unpack(">i", data[0:4])[0]    
    nextData = int(math.ceil((length) / 4.0) * 4) + 4   
    return (data[4:length+4], data[nextData:])


def readInt(data):
    if(len(data)<4):
        print("Error: too few bytes for int", data, len(data))
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest    = data[4:]
        
    return (integer, rest)

def readTrue(data):
    return (True, data)

def readFalse(data):
    return (False, data)

def readNil(data):
    return (None, data)

def readOSCTime(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer."""
    high, low = struct.unpack(">ll", data[0:8])
    big = (int(high) << 32) + low
    rest = data[8:]
    return (big, rest)

def readLong(data):
    assert len(data) >= 8
    long = struct.unpack(">q", data[0:8])[0]
    return (int, data[8:])

def readFloat(data):
    if(len(data)<4):
        print("Error: too few bytes for float", data, len(data))
        rest = data
        f = 0
    else:
        f = struct.unpack(">f", data[0:4])[0]
        rest  = data[4:]

    return (f, rest)

def OSCBlob(next):
    """Convert a string into an OSC Blob,
    returning a (typetag, data) tuple."""

    length = len(next)
    padded = math.ceil((len(next)) / 4.0) * 4
    binary = struct.pack(">i%ds" % (padded), length, next)
    return ('b', binary)

def OSCArray(args):
    typetags = ['[']
    arguments = []
    for arg in args:
        if isinstance(arg, tuple):
            a = OSCArray(arg)
        else:
            a = OSCArgument(arg)
        typetags.append(a[0])
        arguments.append(a[1])

    typetags.append(']')
    return ''.join(typetags), ''.join(arguments) 

def OSCArgument(next):
    """Convert some Python types to their
    OSC binary representations, returning a
    (typetag, data) tuple."""
    
    if next is None:
        binary = ""
        tag = "N"
    elif next is True:
        binary = ""
        tag = "T"
    elif next is False:
        binary = ""
        tag = "F"
    # TODO this should be simplified
    elif isinstance(next, bytes):
        if not string_encodeable(next):
            tag, binary = OSCBlob(next)
        else:         
            l = math.ceil((len(next)+1) / 4.0) * 4
            binary  = struct.pack(">%ds" % l, next)
            tag = "s"
    elif isinstance(next, float):
        binary  = struct.pack(">f", next)
        tag = "f"
    elif isinstance(next, int):
        binary  = struct.pack(">i", next)
        tag = "i"
    elif isinstance(next, int):
        binary  = struct.pack(">q", next)
        tag = "h"
    else:
        raise OSCException(repr(type(next)) + " not supported")
    return (tag, binary)

def parseArgs(args):
    """Given a list of strings, produces a list
    where those strings have been parsed (where
    possible) as floats or integers."""
    parsed = []
    for arg in args:
        arg = arg.strip()
        interpretation = None
        try:
            interpretation = float(arg)
            if arg.find(".") == -1:
                interpretation = int(interpretation)
        except:
            # Oh - it was a string.
            interpretation = arg
            pass
        parsed.append(interpretation)
    return parsed

class OSCException(Exception):
    pass

def decodeOSC(data):
    """Converts a typetagged OSC message to a Python list."""
    table = {"t":readOSCTime, "h":readLong, "i":readInt, "f":readFloat, "s":readString, "b":readBlob, "T":readTrue, "F":readFalse, "N": readNil, "[":readArrayStart}
    decoded = []
    stack = [decoded]
    address, rest = readString(data)
    typetags = ""

    if address == "#bundle":
        time, rest = readOSCTime(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest)>0:
            length, rest = readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest)>0:
        typetags, rest = readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if(typetags[0] == ','):
            for tag in typetags[1:]:
                if tag == ']': 
                    stack.pop()
                    continue

                value, rest = table[tag](rest)
                stack[-1].append(value)
                if tag == '[': 
                    stack.append(value)
        else:
            raise OSCException("Oops, typetag lacks the magic ,")

    if len(stack) != 1:
        raise OSCException("Unbalanced array tags in ", typetags)
    return decoded

class CallbackManager:
    """This utility class maps OSC addresses to callables.

    The CallbackManager calls its callbacks with a list
    of decoded OSC arguments, including the address and
    the typetags as the first two arguments."""

    def __init__(self):
        self.callbacks = {}
        self.add(self.unbundler, "#bundle")

    def handle(self, data, source = None):
        """Given OSC data, tries to call the callback with the
        right address."""
        decoded = decodeOSC(data)
        self.dispatch(decoded)

    def dispatch(self, message):
        """Sends decoded OSC data to an appropriate calback"""
        try:
            address = message[0]
            self.callbacks[address](message)
        except KeyError as e:
            # address not found
            print("Address ", address, " not found.")
        except None as e:
            print("Exception in", address, "callback :", e)
        
        return

    def add(self, callback, name):
        """Adds a callback to our set of callbacks,
        or removes the callback with name if callback
        is None."""
        if callback == None:
            del self.callbacks[name]
        else:
            self.callbacks[name] = callback

    def unbundler(self, messages):
        """Dispatch the messages in a decoded bundle."""
        # first two elements are #bundle and the time tag, rest are messages.
        for message in messages[2:]:
            self.dispatch(message)


if __name__ == "__main__":
    hexDump("Welcome to the OSC testing program.")
    print()
    message = OSCMessage()
    message.setAddress("/foo/play")
    message.append(44)
    message.append(11)
    message.append(4.5)
    message.append("the white cliffs of dover")
    hexDump(message.getBinary())

    print("Making and unmaking a message..")

    strings = OSCMessage()
    strings.append("Mary had a little lamb")
    strings.append("its fleece was white as snow")
    strings.append("and everywhere that Mary went,")
    strings.append("the lamb was sure to go.")
    strings.append(14.5)
    strings.append(14.5)
    strings.append(-400)

    raw  = strings.getBinary()

    hexDump(raw)
    
    print("Retrieving arguments...")
    data = raw
    for i in range(6):
        text, data = readString(data)
        print(text)

    number, data = readFloat(data)
    print(number)

    number, data = readFloat(data)
    print(number)

    number, data = readInt(data)
    print(number)

    hexDump(raw)
    print(decodeOSC(raw))
    print(decodeOSC(message.getBinary()))

    print("Testing Blob types.")
   
    blob = OSCMessage() 
    blob.append("", "b")
    blob.append("b", "b")
    blob.append("bl", "b")
    blob.append("blo", "b")
    blob.append("blob", "b")
    blob.append("blobs", "b")
    blob.append(42)

    hexDump(blob.getBinary())

    print(decodeOSC(blob.getBinary()))

    def printingCallback(stuff):
        sys.stdout.write("Got: ")
        for i in stuff:
            sys.stdout.write(str(i) + " ")
        sys.stdout.write("\n")

    print("Testing the callback manager.")
    
    c = CallbackManager()
    c.add(printingCallback, "/print")
    
    c.handle(message.getBinary())
    message.setAddress("/print")
    c.handle(message.getBinary())
    
    print1 = OSCMessage()
    print1.setAddress("/print")
    print1.append("Hey man, that's cool.")
    print1.append(42)
    print1.append(3.1415926)

    c.handle(print1.getBinary())

    bundle = OSCMessage()
    bundle.setAddress("")
    bundle.append("#bundle")
    bundle.append(0)
    bundle.append(0)
    bundle.append(print1.getBinary(), 'b')
    bundle.append(print1.getBinary(), 'b')

    bundlebinary = bundle.message

    print("sending a bundle to the callback manager")
    c.handle(bundlebinary)
