import struct
import binascii

class Command:
    """ 
        Represents a system exclusive command.

    """

    def __init__(self, section_id, id, name, arg_types,args):
        self.section_id = section_id
        self.id = id
        self.name = name
        self.arg_types = ()

        for arg_type in arg_types:
            if arg_type is not None:
                self.arg_types.append(arg_type)

        assert (len(self.arg_types) == len(args)) 

        self._bytes = []

        for type,arg in zip(arg_types, args):
            self._bytes.append(_to_byte_string(type, arg))

    def get_data_bytes(self):
        """ Returns the sysex byte sequence for this command -
            section, command items and data
        """
        if len(self._bytes) == 0:
            return None
        else:
            return self._bytes

class Request:
    def __init__(self, command):
        bytes = ['\xf0']
        bytes.extend(SYSEX_HEADER) 
        print command.section_id
        bytes.append(command.section_id) 
        bytes.append(command.id) 
        data = command.get_data_bytes()
        if data is not None:
            bytes.extend(data)
        bytes.append('\xf7')

        print "REQ BYTES:>%s<" % repr(bytes)
        self._bytes = ''.join(bytes)

    def get_bytes(self):
        return self._bytes;
        
class Reply:
    def __init__(self, bytes):
        self.bytes = bytes

    def parse(self):
        """ Parses the command sequence
        """

        if int(self.bytes[0:1],16) != START_SYSEX or int(self.bytes[-2:-1],16) != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")

        bytes = self.bytes[2:-2] # get rid of start and end byte
        result = []
        i = 4 # skip vendor id, z8 id, device id, userref (TODO:consider the user ref)
        reply_id = int(bytes[i:i+1],16)
        if reply_id == REPLY_ID_OK:
            return []
        elif reply_id == REPLY_ID_DONE:
            return []
        elif reply_id == REPLY_ID_ERROR:
            raise Exception("System exclusive error, code %i" %(int(bytes[i],16) + 128* int(bytes[i+1],16)))
        else:
            raise ParseException("Unknown reply type: %i" % reply_id)

        i +=  4 # skip the section and command (TODO: reconsider)
        while i < (len(bytes)):
            part,len_parsed = parse_byte_string(bytes, i)
            result.append(part)
            i += len_parsed

        return result

class ParseException(Exception):
    """ Exception raised when parsing system exclusive fails
    """
    pass

class Error(Exception):
    """ Exception raised when system exclusive fails
    """
    pass

# Module vars and methods

BYTE        = 0x01;
SBYTE       = 0x02;
WORD        = 0x03; # 2 BYTES
SWORD       = 0x04;
DWORD       = 0x05;
SDWORD      = 0x06;
QWORD       = 0x07; # 2 x 4 BYTES
SQWORD      = 0x08;
STRING      = 0x09;
TWO_BYTES   = 0x10;
THREE_BYTES = 0x11;
CUSTOM      = 0x20;

STRING_TERMINATOR = '\x00'

REPLY_ID_OK = 0x4F
REPLY_ID_DONE = 0x44
REPLY_ID_REPLY = 0x52
REPLY_ID_ERROR = 0x55

START_SYSEX = 0xf0
SYSEX_HEADER = ('\x47','\x5f', '\x00') # TODO: Shouldn't have this hard coded
END_SYSEX = 0Xf7

def _to_byte_string(src_type, value):
    """
    """
    # TODO: raise valueerrors if value out of range 
    if (src_type == BYTE):
       byte_string = struct.pack('b', value)
    elif (src_type == SBYTE):
       byte_string = struct.pack('b', value)
    elif (src_type == WORD):
       byte_string = struct.pack('2b', (value[1],value[0])) # OR pack big endian?
    elif (src_type == STRING):
        if not type(value) == type(''):
            raise ValueError("Value %s should be a (non unicode) string." % (value))
        else:
            byte_string = [ binascii.unhexlify(_to_akai_char(char)) for char in value ]
            byte_string.append(STRING_TERMINATOR)
    else: 
        raise ValueError("unsupported type %s" % repr(src_type))

    """
    for byte in byte_string:
        assert(int(byte,16) < 0x7f)
    """
    
    return byte_string

def parse_byte_string(data, offset=0):
    """ Parses a bytestring

    >>> parse_byte_string((STRING,'1e','0f','1d','1e','0'))
    ('TEST', 5)

    >>> parse_byte_string((BYTE,'aa'))
    (170, 1)

    """

    dest_type = data[offset:offset+1]
    len_parsed_data = 0

    if (dest_type == BYTE):
        result = int(data[offset+2:offset+3],16)
        len_parsed_data += 2;
    elif (dest_type == SBYTE):
        result = int(data[offset+2:offset+4],16)
        len_parsed_data += 2;
    elif (dest_type == WORD):
        result = struct.unpack('2b', data[1])
        len_parsed_data += 2;
    elif (dest_type == STRING):
        bytes = []
        for char in data[1:]:
            len_parsed_data += 1;
            if char == STRING_TERMINATOR:
                break
            else:
                bytes.append(_convert_akai_char(char))
        result = ''.join(bytes)
    else: 
        raise ValueError("unsupported type %s" % repr(src_type))
        
    return (result, len_parsed_data)

def _to_akai_char(value):
    """ Converts a python char to an string encoded ordinal value
        TODO: Support for cursor values
    """
    return hex(ord(value))[2:]

def _convert_akai_char(value):
    """ Converts an akai string encoded ascii value to a python string
    """
    value = int(value)
    return str(chr(value))


if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
