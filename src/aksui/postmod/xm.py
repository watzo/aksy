
import string, os, traceback, time, array, copy
import autobin, filex, utilx, sample, audioopx, filex

DEFAULT_HEADER_SIZE = 276
DEFAULT_BLANKINSTRUMENT_HEADER_SIZE = 29
DEFAULT_INSTRUMENT_HEADER_SIZE = 243

DEFAULT_PATTERN_ROWS = 64

EVENT_NULL_NOTE = 0
EVENT_NULL_INSTRUMENT = 0
EVENT_NULL_VALUE = 0

EVENT_NOTE_CUT = 97
EVENT_NOTE_OFF = 97

NOTE_MIN = 1
NOTE_MAX = 96

MAX_TRACKS = 32


def midiNoteToXMNote(note):
    return note-12+1

def XMNoteToMidiNote(note):
    return note-1+12


# note: 0 is null volume.  volume 0 is 16 and volumes go up from there.



class XMHeader:

    vars = "id,songName,char1,trackerName,versionNumber,headerSize,numOrders,restartPosition,numTracks,numPatterns,numInstruments,flags,initialSpeed,initialTempo,orders".split(",")
    formats = {
        'id': "<17s",
        'songName': "<20s",
        'char1': "<B",
        'trackerName': "<20s",
        'versionNumber': "<h",
        'headerSize': "<i",
        'numOrders': "<h",
        'restartPosition': "<h",
        'numTracks': "<h",
        'numPatterns': "<h",
        'numInstruments': "<h",
        'flags': "<h",
        'initialSpeed': "<h",
        'initialTempo': "<h",
        'orders': "<256B"
        }        
            
    def __init__(self):
        self.id = "Extended Module: "    
        # strings are NOT null terminated

        self.songName = chr(0) * 20  # 20 chars, padded with zeroes
        self.char1 = chr(0x1A)

        self.trackerName = "FastTracker v2.00"
        self.versionNumber = 0x0104     # docs are for $0104, hi-byte is major, lo-byte minor
        self.headerSize = DEFAULT_HEADER_SIZE 
        
        self.numOrders = 0      # song length
        self.restartPosition = 0
        self.numTracks = 32     # 2,4,6,8..32
        self.numPatterns = 0    # max 256
        self.numInstruments = 0 # max 128

        self.flags = 0          # bit 0: 0 = Amiga freq table, 1 = linear freq table

        self.initialTempo = 140
        self.initialSpeed = 6

        self.orders = [0] * 256        
        
        # not stored in file
        self.extra = ""
                

    def load(self, fp):
        autobin.autoload(fp, self)
        if self.headerSize > DEFAULT_HEADER_SIZE:
            self.extra = fp.read(self.headerSize - DEFAULT_HEADER_SIZE)

    def save(self, fp):
        autobin.autosave(fp, self)
        if self.extra:
            fp.write(self.extra)

    def dump(self):
        autobin.autodump(self)

    def isValid(self):
        return (self.id.upper() == "EXTENDED MODULE: ")


