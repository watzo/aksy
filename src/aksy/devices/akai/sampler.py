from aksy.devices.akai import transfertools
from aksyx import AkaiSampler

from aksy import fileutils

from aksyosc.server import OSCServer
from aksyosc.handler import SamplerCallbackManager

import logging, asyncore

from threading import Thread

log = logging.getLogger("aksy")

class Sampler(object):
    """Base class for AkaiSampler.
    """
    MEMORY = AkaiSampler.MEMORY
    DISK = AkaiSampler.DISK
    def __init__(self, connector):
        self.connector = connector
        self.transfertools = transfertools.Transfertools(connector)

    def get_cmd_by_name(self, section_name, command_name):
        tools_obj = getattr(self, section_name)
        return getattr(tools_obj, command_name + "_cmd")

    def execute_by_cmd_name(self, section_name, command_name, args):
        tools_obj = getattr(self, section_name)
        func = getattr(tools_obj, command_name)
        return apply(func, args)

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
        return self.connector.execute_alt_request(handle, commands, args, index)

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
    
