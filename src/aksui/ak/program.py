import samplerobject, program, keygroup, modulationmatrix, modulationpin

class Program(samplerobject.SamplerObject):
    def __init__(self, s, name, handle = None):
        samplerobject.SamplerObject.__init__(self,s,None,"programtools")

        self.name = name
        if handle:
            self.handle = handle
        else:
            self.handle = self.gettools().get_handle_by_name(self.name)

        self.specialattrs = ["name",]

        self.attrs = ["name", "type", "group_id", "genre", "program_no", "no_keygroups", "keygroup_xfade", "keygroup_xfade_type", "level", "polyphony", "portamento_enabled", "portamento_mode", "portamento_time", "glissando_mode", "aftertouch_mode", "aftertouch_value", "reassignment_method", "softpedal_loudness_reduction", "softpedal_attack_stretch", "softpedal_filter_close", "midi_transpose", "tune", "legato", "pitchbend_up", "pitchbend_down", "pitchbend_mode", "no_modulation_connections"]
        self.attrs_minimal = ["name", "type", "no_keygroups", "level", "polyphony"]
        
        if self.name:
            self.s.programtools.set_curr_by_name(self.name)
        else:
            print "No name..."
            
        self.precache()
        
    def get_handle(self):
        return self.handle
        
    def copy(self, destination_name):
        tools = self.gettools()
        tools.set_curr_by_name(self.name)
        tools.copy_program(destination_name)
        return program.Program(self.s,destination_name)
        
    def init_recycled(self):
        # ultimately this should be a plugin or something, but for now...
        # updates a recycle generated program to the settings i prefer use
        for kg in self.get_keygroups():
            for zone in kg.zones:
                zone.set("playback", 1) # ONE SHOT
            kg.set("polyphony", 1)

    def get_keygroups(self):
        keygroups = []

        for i in range(self.no_keygroups):
            keygroups.append(keygroup.Keygroup(self,i))

        return keygroups

    def set_name(self, name):
        self.s.programtools.set_curr_by_name(self.name)
        self.s.programtools.rename_curr(name)
        self.attrscache["name"] = name

    def dump_matrix(self):
        result = []
        n = self.s.programtools.get_no_modulation_connections()
        #print "number of modulation connections", n
        conns = self.get_matrix(0)

        result.append("Number of modulation connections for %s: %d" % (self.name, n))
        result.append("----")
        
        for c in conns:
            c = conns[c]
            if c.source > 0:
                result.append("%d. %s => %s = %d" % (c.pin_index, modulationmatrix.ModulationMatrix.sources[c.source], modulationmatrix.ModulationMatrix.destinations[c.dest], c.level))
                
        return '\n'.join(result)
    
    def get_matrix(self, keygroup_index):
        n = self.s.programtools.get_no_modulation_connections()

        pins_dict = {}
        pins = []


        cmd = self.s.programtools.get_modulation_connection_cmd

        for j in range(8):
            # create batch get command
            cmds = []
            args = []
            # ????: can only do 8 at a time?
            for i in range(8*j,8*(j+1)):
                #print "getting mod connection:", keygroup_index, "/", i
                cmds.append(cmd)
                args.append([i, keygroup_index])

            results = self.s.execute_alt_request(self.handle, cmds, args)

            if results:
                total_results = len(results) / 3

                for i in range(total_results):
                    offset = 3*i
                    (source, dest, level) = results[offset:offset+3] # snag 3 at a time
                    pin = modulationpin.ModulationPin(self.s, i, source, dest, level, keygroup_index)
                    pins.append(pin)
                    pins_dict[(source, dest)] = pin
            
        return (pins, pins_dict)