class XMSample:
    vars = "length,loopStart,loopEnd,volume,fineTune,flags,panning,transpose,reserved,name".split(",")
    formats = {
        'length': '<i',
        'loopStart': '<i',
        'loopEnd': '<i',
        'volume': '<B',
        'fineTune': '<b',
        'flags' : '<B',
        'panning' : '<B',
        'transpose' : '<b',
        'reserved': '<b',
        'name' : '<22s'
    }
    
    def __init__(self):
        self.length = 0         # int - sample length
        self.loopStart = 0      # int
        self.loopEnd = 0        # int
        self.volume = 0         # byte
        self.fineTune = 0       # signed byte, -16..+15
        self.flags = 0       # byte, bit 0-1: 0= no loop, 1 = forward loop. 2: ping pong. 4: 16-bit data.
        self.panning = 0        # byte 0-255
        self.transpose = 0     # signed byte - relative note number (transpose?)
        self.reserved = 0       # byte
        self.name = ""          # 22 chars

        self.data = ""
        self.__cacheData = ""

        # compatibility
        self.filename = ""

    def numSamples(self):
        #TODO: is this right?
        return self.length

    def save(self, fp, pos=-1):
        if pos <> -1: fp.seek(pos)
        self.beginHeaderPos = fp.tell()
        autobin.autosave(fp, self)
        self.endHeaderPos = fp.tell()

    def saveData(self, fp):
        fp.write(self.data)
        

    def load(self, fp, pos=-1):
        """loads header from an open file."""
        if pos <> -1: fp.seek(pos)
        self.beginHeaderPos = fp.tell()
        autobin.autoload(fp, self)
        self.endHeaderPos = fp.tell()

    def loadData(self, fp):
        if self.getBitsPerSample() == 16:
            self.data = array.array("H")
        else:
            self.data = array.array("b")
        self.data.fromstring(fp.read(self.length))
        self.__cacheData = ""

    def getBitsPerSample(self):
        if self.flags & 4:
            return 16
        else:
            return 8

    def getSampleRate(self):
        return 44100

    def getNumChannels(self):
        return 1

    def savefile(self, path, type="wav", modpath=None):
        """save to sound file, currently only supports mono.  modpath for it compatibility only."""
        x = sample.Sample()
        x.setType(type)
        x.setRate(self.getSampleRate())
        x.setBits(self.getBitsPerSample())
        x.setChannels(self.getNumChannels())

        x.data = self.getData(cache=1, cacheLimit=50000)

        path = filex.requireExt(path, ".wav")
        x.save(path)


    def lenData(self):
        #TODO: is this the same as getData?
        return len(self.data)

    def getData(self, cache=1, cacheLimit=100000):
        """returns data in normal format (not delta).  if cache, caches normal data in memory,
        unless it is larger than cacheLimit bytes."""

        if cache and self.__cacheData:
            return self.__cacheData.tostring()

        #print self.getBitsPerSample()
        #print self.flags
        bits = self.getBitsPerSample()
        if bits == 16:
            data = array.array("H")
        else:
            data = array.array("b")
        old = 0
        for i in range(len(self.data)):
            new = self.data[i] + old
            #print new
            try:
                data.append(new)
            except:
                pass
                #print "no", new
            old = new

        if cache and len(data) <= cacheLimit:
            self.__cacheData = data
        
        if bits == 8:
            data = audioopx.toggleSigned8bit(data.tostring())
        else:
            data = data.tostring()
        return data
    
                
        
        
        

