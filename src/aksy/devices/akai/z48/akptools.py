from StringIO import StringIO
import struct, os.path, os

"""
Reading/writing AKP files

Based on http://mda.smartelectronix.com/akai/AKPspec.html
"""

WAVE_FORMAT_PCM = 0x0001

class Sample:
    """ Models a S5/6000/Z series sample
    which is an ordinary wave file with sampler chunks.
    -dwords manufacturer, product, period
    -midi note
    -pitch fraction
    -smtp format, offset, loopcount
    -loop defs 24 bytes (type, start, end, fraction, count)
    -s5000/6000 specific data:

       Length   Description           Default
       ----------------------------------------------------------------------
          2                           1,0
          1     Original root note    60
          1     Semitone tune +/-36   0
          1     Fine tune     +/-50   0
          1                           0     
          1     Play mode             0=NO LOOPING 1=ONE SHOT 2=LOOP IN REL 3=LOOP TIL REL
          3                           0,0,0
          4     Start point           0
          4     End point             (number of sample words)

    TODO: region support
    """
    def __init__(self, name, pitch, framerate, loops, data):
        self.name = name
        self.pitch = pitch 
        self.framerate = framerate
        self.loops = loops 
        self._sampwidth = 2
        self.nchannels = 1 
        self._nframes = len(data) / (self.nchannels * self._sampwidth)
        self._data = data

    def writefile(self):
        # based on code from the python wave module
        file = open(self.name + '.wav', 'wb')
        file.write('RIFF')
        self._datalength = self._nframes * self.nchannels * self._sampwidth
        data =  struct.pack('<l4s4slhhllhh',
            0, 'WAVE', 'fmt ', 16,
            WAVE_FORMAT_PCM, self.nchannels, self.framerate,
            self.nchannels * self.framerate * self._sampwidth,
            self.nchannels * self._sampwidth, self._sampwidth*8)
         
        file.write(data)
        file.write(self.get_sampler_chunk())
        data = struct.pack('<4sl', 'data', self._datalength)
        file.write(data)
        file.write(self._data)
        length = file.tell()
        file.seek(4)
        file.write(struct.pack('<l', length-8))
        file.close()

    def get_sampler_chunk(self):
        chunk = StringIO() 
            # fraction, smtpe format, offset, count, sampledata
        
        data = struct.pack( '<4s10l', 'smpl', 36 + 18 + 24 * len(self.loops), 
            71, 94, 1000000000/self.framerate, self.pitch, 0, 0, 0, len(self.loops), 18)
        chunk.write(data)
        for cue_id, loop, in enumerate(self.loops):
            chunk.write(loop.get_riff_wavechunk(cue_id))
        
        looptype = len(self.loops) > 0 and self.loops[0].type or 0
        loopstart = len(self.loops) > 0 and self.loops[0].start or 0
        loopend = len(self.loops) > 0 and self.loops[0].end or 0
        # remaining Sampler data
        # unkn, unkn, midi root, semitone t, fine t, unkn, playmode, unkn*3, loopstart, loopend
        chunk.write(
            struct.pack('<10Bll', 2, 0, self.pitch, 0, 0, 0, looptype, 0, 0, 0, loopstart, loopend))
        data =  chunk.getvalue()
        return data
        
class Loop:
    def __init__(self, type, start, end, fraction):
        self.start = start
        self.end = end 
        # 0: no looping, 1: looping 2: one shot
        self.type = type or 0
        self.fraction = 0
        self.count = 0

    def get_riff_wavechunk(self, cue_id):
        """ Returns the 24 byte loop chunk for the wave file
        """
        return struct.pack('<6l', cue_id, 0, self.start, self.end,
                           self.fraction, self.count)

