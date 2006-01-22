import unittest, os, os.path, md5
from aksy.devices.akai import sampler

TESTDIR = os.path.abspath(os.path.split(__file__)[0])

class TestSampler(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'sampler'):
            self.sampler = sampler.Sampler()

    def testTransfers(self):
        # TODO: add files for each type
        self._testTransfer('test.wav')

    def _testTransfer(self, filename):

        fullpath = os.path.join(TESTDIR, filename)
        self.sampler.put(fullpath)
        actualfilename = 'cp' + filename
        self.sampler.get(filename, actualfilename)
        expected = open(fullpath, 'rb')
        actual = open(actualfilename, 'rb')
        self.assertTrue(md5sum(expected), md5sum(actual))
        expected.close()
        actual.close()
        os.remove(actualfilename)

def md5sum(fh):
    m = md5.new()
    while True:
        d = fh.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.tests.test_transfers')
    return suite
