from aksy.device import Devices
from utils.modelutils import *
from samplerobject import *

class zone(samplerobject):
    def __init__(self, kg, index):
        samplerobject.__init__(self, kg.s, kg, "zonetools", index)
        self.samples = kg.samples
        self.keygroup = kg
        self.specialattrs = ["sample",]
        self.need_index_for_set = True
        self.set_current_before_get_set = True

        # skip 'sample' for now
        self.attrs = ["sample", "level", "pan", "output", "filter", "tune", "keyboard_track", "playback", "mod_start", "low_velocity", "high_velocity", "mute"]

        self.update()

    def set_current_method(self):
        # need to do this because it gets called from __getattribute__ and causes inf loop
        s = object.__getattribute__(self, "s")
        keygroup = object.__getattribute__(self, "keygroup")

        kgt = s.keygrouptools
        kgt.set_curr_keygroup(keygroup.index)

    def get_special_attr(self,attrname,attrval):
        # actually used for setting
        if attrname == "sample":
            return self.s.samplesmodel[attrval][0]
        else:
            return None
