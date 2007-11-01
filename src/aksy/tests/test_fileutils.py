import unittest
from aksy import fileutils


VALID_SAMPLES = ['/home/henk/123.wav', 'A-1.WAV',  'a.aiff', 'A +5DB.aif', 'N\!\@#\$%\^\&\*\(\).wav']
VALID_FILENAMES = [ 'with spaces.akp']
VALID_FILENAMES.extend(VALID_SAMPLES)
INVALID_FILENAMES = ['\x0c\x15\x0cw\x0e\xe6\x0e\xdf\x121\x16Q\x14N', '', 'abc+-=']

class TestIsSample(unittest.TestCase):
    def test_is_sample(self):
        for name in VALID_SAMPLES:
            self.assertTrue(fileutils.is_sample(name), msg='%s should be valid' % name)
        
class TestIsFile(unittest.TestCase):
    def test_is_valid_file(self):
        for name in VALID_FILENAMES:
            self.assertTrue(fileutils.is_file(name), msg='%s should be valid' % name)

    def test_is_invalid_file(self):
        for name in INVALID_FILENAMES:
            self.assertFalse(fileutils.is_file(name), msg='%s should be invalid' % name)
    
class TestIsValidName(unittest.TestCase):
    def test_is_valid_name(self):
        for name in VALID_FILENAMES:
            self.assertTrue(fileutils.is_valid_name(name), msg='%s should be valid' % name)
        
        self.assertTrue(fileutils.is_valid_name('abc'))

    def test_is_invalid_name(self):
        self.assertFalse(fileutils.is_valid_name(INVALID_FILENAMES[0]))

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.tests.test_fileutils')
    return suite
