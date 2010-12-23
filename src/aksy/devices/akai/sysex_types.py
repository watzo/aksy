import struct, logging, types

START_SYSEX = '\xf0'
STRING_TERMINATOR = '\x00'
END_SYSEX = '\xf7'

POSTIVE     = '\x00'
NEGATIVE    = '\x01'

log = logging.getLogger("aksy.devices.akai.sysex_types")
log.disabled = True

def byte_repr(bytes):
    return repr([ "%02x" %byte for byte in struct.unpack(str(len(bytes)) + 'B', bytes)])

class SysexType(object):
    def __init__(self, size, signed=False, id=None):
        self.id = id
        self.size = size

        self.max_val = signed and pow(2, 7*size-1) - 1 or pow(2, 7*size) - 1
        self.min_val = signed and self.max_val*-1 or 0

    def validate_encode(self, value):
        if (value < self.min_val or
            value > self.max_val):
            raise ValueError("Value %s out of range:[%s-%s]" % (repr(value),
                              repr(self.min_val), repr(self.max_val)))

    def set_min_val(self, value):
        """
        Override for custom types
        """
        self.min_val = value
    def set_max_val(self, value):
        """
        Override for custom types
        """
        self.max_val = value

    def _encode(self, value):
        raise NotImplementedError("_encode")

    def _decode(self, value):
        raise NotImplementedError("_decode")
    
    def encode(self, value):
        """Encodes a value as sysex byte string
        """
        self.validate_encode(value)
        return self._encode(value)

    def decode(self, value, typed=True):
        """Decodes a value from a sysex byte string
        """
        if value is None or not isinstance(value, types.StringType):
            raise DecodeException(
                "Decoding error at %s.decode: %s is not a string"
                % (self.__class__.__name__, repr(value)))

        if self.size is not None:
            if len(value) == self.size + 1:
                if typed and value[0] != self.id:
                    raise DecodeException(
                        "Decoding error %s while decoding %s"
                            % (self.__class__.__name__, repr(value)))
                value = value[1:]
            elif self.size != len(value):
                raise DecodeException("Length of string to decode %s <> %s" % 
                          (repr(value), repr(self.size)))

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
        return struct.pack('2B', value & 0x7f, value >> 7)

    def _decode(self, string):
        byte1, byte2 = struct.unpack('2B', string)
        return (byte2 << 7) + byte1

class CompoundWordType(SysexType):
    """ the little endian brother of WordType
    """
    def __init__(self):
        SysexType.__init__(self, 2, False, '\x02')

    def _encode(self, value):
        return struct.pack('2B', value >> 7,  value & 0x7f)

    def _decode(self, string):
        byte1, byte2 = struct.unpack('2B', string)
        return (byte1 << 7) + byte2


class SignedWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 3, True, '\x03')

    def _encode(self, value):
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('3B', sign, value & 0x7f, value >> 7)

    def _decode(self, string):
        s, b1, b2 = struct.unpack('3B', string[:3])
        sign = s and -1 or 1
        return sign * ((b2 << 7) | b1)

class DoubleWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 4, False, '\x04')

    def _encode(self, value):
        return struct.pack('4B', value & 0x7f, (value >> 7) & 0x7f, (value >> 14) & 0x7f, (value >> 21) & 0x7f)

    def _decode(self, string):
        b1, b2, b3, b4 = struct.unpack('4B', string)
        return (b4 << 21) | (b3 << 14) | (b2 << 7) | b1

class SignedDoubleWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 5, True, '\x05')

    def _encode(self, value):
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('5B', sign, value & 0x7f, (value >> 7) & 0x7f, (value >> 14) & 0x7f, (value >> 21) & 0x7f)

    def _decode(self, string):
        s, b1, b2, b3, b4 = struct.unpack('5B', string)
        sign = s and -1 or 1
        return sign * ((b4 << 21) | (b3 << 14) | (b2 << 7) | b1)

class QWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 8, False, '\x06')

    def _encode(self, value):
        return struct.pack('8B',  value & 0x7f, (value >> 7) & 0x7f,
            (value >> 14) & 0x7f, (value >> 21) & 0x7f, (value >> 28) & 0x7f,
            (value >> 35) & 0x7f, (value >> 42) & 0x7f, (value >> 49) & 0x7f)

    def _decode(self, string):
        b1, b2, b3, b4, b5, b6, b7, b8 = struct.unpack('8B', string)
        # bitshifting looks prettier but this works ;-)
        return (b8*pow(2,49)|b7*pow(2,42)|b6*pow(2,35)|b5*pow(2,28)|b4*pow(2,21)|b3*pow(2,14)|b2*pow(2,7)|b1)

class SignedQWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 9, True, '\x07')

    def _encode(self, value):
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('9B', sign, value & 0x7f, (value >> 7) & 0x7f,
            (value >> 14) & 0x7f, (value >> 21) & 0x7f, (value >> 28) & 0x7f,
            (value >> 35) & 0x7f, (value >> 42) & 0x7f, (value >> 49) & 0x7f)

    def _decode(self, string):
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
        self.validate_encode(value)
        return struct.pack(str(len(value)+1) + 's', value)

    def decode(self, string):
        index = string.find(STRING_TERMINATOR)
        if index == -1: 
            raise ValueError
        if string[0] == self.id:
            start = 1
        else:
            start = 0
        return index + 1, struct.unpack( str(index-start) + 's', string[start:index])[0]

class StringArrayType(object):
    def __init__(self):
        self.size = None # variable size, parsed length is returned in result

    def encode(self, value):
        raise NotImplementedError()

    def decode(self, string):
        if not string or not isinstance(string, types.StringType):
            raise DecodeException(
                "%s.decode: %s is not a string"
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

class UserRefType(object):
    """ Can be used to stamp a request with an identifier
    size = None: variable size <= 2
    """
    def __init__(self, encoding_size=None):
        if encoding_size is not None and encoding_size > 3 and encoding_size < 0:
            raise ValueError("Illegal userref encoding_size %i" % encoding_size)
        self.encoding_size = encoding_size
        self.min_val = 0
        self.max_val = WORD.max_val

    def _encode_WORD(self, value):
        return BYTE.encode(2 << 4) + WORD.encode(value)

    def _encode_BYTE(self, value):
        return BYTE.encode(1 << 4) + BYTE.encode(value)

    def encode(self, value):
        if value < self.min_val or value > self.max_val:
            raise ValueError("Value %i out of range" % value)

        if self.encoding_size is None:
            if value == 0:
                return BYTE.encode(0)
            if value > BYTE.max_val:
                return self._encode_WORD(value)
            return self._encode_BYTE(value)

        if self.encoding_size == 0:
            return BYTE.encode(0)
        if self.encoding_size == 1:
            return self._encode_BYTE(value)
        if self.encoding_size == 2:
            return self._encode_WORD(value)

    def decode_length(self, byte):
        return byte >> 4

    def decode(self, string):
        if not string or not isinstance(string, types.StringType):
            raise ValueError(
                "Decoding error at %s.decode: %s is not a string"
                % (self.__class__.__name__, repr(string)))

        length = self.decode_length(BYTE.decode(string[0]))
        if length == 0:
            return (1, 0)
        if length == 1:
            return (2, BYTE.decode(string[1:2]))
        if length == 2:
            return (3, WORD.decode(string[1:3]))
        raise DecodeException("Unexpected UserRef length %i" % length)

class Z48UserRefType(UserRefType):

    def _encode_WORD(self, value):
        return BYTE.encode(2 << 5) + WORD.encode(value)

    def _encode_BYTE(self, value):
        return BYTE.encode(1 << 5) + BYTE.encode(value)

    def decode_length(self, byte):
        return byte >> 5

class TypeByteType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 1, False)

    def _decode(self, value):
        return None

class TuneType(SignedWordType):
    """Represents tuning in cents
    """
    def __init__(self):
        SignedWordType.__init__(self)
        self.set_min_val(-3600)
        self.set_max_val(3600)

    def _encode(self, value):
        return super(TuneType, self)._encode(value)

    def _decode(self, string):
        return super(TuneType, self)._decode(string)

class SoundLevelType(SignedWordType):
    """Represents soundlevels in dB
    """
    def __init__(self):
        SignedWordType.__init__(self)
        self.set_min_val(-600)
        self.set_max_val(60)

    def _encode(self, value):
        return super(SoundLevelType, self)._encode(int(value*10))

    def _decode(self, string):
        return super(SoundLevelType, self)._decode(string)/10.0

class PanningType(ByteType):
    """Represents panning levels in -50->L, 50->R
    """

class FileType(ByteType):
    """Akai file types
    """
    ALL = 0
    MULTI = 1
    PROGRAM = 2
    SAMPLE = 3
    MIDI = 4
    def __init__(self):
        ByteType.__init__(self)
        self.set_min_val(0)
        self.set_max_val(4)

class CompositeType(object):
    def __init__(self, type_list):
        # log.debug("Initializing types %s" % repr(type_list))
        self.types = type_list

    def decode(self, string):
        offset = 0
        result = []
        for sysex_type in self.types:
            len_parsed, part = parse_byte_string(string, sysex_type, offset)
            if part is not None:
                result.append(part)
            offset += len_parsed
        if len(result) == 1:
            return offset, result[0]
        return offset, tuple(result)

class TypedCompositeType(object):
    def decode(self, string):
        result = []
        offset = 0
        while offset < (len(string) - 1):
            sysex_type = get_type(string[offset])
            if log.isEnabledFor(logging.DEBUG):
                log.debug("Parsing type %s" % sysex_type)
            offset += 1
            len_parsed, part = parse_byte_string(string, sysex_type, offset)
            if part is not None:
                result.append(part)
                offset += len_parsed
        if len(result) == 1:
            return offset, result[0]
        return offset, tuple(result)

