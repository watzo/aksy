from unittest import TestCase, TestLoader
from aksyosc.osc import decodeOSC, OSCMessage, OSCException

class OSCMessageTest(TestCase):
    def testAppendLong(self):
        m = OSCMessage()
        m.append(1L)
        self.assertEquals(['', ',h', 1L], decodeOSC(m.getBinary()))

    def testEncodeDecodeTrue(self):
        m = OSCMessage()
        m.append(True)
        self.assertEquals(['', ',T', True], decodeOSC(m.getBinary()))

    def testEncodeDecodeFalse(self):
        m = OSCMessage()
        m.append(False)
        self.assertEquals(['', ',F', False], decodeOSC(m.getBinary()))

    def testEncodeDecodeTrue(self):
        m = OSCMessage()
        m.append(None)
        self.assertEquals(['', ',N', None], decodeOSC(m.getBinary()))

    def testAppendDecodeOSCArray(self):
        m = OSCMessage()
        m.append((False, (1L,)))
        self.assertEquals(['', ',[F[h]]', [False, [1,],]], decodeOSC(m.getBinary()))

    def testAppendDecodeOSCArrayEmpty(self):
        m = OSCMessage()
        m.append(())
        self.assertEquals(['',',[]',[]], decodeOSC(m.getBinary()))

    def testDecodeArrayUnbalanced(self):
        self.assertRaises(OSCException, decodeOSC, '\x00\x00\x00\x00,[[]')
         
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyosc.tests.test_osc')