class XMInstrument:
    vars = "headerSize,name,type,numSamples".split(",")
    formats = {
        'headerSize': "<i",
        'name': "<22s",
        'type': "<B",
        'numSamples': "<h"
        }        

    vars2 = "sampleHeaderSize,sampleNumbers,volumeEnvelope,panningEnvelope,lenVolumeEnvelope,lenPanningEnvelope,volumeSustainPoint,volumeLoopStart,volumeLoopEnd,panningSustainPoint,panningLoopStart,panningLoopEnd,volumeType,panningType,vibratoType,vibratoSweep,vibratoDepth,vibratoRate,volumeFadeOut,reserved".split(",")
    formats2 = {
        'sampleHeaderSize': '<i',
        'sampleNumbers': '<96s',
        'volumeEnvelope': '48s',
        'panningEnvelope': '48s',
        'lenVolumeEnvelope': '<B',
        'lenPanningEnvelope': '<B',
        'volumeSustainPoint': '<B',
        'volumeLoopStart': '<B',
        'volumeLoopEnd': '<B',
        'panningSustainPoint': '<B',
        'panningLoopStart': '<B',
        'panningLoopEnd': '<B',
        'volumeType': '<B',
        'panningType': '<B',
        'vibratoType': '<B',
        'vibratoSweep': '<B',
        'vibratoDepth': '<B',
        'vibratoRate': '<B',
        'volumeFadeOut': '<h',
        'reserved': '<h'
    }        
            
    def __init__(self, index=0):
        self.headerSize = 0     # int
        self.name = ""          # 22 chars
        self.type = 0           # byte - "always 0" - but not always 0
        self.numSamples = 0     # word

        # if numSamples > 0, then these follow:    
        self.sampleHeaderSize = 0        # int
        self.sampleNumbers = [0] * 96    # 96 bytes - sample numbers for all notes
        self.volumeEnvelope = [0] * 48   # 48 bytes - volume envelope points
        self.panningEnvelope = [0] * 48  # 48 bytes - panning envelope points
        self.lenVolumeEnvelope = 0      # byte - num volume envelope points
        self.lenPanningEnvelope = 0     # byte - num panning envelope points
        self.volumeSustainPoint = 0     # byte
        self.volumeLoopStart = 0        # byte
        self.volumeLoopEnd = 0          # byte
        self.panningSustainPoint = 0    # byte
        self.panningLoopStart = 0       # byte
        self.panningLoopEnd = 0         # byte
        self.volumeType = 0             # byte 0: on. 1: sustain. 2: loop.
        self.panningType = 0            # byte 0: on. 1: sustain. 2: loop.
        self.vibratoType = 0            # byte
        self.vibratoSweep = 0            # byte
        self.vibratoDepth = 0           # byte
        self.vibratoRate = 0            # byte
        self.volumeFadeOut = 0          # word
        self.reserved = 0               # word

        self.extra = ""     # instrument size tends to be more than just the above, so there is extra.

        # after instrument header comes all sample headers for the instrument, then all sample data
        # for those samples.

        # one example: blank instruments had 4 extra chars: ['(', '\x00', '\x00', '\x00']
        # and regular instruments has 20 \x00 chars.

        self.index = index    # our index in the global instrument list    
        self.samples = []        

    def load(self, fp, pos=-1):
        """loads from an open file."""
        if pos <> -1: fp.seek(pos)
        self.beginHeaderPos = fp.tell()
        autobin.autoload(fp, self)
        if self.numSamples > 0:
            autobin.autoload(fp, self, self.vars2, self.formats2)
            if self.headerSize > DEFAULT_INSTRUMENT_HEADER_SIZE:
                self.extra = fp.read(self.headerSize - DEFAULT_INSTRUMENT_HEADER_SIZE)
                #print "extra", list(self.extra)
        else:
            if self.headerSize > DEFAULT_BLANKINSTRUMENT_HEADER_SIZE:
                self.extra = fp.read(self.headerSize - DEFAULT_BLANKINSTRUMENT_HEADER_SIZE)
                #print "extra(blank)", list(self.extra)
            
        self.endHeaderPos = fp.tell()

        self.loadSamples(fp)



    def usedSamples(self):
        """ returns list of samples used by this instrument, with indexes to master sample table """
        #TODO: should it be 1-based?
        # we need to know our own index in the instrument list to transpose and get the right values
        samps = range(self.numSamples)
        samps = [x+1+self.index for x in samps]
        return samps


    def loadSamples(self, fp):
        # first read headers
        for i in range(self.numSamples):
            sample = XMSample()
            sample.load(fp)
            self.samples.append(sample)
        # now read data
        for s in self.samples:
            s.loadData(fp)

    def save(self, fp, pos=-1):
        if pos <> -1: fp.seek(pos)
        self.beginHeaderPos = fp.tell()
        autobin.autosave(fp, self)
        if self.numSamples > 0:
            autobin.autosave(fp, self, self.vars2, self.formats2)
        if self.extra:
            fp.write(self.extra)
        self.endHeaderPos = fp.tell()

        self.saveSamples(fp)        

    def saveSamples(self, fp):
        # first save headers
        for samp in self.samples:
            samp.save(fp)
        # then save data
        for samp in self.samples:
            samp.saveData(fp)

            
        

                
            
        


