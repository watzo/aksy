from aksy.device import Devices
from utils.modelutils import *
from ak.samplerobject import *
from ak.envelope import *
from ak.zone import *

class keygroup(samplerobject):
    def __init__(self,program,index):
        samplerobject.__init__(self,program.s,None,"keygrouptools")
        self.attrs = ["low_note", "high_note", "mute_group", "fx_override", "fx_send_level", "zone_xfade", "zone_xfade_type", "polyphony", "tune", "level", "play_trigger", "play_trigger_velocity", "filter", "filter_cutoff", "filter_resonance", "filter_attenuation"]
        self.p = program
        self.index = index
        self.s = program.s
        self.initSamples()
        kgt = self.s.keygrouptools
        self.s.programtools.set_curr_by_name(self.p.name)
        kgt.set_curr_keygroup(self.index)

        self.filter_attributes = ['filter', 'filter_cutoff', 'filter_resonance']

        self.amp_envelope = envelope(self, 0)
        self.filter_envelope = envelope(self, 1)
        self.aux_envelope = envelope(self, 2)

        self.zones = [zone(self,1), zone(self,2), zone(self,3), zone(self,4)]

    def initSamples(self):
        self.samples = self.s.sampletools.get_names()

    def set(self, attrname, attrval):
        kgt = self.s.keygrouptools
        kgt.set_curr_keygroup(self.index)

        func = getattr(kgt, "set_" + attrname, None)
        if func:
            if attrname in self.filter_attributes:
                func(0,attrval)
            else:
                func(attrval)

    def update(self):
        kgt = self.s.keygrouptools
        for attr in self.attrs:
            fname = "get_" + attr
            func = getattr(kgt,fname)
            if attr in self.filter_attributes:
                setattr(self,attr,func(0))
            else:
                setattr(self,attr,func())
