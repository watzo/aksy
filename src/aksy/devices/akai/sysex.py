import struct, sys, types

class Command:
    """Represents a system exclusive command.
    """

    def __init__(self, device_id, id, name, arg_types, reply_spec=()):
        self.device_id = device_id
        self.id = id
        self.name = name
        self.arg_types = []
        self.reply_spec = reply_spec

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
    """
    def __init__(self, command, args, userref='\x00'):
        bytes = [START_SYSEX, AKAI_ID]

        bytes.append(command.device_id)
        bytes.append(userref)
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
    def __init__(self, bytes, command, userref='\x00'):
        self.bytes = bytes
        self.command = command
        self.userref = userref

    def parse(self):
        """ Parses the command sequence
        """

        if self.bytes[0] != START_SYSEX or self.bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")
        # TODO: dispatching on z48id, userref and command
        i = 2   # skip start sysex, vendor id
        i += len(self.command.device_id)
        i += len(self.userref)
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
                'Parsing the wrong reply for command %02x %02x'
                    % struct.unpack('2B', self.command.id[:2]))
        if self.command.reply_spec is None:
            return parse_typed_bytes(self.bytes, i)
        else:
            return parse_untyped_bytes(self.bytes, self.command.reply_spec, i)

    def __repr__(self):
         return repr([ "%02x" %byte for byte in struct.unpack(str(len(self.bytes)) + 'B', self.bytes)])

def parse_typed_bytes(bytes, offset):
    result = []
    while offset < (len(bytes) - 1):
        type = _types[bytes[offset]]
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

# Module vars and methods

START_SYSEX = '\xf0'
AKAI_ID = '\x47'
Z48_ID = '\x5f'
AKSYS_Z48_ID = '\x5e\x20\x00' # used by ak.Sys for some requests

DEFAULT_USERREF = '\x00'
END_SYSEX = '\xf7'

POSTIVE     = '\x00'
NEGATIVE    = '\x01'

STRING_TERMINATOR = '\x00'

REPLY_ID_OK = '\x4f'
REPLY_ID_DONE = '\x44'
REPLY_ID_REPLY = '\x52'
REPLY_ID_ERROR = '\x45'

class SysexType(object):
    def __init__(self, size, signed=False, id=None, min_val=None, max_val=None):
        self.id = id
        self.size = size

        if max_val is None:
            self.max_val = signed and pow(2, 7*size-1) - 1 or pow(2, 7*size) - 1
        else:
            self.max_val = max_val

        if min_val is None:
            self.min_val = signed and self.max_val*-1 or 0
        else:
            self.min_val = min_val

    def set_min_val(self, value):
        self.min_val = value

    def set_max_val(self, value):
        self.max_val = value

    def encode(self, value):
        """Encodes a value as sysex byte string
        """
        if (value < self.min_val or
            value > self.max_val):
            raise ValueError("Value %s out of range:[%s-%s]" % (repr(value),
                              repr(self.min_val), repr(self.max_val)))
        return self._encode(value)

    def decode(self, value, typed=True):
        """Decodes a value from a sysex byte string
        """
        if value is None or not isinstance(value, types.StringType):
            raise ValueError(
                "Decoding error at %s.decode: %s is not a string"
                % (self.__class__.__name__, repr(value)))

        if self.size is not None:
            if len(value) == self.size + 1:
                if typed and value[0] != self.id:
                    raise ParseException(
                        "Decoding error %s while decoding %s"
                            % (self.__class__.__name__, repr(value)))
                value = value[1:]
            elif self.size != len(value):
                raise ValueError("Length of string to decode %s <> %s" % (repr(value), repr(self.size)))

        return self._decode(value)

class ByteType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 1, False, '\x00')

    def _encode(self, value):
        """
        >>> b = ByteType()
        >>> b.encode(128)
        Traceback (most recent call last):
            if value > 127: raise ValueError
        ValueError: Value 128 out of range:[0-127]
        """

        return struct.pack('B', value)

    def _decode(self, string):
        """
        b = ByteType()
        b.decode('\x05')
        5
        """
        return struct.unpack('B', string)[0]

class SignedByteType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 2, True, '\x01')

    def _encode(self, value):
        """
        sb = SignedByteType()
        sb.encode(-5)
        '\x01\x05'
        """
        sign = value < 0 and 1 or 0
        return struct.pack('2B', sign, abs(value))

    def _decode(self, string):
        """
        sb = SignedByteType()
        sb.decode('\x01\x05')
        -5
        """
        result = struct.unpack('B', string[1])[0]

        if string[0] == NEGATIVE:
            result *= -1
        return result

class WordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 2, False, '\x02')

    def _encode(self, value):
        """
        w = WordType()
        w.encode(256)
        '\x00\x02'
        """
        return struct.pack('2B', value & 0x0f, value >> 7)

    def _decode(self, string):
        b1, b2 = struct.unpack('2B', string)
        return (b2 << 7) + b1

class SignedWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 3, True, '\x03')

    def _encode(self, value):
        r"""
        >>> sw = SignedWordType()
        >>> sw.encode(256)
        '\x00\x00\x02'

        >>> sw.encode(-16383)
        '\x01\x7f\x7f'

        >>> sw.encode(-256)
        '\x01\x00\x02'
        """
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('3B', sign, value & 0x7f, value >> 7)

    def _decode(self, string):
        r"""
        >>> sw = SignedWordType()
        >>> sw.decode('\x01\x00\x02')
        -256
        >>> sw.decode('\x01\x7f\x7f')
        -16383
        """
        s, b1, b2 = struct.unpack('3B', string[:3])
        sign = s and -1 or 1
        return sign * ((b2 << 7) | b1)

class DoubleWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 4, False, '\x04')

    def _encode(self, value):
        r"""
        >>> dw = DoubleWordType()
        >>> dw.encode(268435455)
        '\x7f\x7f\x7f\x7f'
        >>> dw.encode(1)
        '\x01\x00\x00\x00'
        """
        return struct.pack('4B', value & 0x7f, (value >> 7) & 0x7f, (value >> 14) & 0x7f, (value >> 21) & 0x7f)

    def _decode(self, string):
        r"""
        >>> dw = DoubleWordType()
        >>> dw.decode('\x7f\x7f\x7f\x7f')
        268435455
        """
        b1, b2, b3, b4 = struct.unpack('4B', string)
        return (b4 << 21) | (b3 << 14) | (b2 << 7) | b1

class SignedDoubleWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 5, True, '\x05')

    def _encode(self, value):
        r"""
        >>> sdw = SignedDoubleWordType()
        >>> sdw.encode(-268435455)
        '\x01\x7f\x7f\x7f\x7f'
        """
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('5B', sign, value & 0x7f, (value >> 7) & 0x7f, (value >> 14) & 0x7f, (value >> 21) & 0x7f)

    def _decode(self, string):
        r"""
        >>> sdw = SignedDoubleWordType()
        >>> sdw.decode('\x01\x7f\x7f\x7f\x7f')
        -268435455
        """

        s, b1, b2, b3, b4 = struct.unpack('5B', string)
        sign = s and -1 or 1
        return sign * ((b4 << 21) | (b3 << 14) | (b2 << 7) | b1)

class QWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 8, False, '\x06')

    def _encode(self, value):
        r"""
        >>> qw = QWordType()
        >>> qw.encode(268435455)
        '\x7f\x7f\x7f\x7f\x00\x00\x00\x00'
        """

        return struct.pack('8B',  value & 0x7f, (value >> 7) & 0x7f,
            (value >> 14) & 0x7f, (value >> 21) & 0x7f, (value >> 28) & 0x7f,
            (value >> 35) & 0x7f, (value >> 42) & 0x7f, (value >> 49) & 0x7f)

    def _decode(self, string):
        r"""
        >>> qw = QWordType()
        >>> qw.decode('\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f')
        72057594037927935L
        >>> qw.decode('\x25\x74\x08\x00\x00\x00\x00\x00')
        145957L
        """
        b1, b2, b3, b4, b5, b6, b7, b8 = struct.unpack('8B', string)
        # bitshifting looks prettier but this works ;-)
        return (b8*pow(2,49)|b7*pow(2,42)|b6*pow(2,35)|b5*pow(2,28)|b4*pow(2,21)|b3*pow(2,14)|b2*pow(2,7)|b1)

class SignedQWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 9, True, '\x07')

    def _encode(self, value):
        r"""
        >>> sdw = SignedQWordType()
        >>> sdw.encode(-268435455)
        '\x01\x7f\x7f\x7f\x7f\x00\x00\x00\x00'
        """
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('9B', sign, value & 0x7f, (value >> 7) & 0x7f,
            (value >> 14) & 0x7f, (value >> 21) & 0x7f, (value >> 28) & 0x7f,
            (value >> 35) & 0x7f, (value >> 42) & 0x7f, (value >> 49) & 0x7f)

    def _decode(self, string):
        r"""
        >>> qw = SignedQWordType()
        >>> qw.decode('\x01\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f')
        -72057594037927935L

        >>> qw.decode('\x01\x00\x00\x00\x00\x00\x00\x7f\x00')
        -558551906910208L
        """
        s, b1, b2, b3, b4, b5, b6, b7, b8 = struct.unpack('9B', string)
        sign = s and -1 or 1
        # bitshifting looks prettier but this works without losing bits ;-)
        return sign * (b8*pow(2,49)|b7*pow(2,42)|b6*pow(2,35)|b5*pow(2,28)|b4*pow(2,21)|b3*pow(2,14)|b2*pow(2,7)|b1)

class BoolType(ByteType):
    def __init__(self):
        ByteType.__init__(self)
        self.set_min_val(0)
        self.set_max_val(1)

    def _encode(self, value):
        r"""
        >>> b = BoolType()
        >>> b.encode(False)
        '\x00'
        >>> b.encode(True)
        '\x01'
        """
        return super(BoolType, self)._encode(int(value))

    def _decode(self, string):
        return bool(struct.unpack('B', string)[0])

class StringType(object):
    def __init__(self):
        self.id = '\x08'
        self.size = None # variable size, parsed length is returned in result

    def validate_encode(self, value):
        if not type(value) == type('') and value != '':
            raise ValueError("Value %s should be a (non unicode) string." % repr(value))

    def encode(self, value):
        r"""
        Todo: send the raw bytes + terminator if validate_encode fails
        >>> s = StringType()
        >>> s.encode('test sdf')
        'test sdf\x00'
        """
        self.validate_encode(value)
        return struct.pack(str(len(value)+1) + 's', value)

    def decode(self, string):
        r"""
        >>> s = StringType()
        >>> s.decode('test sdf\x00')
        (9, 'test sdf')
        """
        index = string.find(STRING_TERMINATOR)
        if index == -1: raise ValueError
        if string[0] == self.id:
            start = 1
        else:
            start = 0
        return index + 1, struct.unpack( str(index-start) + 's', string[start:index])[0]

class StringArrayType(object):
    """
    """
    def __init__(self):
        self.size = None # variable size, parsed length is returned in result

    def encode(self, value):
        raise NotImplementedError()

    def decode(self, string):
        if not string or not isinstance(string, types.StringType):
            raise ValueError(
                "Decoding error at %s.decode: %s is not a string"
                % (self.__class__.__name__, repr(string)))

        result = []
        index = 0
        offset = 0
        for char in string:
            #sys.stderr.writelines( "c:%s i:%s\n" % (char, index) )
            if (char == END_SYSEX):
                break;
            if char == STRING_TERMINATOR:
                result.append(struct.unpack( str(index) + 's', string[offset:offset+index])[0])
                offset += index + 1
                index = 0
            else:
                index += 1
        return (offset + index, tuple(result))

class PadType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 1, False)

    def _decode(self, value):
        return None

class SoundLevelType(SignedWordType):
    r"""Represents soundlevels in dB
    >>> sl = SoundLevelType()
    >>> sl.decode(sl.encode(-34.0))
    -34.0
    """
    def __init__(self):
        SignedWordType.__init__(self)
        self.set_min_val(-600)
        self.set_max_val(60)

    def _encode(self, value):
        return super(SoundLevelType, self)._encode(int(value*10))

    def _decode(self, string):
        """XXX: reconsider conversion here
        """
        return super(SoundLevelType, self)._decode(string)/10.0

class PanningType(ByteType):
    """Represents panning levels in -50->L, 50->R
    """

# Sysex type ids
BYTE        = ByteType()
SBYTE       = SignedByteType()
WORD        = WordType()
SWORD       = SignedWordType()
DWORD       = DoubleWordType()
SDWORD      = SignedDoubleWordType()
QWORD       = QWordType()
SQWORD      = SignedQWordType()
STRING      = StringType()
STRINGARRAY = StringArrayType()

TWO_BYTES   = SysexType(2, False, '\x09')
THREE_BYTES = SysexType(3, False, '\x0b')

# aksy type extensions
PAD         = PadType()
BOOL        = BoolType()
CENTS       = '\x23' # SWORD(+- 3600)
PAN         = PanningType()
LEVEL       = SoundLevelType()

_types = {
    BYTE.id: BYTE,
    SBYTE.id: SBYTE,
    WORD.id: WORD,
    SWORD.id: SWORD,
    DWORD.id: DWORD,
    SDWORD.id: SDWORD,
    QWORD.id: QWORD,
    SQWORD.id: SQWORD,
    STRING.id: STRING,
    TWO_BYTES.id: TWO_BYTES,
    THREE_BYTES.id: THREE_BYTES,
}

class UnknownSysexTypeError(Exception):
    pass

def getType(typeId):
    type = _types.get(typeId, None)
    if type is None:
        raise UnknownSysexTypeError( "%02x" % struct.unpack('B', '\x0a'))

class HandleNameArrayType(object):
    r"""Mixed data type, wrapping handle(DoubleWord) and name (StringType)

    >>> handle_name_type = HandleNameArrayType()
    >>> handle_name_type.decode('\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
    (16, (65537, 'SynthTest'))
    >>> handle_name_type.decode('\x04\x00\x00\x04\x00\x08\x44\x72\x79\x20\x4b\x69\x74\x20\x30\x32\x00\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
    (33, (65536, 'Dry Kit 02', 65537, 'SynthTest'))

    """
    def __init__(self):
        self.size = None
    def encode(self, value):
        raise NotImplementedError

    def decode(self, string):
        results = []
        len_to_parse = len(string)
        len_parsed = 0
        while len_parsed < len_to_parse:
            results.append(
                DWORD.decode(
                    string[len_parsed:len_parsed+5], typed=False))
            len_parsed += 5
            len_result, result = STRING.decode(string[len_parsed:])
            results.append(result)
            len_parsed += len_result
        return len_parsed, tuple(results)

HANDLENAMEARRAY = HandleNameArrayType()

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
