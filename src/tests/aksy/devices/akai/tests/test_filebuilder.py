from aksy.devices.akai import filebuilder
from aksy.devices.akai.filemodel import Program
from aksy.devices.akai.filemodel import Zone
from aksy.devices.akai.filemodel import Keygroup
import unittest
from io import StringIO

class TestZoneBuilder(unittest.TestCase):
    def testBuild(self):
        builder = filebuilder.ZoneBuilder()
        zone = Zone.create_default()
        zone.samplename = 'test'
        chunk = builder.build(zone)
        self.assertNotEqual(None, chunk)
        self.assertEqual("zone", chunk.name)
        self.assertEqual(56, chunk.get_length())
                                           
class TestProgramWriter(unittest.TestCase):
    def testWrite(self):
        writer = filebuilder.ProgramWriter()
        zones = [Zone()] * 4
        keygroups = [Keygroup(zones)] * 4
        program = Program.create_default(keygroups)
        out = StringIO()
        writer.write(program, out)
    
def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('tests.aksy.devices.akai.tests.test_filebuilder')
