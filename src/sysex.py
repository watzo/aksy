import struct, sys 

class Command:
    """ 
        Represents a system exclusive command.

    """

    def __init__(self, section_id, id, name, arg_types, reply_spec=None):
        self.section_id = section_id
        self.id = id
        self.name = name
        self.arg_types = []
        self.reply_spec = reply_spec

        for arg_type in arg_types:
            if arg_type is not None:
                self.arg_types.append(arg_type)

    def create_arg_bytes(self, args):
        """ Returns the sysex byte sequence for the command arg data -
            
        """
        bytes = []
        for type,arg in zip(self.arg_types, args):
            bytes.append(_to_byte_string(type, arg))

        if len(bytes) == 0:
            return None
        else:
            return bytes

class Request:
    """ Encapsulates a sysex request

    Select disk:
    >>> arg = 256 
    >>> command = Command('\x20', '\x02', 'select_disk', (WORD,None), ()) 
    >>> Request(command, (arg,))
    ['f0', '47', '5f', '00', '20', '02', '00', '02', 'f7']

    Select root folder:
    >>> folder = ''
    >>> command = Command('\x20', '\x13', 'set_curr_folder', (STRING,None), ()) 
    >>> Request(command, (folder,))
    ['f0', '47', '5f', '00', '20', '13', '00', 'f7']

    Select autoload folder:
    >>> folder = 'autoload'
    >>> command = Command('\x20', '\x13', 'set_curr_folder', (STRING,None), ()) 
    >>> Request(command, (folder,))
    ['f0', '47', '5f', '00', '20', '13', '61', '75', '74', '6f', '6c', '6f', '61', '64', '00', 'f7']

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

        bytes.append(command.section_id) 
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

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20','\x05', BYTE, '\x01', END_SYSEX)
    >>> reply = Reply(''.join(bytes)) 
    >>> reply.parse()
    1

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20','\x05', '\x01', END_SYSEX)
    >>> reply = Reply(''.join(bytes), (BYTE)) 
    >>> reply.parse()
    1

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20\x05', '\x00','\x02\x01\x02', '\x00', '\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b', '\x00', END_SYSEX)
    >>> reply = Reply(''.join(bytes), (WORD, BYTE, BYTE, BYTE, BYTE, STRING)) 
    >>> reply.parse() 
    (256, 1, 2, 0, 1, 'Z48 & MPC4K')

    # Future: should raise unknown disk error 
    >>> bytes = '\xf0G_\x00E \x00\x00\x03\xf7'
    >>> reply = Reply(bytes,()) 
    >>> reply.parse() 
    Traceback (most recent call last):
        raise Exception("System exclusive error, code %2x, message %s" % (code, errors[code])
    Exception: System exclusive error, code 180, message: Unknown disk error

    # using pad type if we encounter bytes not according to specification
    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20', '\x10', '\x02', '\x15', '\x00', '\xf7')
    >>> reply = Reply(''.join(bytes),(PAD, WORD)) 
    >>> reply.parse() 
    21

    # not possible yet how to deal with the dump request replies
    >>> reply = Reply('\xf0G_ ' + '\x00' * 2 + 'R\x10 i\x01\xf7',()) 
    >>> reply.parse() 
    Traceback (most recent call last):
        ParseException("Unknown reply type: %02x" % struct.unpack('B', reply_id))
    ParseException: Unknown reply type: 00

    # reply on 'bulk command 10 05' 10 0a 00 f0 47 5e 20 00 00 10 05 15 f7
    # popped 2 0 bytes after header 5f  and here we discover how ak.sys gets its disk list! (but what about the 15? arg checksum?)
    >>> bytes = _transform_hexstring('f0 47 5f 00 52 10 05 00 02 01 02 00 01 5a 34 38 20 26 20 4d 50 43 34 4b 00 f7')
    >>> reply = Reply(bytes, (WORD, BYTE, BYTE, BYTE, BYTE, STRING)) 
    >>> reply.parse() 
    (256, 1, 2, 0, 1, 'Z48 & MPC4K')

    # select_disk 10 0c 00 f0 47 5e 20 00 00 10 02 00 02 14 f7
    # 10 0a 00 f0 47 5e 20 00 00 10 10 20 f7
    # f0 47 5f 20 00 00 52 10 10 15 00 f7
    # 10 0a 00 f0 47 5e 20 00 00 10 12 22 f7
    >>> bytes = _transform_hexstring( 'f0 47 5f 00 52 10 22 4d 65 6c 6c 20 53 74 72 69 6e 67 20 41 32 2e 77 61 76 00 f7')
    >>> reply = Reply(bytes, (STRING,)) 
    >>> reply.parse() 
    'Mell String A2.wav'

    >>> bytes = _transform_hexstring( 'f0 47 5f 00 52 10 22 4d 65 6c 6c 6f 74 72 6f 6e 20 53 74 72 69 6e 67 73 2e 61 6b 70 00 f7')
    >>> reply = Reply(bytes, (STRING,)) 
    >>> reply.parse() 
    'Mellotron Strings.akp'
    """
    def __init__(self, bytes, reply_spec=(), z48id=None, userref=None):
        self.bytes = bytes
        self.reply_spec = reply_spec
        self.z48id = z48id
        self.userref = userref

    def parse(self):
        """ Parses the command sequence
        """

        if self.bytes[0] != START_SYSEX or self.bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")

        # TODO: dispatching on z48id, userref and command
        i = 2   # skip start sysex, vendor id
        if self.z48id is not None:
            i += len(self.z48id)
        else:
            i += 1

        i += 1 # userref 
        reply_id = self.bytes[i]

        i +=  3 # skip past the reply, section and command
        if reply_id == REPLY_ID_OK:
            return None 
        elif reply_id == REPLY_ID_DONE:
            return None 
        elif reply_id == REPLY_ID_ERROR: 
            b1, b2 = struct.unpack('2B', self.bytes[i:i+2])
            code = (b2 << 7) + b1

            raise Exception("System exclusive error, code %02x, message: %s " % (code, errors[code]))
        elif reply_id == REPLY_ID_REPLY:
            # continue
            pass
        else:
            raise ParseException("Unknown reply type: %02x" % struct.unpack('b', reply_id))


        if len(self.reply_spec) > 0:
            return self.parse_untyped_bytes(self.bytes, i)
        else:
            return self.parse_typed_bytes(self.bytes, i)

    def parse_typed_bytes(self, bytes, offset):
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
            part, len_parsed = parse_byte_string(bytes, offset, type) 
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

