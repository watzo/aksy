class ModulationPin:
    def __init__(self, s, pin_index, source, dest, level, keygroup_index):
        self.s = s
        self.pin_index = pin_index
        self.source = source
        self.dest = dest
        self.level = level
        self.keygroup_index = keygroup_index
        self.min = -100
        self.max = 100

    def set_value(self, value, all = False):
        # keep it within bounds

        if value > self.max:
            value = self.max
        elif value < self.min:
            value = self.min

        self.level = value
       
        if all:
            keygroup_index = 0
        else:
            keygroup_index = self.keygroup_index
       
        #print "DEBUG", self.pin_index, keygroup_index, self.source, self.dest, self.level
        self.s.programtools.set_modulation_connection(self.pin_index, keygroup_index, self.source, self.dest, self.level)
        
        return self.level
