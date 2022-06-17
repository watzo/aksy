import unittest, logging
from aksy.devices.akai import sysex, sysex_types, model

log = logging.getLogger("aksy")


class TestCommand(unittest.TestCase):
    def test_create_arg_bytes(self): #IGNORE:W0212
        dcmd = sysex.Command(sysex.Z48_ID, b'\x20\x05', 'dummy', 'dummy', (sysex_types.BYTE,), None)


class TestRequest(unittest.TestCase):
    def testCreateRequest(self):
        # Select disk
        command = sysex.Command(b'\x5f', b'\x20\x02', 'disktools', 'select_disk', (sysex_types.WORD,), None)
        bytes = sysex.Request(command, (256,)).get_bytes()
        self.assertEqual(
            b'\xf0\x47\x5f\x00\x20\x02\x00\x02\xf7', bytes)

        # Select root folder:
        folder = ''
        command = sysex.Command(b'\x5f', b'\x20\x13', 'disktools', 'open_folder', (sysex_types.STRING,), None)
        bytes = sysex.Request(command, (folder,)).get_bytes()
        self.assertEqual(
            b'\xf0\x47\x5f\x00\x20\x13\x00\xf7', bytes)

        # Select autoload folder:
        folder = 'autoload'
        command = sysex.Command(b'\x5f', b'\x20\x13', 'disktools', 'open_folder', (sysex_types.STRING,), None)
        bytes = sysex.Request(command, (folder,)).get_bytes()
        self.assertEqual(
            b'\xf0\x47\x5f\x00\x20\x13\x61\x75\x74\x6f\x6c\x6f\x61\x64\x00\xf7', bytes)

    def testRequestWithNondefaultUserref(self):
        # slightly theoretical, because the z48 doesn't process these requests as expected
        command = sysex.Command(b'\x5f', b'\x07\x01', 'disktools', 'get_sampler_name', (),(sysex_types.STRING,), sysex_types.USERREF)
        bytes = sysex.Request(command, (), request_id=129).get_bytes()
        self.assertEqual(
            b'\xf0\x47\x5f\x20\x01\x01\x07\x01\xf7', bytes)

    def testCreateS56KRequest(self):
        command = sysex.Command(b'\x5e', b'\x07\x01', 'disktools', 'get_sampler_name', (),(sysex_types.STRING,), sysex_types.S56K_USERREF)
        bytes = sysex.Request(command, ()).get_bytes()
        self.assertEqual(
            b'\xf0\x47\x5e\x20\x00\x00\x07\x01\xf7', bytes)