# Sysex type ids
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
REPLY_ID_ERROR = '\x45'

# aksy type extensions
PAD         = '\x21' # unspecified return code
BOOL        = '\x22' # BYTE(0,1)
CENTS       = '\x22' # SWORD(+- 3600)

def _to_byte_string(src_type, value):
    r"""

    TODO: raise value errors if value out of range 
    >>> _to_byte_string(WORD, 256)
    '\x00\x02'

    >>> _to_byte_string(BYTE, 128)
    Traceback (most recent call last):
        if value > 127: raise ValueError
    ValueError

    >>> _to_byte_string(BOOL, False)
    '\x00'
    >>> _to_byte_string(STRING, '')
    '\x00'
    >>> _to_byte_string(STRING, 'test')
    'test\x00'
    >>> _to_byte_string(STRING, 'test sdf')
    'test sdf\x00'
    """
    if (src_type == BOOL):
        value = int(value)
        byte_string = struct.pack('B', value)
    elif (src_type == BYTE):
        if value > 127: raise ValueError
        byte_string = struct.pack('B', value)
    elif (src_type == SBYTE):
        if value > 127 or value < -127: raise ValueError

        # FIXME: sign byte
        byte_string = struct.pack('B', value)
    elif (src_type == WORD):
        if value > 16383: raise ValueError
        byte_string = struct.pack('2B', value & 0x0f, value >> 7)
    elif (src_type == STRING):
        if not type(value) == type('') and value != '':
            raise ValueError("Value %s should be a (non unicode) string." % (value))
        else:
            # note: string length+1 to automagically add the string terminator
            byte_string = struct.pack(str(len(value)+1) + 's', value) 
    else: 
        raise ValueError("unsupported type %s" % repr(src_type))

    return byte_string

