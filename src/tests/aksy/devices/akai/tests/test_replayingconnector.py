from tests.aksy.devices.akai import replayingconnector
from tests.aksy.util import testutil
import unittest

REQ = "['f0', '47', '5f', '00', '60', '03', '00', '00', '04', '00', '00', '00', '50', 'f7']"
RESP = "['f0', '47', '5f', '00', '45', '60', '00', '00', '00', 'f7']"

def create_bytes(str_repr):
    return replayingconnector.encode(eval(str_repr))

class Request:
    def __init__(self, byte_str):
        self.bytes = replayingconnector.encode(eval(byte_str))
    def get_bytes(self):
        return self.bytes
    
class TestReplayingConnector(unittest.TestCase):
    def testEncode(self):
        self.assertEqual('\xf0G_\x00E`\x00\x00\x00\xf7', replayingconnector.encode(eval(RESP)))

    def testParse(self):
        f = testutil.get_test_resource('aksy_20070624.log')
        conn = replayingconnector.ReplayingConnector('z48', f)
        self.assertEqual(create_bytes("['f0', '47', '5f', '00', '44', '00', '01', 'f7']"), 
                          conn.requests[create_bytes(" ['f0', '47', '5f', '00', '00', '01', '00', 'f7']")])
        self.assertEqual(create_bytes(RESP), 
                          conn.requests[create_bytes(REQ)])
        
        self.assertEqual(34, len(conn.requests))
    
    def testExecuteRequest(self):
        f = testutil.get_test_resource('aksy_20070624.log')
        conn = replayingconnector.ReplayingConnector('z48', f)
        conn.execute_request(Request(REQ))
    
def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('tests.aksy.devices.akai.tests.test_replayingconnector')
