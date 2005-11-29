import struct, sys, unittest
from aksy.devices.akai import sysex

class TestCommand(unittest.TestCase):
    def test_create_arg_bytes(self):
        dcmd = sysex.Command(sysex.Z48_ID, '\x20\x05', 'dummy', (sysex.BYTE,))

class TestRequest(unittest.TestCase):
    def testCreateRequest(self):
        # Select disk
        command = sysex.Command('\x5f', '\x20\x02', 'select_disk', (sysex.WORD,))
        bytes = sysex.Request(command, (256,)).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x20\x02\x00\x02\xf7', bytes)

        # Select root folder:
        folder = ''
        command = sysex.Command('\x5f', '\x20\x13', 'set_curr_folder', (sysex.STRING,), ())
        bytes = sysex.Request(command, (folder,)).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x20\x13\x00\xf7', bytes)

        # Select autoload folder:
        folder = 'autoload'
        command = sysex.Command('\x5f', '\x20\x13', 'set_curr_folder', (sysex.STRING,), ())
        bytes = sysex.Request(command, (folder,)).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x20\x13\x61\x75\x74\x6f\x6c\x6f\x61\x64\x00\xf7', bytes)

        command = sysex.Command('\x5f', '\x07\x01', 'get_sampler_name', (),(sysex.STRING,))
        bytes = sysex.Request(command, ()).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x07\x01\xf7', bytes)

