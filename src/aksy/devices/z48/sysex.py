import struct, sys 

class Command:
    """Represents a system exclusive command.
    """

    def __init__(self, id, name, arg_types, reply_spec=()):
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

    Select disk:
    >>> arg = 256 
    >>> command = Command('\x20\x02', 'select_disk', (WORD,), ()) 
    >>> Request(command, (arg,))
    ['f0', '47', '5f', '00', '20', '02', '00', '02', 'f7']

    Select root folder:
    >>> folder = ''
    >>> command = Command('\x20\x13', 'set_curr_folder', (STRING,), ()) 
    >>> Request(command, (folder,))
    ['f0', '47', '5f', '00', '20', '13', '00', 'f7']

    Select autoload folder:
    >>> folder = 'autoload'
    >>> command = Command('\x20\x13', 'set_curr_folder', (STRING,), ()) 
    >>> Request(command, (folder,))
    ['f0', '47', '5f', '00', '20', '13', '61', '75', '74', '6f', '6c', '6f', '61', '64', '00', 'f7']

    >>> command = Command('\x07\x01', 'get_sampler_name', (),(STRING,))
    >>> Request(command, ())
    ['f0', '47', '5f', '00', '07', '01', 'f7']

    """

    def __init__(self, command, args, z48id=None, userref=None):
        bytes = [START_SYSEX, AKAI_ID]

        if z48id is not None:
            bytes.append(z48id) 
        else:
            bytes.append(Z48_ID) 

        if userref is not None:
            bytes.append(userref) 
        else:
            bytes.append(DEFAULT_USERREF) 

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
    r""" Encapsulates a sysex reply

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20\x05', '\x01', END_SYSEX)
    >>> dcmd = Command('\x01\x01', 'dummy', (),(BYTE,))
    >>> reply = Reply(''.join(bytes), dcmd) 
    >>> reply.parse()
    1

    >>> dcmd.reply_spec = (WORD, BYTE, BYTE, BYTE, BYTE, STRING)
    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20\x05', '\x00','\x02\x01\x02', '\x00', '\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b', '\x00', END_SYSEX)
    >>> reply = Reply(''.join(bytes), dcmd) 
    >>> reply.parse() 
    (256, 1, 2, 0, 1, 'Z48 & MPC4K')

    # Future: should raise unknown disk error 
    >>> dcmd.reply_spec = ()
    >>> bytes = '\xf0G_\x00E \x00\x00\x03\xf7'
    >>> reply = Reply(bytes, dcmd) 
    >>> reply.parse() 
    Traceback (most recent call last):
    Exception: System exclusive error, code 180, message: Unknown disk error

    # using pad type if we encounter bytes not according to specification
    >>> dcmd.reply_spec = (PAD, WORD)
    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20\x10', '\x02', '\x15', '\x00', '\xf7')
    >>> reply = Reply(''.join(bytes), dcmd) 
    >>> reply.parse() 
    21

    # not possible yet how to deal with the dump request replies
    >>> dcmd.reply_spec = ()
    >>> reply = Reply('\xf0G_ ' + '\x00' * 2 + 'R\x10 i\x01\xf7', dcmd) 
    >>> reply.parse() 
    Traceback (most recent call last):
        ParseException("Unknown reply type: %02x" % struct.unpack('B', reply_id))
    ParseException: Unknown reply type: 00

    # reply on 'bulk command 10 05' 10 0a 00 f0 47 5e 20 00 00 10 05 15 f7
    # popped 2 0 bytes after header 5f  and here we discover how ak.sys gets its disk list! (but what about the 15? arg checksum?)
    >>> dcmd.reply_spec = (WORD, BYTE, BYTE, BYTE, BYTE, STRING)
    >>> bytes = '\xf0\x47\x5f\x00\x52\x10\x05\x00\x02\x01\x02\x00\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b\x00\xf7'
    >>> reply = Reply(bytes, dcmd) 
    >>> reply.parse() 
    (256, 1, 2, 0, 1, 'Z48 & MPC4K')

    >>> bytes = '\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x20\x53\x74\x72\x69\x6e\x67\x20\x41\x32\x2e\x77\x61\x76\x00\xf7'
    >>> dcmd.reply_spec = (STRING,)
    >>> reply = Reply(bytes, dcmd) 
    >>> reply.parse() 
    'Mell String A2.wav'

    >>> bytes = '\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x6f\x74\x72\x6f\x6e\x20\x53\x74\x72\x69\x6e\x67\x73\x2e\x61\x6b\x70\x00\xf7'
    >>> dcmd.reply_spec = (STRING,)
    >>> reply = Reply(bytes, dcmd) 
    >>> reply.parse() 
    'Mellotron Strings.akp'

    >>> bytes = '\xf0\x47\x5f\x00\x52\x07\x01\x08\x5a\x38\x20\x53\x61\x6d\x70\x6c\x65\x72\x00\xf7'
    >>> dcmd.reply_spec = (PAD, STRING,)
    >>> reply = Reply(bytes, dcmd) 
    >>> reply.parse() 
    'Z8 Sampler'

    """
    def __init__(self, bytes, command, z48id=None, userref=None):
        self.bytes = bytes
        self.command = command
        self.z48id = z48id
        self.userref = userref

    def parse(self):
        """ Parses the command sequence
        """

        if self.bytes[0] != START_SYSEX or self.bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")

        # TODO: dispatching on z48id, userref and command
        i = 2   # skip start sysex, vendor id
        if self.userref is not None:
            i += len(self.z48id)
        else:
            i += 1

        i += 1 # userref 
        reply_id = self.bytes[i]

        i +=  1 # skip past the reply
        i += len(self.command.id) # skip past the command id (section, item)
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

        return self.parse_untyped_bytes(self.bytes, i)

    def parse_untyped_bytes(self, bytes, offset):
        """Parses a byte string without type information
        """
        result = []
        for type in self.command.reply_spec:
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

class StringArrayType(object):
    """
    """
    def encode(self, value):
        raise NotImplementedError()

    def decode(self, string):    
        r"""
        >>> s = StringArrayType()
        >>> s.decode('test sdf\x00test ghi\x00')
        ['test sdf', 'test ghi']
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

    def encode(self, value):
        return super(SoundLevelType, self).encode(int(value*10))

    def decode(self, string):
        """XXX: reconsider conversion here
        """
        return super(SoundLevelType, self).decode(string)/10.0

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


TWO_BYTES   = SysexType(2, False, '\x0a')
THREE_BYTES = SysexType(3, False, '\x0b')

# aksy type extensions
PAD         = PadType()
BOOL        = BoolType()
CENTS       = '\x23' # SWORD(+- 3600)
PAN         = PanningType()
LEVEL       = SoundLevelType() 

class HandleNameArrayType(object):
    r"""Mixed data type, wrapping handle(DoubleWord) and name (StringType)
    >>> handle_name_type = HandleNameArrayType() 
    >>> handle_name_type.decode('\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
    (174194692, 'SynthTest')
    """
    def encode(self, value):
        raise NotImplementedError

    def decode(self, string):
        return  (DWORD.decode(string[:4]),
                STRING.decode(string[3:]),)

HANDLESNAMES  = HandleNameArrayType()

def parse_byte_string(data, type, offset=0):
    r""" Parses a byte string

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, STRING)
    ('TEST', 5)

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, STRING, 1)
    ('EST', 4)

    >>> parse_byte_string('\x54\x45\x53\x54\x00\x54\x45\x53\x54\x00', STRING, 0)
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