class Base:
    def __init__(self, chunks={}, **kwargs):
        self._chunks = chunks
        self._chunk_index = 0
        if chunks is not None:
            self.setvalues()
            #self.setdefaults()
        else:
            self.setdefaults()
            for kw, value in kwargs.iteritems():
                if not hasattr(self, kw):
                    raise Exception("Unknown property: %s" % kw)
                setattr(self, kw, value)

    def curr_index(self, index, update=1):
        if index is None: 
            index = self._chunk_index
        self._chunk_index += update 
        return index 

    def read_chunk(self, fh, index=None):
        #
        if index is None:
            index = self.curr_index(index)
        fh.seek(index)
        
        bytes_read = fh.read(4)
        assert len(bytes_read) > 0
        
        length = struct.unpack('<l', bytes_read)[0]

        return length, fh.read(length) 

    def read_byte(self, index=None):
        index = self.curr_index(index) 
        return struct.unpack('<b', self._chunk[index])

    def read_string(self, chunk=None, index=None, length=None):
        if not chunk:
            chunk = self._chunk
        index = self.curr_index(index) 
        if length is None:
            length = struct.unpack('<b', chunk[index])[0]
            index = self.curr_index(index) 

        self.curr_index(index, length) 
        string = struct.unpack( '%is' %length, chunk[index: index+length])

