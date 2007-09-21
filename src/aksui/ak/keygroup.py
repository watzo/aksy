import samplerobject, zone, envelope

keygroup_cache = {}

def get_keygroup_cached(p, index):
    key = (p.handle, index)

    if not key in keygroup_cache.keys():
        keygroup_cache[key] = Keygroup(p, index) 

    keygroup = keygroup_cache[key]

    return keygroup

class Keygroup(samplerobject.SamplerObject):
    def __init__(self, program, index, precache_on_init = True):
        samplerobject.SamplerObject.__init__(self, program.s, None, "keygrouptools")
        self.current_mod_source_index = 11
        self.attrs = ["low_note", "high_note", "mute_group", "fx_override", "fx_send_level", "zone_xfade", "zone_xfade_type", "polyphony", "tune", "level", "play_trigger", "play_trigger_velocity", "filter", "filter_cutoff", "filter_resonance", "filter_attenuation"]
        self.attrs_minimal = ["low_note", "high_note"]
        self.abbr = {'polyphony' : 'poly', 'filter_cutoff':'cutoff', 'filter_resonance':'res', 'MOD_12_14':'filtenv', 'MOD_12_15':'filtenv', 'MOD_6_1':'velo', 'MOD_11_1':'ampenv', 'MOD_13_3':'auxenv',}
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

        self.amp_envelope = envelope.Envelope(self, 0)
        self.filter_envelope = envelope.Envelope(self, 1)
        self.aux_envelope = envelope.Envelope(self, 2)

        self.zones = [zone.Zone(self, 1), zone.Zone(self, 2), zone.Zone(self, 3), zone.Zone(self, 4)]
        self.mod_matrix = []
        self.mod_matrix_dict = {}
       
        if precache_on_init:
            self.precache()

    def load_matrix(self):
        (self.mod_matrix, self.mod_matrix_dict) = self.p.get_matrix(self.index + 1)

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
        kgt.set_curr_keygroup(self.keygroup_index)
        func = getattr(kgt, "set_" + attrname, None)
        if func:
            if attrname in self.filter_attributes:
                func(0, attrval)
            else:
                if isinstance(attrval, float):
                    attrval = int(attrval)
                func(attrval)
        else:
            print "no method set_" + attrname

        if self.set_callback:
            self.set_callback(attrname, attrval)
            
        self.attrscache[attrname] = attrval
        
    def set_pin_value(self, source, value):
        if len(self.mod_matrix) > 0:
            return self.mod_matrix[source]
        else:
            return None

    def get_next_empty_pin(self):
        for pin in self.mod_matrix:
            if pin.dest == 0:
                return pin
        return None

    def get_pin_by_name(self, attrname, create_new = False):
        if attrname.startswith("MOD_"):
            (blah, source, dest) = attrname.split("_")
            return self.get_pin_by_source_and_dest(int(source), int(dest), create_new)
        
    def get_pin_by_source_and_dest(self, source, dest, create_new = False):
        pin = None

        source_dest_index = (source, dest)

        if source_dest_index in self.mod_matrix_dict:
            pin = self.mod_matrix[self.mod_matrix_dict[source_dest_index].pin_index]
        elif create_new:
            # didnt find a pin!
            pin = self.get_next_empty_pin()
            pin.source = source
            pin.dest = dest
            self.mod_matrix_dict[(source, dest)] = pin

        return pin
