from aksy.devices.akai import fileparser
from tests.aksy.util import testutil
import unittest

class TestProgram(unittest.TestCase):
    def testRead(self):
        pfile = testutil.get_test_resource('221 Angel.akp')
        
        parser = fileparser.ProgramParser()
        program = parser.parse(pfile)
        self.assertEqual(9, len(program.keygroups))
        self.assertEqual('angel 01', program.keygroups[0].zones[0].samplename)
        self.assertEqual('', program.keygroups[0].zones[2].samplename)
    
def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('tests.aksy.devices.akai.tests.test_fileparser')
