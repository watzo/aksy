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

    # select disk:
    >>> arg = 512 
    >>> command = Command('\x20', '\x02', 'select_disk', (WORD,None), ()) 
    >>> Request(command, (arg,))
    ['f0', '47', '5f', '00', '20', '02', '00', '02', 'f7']

    # select root folder:
    >>> folder = ''
    >>> command = Command('\x20', '\x13', 'set_curr_folder', (STRING,None), ()) 
    >>> Request(command, (folder,))
    ['f0', '47', '5f', '00', '20', '13', '00', 'f7']

    # select autoload folder:
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
    """ Encapsulates a sysex reply

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20','\x05', BYTE, '\x01', END_SYSEX)
    >>> reply = Reply(''.join(bytes)) 
    >>> reply.parse()
    1

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20','\x05', '\x01', END_SYSEX)
    >>> reply = Reply(''.join(bytes), (BYTE)) 
    >>> reply.parse()
    1

    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY,\
    '\x20\x05', ZERO,'\x02\x01\x02', ZERO, '\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b', ZERO, END_SYSEX)
    >>> reply = Reply(''.join(bytes), (WORD, BYTE, BYTE, BYTE, BYTE, STRING)) 
    >>> reply.parse() 
    [512, 1, 2, 0, 1, 'Z48 & MPC4K']

    # Future: should raise unknown disk error 
    >>> bytes = '\xf0G_' + ZERO + 'E \x02\x03' + ZERO + '\xf7'
    >>> reply = Reply(bytes,()) 
    >>> reply.parse() 
    Traceback (most recent call last):
        raise Exception("System exclusive error, code %02x" % code)
    Exception: System exclusive error, code 180

    # using pad type if we encounter bytes not according to specification
    >>> bytes =  (START_SYSEX, AKAI_ID, Z48_ID, DEFAULT_USERREF, REPLY_ID_REPLY, '\x20', '\x10', '\x02', '\x15', ZERO, '\xf7')
    >>> reply = Reply(''.join(bytes),(PAD, WORD)) 
    >>> reply.parse() 
    21

    # not possible yet how to deal with the dump request replies
    >>> reply = Reply('\xf0G_ ' + ZERO * 2 + 'R\x10 i\x01\xf7',()) 
    >>> reply.parse() 
    Traceback (most recent call last):
        ParseException("Unknown reply type: %02x" % struct.unpack('B', reply_id))
    ParseException: Unknown reply type: 00

    # reply on 'bulk command 10 05' 10 0a 00 f0 47 5e 20 00 00 10 05 15 f7
    # popped 2 0 bytes after header 5f  and here we discover how ak.sys gets its disk list! (but what about the 15? arg checksum?)
    >>> bytes = _transform_hexstring('f0 47 5f 00 52 10 05 00 02 01 02 00 01 5a 34 38 20 26 20 4d 50 43 34 4b 00 f7')
    >>> reply = Reply(bytes, (WORD, BYTE, BYTE, BYTE, BYTE, STRING)) 
    >>> reply.parse() 
    [512, 1, 2, 0, 1, 'Z48 & MPC4K']

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
            codes = struct.unpack('2b', self.bytes[i:i+2])
            code = 128 * codes[0] + codes[1]
            raise Exception("System exclusive error, code %02x" % code)
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
            return result

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
ZERO        = '\x00'
PAD         = '\x21' # unspecified return code

def _to_byte_string(src_type, value):
    """
    doc-tests don't handle x-escaped values too well, so we unwrap the encoded
    value again:

    TODO: raise value errors if value out of range 
    >>> struct.unpack('2b', _to_byte_string(WORD, 512))
    (0, 2)

    >>> # _to_byte_string(STRING, '')
    '\x00'
    >>> _to_byte_string(STRING, 'test')
    >>> _to_byte_string(STRING, 'test sdf')
    """
    if (src_type == BYTE or src_type == ZERO):
       byte_string = struct.pack('<b', value)
    elif (src_type == SBYTE):
       byte_string = struct.pack('<b', value)
    elif (src_type == WORD):
       byte_string = struct.pack('<H', value)
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
    """ Parses a byte string

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

    >>> parse_byte_string(WORD + _transform_hexstring('15 00'))
    (21, 3)

    >>> parse_byte_string(SWORD + '\x01\x0f\x0f')
    (-3855, 4)

    >>> parse_byte_string(DWORD + '\x01\x01\x01\x0f')
    (251724033L, 5)

    >>> parse_byte_string(SDWORD + '\x01\x01\x01\x0f\x0f')
    (-252641537L, 6)
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

    elif (type == SBYTE):
        result = struct.unpack('B', data[offset+1])[0]

        if data[offset] == NEGATIVE:
            result *= -1 
         
        len_parsed_data += 2;

    elif (type == WORD or type == TWO_BYTES):
        result = struct.unpack('<H', data[offset:offset+2])[0]
        len_parsed_data += 2;

    elif (type == SWORD):
        result = struct.unpack('<H', data[offset+1:offset+3])[0]

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
    
if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
