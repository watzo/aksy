import ak, utils

class Keygroup(ak.SamplerObject):
    def __init__(self, program, index):
        ak.SamplerObject.__init__(self, program.s, None, "keygrouptools")
        self.current_mod_source_index = 11
        self.attrs = ["low_note", "high_note", "mute_group", "fx_override", "fx_send_level", "zone_xfade", "zone_xfade_type", "polyphony", "tune", "level", "play_trigger", "play_trigger_velocity", "filter", "filter_cutoff", "filter_resonance", "filter_attenuation"]
        self.attrs_minimal = ["low_note", "high_note"]
        self.abbr = {'polyphony' : 'poly', 'filter_cutoff':'cutoff', 'filter_resonance':'res', 'MOD_12_14':'filtenv', 'MOD_12_15':'filtenv',
            'MOD_7_1':'tiltvel',            'MOD_11_1':'ampenv',            'MOD_13_3':'auxenv',                     }
        self.p = program
        self.index = index
        self.keygroup_index = index
        self.s = program.s
        
        if getattr(self.s, "samples", None):
            self.samples = self.s.samples
        else:
            self.samples = None
            
        kgt = self.s.keygrouptools

        self.filter_attributes = ['filter', 'filter_cutoff', 'filter_resonance']

        self.amp_envelope = ak.Envelope(self, 0)
        self.filter_envelope = ak.Envelope(self, 1)
        self.aux_envelope = ak.Envelope(self, 2)

        self.zones = [ak.Zone(self, 1), ak.Zone(self, 2), ak.Zone(self, 3), ak.Zone(self, 4)]
        self.mod_matrix = self.p.get_matrix(self.index)
        
        self.precache()
        
    def get_handle(self):
        # get handle by name or whatever, override in derived classes
        return self.p.handle

    def set_current(self):
        self.s.keygrouptools.set_curr_keygroup(self.index)

    def on_mod_source_changed(self, widget):
        self.current_mod_source_index = widget.get_active()

    """
    Need to phase this override out and merge it into samplerobject.set
    """
    def set(self, attrname, attrval):
        if attrname.startswith("MOD_"):
            pin = self.get_pin_by_name(attrname, True)
            self.attrscache[attrname] = pin.set_value(attrval)
            return
        
        kgt = self.s.keygrouptools
        kgt.set_curr_keygroup(self.index)
        func = getattr(kgt, "set_" + attrname, None)
        if func:
            if attrname in self.filter_attributes:
                func(0, attrval)
            else:
                if isinstance(attrval, float):
                    attrval = int(attrval)
                func(attrval)

        if self.set_callback:
            self.set_callback(attrname, attrval)
            
        self.attrscache[attrname] = attrval
        
    def set_pin_value(self, source, value):
        return self.mod_matrix[source]

    def get_next_empty_pin(self):
        for pin in self.mod_matrix:
            pin = self.mod_matrix[pin]
            if pin.dest == 0:
                return pin
        return None

    def get_pin_by_name(self, attrname, create_new = False):
        if attrname.startswith("MOD_"):
            (blah, source, dest) = attrname.split("_")
            return self.get_pin_by_source_and_dest(int(source), int(dest), create_new)
        
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
            
        if pin:
            return pin
        else:
            return None
