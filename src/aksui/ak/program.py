from aksy.device import Devices
import ak,utils

class Program(ak.SamplerObject):
    def __init__(self, s, name, handle = None):
        ak.SamplerObject.__init__(self,s,None,"programtools")

        self.name = name
        self.handle = handle

        self.specialattrs = ["name",]

        self.attrs = ["name", "type", "group_id", "genre", "program_no", "no_keygroups", "keygroup_xfade", "keygroup_xfade_type", "level", "polyphony", "portamento_enabled", "portamento_mode", "portamento_time", "glissando_mode", "aftertouch_mode", "aftertouch_value", "reassignment_method", "softpedal_loudness_reduction", "softpedal_attack_stretch", "softpedal_filter_close", "midi_transpose", "tune", "legato", "pitchbend_up", "pitchbend_down", "pitchbend_mode", "no_modulation_connections"]
        
        #self.precache()

        if self.name:
            self.s.programtools.set_curr_by_name(self.name)
            self.update()
        else:
            print "No name..."
            
    def copy(self, destination_name):
        tools = self.gettools()
        tools.set_curr_by_name(self.name)
        tools.copy_program(destination_name)
        return ak.Program(self.s,destination_name)
        
    def init_recycled(self):
        # ultimately this should be a plugin or something, but for now...
        # updates a recycle generated program to the settings i prefer use
        for kg in self.get_keygroups():
            for zone in kg.zones:
                zone.set_playback(1) # ONE SHOT
            kg.set_polyphony(1)

    def get_keygroups(self):
        keygroups = []

        for i in range(self.no_keygroups):
            keygroups.append(ak.Keygroup(self,i))

        return keygroups

    def set_name(self, name):
        self.s.programtools.rename_curr(name)

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
                result.append("%d. %s => %s = %d" % (c.pin_index, ak.ModulationMatrix.sources[c.source], ak.ModulationMatrix.destinations[c.dest], c.level))
                
        return '\n'.join(result)
    
    def get_matrix(self, kgindex):
        n = self.s.programtools.get_no_modulation_connections()
        conns = { }

        kg = 0 # all

        for i in range(n):
            conn = self.s.programtools.get_modulation_connection(i, kg)
            conns[i] = ak.ModulationPin(self.s, i, conn[0], conn[1], conn[2], kg)
            c = conns[i]
            #print ak.ModulationMatrix.sources[c.source], '\t', ak.ModulationMatrix.destinations[c.dest], '\t', c.level
            
        return conns