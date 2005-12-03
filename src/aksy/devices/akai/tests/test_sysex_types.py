import unittest
from aksy.devices.akai import sysex_types

class TestByteType(unittest.TestCase):
    def testInvalidValues(self):
        b = sysex_types.ByteType()
        self.assertRaises(ValueError, b.encode, 128)

    def testDecode(self):
        b = sysex_types.ByteType()
        self.assertEquals(5, b.decode('\x05'))

class TestSignedByteType(unittest.TestCase):
    def testEncode(self):
        sb = sysex_types.SignedByteType()
        self.assertEquals('\x01\x05', sb.encode(-5))

    def testDecode(self):
        sb = sysex_types.SignedByteType()
        self.assertEquals(-5, sb.decode('\x01\x05'))

class TestWordType(unittest.TestCase):
    def testEncode(self):
        w = sysex_types.WordType()
        self.assertEquals('\x00\x02', w.encode(256))
        self.assertEquals('\x7f\x7f', w.encode(16383))

    def testDecode(self):
        w = sysex_types.WordType()
        self.assertEquals(256, w.decode('\x00\x02'))
        self.assertEquals(16383, w.decode('\x7f\x7f'))

    def testInvalidValues(self):
        w = sysex_types.WordType()
        self.assertRaises(ValueError, w.encode, 16383 + 1)


class TestSignedWordType(unittest.TestCase):
    def testEncode(self):
        sw = sysex_types.SignedWordType()
        self.assertEquals('\x00\x00\x02', sw.encode(256))

        self.assertEquals('\x01\x7f\x7f', sw.encode(-16383))
        self.assertEquals('\x01\x00\x02', sw.encode(-256))

    def testDecode(self):
        sw = sysex_types.SignedWordType()
        self.assertEquals(-256, sw.decode('\x01\x00\x02'))
        self.assertEquals(-16383, sw.decode('\x01\x7f\x7f'))

class TestDoubleWordType(unittest.TestCase):
    def testEncode(self):
        dw = sysex_types.DoubleWordType()
        self.assertEquals('\x7f\x7f\x7f\x7f', dw.encode(268435455))
        self.assertEquals('\x01\x00\x00\x00', dw.encode(1))

    def testDecode(self):
        dw = sysex_types.DoubleWordType()
        self.assertEquals(268435455, dw.decode('\x7f\x7f\x7f\x7f'))

class TestSignedDoubleWordType(unittest.TestCase):
    def testEncode(self):
        sdw = sysex_types.SignedDoubleWordType()
        self.assertEquals('\x01\x7f\x7f\x7f\x7f', sdw.encode(-268435455))

    def testDecode(self):
        sdw = sysex_types.SignedDoubleWordType()
        self.assertEquals(-268435455, sdw.decode('\x01\x7f\x7f\x7f\x7f'))

class TestQWordType(unittest.TestCase):
    def testEncode(self):
        qw = sysex_types.QWordType()
        self.assertEquals('\x7f\x7f\x7f\x7f\x00\x00\x00\x00', qw.encode(268435455))

    def testDecode(self):
        qw = sysex_types.QWordType()
        self.assertEquals(
            72057594037927935L,
            qw.decode('\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f'))
        self.assertEquals(145957L, qw.decode('\x25\x74\x08\x00\x00\x00\x00\x00'))

class TestSignedQWordType(unittest.TestCase):
    def testEncode(self):
        sdw = sysex_types.SignedQWordType()
        self.assertEquals(
            '\x01\x7f\x7f\x7f\x7f\x00\x00\x00\x00',
            sdw.encode(-268435455))

    def testDecode(self):
        qw = sysex_types.SignedQWordType()
        self.assertEquals(
            -72057594037927935L,
            qw.decode('\x01\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f'))

        self.assertEquals(
            -558551906910208L,
            qw.decode('\x01\x00\x00\x00\x00\x00\x00\x7f\x00'))

class TestBoolType(unittest.TestCase):
    def testEncode(self):
        b = sysex_types.BoolType()
        self.assertEquals('\x00', b.encode(False))
        self.assertEquals('\x01', b.encode(True))

    def testDecode(self):
        b = sysex_types.BoolType()
        self.assertTrue(b.decode('\x01'))
        self.assertFalse(b.decode('\x00'))

class TestStringType(unittest.TestCase):
    def testEncode(self):
        s = sysex_types.StringType()
        self.assertEquals('test sdf\x00', s.encode('test sdf'))

    def testDecode(self):
        s = sysex_types.StringType()
        self.assertEquals((9, 'test sdf'), s.decode('test sdf\x00'))

class TestStringArrayType(unittest.TestCase):
    def testEncode(self):
        s = sysex_types.StringArrayType()
        self.assertRaises(NotImplementedError, s.encode, None)

    def testDecode(self):
        s = sysex_types.StringArrayType()
        self.assertEquals(
            (18, ('test sdf', 'test ghi')),
            s.decode('test sdf\x00test ghi\x00'))

    def testInvalidValues(self):
        s = sysex_types.StringArrayType()
        self.assertRaises(ValueError, s.decode, 44)

class TestUserRefType(unittest.TestCase):
    def testEncode(self):
        u = sysex_types.UserRefType()
        self.assertEquals('\x00', u.encode(0))
        self.assertEquals('\x01\x7f', u.encode(127))
        self.assertEquals('\x02\x7f\x7f', u.encode(sysex_types.WORD.max_val))

    def testFixedSizeEncode(self):
        u = sysex_types.UserRefType(2)
        self.assertEquals('\x02\x00\x00', u.encode(0))
        self.assertEquals('\x02\x7f\x00', u.encode(127))

    def testDecode(self):
        u = sysex_types.UserRefType()
        self.assertEquals((1, 0), u.decode('\x00'))
        self.assertEquals((3, 0), u.decode('\x02\x00\x00'))

        self.assertEquals((2, 127), u.decode('\x01\x7f'))
        self.assertEquals((3, 16383), u.decode('\x02\x7f\x7f'))

        self.assertEquals((3, 0), u.decode('\x02\x00\x00'))

    def testInvalidValues(self):
        u = sysex_types.UserRefType()
        self.assertRaises(ValueError, u.encode, -1)
        self.assertRaises(ValueError, u.encode, 16384)
        self.assertRaises(ValueError, u.decode, '\x02\x00')

class TestPadType(unittest.TestCase):
    def testDecode(self):
        self.assertEquals(None, sysex_types.PadType().decode('\x33'))

class TestSoundLevelType(unittest.TestCase):
    def setUp(self):
        self.sl = sysex_types.SoundLevelType()

    def testEncodeDecode(self):
        sl = self.sl
        self.assertEquals(-34, sl.decode(sl.encode(-34.0)))

    def testInvalidValues(self):
        self.assertRaises(ValueError, self.sl.encode, 61)
        self.assertRaises(ValueError, self.sl.encode, -601)

class TestPanningType(unittest.TestCase):
    pass

class TestTestHandleNameArrayType(unittest.TestCase):
    def setUp(self):
        self.handle_name_type = sysex_types.HandleNameArrayType()
    def testDecode(self):
        result = self.handle_name_type.decode('\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
        self.assertEquals((16, (65537, 'SynthTest')), result)

        result = self.handle_name_type.decode('\x04\x00\x00\x04\x00\x08\x44\x72\x79\x20\x4b\x69\x74\x20\x30\x32\x00\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
        self.assertEquals((33, (65536, 'Dry Kit 02', 65537, 'SynthTest')), result)

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.tests.test_sysex_types')
    return suite
