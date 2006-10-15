import struct, sys, unittest, logging, os

from aksy.devices.akai import sysex, sysex_types, sampler
from aksy.devices.akai.z48 import sampler

log = logging.getLogger("aksy")
z48 = sampler.Z48()

class TestUserRef(unittest.TestCase):
    def testEncodeDecode(self):
        cmd = sysex.Command(sysex.Z48_ID, '\x20\x04', 'get_no_disks', (), (sysex_types.TYPEBYTE, sysex_types.BYTE,),
            userref_type=sysex_types.USERREF)
        request = sysex.Request(cmd, (), 0)
        bytes = z48._execute(request.get_bytes())
        length, request_id = sysex_types.USERREF.decode(bytes[3:])

        self.assertEquals(0, request_id)

        cmd = sysex.Command(sysex.S56K_ID, '\x10\x04', 'get_no_disks', (), (sysex_types.BYTE,),
            userref_type=sysex_types.S56K_USERREF)
        request = sysex.Request(cmd, (), 16000)

        bytes = z48._execute(request.get_bytes())
        length, request_id = sysex_types.USERREF.decode(bytes[3:])

        self.assertEquals(3, length)
        self.assertEquals(16000, request_id)

        cmd = sysex.Command(sysex.Z48_ID, '\x20\x04', 'get_no_disks', (), (sysex_types.TYPEBYTE, sysex_types.BYTE,),
            userref_type=sysex_types.Z48USERREF)

        request = sysex.Request(cmd, (), 126)
        bytes = z48._execute(request.get_bytes())
        result = sysex.Reply(bytes, cmd)
        request_id = result.get_request_id()
        self.assertEquals(126, request_id)

        request = sysex.Request(cmd, (), 16000)
        bytes = z48._execute(request.get_bytes())
        result = sysex.Reply(bytes, cmd)
        request_id = result.get_request_id()
        self.assertEquals(16000, request_id)

def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('aksy.devices.akai.z48.ftests.test_sysex_integ')