class XMPackedPattern:

    vars = "headerLength,packingType,rows,length".split(",")
    formats = {
        'headerLength': "<i",
        'packingType': "<B",
        'rows': "<h",
        'length': "<h"
        }        
            
    def __init__(self, numTracks):
        self.headerLength = 9       # int, header length
        self.packingType = 0        # byte, always 0
        self.rows = 0               # word, 1..256
        self.length = 0             # word, if 0, pattern is empty and has no data

        self.data = ""      # packed data

        # not stored in file
        self.beginHeaderPos = 0
        self.endHeaderPos = 0

        self.numTracks = numTracks  # set in mod header, and required for loading patterns.


    def load(self, fp, pos=-1):
        """loads from an open file."""
        if pos <> -1:
            fp.seek(pos)
        self.beginHeaderPos = fp.tell()
        autobin.autoload(fp, self)
        if self.length:
            self.data = fp.read(self.length)
        self.endHeaderPos = fp.tell()

    def save(self, fp, pos=-1):
        """saves to an open file."""
        if pos <> -1:
            fp.seek(pos)
        curpos = fp.tell()
        self.beginHeaderPos = curpos
        autobin.autosave(fp, self)
        fp.write(self.data)
        self.endHeaderPos = fp.tell()

        if not self.data:
            curpos = 0
            self.beginHeaderPos = self.endHeaderPos = 0

        self.changedSinceSave = 0            

    def isBlank(self):
        # TODO: check if XM needs the replace
        # pattern is blank if data is blank or has no non-0 characters
        minuszeroes = string.replace(self.data, "\x00", "")
        return not bool(minuszeroes)


    # packing scheme:
    # sets of 5 bytes
    # either all 5 values straight (note, instrument, volume, command, commandvalue)
    # OR the first byte tells which bytes follow out of those 5

    def unpack(self):
        pattern = XMPattern(rows=self.rows, tracks=self.numTracks)
        data = array.array("B", self.data)
        offset = 0
        for row in range(self.rows):
            for track in xrange(self.numTracks):
                note = instrument = volume = command = commandValue = 0
                content = data[offset]
                if (content & 0x80):
                    offset += 1
                else:
                    content = 0x1F

                # note
                if (content & 0x01):
                    note = data[offset]
                    offset += 1
                    #TODO:
                    #if (note == 97):
                    #    pass
                    #    command = 0x0A
                    #    commandValue = 0x00
                    #else:
                    #    note = note - 1
                    #if note != 97:
                    #    note -= 1

                # instrument
                if (content & 0x02):
                    instrument = data[offset]
                    offset += 1

                # volume
                if (content & 0x04):
                    volume = data[offset]
                    offset += 1

                # command
                if (content & 0x08):
                    command = data[offset]
                    offset += 1

                # command value
                if (content & 0x10):
                    commandValue = data[offset]
                    offset += 1

                if (note,instrument,volume,command,commandValue) != (0,0,0,0,0):
                    #pattern.set(track, row, note, instrument, volume, command, commandValue)
                    #HACK: speed hack
                    pattern.data[(track,row)] = [note, instrument, volume, command, commandValue]
                    
                    #print row, track, note, instrument
                
        return pattern



    def unpackslo(self):
        pattern = XMPattern(self.numTracks)
        offset = 0
        for row in range(self.rows):
            for track in xrange(self.numTracks):
                note = instrument = volume = command = commandValue = 0
                content = ord(self.data[offset])
                if (content & 0x80):
                    offset += 1
                else:
                    content = 0x1F

                # note
                if (content & 0x01):
                    note = ord(self.data[offset])
                    offset += 1
                    #TODO:
                    #if (note == 97):
                    #    pass
                    #    command = 0x0A
                    #    commandValue = 0x00
                    #else:
                    #    note = note - 1
                    if note != 97:
                        note -= 1

                # instrument
                if (content & 0x02):
                    instrument = ord(self.data[offset])
                    offset += 1

                # volume
                if (content & 0x04):
                    volume = ord(self.data[offset])
                    offset += 1

                # command
                if (content & 0x08):
                    command = ord(self.data[offset])
                    offset += 1

                # command value
                if (content & 0x10):
                    commandValue = ord(self.data[offset])
                    offset += 1

                if (note,instrument,volume,command,commandValue) != (0,0,0,0,0):
                    #pattern.set(track, row, note, instrument, volume, command, commandValue)
                    #HACK: speed hack
                    pattern.data[(track,row)] = [note, instrument, volume, command, commandValue]
                    
                    #print row, track, note, instrument
                
        return pattern