class TestReply(unittest.TestCase):
    def createCommand(self):
        return sysex.Command(sysex.Z48_ID, b'\x20\x05', 'dummy', 'dummy', (), (sysex_types.BYTE,))

    def testCreateReply(self):
        DEFAULT_USERREF = b'\x00'
        bytes = (sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID, DEFAULT_USERREF, 
                 sysex.REPLY_ID_REPLY, b'\x20\x05', b'\x01', sysex.END_SYSEX)
        dcmd = sysex.Command(sysex.Z48_ID, b'\x20\x05', 'dummy', 'dummy', (), (sysex_types.BYTE,))
        reply = sysex.Reply(b''.join(bytes), dcmd)
        self.assertEqual(1, reply.get_return_value())

        bytes =  (
            sysex.START_SYSEX, sysex.AKAI_ID, b'\x5e\x20', b'\x00',
            sysex.REPLY_ID_REPLY, b'\x20\x05', b'\x01', sysex.END_SYSEX)
        custom_cmd = sysex.Command(b'\x5e\x20', b'\x20\x05', 'disktools', 'dummy', (),(sysex_types.BYTE,))
        reply = sysex.Reply(b''.join(bytes), custom_cmd)
        self.assertEqual(1, reply.get_return_value())

        dcmd.reply_spec = (sysex_types.WORD, sysex_types.BYTE, sysex_types.BYTE, sysex_types.BYTE, sysex_types.BYTE, sysex_types.STRING)
        bytes = (
            sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID, b'\x00',
            sysex.REPLY_ID_REPLY, b'\x20\x05', b'\x00', b'\x02\x01\x02', b'\x00',
            b'\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b', b'\x00', sysex.END_SYSEX)
        reply = sysex.Reply(b''.join(bytes), dcmd)
        self.assertEqual((256, 1, 2, 0, 1, 'Z48 & MPC4K'), reply.get_return_value())

        # Future: should raise unknown disk error
        dcmd.id = b'\x20\x05'
        dcmd.reply_spec = ()
        bytes = b'\xf0G_\x00E \x00\x00\x03\xf7'
        self.assertRaises(model.SamplerException, sysex.Reply, bytes, dcmd)
        # using pad type if we encounter bytes not according to specification
        dcmd.id = b'\x20\x10'
        dcmd.reply_spec = None
        bytes =  (
            sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID,
            b'\x00', sysex.REPLY_ID_REPLY, b'\x20\x10', b'\x02',
            b'\x15', b'\x00', b'\xf7')
        reply = sysex.Reply(b''.join(bytes), dcmd)
        self.assertEqual(21, reply.get_return_value())

        # not possible yet how to deal with the dump request replies
        dcmd.reply_spec = ()
        self.assertRaises(sysex.ParseException,  sysex.Reply, '\xf0G_ ' + '\x00' * 2 
                          + 'R\x10 i\x01\xf7', dcmd)

        # reply on 'bulk command 10 05' 10 0a 00 f0 47 5e 20 00 00 10 05 15 f7
        dcmd.id = b'\x10\x05'
        dcmd.reply_spec = (sysex_types.WORD, sysex_types.BYTE, sysex_types.BYTE, sysex_types.BYTE, 
                           sysex_types.BYTE, sysex_types.STRING)
        bytes = b'\xf0\x47\x5f\x00\x52\x10\x05\x00\x02\x01\x02\x00\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b\x00\xf7'
        reply = sysex.Reply(bytes, dcmd)
        self.assertEqual((256, 1, 2, 0, 1, 'Z48 & MPC4K'), reply.get_return_value())

        dcmd.id = b'\x10\x22'
        bytes = b'\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x20\x53\x74\x72\x69\x6e\x67\x20\x41\x32\x2e\x77\x61\x76\x00\xf7'
        dcmd.reply_spec = (sysex_types.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEqual('Mell String A2.wav', reply.get_return_value())

        dcmd.id = b'\x10\x22'
        bytes = b'\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x6f\x74\x72\x6f\x6e\x20\x53\x74\x72\x69\x6e\x67\x73\x2e\x61\x6b\x70\x00\xf7'
        dcmd.reply_spec = (sysex_types.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEqual('Mellotron Strings.akp', reply.get_return_value())

        dcmd.id = b'\x07\x01'
        dcmd.reply_spec = (sysex_types.STRING,)
        reply = sysex.Reply(b'\xf0\x47\x5f\x00\x52\x07\x01\x08\x5a\x38\x20\x53\x61\x6d\x70\x6c\x65\x72\x00\xf7', dcmd)
        self.assertEqual('Z8 Sampler', reply.get_return_value())

        self.assertRaises(NotImplementedError, sysex.Reply, b'\xf0G_\x00E\x1eJ\x00\x00\xf7', self.createCommand())

    def testParseFileNotFound(self):
        self.assertRaises(IOError, sysex.Reply, b'\xf0G_\x00E\x1eJ\x01\x02\xf7', self.createCommand())
        
    def testParseUserRef(self):
         cmd = sysex.Command(sysex.S56K_ID, b'\x07\x01', 'dummy', 'dummy', (), (sysex_types.BYTE,), sysex_types.S56K_USERREF)
         bytes = b'\xf0\x47\x5e\x20\x7e\x00\x52\x07\x01\x08\x5a\x38\x20\x53\x61\x6d\x70\x6c\x65\x72\x00\xf7'
         reply = sysex.Reply(bytes, cmd)
         self.assertEqual(126, reply.get_request_id())

    def testParseExtendedDisklist(self):
        reply_bytes = sysex.repr_bytes(
            ['f0', '47', '5e', '20', '00', '00', '52', '10', '05', '01', '00', '00',
            '08', '00', '01', '4e', '6f', '20', '64', '69', '73', '6b', '00', '01', '01',
            '03', '08', '01', '00', '4e', '6f', '20', '64', '69', '73', '6b', '00', '01',
            '02', '03', '08', '02', '00', '4e', '6f', '20', '64', '69', '73', '6b', '00',
            '02', '03', '03', '01', '04', '01', '4e', '6f', '20', '44', '69', '73', '6b',
            '20', '4e', '61', '6d', '65', '00', 'f7'])
        cmd = sysex.Command(sysex.S56K_ID, b'\x10\x05', 'dummy', 'dummy', (),(
            sysex_types.DISKLIST,), sysex_types.USERREF)
        reply = sysex.Reply(reply_bytes, cmd)
        self.assertEqual(
            ((1, 0, 8, 0, 1, 'No disk'), (129, 3, 8, 1, 0, 'No disk'),
            (257, 3, 8, 2, 0, 'No disk'), (386, 3, 1, 4, 1, 'No Disk Name'))
            , reply.get_return_value())

    def testParseEchoReply(self):
        reply_bytes = sysex.repr_bytes(
            ['f0', '47', '5f', '00', '52', '00', '06', '0b', '01', '01', '01', '01', 'f7'])
        cmd = sysex.Command(sysex.Z48_ID, b'\x00\x06', 'sysextools', 'query', (), None)
        reply = sysex.Reply(reply_bytes, cmd)
        self.assertEqual((1,1,1,1), reply.get_return_value())

    def testParseHandleNameArray(self):
        cmd_bytes = sysex.repr_bytes(['F0','47','5F','00','52','14','02','20','08','44',
            '72','79','20','4B','69','74','20','30','32','00','08','50','72','6F','67','72','61','6D','20','31','00',
            '08','53','79','6E','74','68','54','65','73','74','00','F7'])
        cmd = sysex.Command(sysex.Z48_ID, b'\x14\x02\02', 'programtools', 'get_handles_names', (), None)
        reply = sysex.Reply(cmd_bytes, cmd)
        self.assertEqual(('Dry Kit 02', 'Program 1', 'SynthTest'), reply.get_return_value())

class TestAlternativeRequest(unittest.TestCase):
    def test_no_args(self):
        cmd = sysex.Command(sysex.Z48_ID, b'\x1F\x50', 'sampletools', 'get_sample_length', (), None)
        req = sysex.AlternativeRequest(65536, [cmd], [])
        self.assertEqual(b'\xf0G_\x00`\x03\x00\x00\x04\x00\x01P\xf7', req.get_bytes())

    def test_with_args(self):
        cmd = sysex.Command(b'_', b'\x1E\x26', 'programtools', 'set_playback_mode', (sysex_types.BYTE,), None)
        req = sysex.AlternativeRequest(65536, [cmd, cmd], [[1],[2]])
        self.assertEqual(b'\xf0G_\x00`\x02\x00\x00\x04\x00\x02&\x01\x02&\x02\xf7', req.get_bytes())
    
    def test_with_multiple_args(self):
        cmd = sysex.Command(b'_', b'\x0E\x09', 'programtools', 'set_mod_start', (sysex_types.BYTE, sysex_types.SWORD), None)
        req = sysex.AlternativeRequest(65536, [cmd, cmd], [[1,1],[1,2]])
        self.assertEqual(b'\xf0G_\x00a\x02\x00\x00\x04\x00\x05\t\x01\x00\x01\x00\x05\t\x01\x00\x02\x00\xf7', req.get_bytes())

    def test_keygroup_index(self):
        cmd = sysex.Command(b'_', b'\x13\x30', 'programtools', 'get_envelope_rate1', (sysex_types.BYTE,), None)
        req = sysex.AlternativeRequest(65536, [cmd, cmd], [[1],[2]], index=3)
        self.assertEqual(b'\xf0G_\x00a\x07\x00\x00\x04\x00\x03\x020\x01\x020\x02\xf7', req.get_bytes())
    
class TestModuleMethods(unittest.TestCase):
    def test_byte_repr(self):
        bytes = b'\xf0G_\x00E \x00\x00\x03\xf7'
        self.assertEqual(
            "['f0', '47', '5f', '00', '45', '20', '00', '00', '03', 'f7']",
            sysex.byte_repr(bytes))
    def test_repr_bytes(self):
        self.assertEqual(
            b'\xf0G_\x00E \x00\x00\x03\xf7',
            sysex.repr_bytes(['f0', '47', '5f', '00', '45', '20', '00', '00', '03', 'f7']))

def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('tests.aksy.devices.akai.tests.test_sysex')
