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
        bytes.append(command.section_id) 
        bytes.append(command.id) 
        data = command.get_data_bytes()
        if data is not None:
            bytes.extend(data)
        bytes.append('\xf7')

        self._bytes = ''.join(bytes)

    def get_bytes(self):
        return self._bytes;
        
class Reply:
    """ Encapsulates a sysex reply

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, USERREF, REPLY_ID_REPLY, '\x20','\x05', BYTE, '\x01', END_SYSEX)
    >>> reply = Reply(''.join(bytes)) 
    >>> reply.parse()
    1
    """
    def __init__(self, bytes):
        self.bytes = bytes

    def parse(self):
        """ Parses the command sequence
        """

        if self.bytes[0] != START_SYSEX or self.bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")

        result = []
        i = 4 # skip start, vendor id, z8 id, userref (TODO:consider the user ref)
        reply_id = self.bytes[i]
        if reply_id == REPLY_ID_OK:
            return []
        elif reply_id == REPLY_ID_DONE:
            return []
        elif reply_id == REPLY_ID_ERROR:
            raise Exception("System exclusive error, code %i" %(int(bytes[i],16) + 128* int(bytes[i+1],16)))
        elif reply_id == REPLY_ID_REPLY:
            # continue
            pass
        else:
            raise ParseException("Unknown reply type: %02x" % struct.unpack('b', reply_id))

        i +=  3 # skip the section and command (TODO: reconsider)
        while i < (len(self.bytes) - 1):
            part, len_parsed = parse_byte_string(self.bytes, i)
            result.append(part)
            i += len_parsed
        if len(result) == 1:
            return result[0]
        else:
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

INT         = '\x00'
BYTE        = '\x01'
SBYTE       = '\x02'
WORD        = '\x03' # 2 BYTES
SWORD       = '\x04'
DWORD       = '\x05'
SDWORD      = '\x06'
QWORD       = '\x07' # 2 x 4 BYTES
SQWORD      = '\x08'
STRING      = '\x09'
TWO_BYTES   = '\x10'
THREE_BYTES = '\x11'
CUSTOM      = '\x20'

POSTIVE     = '\x00'
NEGATIVE    = '\x01'

STRING_TERMINATOR = '\x00'

REPLY_ID_OK = '\x4f'
REPLY_ID_DONE = '\x44'
REPLY_ID_REPLY = '\x52'
REPLY_ID_ERROR = '\x55'

START_SYSEX = '\xf0'
AKAI_ID = '\x47'
Z48_ID = '\x5f'
USERREF = '\x00'
SYSEX_HEADER = (AKAI_ID, Z48_ID, USERREF ) # TODO: Shouldn't have this hard coded
END_SYSEX = '\xf7'

def _to_byte_string(src_type, value):
    """
    """
    # TODO: raise valueerrors if value out of range 
    if (src_type == BYTE or src_type == INT):
       byte_string = struct.pack('<b', value)
    elif (src_type == SBYTE):
       byte_string = struct.pack('<b', value)
    elif (src_type == WORD):
       byte_string = struct.pack('<2b', (value[1],value[0])) 
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

    >>> parse_byte_string((STRING, '\x54','\x45','\x53','\x54', STRING_TERMINATOR))
    ('TEST', 6)

    >>> parse_byte_string((BYTE + '\x0f'))
    (15, 2)


    >>> parse_byte_string((SBYTE + '\x01\x0f'))
    (-15, 3)

    >>> parse_byte_string((WORD + '\x0f\x0f'))
    (3855, 3)

    >>> parse_byte_string((SWORD + '\x01\x0f\x0f'))
    (-3855, 4)

    >>> parse_byte_string((DWORD + '\x00\x0f\x0f'))
    (3855, 4)

    >>> parse_byte_string((SDWORD + '\x01\x00\x0f\x0f'))
    (3855, 5)
    """

    dest_type = data[offset]
    len_parsed_data = 1 
    if (dest_type == BYTE or dest_type == INT):
        result = struct.unpack('b', data[offset+1])[0]
        len_parsed_data += 1

    elif (dest_type == SBYTE):
        result = struct.unpack('b', data[offset+2])[0]

        if data[offset+1] == NEGATIVE:
            result *= -1 
         
        len_parsed_data += 2;

    elif (dest_type == WORD):
        result = struct.unpack('<H', data[offset+1:offset+3])[0]
        len_parsed_data += 2;

    elif (dest_type == SWORD):
        result = struct.unpack('<H', data[offset+2:offset+4])[0]

        if data[offset+1] == NEGATIVE:
            result *= -1 

        len_parsed_data += 3;
    elif (dest_type == DWORD):
        result = struct.unpack('<I', data[offset+1:offset+5])[0]

        len_parsed_data += 3;
    elif (dest_type == SDWORD):
        result = struct.unpack('<I', data[offset+1:offset+5])[0]
        len_parsed_data += 5;

        result = struct.unpack('<I', data[offset+2:offset+4])[0]
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
        raise ValueError("unsupported type %s" % repr(dest_type))
        
    return (result, len_parsed_data)

def _to_akai_char(value):
    """ Converts a python char to an string encoded ordinal value
        TODO: Support for cursor values
    """
    return hex(ord(value))[2:]

def _convert_akai_char(value):
    """ Converts an akai string encoded ascii value to a python string

    >>> _convert_akai_char('\x3f')
    '?'
    """
    value = struct.unpack('b', value)[0]
    assert value > 0 and value < 256
    return str(chr(value))


if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
