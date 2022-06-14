import unittest
from tests.aksy.util import testutil
from aksy import config

INI_FILE = testutil.get_test_resource('aksy.ini')

class TestConfig(unittest.TestCase):
    def test_get_config(self):
        cfg = config.get_config(INI_FILE)
        self.assertEqual('z48', cfg.get('sampler', 'type'))
        self.assertEqual('localhost', cfg.get('osc', 'host'))
        self.assertEqual(6576, cfg.getint('osc', 'port'))
    
    def test_get_config_defaults(self):
        cfg = config.get_config(ini_file='non-existent')
        self.assertEqual('z48', cfg.get('sampler', 'type'))
        self.assertEqual('localhost', cfg.get('osc', 'host'))
        self.assertEqual(6575, cfg.getint('osc', 'port'))
        self.assertEqual(6575, cfg.getint('osc_client', 'port'))
        self.assertEqual('INFO', cfg.get('logging', 'level'))

def test_suite():
    testloader = unittest.TestLoader()
    suite = testloader.loadTestsFromName('tests.aksy.tests.test_config')
    return suite
