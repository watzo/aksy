import unittest, logging
from aksy.devices.akai import sysex, sysex_types, base

log = logging.getLogger("aksy")
class TestCommand(unittest.TestCase):
    def test_create_arg_bytes(self): #IGNORE:W0212
        dcmd = sysex.Command(sysex.Z48_ID, '\x20\x05', 'dummy', (sysex_types.BYTE,), None)

class TestRequest(unittest.TestCase):
    def testCreateRequest(self):
        # Select disk
        command = sysex.Command('\x5f', '\x20\x02', 'select_disk', (sysex_types.WORD,), None)
        bytes = sysex.Request(command, (256,)).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x20\x02\x00\x02\xf7', bytes)

        # Select root folder:
        folder = ''
        command = sysex.Command('\x5f', '\x20\x13', 'open_folder', (sysex_types.STRING,), None)
        bytes = sysex.Request(command, (folder,)).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x20\x13\x00\xf7', bytes)

        # Select autoload folder:
        folder = 'autoload'
        command = sysex.Command('\x5f', '\x20\x13', 'open_folder', (sysex_types.STRING,), None)
        bytes = sysex.Request(command, (folder,)).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x00\x20\x13\x61\x75\x74\x6f\x6c\x6f\x61\x64\x00\xf7', bytes)

    def testRequestWithNondefaultUserref(self):
        # slightly theoretical, because the z48 doesn't process these requests as expected
        command = sysex.Command('\x5f', '\x07\x01', 'get_sampler_name', (),(sysex_types.STRING,), sysex_types.USERREF)
        bytes = sysex.Request(command, (), request_id=129).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5f\x20\x01\x01\x07\x01\xf7', bytes)

    def testCreateS56KRequest(self):
        command = sysex.Command('\x5e', '\x07\x01', 'get_sampler_name', (),(sysex_types.STRING,), sysex_types.S56K_USERREF)
        bytes = sysex.Request(command, ()).get_bytes()
        self.assertEquals(
            '\xf0\x47\x5e\x20\x00\x00\x07\x01\xf7', bytes)

