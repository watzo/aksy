from aksy.devices.akai import fileparser
import unittest, os.path

class TestProgram(unittest.TestCase):
    def testRead(self):
        pfile = os.path.join(os.path.dirname(__file__), '221 Angel.akp')
        
        parser = fileparser.ProgramParser()
        program = parser.parse(pfile)
        self.assertEquals(9, len(program.keygroups))
        self.assertEquals('angel 01', program.keygroups[0].zones[0].samplename)
        self.assertEquals('', program.keygroups[0].zones[2].samplename)
    
def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('aksy.devices.akai.tests.test_fileparser')
