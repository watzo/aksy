NOTE_NAMES = 'a', 'b', 'bes', 'c', 'cis', 'd' 'es', 'e', 'f', 'fis', 'g', 'gis'

class Envelope:
    @staticmethod
    def create_default():
        env = Envelope()
        env.attack = 0
        env.decay = 50
        env.release = 15
        env.sustain = 100
        env.velo_to_attack = 0
        env.velo_on_to_release = 0
        env.velo_off_to_release = 0
        env.keyscale = 0
        return env

class AmpEnvelope(Envelope):
   pass

class FilterEnvelope(Envelope):
    @staticmethod
    def create_default():
        env = Envelope.create_default()
        env.filter_env_depth = 0
        return env
        
class AuxEnvelope:
    @staticmethod
    def create_default():
        env = Envelope()
        env.rate1 = 0
        env.rate2 = 50
        env.rate3 = 50
        env.rate4 = 15 
        env.level1 = 100 
        env.level2 = 100 
        env.level3 = 100 
        env.level4 = 0 
        env.velo_to_rate1 = 0
        env.kb_to_r2_r4 = 0
        env.velo_on_to_r4 = 0
        env.velo_off_to_r4 = 0
        env.velo_to_out_level = 0
        return env

class Filter:
    LP2P = 0
    LP4P = 1 
    LP4PPLUS = 2
    BP2P = 3
    BP4P = 4
    BP2PPLUS = 5
    HP1 = 6
    HP2 = 7
    HP8PLUS = 8
    LO_HI = 9
    LO_BAND = 10
    BAND_HI = 11
    NOTCH1 = 12
    NOTCH2 = 13
    NOTCH3 = 14
    NOTCH_WIDE = 15
    NOTCH_BI = 16
    PEAK1 = 17
    PEAK1 = 18
    PEAK1 = 19
    PEAK_WIDE = 20
    PEAK_BI = 21 
    PHASER1 = 22 
    PHASER2 = 23 
    PHASER_BI = 24 
    VOWEL = 25 

    HEADROOM_0db = 0
    HEADROOM_6db = 1
    HEADROOM_12db = 2
    HEADROOM_18db = 3
    HEADROOM_24db = 4
    HEADROOM_30db = 5
    
    @staticmethod
    def create_default():
        filter = Filter()
        filter.mode = 0 # 2 pole LP
        filter.cutoff = 100
        filter.resonance = 0
        filter.kb_track = 0
        filter.mod1_input = 0
        filter.mod2_input = 0
        filter.mod3_input = 0
        filter.headroom = 0
        return filter

class LFO:
    """ 
    >>> lfo = LFO(waveform=LFO.SAW_BI, rate_mod=36)
    """
    SINE = 0  
    TRIANGLE = 1
    SQUARE = 2
    SQUARE_PLUS = 3
    SQUARE_MINUS = 4
    SAW_BI = 5
    SAW_UP = 6
    SAW_DOWN = 7
    RANDOM = 8

    @staticmethod
    def create_default():
        lfo = LFO()
        lfo.waveform = LFO.TRIANGLE 
        lfo.rate = 43
        lfo.delay = 0
        lfo.depth = 0
        lfo.rate_mod = 0
        lfo.delay_mod = 0
        lfo.depth_mod = 0
        return lfo
 
class LFO1(LFO):
    @staticmethod
    def create_default(self):
        lfo = LFO.create_default()
        lfo.lfo_sync = 0
        lfo.phase = 0 # from sysex docs 
        lfo.lfo_shift   = 0 # from sysex docs 
        lfo.lfo_mid_clock_div = 0 # from sysex docs
        lfo.modwheel = 15
        lfo.aftertouch = 0
        return lfo
    
class LFO2(LFO):
    @staticmethod
    def create_default():
        lfo = LFO.create_default()
        lfo.lfo_retrigger = 0
        return lfo
        