class XMPattern:
    def __init__(self, rows=DEFAULT_PATTERN_ROWS, tracks=0):
        self.numRows = rows
        self.__numTracks = tracks
        self.tracks = []
        self.data = {}

        self.__i = 0        

    def __iter__(self):
        return self

    def next(self):        
        try:
            position,event = self.data.items()[self.__i]
            self.__i += 1
            return event, position
        except IndexError:
            self.__i = 0
            raise StopIteration

    def set(self, track, row, note, instrument, volume, command, commandValue):
        #print track, row, note, instrument, volume, command, commandValue
        self.data[(track,row)] = [note, instrument, volume, command, commandValue]

    def setEvent(self, track, row, event):
        self.data[(track,row)] = event

    def get(self, track, row):
        return self.data.get((track,row), (0,0,0,0,0))

    __call__ = get

    def getNumTracks(self):
        return __self.numTracks

    numTracks = getNumTracks    

    def getNumRows(self):
        return self.numRows

    def copy(self, target):
        for key, value in self.data.items():
            target.set(key[0], key[1], value[0], value[1], value[2], value[3], value[4])


    def getLastRow(self):
        # return last playback row - either total number of rows, or row where D command occurs.
        termrow = 10000
        # we have to loop through all events because they may be out of order
        for position,event in self.data.items():
            if event[3] == 13:
                termrow = min(termrow, position[1])

        if termrow < 10000:
            return termrow
        else:
            return self.numrows



    def areTrackNotesEmpty(self, track):
        """returns true if all events is specified track of this pattern are empty of note data (note or instrument values)."""

        # the IT formula for whether a note is empty:
        #if self.note in [EVENT_NULL_NOTE, EVENT_NOTE_OFF] and self.instrument == EVENT_NULL_INSTRUMENT

        # but blank instruments are not notes in XM.  97 is key off.

        for position,event in self.data.items():
            if position[0] == track:
                if event[0] not in (0,97):
                    return 0
        return 1


    def makeSolo(self, tracks):
        """clear all tracks except specified track(s)"""
        # allow user to pass single track or list of tracks
        tracks = utilx.tolist(tracks)

        for position,event in self.data.items():
            if position[0] not in tracks:
                # clear this event
                event[0:3] = [0,0,0]    # note, ins, volume
                # commands to keep: D (pattern break), F (speed/tempo), G,H (global volume), (13,15,16,17)
                if event[3] not in (13,15,16,17):
                    event[3:] = [0,0]
                


    def usedInstruments(self):
        """returns list of what instruments are used in this pattern"""
        instruments = {}
        for position,event in self.data.items():
            if event[1] not in (0,97):
                instruments[event[1]] = 1
        return instruments.keys()
                

    # packing scheme:
    # sets of 5 bytes
    # either all 5 values straight (note, instrument, volume, command, commandvalue)
    # OR the first byte tells which bytes follow out of those 5

    def pack(self):
        pattern = XMPackedPattern(self.__numTracks)
        pdata = []  # the packed data, list of ints
        data = self.data
        offset = 0
        for row in xrange(self.numRows):
            for track in xrange(self.__numTracks):
                note, instrument, volume, command, commandValue = data.get((track,row), (0,0,0,0,0))
                # now make mask byte
                thevals = []
                mask = 0
                if note: mask = mask | 0x01; thevals.append(note)
                if instrument: mask = mask | 0x02; thevals.append(instrument)
                if volume: mask = mask | 0x04; thevals.append(volume)
                if command: mask = mask | 0x08; thevals.append(command)
                if commandValue: mask = mask | 0x10; thevals.append(commandValue)
                # 0x1F means all values, ie, no packing
                if mask == 0x1F:
                    pdata += thevals
                else:
                    pdata += ([mask | 0x80] + thevals)
        pattern.data = array.array("B", pdata).tostring()
        pattern.rows = self.numRows
        pattern.length = len(pattern.data)
        #TODO: does updating numtracks require us to update numtracks in the module header? probably.  probably somewhere else.
        return pattern        
        
                    
            
            

