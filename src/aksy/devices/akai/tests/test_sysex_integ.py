import struct, sys, unittest
from aksy.devices.akai import sysex, sysex_types, sampler

class TestUserRef(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'z48'):
            self.z48 = sampler.Sampler()
            self.z48.init()

    def testEncodeDecode(self):
        cmd = sysex.Command(sysex.Z48_ID, '\x20\x04', 'get_no_disks', (sysex_types.PAD, sysex_types.BYTE,),
            userref_type=sysex_types.USERREF)
        self.z48.execute(cmd, (), 0)

        # this fails on Z48
        cmd = sysex.Command(sysex.Z48_ID, '\x20\x04', 'get_no_disks', (sysex_types.PAD, sysex_types.BYTE,),
            userref_type=sysex_types.USERREF)
        self.z48.execute(cmd, (), 300)

        cmd = sysex.Command(sysex.S56K_ID, '\x10\x05', 'get_no_disks', (sysex_types.BYTE,),
            userref_type=sysex_types.S56K_USERREF)
        self.z48.execute(cmd, (), 300)


    def tearDown(self):
        self.z48.close()

    def __del__(self):
        try:
            pass # self.z48.close()
        except Exception, e:
            print e


def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.tests.test_sysex_integ')
    return suite
