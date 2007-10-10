from aksy.devices.akai import sysex
from aksyx import AkaiSampler

from aksy import fileutils
from aksy.concurrent import transaction

from aksyosc.server import OSCServer
from aksyosc.handler import SamplerCallbackManager

import os.path, logging, asyncore

from threading import Lock, Thread

log = logging.getLogger("aksy")

class Sampler(object):
    lock = Lock()
    """Base class for AkaiSampler.
    """
    def __init__(self, connector):
        self.connector = connector

    @transaction(lock)
    def execute_by_cmd_name(self, section_name, command_name, args, request_id=0):
        tools_obj = getattr(self, section_name)
        cmd = getattr(tools_obj, command_name + "_cmd")
        return self.execute(cmd, args, request_id)

    def get(self, filename, destfile=None, source=AkaiSampler.MEMORY):
        """Gets a file from the sampler, overwriting destfile if it already exists.
        """
        # TODO: consider removal
        self.connector.get(filename, destfile, source)

    def put(self, sourcepath, remote_name=None, destination=AkaiSampler.MEMORY):
        """Transfers a file to the sampler, overwriting it if it already exists.
        Default destination is memory
        """
        # TODO: consider replace connector put by _put
        self.connector.put(sourcepath, remote_name, destination)
        
    def execute_alt_request(self, handle, commands, args, index = None):
        """Execute a list of commands on the item with the specified handle using Akai System Exclusive "Alternative Operations"
        All commands must be from the same sub section (get/set/main), the section id will be determined from the first command in the list.
        
        Examples:
        
            cmd = z48.sampletools.get_sample_length_cmd
            cmd2 = z48.sampletools.get_bit_depth_cmd
            cmd3 = z48.sampletools.get_playback_mode_cmd
            z48.execute_alt_request(65536, [cmd, cmd2, cmd3], [])
        (95955L, 16, 0)

            cmd = z48.sampletools.set_playback_mode_cmd
            cmd2 = z48.sampletools.set_orig_pitch_cmd
            z48.execute_alt_request(65536, [cmd, cmd2], [[1], [2]])

        """
        result_bytes = self.connector.execute_request(sysex.AlternativeRequest(handle, commands, args, index))
        # TODO: move to usbconnector
        result = sysex.Reply(result_bytes, commands[0], True)
        return result.get_return_value()


    def execute(self, command, args, request_id=0):
        """Executes a command on the sampler
        """
        return self.connector.execute(command, args, request_id)

    def close(self):
        self.connector.close()
        
    def start_osc_server(self):
        # for i in 'AK': print ord(i)
        OSCServer('localhost', 6575,  SamplerCallbackManager(self))
        class ServerThread(Thread):
            def __init__(self):
                Thread.__init__(self, name='OSC Server Thread')
            def run(self):
                asyncore.loop()
        self.serverThread = ServerThread()
        self.serverThread.start()

    def stop_osc_server(self):
        asyncore.close_all()
        self.serverThread.join()
        
    @staticmethod
    def is_filetype_supported(fname):
        return fileutils.is_file_type_supported(Sampler.get_supported_file_types(), fname)

    @staticmethod
    def get_supported_file_types():
        return ('wav', 'aif', 'aiff', 'akp', 'akm', 'mid', 'pgm')
    
