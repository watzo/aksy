from aksy.devices.akai.z48.sampler import Z48
from aksy.devices.akai.s56k.sampler import S56K
from aksy.devices.akai.mock_z48.sampler import MockZ48, MockConnector
from aksy.devices.akai.connector import USBConnector
from aksyosc.connector import OSCConnector

_devices = { 'z48': Z48, 's56k': S56K, 'mpc4k': Z48, 'mock_z48': MockZ48 }
_connectors = { 'usb': USBConnector, 'osc': OSCConnector, 'mock': MockConnector }

class Devices:
    """
    return an instance for a specified device
    """

    @staticmethod
    def get_instance(device_id, connector_type='usb', *args, **kwargs):
        try:
            if connector_type == 'usb':
                connector = USBConnector(device_id)
            elif connector_type == 'osc':
                connector = OSCConnector('localhost', 6575)
            elif connector_type == 'mock':
                connector = MockConnector()
            else:
                raise Exception("Unknown connector type ", connector_type)
            return _devices[device_id](connector, *args, **kwargs)
        except KeyError, e:
            raise Exception("Device %s not found" % e[0])