class TestReply(unittest.TestCase):
    def testCreateReply(self):
        DEFAULT_USERREF='\x00'
        bytes =  (sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID, sysex.DEFAULT_USERREF, sysex.REPLY_ID_REPLY, '\x20\x05', '\x01', sysex.END_SYSEX)
        dcmd = sysex.Command(sysex.Z48_ID, '\x20\x05', 'dummy', (),(sysex.BYTE,))
        reply = sysex.Reply(''.join(bytes), dcmd)
        self.assertEquals(1, reply.parse())

        bytes =  (
            sysex.START_SYSEX, sysex.AKAI_ID, '\x5e\x20', sysex.DEFAULT_USERREF,
            sysex.REPLY_ID_REPLY, '\x20\x05', '\x01', sysex.END_SYSEX)
        custom_cmd = sysex.Command('\x5e\x20', '\x20\x05', 'dummy', (),(sysex.BYTE,))
        reply = sysex.Reply(''.join(bytes), custom_cmd)
        self.assertEquals(1, reply.parse())

        dcmd.reply_spec = (sysex.WORD, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.STRING)
        bytes = (
            sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID, sysex.DEFAULT_USERREF,
            sysex.REPLY_ID_REPLY, '\x20\x05', '\x00','\x02\x01\x02', '\x00',
            '\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b', '\x00', sysex.END_SYSEX)
        reply = sysex.Reply(''.join(bytes), dcmd)
        self.assertEquals((256, 1, 2, 0, 1, 'Z48 & MPC4K'), reply.parse())

        # Future: should raise unknown disk error
        dcmd.id = '\x20\x05'
        dcmd.reply_spec = ()
        bytes = '\xf0G_\x00E \x00\x00\x03\xf7'
        reply = sysex.Reply(bytes, dcmd)
        self.assertRaises(sysex.SamplerException, reply.parse)
        # using pad type if we encounter bytes not according to specification
        dcmd.id = '\x20\x10'
        dcmd.reply_spec = None
        bytes =  (
            sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID,
            sysex.DEFAULT_USERREF, sysex.REPLY_ID_REPLY, '\x20\x10', '\x02',
            '\x15', '\x00', '\xf7')
        reply = sysex.Reply(''.join(bytes), dcmd)
        self.assertEquals(21, reply.parse())

        # not possible yet how to deal with the dump request replies
        dcmd.reply_spec = ()
        reply = sysex.Reply('\xf0G_ ' + '\x00' * 2 + 'R\x10 i\x01\xf7', dcmd)
        self.assertRaises(sysex.ParseException, reply.parse)

        # reply on 'bulk command 10 05' 10 0a 00 f0 47 5e 20 00 00 10 05 15 f7
        dcmd.id = '\x10\x05'
        dcmd.reply_spec = (sysex.WORD, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.BYTE, sysex.STRING)
        bytes = '\xf0\x47\x5f\x00\x52\x10\x05\x00\x02\x01\x02\x00\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b\x00\xf7'
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals((256, 1, 2, 0, 1, 'Z48 & MPC4K'), reply.parse())

        dcmd.id = '\x10\x22'
        bytes = '\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x20\x53\x74\x72\x69\x6e\x67\x20\x41\x32\x2e\x77\x61\x76\x00\xf7'
        dcmd.reply_spec = (sysex.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals('Mell String A2.wav', reply.parse())

        dcmd.id = '\x10\x22'
        bytes = '\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x6f\x74\x72\x6f\x6e\x20\x53\x74\x72\x69\x6e\x67\x73\x2e\x61\x6b\x70\x00\xf7'
        dcmd.reply_spec = (sysex.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals('Mellotron Strings.akp', reply.parse())

        dcmd.id = '\x07\x01'
        bytes = '\xf0\x47\x5f\x00\x52\x07\x01\x08\x5a\x38\x20\x53\x61\x6d\x70\x6c\x65\x72\x00\xf7'
        dcmd.reply_spec = (sysex.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals('Z8 Sampler', reply.parse())

        bytes = '\xf0G_\x00E\x1eJ\x00\x00\xf7'
        reply = sysex.Reply(bytes, dcmd)
        self.assertRaises(sysex.SamplerException, reply.parse)

class TestByteType(unittest.TestCase):
    def testInvalidValues(self):
        b = sysex.ByteType()
        self.assertRaises(ValueError, b.encode, 128)

    def testDecode(self):
        b = sysex.ByteType()
        self.assertEquals(5, b.decode('\x05'))

class TestSignedByteType(unittest.TestCase):
    def testEncode(self):
        sb = sysex.SignedByteType()
        self.assertEquals('\x01\x05', sb.encode(-5))

    def testDecode(self):
        sb = sysex.SignedByteType()
        self.assertEquals(-5, sb.decode('\x01\x05'))

class TestWordType(unittest.TestCase):
    def testEncode(self):
        w = sysex.WordType()
        self.assertEquals('\x00\x02', w.encode(256))

    def testDecode(self):
        w = sysex.WordType()
        self.assertEquals(256, w.decode('\x00\x02'))

class TestSignedWordType(unittest.TestCase):
    def testEncode(self):
        sw = sysex.SignedWordType()
        self.assertEquals('\x00\x00\x02', sw.encode(256))

        self.assertEquals('\x01\x7f\x7f', sw.encode(-16383))
        self.assertEquals('\x01\x00\x02', sw.encode(-256))

    def testDecode(self):
        sw = sysex.SignedWordType()
        self.assertEquals(-256, sw.decode('\x01\x00\x02'))
        self.assertEquals(-16383, sw.decode('\x01\x7f\x7f'))

class TestDoubleWordType(unittest.TestCase):
    def testEncode(self):
        dw = sysex.DoubleWordType()
        self.assertEquals('\x7f\x7f\x7f\x7f', dw.encode(268435455))
        self.assertEquals('\x01\x00\x00\x00', dw.encode(1))

    def testDecode(self):
        dw = sysex.DoubleWordType()
        self.assertEquals(268435455, dw.decode('\x7f\x7f\x7f\x7f'))

class TestSignedDoubleWordType(unittest.TestCase):
    def testEncode(self):
        sdw = sysex.SignedDoubleWordType()
        self.assertEquals('\x01\x7f\x7f\x7f\x7f', sdw.encode(-268435455))

    def testDecode(self):
        sdw = sysex.SignedDoubleWordType()
        self.assertEquals(-268435455, sdw.decode('\x01\x7f\x7f\x7f\x7f'))

class TestQWordType(unittest.TestCase):
    def testEncode(self):
        qw = sysex.QWordType()
        self.assertEquals('\x7f\x7f\x7f\x7f\x00\x00\x00\x00', qw.encode(268435455))

    def testDecode(self):
        qw = sysex.QWordType()
        self.assertEquals(
            72057594037927935L,
            qw.decode('\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f'))
        self.assertEquals(145957L, qw.decode('\x25\x74\x08\x00\x00\x00\x00\x00'))

class TestSignedQWordType(unittest.TestCase):
    def testEncode(self):
        sdw = sysex.SignedQWordType()
        self.assertEquals(
            '\x01\x7f\x7f\x7f\x7f\x00\x00\x00\x00',
            sdw.encode(-268435455))

    def testDecode(self):
        qw = sysex.SignedQWordType()
        self.assertEquals(
            -72057594037927935L,
            qw.decode('\x01\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f'))

        self.assertEquals(
            -558551906910208L,
            qw.decode('\x01\x00\x00\x00\x00\x00\x00\x7f\x00'))

class TestBoolType(unittest.TestCase):
    def testEncode(self):
        b = sysex.BoolType()
        self.assertEquals('\x00', b.encode(False))
        self.assertEquals('\x01', b.encode(True))

    def testDecode(self):
        b = sysex.BoolType()
        self.assertTrue(b.decode('\x01'))
        self.assertFalse(b.decode('\x00'))

class TestStringType(unittest.TestCase):
    def testEncode(self):
        s = sysex.StringType()
        self.assertEquals('test sdf\x00', s.encode('test sdf'))

    def testDecode(self):
        s = sysex.StringType()
        self.assertEquals((9, 'test sdf'), s.decode('test sdf\x00'))

class TestStringArrayType(unittest.TestCase):
    def testEncode(self):
        s = sysex.StringArrayType()
        self.assertRaises(NotImplementedError, s.encode, None)

    def testDecode(self):
        s = sysex.StringArrayType()
        self.assertEquals(
            (18, ('test sdf', 'test ghi')),
            s.decode('test sdf\x00test ghi\x00'))

    def testInvalidValues(self):
        s = sysex.StringArrayType()
        self.assertRaises(ValueError, s.decode, 44)

class TestPadType(unittest.TestCase):
    def testDecode(self):
        self.assertEquals(None, sysex.PadType().decode('\x33'))

class TestSoundLevelType(unittest.TestCase):
    def setUp(self):
        self.sl = sysex.SoundLevelType()

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
        self.handle_name_type = sysex.HandleNameArrayType()
    def testDecode(self):
        result = self.handle_name_type.decode('\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
        self.assertEquals((16, (65537, 'SynthTest')), result)

        result = self.handle_name_type.decode('\x04\x00\x00\x04\x00\x08\x44\x72\x79\x20\x4b\x69\x74\x20\x30\x32\x00\x04\x01\x00\x04\x00\x08\x53\x79\x6e\x74\x68\x54\x65\x73\x74\x00')
        self.assertEquals((33, (65536, 'Dry Kit 02', 65537, 'SynthTest')), result)

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.tests.test_sysex')
    return suite