class Modulation(Base):  
    """
    Contains modulation routings
    >>> mod = Modulation()
    >>> len(mod.create_chunk())
    46
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
    
    def setdefaults(self):
        self.amp_src1 = 6
        self.amp_src2 = 3
        self.pan_src1 = 8
        self.pan_src2 = 6
        self.pan_src3 = 1
        self.lfo1_rate_src = 6
        self.lfo1_delay_src = 6
        self.lfo1_depth_src = 6
        self.lfo2_rate_src = 0
        self.lfo2_delay_src = 0
        self.lfo2_depth_src = 0
        # keygroup mod
        self.pitch1_src = 7
        self.pitch2_src = 11 
        self.amp_src = 11 
        self.filter_input1 = 5 
        self.filter_input2 = 8 
        self.filter_input3 = 9 

    def create_chunk(self):
        return struct.pack('<4sl38b',
            'mods',
            38,
            0,
            0,
            0,
            0,
            0,
            self.amp_src1,
            0,
            self.amp_src2,
            0,
            self.pan_src1,
            0,
            self.pan_src2,
            0,
            self.pan_src3,
            0,
            self.lfo1_rate_src,
            0,
            self.lfo1_delay_src,
            0,
            self.lfo1_depth_src,
            0,
            self.lfo2_rate_src,
            0,
            self.lfo2_delay_src,
            0,
            self.lfo2_depth_src,
            # keygroup mod
            0,
            self.pitch1_src,
            0,
            self.pitch1_src,
            0,
            self.amp_src,
            0,
            self.filter_input1,
            0,
            self.filter_input2,
            0,
            self.filter_input3)

       
NOTE_NAMES = 'a','b', 'bes','c', 'cis', 'd' 'es', 'e', 'f', 'fis', 'g', 'gis'

class Program(Base):
    """
    >>> p = Program('sooperstrings.akp', 'w')
    >>> len(p.create_chunk())
    164
    
    >>> p.midi_prog_no = 1
    >>> p.lfos[0].waveform = LFO.SAW_BI 

    Note the lack of file extension with sample assigning:
    >>> p.keygroups.append(Keygroup())
    >>> p.keygroups[0].low_note = 25
    >>> p.keygroups[0].high_note = 126 
    >>> p.keygroups[0].zones[0].samplename = 'FSM Strings4 C1'
    >>> p.keygroups.append(Keygroup())
    >>> p.keygroups[1].zones[0].samplename = 'test'
    >>> p.keygroups[0].zones[0].low_vel = 33
    >>> p.keygroups[0].zones[0].high_vel = 35 
    >>> p.writefile()
    >>> rp = Program('smstrings.akp', 'r')

    """
    def __init__(self, filename=None, mode='r', **kwargs):
        self.filename = filename
        self._chunks = {}
        chunk = None
        if filename is not None and not os.path.exists(filename):
            raise IOError("File not found: " + filename)
        
        self.fh = file(filename, mode)
        self._read_chunks(self.get_file_length())
                # need more subchunks here
        Base.__init__(self, self._chunks, **kwargs)
        self.keygroups = []

    def get_file_length(self):
        return os.stat(self.filename).st_size
        
    def __del__(self):
        self.fh.close()

    def _read_chunks(self, filelength):
        # collects all chunks adding them to a dict with key chunk label,
        # data value. label and data length bytes are stripped.
        # first bytes are not according to standard, so start with prg chunk
        # prg
        offset = 0x15
        self.fh.seek(0, 1)
        length, self._chunks["prg "] = self.read_chunk(self.fh, offset)
        # prg length
        offset += length
        self._chunk = self._chunks["prg "]
        while offset < filelength:
            length = self.add_chunk(offset)
            if length == 0: break
            offset += length
        
    def add_chunk(self, offset):
        length, chunk = self.read_chunk(self.fh, offset)
        chunk_label = self.read_string(chunk, offset)
        self._chunks[chunk_label] = chunk[offset+4:]
        return length

    def setvalues(self):
        label = self.read_string(index=0x0, length=4)
        print repr(self._chunk)
        assert label == "APRG"
        assert self.read_string(0x5, 4) == "prg "
        self.midi_prog_no = self.read_byte(0x15) 
        self.no_keygrps = self.read_byte(0x16)
        self.loudness = self.read_byte(0x23)
        self.amp_mod1 = self.read_byte()
        self.amp_mod2 = self.read_byte()
        self.pan_mod1 = self.read_byte()
        self.pan_mod2 = self.read_byte()
        self.pan_mod3 = self.read_byte()
        self.velo_sens = self.read_byte()
        self.semi = self.read_byte(0x33)
        self.fine = self.read_byte()
        self.a_detune = self.read_byte()
        self.ais_detune = self.read_byte()
        self.b_detune = self.read_byte()
        self.bes_detune = self.read_byte()
        self.c_detune = self.read_byte()
        self.cis_detune = self.read_byte()
        self.des_detune = self.read_byte()
        self.e_detune = self.read_byte()
        self.f_detune = self.read_byte()
        self.fis_detune = self.read_byte()
        self.g_detune = self.read_byte()
        self.gis_detune = self.read_byte()
        self.pitchbend_up = self.read_byte()
        self.pitchbend_down = self.read_byte()
        self.bend_mode = self.read_byte()
        self.aftertouch = self.read_byte()
        self.lfos = (LFO1(chunk=self._chunk[0x4a:]), 
                     LFO2(chunk=self._chunk[0x4a:]),)
    
    def setdefaults(self):
        self.keygroups = [Keygroup()]
        self.midi_prog_no = 0
        self.no_keygrps = 1 
        self.loudness = 85
        self.amp_mod1 = 0
        self.amp_mod2 = 0
        self.pan_mod1 = 0
        self.pan_mod2 = 0
        self.pan_mod3 = 0
        self.velo_sens = 25
        self.semi = 0 
        self.fine = 0 
        self.a_detune = 0
        self.ais_detune = 0
        self.b_detune = 0
        self.bes_detune = 0
        self.c_detune = 0
        self.cis_detune = 0
        self.des_detune = 0
        self.e_detune = 0
        self.f_detune = 0
        self.fis_detune = 0
        self.g_detune = 0
        self.gis_detune = 0
        self.pitchbend_up = 2
        self.pitchbend_down = 2
        self.bend_mode = 0 # 1: held
        self.aftertouch = 0
        self.lfos = (LFO1(), LFO2(),)
        self.mod = Modulation()

    def create_chunk(self):
        chunk = StringIO()
        # explicitly setting little endian 
        # native mode aligns the longs. eek!
        chunk.write(struct.pack('<4sl8sl6b 4sl8b 4sl24b',
            'RIFF',
            0,
            'APRG'
            'prg ',
            6, 
            1, # set to zero program was not read...
            self.midi_prog_no,
            len(self.keygroups),
            0, 
            0,
            0,
            'out ',
            8,
            0,
            self.loudness,
            self.amp_mod1,
            self.amp_mod2,
            self.pan_mod1,
            self.pan_mod2,
            self.pan_mod3,
            self.velo_sens,
            'tune',
            24,
            0,
            self.semi,
            self.fine,
            self.a_detune,
            self.ais_detune,
            self.b_detune,
            self.bes_detune,
            self.c_detune,
            self.cis_detune,
            self.des_detune,
            self.e_detune,
            self.f_detune,
            self.fis_detune,
            self.g_detune,
            self.gis_detune,
            self.pitchbend_up,
            self.pitchbend_down,
            self.bend_mode,
            self.aftertouch,
            0,
            0,
            0,
            0,
            0))
        chunk.write(''.join([lfo.create_chunk() for lfo in self.lfos]))
        chunk.write(self.mod.create_chunk())
        return chunk.getvalue()

    def writefile(self):
        file = open(self.filename, 'wb')
        file.write(self.create_chunk())
        for kg in self.keygroups:
            file.write(kg.create_chunk())
        file.close()

    def __repr__(self):
        string_repr = StringIO()
        string_repr.write('<Akai Program')
        string_repr.write(''.join(['property: %s, val %s\n' % (item, val) 
                                for item,val in self.__dict__.iteritems()]))
        string_repr.write('>')
        return string_repr.getvalue()

class LFO(Base):
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

    def setdefaults(self):
        self.waveform = LFO.TRIANGLE 
        self.rate = 43
        self.delay = 0
        self.depth = 0
        self.rate_mod = 0
        self.delay_mod = 0
        self.depth_mod = 0

    def setvalues(self):
        self.waveform = self.read_byte(1) 
        self.rate = self.read_byte(1) 
        self.delay = self.read_byte(1) 
        self.depth = self.read_byte(1) 
        self.rate_mod = self.read_byte(1) 
        self.delay_mod = self.read_byte(1) 
        self.depth_mod = self.read_byte(1) 
 
class LFO1(LFO):
    """
    >>> lfo = LFO1(lfo_sync=1)
    >>> len(lfo.create_chunk())
    22
    """
    def setdefaults(self):
        LFO.setdefaults(self)
        self.lfo_sync = 0
        self.phase = 0 # from sysex docs 
        self.lfo_shift   = 0 # from sysex docs 
        self.lfo_mid_clock_div = 0 # from sysex docs
        self.modwheel = 15
        self.aftertouch = 0

    def create_chunk(self):
        return struct.pack('<4sl14b',
            'lfo ',
            14,
            0,
            self.waveform,
            self.rate,
            self.delay,
            self.depth,
            self.lfo_sync,
            0,
            self.modwheel,
            self.aftertouch,
            self.rate_mod,
            self.delay_mod,
            self.depth_mod,
            0,
            0)


class LFO2(LFO):
    """ 
    >>> lfo = LFO2(lfo_sync=1)
    Traceback (most recent call last):
    Exception: Unknown property: lfo_sync
    >>> lfo = LFO2(lfo_retrigger=1)
    >>> len(lfo.create_chunk())
    22
    """

    def setdefaults(self):
        LFO.setdefaults(self)
        self.lfo_retrigger = 0
        
    def create_chunk(self):
        return struct.pack('<4sl14b',
            'lfo ',
            14,
            0,
            self.waveform,
            self.rate,
            self.delay,
            self.depth,
            0,
            self.lfo_retrigger,
            0,
            0,
            self.rate_mod,
            self.delay_mod,
            self.depth_mod,
            0,
            0)


class Keygroup(Base):
    """ 
    Models a keygroup, a group that contains samples in zones

    >>> kg = Keygroup(blow_note=45)
    Traceback (most recent call last):
    Exception: Unknown property: blow_note
    >>> kg = Keygroup(low_note=45)
    >>> len(kg.create_chunk())
    352
    """
    def setdefaults(self):
        self.low_note=21 
        self.high_note=127 
        self.semi=0
        self.fine=0 
        self.override_fx=0
        self.fx_send=0
        self.pitch_mod1=100
        self.pitch_mod2=0
        self.amp_mod=0
        self.zone_xfade=0
        self.mute_group=0
        self.envelopes = (AmpEnvelope(), FilterEnvelope(), AuxEnvelope())
        self.filter = Filter()
        # always four zones
        self.zones= (Zone(), Zone(), Zone(), Zone(),)

    def create_chunk(self):
        chunk = StringIO()
        chunk.write(struct.pack('<4sl4sl16b',
            'kgrp',
            344,
            'kloc',
            16,
            0,
            0,
            0,
            0,
            self.low_note, 
            self.high_note, 
            self.semi,
            self.fine, 
            self.override_fx,
            self.fx_send,
            self.pitch_mod1,
            self.pitch_mod2,
            self.amp_mod,
            self.zone_xfade,
            self.mute_group,
            0))
        chunk.write(''.join([env.create_chunk() for env in self.envelopes]))
        chunk.write(self.filter.create_chunk()) 
        chunk.write(''.join([zone.create_chunk() for zone in self.zones]))
        return chunk.getvalue()


class Zone(Base):
    """
    >>> z = Zone()
    >>> len(z.create_chunk())
    56
    """
    def setdefaults(self):
        # XXX: 2 bytes missing from description
        self.samplename = '' # no sample assigned 
        self.low_vel = 0
        self.high_vel = 127
        self.fine = 0
        self.semi = 0
        self.filter = 0
        self.pan = 0
        self.playback = 4 # as sample
        self.output = 0 # multi
        self.level = 0
        self.kb_track = 1
        self.velo_start = 0

    def create_chunk(self):
        return struct.pack('<4sl2b20s22bh2b',
            'zone',
            48,
            0,
            len(self.samplename),
            self.samplename,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            self.low_vel,
            self.high_vel,
            self.fine,
            self.semi,
            self.filter,
            self.pan,
            self.playback,
            self.output,
            self.level,
            self.kb_track,
            self.velo_start,
            0,
            0)

class Filter(Base):
    """
    >>> f = Filter(mode=Filter.NOTCH_BI)
    """
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
    
    def setdefaults(self):
        self.mode = 0 # 2 pole LP
        self.cutoff = 100
        self.resonance = 0
        self.kb_track = 0
        self.mod1_input = 0
        self.mod2_input = 0
        self.mod3_input = 0
        self.headroom = 0

    def create_chunk(self):
        return struct.pack('<4sl10b',
            'filt',
            10,
            0,
            self.mode,
            self.cutoff,
            self.resonance,
            self.kb_track,
            self.mod1_input,
            self.mod2_input,
            self.mod3_input,
            self.headroom,
            0)

class Envelope(Base):
    def setdefaults(self):
        self.attack = 0
        self.decay = 50
        self.release = 15
        self.sustain = 100
        self.velo_to_attack = 0
        self.velo_on_to_release = 0
        self.velo_off_to_release = 0
        self.keyscale = 0


class AmpEnvelope(Envelope):
    """
    >>> amp = AmpEnvelope()
    >>> len(amp.create_chunk()) 
    26
    """
    def create_chunk(self):
        return struct.pack('<4sl18b',
            'env ',
            18,
            0,
            self.attack,
            0,
            self.decay,
            self.release,
            0,
            0,
            self.sustain,
            0,
            0,
            self.velo_to_attack,
            0,
            self.keyscale,
            0,
            self.velo_on_to_release,
            self.velo_off_to_release,
            0,
            0)


class FilterEnvelope(Envelope):
    """
    >>> filt_env = FilterEnvelope()
    >>> len(filt_env.create_chunk()) 
    26
    """
    def setdefaults(self):
        Envelope.setdefaults(self)
        self.filter_env_depth = 0
        
    def create_chunk(self):
        return struct.pack('<4sl18b',
            'env ',
            18,
            0,
            self.attack,
            0,
            self.decay,
            self.release,
            0,
            0,
            self.sustain,
            0,
            self.filter_env_depth,
            self.velo_to_attack,
            0,
            self.keyscale,
            0,
            self.velo_on_to_release,
            self.velo_off_to_release,
            0,
            0)

class AuxEnvelope(Base):
    """
    >>> aux_env = AuxEnvelope()
    >>> len(aux_env.create_chunk()) 
    26
    """
    def setdefaults(self):
        self.rate1 = 0
        self.rate2 = 50
        self.rate3 = 50
        self.rate4 = 15 
        self.level1 = 100 
        self.level2 = 100 
        self.level3 = 100 
        self.level4 = 0 
        self.velo_to_rate1 = 0
        self.kb_to_r2_r4 = 0
        self.velo_on_to_r4 = 0
        self.velo_off_to_r4 = 0
        self.velo_to_out_level = 0

    def create_chunk(self):
        return struct.pack('<4sl18b',
            'env ',
            18,
            0,
            self.rate1,
            self.rate2,
            self.rate3,
            self.rate4,
            self.level1,
            self.level2,
            self.level3,
            self.level4,
            0,
            self.velo_to_rate1,
            0,
            self.kb_to_r2_r4,
            0,
            self.velo_on_to_r4,
            self.velo_off_to_r4,
            self.velo_to_out_level,
            0)

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
    amp = pow(2, 15) - 1
    samplerate = 44100
    no_samples = 1 * samplerate
    loops = (Loop(0, 0, no_samples, 0),)
    freq = 441.0/samplerate
    import math
    samples = []
    for s in range(no_samples):
       samples.append(struct.pack('<h', math.sin(freq * s * 2 * math.pi) * amp))
    samples = ''.join(samples)
    sample = Sample('test', 91, samplerate, loops, samples)
    sample.writefile()

