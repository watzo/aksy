import struct, sys 

class Command:
    """Represents a system exclusive command.
    """
    def __init__(self, id, name, arg_types, reply_spec=None):
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

class CommandSpec:
    """Represents the format of system exclusive command.
    where ID is one id byte, IDS a list of ids, 
    EG GX700:
    (sysex.Command.HEADER, sysex.Command.ARG, sysex.Command.ID, sysex.Command.ARGS)
    EG Z48:
    (sysex.Command.HEADER, sysex.Command.ID, sysex.Command.ARGS)
    """
    ID = "id" 
    ID = "ids" 
    ARG = "arg" 
    ARGS = "args"
    EXTRA_ID = 5
    def __init__(self, header, *args):
        self.header = header
        self.items = args

class Request:
    r""" Encapsulates a sysex request

    Select disk:
    >>> arg = 256
    >>> command_spec = CommandSpec('\x47\x5f\x00', CommandSpec.ID, CommandSpec.ARGS)
    >>> command = Command('\x20\x02', 'select_disk', (WORD,None), ())
    >>> Request(command, command_spec, (arg,))
    ['f0', '47', '5f', '00', '20', '02', '00', '02', 'f7']
    """

    def __init__(self, command, command_spec, args=(), ids=()):
        bytes = [START_SYSEX, command_spec.header,]

        ids = [command.id, ] + list(ids)
        for item in command_spec.items:
            if item == CommandSpec.ARG:
                data = self._create_byte_fragment(args, command, True)
            elif item == CommandSpec.ARGS:
                data = self._create_byte_fragment(args, command, False)
            elif item == CommandSpec.ID:
                data = ids.pop(0)
            elif item == CommandSpec.IDS:
                data = ids
            else:
                raise Exception("Unknown command specification %s\n" % item)

            if data is not None:
                bytes.extend(data)
            
        bytes.append(END_SYSEX)

        self.bytes = ''.join(bytes)

    def _create_byte_fragment(self, list, command, one_item):
        if len(list) == 0:
            return None
        if one_item:
            return command.create_arg_bytes(list.pop(0)) 
        else:
            return command.create_arg_bytes(list) 
        
    def get_bytes(self):
        return self.bytes;

    def __repr__(self):
        return repr([ "%02x" %byte for byte in struct.unpack(str(len(self.bytes)) + 'B', self.bytes)])

class ReplySpec:
    """Represents the format of system exclusive reply.
    EG GX700:
    vendor_id, device_id, model_id, command id, patch addresses, data
    EG Z48:
    vendor_id, device_id, model_id, command ids, reply_id, data
    """
    def __init__(self, spec): 
        self.spec = ('vendor_id', 'device_id', 'model_id')
        self.spec.extend(spec) 

class ReplyParser:
    r""" Encapsulates a sysex reply

    """
    def __init__(self, reply_spec, types):
        self.reply_spec = reply_spec
        self.types = types

    def parse(self, command, bytes):
        """ Parses the command sequence
        """

        if bytes[0] != START_SYSEX or bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")
        bytes = bytes[1:-1]
        reply_spec = command.reply_spec
        i = 1   # skip vendor id
#        if self.model_id is not None:
#            i += len(self.model_id)
#        else:
        i += 1

        # XXX: These akai z48 specifix should go
        i += 1 # userref 
        reply_id = bytes[i]

        i +=  3 # skip past the reply, section and command
        if reply_id == REPLY_ID_OK:
            return None 
        elif reply_id == REPLY_ID_DONE:
            return None 
        elif reply_id == REPLY_ID_ERROR: 
            b1, b2 = struct.unpack('2B', self.bytes[i:i+2])
            code = (b2 << 7) + b1

            raise Exception("System exclusive error, code %02x, message: %s " % (code, errors.get(code, "Unknown")))
        elif reply_id == REPLY_ID_REPLY:
            # continue
            pass
        else:
            raise ParseException("Unknown reply type: %02x" % struct.unpack('b', reply_id))

        return self.parse_untyped_bytes(bytes, i)

    def parse_typed_bytes(self, bytes, offset):
        raise NotImplementedError

        result = []
        while offset < (len(bytes) - 1):
            part, len_parsed = parse_byte_string(bytes, offset)
            if part is not None:
                result.append(part)
            offset += len_parsed
        if len(result) == 1:
            return result[0]
        else:
            return tuple(result)

    def parse_untyped_bytes(self, bytes, offset):
        """Parses a byte string without type information
        """
        result = []
        for type in self.reply_spec:
            part, len_parsed = parse_byte_string(bytes, type, offset) 
            if part is not None:
                result.append(part)
            offset += len_parsed
        if len(result) == 1:
            return result[0]
        else:
            return tuple(result)

    def __repr__(self):
         return repr([ "%02x" %byte for byte in struct.unpack(str(len(self.bytes)) + 'B', self.bytes)])

