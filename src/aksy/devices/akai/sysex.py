import struct, logging, errno
from aksy.devices.akai import sysex_types, model
from aksy.devices.akai.sysex_types import START_SYSEX, END_SYSEX

AKAI_ID = '\x47'
Z48_ID = '\x5f'
S56K_ID = '\x5e'

REPLY_ID_OK = '\x4f'
REPLY_ID_DONE = '\x44'
REPLY_ID_REPLY = '\x52'
REPLY_ID_ERROR = '\x45'

log = logging.getLogger("aksy")

class Command:
    """Represents a system exclusive command.
    """
    def __init__(self, device_id, cmd_id, section, name, arg_types,
            reply_spec, userref_type=sysex_types.USERREF):
        self.device_id = device_id
        self.id = cmd_id
        self.section = section
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
        for sysex_type, arg in zip(self.arg_types, args):
            bytes.append(sysex_type.encode(arg))

        if len(bytes) == 0:
            return None
        else:
            return bytes

class Request:
    """ Encapsulates a sysex request
    command: the command to execute
    """
    def __init__(self, command, args, request_id=0):
        self.command = command
        self.args = args
        self.bytes = self._create_bytes(command, args, request_id)
        
    def _create_bytes(self, command, args, request_id):
        bytes = self._create_start_bytes(command, request_id)
        bytes.append(command.id)
        data = command.create_arg_bytes(args)
        if data is not None:
            bytes.extend(data)
        bytes.append(END_SYSEX)

        return ''.join(bytes)

    def _create_start_bytes(self, command, request_id):
        bytes = [START_SYSEX, AKAI_ID]
        bytes.append(command.device_id)
        bytes.append(command.userref_type.encode(request_id))
        return bytes
        
    def get_bytes(self):
        return self.bytes
    
    def __repr__(self):
        return repr([ "%02x" %byte for byte in struct.unpack(str(len(self.bytes)) + 'B', 
                                                             self.bytes)])
class AlternativeRequest(Request):
    SECTION_SAMPLE = '\x60'
    SECTION_KEYGROUP = '\x61'
    SECTION_PROGRAM = '\x62'
    SECTION_MULTI = '\x63'
    SECTION_MULTIFX = '\x64'
    SECTION_SONG = '\x65'

    BASE_SECTION_SAMPLE = '\x1c'
    BASE_SECTION_KEYGROUP = '\x0c'
    BASE_SECTION_PROGRAM = '\x14'
    BASE_SECTION_MULTI = '\x18'
    BASE_SECTION_MULTIFX = '\x25'
    BASE_SECTION_SONG = '\x28'

    BASE_ALT_SECTION_MAP = {
        BASE_SECTION_SAMPLE : SECTION_SAMPLE,
        BASE_SECTION_KEYGROUP : SECTION_KEYGROUP,
        BASE_SECTION_PROGRAM : SECTION_PROGRAM,
        BASE_SECTION_MULTI : SECTION_MULTI,
        BASE_SECTION_MULTIFX : SECTION_MULTIFX,
        BASE_SECTION_SONG : SECTION_SONG
    }

    def __init__(self, handle, commands, args, index=None, request_id=0):
        bytes = self._create_start_bytes(commands[0], request_id)
        no_sections = index is None and 4 or 8
        # TODO: this is z48 specific
        alt_section_id, offset = self.find_section_ids(commands[0].id, no_sections)
        bytes.append(alt_section_id)
        bytes.append(offset)
        bytes.append(sysex_types.DWORD.encode(handle))
        if index is not None:
            bytes.append(sysex_types.BYTE.encode(index))
            
        for i, command in enumerate(commands):
            if len(command.arg_types) > 0:
                data = ''.join(command.create_arg_bytes(args[i]))
                bytes.append(sysex_types.BYTE.encode(len(data) + 1))
            else:
                data = []
                bytes.append(sysex_types.BYTE.encode(1))

            bytes.append(command.id[1])
            bytes.extend(data)
        
                 
        bytes.append(END_SYSEX)
        self.bytes = ''.join(bytes)
        
    def find_section_ids(self, command_id, no_sections):
        section_id = sysex_types.BYTE.decode(command_id[:1], False)
        for i in range(no_sections):
            base_section =  sysex_types.BYTE.encode(section_id - i)
            alt_section = self.BASE_ALT_SECTION_MAP.get(base_section, None) 
            if alt_section is not None:
                return alt_section, sysex_types.BYTE.encode(i)
        
        raise model.SamplerException("No alternative operations defined for %s" % 
                                    repr(command_id[:1]))
        
    
class Reply:
    """ Encapsulates a sysex reply
    """
    def __init__(self, bytes, command, alt_request=False):
        self.bytes = bytes
        self.command = command
        self.request_id  = 0
        self.alt_request = alt_request
        self.return_value = self._parse()

    def get_request_id(self):
        return self.request_id

    def get_return_value(self):
        return self.return_value

    def _parse(self):
        """ Parses the command sequence
        """

        if self.bytes[0] != START_SYSEX or self.bytes[-1] != END_SYSEX:
            raise ParseException("Invalid system exclusive string received")
        # keep alive message
        if len(self.bytes) == 2:
            return None
        # TODO: dispatching on z48id, userref and command
        i = 2   # skip start sysex, vendor id
        i += len(self.command.device_id)
        len_userref, self.request_id = self.command.userref_type.decode(self.bytes[i:])
        i += len_userref
        reply_id = self.bytes[i]
        i +=  1 # skip past the reply code
        command = self.bytes[i:i+2]
        i += len(self.command.id) # skip past the command id (section, item, optional subcmd)
        if reply_id == REPLY_ID_OK:
            return None
        elif reply_id == REPLY_ID_DONE:
            return None
        elif reply_id == REPLY_ID_ERROR:
            byte1, byte2 = struct.unpack('2B', self.bytes[i:i+2])
            code = (byte2 << 7) + byte1
            raise _create_exception(
                errors.get(code, "Unknown"), code)
        elif reply_id == REPLY_ID_REPLY:
            # continue
            pass
        else:
            raise ParseException("Unknown reply type: %02x" % struct.unpack('b', reply_id))

        if not self.alt_request and self.command.id[:2] != command:
            raise ParseException(
                'Parsing the wrong reply for command %02x %02x'
                    % struct.unpack('2B', self.command.id[:2]))
        if self.command.reply_spec is None:
            return sysex_types.TYPED_COMPOSITE.decode(self.bytes[i:])[1]
        else:
            return sysex_types.CompositeType(self.command.reply_spec).decode(self.bytes[i:])[1]

class ParseException(Exception):
    """ Exception raised when parsing system exclusive fails
    """
    pass

def byte_repr(bytes):
    return repr([ "%02x" %byte for byte in struct.unpack(str(len(bytes)) + 'B', bytes)])

def repr_bytes(bytes):
    return  ''.join([struct.pack('1B', int(byte, 16)) for byte in bytes])

def _to_string(ordvalues):
    """Method to quickly convert to a string
    >>> ordvalues = (90, 52, 56, 32, 38, 32, 77, 80, 67, 52, 75)
    >>> _to_string(ordvalues)
    'Z48 & MPC4K'
    """
    return ''.join([chr(value) for value in ordvalues])

def _create_exception(msg, code):
    if code == 0x101 or code == 0x203:
        return IOError(errno.ENOENT, msg)
    if code == 0x0:
        return NotImplementedError(msg)
        
    return model.SamplerException(msg, code)

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
    0x202:"WAV format is incorrect",
    0x203:"File not found",
    0x204:"File already exists",
}
