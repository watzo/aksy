import os,os.path,re,logging,sys,struct,math,traceback
import gtk,pygtk,gobject
import aksy

from aksy.device import Devices
from modelutils import *
from samplerobject import *

class record(samplerobject):
    def __init__(self, s):
        samplerobject.__init__(self, s, None, "recordingtools")
        self.attrs = ["status", "progress", "maximum_record_time", "input", "mode", "monitor", "rec_time", "pitch", "threshold", "trigger_src", "bit_depth", "prerec_time", "name", "name_seed", "autorecord_mode", "autonormalize"]
        self.update()