def parse_byte_string(data, offset=0, type=None):
    r""" Parses a byte string

    >>> parse_byte_string(STRING + '\x54\x45\x53\x54' + STRING_TERMINATOR)
    ('TEST', 6)

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR, 0, STRING)
    ('TEST', 5)

    >>> parse_byte_string('\x54\x45\x53\x54' + STRING_TERMINATOR + '\x54\x45\x53\x54' + STRING_TERMINATOR, 0, STRING)
    (('TEST', 'TEST'), 10)

    Type info in the data: 
    >>> parse_byte_string(BYTE + '\x0f')
    (15, 2)

    No type info in the data: 
    >>> parse_byte_string('\x0f', 0, BYTE)
    (15, 1)

    >>> parse_byte_string(SBYTE + '\x01\x0f')
    (-15, 3)

    XXX: this is probably not correct
    >>> parse_byte_string(WORD + '\x00\x03')
    (384, 3)

    >>> parse_byte_string(SWORD + '\x01\x0f\x0f')
    (-1935, 4)

    >>> parse_byte_string(DWORD + '\x01\x01\x01\x0f')
    (251724033L, 5)

    >>> parse_byte_string(SDWORD + '\x01\x01\x01\x0f\x0f')
    (-252641537L, 6)

    >>> parse_byte_string(BOOL + '\x00')
    (False, 2)

    >>> parse_byte_string(BOOL + '\x01')
    (True, 2)

    """

    len_parsed_data = 0

    if type == None:
        type = data[offset]
        offset += 1
        len_parsed_data += 1 
    if (type == PAD):
        return (None, 1)
    if (type == BYTE ):
        result = struct.unpack('B', data[offset])[0]
        len_parsed_data += 1

    elif (type == BOOL):
        result = bool(struct.unpack('B', data[offset])[0])
        len_parsed_data += 1

    elif (type == SBYTE):
        result = struct.unpack('B', data[offset+1])[0]

        if data[offset] == NEGATIVE:
            result *= -1 
         
        len_parsed_data += 2;

    elif (type == WORD or type == TWO_BYTES):
        b1, b2 = struct.unpack('2B', data[offset:offset+2])
        result = (b2 << 7) + b1
        len_parsed_data += 2;

    elif (type == SWORD):
        b1, b2 = struct.unpack('2B', data[offset+1:offset+3])
        result = (b1 << 7) + b2
        
        if data[offset] == NEGATIVE:
            result *= -1 

        len_parsed_data += 3;
    elif (type == DWORD):
        result = struct.unpack('<I', data[offset:offset+4])[0]
        len_parsed_data += 4;

    elif (type == SDWORD):
        result = struct.unpack('<I', data[offset+1:offset+5])[0]

        if data[offset+1] == NEGATIVE:
            result *= -1 

        len_parsed_data += 5;
    elif (type == STRING):
        index = 0
        strings = []
        for char in data[offset:]:
            #sys.stderr.writelines( "c:%s i:%s\n" % (char, index) )
            if (char == END_SYSEX):
                break;
            if char == STRING_TERMINATOR:
                strings.append(struct.unpack( str(index) + 's', data[offset:offset+index])[0])
                offset += index + 1
                index = 0
            else:
                index += 1

        for string in strings:
            len_parsed_data += (len(string) + 1)

        if len(strings) == 0:
            result = None
        else:
            result = len(strings) > 1 and tuple(strings) or strings[0]
    else: 
        raise ValueError("unsupported type %s" % repr(type))
        
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
