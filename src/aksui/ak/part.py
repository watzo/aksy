import ak

class Part(ak.SamplerObject):
    def __init__(self, s, m, index):
        ak.SamplerObject.__init__(self, s, m, "multitools", index)
        self.attrs = ["multi_part_name", "part_midi_channel", "part_mute", "part_solo", "part_level", "part_output", "part_pan", "part_fx_channel", "part_fx_send_level", "part_tune", "part_low_note", "part_high_note", "part_priority", "part_prog_no", "part_group_id"]
        self.need_index_for_set = True
        self.m = m
        
        self.precache()