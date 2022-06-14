from unittest import TestCase, TestLoader
from aksyosc import connector
from aksy.device import Devices
from aksyosc.osc import decodeOSC

MOCK_SAMPLER = Devices.get_instance('mock_z48', 'mock')
CMDS = [MOCK_SAMPLER.sampletools.get_bit_depth_cmd]

class OSCConnectorTest(TestCase):
    def test_creat_alt_req_msg(self):
        msg = connector.OSCConnector.create_alt_req_msg(1, CMDS, (), None)
        expected = '#bundle\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18/altoperations\x00\x00,iN\x00\x00\x00\x00\x01\x00\x00\x00 /sampletools/get_bit_depth\x00\x00,\x00\x00\x00'
        self.assertEqual(str(expected), str(msg))

    def test_parse_alt_req_msg(self):
        msg = connector.OSCConnector.create_alt_req_msg(1, CMDS, (), None)
        self.assertEqual(['#bundle', 0, ['/altoperations', ',iN', 1, None],
                          ['/sampletools/get_bit_depth', ',']], decodeOSC(msg))
            
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('tests.aksyosc.tests.test_connector')

