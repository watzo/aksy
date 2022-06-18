import unittest

from aksy.constants import TransferLocation
from aksyx import AkaiSampler


class TestConstants(unittest.TestCase):
    def test_enum_values_shall_be_identical(self):
        assert AkaiSampler.DISK == TransferLocation.DISK
        assert AkaiSampler.MEMORY == TransferLocation.MEMORY


def test_suite():
    testloader = unittest.TestLoader()
    return testloader.loadTestsFromName('tests.aksy.tests.test_constants')
