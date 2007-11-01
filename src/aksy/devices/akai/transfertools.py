
""" Transfertools

Methods to send and receive files from the sampler.
"""

__author__ =  'Walco van Loon'
__version__=  "$Rev: 1354 $"

import os.path, logging

import aksy.devices.akai.sysex
from aksyx import AkaiSampler

LOG = logging.getLogger('aksy.devices.akai.transfertools')

class Transfertools:
    def __init__(self, connector):
        self.connector = connector
        self.get_cmd = aksy.devices.akai.sysex.Command('', '', 'transfertools', 'get', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), None)
        self.put_cmd = aksy.devices.akai.sysex.Command('', '', 'transfertools', 'put', (aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING, aksy.devices.akai.sysex_types.STRING), None)

    def get(self, filename, destfile=None, source=AkaiSampler.MEMORY):
        """Gets a file from the sampler, overwriting destfile if it already exists.
        """
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("get(%s, %s, %i)", filename, destfile, source)

        if destfile is None:
            destfile = filename

        if hasattr(self.connector, 'get'):
            return self.connector.get(filename, destfile, source)
        else:
            return self.connector.execute(self.get_cmd, (filename, destfile, source))

    def put(self, sourcepath, remote_name=None, destination=AkaiSampler.MEMORY):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("put(%s, %s, %i)", sourcepath, remote_name, destination)

        if remote_name is None:
            remote_name = os.path.basename(sourcepath)

        if hasattr(self.connector, 'put'):
            return self.connector.put(sourcepath, remote_name, destination)
        else:
            return self.connector.execute(self.put_cmd, (sourcepath, remote_name, destination,))