class XMModule:
    def __init__(self, fname=None, unpack=1, loadSampleData=1):
        self.header = XMHeader()
        self.patterns = []      # unpacked patterns
        self.ppatterns = []     # packed patterns
        self.samples = []
        self.instruments = []

        self.packed = 1
        self.unpacked = 0

        self.corrupt = 0
        self.corruption = 0
        self.corruptSamples = 0
        self.corruptInstruments = 0

        self.unlimitedSamples = 0        

        self.path = ""        

        self.unpacking = 0

        self.__gettingBlanks = 0
        self.blanks = []    # list of blank patterns

        # for iteration
        self.__track = 0
        self.__pattern = 0
        self.__row = 0

        self.modtype = "XM"
        self.ext = ".xm"
        self.MAX_TRACKS = MAX_TRACKS

        if fname:
            self.load(fname)

    def getNewPattern(self):
        return XMPattern()

    def parseFlags(self):
        pass


    def orderList(self):
        return self.header.orders[:self.header.numOrders]

    def isOrderListEmpty(self):
        return (not len(self.orderList()))

    def setOrderList(self, list):
        self.header.orders = list[:256]
        self.header.numOrders = len(list)
        if len(self.header.orders) < 256:
            self.header.orders += ([0] * 256-len(self.header.orders))

    def getPatternOrder(self, pattern):
        # return orderlist index of specified pattern, or None
        try:
            return self.header.orders.index(pattern)
        except ValueError:
            return None

    def getLastRow(self, pattern):
        return self.patterns[pattern].getLastRow()


    def save(self, path, pack=1, checkpack=1):
        if pack:
            self.pack(checkpack)

        #self.header.resize(len(self.samples), len(self.instruments), len(self.ppatterns))
        #self.header.prepareForSave()
            
        f = open(path, "wb")
        #self.setFlags()
        self.header.save(f)

        for p in self.ppatterns:
            p.save(f)

        for i in self.instruments:
            i.save(f)

        self.path = path        
        

    def load(self, path, unpack=1, loadSampleData=1, checkValid=1, checkpack=1):
        #unpack=1

        try:
            #print "loading", path
            if not os.path.exists(path):
                return 0

            try:
                filesize = os.stat(path)[stat.ST_SIZE]
                if filesize == 0:
                    print path, "has no data!"
                    self.corruption += 1
                    self.corrupt = 1
                    return 0
            except:
                pass
            
            f = open(path, "rb")

            """
            headerid = f.read(4)
            if string.upper(headerid) != "IMPM":
                f.seek(0)
                headerid = f.read(8)
                if headerid == "ziRCONia":
                    print path, "is MMCMP-compressed, can't load it."
                else:
                    print path, "header is corrupt, or is not an IT file."
                self.corruption += 1
                self.corrupt = 1
                return 0
            """

            #f.seek(0)
                    
            try:            
                self.header.load(f)
                self.parseFlags()
            except:
                print path, "header is corrupt, or is not an XM file."
                self.corruption += 1
                self.corrupt = 1
                traceback.print_exc()
                return 0
            
            if checkValid and not self.header.isValid():
                print path, "header is corrupt, or is not an XM file."
                self.corruption = self.corrupt + 1
                self.corrupt = 1
                return 0

            # load patterns
            self.ppatterns = []
            for i in range(self.header.numPatterns):
                self.ppatterns.append(XMPackedPattern(self.header.numTracks))
                self.ppatterns[-1].load(f)

            print "loaded", len(self.ppatterns), "patterns"

            # load instruments and samples
            self.instruments = []
            self.samples = []
            for i in range(self.header.numInstruments):
                self.instruments.append(XMInstrument(index=i))
                #print "loading instrument", i
                self.instruments[-1].load(f)
                self.samples += self.instruments[-1].samples

            print "loaded", len(self.instruments), "instruments", len(self.samples), "samples"
            
            """
            if self.corruptSamples and self.corruptSamples >= len(self.samples):
                self.corrupt = 1
            """
            
            if self.corrupt:
                print "failed loading, module is corrupt"
                return 0
                

            # set endfilepos
            f.seek(0, 2)
            self.header.endFilePos = f.tell()


            # load header extra data, if any
            #chunk = self.headerExtraChunk()
            #if chunk[1]-chunk[0] > 0:
            #    self.header.loadExtra(f, chunk[0], chunk[1])
                
            f.close()

            self.packed = 1
            self.unpacked = 0
            if unpack:
                try:
                    a = time.time()
                    self.unpack(checkpack)
                    print ".. unpacked in", time.time() - a
                except:
                    print "failed unpacking"
                    traceback.print_exc()
            
            self.path = path
            return 1


        except:
            print "failed loading", path
            traceback.print_exc()
            return 0


    def pack(self, check=1):
        """ pack patterns """
        if check and self.packed:
            return

        self.ppatterns = []
        for p in self.patterns:
            self.ppatterns.append(p.pack())
        self.packed = 1
        self.unpacked = 0


    def unpack(self, check=1):
        """ unpack patterns.  threadsafe, checks self.unpacking, a second call will wait til it completes.
        so you can start unfolding a thread, and future calls will wait for it to complete if it hasn't yet."""

        if self.unpacking:
            while self.unpacking:
                time.sleep(0.1)
            # should be all done now
            return
                        
        if check and self.unpacked:
            return

        self.unpacking = 1
        
        self.patterns = []
        idx = 0
        for p in self.ppatterns:
            a = p.unpack()
            self.patterns.append(p.unpack())
            idx += 1
        self.unpacked = 1
        self.packed = 0

        self.unpacking = 0        


    def exportSomeSamples(self, path, samples):
        samples = utilx.tolist(samples)
        filenames = []
        for index in samples:
            try:
                sample = self.samples[index]
                if sample.filename:
                    fname = os.path.basename(self.path) + "-" + str(index) + "-" + utilx.nonulls(sample.filename)
                else:
                    fname = os.path.basename(self.path) + "-" + str(index)
                fname = filex.pathjoin(path, fname)
                sample.savefile(fname, modpath=self.path)
                filenames.append(fname)
            except:
                #traceback.print_exc()
                filenames.append(None)
        return filenames


    def exportSamples(self, path):
        i = 0
        for s in self.samples:
            s.savefile(filex.pathjoin(path, os.path.basename(self.path) + str(i)))
            i = i + 1


    def numTracks(self):
        return self.header.numTracks

    def numSamples(self):
        return len(self.samples)

    def patternList(self):
        return range(0, len(self.patterns))

    def numPatterns(self):
        return (max((len(self.ppatterns), len(self.patterns))))

    def numOrders(self):
        return self.header.numOrders


    def validSamples(self):
        """return indexes of valid (non-blank) samples"""
        valid = []
        for x in range(0, len(self.samples)):
            if self.samples[x].numSamples() > 0:
                valid.append(x)
                
        return valid

    def sampleNames(self):
        """return list of valid sample names, with index number prepended."""
        vs = self.validSamples()
        names = []
        for i in vs:
            name = str(i+1) + ". " + self.samples[i].name
            names.append(name)
        return names

    def instrumentNames(self):
        """return list of valid instrument names, with index number prepended."""
        names = []
        i = 0
        for ins in self.instruments:
            i += 1
            name = str(i) + ". " + ins.name
            names.append(name)
        return names

    def trackNames(self, unpack=0, numTracks=0):
        #TODO: can we figure the real value without unpacking?
        if numTracks:
            trks = numTracks
        elif self.unpacked or unpack:
            trks = self.numTracks()
        else:
            trks = 64
        names = ["Track "] * trks
        for i in xrange(0, trks):
            names[i] += str(i+1)
        return names

    def patternNames(self):
        patterns = self.numPatterns()
        names = ["Pattern "] * patterns
        for i in xrange(0, patterns):
            names[i] += str(i)
        return names

    def numPatterns(self):
        return (max((len(self.ppatterns), len(self.patterns))))

    def getTempo(self):
        return self.header.initialTempo

    def getSpeed(self):
        return self.header.initialSpeed

    def getGlobalVolume(self):
        return 0

    def getMixingVolume(self):
        return 0

    def getName(self):
        return self.header.songName

    def setSpeed(self, speed):
        self.header.initialSpeed = speed
        #TODO: range checking

    def setTempo(self, tempo):
        self.header.initialTempo = tempo
        #TODO: range checking

    def setGlobalVolume(self, volume):
        pass

    def setMixingVolume(self, volume):
        pass

    def setName(self, name):
        self.header.songName = name
        #TODO: it format string?


    def getBlankPatterns(self):
        #TODO
        return []
    
        # threadsafe
        try:
            while self.__gettingBlanks:
                time.sleep(0.1)
                #print "-- getblank waiting"
            self.__gettingBlanks = 1
            self.blanks = []
            self.unpack()
            i = 0
            for p in self.patterns:
                if p.areNotesEmpty():
                    self.blanks.append(i)
                    #print "blank", i

                i += 1
            
        finally:
            self.__gettingBlanks = 0

        return self.blanks      

    def unfold(self, pack=1):
        # do unfolding

        if self.unpacked:
            wasunpacked = 1
        else:
            wasunpacked = 0

        # pack patterns
        if self.unpacked and pack:
            self.pack()

        # if no order list exists currently, make order list from existing patterns.
        if self.isOrderListEmpty():
            self.header.orders = range(0, len(self.ppatterns))
            self.header.orders.append(255)
            return
                    
        newpatterns = []
        usedPatterns = []
        idx = 0
        for o in self.header.orders:
            #debug("processing order" + str(idx))
            if o < len(self.ppatterns) and o != 255:
                #debug("copying pattern" + str(o))
                p = copy.deepcopy(self.ppatterns[o])
                usedPatterns.append(o)
                newpatterns.append(p)
                idx = idx + 1
            else:
                #debug("invalid pattern" + str(o))
                pass
        numorders = len(self.header.orders) - self.header.orders.count(255)
        #debug("old orders: " + str(self.header.orders))
        self.header.orders = []
        for i in xrange(0, numorders):
            self.header.orders.append(i)
        #debug("new orders: " + str(self.header.orders))

        self.header.orders.append(255)

        # now add unused patterns onto end
        for pp in xrange(0, len(self.ppatterns)):
            if pp not in usedPatterns:
                newpatterns.append(self.ppatterns[pp])

        self.ppatterns = newpatterns
        #self.header.resize(len(self.samples), len(self.instruments), len(self.ppatterns))

        if wasunpacked:
            self.unpack()



    def areTrackNotesEmpty(self, track):
        """returns true if all note data in specified track in all patterns are empty"""
        if not self.unpacked:
            self.unpack()
        for p in self.patterns:
            if not p.areTrackNotesEmpty(track):
                return 0
        return 1


    def makeSolo(self, track, useVolumes=0):
        # note: xm doesn't support useVolumes (has no global track volumes)
        self.unpack()
        for p in self.patterns:
            p.makeSolo(track)


    def usedInstruments(self):
        """return list of all instruments used in all patterns"""
        instruments = []
        self.unpack()
        for p in self.patterns:
            instruments = instruments + p.usedInstruments()
        instruments = utilx.unique_seq(instruments)
        instruments.sort()
        return instruments


    def usedSamples(self):
        """return list of all samples used by all instruments used"""
        # if this module doesn't use instruments, usedSamples will be identical to usedInstruments
        samples = []
        instruments = self.usedInstruments()
        for i in instruments:
            try:
                samples = samples + self.instruments[i-1].usedSamples()
            except IndexError:
                pass
        samples = utilx.unique_seq(samples)
        samples.sort()
        return samples


    def optimizeSamples(self, usamples=None):
        removed = 0
        if not usamples:
            usamples = self.usedSamples()
        #print "usamples", usamples
        i = 0
        for i in self.validSamples():
            if i+1 not in usamples:
                #print "removing", i
                # make blank
                self.samples[i] = ITSample()
                removed += 1

        return removed        



    def makePlayableCopy(self, *args, **kwargs):
        return makePlayableCopy(*args, **kwargs)



