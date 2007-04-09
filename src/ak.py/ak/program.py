from utils.modelutils import *
from aksy.device import Devices
from samplerobject import samplerobject

class programs:
    programtypes = {0:"Keygroup", 1:"Drum"}

    def __init__(self,s):
        self.s = s
        pt = s.programtools
        self.no_items = pt.get_no_items()
        self.handles_names = pt.get_handles_names()
        self.names = pt.get_names()

        self.curr_handle = pt.get_curr_handle()
        if self.curr_handle != 268435455:
            self.curr_name = pt.get_curr_name()

        self.programdict = { }        

        i = 0

        while i < len(self.handles_names):
            self.programdict[self.handles_names[i]] = self.handles_names[i+1]
            i += 2

        self.programsmodel = get_model_from_list(self.programdict)
        self.programtypesmodel = get_model_from_list(programs.programtypes)
        #self.handles_names = pt.get_handles_names()
        #self.handles = pt.get_handles()
        #self.modified = pt.get_modified()

    def getCurr(self):
        if self.curr_handle in self.programdict:
            return program(self.s, self.programdict[self.curr_handle])
        else:
            return None
    
    def getProgram(self, name):
        return program(self.s, name)

class program(samplerobject):
    def __init__(self, s, name, handle = None):
        samplerobject.__init__(self,s,None,"programtools")

        self.name = name
        self.handle = handle

        self.specialattrs = ["name",]

        self.attrs = ["name", "type", "group_id", "genre", "program_no", "no_keygroups", "keygroup_xfade", "keygroup_xfade_type", "level", "polyphony", "portamento_enabled", "portamento_mode", "portamento_time", "glissando_mode", "aftertouch_mode", "aftertouch_value", "reassignment_method", "softpedal_loudness_reduction", "softpedal_attack_stretch", "softpedal_filter_close", "midi_transpose", "tune", "legato", "pitchbend_up", "pitchbend_down", "pitchbend_mode", "no_modulation_connections"]

        if self.name:
            self.s.programtools.set_curr_by_name(self.name)
            self.update()
        else:
            print "No name..."

    def set_name(self, name):
        self.s.programtools.rename_curr(name)

    def dump_matrix(self):
        n = self.s.programtools.get_no_modulation_connections()

        print "number of modulation connections", n

        conns = { }

        kg = 0 # all

        for i in range(n):
            conn = self.s.programtools.get_modulation_connection(i, kg)
            conns[i] = modulation_pin(self.s, i, conn[0], conn[1], conn[2], kg)

        for c in conns:
            c = conns[c]
            if c.source > 0:
                print modulation_matrix.sources[c.source], '\t', modulation_matrix.destinations[c.dest], '\t', c.level

class modulation_pin:
    def __init__(self, s, pin_index, source, dest, level, keygroup_index):
        self.s = s
        self.pin_index = pin_index
        self.source = source
        self.dest = dest
        self.level = level
        self.keygroup_index = keygroup_index

class modulation_matrix:
    # should be a total of 36 (0 based) * marks sample + hold mods
    sources      = ['NONE','MODWHEEL','BEND UP','BEND DOWN','AFTERTOUCH','VELOCITY','BIPOLAR VELOCITY','OFF VELOCITY','KEYBOARD','LFO1','LFO2','AMP ENV','FILTER ENV','AUX ENV','MIDI CTRL','Q-LINK 1','Q-LINK 2','Q-LINK 3','Q-LINK 4','Q-LINK 5','Q-LINK 6','Q-LINK 7','Q-LINK 8','*MODWHEEL','*BEND UP','*BEND DOWN','*Q-LINK 1','*Q-LINK 2','*Q-LINK 3','*Q-LINK 4','*Q-LINK 5','*Q-LINK 6','*Q-LINK 7','*Q-LINK 8','*LFO1','*LFO2','*MIDI CTRL']

    # should be a total of 52 (0 based), qlink adds 4 'EXT' options
    destinations = ['NONE',           'AMPLITUDE',    'PAN',            'PITCH',
                    'LFO1 RATE',      'LFO1 DEPTH',   'LFO1 DELAY',     'LFO1 PHASE',
                    'LFO1 OFFSET',    'LFO2 RATE',    'LFO2 DEPTH',     'LFO2 DELAY',
                    'LFO2 PHASE',     'LFO2 OFFSET',  'FILTER CUTOFF',  'FILTER RESONANCE',
                    'TR 1 CUTOFF',    'TR 1 RES',     'TR 2 CUTOFF',    'TR 2 RES',
                    'TR 3 CUTOFF',    'TR 3 RES',     'AMP ENV ATTACK', 'AMP ENV DECAY',
                    'AMP ENV RELEASE','FILT ENV R1',  'FILT ENV R2',    'FILT ENV R4',
                    'AUX ENV R1',     'AUX ENV R2',   'AUX ENV R4',     'ZONE CROSSFADE',
                    'ZONE 1 LEVEL',   'ZONE 1 PAN',   'ZONE 1 PITCH',   'ZONE 1 START', 'ZONE 1 FILTER'
                    'ZONE 2 LEVEL',   'ZONE 2 PAN',   'ZONE 2 PITCH',   'ZONE 2 START', 'ZONE 2 FILTER'
                    'ZONE 3 LEVEL',   'ZONE 3 PAN',   'ZONE 3 PITCH',   'ZONE 3 START', 'ZONE 3 FILTER'
                    'ZONE 4 LEVEL',   'ZONE 4 PAN',   'ZONE 4 PITCH',   'ZONE 4 START', 'ZONE 4 FILTER']

    def __init__(self,program,index):
        pass

