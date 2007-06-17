from samplerobject import samplerobject

class recording(samplerobject):
    def __init__(self, s):
        samplerobject.__init__(self, s, None, "recordingtools")
        self.attrs = ["status", "progress", "max_rec_time", "input", "mode", "monitor", "rec_time", "pitch", "threshold", "trigger_src", "bit_depth", "prerec_time", "name", "name_seed", "autorec_mode", "autonormalize"]
        self.update()
