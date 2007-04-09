import os, struct
from StringIO import StringIO
from z48.akptools import Keygroup

# TODO move this to model.
class Program:
    def __init__(self, keygroups):
        self.keygroups = keygroups

class Keygroup:
    def __init__(self, zones):
        self.zones = zones

class Zone:
    def __init__(self):
        pass
        
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
        
def parse_byte(chunk, offset):
    return 1, struct.unpack('<b', self._chunk[offset])

def parse_string(chunk, offset, length=None):
    if length is None:
        length = struct.unpack('B', chunk[offset:offset+1])[0]
        offset += 1
        
    return length, struct.unpack('%is' %length, chunk[offset: offset+length])[0]
        
class ChunkParser:
    def parse(self, fh, offset):
        bytes_read = fh.read(4)
        assert len(bytes_read) == 4
        size, name = parse_string(bytes_read, 0, 4)
        bytes_read = fh.read(4)
        assert len(bytes_read)
        length = struct.unpack('<l', bytes_read)[0]
        bytes = fh.read(length)
        return Chunk(name, bytes, length+8)

    def parse_chunks(self, fh, offset, end):
        chunks = []
        while offset < end:
            chunk = self.parse(fh, offset)
            offset += chunk.length
            chunks.append(chunk)
        return chunks


def get_file_length(filename):
        return os.stat(filename).st_size
    
class ProgramParser:
    def __init__(self):
        self.chunkParser = ChunkParser()
        self.keygroupParser = KeygroupParser()
        self.chunks = []
        
    def parse_chunks(self, filelength):
        offset = 0x0c
        self.fh.seek(offset)
        return self.chunkParser.parse_chunks(self.fh, offset, filelength)

    def parse_keygroups(self):
        keygroups = []
        for chunk in self.chunks:
            if chunk.name == "kgrp":
                keygroups.append(self.keygroupParser.parse(chunk))
        return keygroups
            
    def parse(self, filename):
        self.fh = file(filename, 'rb')
        self.chunks = self.parse_chunks(get_file_length(filename))
        prg = Program(self.parse_keygroups())
        return prg

class KeygroupParser:
    def __init__(self):
        self.chunkParser = ChunkParser()
        self.zoneParser = ZoneParser()
        self.chunks = []
        
    def parse_zones(self, chunks):
        zones = []
        for chunk in chunks:
            if chunk.name == "zone":
                zones.append(self.zoneParser.parse(chunk))
        return zones
    
    def parse(self, chunk):
        chunks = self.chunkParser.parse_chunks(StringIO(chunk.bytes), 0, chunk.get_content_length())
        kg = Keygroup(self.parse_zones(chunks))
        return kg
    
class ZoneParser:
    def parse(self, chunk):
        zone = Zone()
        length, zone.samplename = parse_string(chunk.bytes, 1)
        return zone