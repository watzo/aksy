import struct, logging, errno
from aksy.devices.akai import sysex_types, base
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
    def __init__(self, device_id, cmd_id, name, arg_types,
            reply_spec, userref_type=sysex_types.USERREF):
        self.device_id = device_id
        self.id = cmd_id
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
        bytes = self._create_start_bytes(command, request_id)
        bytes.append(command.id)
        data = command.create_arg_bytes(args)
        if data is not None:
            bytes.extend(data)
        bytes.append(END_SYSEX)

        self.bytes = ''.join(bytes)

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
    def __init__(self, section_id, handle, commands, args, base_section_id, index=None, request_id=0):
        bytes = self._create_start_bytes(commands[0], request_id)
        bytes.append(section_id)
        # TODO: this is z48 specific
        bytes.append(self.calc_offset(base_section_id, commands[0].id))
        bytes.append(sysex_types.DWORD.encode(handle))
        if index is not None:
            bytes.append(sysex_types.BYTE.encode(index))
        
        for command in commands:
            data = command.create_arg_bytes(args)
            if data is not None:
                # TODO: this is z48 specific
                bytes.append(sysex_types.BYTE.encode(len(data)))
                bytes.extend(data)
            else:
                bytes.append(sysex_types.BYTE.encode(0))
            bytes.append(command.id[1:])
                     
        bytes.append(END_SYSEX)
        self.bytes = ''.join(bytes)
        
    def calc_offset(self, base_section_id, command_id):
        base_section_id = sysex_types.BYTE.decode(base_section_id, False)
        section_id = sysex_types.BYTE.decode(command_id[:1], False)
        section_offset = section_id - base_section_id
        if section_offset > 3:
            raise base.SamplerException("Offset should be between 0 and 3")
        return sysex_types.BYTE.encode(section_offset)
    
class Reply:
    """ Encapsulates a sysex reply
    """
    def __init__(self, bytes, command):
        self.bytes = bytes
        self.command = command
        self.request_id  = 0
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

        if self.command.id[:2] != command:
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
        
    return base.SamplerException(msg, code)

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