def makePlayableCopy(fname, newname, copyAlways=1, mod=None, settingsFunc=None, checkValid=0):
    """makes a playable copy from fname and saves to newname.
    this makes a linear sequence if there is no sequence.  if no changes are necessary,
    newname will simply be a copy of fname.
    if copyAlways is false, a copy will only be created if changes are made. default is true.
    returns filename of new copy (or returns fname if copyAlways is false and no changes made), and numorders
    settingsFunc optionally gets different track volume and pan settings to use in the copy.
    """

    if not mod:    
        mod = XMModule(fname=fname, unpack=0)
    corrupt = mod.corrupt

    empty = mod.isOrderListEmpty()    
    if empty or settingsFunc or checkValid:
        #print "unfolding", fname, "to", newname
        pack=0
        if settingsFunc:
            #print ".. settingsFunc", settingsFunc
            tv, tp = settingsFunc()
            mod.setTrackVolumes(tv)
            mod.setTrackPannings(tp)
        if empty:
            mod.unpack()
            mod.unfold()
            pack=1
            
        mod.save(newname, pack=pack)
        result = newname
        numorders = mod.numOrders()
        del mod
    elif copyAlways:
        numorders = mod.numOrders()
        del mod
        #print "filex.copy", fname, "to", newname
        filex.copy(fname, newname)
        result = newname
    else:
        result = fname
        numorders = mod.numOrders()
        del mod

    if checkValid:
        return result, numorders, corrupt
    else:
        return result, numorders



        


        
