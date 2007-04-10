from aksy.devices.akai.filemodel import Chunk
import struct

def create_chunk(name, spec, *bytes):
    raw_bytes = struct.pack(spec, *bytes)
    return Chunk(name, raw_bytes, 
            len(raw_bytes)+8)

class ChunkBuilder:
    def build(self, chunk, fh):
        fh.write(struct.pack("<sl", chunk.name, chunk.length))
    
class ProgramWriter:
    def __init__(self):
        self.programBuilder = ProgramBuilder()
        
    def write(self, program, fh):
        fh.write(self.programBuilder.build(program))
        
class ProgramBuilder:
    def build(self, program):
        return struct.pack('<4sl8sl6b 4sl8b 4sl24b', 
            'RIFF', 
            0, 
            'APRG'
            'prg ', 
            6, 
            1, # set to zero program was not read...
            program.midi_prog_no, 
            len(program.keygroups), 
            0, 
            0, 
            0, 
            'out ', 
            8, 
            0, 
            program.loudness, 
            program.amp_mod1, 
            program.amp_mod2, 
            program.pan_mod1, 
            program.pan_mod2, 
            program.pan_mod3, 
            program.velo_sens, 
            'tune', 
            24, 
            0, 
            program.semi, 
            program.fine, 
            program.a_detune, 
            program.ais_detune, 
            program.b_detune, 
            program.bes_detune, 
            program.c_detune, 
            program.cis_detune, 
            program.des_detune, 
            program.e_detune, 
            program.f_detune, 
            program.fis_detune, 
            program.g_detune, 
            program.gis_detune, 
            program.pitchbend_up, 
            program.pitchbend_down, 
            program.bend_mode, 
            program.aftertouch, 
            0, 
            0, 
            0, 
            0, 
            0)

class ModulationBuilder:
    def build(self, modulation):
        bytes = (0, 
            0, 
            0, 
            0, 
            0, 
            modulation.amp_src1, 
            0, 
            modulation.amp_src2, 
            0, 
            modulation.pan_src1, 
            0, 
            modulation.pan_src2, 
            0, 
            modulation.pan_src3, 
            0, 
            modulation.lfo1_rate_src, 
            0, 
            modulation.lfo1_delay_src, 
            0, 
            modulation.lfo1_depth_src, 
            0, 
            modulation.lfo2_rate_src, 
            0, 
            modulation.lfo2_delay_src, 
            0, 
            modulation.lfo2_depth_src, 
            # keygroup mod
            0, 
            modulation.pitch1_src, 
            0, 
            modulation.pitch1_src, 
            0, 
            modulation.amp_src, 
            0, 
            modulation.filter_input1, 
            0, 
            modulation.filter_input2, 
            0, 
            modulation.filter_input3,)
        return create_chunk('mods', "%iB" % len(bytes))

class ZoneBuilder:
    def build(self, zone):
        return create_chunk('zone', '<2b20s22bh2b', 
            0, 
            len(zone.samplename), 
            zone.samplename, 
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
            zone.low_vel, 
            zone.high_vel, 
            zone.fine, 
            zone.semi, 
            zone.filter, 
            zone.pan, 
            zone.playback, 
            zone.output, 
            zone.level, 
            zone.kb_track, 
            zone.velo_start, 
            0, 
            0)
