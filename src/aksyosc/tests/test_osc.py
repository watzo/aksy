from unittest import TestCase, TestLoader
from aksyosc.osc import decodeOSC, OSCMessage, OSCException

class OSCMessageTest(TestCase):
    def testEncodeDecodeInt(self):
        m = OSCMessage()
        m.append(1)
        self.assertEquals(['', ',i', 1], decodeOSC(m.getBinary()))

    def testEncodeDecodeString(self):
        m = OSCMessage()
        m.append("abc")
        self.assertEquals(['', ',s', "abc"], decodeOSC(m.getBinary()))

    def testEncodeDecodeFloat(self):
        m = OSCMessage()
        m.append(1.0)
        self.assertEquals(['', ',f', 1.0], decodeOSC(m.getBinary()))

    def testEncodeDecodeLong(self):
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

    def testEncodeDecodeNone(self):
        m = OSCMessage()
        m.append(None)
        self.assertEquals(['', ',N', None], decodeOSC(m.getBinary()))

    def testEncodeDecodeIterable(self):
        m = OSCMessage()
        m.append((False, (1L,)))
        self.assertEquals(['', ',[F[h]]', [False, [1,],]], decodeOSC(m.getBinary()))

    def testAppendDecodeIterableEmpty(self):
        m = OSCMessage()
        m.append([])
        self.assertEquals(['',',[]',[]], decodeOSC(m.getBinary()))

    def testDecodeOSCArrayUnbalanced(self):
        self.assertRaises(OSCException, decodeOSC, '\x00\x00\x00\x00,[[]')
         
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyosc.tests.test_osc')

