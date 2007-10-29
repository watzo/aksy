import unittest
from aksy import fileutils


VALID_FILENAMES = ['123.wav', 'A-1.WAV', 'with spaces.akp', 'A +5DB.aif', 'N\!\@#\$%\^\&\*\(\).wav']
INVALID_FILENAMES = ['\x0c\x15\x0cw\x0e\xe6\x0e\xdf\x121\x16Q\x14N', '', 'abc+-=']

class TestIsFile(unittest.TestCase):
    def test_is_valid_file(self):
        for name in VALID_FILENAMES:
            self.assertTrue(fileutils.is_file(name), msg='% should be valid' % name)

    def test_is_invalid_file(self):
        for name in INVALID_FILENAMES:
            self.assertFalse(fileutils.is_file(name), msg='% should be invalid' % name)
    
class TestIsValidName(unittest.TestCase):
    def test_is_valid_name(self):
        for name in VALID_FILENAMES:
            self.assertTrue(fileutils.is_valid_name(name), msg='% should be valid' % name)
        
        self.assertTrue(fileutils.is_valid_name('abc'))

    def test_is_invalid_name(self):
        self.assertFalse(fileutils.is_valid_name(INVALID_FILENAMES[0]))

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.tests.test_fileutils')
    return suite
