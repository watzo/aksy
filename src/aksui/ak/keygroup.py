from aksy.device import Devices
import ak, utils

class Keygroup(ak.SamplerObject):
    def __init__(self,program,index):
        ak.SamplerObject.__init__(self,program.s,None,"keygrouptools")
        self.current_mod_source_index = 11
        self.attrs = ["low_note", "high_note", "mute_group", "fx_override", "fx_send_level", "zone_xfade", "zone_xfade_type", "polyphony", "tune", "level", "play_trigger", "play_trigger_velocity", "filter", "filter_cutoff", "filter_resonance", "filter_attenuation"]
        self.p = program
        self.index = index
        self.s = program.s
        
        if getattr(self.s,"samples",None):
            self.samples = self.s.samples
        else:
            self.samples = None
            
        kgt = self.s.keygrouptools

        self.filter_attributes = ['filter', 'filter_cutoff', 'filter_resonance']

        self.amp_envelope = ak.Envelope(self, 0)
        self.filter_envelope = ak.Envelope(self, 1)
        self.aux_envelope = ak.Envelope(self, 2)

        self.zones = [ak.Zone(self,1), ak.Zone(self,2), ak.Zone(self,3), ak.Zone(self,4)]
        self.mod_matrix = self.p.get_matrix(self.index)

    def on_mod_source_changed(self, widget):
        self.current_mod_source_index = widget.get_active()

    def set(self, attrname, attrval):
        kgt = self.s.keygrouptools
        kgt.set_curr_keygroup(self.index)
        func = getattr(kgt, "set_" + attrname, None)
        if func:
            if attrname in self.filter_attributes:
                func(0,attrval)
            else:
                if isinstance(attrval,float):
                    attrval = int(attrval)
                func(attrval)

        self.attrscache[attrname] = attrval
        
    def update(self):
        kgt = self.s.keygrouptools
        for attr in self.attrs:
            fname = "get_" + attr
            func = getattr(kgt,fname)
            if attr in self.filter_attributes:
                setattr(self,attr,func(0))
            else:
                setattr(self,attr,func())

    def set_pin_value(self, source, value):
        return self.mod_matrix[source]

    def get_next_empty_pin(self):
        for pin in self.mod_matrix:
            pin = self.mod_matrix[pin]
            if pin.dest == 0:
                return pin
        return None

    def get_pin_by_source_and_dest(self, source, dest, create_new = False):
        for pin in self.mod_matrix:
            pin = self.mod_matrix[pin]
            if pin.dest == dest and pin.source == source:
                return pin

        if create_new:
            # didnt find a pin!
            pin = self.get_next_empty_pin()
            pin.source = source
            pin.dest = dest
        return pin