class TestReply(unittest.TestCase):
    def createCommand(self):
        return sysex.Command(sysex.Z48_ID, '\x20\x05', 'dummy', (), (sysex_types.BYTE,))

    def testCreateReply(self):
        DEFAULT_USERREF = '\x00'
        bytes = (sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID, DEFAULT_USERREF, 
                 sysex.REPLY_ID_REPLY, '\x20\x05', '\x01', sysex.END_SYSEX)
        dcmd = sysex.Command(sysex.Z48_ID, '\x20\x05', 'dummy', (), (sysex_types.BYTE,))
        reply = sysex.Reply(''.join(bytes), dcmd)
        self.assertEquals(1, reply.get_return_value())

        bytes =  (
            sysex.START_SYSEX, sysex.AKAI_ID, '\x5e\x20', '\x00',
            sysex.REPLY_ID_REPLY, '\x20\x05', '\x01', sysex.END_SYSEX)
        custom_cmd = sysex.Command('\x5e\x20', '\x20\x05', 'dummy', (),(sysex_types.BYTE,))
        reply = sysex.Reply(''.join(bytes), custom_cmd)
        self.assertEquals(1, reply.get_return_value())

        dcmd.reply_spec = (sysex_types.WORD, sysex_types.BYTE, sysex_types.BYTE, sysex_types.BYTE, sysex_types.BYTE, sysex_types.STRING)
        bytes = (
            sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID, '\x00',
            sysex.REPLY_ID_REPLY, '\x20\x05', '\x00','\x02\x01\x02', '\x00',
            '\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b', '\x00', sysex.END_SYSEX)
        reply = sysex.Reply(''.join(bytes), dcmd)
        self.assertEquals((256, 1, 2, 0, 1, 'Z48 & MPC4K'), reply.get_return_value())

        # Future: should raise unknown disk error
        dcmd.id = '\x20\x05'
        dcmd.reply_spec = ()
        bytes = '\xf0G_\x00E \x00\x00\x03\xf7'
        self.assertRaises(base.SamplerException, sysex.Reply, bytes, dcmd)
        # using pad type if we encounter bytes not according to specification
        dcmd.id = '\x20\x10'
        dcmd.reply_spec = None
        bytes =  (
            sysex.START_SYSEX, sysex.AKAI_ID, sysex.Z48_ID,
            '\x00', sysex.REPLY_ID_REPLY, '\x20\x10', '\x02',
            '\x15', '\x00', '\xf7')
        reply = sysex.Reply(''.join(bytes), dcmd)
        self.assertEquals(21, reply.get_return_value())

        # not possible yet how to deal with the dump request replies
        dcmd.reply_spec = ()
        self.assertRaises(sysex.ParseException,  sysex.Reply, '\xf0G_ ' + '\x00' * 2 
                          + 'R\x10 i\x01\xf7', dcmd)

        # reply on 'bulk command 10 05' 10 0a 00 f0 47 5e 20 00 00 10 05 15 f7
        dcmd.id = '\x10\x05'
        dcmd.reply_spec = (sysex_types.WORD, sysex_types.BYTE, sysex_types.BYTE, sysex_types.BYTE, 
                           sysex_types.BYTE, sysex_types.STRING)
        bytes = '\xf0\x47\x5f\x00\x52\x10\x05\x00\x02\x01\x02\x00\x01\x5a\x34\x38\x20\x26\x20\x4d\x50\x43\x34\x4b\x00\xf7'
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals((256, 1, 2, 0, 1, 'Z48 & MPC4K'), reply.get_return_value())

        dcmd.id = '\x10\x22'
        bytes = '\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x20\x53\x74\x72\x69\x6e\x67\x20\x41\x32\x2e\x77\x61\x76\x00\xf7'
        dcmd.reply_spec = (sysex_types.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals('Mell String A2.wav', reply.get_return_value())

        dcmd.id = '\x10\x22'
        bytes = '\xf0\x47\x5f\x00\x52\x10\x22\x4d\x65\x6c\x6c\x6f\x74\x72\x6f\x6e\x20\x53\x74\x72\x69\x6e\x67\x73\x2e\x61\x6b\x70\x00\xf7'
        dcmd.reply_spec = (sysex_types.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals('Mellotron Strings.akp', reply.get_return_value())

        dcmd.id = '\x07\x01'
        bytes = '\xf0\x47\x5f\x00\x52\x07\x01\x08\x5a\x38\x20\x53\x61\x6d\x70\x6c\x65\x72\x00\xf7'
        dcmd.reply_spec = (sysex_types.STRING,)
        reply = sysex.Reply(bytes, dcmd)
        self.assertEquals('Z8 Sampler', reply.get_return_value())

        bytes = '\xf0G_\x00E\x1eJ\x00\x00\xf7'
        self.assertRaises(NotImplementedError, sysex.Reply, bytes, self.createCommand())

    def testParseFileNotFound(self):
        bytes = '\xf0G_\x00E\x1eJ\x01\x02\xf7'
        self.assertRaises(IOError, sysex.Reply, bytes, self.createCommand())
        
    def testParseUserRef(self):
         cmd = sysex.Command(sysex.S56K_ID, '\x07\x01', 'dummy', (), (sysex_types.BYTE,), sysex_types.S56K_USERREF)
         bytes = '\xf0\x47\x5e\x20\x7e\x00\x52\x07\x01\x08\x5a\x38\x20\x53\x61\x6d\x70\x6c\x65\x72\x00\xf7'
         reply = sysex.Reply(bytes, cmd)
         self.assertEquals(126, reply.get_request_id())

    def testParseExtendedDisklist(self):
        bytes = sysex.repr_bytes(
            ['f0', '47', '5e', '20', '00', '00', '52', '10', '05', '01', '00', '00',
            '08', '00', '01', '4e', '6f', '20', '64', '69', '73', '6b', '00', '01', '01',
            '03', '08', '01', '00', '4e', '6f', '20', '64', '69', '73', '6b', '00', '01',
            '02', '03', '08', '02', '00', '4e', '6f', '20', '64', '69', '73', '6b', '00',
            '02', '03', '03', '01', '04', '01', '4e', '6f', '20', '44', '69', '73', '6b',
            '20', '4e', '61', '6d', '65', '00', 'f7'])
        cmd = sysex.Command(sysex.S56K_ID, '\x10\x05', 'dummy', (),(
            sysex_types.DISKLIST,), sysex_types.USERREF)
        reply = sysex.Reply(bytes, cmd)
        self.assertEquals(
            (sysex_types.DiskInfo((1, 0, 8, 0, 1, 'No disk')), sysex_types.DiskInfo((129, 3, 8, 1, 0, 'No disk')),
            sysex_types.DiskInfo((257, 3, 8, 2, 0, 'No disk')), sysex_types.DiskInfo((386, 3, 1, 4, 1, 'No Disk Name')))
            , reply.get_return_value())

    def testParseEchoReply(self):
        bytes = sysex.repr_bytes(
            ['f0', '47', '5f', '00', '52', '00', '06', '0b', '01', '01', '01', '01', 'f7'])
        cmd = sysex.Command(sysex.Z48_ID, '\x00\x06', 'query', (), None)
        reply = sysex.Reply(bytes, cmd)
        self.assertEquals((1,1,1,1), reply.get_return_value())

    def testParseHandleNameArray(self):
        bytes = sysex.repr_bytes(['F0','47','5F','00','52','14','02','20','08','44',
            '72','79','20','4B','69','74','20','30','32','00','08','50','72','6F','67','72','61','6D','20','31','00',
            '08','53','79','6E','74','68','54','65','73','74','00','F7'])
        cmd = sysex.Command(sysex.Z48_ID, '\x14\x02\02', 'get_handles_names', (), None)
        reply = sysex.Reply(bytes, cmd)
        self.assertEquals(('Dry Kit 02', 'Program 1', 'SynthTest'), reply.get_return_value())

class TestAlternativeRequest(unittest.TestCase):
    def test_no_args(self):
        cmd = sysex.Command(sysex.Z48_ID, '\x1F\x50', 'get_sample_length', (), None)
        req = sysex.AlternativeRequest(65536, [cmd], [])
        self.assertEquals('\xf0G_\x00`\x03\x00\x00\x04\x00\x01P\xf7', req.get_bytes())
    def test_with_args(self):
        cmd = sysex.Command('_', '\x1E\x26', 'set_playback_mode', (sysex_types.BYTE,), None)
        req = sysex.AlternativeRequest(65536, [cmd, cmd], [[1],[2]])
        self.assertEquals('\xf0G_\x00`\x02\x00\x00\x04\x00\x02&\x01\x02&\x02\xf7', req.get_bytes())
    
class TestModuleMethods(unittest.TestCase):
    def test_byte_repr(self):
        bytes = '\xf0G_\x00E \x00\x00\x03\xf7'
        self.assertEquals(
            "['f0', '47', '5f', '00', '45', '20', '00', '00', '03', 'f7']",
            sysex.byte_repr(bytes))
    def test_repr_bytes(self):
        self.assertEquals(
            '\xf0G_\x00E \x00\x00\x03\xf7',
            sysex.repr_bytes(['f0', '47', '5f', '00', '45', '20', '00', '00', '03', 'f7']))

def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('aksy.devices.akai.tests.test_sysex')
