from aksy.devices.akai import sysex
from aksyxusb import AkaiSampler

from aksy import model

import os.path
import logging

class Sampler(AkaiSampler):
    """Base class for AkaiSampler.
    """
    def __init__(self, usb_product_id=0, debug=1):
        self.debug = debug
        AkaiSampler.__init__(self, usb_product_id)

    def execute_by_cmd_name(self, section_name, command_name, args, request_id=0):
        tools_obj = getattr(self, section_name)
        cmd = getattr(tools_obj, command_name + "_cmd")
        return self.execute(cmd, args, request_id)

    def get(self, filename, destfile=None, source=AkaiSampler.MEMORY):
        """Gets a file from the sampler, overwriting destfile if it already exists.
        """
        if destfile is None:
            destfile = filename

        self._get(filename, destfile, source)

    def put(self, sourcepath, remote_name=None, destination=AkaiSampler.MEMORY):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        if remote_name is None:
            remote_name = os.path.basename(sourcepath)

        self._put(sourcepath, remote_name, destination)

    def execute(self, command, args, request_id=0):
        """Executes a command on the sampler
        """
        request = sysex.Request(command, args, request_id)
        if self.debug:
            logging.debug("Request: %s, id %i\n" % (repr(request), request_id))
        result_bytes = self._execute(request.get_bytes())
        if self.debug:
            logging.debug("Reply %s\n" % sysex.byte_repr(result_bytes))
        result = sysex.Reply(result_bytes, command)
        return result.get_return_value()