class Modulation:
    """
    Contains modulation routings
    """

    NO_SOURCE = 0  
    MODWHEEL = 1
    BEND = 2 
    AFTERTOUCH = 3
    EXTERNAL = 4
    VELOCITY = 5
    KEYBOARD = 6 
    LFO1 = 7
    LFO2 = 8
    AMP_ENV = 9
    FILT_ENV = 10
    AUX_ENV = 11  
    MIDI_MODWHEEL = 12
    MIDI_BEND = 13
    MIDI_EXTERNAL = 14 
    
    @staticmethod
    def create_default():
        mod = Modulation()
        mod.amp_src1 = 6
        mod.amp_src2 = 3
        mod.pan_src1 = 8
        mod.pan_src2 = 6
        mod.pan_src3 = 1
        mod.lfo1_rate_src = 6
        mod.lfo1_delay_src = 6
        mod.lfo1_depth_src = 6
        mod.lfo2_rate_src = 0
        mod.lfo2_delay_src = 0
        mod.lfo2_depth_src = 0
        # keygroup mod
        mod.pitch1_src = 7
        mod.pitch2_src = 11 
        mod.amp_src = 11 
        mod.filter_input1 = 5 
        mod.filter_input2 = 8 
        mod.filter_input3 = 9 
        return mod

class Program:
    def __init__(self, keygroups):
        self.keygroups = keygroups
        
    @staticmethod
    def create_default(keygroups):
        program = Program(keygroups)
        program.midi_prog_no = 0
        program.no_keygrps = 1 
        program.loudness = 85
        program.amp_mod1 = 0
        program.amp_mod2 = 0
        program.pan_mod1 = 0
        program.pan_mod2 = 0
        program.pan_mod3 = 0
        program.velo_sens = 25
        program.semi = 0 
        program.fine = 0 
        program.a_detune = 0
        program.ais_detune = 0
        program.b_detune = 0
        program.bes_detune = 0
        program.c_detune = 0
        program.cis_detune = 0
        program.des_detune = 0
        program.e_detune = 0
        program.f_detune = 0
        program.fis_detune = 0
        program.g_detune = 0
        program.gis_detune = 0
        program.pitchbend_up = 2
        program.pitchbend_down = 2
        program.bend_mode = 0 # 1: held
        program.aftertouch = 0
        program.lfos = (LFO1(), LFO2(),)
        program.mod = Modulation()
        return program

class Keygroup:
    def __init__(self, zones):
        self.zones = zones
        
    @staticmethod
    def create_default(zones):
        kg = Keygroup(zones)
        kg.low_note=21 
        kg.high_note=127 
        kg.semi=0
        kg.fine=0 
        kg.override_fx=0
        kg.fx_send=0
        kg.pitch_mod1=100
        kg.pitch_mod2=0
        kg.amp_mod=0
        kg.zone_xfade=0
        kg.mute_group=0
        kg.envelopes = (AmpEnvelope(), FilterEnvelope(), AuxEnvelope())
        kg.filter = Filter()
        return kg

class Zone:
    @staticmethod
    def create_default():
        zone = Zone()
        # XXX: 2 bytes missing from description
        zone.samplename = '' # no sample assigned 
        zone.low_vel = 0
        zone.high_vel = 127
        zone.fine = 0
        zone.semi = 0
        zone.filter = 0
        zone.pan = 0
        zone.playback = 4 # as sample
        zone.output = 0 # multi
        zone.level = 0
        zone.kb_track = 1
        zone.velo_start = 0
        return zone
        
class Chunk:
    def __init__(self, name, bytes, length):
        self.name = name
        self.bytes = bytes
        self.length = length
    def get_length(self):
        return self.length
    def get_content_length(self):
        return self.length - 8
    
    def __repr__(self):
        return "<Chunk %s, length=%i, bytes=%s>" % (repr(self.name), self.length, repr(self.bytes))
        