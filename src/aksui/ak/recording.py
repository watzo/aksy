import samplerobject

from aksy import fileutils

class Recording(samplerobject.SamplerObject):
    def __init__(self, s):
        samplerobject.SamplerObject.__init__(self, s, None, "recordingtools")
        self.attrs = ["status", "progress", "max_rec_time", "input", "mode",
"monitor", "rec_time", "pitch", "threshold", "trigger_src", "bit_depth",
"prerec_time", "name", "name_seed", "autorec_mode", "autonormalize"]
        if not fileutils.is_valid_name(self.s.recordingtools.get_name()):
            self.set("name", "Sample %i" % (self.s.sampletools.get_no_items() + 1))
        self.update()

    def set(self, attrname, attrval):
        """ Overrides handle based lookups in base class
        """
        tools = self.gettools()
        getattr(tools, "set_" + attrname)(attrval)