class ParseException(Exception):
    """ Exception raised when parsing system exclusive fails
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

# Need to move this into an enum type
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
        raise NotImplementedError

    def decode(self, value):
        """Decodes a value from a sysex byte string
        """
        raise NotImplementedError

    def validate_encode(self, value):
        """Validates the value to encode
        """
        if (value < self.min_val or
            value > self.max_val): 
            raise ValueError("Value %s out of range:[%s-%s]" % (repr(value),
                              repr(self.min_val), repr(self.max_val)))

    def validate_decode(self, value):
        """Validates the value to decode
        """
        if value is None or self.size != len(value):
            raise ValueError("Length of string to decode %s <> %s" % (repr(value), repr(self.size)))

class ByteType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 1, False, 'x01')

    def encode(self, value):
        """
        >>> b = ByteType()
        >>> b.encode(128)
        Traceback (most recent call last):
            if value > 127: raise ValueError
        ValueError: Value 128 out of range:[0-127]
        """

        super(ByteType, self).validate_encode(value)
        return struct.pack('B', value)

    def decode(self, string):
        """
        b = ByteType()
        b.decode('\x05')
        5
        """
        super(ByteType, self).validate_decode(string)
        return struct.unpack('B', string)[0]

class SignedByteType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 2, True, 'x02')

    def encode(self, value):
        """
        sb = SignedByteType()
        sb.encode(-5)
        '\x01\x05'
        """
        super(SignedByteType, self).validate_encode(value)
        sign = value < 0 and 1 or 0
        return struct.pack('2B', sign, abs(value))

    def decode(self, string):
        """
        sb = SignedByteType()
        sb.decode('\x01\x05')
        -5
        """
        super(SignedByteType, self).validate_decode(string)
        result = struct.unpack('B', string[1])[0]

        if string[0] == NEGATIVE:
            result *= -1 
        return result

class WordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 2, False, 'x03')

    def encode(self, value):
        """
        w = WordType()
        w.encode(256)
        '\x00\x02'
        """
        super(WordType, self).validate_encode(value)
        return struct.pack('2B', value & 0x0f, value >> 7)

    def decode(self, string):
        super(WordType, self).validate_decode(string)
        b1, b2 = struct.unpack('2B', string)
        return (b2 << 7) + b1

class SignedWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 3, True, 'x04')

    def encode(self, value):
        r"""
        >>> sw = SignedWordType()
        >>> sw.encode(256)
        '\x00\x00\x02'

        >>> sw.encode(-16383)
        '\x01\x7f\x7f'

        >>> sw.encode(-256)
        '\x01\x00\x02'
        """
        super(SignedWordType, self).validate_encode(value)
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('3B', sign, value & 0x7f, value >> 7)

    def decode(self, string):
        r"""
        >>> sw = SignedWordType()
        >>> sw.decode('\x01\x00\x02')
        -256
        >>> sw.decode('\x01\x7f\x7f')
        -16383
        """
        super(SignedWordType, self).validate_decode(string)
        s, b1, b2 = struct.unpack('3B', string[:3])
        sign = s and -1 or 1
        return sign * ((b2 << 7) | b1)

class DoubleWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 4, False, '\x05')

    def encode(self, value):
        r"""
        >>> dw = DoubleWordType()
        >>> dw.encode(268435455) 
        '\x7f\x7f\x7f\x7f'
        >>> dw.encode(1) 
        '\x01\x00\x00\x00'
        """
        return struct.pack('4B', value & 0x7f, (value >> 7) & 0x7f, (value >> 14) & 0x7f, (value >> 21) & 0x7f)

    def decode(self, string):
        r"""
        >>> dw = DoubleWordType()
        >>> dw.decode('\x7f\x7f\x7f\x7f')
        268435455
        """
        super(DoubleWordType, self).validate_decode(string)
        b1, b2, b3, b4 = struct.unpack('4B', string)
        return (b4 << 21) | (b3 << 14) | (b2 << 7) | b1

class SignedDoubleWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 5, True, '\x06')

    def encode(self, value):
        r"""
        >>> sdw = SignedDoubleWordType()
        >>> sdw.encode(-268435455) 
        '\x01\x7f\x7f\x7f\x7f'
        """
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('5B', sign, value & 0x7f, (value >> 7) & 0x7f, (value >> 14) & 0x7f, (value >> 21) & 0x7f)
        
    def decode(self, string):
        r"""
        >>> sdw = SignedDoubleWordType()
        >>> sdw.decode('\x01\x7f\x7f\x7f\x7f')
        -268435455
        """
        super(SignedDoubleWordType, self).validate_decode(string)

        s, b1, b2, b3, b4 = struct.unpack('5B', string)
        sign = s and -1 or 1
        return sign * ((b4 << 21) | (b3 << 14) | (b2 << 7) | b1)

class QWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 8, False, '\x07')

    def encode(self, value):
        r"""
        >>> qw = QWordType()
        >>> qw.encode(268435455) 
        '\x7f\x7f\x7f\x7f\x00\x00\x00\x00'
        """

        super(QWordType, self).validate_encode(value)
        return struct.pack('8B',  value & 0x7f, (value >> 7) & 0x7f,
            (value >> 14) & 0x7f, (value >> 21) & 0x7f, (value >> 28) & 0x7f,
            (value >> 35) & 0x7f, (value >> 42) & 0x7f, (value >> 49) & 0x7f)

    def decode(self, string):
        """
        >>> qw = QWordType()
        >>> qw.decode('\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f')
        72057594037927935L
        """
        super(QWordType, self).validate_decode(string)
        b1, b2, b3, b4, b5, b6, b7, b8 = struct.unpack('8B', string)
        # bitshifting looks prettier but this works ;-)
        return (b8*pow(2,49)|b7*pow(2,42)|b6*pow(2,35)|b5*pow(2,28)|b4*pow(2,21)|b3*pow(2,14)|b2*pow(2,7)|b1)

class SignedQWordType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 9, True, '\x08')

    def encode(self, value):
        r"""
        >>> sdw = SignedQWordType()
        >>> sdw.encode(-268435455) 
        '\x01\x7f\x7f\x7f\x7f\x00\x00\x00\x00'
        """
        super(SignedQWordType, self).validate_encode(value)
        sign = value < 0 and 1 or 0
        value = abs(value)
        return struct.pack('9B', sign, value & 0x7f, (value >> 7) & 0x7f,
            (value >> 14) & 0x7f, (value >> 21) & 0x7f, (value >> 28) & 0x7f,
            (value >> 35) & 0x7f, (value >> 42) & 0x7f, (value >> 49) & 0x7f)

    def decode(self, string):
        r"""
        >>> qw = SignedQWordType()
        >>> qw.decode('\x01\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f')
        -72057594037927935L

        >>> qw.decode('\x01\x00\x00\x00\x00\x00\x00\x7f\x00')
        -558551906910208L
        """
        super(SignedQWordType, self).validate_decode(string)
        s, b1, b2, b3, b4, b5, b6, b7, b8 = struct.unpack('9B', string)
        sign = s and -1 or 1
        # bitshifting looks prettier but this works without losing bits ;-)
        return sign * (b8*pow(2,49)|b7*pow(2,42)|b6*pow(2,35)|b5*pow(2,28)|b4*pow(2,21)|b3*pow(2,14)|b2*pow(2,7)|b1)

class BoolType(ByteType):
    def __init__(self):
        ByteType.__init__(self)
        self.set_max_val(1)

    def encode(self, value):
        r"""
        >>> b = BoolType()
        >>> b.encode(False)
        '\x00'
        """
        value = int(value)
        return super(BoolType, self).encode(value)

    def decode(self, string):
        super(BoolType, self).validate_decode(string)
        return bool(struct.unpack('B', string)[0])

class StringType(object):
    def __init__(self):
        self.id = '\x09' 
        self.size = None # variable size

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
        'test sdf'
        """
        index = string.find(STRING_TERMINATOR)
        if index == -1: raise ValueError
        return struct.unpack( str(index) + 's', string[:index])[0]

    def decode_strings(self, string):    
        """XXX: move this method to a string array class
        """
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
        return result

