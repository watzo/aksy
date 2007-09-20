import samplerobject

class Zone(samplerobject.SamplerObject):
    def __init__(self, kg, index):
        samplerobject.SamplerObject.__init__(self, kg.s, kg, "zonetools", index)
        self.samples = kg.samples
        self.keygroup = kg
        self.specialattrs = ["sample",]
        self.keygroup_index = self.keygroup.index
        self.need_index_for_set = True
        self.need_index_in_arguments = True
        self.set_current_before_get_set = True

        # skip 'sample' for now
        self.attrs = ["sample", "level", "pan", "output", "filter", "tune", "keyboard_track", "playback", "mod_start", "low_velocity", "high_velocity", "mute"]
        self.abbr = {'mod_start' : 'start', 'low_velocity' : 'lo', 'high_velocity' : 'hi'}

        #self.precache()
        
    def get_handle(self):
        return self.keygroup.p.handle
        
    def get_special_attr(self,attrname,attrval):
        # actually used for setting
        if attrname == "sample":
            return attrval
        else:
            return None
