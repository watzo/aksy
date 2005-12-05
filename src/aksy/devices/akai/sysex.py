import struct, sys, types, sysex_types
from sysex_types import START_SYSEX, END_SYSEX
# Module vars

AKAI_ID = '\x47'
Z48_ID = '\x5f'
S56K_ID = '\x5e'

REPLY_ID_OK = '\x4f'
REPLY_ID_DONE = '\x44'
REPLY_ID_REPLY = '\x52'
REPLY_ID_ERROR = '\x45'

class Command:
    """Represents a system exclusive command.
    """
    def __init__(self, device_id, id, name, arg_types,
            reply_spec=(), userref_type=sysex_types.USERREF):
        self.device_id = device_id
        self.id = id
        self.name = name
        self.arg_types = []
        self.reply_spec = reply_spec
        self.userref_type = userref_type

        for arg_type in arg_types:

            if arg_type is not None:
                self.arg_types.append(arg_type)

    def create_arg_bytes(self, args):
        """Returns the sysex byte sequence for the command arg data -
        """
        bytes = []
        for type,arg in zip(self.arg_types, args):
            bytes.append(type.encode(arg))

        if len(bytes) == 0:
            return None
        else:
            return bytes

class Request:
    """ Encapsulates a sysex request
    command: the command to execute

    """
    def __init__(self, command, args, request_id=0):
        bytes = [START_SYSEX, AKAI_ID]

        bytes.append(command.device_id)
        bytes.append(command.userref_type.encode(request_id))
        bytes.append(command.id)
        data = command.create_arg_bytes(args)
        if data is not None:
            bytes.extend(data)
        bytes.append(END_SYSEX)

        self.bytes = ''.join(bytes)

    def get_bytes(self):
        return self.bytes;

    def __repr__(self):
        return repr([ "%02x" %byte for byte in struct.unpack(str(len(self.bytes)) + 'B', self.bytes)])

class Reply:
    """ Encapsulates a sysex reply
    """
    def __init__(self, bytes, command):
        self.bytes = bytes
        self.command = command
        self.request_id  = 0
        #self.return_value = self.parse()

    def get_request_id(self):
        return self.request_id

    def get_return_value(self):
        return self.return_value

    def parse(self):
        """ Parses the command sequence
        """

        if self.bytes[0] != START_SYSEX or self.bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")
        # TODO: dispatching on z48id, userref and command
        i = 2   # skip start sysex, vendor id
        i += len(self.command.device_id)
        len_userref, self.request_id = sysex_types.USERREF.decode(self.bytes[i])
        i += len_userref
        reply_id = self.bytes[i]
        i +=  1 # skip past the reply code
        command = self.bytes[i:i+2]
        i += 2 # skip past the command id (section, item)
        if reply_id == REPLY_ID_OK:
            return None
        elif reply_id == REPLY_ID_DONE:
            return None
        elif reply_id == REPLY_ID_ERROR:
            b1, b2 = struct.unpack('2B', self.bytes[i:i+2])
            code = (b2 << 7) + b1
            raise SamplerException(
                "code %02x (%s)" % (code, errors.get(code, "Unknown")))
        elif reply_id == REPLY_ID_REPLY:
            # continue
            pass
        else:
            raise ParseException("Unknown reply type: %02x" % struct.unpack('b', reply_id))

        if self.command.id[:2] != command:
            raise ParseException(
                'Parsing the wrong reply (%s) for command %02x %02x'
                    % (repr(self), struct.unpack('2B', self.command.id[:2])))
        if self.command.reply_spec is None:
            return parse_typed_bytes(self.bytes, i)
        else:
            return parse_untyped_bytes(self.bytes, self.command.reply_spec, i)

    def __repr__(self):
         return repr([ "%02x" %byte for byte in struct.unpack(str(len(self.bytes)) + 'B', self.bytes)])