class PadType(SysexType):
    def __init__(self):
        SysexType.__init__(self, 1, False)

    def decode(self, value):
        return None

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

# aksy type extensions
PAD         = PadType()
BOOL        = BoolType()

def parse_byte_string(data, type, offset=0):
    r""" Parses a byte string

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, STRING)
    ('TEST', 5)

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, STRING, 1)
    ('EST', 4)

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR + '\x54\x45\x53\x54' + STRING_TERMINATOR, STRING, 0)
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
    if not isinstance(type, StringType):
        result = type.decode(data[offset:offset+type.size])
        len_parsed_data += type.size
    else:
        # TODO: use a factory which returns instances with a size set ?
        result = type.decode_strings(data[offset:])
        if len(result) == 0:
            result = None
        else:
            for string in result:
                len_parsed_data += (len(string) + 1)

            result = len(result) > 1 and tuple(result) or result[0]
 
    return (result, len_parsed_data)

def _to_string(ordvalues):
    """Method to quickly scan a string 
    >>> ordvalues = (90, 52, 56, 32, 38, 32, 77, 80, 67, 52, 75)
    >>> _to_string(ordvalues)
    'Z48 & MPC4K'
    """
    return ''.join([chr(value) for value in ordvalues])

def _transform_hexstring(value):
    result = []
    for char in value.split(' '):
        result.append(struct.pack('B', int(char, 16)))
    return ''.join(result)
    
if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