def getNameFromFile(fname):
    """ read name of song from file """
    f = open(fname, "rb")
    f.seek(17)
    name = autobin.load(f, "<20s")
    f.close()
    name = utilx.nonulls(name)
    return name

        
def showinfo(fname):
    print "---", fname, "---"
    try:
        f = open(fname, "rb")
        x = XMHeader()
        x.load(f)
        f.close()
        autobin.autodump(x)
    except:
        print "error reading", fname
    print


import filex, sys

def test1():
    errors = 0
    fuofuofuo = open("xmtitles.txt", "w")
    for file in filex.dirtree("d:\\hornet\\", "*.xm"):
        try:
            fuofuofuo.write(getNameFromFile(file) + "\n")
            sys.stdout.write(".")
        except:
            errors += 1
    print "errors", errors
    fuofuofuo.close()


pass

def load(fname):
    return XMModule(fname)


if __name__ == "__main__":

    infile = "c:\\it\\inpuj\\poo.xm"
    outfile = "c:\\dev\\postmod\\testpoo.xm"
    a = XMModule(infile)
    a.unpack()
    a.pack()
    a.save(outfile)
    print "same?", filex.areSame(infile, outfile)
    print "same?", filex.areSame(infile, "c:\\it\\baes.it")
    
    #m = XMModule("c:\\it\\rw\\symphony.xm")
    #print m
    #m.header.dump()
    #rb = m.patterns[0]

    #m.exportSamples("c:\\it\\export")

    #m.save("c:\\dev\\postmod\\test.xm")

    #for event in rb:
    #    print event

    #for p in m.patterns:
    #    print p.data

    #for s in m.samples:
    #    print len(s.getData())



