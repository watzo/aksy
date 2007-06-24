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

class TestCompoundWordType(unittest.TestCase):
    def testEncode(self):
        cw = sysex_types.CompoundWordType()
        self.assertEquals('\x00\x5d', cw.encode(93))
        self.assertEquals('\x00\x7f', cw.encode(127))
        self.assertEquals('\x05\x41', cw.encode(705))
        self.assertEquals('\x02\x00', cw.encode(256))
        self.assertEquals('\x7f\x7f', cw.encode(16383))

    def testDecode(self):
        cw = sysex_types.CompoundWordType()
        self.assertEquals(93, cw.decode('\x00\x5d'))
        self.assertEquals(128, cw.decode('\x01\x00'))
        self.assertEquals(705, cw.decode('\x05\x41'))
        self.assertEquals(256, cw.decode('\x02\x00'))
        self.assertEquals(16383, cw.decode('\x7f\x7f'))

    def testInvalidValues(self):
        cw = sysex_types.CompoundWordType()
        self.assertRaises(ValueError, cw.encode, 16383 + 1)

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
        self.assertRaises(sysex_types.DecodeException, s.decode, 44)

class TestUserRefType(unittest.TestCase):
    def testEncode(self):
        u = sysex_types.UserRefType()
        self.assertEquals('\x00', u.encode(0))
        self.assertEquals('\x10\x7f', u.encode(127))
        self.assertEquals('\x20\x7f\x7f', u.encode(sysex_types.WORD.max_val))

    def testFixedSizeEncode(self):
        u = sysex_types.UserRefType(2)
        self.assertEquals('\x20\x00\x00', u.encode(0))
        self.assertEquals('\x20\x7f\x00', u.encode(127))

    def testDecode(self):
        u = sysex_types.UserRefType()
        self.assertEquals((1, 0), u.decode('\x00'))
        self.assertEquals((3, 0), u.decode('\x20\x00\x00'))

        self.assertEquals((2, 127), u.decode('\x10\x7f'))
        self.assertEquals((3, 16383), u.decode('\x20\x7f\x7f'))

        self.assertEquals((3, 0), u.decode('\x20\x00\x00'))

    def testInvalidValues(self):
        u = sysex_types.UserRefType()
        self.assertRaises(ValueError, u.encode, -1)
        self.assertRaises(ValueError, u.encode, 16384)
        self.assertRaises(sysex_types.DecodeException, u.decode, '\x20\x00')

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
        self.assertEquals((16, ((65537, 'SynthTest'),)), result)

        result = self.handle_name_type.decode('\x04\x00\x00\x04\x00\x08\x44\x72\x79\x20\x4b\x69\x74\x20\x30\x32\x00\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
        self.assertEquals((33, ((65536, 'Dry Kit 02'), (65537, 'SynthTest'))), result)

class TestDiskInfo(unittest.TestCase):
    def test_repr(self):
        diskInfo = sysex_types.DiskInfo((256, 1, 0, 6, 1, 'Some disk'))
        self.assertEquals("<DiskInfo object name='Some disk', handle=256>", repr(diskInfo))
    def test_eq_neq(self):
        diskInfo1 = sysex_types.DiskInfo((256, 1, 0, 6, 1, 'Some disk'))
        diskInfo2 = sysex_types.DiskInfo((255, 1, 0, 6, 1, 'Some other disk'))
        diskInfo3 = sysex_types.DiskInfo((256, 1, 0, 6, 1, 'Some other name'))
        self.assertTrue(diskInfo1 == diskInfo3)
        self.assertFalse(diskInfo1 != diskInfo3)
        self.assertFalse(diskInfo1 == diskInfo2)
        self.assertTrue(diskInfo1 != diskInfo2)

class TestFourByteType(unittest.TestCase):
    def testEncode(self):
        fourByteType = sysex_types.FourByteType()
        self.assertEquals("\x01\x01\x01\x01", fourByteType.encode(1,1,1,1))

    def testDecode(self):
        fourByteType = sysex_types.FourByteType()
        self.assertEquals((1,1,1,1), fourByteType.decode("\x01\x01\x01\x01"))

    def testInvalidValues(self):
        fourByteType = sysex_types.FourByteType()
        self.assertRaises(ValueError, fourByteType.encode, 1,1,1)
        self.assertRaises(ValueError, fourByteType.encode, 128,1,1,1)
        self.assertRaises(sysex_types.DecodeException, fourByteType.decode, "\x01\x01\x01\x01\x05")

class TestThreeByteType(unittest.TestCase):
    def testEncode(self):
        threeByteType = sysex_types.ThreeByteType()
        self.assertEquals("\x01\x01\x01", threeByteType.encode(1,1,1))

    def testDecode(self):
        threeByteType = sysex_types.ThreeByteType()
        self.assertEquals((127,1,1), threeByteType.decode("\x7f\x01\x01"))

    def testInvalidValues(self):
        threeByteType = sysex_types.ThreeByteType()
        self.assertRaises(ValueError, threeByteType.encode, 1,1,1,1)
        self.assertRaises(sysex_types.DecodeException, threeByteType.decode, "\x01\x01\x01\x01\x05")

class TestTwoByteType(unittest.TestCase):
    def testEncode(self):
        twoByteType = sysex_types.TwoByteType()
        self.assertEquals("\x01\x01", twoByteType.encode(1,1))

    def testDecode(self):
        twoByteType = sysex_types.TwoByteType()
        self.assertEquals((127,1), twoByteType.decode("\x7f\x01"))

    def testInvalidValues(self):
        twoByteType = sysex_types.TwoByteType()
        self.assertRaises(ValueError, twoByteType.encode, 128,1)
        self.assertRaises(ValueError, twoByteType.encode, 1,1,1)
        self.assertRaises(sysex_types.DecodeException, twoByteType.decode, "\x01")
        self.assertRaises(sysex_types.DecodeException, twoByteType.decode, "\x01\x01\x01\x01\x05")


class TestModuleMethods(unittest.TestCase):
    def test_parse_byte_string(self):
        self.assertEquals(
            (5,'TEST'),
            sysex_types.parse_byte_string('\x54\x45\x53\x54' + sysex_types.STRING_TERMINATOR, sysex_types.STRING))
        self.assertEquals(
            (4,'EST'),
            sysex_types.parse_byte_string('\x54\x45\x53\x54' + sysex_types.STRING_TERMINATOR, sysex_types.STRING, 1))

        self.assertEquals(
            (10, ('TEST', 'TEST')),
            sysex_types.parse_byte_string('\x54\x45\x53\x54\x00\x54\x45\x53\x54\x00', sysex_types.STRINGARRAY))

        self.assertEquals(
            (1, 15),
            sysex_types.parse_byte_string('\x0f', sysex_types.BYTE))

        self.assertEquals(
            (2, -15),
            sysex_types.parse_byte_string('\x01\x0f', sysex_types.SBYTE))

        self.assertEquals(
            (2, 384),
            sysex_types.parse_byte_string('\x00\x03', sysex_types.WORD))

        self.assertEquals(
            (3, -1935),
            sysex_types.parse_byte_string('\x01\x0f\x0f', sysex_types.SWORD))

        self.assertEquals(
            (4, 268435455),
            sysex_types.parse_byte_string('\x7f\x7f\x7f\x7f', sysex_types.DWORD))

        self.assertEquals(
            (5, -268435455),
            sysex_types.parse_byte_string('\x01\x7f\x7f\x7f\x7f', sysex_types.SDWORD))

        self.assertEquals(
            (1, False),
            sysex_types.parse_byte_string('\x00', sysex_types.BOOL))

        self.assertEquals(
            (1, True),
            sysex_types.parse_byte_string('\x01', sysex_types.BOOL))

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.tests.test_sysex_types')
    return suite
