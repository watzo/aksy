import samplerobject

class LFO(samplerobject.SamplerObject):
    def __init__(self, s, kg, index):
        samplerobject.SamplerObject.__init__(self, s, kg, "keygrouptools", index)
        self.attrs = ['lfo_rate','lfo_delay','lfo_depth','lfo_waveform','lfo_phase','lfo_shift','lfo_midi_sync','midi_clock_sync_div','lfo_retrigger','lfo_sync']
        self.abbr = {
                "lfo_rate" : "rate",
                "lfo_delay" : "delay",
                "lfo_depth" : "depth",
                "lfo_waveform" : "wave",
                "lfo_phase" : "phase",
                "lfo_shift" : "shift",
                "lfo_midi_sync" : "midi sync",
                "midi_clock_sync_div" : "midi sync div", # ???
                "lfo_retrigger" : "retrig",
                "lfo_sync" : "sync",
                }
        self.keygroup_index = kg.index
        self.need_index_for_set = True
        self.need_index_in_arguments = True
        self.set_current_before_get_set = True
        self.keygroup = kg
        
        self.precache()
        
    def get_handle(self):
        return self.keygroup.p.handle