class DiskType(CompositeType):
    def __init__(self):
        super(DiskType, self).__init__((
            WORD, BYTE,
            BYTE, BYTE,
            BYTE, STRING,))

class S56kDiskType(CompositeType):
    def __init__(self):
        super(S56kDiskType, self).__init__((
            CWORD, BYTE,
            BYTE, BYTE,
            BYTE, STRING,))


class DisklistType(object):
    def __init__(self):
        self.size = None

    def decode(self, string):
        result = []
        index = 0
        while string[index] != END_SYSEX:
            length, val = DISK.decode(string[index:])
            result.append(val)
            index += length
        return index, tuple(result)

class S56kDisklistType(object):
    def __init__(self):
        self.size = None

    def decode(self, string):
        result = []
        index = 0
        while string[index] != END_SYSEX:
            length, val = S56KDISK.decode(string[index:])
            result.append(val)
            index += length
        return index, tuple(result)


def parse_byte_string(data, sysex_type, offset=0):
    """ Parses a byte string
    """

    len_parsed_data = 0
    if sysex_type.size is not None:
        result = sysex_type.decode(data[offset:offset+sysex_type.size])
        len_parsed_data = sysex_type.size
    else:
        # TODO: use a factory which returns instances with a size set ?
        len_parsed_data, result = sysex_type.decode(data[offset:])
        if len_parsed_data == 0:
            result = None

    return len_parsed_data, result

class CompositeByteType(SysexType):
    def __init__(self, size, type_id):
        super(CompositeByteType, self).__init__(size, False, type_id)
        self.set_min_val(0)
        self.set_max_val(127)
    def encode(self, *args):
        if len(args) != self.size:
            raise ValueError("%s ints expected" % self.size)
        for byte in args:
            self.validate_encode(byte)

        return struct.pack("%iB" %self.size, *args)

    def _encode(self, string):
        pass # no-op, as encode itself is overridden
    
    def _decode(self, string):
        return struct.unpack("%iB" %self.size, string)

class TwoByteType(CompositeByteType):
    def __init__(self):
        super(TwoByteType, self).__init__(2, '\x09')

class ThreeByteType(CompositeByteType):
    def __init__(self):
        super(ThreeByteType, self).__init__(3, '\x0a')

class FourByteType(CompositeByteType):
    def __init__(self):
        super(FourByteType, self).__init__(4, '\x0b')

# TODO: make HandleNameDictType
class HandleNameArrayType(object):
    """Mixed data type, wrapping handle(DoubleWord) and name (StringType)
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
            handle = DWORD.decode(
                    string[len_parsed:len_parsed+5], typed=False)
            len_parsed += 5
            len_result, name = STRING.decode(string[len_parsed:])
            results.append((handle, name))
            len_parsed += len_result
        return len_parsed, tuple(results)

class NameSizeArrayType(object):
    """Mixed data type, wrapping name (StringType) and size (DoubleWord)
    """
    def __init__(self):
        self.size = None
    def encode(self, value):
        raise NotImplementedError

    def decode(self, string):
        results = []
        len_to_parse = len(string)
        len_parsed = 0
        while len_parsed < len_to_parse and string[len_parsed] != END_SYSEX:
            len_result, name = STRING.decode(string[len_parsed:])
            len_parsed += len_result
            size = DWORD.decode(
                    string[len_parsed-1:len_parsed+4], typed=False)
            len_parsed += 4
            results.append(name)
            results.append(size)
        return len_parsed, tuple(results)

# Base Sysex types
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

USERREF     = UserRefType()
Z48USERREF  = Z48UserRefType()

# S56k types
S56K_USERREF = UserRefType(2)
CWORD        = CompoundWordType()

TWO_BYTES   = TwoByteType()
THREE_BYTES = ThreeByteType()
FOUR_BYTES  = FourByteType()

# derived types
TYPEBYTE    = TypeByteType()
BOOL        = BoolType()
TUNE        = TuneType()
PAN         = PanningType()
FILETYPE    = FileType()
LEVEL       = SoundLevelType()

# Composite types
DISK        = DiskType()
DISKLIST    = DisklistType()
S56KDISK        = S56kDiskType()
S56KDISKLIST    = S56kDisklistType()
TYPED_COMPOSITE = TypedCompositeType()
HANDLENAMEARRAY = HandleNameArrayType()
NAMESIZEARRAY = NameSizeArrayType()

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
    FOUR_BYTES.id: FOUR_BYTES,
}

class UnknownSysexTypeError(Exception):
    pass

class DecodeException(Exception):
    pass

def get_type(typeId):
    type = _types.get(typeId, None)
    if type is None:
        raise UnknownSysexTypeError( "%02x" % struct.unpack('B', typeId))
    return type