def parse_typed_bytes(bytes, offset):
    result = []
    while offset < (len(bytes) - 1):
        type = sysex_types.get_type(bytes[offset])
        offset += 1
        part, len_parsed = parse_byte_string(bytes, type, offset)
        if part is not None:
            result.append(part)
        offset += len_parsed
    if len(result) == 1:
        return result[0]
    else:
        return tuple(result)

def parse_untyped_bytes(bytes, reply_spec, offset):
    """Parses a byte string without type information
    """
    result = []
    for type in reply_spec:
        part, len_parsed = parse_byte_string(bytes, type, offset)
        if part is not None:
            result.append(part)
        offset += len_parsed
    if len(result) == 1:
        return result[0]
    else:
        return tuple(result)


class ParseException(Exception):
    """ Exception raised when parsing system exclusive fails
    """
    pass

class SamplerException(Exception):
    """ Exception raised by the sampler
    """
    pass

class Error(Exception):
    """ Exception raised when system exclusive fails
    """
    pass

def parse_byte_string(data, type, offset=0):
    r""" Parses a byte string

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, STRING)
    ('TEST', 5)

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, STRING, 1)
    ('EST', 4)

    >>> parse_byte_string('\x54\x45\x53\x54\x00\x54\x45\x53\x54\x00', STRINGARRAY, 0)
    (('TEST', 'TEST'), 10)

    >>> parse_byte_string('\x0f', BYTE)
    (15, 1)

    >>> parse_byte_string('\x01\x0f', SBYTE)
    (-15, 2)

    >>> parse_byte_string('\x00\x03', WORD)
    (384, 2)

    >>> parse_byte_string('\x01\x0f\x0f', SWORD)
    (-1935, 3)

    >>> parse_byte_string('\x7f\x7f\x7f\x7f', DWORD)
    (268435455, 4)

    >>> parse_byte_string('\x01\x7f\x7f\x7f\x7f', SDWORD)
    (-268435455, 5)

    >>> parse_byte_string('\x00', BOOL)
    (False, 1)

    >>> parse_byte_string('\x01', BOOL)
    (True, 1)

    """

    len_parsed_data = 0
    if type.size is not None:
        result = type.decode(data[offset:offset+type.size])
        len_parsed_data = type.size
    else:
        # TODO: use a factory which returns instances with a size set ?
        len_parsed_data, result = type.decode(data[offset:])
        if len_parsed_data == 0:
            result = None

    return (result, len_parsed_data)

def _to_string(ordvalues):
    """Method to quickly scan a string
    >>> ordvalues = (90, 52, 56, 32, 38, 32, 77, 80, 67, 52, 75)
    >>> _to_string(ordvalues)
    'Z48 & MPC4K'
    """
    return ''.join([chr(value) for value in ordvalues])

errors = {
    0x00:"The <Section> <Item> supplied are not supported",
    0x01:"Checksum invalid",
    0x02:"Unknown error",
    0x03:"Invalid message format",
    0x04:"Parameter out of range",
    0x05:"Operation is pending",
    0x80:"Unknown system error",
    0x81:"Operation had no effect",
    0x82:"Fatal error",
    0x83:"CPU memory is full",
    0x84:"WAVE memory is full",
    0x100:"Unknown item error",
    0x101:"Item not found",
    0x102:"Item in use",
    0x103:"Invalid item handle",
    0x104:"Invalid item name",
    0x105:"Maximum number of items of a particular type reached",
    0x120:"Keygroup not found",
    0x180:"Unknown disk error",
    0x181:"No Disks",
    0x182:"Disk is invalid",
    0x183:"Load error",
    0x184:"Create error",
    0x185:"Directory not empty",
    0x186:"Delete error",
    0x187:"Disk is write-protected",
    0x188:"Disk is not writable",
    0x189:"Disk full",
    0x18A:"Disk abort",
    0x200:"Unknown file error",
    0x201:"File format is not supported",
}

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
