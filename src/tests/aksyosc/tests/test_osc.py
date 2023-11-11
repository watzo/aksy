from unittest import TestCase, TestLoader
from aksyosc.osc import decodeOSC, OSCMessage, OSCException

class OSCMessageTest(TestCase):
    def testEncodeDecodeInt(self):
        m = OSCMessage()
        m.append(1)
        self.assertEqual(['', ',i', 1], decodeOSC(m.getBinary()))

    def testEncodeDecodeString(self):
        m = OSCMessage()
        m.append("abc")
        self.assertEqual(['', ',s', "abc"], decodeOSC(m.getBinary()))

    def testEncodeDecodeBinaryString(self):
        m = OSCMessage()
        m.append("\x00\x01\x02")
        self.assertEqual(['', ',b', "\x00\x01\02"], decodeOSC(m.getBinary()))

    def testEncodeDecodeFloat(self):
        m = OSCMessage()
        m.append(1.0)
        self.assertEqual(['', ',f', 1.0], decodeOSC(m.getBinary()))

    def testEncodeDecodeLong(self):
        m = OSCMessage()
        m.append(1)
        self.assertEqual(['', ',h', 1], decodeOSC(m.getBinary()))

    def testEncodeDecodeTrue(self):
        m = OSCMessage()
        m.append(True)
        self.assertEqual(['', ',T', True], decodeOSC(m.getBinary()))

    def testEncodeDecodeFalse(self):
        m = OSCMessage()
        m.append(False)
        self.assertEqual(['', ',F', False], decodeOSC(m.getBinary()))

    def testEncodeDecodeNone(self):
        m = OSCMessage()
        m.append(None)
        self.assertEqual(['', ',N', None], decodeOSC(m.getBinary()))

    def testEncodeDecodeIterable(self):
        m = OSCMessage()
        m.append((False, (1,)))
        self.assertEqual(['', ',[F[h]]', [False, [1,],]], decodeOSC(m.getBinary()))

    def testAppendDecodeIterableEmpty(self):
        m = OSCMessage()
        m.append([])
        self.assertEqual(['',',[]',[]], decodeOSC(m.getBinary()))

    def testDecodeOSCArrayUnbalanced(self):
        self.assertRaises(OSCException, decodeOSC, '\x00\x00\x00\x00,[[]')
         
def test_suite():
    # TODO replace OSC implementation
    return None

    testloader = TestLoader()
    return testloader.loadTestsFromName('tests.aksyosc.tests.test_osc')

