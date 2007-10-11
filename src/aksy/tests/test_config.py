import unittest
from aksy.test import testutil
from aksy import config

INI_FILE = testutil.get_test_resource('aksy.ini')

class TestConfig(unittest.TestCase):
    def test_get_config(self):
        cfg = config.get_config(INI_FILE)
        self.assertEquals('z48', cfg.get('sampler', 'type'))
        self.assertEquals('localhost', cfg.get('osc', 'host'))
        self.assertEquals(6576, cfg.getint('osc', 'port'))
    
    def test_get_config_defaults(self):
        cfg = config.get_config(ini_file='non-existent')
        self.assertEquals('z48', cfg.get('sampler', 'type'))
        self.assertEquals('localhost', cfg.get('osc', 'host'))
        self.assertEquals(6575, cfg.getint('osc', 'port'))
        self.assertEquals(6575, cfg.getint('osc_client', 'port'))
        self.assertEquals('INFO', cfg.get('logging', 'level'))

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('aksy.tests.test_config')
    return suite
