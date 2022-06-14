import unittest, os, os.path, md5, aksyx
from aksy.devices.akai import sampler as sampler_mod
from aksy.devices.akai import connector

from tests.aksy.util import testutil

conn = connector.USBConnector('z48')
sampler = sampler_mod.Sampler(conn)
    
class TestSampler(unittest.TestCase):
    def testTransfers(self):
        # TODO: add files for each type
        self._testTransfer('test.wav')

    def _testTransfer(self, filename):
        fullpath = testutil.get_test_resource(filename)
        sampler.put(fullpath)
        actualfilename = 'cp' + filename
        sampler.get(filename, actualfilename)
        expected = open(fullpath, 'rb')
        actual = open(actualfilename, 'rb')
        self.assertEqual(md5sum(expected), md5sum(actual))
        expected.close()
        actual.close()
        os.remove(actualfilename)

def md5sum(fhandle):
    digester = md5.new()
    while True:
        read = fhandle.read(8096)
        if not read:
            break
        digester.update(read)
    return digester.hexdigest()

def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('tests.aksy.devices.akai.ftests.test_transfers')
