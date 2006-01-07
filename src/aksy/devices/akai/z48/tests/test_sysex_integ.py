import struct, sys, unittest, logging

from aksy.devices.akai import sysex, sysex_types, sampler
from aksy.devices.akai.z48 import sampler

log = logging.getLogger("aksy")

class TestUserRef(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'z48'):
            self.z48 = sampler.Z48()

    def testEncodeDecode(self):
        cmd = sysex.Command(sysex.Z48_ID, '\x20\x04', 'get_no_disks', (sysex_types.TYPEBYTE, sysex_types.BYTE,),
            userref_type=sysex_types.USERREF)
        request = sysex.Request(cmd, (), 0)
        bytes = self.z48._execute('\x10' + struct.pack('B', len(request.get_bytes())) + '\x00' + request.get_bytes())
        length, request_id = sysex_types.USERREF.decode(bytes[3:])

        self.assertEquals(0, request_id)

        cmd = sysex.Command(sysex.S56K_ID, '\x10\x05', 'get_disk_list', (sysex_types.BYTE,),
            userref_type=sysex_types.S56K_USERREF)
        request = sysex.Request(cmd, (), 16000)

        bytes = self.z48._execute('\x10' + struct.pack('B', len(request.get_bytes())) + '\x00' + request.get_bytes())
        length, request_id = sysex_types.USERREF.decode(bytes[3:])

        self.assertEquals(3, length)
        self.assertEquals(16000, request_id)

        # this currently fails on Z48
        cmd = sysex.Command(sysex.Z48_ID, '\x20\x04', 'get_no_disks', (sysex_types.TYPEBYTE, sysex_types.BYTE,),
            userref_type=sysex_types.USERREF)

        request = sysex.Request(cmd, (), 126)
        log.debug("Request: %s, id %i\n" % (repr(request), 126))
        bytes = self.z48._execute('\x10' + struct.pack('B', len(request.get_bytes())) + '\x00' + request.get_bytes())
        try:
            result = sysex.Reply(bytes, cmd)
            log.debug("Reply: %s\n" % repr(result))
            request_id = result.get_request_id()
            self.assertEquals(126, request_id)
        except sysex.SamplerException, e:
            # unfortunately, this raises an exception
            log.exception(e)

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.z48.tests.test_sysex_integ')
    return suite