import os, sys, array, struct, string, copy, audioop, traceback, operator, time, sets


import utilx, filex, autobin

from sample import *
from utilx import *
from notes import *  #TODO: remove references to notes

# if platform is windows, use win32api to get 8.3 filenames
try:
    import win32api
except:
    print "cannot find win32api module"
    win32api = None

# get itsmp module if available (c extension for loading compressed it samples)
try:
    import itsmpc
except:
    print "cannot find itsmpc module"
    itsmpc = None

DEBUG = 0
DEBUGSMP = 0

PATTERN_NULL_VALUE = 255

EVENT_NULL_NOTE = 0
EVENT_NULL_INSTRUMENT = 0
EVENT_NULL_VALUE = 255      # used for volpan and command fields

EVENT_NOTE_CUT = 254
EVENT_NOTE_OFF = 255

MAX_TRACKS = 64
MAX_PATTERN_CHANNELS = 64
MAX_PACKED_PATTERN_DATA = 65000

MAX_SAMPLES = 99
MAX_SAMPLES_UNLIMITED = 255
MAX_INSTRUMENTS = 99
MAX_INSTRUMENTS_UNLIMITED = 255

MAX_PATTERNNAME = 32
MAX_CHANNELNAME = 20

BLANK_PATTERN_NAME = "\x00" * MAX_PATTERNNAME
BLANK_CHANNEL_NAME = "\x00" * MAX_CHANNELNAME

PACK_PATTERNS = 1
UNPACK_PATTERNS = 2

DEFAULT_NUM_ROWS = 64
MAX_PATTERN_ROWS = 256

# file format constants
FORMAT_2XX = 0
FORMAT_214 = 1
FORMAT_215 = 2

# sample compression constants
COMPRESSION_NONE = 0
COMPRESSION_IT214 = 1
COMPRESSION_IT215 = 2

# sample loop modes
LOOP_NONE = 0
LOOP_NORMAL = 1
LOOP_PINGPONG = 2

# sample format constants
SF_DEFAULT = 0
SF_16BITS = 1
SF_STEREO = 2
SF_SIGNED = 4
SF_DELTA = 8
SF_BIGENDIAN = 16
SF_BYTEDELTA = 32
SF_TXWAVE = 64
SF_STEREOPROMPT = 128

SILENCEDATA = chr(0) * 32

defaultSampleRates = [44100, 22050, 11025]


"""
classes:

main IT file classes:

ITHeader
ITSample
ITInstrument
ITPackedPattern
ITModule

pattern classes for editing:

ITEventData
ITChannelData
ITRowData
ITPattern

other classes:

ITEditor

-----------------------------------------------

ITHeader, ITSample, ITInstrument, and ITPackedPattern closely mirror data structures
stored in an .IT file, with methods for loading, saving, and editing.

ITModule represents an entire .IT file.  It has an ITHeader and lists of ITSamples,
ITInstruments, and ITPackedPatterns.  It also has some higher level editing methods.

IT pattern data is stored in a compressed format.  To handle general editing, ITModule
unpacks the data into ITPatterns, which also use the ITEventData and ITChannelData
data structures.

The general method for editing pattern data is to load the module, unpack the patterns,
modify the unpacked pattern data, then repack the patterns before saving.
By default, ITModule handles this unpacking and packing transparently, but that behavior
can be changed with the "pack" and "unpack" parameters of its "save" and "load" methods.

ITEditor is a higher level editor for IT modules.  It stores a cursor position based
on current pattern, track and row, and has methods for modifying data at the cursor.


"""


"""
notes on offset updates:
an ITHeader contains three lists of offsets that must be set to the correct file position of sample, instrument, and pattern records.
an ITSample also contains a sampleOffset that must be set to the correct file position of the sample's sample data.
the order that these structures are stored in an IT file are as follows:
1. ITHeader
2. all ITInstrument records
3. all ITSample headers
4. all ITPackedPattern records
5. all ITSample sampledata

the saving code in this module is generally set up to work as follows, when saving an IT module:
1. make sure the ITHeader is sized correctly (correct number of offsets in its lists), and save it to the file
2. save the ITInstrument records, updating the ITHeader instrumentOffsets as each is saved.
    the ITHeader in memory is modified, but not rewritten to the file at each write.
3. save the ITSample headers, updating the ITHeader sampleOffsets as each is saved (same method as 2)
4. save the ITPackedPattern records, updating the ITHeader patternOffsets as each is saved (same method as 2)
5. each ITSample's sampledata is written. as each set of data is written, the corresponding ITSample header's sampleOffset
    is updated, and the ITSample header is rewritten to the file in the same position it was written previously.
6. The now updated ITHeader is rewritten at the beginning of the file.

"""

"""
Known Issues:
    Creating a new module and loading samples into it, but saving it without creating
any patterns, results in a corrupt module file.
"""

"""
embedded midi configuration:

possibly:
    search backwards from either song message start (if exists),
    or first sample or instrument.
    some old files have song message at end, but it appears newer
    files have song message before samples or instruments, and
    embedded midi before song message.
    issue: one file, chris31b, had what looked like a dummy copy
    of the first instrument record BEFORE the embedded midi!
    but perhaps that can be ignored.
"""

"""
extra fragment notes:
sample headers sometimes have the 8 byte cache information appended.  i think this is safe to ignore.
instrument headers seem to usually be 554 bytes, similar to old instrument format, but not always.
midi config might be 4984 bytes?
"""

"""
stereo samples:
i think stereo samples (as saved by MPT) are actually saved with all the left channel data first,
then all the right channel data.
""" 

# orderlist notes: 255 is always the end of a pattern.  a blank order list is [255,255]
# orderlists can have blank entries which are also identified by 255, for example,
# [1,5,255,3,4,255,255,8,10,255]




ITCMD_A = 1
ITCMD_B = 2
ITCMD_C = 3

if (DEBUG):
    def debug(s):
        print s
        return 1
else:
    def debug(s):
        return 1



def itstr(s, length):
    """it format strings are null-padded.
    this function returns a string padded to the specified length with nulls.
    it will also truncate the string if it is greater than the specified length."""

    result = s    
    if len(result) > length:
        result = s[0:length]

    while len(result) < length:
        result = result + "\0"

    return result        


def itversion(version):
    pass


def toggleSigned8bit2(data):
    # obsolete?
    newdata = ""
    for x in data:
        newdatum = ord(x) ^ 0x80
        newdata = newdata + chr(newdatum)
    return newdata

def toggleSigned8bit(data):
    #print "toggling"
    newdata = array.array('B')
    newdata.fromstring(data)
    lendata = len(data)
    for x in xrange(0, lendata):
        newdata[x] = newdata[x] ^ 0x80
    return newdata.tostring()



def nearestSampleRate(sourceRate):
    ldiff = sys.maxint
    rate = 44100
    for x in defaultSampleRates:
        diff = abs(x - sourceRate)
        if diff < ldiff:
            ldiff = diff
            rate = x
    return rate            
        

def autoload(fp, obj):
    """autoloads binary data from a file into class instance members.
    the class instance must have a member named "vars" which is a list of member variable names to be loaded.
    it must also have a member named "formats" which is a dictionary specifiying struct-module-style format
    strings for each variable name."""

    for x in obj.vars:
        temp = fp.read(struct.calcsize(obj.formats[x]))
        temp = struct.unpack(obj.formats[x], temp)
        # struct.unpack always returns a tuple even if there is only one value.
        # convert to single value if there is only one.
        if len(temp) == 1:
            temp = temp[0]

        obj.__dict__[x] = temp
        if type(obj.__dict__[x]) == tuple:
            obj.__dict__[x] = list(obj.__dict__[x])
            
        


def autosave(fp, obj):
    """autosaves binary data from a file into class instance members.
    the class instance must have a member named "vars" which is a list of member variable names to be saved.
    it must also have a member named "formats" which is a dictionary specifiying struct-module-style format
    strings for each variable name."""
    for x in obj.vars:

        # struct.pack can't accept a tuple for an array of values, so we must call it with
        # apply.  we need to build a tuple of args to pass it. 
        argtup = [obj.formats[x]]
        if type(obj.__dict__[x]) in (tuple, list):
            argtup = argtup + list(obj.__dict__[x])
        else:
            argtup.append(obj.__dict__[x])
        argtup = tuple(argtup)
        
        #print "argtup", argtup
        temp = struct.pack(*argtup)
        fp.write(temp)
    

def autodump(obj):
    for x in obj.vars:
        print x,":",nonulls(obj.__dict__[x])



class MidiConfig:
    vars = "midiGlobal,midiSFX,midiZXX".split(",")
    formats = {
        'midiGlobal': "<288s",  # 9*32
        'midiSFX': "<512s",     # 16*32
        'midiZXX': "<4096s",    # 128*32
    }

    def __init__(self):
        self.midiGlobal = ""
        self.midiSFX = ""
        self.midiZXX = ""

    def load(self, fp):
        autobin.autoload(fp, self)

    def save(self, fp):
        autobin.autosave(fp, self)
    


class MPTPlugin:
    # based on _SNDMIXPLUGININFO in modplug tracker, 128 bytes

    vars = "id1,id2,inputRouting,outputRouting,reserved,name,libraryName".split(",")
    formats = {
        'id1': "<i",
        'id2': "<i",
        'inputRouting': "<i",
        'outputRouting': "<i",
        'reserved': "<4i",
        'name': "<32s",
        'libraryName': "<64s",
    }

    def __init__(self):
        self.id1 = 0    # DWORD
        self.id2 = 0    # DWORD
        self.inputRouting = 0 # DWORD - MIXPLUG_INPUTF_XXXX
        self.outputRouting = 0  # DWORD - 0=mix, 0x80+=fx
        self.reserved = []       # DWORD - reserved for routing info, not used, 4 ints
        self.name = ""          # char(32)
        self.libraryName = ""   # char(64) - original dll name

        self.data = ""  # plugin specific data
        self.index = 0

    #define MIXPLUG_INPUTF_MASTEREFFECT		0x01	// Apply to master mix
    #define MIXPLUG_INPUTF_BYPASS			0x02	// Bypass effect
    #define MIXPLUG_INPUTF_WETMIX			0x04	// Wet Mix (dry added)

    def getDLLName(self):
        return utilx.stripnulls(self.libraryName)

    def load(self, fp, index):
        # position should be right after FX00 header string
        # index is the plugin number, FX02 should be passed index 2

        self.index = index
        
        datalen = autobin.load(fp, "<i")
        
        autobin.autoload(fp, self)
        print ".. loaded MPTPlugin", self.name, datalen
        autobin.autodump(self)

        self.data = fp.read(datalen-128)


    def save(self, fp):
        fp.write(struct.pack("<4s", "FX" + str(self.index).zfill(2)))
        datalen = len(self.data) + 128
        fp.write(struct.pack("<i", datalen))
        
        autobin.autosave(fp, self)

        fp.write(self.data)

    def show(self):
        autobin.autodump(self)
        print "index", data.index
        print "data", self.data



class ITHeader(object):
    def __init__(self):
        self.headerID = "IMPM"      # char[4]
        self.songName = ""          # char[26]
        self.extra = 4100           # short
        self.numOrders = 0          # short
        self.numIns = 0             # short
        self.numSamples = 0         # short
        self.numPatterns = 0        # short
        self.trackerVersion = 533   # short - versions are stored from hex representations, example: 214h = 532
        self.formatVersion = 532    # short - defaults are 215 tracker, 214 format
        self.flags = 9              # short
        self.special = 6            # short. if bit 0 is set, song message attached

        self.globalVolume = 128     # unsigned char
        self.mixVolume = 48         # unsigned char
        self.initialSpeed = 6       # unsigned char
        self.initialTempo = 125     # unsigned char
        self.seperation = 128       # unsigned char

        self.nullByte = 0           # unsigned char

        self.messageLength = 0      # short
        self.messageOffset = 0      # int

        self.reserved = 0           # int

        self.channelPan = []        # unsigned char[64]
        self.channelVolume = []     # unsigned char[64]
        for x in xrange(0,64):
            self.channelPan.append(32)
            self.channelVolume.append(64)

        self.orders = [255, 255]    # unsigned char* - length is numOrders.
                                    # a "blank" order list should have two entries of 0xFF

        self.instrumentOffsets = [] # int* - length is numIns * sizeof(int)
        self.sampleOffsets = []     # int* - length is numSamples * sizeof(int)
        self.patternOffsets = []    # int* - length is numPatterns * sizeof(int)

        #self.undocumented = "\x01\x00\xCA\x2A\xA5\x11\xCA\x0C\x00\x00" # 10 undocumented bytes
        #self.undocumented2 = "\xCA\x2A\xE4\x04\xEC\x00\x00\x00" # another 8 undocumented bytes

        # some it files have 10 undocumented bytes, some have 18.  and some have other lengths!

        self.message = ""   # song message

        self.numHistoryEntries = 0
        self.historyEntries = []

        self.plugins = []
        self.channelFX = []

        self.midiConfig = None

        self.patternNames = {}
        self.trackNames = {}

        #self.extraData = "\x01\x00\xCA\x2A\xA5\x11\xCA\x0C\x00\x00"
        self.extraData = ""
                                    # the extra stuff after the documented header and before the next chunk starts.
                                    # may include embedded midi config.  not auto-loaded or saved.

        # the following member values are not stored in the file
        self.changedSinceSave = 0 # changed since last save?
        self.endFilePos = 0  # filepos of the end of the file (filesize)
        self.beginHeaderPos = 0
        self.endHeaderPos = 0

        self.formats = {}
        self.formats["headerID"] = "<4s"
        self.formats["songName"] = "<26s"
        self.formats["extra"] = "<h"
        self.formats["numOrders"] = "<h"
        self.formats["numIns"] = "<h"        
        self.formats["numSamples"] = "<h"
        self.formats["numPatterns"] = "<h"
        self.formats["trackerVersion"] = "<h"
        self.formats["formatVersion"] = "<h"
        self.formats["flags"] = "<h"
        self.formats["special"] = "<h"
        self.formats["globalVolume"] = "<B"
        self.formats["mixVolume"] = "<B"
        self.formats["initialSpeed"] = "<B"
        self.formats["initialTempo"] = "<B"
        self.formats["seperation"] = "<B"
        self.formats["nullByte"] = "<B"
        self.formats["messageLength"] = "<h"
        self.formats["messageOffset"] = "<i"
        self.formats["reserved"] = "<i"
        self.formats["channelPan"] = "<64B"
        self.formats["channelVolume"] = "<64B"
        self.formats["orders"] = "<B"
        self.formats["instrumentOffsets"] = "<i"
        self.formats["sampleOffsets"] = "<i"
        self.formats["patternOffsets"] = "<i"
        #self.formats["undocumented"] = "<10s"
        #self.formats["undocumented2"] = "<8s"
                     
        

        # members that are stored in the file header
        self.vars=["headerID", "songName", "extra", "numOrders", "numIns", "numSamples", "numPatterns", \
                    "trackerVersion", "formatVersion", "flags", "special", "globalVolume", \
                    "mixVolume", "initialSpeed", "initialTempo", "seperation", "nullByte", \
                    "messageLength", "messageOffset", "reserved", "channelPan", "channelVolume", \
                    "orders", "instrumentOffsets", "sampleOffsets", "patternOffsets"]

    def load(self, fp, pos=-1):
        """loads header from an open file."""

        if pos <> -1:
            fp.seek(pos)

        self.beginHeaderPos = fp.tell()            

        for x in self.vars:
            temp = fp.read(struct.calcsize(self.formats[x]))
            temp = struct.unpack(self.formats[x], temp)
            # struct.unpack always returns a tuple even if there is only one value.
            # convert to single value if there is only one.
            if len(temp) == 1:
                temp = temp[0]
            self.__dict__[x] = temp
            if type(self.__dict__[x]) == tuple:
                self.__dict__[x] = list(self.__dict__[x])

            # if this is one of the values that determines a future value, update the format
            # of the future value.
            if x == "numOrders":
                self.formats["orders"] = "<%dB" % (self.numOrders)
            elif x == "numIns":
                self.formats["instrumentOffsets"] = "<%di" % (self.numIns)
            elif x == "numSamples":
                self.formats["sampleOffsets"] = "<%di" % (self.numSamples)
            elif x == "numPatterns":
                self.formats["patternOffsets"] = "<%di" % (self.numPatterns)

            # make sure these are lists - if they are only 1 length, they won't be.
            # TODO: why are these not lists in the first place?
            if type(self.instrumentOffsets) != list:
                self.instrumentOffsets = [self.instrumentOffsets]
            if type(self.sampleOffsets) != list:
                self.sampleOffsets = [self.sampleOffsets]
            if type(self.patternOffsets) != list:
                self.patternOffsets = [self.patternOffsets]

            if type(self.orders) != list:
                self.orders = [self.orders]

        # everything from here on might not be there.
        # try to read history entries

        try:
            spos = fp.tell()
            if spos == self.messageOffset:
                # no history info, and no extra chunks
                self.numHistoryEntries = 0
            else:
                
                #print "examine history at ", spos
                numHistoryEntries = autobin.load(fp, "<h")
                if numHistoryEntries == 19785:
                    # this is some other chunk, 19785 = "IM"
                    #no history information was there, not even the numHistoryEntries
                    self.numHistoryEntries = 0
                else:
                    # otherwise             
                    historyEntries = []
                    if numHistoryEntries:
                        for i in range(numHistoryEntries):
                            entry = autobin.load(fp, "<8s")
                            historyEntries.append(entry)
                    self.numHistoryEntries = numHistoryEntries
                    self.historyEntries = historyEntries
        except:
            # history entries probably aren't appended, go back
            traceback.print_exc()
            fp.seek(spos)

        #print "history", self.numHistoryEntries, self.historyEntries

        if self.flags & 128:
            # read midi config
            spos = fp.tell()
            try:
                self.midiConfig = MidiConfig()
                self.midiConfig.load(fp)
                print ".. read midi config"
            except:
                fp.seek(spos)
                

        # look for MPT chunks
        while 1:
            spos = fp.tell()
            try:
                code = autobin.load(fp, "<4s")
                if code == "PNAM":
                    datalen = autobin.load(fp, "<i")
                    for i in range(datalen / MAX_PATTERNNAME):
                        self.patternNames[i] = fp.read(MAX_PATTERNNAME)
                    #print names
                elif code == "CNAM":
                    datalen = autobin.load(fp, "<i")
                    for i in range(datalen / MAX_CHANNELNAME):
                        self.trackNames[i+1] = fp.read(MAX_CHANNELNAME)
                    #print names
                elif code[:2] == "FX":
                    # read FX
                    plugin = MPTPlugin()
                    plugin.load(fp, int(code[2:]))
                    self.plugins.append(plugin)
                    
                elif code == "CHFX":
                    datalen = autobin.load(fp, "<i")
                    channelFX = []
                    for i in range(datalen / 4):
                        channelFX.append(autobin.load(fp, "<i"))
                    self.channelFX = channelFX
                    print channelFX
                        
                elif code == "EQFX":
                    # read eq settings
                    pass
                else:
                    break
            except:
                # no more chunks
                traceback.print_exc()
                fp.seek(spos)
                break

        self.endHeaderPos = fp.tell()

        if self.messageOffset and self.messageLength:
            fp.seek(self.messageOffset)
            self.message = fp.read(self.messageLength)
            fp.seek(self.endHeaderPos)
            

        #print "version", self.trackerVersion, self.formatVersion
        #x = raw_input()

    def loadExtra(self, fp, start, end):
        # loadExtra is called after everything has been loaded, by ITModule, which can determine the start and end pos of the extra data.
        # the extra data is saved normally in the save method.
        
        lendata = end-start
        if lendata > 0:
            fp.seek(start)
            format = "<%ds" % lendata
            self.extraData = fp.read(struct.calcsize(format))
            self.extraData = struct.unpack(format, self.extraData)[0]
        else:
            self.extraData = ""

        self.endHeaderPos = fp.tell()                    

    def isValid(self):
        return (self.headerID == "IMPM")
             
                
    def save(self, fp, pos=-1):
        """saves header to an open file.
        before saving, you should make sure the header has been sized correctly with resize(), if necessary."""

        #self.undocumented2 = "\x00" * 8

        if pos <> -1:
            fp.seek(pos)

        self.beginHeaderPos = fp.tell()

        self.numOrders = len(self.orders)
        self.update_formats()
        
        autosave(fp, self)

        # save history and MPT chunks
        #print "saving history", self.numHistoryEntries, self.historyEntries
        fp.write(struct.pack("<h", self.numHistoryEntries))
        for h in self.historyEntries:
            fp.write(struct.pack("<8s", h))

        # save midi config
        if (self.flags & 128) and self.midiConfig:
            print "saving midiconfig"
            self.midiConfig.save(fp)

        if self.patternNames:
            fp.write("PNAM")
            keys = self.patternNames.keys()
            fp.write(struct.pack("<i", (max(keys)+1) * MAX_PATTERNNAME))
            keys.sort()
            for i in keys:
                fp.write(self.patternNames.get(i, BLANK_PATTERN_NAME)[:MAX_PATTERNNAME])

        if self.trackNames:
            fp.write("CNAM")
            keys = self.trackNames.keys()
            fp.write(struct.pack("<i", max(keys) * MAX_CHANNELNAME))
            keys.sort()
            for i in keys:
                fp.write(self.trackNames.get(i, BLANK_CHANNEL_NAME)[:MAX_CHANNELNAME])


        # save plugins
        if self.plugins:
            for p in self.plugins:
                print "saving plugin"
                p.save(fp)

        # save channel fx
        if self.channelFX:
            fp.write("CHFX")
            fp.write(struct.pack("<i", len(self.channelFX)*4))
            for fx in self.channelFX:
                fp.write(struct.pack("<i", fx))
            
        if self.extraData:
            pass
            #print ".. has ", len(self.extraData), "extra"
            #print self.extraData
            #format = "<%ds" % len(self.extraData)
            #extra = struct.pack(format, self.extraData)
            #fp.write(extra)

        self.endHeaderPos = fp.tell()        

        if self.message:
            pos = self.endHeaderPos
            format = "<" + str(len(self.message)) + "s"
            temp = struct.pack(format, self.message)
            fp.write(temp)
            self.messageOffset = pos
            self.messageLength = len(self.message)
            fp.seek(pos)

        self.changedSinceSave = 0

    def prepareForSave(self):
        # make sure order list ends with 255
        if len(self.orders) > 0:
            if self.orders[-1] != 255:
                self.orders.append(255)

    def update_formats(self):
        """make sure dynamic formats are set correctly."""
        self.formats["orders"] = "<%dB" % (self.numOrders)
        self.formats["instrumentOffsets"] = "<%di" % (self.numIns)
        self.formats["sampleOffsets"] = "<%di" % (self.numSamples)
        self.formats["patternOffsets"] = "<%di" % (self.numPatterns)

    def resize(self, numsamples, numins, numpatterns):
        """resize offset lists and formats. this should always be done before saving an it module,
        so that the header will be the correct size when it is first written."""        

        self.numOrders = len(self.orders)
        self.numIns = numins
        self.numSamples = numsamples
        self.numPatterns = numpatterns
        self.update_formats()

        resize_list(self.instrumentOffsets, numins, 0)
        resize_list(self.sampleOffsets, numsamples, 0)
        resize_list(self.patternOffsets, numpatterns, 0)
                

    def dump(self):
        autodump(self)

    def set_pattern_offset(self, p, offset):
        while (len(self.patternOffsets)-1 < p):
            self.patternOffsets.append(255)
        self.patternOffsets[p] = offset

    def set_sample_offset(self, p, offset):
        while (len(self.sampleOffsets)-1 < p):
            self.sampleOffsets.append(255)
        self.sampleOffsets[p] = offset

    def set_instrument_offset(self, p, offset):
        while (len(self.instrumentOffsets)-1 < p):
            self.instrumentOffsets.append(255)
        self.instrumentOffsets[p] = offset


"""
ITSample flags:
      Flg:      Bit 0. On = sample associated with header.
                Bit 1. On = 16 bit, Off = 8 bit.
                Bit 2. On = stereo, Off = mono. Stereo samples not supported yet
                Bit 3. On = compressed samples.
                Bit 4. On = Use loop
                Bit 5. On = Use sustain loop
                Bit 6. On = Ping Pong loop, Off = Forwards loop
                Bit 7. On = Ping Pong Sustain loop, Off = Forwards Sustain loop

   Convert - bits other than bit 0 are used internally for the loading
             of alternative formats.
        Bit 0:
         Off: Samples are unsigned   } IT 2.01 and below use unsigned samples
          On: Samples are signed     } IT 2.02 and above use signed samples
        Bit 1:
         Off: Intel lo-hi byte order for 16-bit samples    } Safe to ignore
         On: Motorola hi-lo byte order for 16-bit samples  } these values...
        Bit 2:                                             }
         Off: Samples are stored as PCM values             }
          On: Samples are stored as Delta values           }
        Bit 3:                                             }
          On: Samples are stored as byte delta values      }
              (for PTM loader)                             }
        Bit 4:                                             }
          On: Samples are stored as TX-Wave 12-bit values  }
        Bit 5:                                             }
          On: Left/Right/All Stereo prompt                 }
        Bit 6: Reserved
        Bit 7: Reserved

"""


class ITSample(object):

    """
    // set looping flags
    if(s.flag & 16)  q->flags |= SL_LOOP;
    if(s.flag & 32)  q->flags |= SL_SUSTAIN_LOOP;
    if(s.flag & 64)  q->flags |= SL_BIDI;
    if(s.flag & 128) q->flags |= SL_SUSTAIN_BIDI;

    // set disk format
    if(s.flag & 8)  q->compress = DECOMPRESS_IT214;
    if(s.flag & 2)  q->format  |= SF_16BITS;
    if(h->mh.cwt >= 0x200)
    {   if(s.convert & 1) q->format |= SF_SIGNED;
        if(s.convert & 4) q->format |= SF_DELTA;   
    }
    """

    def __init__(self, path="", data=None, params=None, forceMono=1):        
        self.headerID = "IMPS"      # char[4]
        self.filename = ""          # char[12]
        self.nullByte = 0           # unsigned char
        self.globalVolume = 64      # unsigned char
        self.flags = 0              # unsigned char. 
        self.defaultVolume= 64      # unsigned char
        self.name = ""              # char[26]
        self.convert = 1            # unsigned char, should be 1 for normal samples with data
        self.defaultPan = 32        # unsigned char, defaults 0.  32 is middle?
        self.length = 0             # int.  length in number of samples, NOT in number of bytes
        self.loopBegin = 0          # int
        self.loopEnd = 0            # int
        self.c5speed = 0            # int. number of bytes a second for C-5
        self.sustainLoopBegin = 0   # int
        self.sustainLoopEnd = 0     # int
        self.sampleOffset = 0       # int, long offset of sample data in file
        self.vibratoSpeed = 0       # unsigned char
        self.vibratoDepth = 0       # unsigned char
        self.vibratoRate = 0        # unsigned char
        self.vibratoType = 0        # unsigned char

        self.data = ""               # unsigned char*, the sample data

        # the following member values aren't stored in the file
        
        self.lengthInBytes = 0
        self.numBytesData = None  # num bytes compressed or uncompressed data, none if unknown
                                  # (for compressed samples, sample data must be inspected to know numbytes)
        self.sampleSize = 2
        self.compression = COMPRESSION_NONE  # COMPRESSION_NONE, COMPRESSION_IT214
        self.loopMode = LOOP_NONE  # LOOP_NONE, LOOP_NORMAL, LOOP_PINGPONG
        self.susLoopMode = LOOP_NONE # LOOP_NONE, LOOP_NORMAL, LOOP_PINGPONG
        self.sampleFormat = SF_DEFAULT

        self.signed = 1   # it 2.02 and above default to signed, below uses unsigned. this only applies to 8-bit samples.
                            # NOTE: i think i got this backwards, 16-bit is signed and 8-bit is unsigned.
                            

        self.delta = 0    # true if IT215 compression
        self.bigEndian = 0    # ittech.txt says this is safe to ignore, default is little endian
        self.bytedelta = 0
        self.txwave = 0
        self.stereoPrompt = 0

        self.channels = 1       # 1 = mono, 2 = stereo. MPT supports stereo.

        self.beginHeaderPos = 0
        self.endHeaderPos = 0
        self.beginDataPos = 0
        self.endDataPos = 0

        self.formats = {}
        self.formats["headerID"] = "<4s"
        self.formats["filename"] = "<12s"
        self.formats["nullByte"] = "<B"
        self.formats["globalVolume"] = "<B"
        self.formats["flags"] = "<B"
        self.formats["defaultVolume"] = "<B"
        self.formats["name"] = "<26s"
        self.formats["convert"] = "<B"
        self.formats["defaultPan"] = "<B"
        self.formats["length"] = "<i"
        self.formats["loopBegin"] = "<i"
        self.formats["loopEnd"] = "<i"
        self.formats["c5speed"] = "<i"
        self.formats["sustainLoopBegin"] = "<i"
        self.formats["sustainLoopEnd"] = "<i"
        self.formats["sampleOffset"] = "<i"
        self.formats["vibratoSpeed"] = "<B"
        self.formats["vibratoDepth"] = "<B"
        self.formats["vibratoRate"] = "<B"
        self.formats["vibratoType"] = "<B"
        self.formats["data"] = "<s"

        # members that are stored in the file sampleheader
        self.vars = ["headerID", "filename", "nullByte", "globalVolume", "flags", "defaultVolume", \
                     "name", "convert", "defaultPan", "length", "loopBegin", "loopEnd", "c5speed",
                     "sustainLoopBegin", "sustainLoopEnd", "sampleOffset", "vibratoSpeed", \
                     "vibratoDepth", "vibratoRate", "vibratoType"]

        if (path != ""):
            #print "loading itsample", path
            self.loadfile(path)
        elif (data != None):
            # careful, setting data defaults to 16bit 44100 mono
            self.setData(data, params=params, forceMono=forceMono)
            #print "it set", len(data), "bytes of data"

    def setData(self, data, samplerate=44100, samplewidth=2, channels=1, params=None, forceMono=1):
        """careful, setting data currently defaults to 16bit 44100 mono"""

        self.signed = 1

        #print "params", params
        if params:
            self.samplerate = params[2]
            self.sampleSize = params[1]
            channels = params[0]
        else:
            self.samplerate = samplerate
            self.sampleSize = samplewidth

        # if stereo, convert to mono
        if channels == 2 and forceMono:
            #print "!! converting to mono"
            data = audioop.tomono(data, self.sampleSize, .5, .5)
            channels = 1
        """
        if channels == 2:
            # convert to weird format (left then right)
            # [s[i:i+2] for i in range(len(s))[::2]]
            if self.sampleSize == 1:
                fmt = numpy.UInt8
            else:
                fmt = numpy.Int16
            #print "!! converting to weird stereo", fmt
            left = numpy.fromstring(data, fmt)[0::2].tostring()
            right = numpy.fromstring(data, fmt)[1::2].tostring()
            data = left + right
        """
        if self.sampleSize == 1 and self.signed:
            #data = toggleSigned8bit(data)
            self.signed = 0
        
        self.data = data

        self.setflags(self.sampleSize, channels) 
        self.c5speed = self.samplerate
        self.length = (len(self.data) / self.sampleSize) / channels
        
        self.update()

    def setName(self, name):
        #TODO: itstr?
        self.name = name[:26]

    def setFileName(self, fname):
        self.filename = fname[:12]

    def setDefaultVolume(self, volume):
        self.defaultVolume = max(min(volume, 64), 0)

    def setGlobalVolume(self, volume):
        self.globalVolume = max(min(volume, 64), 0)

    def getGlobalVolume(self):
        return self.globalVolume


    def setDefaultPan(self, pan=32, use=1, scale=None):
        # pan should be 0..64.  128 is added to the pan value if it should be used, otherwise pan setting
        # is disabled.
        # scale can be passed as a tuple (scalemin, scalemax) - NOT IMPLEMENTED YET.

        self.defaultPan = max(min(pan, 64), 0) + (128 * use)
        
        

    def lenData(self):
        return len(self.data)

    def loadfile(self, path, forceMono=1):
        """load from sound file"""
        self.__init__()
        x = Sample()
        x.load(path)
        #if stereo, convert to mono
        if x.channels == 2 and forceMono:
            self.data = audioop.tomono(x.data, x.bits/8, .5, .5)
        else:
            self.data = x.data

        # if 8 bit, toggle
        #TODO: not sure if toggle is necessary, rather just turn self.signed off?
        if x.bits == 8 and self.signed:
            self.data = toggleSigned8bit(self.data)

        self.filename = os.path.basename(path)
        if len(self.filename) > 12:
            try:
                # try getting the 8.3 dos filename
                self.filename = win32api.FindFiles(path)[0][-1]
            except:
                self.filename = self.filename[0:12]

        self.filename = itstr(self.filename, 12)
        self.name = itstr(self.filename, 26)

        self.sampleSize = x.bits / 8
        self.setflags(self.sampleSize, x.channels)
        self.c5speed = x.samplerate
        self.length = x.numsamples
        self.update()
        #print "samplerate:",self.c5speed,"samplesize",self.sampleSize,"flags",self.flags,"length",self.length,"lib",self.lengthInBytes

    def uncompress(self, itpath=None):
        if not itpath:
            print "-- Must supply itfile path for uncompression"
            return 0
        if self.compression == COMPRESSION_IT214 or self.compression == COMPRESSION_IT215:
            if not itsmpc:
                print "-- Can't uncompress",self.name
                return 0

            print ".. decomp", itpath, self.sampleOffset, self.lengthInBytes, self.samplesize(), self.delta            
            self.data = itsmpc.decompress(itpath, self.sampleOffset, self.lengthInBytes, self.samplesize(), self.delta)
            self.compression = COMPRESSION_NONE
            self.setflags(self.sampleSize, 1) # mono
            self.length = len(self.data) / self.sampleSize

        return 1
            
            #print "new datalen", len(self.data)
        

    def savefile(self, path, type="wav", modpath=None):
        """save to sound file, currently only supports mono.  path to itfile must be supplied if uncompression is needed."""
        x = Sample()
        x.setType(type)
        #x.setRate(self.c5speed)
        x.setRate(nearestSampleRate(self.c5speed))
        x.setBits((self.samplesize() / self.channels) * 8)
        x.setChannels(self.channels)

        if self.compression == COMPRESSION_IT214 or self.compression == COMPRESSION_IT215:
            if not itsmpc:
                return 0
            
            if modpath:
                #print "uncompressing 214/215", "size:", self.samplesize(), "signed:", self.signed, "delta:", self.delta
                comp215 = self.delta
                x.data = itsmpc.decompress(modpath, self.sampleOffset, self.lengthInBytes, self.samplesize(), comp215)
                if (self.samplesize() / self.channels) == 1:
                    #print "converting signed/unsigned", self.lengthInBytes
                    #x.data = itsmpc.toggleSigned(x.data, self.lengthInBytes, 1)
                    x.data = toggleSigned8bit(x.data)
                    self.signed = 1
            else:
                print "-- Must supply itfile path for uncompression"
                x.data = self.data
        else:
            if (self.samplesize() / self.channels) == 1 and self.signed:
                #print "converting to unsigned"
                x.data = toggleSigned8bit(self.data)
            else:
                x.data = self.data

        if self.channels == 2:
            # convert from weird format (left then right)
            datalen = len(x.data) / 2
            bps = self.bytesPerSample()
            stuff = array.array('c', x.data)
            if bps == 2:
                xi = 0
                for i in xrange(0, datalen, 2):
                    stuff[xi] = x.data[i]
                    stuff[xi+1] = x.data[i+1]
                    stuff[xi+2] = x.data[datalen+i]
                    stuff[xi+3] = x.data[datalen+i+1]
                    xi += 4
            else:
                xi = 0
                for i in xrange(0, datalen):
                    stuff[xi] = x.data[i]
                    stuff[xi+1] = x.data[datalen+i]
                    xi += 2
                
            x.data = stuff.tostring()
                        
        x.save(path)
        
    def setflags(self, samplewidth, channels=None):
        if not channels:
            channels = self.channels

        flags = 0
        if len(self.data) > 0:
            flags = flags | 1   # sample has data associated with it.
            if (samplewidth == 2):
                flags = flags | 2
            if (channels == 2):
                flags = flags | 4

        if self.compression != COMPRESSION_NONE:
            flags = flags | 8

        if self.loopMode == LOOP_NORMAL:
            flags = flags | 16
        if self.susLoopMode == LOOP_NORMAL:
            flags = flags | 32
        if self.loopMode == LOOP_PINGPONG:
            flags = flags | 64
        if self.susLoopMode == LOOP_PINGPONG:
            flags = flags | 128

        self.flags = flags

        self.convert = 0
        if self.signed:
            self.convert = self.convert | 1     
        if self.bigEndian:
            self.convert = self.convert | 2
        if self.delta:
            self.convert = self.convert | 4
        if self.bytedelta:
            self.convert = self.convert | 8
        if self.txwave:
            self.convert = self.convert | 16
        if self.stereoPrompt:
            self.convert = self.convert | 32

    def parseflags(self):
        #TODO: update setflags; verify loops and compression

        #if self.flags & 1:
        #    sample is associated with header

        if self.flags & 2:
            self.sampleFormat = self.sampleFormat & SF_16BITS

        if self.flags & 4:
            self.channels = 2
        else:
            self.channels = 1
        
        self.loopMode = LOOP_NONE  # LOOP_NONE, LOOP_NORMAL, LOOP_PINGPONG
        self.susLoopMode = LOOP_NONE # LOOP_NONE, LOOP_NORMAL, LOOP_PINGPONG
        
        if self.flags & 16:
            self.loopMode = LOOP_NORMAL
        if self.flags & 32:
            self.susLoopMode = LOOP_NORMAL
        if self.flags & 64:
            self.loopMode = LOOP_PINGPONG
        if self.flags & 128:
            self.susLoopMode = LOOP_PINGPONG

        self.signed = 0
        self.delta = 0
        self.bigEndian = 0
        self.bytedelta = 0
        self.txwave = 0
        self.stereoPrompt = 0
        
        if self.convert & 1:
            self.sampleFormat = self.sampleFormat | SF_SIGNED
            self.signed = 1
        if self.convert & 2:
            self.sampleFormat = self.sampleFormat | SF_BIGENDIAN
            self.bigEndian = 1
        if self.convert & 4:
            self.sampleFormat = self.sampleFormat | SF_DELTA
            self.delta = 1
        if self.convert & 8:
            self.sampleFormat = self.sampleFormat | SF_BYTEDELTA
            self.bytedelta = 1
        if self.convert & 16:
            self.sampleFormat = self.sampleFormat | SF_TXWAVE
            self.txwave = 1
        if self.convert & 32:
            self.stereoPrompt = 1
            self.sampleFormat = self.sampleFormat | SF_STEREOPROMPT

        if self.flags & 8:
            self.compression = COMPRESSION_IT214
            if self.delta:
                self.compression = COMPRESSION_IT215
        else:
            self.compression = COMPRESSION_NONE
            

    def setLoopPoints(self, begin=0, end=None):
        self.loopBegin = begin
        if not end:
            self.loopEnd = self.length
        else:
            self.loopEnd = end

    def setLoopMode(self, mode=None):
        # reset loop settings
        if self.flags & 16:
            self.flags = self.flags ^ 16
        if self.flags & 64:
            self.flags = self.flags ^ 64
            
        if mode == LOOP_NORMAL:
            self.flags = self.flags | 16
        elif mode == LOOP_PINGPONG:
            self.flags = self.flags | 64

    def setLoopNormal(self):
        self.setLoopMode(LOOP_NORMAL)

    def setLoopPingPong(self):
        self.setLoopMode(LOOP_PINGPONG)
            

    def bitsPerSample(self):
        return (self.samplesize() / self.channels) * 8

    def bytesPerSample(self):
        return (self.samplesize() / self.channels)

    def samplesize(self):
        size = 1
        if self.flags & 2:
            size = 2
        if self.flags & 4:
            size = size * 2
        return size

    def update(self):
        self.sampleSize = self.samplesize()
        self.lengthInBytes = self.sampleSize * self.length
        self.parseflags()
        

    def load(self, fp, pos=-1, loadData=1):
        """loads sample from an open file.  optional second argument gives filepos to load from,
        otherwise the current position is used."""
        try:
            if pos <> -1:
                fp.seek(pos)

            self.beginHeaderPos = fp.tell()
            
            autoload(fp, self)

            if self.headerID != "IMPS":
                print "-- Corrupt sample header"
                return 0

            self.endHeaderPos = fp.tell()

            self.beginDataPos = self.sampleOffset            

            # now load sampledata
            self.sampleSize = self.samplesize()
            self.lengthInBytes = self.sampleSize * self.length
            if DEBUGSMP:
                print "loading ss", self.sampleSize, "lib", self.lengthInBytes, "len", self.length

            # set length in data bytes
            corrupt = 0
            if self.flags & 8: # compressed
                fp.seek(self.sampleOffset)
                lendata = self.lengthInBytes
                numBytesData = 0
                while lendata:
                    if lendata < 0x8000:
                        blklen = lendata
                    else:
                        blklen = 0x8000
                    # first two bytes (unsigned word) are the size of the compressed data
                    datasize = fp.read(struct.calcsize("<H"))
                    #print "ds", datasize, len(datasize)
                    if len(datasize):
                        datasize = struct.unpack("<H", datasize)[0]
                        numBytesData += (datasize + 2)    # plus 2 for the size word!
                        lendata -= blklen
                        try:
                            fp.seek(datasize, 1)
                        except IOError:
                            lendata = 0
                            corrupt = 1
                    else:
                        lendata = 0
                        corrupt = 1

                #print ".. Setting len bytes to", numBytesData
                self.numBytesData = numBytesData
            else:
                self.numBytesData = self.lengthInBytes

            #numBytesData is the length of the compressed data?

            #print "datasize", self.numBytesData, self.lengthInBytes

            if loadData:
                fp.seek(self.sampleOffset)
                #self.data = fp.read(self.lengthInBytes)
                self.data = fp.read(self.numBytesData)
                self.endDataPos = fp.tell()
            else:
                self.data = []
            if DEBUGSMP:
                print "sample bytes loaded", len(self.data)
            self.update()
            #if corrupt:
            #    return 0
            #else:
            #    return 1
            return 1
        except:
            print "-- Failed to load sample"
            traceback.print_exc()
            return 0

    def saveheader(self, fp, pos=-1, header=None, headIndex=0):
        """saves the sample header. if an ITHeader is specified, its sample offset is updated
        to reflect the new file position.  headIndex should also be specified with the header."""

        if pos <> -1:
            fp.seek(pos)
            if DEBUGSMP:
                print "SMPSAVE seeking to", pos
        curpos = fp.tell()
        if DEBUGSMP:
            print "SMPSAVE starting at", curpos

        self.beginHeaderPos = curpos        

        autosave(fp, self)
        if DEBUGSMP:
            print "SMPSAVE saved, now at", fp.tell()

        self.endHeaderPos = fp.tell()            

        # if header and sample index supplied, update header
        if header != None:
            header.sampleOffsets[headIndex] = curpos
            if DEBUGSMP:
                print "SMPSAVE set sampleoffset", headIndex, "to", curpos
            header.changedSinceSave = 1

        self.changedSinceSave = 0            


    def savedata(self, fp, pos=-1, header=None, headIndex=0, updateSampleOffset=1, saveSampleOffset=1):
        """
        saves the sample data to current filepos or specified offset.
        if updateSampleOffset, the sampleOffset of the sampleheader is updated to where the sample data was written.
        if saveSampleOffset, and a header and headIndex are specified, the sample header is written again to its current
        position (to save the updated sampleOffset value)
        """

        if pos <> -1:
            fp.seek(pos)
        curpos = fp.tell()
        if DEBUGSMP:
            print "here we are at", curpos

        self.beginDataPos = curpos

        if curpos <> self.sampleOffset:
            self.changedSinceSave = 1

        fp.write(self.data)
        if DEBUGSMP:
            print "we saved the data, now we're at", fp.tell()

        self.endDataPos = fp.tell()            

        if (updateSampleOffset):
            self.sampleOffset = curpos
            if DEBUGSMP:
                print "updated sampleheader.sampleOffset to", curpos

        if (saveSampleOffset) and (header != None):
            savepos = fp.tell()
            self.saveheader(fp, pos=header.sampleOffsets[headIndex])
            fp.seek(savepos)
            self.changedSinceSave = 0
                    
    def numSamples(self):
        return self.length

    def dump(self):
        autodump(self)
        print "byte length", len(self.data)

    def isEmpty(self):
        if self.data:
            return 0
        else:
            return 1
            



class ITInstrumentEnvelope(object):
    def __init__(self):
        self.flag = 0                   # unsigned char
        self.numNodePoints = 0          # unsigned char
        self.loopBeginning = 0          # unsigned char
        self.loopEnd = 0                # unsigned char
        self.sustainLoopBeginning = 0   # unsigned char
        self.sustainLoopEnd = 0         # unsigned char

        #struct {
        #    unsigned char yValue;
        #    short tickNumber;
        #} nodePoints[25];

        self.nodePoints = []
        for x in xrange(0, 25):
            self.nodePoints.append({'yvalue':0, 'tick':0})

        self.formats = {}
        self.formats["flag"] = "<B"
        self.formats["numNodePoints"] = "<B"
        self.formats["loopBeginning"] = "<B"
        self.formats["loopEnd"] = "<B"
        self.formats["sustainLoopBeginning"] = "<B"
        self.formats["sustainLoopEnd"] = "<B"

        # vars to autoload / save
        self.vars = ["flag", "numNodePoints", "loopBeginning", "loopEnd", "sustainLoopBeginning", "sustainLoopEnd"]

    def load(self, fp, pos=-1):
        """loads from an open file."""
        if pos <> -1:
            fp.seek(pos)

        autoload(fp, self)

        # now load nodepoints
        for x in xrange(0, 25):
            yvalue = fp.read(struct.calcsize("<B"))
            yvalue = struct.unpack("<B", yvalue)
            tick = fp.read(struct.calcsize("<h"))
            tick = struct.unpack("<h", tick)
            self.nodePoints[x]['yvalue'] = yvalue[0]
            self.nodePoints[x]['tick'] = tick[0]

    def save(self, fp):
        """save to an open file."""
        autosave(fp, self)

        # now save nodepoints
        for x in self.nodePoints:
            yvalue = struct.pack("<B", x['yvalue'])
            tick = struct.pack("<h", x['tick'])
            fp.write(yvalue)
            fp.write(tick)
            


class ITInstrument(object):
    def __init__(self):
        self.headerID = "IMPI"          # char[4]
        self.filename = ""              # char[12]
        self.nullByte = 0               # unsigned char
        self.newNoteAction = 0          # unsigned char
        self.duplicateCheckType = 0     # unsigned char
        self.duplicateCheckAction = 0   # unsigned char

        self.fadeOut = 0                # short                

        self.pitchPanSeperation = 0     # unsigned char
        self.pitchPanCenter = 0         # unsigned char

        self.globalVolume = 64          # unsigned char
        self.defaultPan = 32            # unsigned char
        self.randomVolumeVariation = 0  # unsigned char - percentage
        self.randomPanningVariation = 32 # unsigned char

        self.trackerVersion = 0         # short                
        self.numSamples = 1             # unsigned char.  number of samples associated with this instrument.

        self.extraByte = 0              # unsigned char

        self.name = ""                  # char[26]
        
        self.extraWord = 0              # short                

        self.midiChannel = 0            # unsigned char
        self.midiProgram = 0            # unsigned char
        self.midiBank = 0               # short                

        self.__noteTable = []
        # noteTable will be a list of tuples, where each tuple is (note, sample)
        #for x in xrange(0, 120):
            #self.__noteTable.append((0,0))
        self.__noteTable = [(x,0) for x in xrange(0, 120)] 

        self.volumeEnvelope = ITInstrumentEnvelope()
        self.panningEnvelope = ITInstrumentEnvelope()
        self.pitchEnvelope = ITInstrumentEnvelope()

        self.extra7 = ""                # char[7], because all instrument headers are 554 bytes like the old instrument format.

        # the following members are not stored in the file format
        self.__usedSamples = []  # list of samples used by the instrument.

        self.beginHeaderPos = 0
        self.endHeaderPos = 0

        self.formats = {}
        self.formats["headerID"] = "<4s"
        self.formats["filename"] = "<12s"
        self.formats["nullByte"] = "<B"
        self.formats["newNoteAction"] = "<B"
        self.formats["duplicateCheckType"] = "<B"
        self.formats["duplicateCheckAction"] = "<B"
        self.formats["fadeOut"] = "<h"
        self.formats["pitchPanSeperation"] = "<B"
        self.formats["pitchPanCenter"] = "<B"
        self.formats["globalVolume"] = "<B"
        self.formats["defaultPan"] = "<B"
        self.formats["randomVolumeVariation"] = "<B"
        self.formats["randomPanningVariation"] = "<B"
        self.formats["trackerVersion"] = "<h"
        self.formats["numSamples"] = "<B"
        self.formats["extraByte"] = "<B"
        self.formats["name"] = "<26s"
        self.formats["extraWord"] = "<h"
        self.formats["midiChannel"] = "<B"
        self.formats["midiProgram"] = "<B"
        self.formats["midiBank"] = "<h"
        
        self.vars = ["headerID", "filename", "nullByte", "newNoteAction", "duplicateCheckType", "duplicateCheckAction", \
                     "fadeOut", "pitchPanSeperation", "pitchPanCenter", "globalVolume", "defaultPan", "randomVolumeVariation", \
                     "randomPanningVariation", "trackerVersion", "numSamples", "extraByte", "name", "extraWord", "midiChannel", \
                     "midiProgram", "midiBank"]

    def setName(self, name):
        self.name = name[:26]

    def setFileName(self, name):
        self.filename = name[:12]
        
    def getNoteTable(self):
        return self.__noteTable

    def clearSamples(self):
        self.__noteTable = [(x,0) for x in xrange(0, 120)] 
        self.__usedSamples = [0]

    def setAllSamples(self, sampleIndex):
        self.__noteTable = [(x, sampleIndex) for x in xrange(0, 120)] 
        self.__usedSamples = [sampleIndex]

    def transposeSamples(self, transpose):
        nt = self.__noteTable
        self.__usedSamples = []
        for i in range(len(nt)):
            val = nt[i]
            newsamp = val[1] + transpose
            val = (val[0], newsamp)
            nt[i] = val
            if newsamp not in self.__usedSamples:
                self.__usedSamples.append(newsamp)

    def getGlobalVolume(self):
        return self.globalVolume

    def setGlobalVolume(self, volume):
        self.globalVolume = max(min(volume, 128), 0)

    def usedSamples(self):
        """ returns list of samples used by this instrument """
        return self.__usedSamples
            

    def load(self, fp, pos=-1):
        """loads from an open file."""

        if pos <> -1:
            fp.seek(pos)

        self.beginHeaderPos = fp.tell()            
        
        autoload(fp, self)

        #TODO:
        # i'm allowing IMP\x01 because a number of files in the hornet archive had single instruments with that
        # headerID.  i'm not really sure it's a good idea though..
        if self.headerID not in ("IMPI", "IMP\x01"):
            print "-- Corrupt instrument header", self.headerID
            return 0

        # if it was IMP\x01, change it
        self.headerID = "IMPI"

        # load noteTable
        for x in xrange(0, 120):
            note = fp.read(struct.calcsize("<B"))
            note = struct.unpack("<B", note)
            sample = fp.read(struct.calcsize("<B"))
            sample = struct.unpack("<B", sample)
            #self.__noteTable[x]['note'] = note[0]
            #self.__noteTable[x]['sample'] = sample[0]
            self.__noteTable[x] = (note[0], sample[0])
            if sample[0] not in self.__usedSamples:
                self.__usedSamples.append(sample[0])

        # load envelopes            
        self.volumeEnvelope.load(fp)
        self.panningEnvelope.load(fp)
        self.pitchEnvelope.load(fp)

        self.extra7 = fp.read(struct.calcsize("<7s"))
        self.extra7 = struct.unpack("<7s", self.extra7)

        self.endHeaderPos = fp.tell()        

        return 1
    

    def save(self, fp, pos=-1, header=None, headIndex=0):
        """saves instrument to open file. if an ITHeader is specified, its instrument offset is updated
        to reflect the new file position.  headIndex should also be specified with the header."""

        self.extra7 = "\x00" * 7

        if pos <> -1:
            fp.seek(pos)
        curpos = fp.tell()

        self.beginHeaderPos = curpos

        autosave(fp, self)

        # save noteTable
        for x in self.__noteTable:
            n, s = x
            note = struct.pack("<B", n)
            sample = struct.pack("<B", s)
            fp.write(note)
            fp.write(sample)

        # save envelopes            
        self.volumeEnvelope.save(fp)
        self.panningEnvelope.save(fp)
        self.pitchEnvelope.save(fp)

        extra7 = struct.pack("<7s", str(self.extra7))
        fp.write(extra7)

        self.endHeaderPos = fp.tell()        

        if header != None:
            header.instrumentOffsets[headIndex] = curpos
            header.changedSinceSave = 1

        self.changedSinceSave = 0            
        

    #TODO: check ins loading and saving
    def dump(self, table=0):
        autodump(self)
        autodump(self.volumeEnvelope)
        autodump(self.panningEnvelope)
        autodump(self.pitchEnvelope)

        if table:
            for x in self.__noteTable:
                print "n", x[0], "s", x[1]

        print "usedSamples:", self.usedSamples()



class ITInstrumentOld(object):
    # Old Instrument Format
    
    def __init__(self):
        self.headerID = "IMPI"          # char[4]
        self.filename = ""              # char[12]
        self.nullByte = 0               # unsigned char

        self.flag = 0                   # unsigned char.  bit 0 = use vol envelope, bit 1 = use vol loop, bit 2 = use sustain vol loop
        self.volumeLoopStart = 0        # unsigned char
        self.volumeLoopEnd = 0          # unsigned char
        self.sustainLoopStart = 0        # unsigned char
        self.sustainLoopEnd = 0          # unsigned char

        self.fadeOut = 0                # short                

        self.duplicateNoteCheck = 0     # 0 / 1
        self.newNoteAction = 0          # unsigned char

        self.trackerVersion = 0         # short                

        self.numSamples = 1             # unsigned char.  number of samples associated with this instrument.

        self.extraByte = 0              # unsigned char

        self.name = ""                  # char[26]

        self.extraWord = 0              # short 
        self.extraWord2 = 0              # short 
        self.extraWord3 = 0              # short 

        # these aren't auto-loaded or auto-saved.

        self.__noteTable = []
        # noteTable will be a list of tuples, where each tuple is (note, sample)
        for x in xrange(0, 120):
            #self.__noteTable.append({'note':0, 'sample':0})
            self.__noteTable.append((0,0))

        self.volumeEnvelope = ""        # char[200]
        self.volumeNodePoints = ""      # char[50] - 25 x 2 bytes - tick, then magnitude
        
        # meta-data for autoload/save
        
        self.formats = {}
        self.formats["headerID"] = "<4s"
        self.formats["filename"] = "<12s"
        self.formats["nullByte"] = "<B"
        self.formats["flag"] = "<B"
        self.formats["volumeLoopStart"] = "<B"
        self.formats["volumeLoopEnd"] = "<B"
        self.formats["sustainLoopStart"] = "<B"
        self.formats["sustainLoopEnd"] = "<B"
        self.formats["fadeOut"] = "<h"
        self.formats["duplicateNoteCheck"] = "<B"
        self.formats["newNoteAction"] = "<B"
        self.formats["trackerVersion"] = "<h"
        self.formats["numSamples"] = "<B"
        self.formats["extraByte"] = "<B"
        self.formats["name"] = "<26s"
        self.formats["extraWord"] = "<h"
        self.formats["extraWord2"] = "<B"
        self.formats["extraWord3"] = "<B"
        
        self.vars = ["headerID", "filename", "nullByte", "flag", "volumeLoopStart", "volumeLoopEnd", \
                     "sustainLoopStart", "sustainLoopEnd", "fadeOut", "duplicateNoteCheck", "newNoteAction", "trackerVersion", \
                     "numSamples", "extraByte", "name", "extraWord", "extraWord2", "extraWord3"]

        # the following members are not stored in the file format,
        # but are here for compatibility with new instrument format:        
        
        self.duplicateCheckType = 0     # unsigned char
        self.duplicateCheckAction = 0   # unsigned char

        self.pitchPanSeperation = 0     # unsigned char
        self.pitchPanCenter = 0         # unsigned char

        self.globalVolume = 64          # unsigned char
        self.defaultPan = 32            # unsigned char
        self.randomVolumeVariation = 0  # unsigned char - percentage
        self.randomPanningVariation = 32 # unsigned char

        self.midiChannel = 0            # unsigned char
        self.midiProgram = 0            # unsigned char
        self.midiBank = 0               # short                

        self.volumeEnvelope = ITInstrumentEnvelope()
        self.panningEnvelope = ITInstrumentEnvelope()
        self.pitchEnvelope = ITInstrumentEnvelope()

        # the following members are not stored in the file format
        self.__usedSamples = []  # list of samples used by the instrument.

        self.beginHeaderPos = 0
        self.endHeaderPos = 0


    def usedSamples(self):
        """ returns list of samples used by this instrument """
        return self.__usedSamples
            

    def load(self, fp, pos=-1):
        """loads from an open file."""

        if pos <> -1:
            fp.seek(pos)

        self.beginHeaderPos = fp.tell()            
        
        autoload(fp, self)

        if self.headerID != "IMPI":
            print "-- Corrupt instrument header"
            return 0

        # load noteTable
        for x in xrange(0, 120):
            note = fp.read(struct.calcsize("<B"))
            note = struct.unpack("<B", note)
            sample = fp.read(struct.calcsize("<B"))
            sample = struct.unpack("<B", sample)
            #self.__noteTable[x]['note'] = note[0]
            #self.__noteTable[x]['sample'] = sample[0]
            self.__noteTable[x] = (note[0], sample[0])
            if sample[0] not in self.__usedSamples:
                self.__usedSamples.append(sample[0])

        # load volume envelope
        self.volumeEnvelope = fp.read(struct.calcsize("<200s"))
        self.volumeEnvelope = struct.unpack("<200s", self.volumeEnvelope)
        self.volumeNodePoints = fp.read(struct.calcsize("<50s"))
        self.volumeNodePoints = struct.unpack("<50s", self.volumeNodePoints)

        self.endHeaderPos = fp.tell()        

        return 1
    

    def save(self, fp, pos=-1, header=None, headIndex=0):
        """saves instrument to open file. if an ITHeader is specified, its instrument offset is updated
        to reflect the new file position.  headIndex should also be specified with the header."""

        if pos <> -1:
            fp.seek(pos)
        curpos = fp.tell()

        self.beginHeaderPos = curpos

        autosave(fp, self)

        # save noteTable
        for x in self.__noteTable:
            n, s = x
            note = struct.pack("<B", n)
            sample = struct.pack("<B", s)
            fp.write(note)
            fp.write(sample)

        # save volume envelope
        venv = struct.pack("<200s", self.volumeEnvelope)
        nodes = struct.pack("<50s", self.volumeNodePoints)
        fp.write(venv)
        fp.write(nodes)

        self.endHeaderPos = fp.tell()        

        if header != None:
            header.instrumentOffsets[headIndex] = curpos
            header.changedSinceSave = 1

        self.changedSinceSave = 0            
        

    #TODO: check ins loading and saving
    def dump(self, table=0):
        autodump(self)
        autodump(self.volumeEnvelope)
        autodump(self.panningEnvelope)
        autodump(self.pitchEnvelope)

        if table:
            for x in self.__noteTable:
                print "n", x[0], "s", x[1]

        print "usedSamples:", self.usedSamples()


# the values of an S effect that are position based effects.
SFXPOSVALS = range(0xB0, 0xB9) + range(0xE0, 0xE9)

#itc is a pyrex module to speed up the ITEventData class
#import itc
#ITEventData = itc.ITEvent


##class ITEventData(object):
##    def __init__(self):
##        #self.note = EVENT_NULL_NOTE
##        #self.instrument = EVENT_NULL_INSTRUMENT
##        #self.volpan = self.command = self.commandvalue = EVENT_NULL_VALUE
##
##        # hack for speed
##        self.__dict__ = {'note': 0, 'instrument': 0, 'command': 255, 'commandvalue': 255, 'volpan': 255}
##
##    def getNote(self):
##        return self.note
##
##    def getInstrument(self):
##        return self.instrument
##
##    def getVolPan(self):
##        return self.volpan
##
##    def getCommand(self):
##        return self.command
##
##    def getCommandValue(self):
##        return self.commandvalue
##
##    def setNote(self, value):
##        self.note = value
##
##    def setInstrument(self, value):
##        self.instrument = value
##
##    def setVolPan(self, value):
##        self.volpan = value
##
##    def setCommand(self, value):
##        self.command = value
##
##    def setCommandValue(self, value):
##        self.commandvalue = value
##
##
##    def clear(self):
##        """set all event data to defaults (no data).
##        the exception are B,C,A,T, SB, and SE commands, which are retained to have them function as pattern settings.
##        (they are position jump, tempo, and pattern looping commands)"""
##        self.note = 0
##        self.instrument = 0
##        self.volpan = EVENT_NULL_VALUE
##        # B,C,SB,SE, A,T commands are considered pattern settings, and aren't cleared
##        if (self.command not in (1,2,3,20)) and not (self.command==19 and self.commandvalue in SFXPOSVALS):    # A,B,C,T
##            self.command = self.commandvalue = EVENT_NULL_VALUE
##
##    def isNoteEmpty(self):
##        """returns true if this event is empty of note data.  note data is considered a note or instrument value,
##        not any commands, volpans, etc."""
##        if self.note in [EVENT_NULL_NOTE, EVENT_NOTE_OFF] and self.instrument == EVENT_NULL_INSTRUMENT:
##            return 1
##        else:
##            return 0
##
##    def isEmpty(self):
##        return (self.note, self.instrument, self.volpan, self.command, self.commandvalue) == (EVENT_NULL_NOTE, EVENT_NULL_INSTRUMENT, EVENT_NULL_VALUE, EVENT_NULL_VALUE, EVENT_NULL_VALUE)
##            
##    def clearInstrument(self):
##        """deletes instrument value of event (setting to 0), but keeps any other event data."""
##        self.instrument = EVENT_NULL_INSTRUMENT
##
##    def clearNote(self):
##        """deletes the note value of the event (setting to 0), but keeps any other event data."""
##        self.note = EVENT_NULL_NOTE
##
##    def setNoteOff(self):
##        """sets note data to a 'note off' value.  other event data is unchanged."""
##        self.note = EVENT_NOTE_OFF
##
##    def show(self):
##        print self.note,"-",self.instrument,"-",self.volpan,"-",self.command

# index constants for the data array of ITEventDataFast
EV_NOTE = 0
EV_INSTRUMENT = 1
EV_VOLPAN = 2
EV_COMMAND = 3
EV_COMMANDVALUE = 4

EventDataLookup = { "note": EV_NOTE, "instrument": EV_INSTRUMENT, "volpan": EV_VOLPAN,
                    "command": EV_COMMAND, "commandvalue": EV_COMMANDVALUE }

BLANKNOTEDATA = array.array("B", [EVENT_NULL_NOTE, EVENT_NULL_INSTRUMENT,
                                          EVENT_NULL_VALUE, EVENT_NULL_VALUE, EVENT_NULL_VALUE])


#ITEventDataFast is OBSOLETE, use itc.ITEvent instead
class ITEventDataFast(object):
    """ optimized version of ITEventData """
    def __init__(self):
        self.data = array.array("B", [EVENT_NULL_NOTE, EVENT_NULL_INSTRUMENT,
                                          EVENT_NULL_VALUE, EVENT_NULL_VALUE, EVENT_NULL_VALUE])
        # data array = [note, instrument, volpan, command, commandValue]

    def note(self, note):
        self.data[0] = note

    def instrument(self, ins):
        self.data[1] = ins

    def volpan(self, volpan):
        self.data[2] = volpan

    def command(self, command):
        self.data[3] = command

    def commandvalue(self, value):
        self.data[4] = value

    """
    def __getattr__(self, key):
        # for compatibility / direct access by attribute name
        try:
            return self.__dict__[key]
        except KeyError:
            return self.__dict__["data"][EventDataLookup[key]]

    def __setattr__(self, key, value):
        # for compatibility / direct access by attribute name
        try:
            try:
                self.__dict__["data"][EventDataLookup[key]] = value
            except KeyError:
                self.__dict__[key] = value
        except:
            traceback.print_exc()
            print "Setting", key, value
    """
                
    def clear(self):
        """set all event data to defaults (no data).
        the exception is C commands, which are retained to have them function as pattern settings."""

        # C commands are considered pattern settings, and aren't cleared
        if (self.command != 3):
            # clear all
            self.__init__()
        else:
            # clear only note, instrument and value
            self.data[0] = EVENT_NULL_NOTE
            self.data[1] = EVENT_NULL_INSTRUMENT
            self.data[2] = EVENT_NULL_VALUE

    def isBlank(self):
        # true if note is completely blank
        return (self.data == BLANKNOTEDATA)

    def isNoteEmpty(self):
        """returns true if this event is empty of note data.  note data is considered a note or instrument value,
        not any commands, volpans, etc."""
        if self.data[0] in [EVENT_NULL_NOTE, EVENT_NOTE_OFF] and self.data[1] == EVENT_NULL_INSTRUMENT:
            return 1
        else:
            return 0

    def clearInstrument(self):
        """deletes instrument value of event (setting to 0), but keeps any other event data."""
        self.data[1] = EVENT_NULL_INSTRUMENT

    def clearNote(self):
        """deletes the note value of the event (setting to 0), but keeps any other event data."""
        self.data[0] = EVENT_NULL_NOTE

    def setNoteOff(self):
        """sets note data to a 'note off' value.  other event data is unchanged."""
        self.data[0] = EVENT_NOTE_OFF

    def show(self):
        print self.data[EV_NOTE],"-",self.data[EV_INSTRUMENT],"-",self.data[EV_VOLPAN],"-",self.data[EV_COMMAND]



class ITChannelData(object):
    def __init__(self, rows=0):
        #self.events = [] # list of ITEventData
        self.numrows = rows
        #for i in xrange(0, self.numrows):
        #    self.events.append(ITEventData())

        self.events = [ITEventData() for i in xrange(0, rows)]
        resize_list(self.events, rows)
        #self.events = []

    def isBlank(self):
        for e in self.events:
            if not e.isBlank():
                return 0
        return 1

    def clear(self):
        for e in self.events:
            e.clear()

    def rowList(self):
        return range(0, len(self.events))

    def SetNumRows(self, numrows):
        while len(self.events) < numrows:
            self.events.append(ITEventData())
        if len(self.events) > numrows:
            self.events = self.events[0:numrows-1]
        self.numrows = numrows            

    def AddRows(self, numrows):
        self.SetNumRows(self.numrows + numrows)
        #print "added", numrows, "rows"

    def SetNote(self, frame, value):
        if (frame < self.numrows):
            self.events[frame].setNote(value)

    def SetInstrument(self, frame, value):
        if (frame < self.numrows):
            self.events[frame].setInstrument(value)

    def SetVolPan(self, frame, value):
        if (frame < self.numrows):
            self.events[frame].setVolPan(value)

    def SetCommand(self, frame, command, value):
        if (frame < self.numrows):
            self.events[frame].setCommand(command)
            self.events[frame].setCommandValue(value)

    def show(self):
        for e in self.events:
            e.show()

    def setFromSeq(self, seq):
        if len(self.events) < len(seq):
            self.SetNumRows(len(seq))
        curframe = 0
        for x in seq:
            self.SetNote(curframe, x.getNote())
            curframe = curframe + x.duration

    def noteAdd(self, value):
        """add specified value to all notes in this channel"""
        for e in self.events:
            if e.getNote() != 0:
                e.setNote(e.getNote() + value)
            



# for ITChannelDataFast
class ITEventList(dict):
    def __init__(self, numrows=0):
            dict.__init__(self)
            self.numrows = numrows
            
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            # if in range, return blank event
            if int(key) < self.numrows:
                return ITEventDataLazy(self, key)
                #return ITEventData()
            else:
                return None


#TODO: ITChannelDataFast is OBSOLETE
class ITChannelDataFast:
    def __init__(self, rows=0):
        #self.events = [] # list of ITEventData
        self.events = ITEventList(rows)
        self.numrows = rows
        #for i in xrange(0, self.numrows):
        #    self.events.append(ITEventData())
        #resize_list(self.events, rows)

    def clear(self):
        for e in self.events.values():
            e.clear()

    def rowList(self):
        return range(0, self.numrows)

    def SetNumRows(self, numrows):
        #while len(self.events) < numrows:
        #    self.events.append(ITEventData())
        #if len(self.events) > numrows:
        #    self.events = self.events[0:numrows-1]
        self.numrows = numrows
        self.events.numrows = numrows

        for key in self.events.keys():
            if key > numrows:
                del self.events[key]

    def AddRows(self, numrows):
        self.SetNumRows(self.numrows + numrows)
        #print "added", numrows, "rows"

    def SetNote(self, frame, value):
        if (frame < self.numrows):
            self.events[frame].setNote(value)

    def SetInstrument(self, frame, value):
        if (frame < self.numrows):
            self.events[frame].setInstrument(value)

    def SetVolPan(self, frame, value):
        if (frame < self.numrows):
            self.events[frame].setVolPan(value)

    def SetCommand(self, frame, command, value):
        if (frame < self.numrows):
            self.events[frame].setCommand(command)
            self.events[frame].setCommandValue(value)

    def show(self):
        for e in self.events:
            e.show()

    def setFromSeq(self, seq):
        if len(self.events) < len(seq):
            self.SetNumRows(len(seq))
        curframe = 0
        for x in seq:
            self.SetNote(curframe, x.getNote())
            curframe = curframe + x.duration

    def noteAdd(self, value):
        """add specified value to all notes in this channel"""
        for e in self.events.values():
            if e.getNote() != 0:
                e.setNote(e.getNote() + value)
            
            


class ITRowData(object):
    def __init__(self):
        self.channels = []
        for i in xrange(0, MAX_PATTERN_CHANNELS):
            self.channels.append(ITEventData())

    def __getitem__(self, channel):
        return self.channels[channel]

class ITPattern(object):
    def __init__(self, numrows=DEFAULT_NUM_ROWS):
        self.numrows = numrows
        self.numchannels = 0
        # TODO: does self.channels really need null values, or can it just grow as needed?
        # the list of nulls was a holdover from the C code.
        # UPDATE: actually, i think it needs null values for editing purposes, but i still
        # have to look into this.
        self.channels = []
        for i in xrange(0, MAX_PATTERN_CHANNELS):
            self.channels.append(None)

    def set(self, track, row, note, instrument, volume, command, commandValue):
        #print track, row, note, instrument, volume, command, commandValue
        self.setNote(track, row, note)
        self.setInstrument(track, row, instrument)
        self.setVolpan(track, row, volume)
        self.setCommand(track, row, command, commandValue)

    def setEvent(self, track, row, event):
        self.set(track, row, event[0], event[1], event[2], event[3], event[4])

    def get(self, track, row):
        try:
            return (self.channels[track].events[row].getNote(), self.channels[track].events[row].getInstrument(), self.channels[track].events[row].getVolPan(), self.channels[track].events[row].getCommand(), self.channels[track].events[row].getCommandValue())
        except:
            return (0,0,0,0,0)

    def track(self, num):
        return self.channels[num]

    def numTracks(self):
        #return len(self.channels)
        return self.numchannels

    def clear(self):
        for c in self.channels:
            if c:
                c.clear()

    def CalcNumRows(self):
        maxnumrows = 0
        for c in self.channels:
            if c and c.numrows > maxnumrows:
                maxnumrows = c.numrows
        self.numrows = maxnumrows
        return self.numrows

    def AddChannel(self, rows=None, num=1):

        if not rows:
            rows = self.numrows
        
        for i in xrange(0, num):
            if (self.numchannels >= MAX_PATTERN_CHANNELS):
                return 0

            self.channels[self.numchannels] = ITChannelData(rows)
            
            self.numchannels = self.numchannels + 1

    def AddChannelsUpTo(self, num, rows=None):
        # if the channel specified hasn't been allocated, allocate as many channels as needed
        while (self.numchannels <= num):
            self.AddChannel(rows)

    def AddRows(self, rows=1):
        """ add rows to all channels in the pattern """
        for c in self.channels:
            if c:
                c.AddRows(rows)
        self.CalcNumRows()

    def AddRowsUpTo(self, rows):
        toAdd = rows - self.numrows
        if toAdd:
            self.AddRows(toAdd)

    def RemoveChannel(self):
        #TODO
        pass

    def RemoveAllChannels(self):
        #TODO
        pass

    def note(self, channel, frame):
        return self.channels[channel].events[frame].getNote()

    def instrument(self, channel, frame):
        return self.channels[channel].events[frame].getInstrument()
        
    def volpan(self, channel, frame):
        return self.channels[channel].events[frame].getVolPan()

    def command(self, channel, frame):
        return self.channels[channel].events[frame].getCommand()

    def commandvalue(self, channel, frame):
        return self.channels[channel].events[frame].getCommandValue()


    def clearNote(self, channel, frame):
        #self.AddRowsUpTo(frame)
    	#self.AddChannelsUpTo(channel, self.numrows)
        if not (self.numchannels <= channel):
        	self.channels[channel].SetNote(frame, 0)


    def SetChannelNote(self, channel, frame, value):
        #self.AddRowsUpTo(frame)
    	#self.AddChannelsUpTo(channel, self.numrows)
        while (self.numchannels <= channel):
            #print "wants channel", channel
            self.AddChannel(self.numrows)
    	self.channels[channel].SetNote(frame, value)

    def SetChannelInstrument(self, channel, frame, value):
        #self.AddRowsUpTo(frame)
    	self.AddChannelsUpTo(channel, self.numrows)
    	self.channels[channel].SetInstrument(frame, value)

    def SetChannelVolPan(self, channel, frame, value):
        #self.AddRowsUpTo(frame)
    	self.AddChannelsUpTo(channel, self.numrows)
    	self.channels[channel].SetVolPan(frame, value)

    def SetChannelCommand(self, channel, frame, command, value):
        #self.AddRowsUpTo(frame)
    	self.AddChannelsUpTo(channel, self.numrows)
    	self.channels[channel].SetCommand(frame, command, value)

    setNote = SetChannelNote
    setInstrument = SetChannelInstrument
    setVolpan = SetChannelVolPan
    setCommand = SetChannelCommand


    def setChannelFromSeq(self, channel, seq):
        #self.AddRowsUpTo(frame)
        self.AddChannelsUpTo(channel, self.numrows)
        self.channels[channel].setFromSeq(seq)

    def setFromSeq(self, seq):
        """self should be a list of SeqNote lists"""
        print "hello from setfromseq"
        frame = 0
        for notelist in seq:
            print "notelist", notelist
            track = 0
            for seqnote in notelist:
                self.setNote(track, frame, seqnote.getNote())
                track = track + 1
            frame = frame + notelist[0].duration
            print "frame", frame
            #TODO: allow for varying durations in the same notelist
            
    def channelNoteAdd(self, channel, value):
        self.AddChannelsUpTo(channel, self.numrows)
        self.channels[channel].noteAdd(value)

    def noteAdd(self, value):
        for x in self.channelList():
            if self.channels[x] != None:
                self.channels[x].noteAdd(value)
   

    def channelList(self):
        return range(0, len(self.channels))

    def getBlankTracks(self, totaltracks):
        return [i for i in range(len(self.channels)) if (i < totaltracks and not self.channels[i]) or (self.channels[i] and self.channels[i].isBlank())]
        
        


    def makeSolo(self, tracks):
        """clear all tracks except specified track(s)"""
        # allow user to pass single track or list of tracks
        tracks = tolist(tracks)
        
        channels = self.channelList()
        for x in channels:
            if x not in tracks:
                if self.channels[x] != None:
                    self.channels[x].clear()

    def transposeInstruments(self, transpose):
        channels = self.channelList()
        for chan in channels:
            channel = self.channels[chan]
            if channel:
                for event in channel.events:
                    if event.getInstrument() != EVENT_NULL_INSTRUMENT:
                        #print event.instrument, "to", event.instrument+transpose
                        event.setInstrument(event.getInstrument() + transpose)

    def soloInstruments(self, instruments, noteoffs=1):
        """clear all note events except those of the specified instruments.
        requires the sequence to be made instrument-explicit first.

        if noteoffs is true, then the notes are replaced with noteoffs instead of being deleted.
        """
        # allow user to pass single instrument or list of instruments
        instruments = tolist(instruments)

        channels = self.channelList()
        for x in channels:
            channel = self.channels[x]
            if channel:
                for event in channel.events:
                    # if an instrument is defined for this event and is not in the allowed instrument list,
                    # delete the note (replacing with either blank or note off), and clear the instrument value
                    if (event.getInstrument() != EVENT_NULL_INSTRUMENT) and (event.getInstrument() not in instruments):
                        if noteoffs:
                            event.setNoteOff()
                            #TODO: if volume not already null, we should check it and save it for running value
                            if event.getVolPan() < 65:
                                # if less than 65, it is a volume setting (0-64)
                                #print "wiping volume", event.getVolPan()
                                event.setVolPan(255)
                        else:
                            event.clearNote()
                        event.clearInstrument()


    def explicitVolumes(self):
        """make all events have explicit instrument values (instead of data memory)"""
        #TODO - convert only significant events?
        channels = self.channelList()
        memory = {}
        for x in channels:
            channel = self.channels[x]
            #HERE
            #memory[x] = None
            memory[x] = 0
            if channel:
                for event in channel.events:
                    if event.getInstrument() != EVENT_NULL_INSTRUMENT:
                        memory[x] = event.getInstrument()
                    else:
                        #TODO: are any volpan or commands considered note triggers?
                        # (EVENT_NULL_NOTE, EVENT_NOTE_CUT, EVENT_NOTE_OFF)
                        if event.getNote() not in (0,254,255):
                            #print "si", memory[x]
                            event.setInstrument(memory[x])


        
    def explicitInstruments(self):
        """make all events have explicit instrument values (instead of data memory)"""
        #TODO - convert only significant events?
        channels = self.channelList()
        memory = {}
        for x in channels:
            channel = self.channels[x]
            #HERE
            #memory[x] = None
            memory[x] = 0
            if channel:
                for event in channel.events:
                    if event.getInstrument() != EVENT_NULL_INSTRUMENT:
                        memory[x] = event.getInstrument()
                    else:
                        #TODO: are any volpan or commands considered note triggers?
                        # (EVENT_NULL_NOTE, EVENT_NOTE_CUT, EVENT_NOTE_OFF)
                        if event.getNote() not in (0,254,255):
                            #print "si", memory[x]
                            event.setInstrument(memory[x])

    def implicitInstruments(self):
        """the opposite of explicitInstruments!  all unnecessary instrument data is removed."""
        #TODO - TEST
        channels = self.channelList()
        memory = {}
        for x in channels:
            channel = self.channels[x]
            #memory[x] = None
            memory[x] = 0
            if channel:
                for event in channel.events:
                    if event.getInstrument() == memory[x]:
                        event.setInstrument(EVENT_NULL_INSTRUMENT)
                    elif event.getInstrument() != EVENT_NULL_INSTRUMENT:
                        memory[x] = event.getInstrument()

    def usedInstrumentsNew(self):
        """returns list of what instruments are used in this pattern"""
        instruments = {}
        channels = self.channelList()
        for x in channels:
            channel = self.channels[x]
            if channel:
                for event in channel.events:
                    if event.getInstrument() != EVENT_NULL_INSTRUMENT:
                        instruments[event.getInstrument()] = 1
        return instruments.keys()

    def usedInstruments(self, ignoreTracks=[]):
        """returns list of what instruments are used in this pattern"""
        instruments = []
        channels = self.channelList()
        for x in channels:
            channel = self.channels[x]
            if channel and x not in ignoreTracks:
                for event in channel.events:
                    ei = event.getInstrument()
                    if (ei != EVENT_NULL_INSTRUMENT) and (ei not in instruments):
                        instruments.append(ei)
        return instruments


    def trackUsedInstruments(self, track):
        """returns list of what instruments are used in the specified track of this pattern"""
        instruments = []
        channel = self.channels[x]
        if channel:
            for event in channel.events:
                if event.getInstrument() != EVENT_NULL_INSTRUMENT:
                    if event.getInstrument() not in instruments:
                        instruments.append(event.getInstrument())
        return instruments

    def areNotesEmpty(self):
        """returns true if all events is this pattern are empty of note data (note or instrument values)."""

        channels = self.channelList()
        for x in channels:
            channel = self.channels[x]
            if channel:
                for event in channel.events:
                    if not event.isNoteEmpty():
                        return 0
        return 1

    def areTrackNotesEmpty(self, track):
        """returns true if all events is specified track of this pattern are empty of note data (note or instrument values)."""
        channel = self.channels[track]
        if channel:
            for event in channel.events:
                if not event.isNoteEmpty():
                    return 0
        return 1

    def getLastRow(self):
        # return last playback row - either total number of rows, or row where B or C command occurs.
        # check for C00
        channels = self.channelList()
        for row in xrange(self.numrows):
            for x in channels:
                if self.channels[x]:
                    channel = self.channels[x]
                    if channel:
                        if channel.events[row].getCommand() in (3,2):
                            #print channel.events[row].command, channel.events[row].commandvalue
                            return row

        # if we haven't returned yet, it's just the numrows
        return self.numrows
    

    def pack(self):
        packed = ITPackedPattern()
        #packed.data, packed.rows = itc.pack(self)
        packed.length = len(packed.data)
        return packed

##    def pack(self):
##        # optimized by hardcoding instead of using note, instrument, volpan, command, commandvalue accessor functions
##        # return packed pattern
##        channelVariable = 0
##        maskVariable = 0
##
##        curPos = 0
##
##        #row = ITRowData() # used to keep track of last value in channels
##
##        #row = []
##        #for i in xrange(0, MAX_PATTERN_CHANNELS):
##        #    row.append(ITEventData())
##        row = [ITEventData() for i in xrange(0, self.numchannels)]
##
##        #lastMask = []
##        #for i in xrange(0, self.numchannels):
##        #    lastMask.append(0)
##        lastMask = [0] * self.numchannels
##
##        packed = ITPackedPattern()
##        packed.rows = self.numrows
##
##        data = ""
##
##        # according to ITTECH.DOC, the packed pattern data plus 8 byte header will always
##        # be less than 64k.
##
##        for frame in xrange(0, self.numrows):
##
##            for channel in xrange(0, self.numchannels):
##
##                channelVariable = channel + 1
##                maskVariable = 0
##
##                event = self.channels[channel].events[frame]
##                
##                note = event.getNote()
##                if (note > 0):
##                    
##                    # does note equal last note for this channel?
##                    if (note == row[channel].getNote()):
##                        maskVariable = maskVariable | 16
##                    else:
##                        maskVariable = maskVariable | 1
##                                                                    
##                instrument = event.getInstrument()
##                if (instrument > 0):
##
##                    if (instrument == row[channel].getInstrument()):
##                        maskVariable = maskVariable | 32
##                    else:
##                        maskVariable = maskVariable | 2
##
##                volpan = event.getVolPan()                
##                if (volpan != 255):
##
##                    if (volpan == row[channel].getVolPan()):
##                        maskVariable = maskVariable | 64
##                    else:
##                        maskVariable = maskVariable | 4
##
##                command = event.getCommand()
##                commandvalue = event.getCommandValue()
##                if ((command != 255) or  \
##                    (commandvalue != 255)):
##
##                    if ((command == row[channel].getCommand()) and    \
##                        (commandvalue == row[channel].getCommandValue())):
##                        maskVariable = maskVariable | 128
##                    else:
##                        maskVariable = maskVariable | 8
##
##
##                if (maskVariable != lastMask[channel]):
##                    channelVariable = channelVariable | 128
##
##                # update "last" values for this channel
##                if (maskVariable != 0):
##                    lastMask[channel] = maskVariable
##                if (note != 0):
##                    row[channel].setNote(note)
##                if (instrument != 0):
##                    row[channel].setInstrument(instrument)
##                if (volpan != 255):
##                    row[channel].setVolPan(volpan)
##                if (command != 255):
##                    row[channel].setCommand(command)
##                if (commandvalue != 255):
##                    row[channel].setCommandValue(commandvalue)
##
##                if (maskVariable == 0):
##                    continue  # no info needed.
##                
##                data = data + chr(channelVariable)
##
##                if (channelVariable & 128):
##                    data = data + chr(maskVariable)
##
##                if (maskVariable & 1):
##                    data = data + chr(note)
##
##                if (maskVariable & 2):
##                    data = data + chr(instrument)
##
##                if (maskVariable & 4):
##                    data = data + chr(volpan)
##
##                if (maskVariable & 8):
##                    data = data + chr(command)
##                    data = data + chr(commandvalue)
##
##            # end of row
##
##            data = data + chr(0)
##
##        # end of pattern
##
##        packed.data = data
##        packed.length = len(data)
##        return packed

        

    #TODO: obsolete                
    def packOld(self):
        # unoptimized version of pack
        # return packed pattern 
        channelVariable = 0
        maskVariable = 0

        curPos = 0

        row = ITRowData() # used to keep track of last value in channels

        lastMask = []
        for i in xrange(0, MAX_PATTERN_CHANNELS):
            lastMask.append(0)

        packed = ITPackedPattern()
        packed.rows = self.numrows

        data = ""

        # according to ITTECH.DOC, the packed pattern data plus 8 byte header will always
        # be less than 64k.

        for frame in xrange(0, self.numrows):

            for channel in xrange(0, self.numchannels):

                channelVariable = channel + 1
                maskVariable = 0

                if (self.note(channel, frame) > 0):
                    
                    # does note equal last note for this channel?
                    if (self.note(channel, frame) == row[channel].getNote()):
                        maskVariable = maskVariable | 16
                    else:
                        maskVariable = maskVariable | 1
                                                                    

                if (self.instrument(channel, frame) > 0):

                    if (self.instrument(channel, frame) == row[channel].getInstrument()):
                        maskVariable = maskVariable | 32
                    else:
                        maskVariable = maskVariable | 2
                
                if (self.volpan(channel, frame) != PATTERN_NULL_VALUE):

                    if (self.volpan(channel, frame) == row[channel].getVolPan()):
                        maskVariable = maskVariable | 64
                    else:
                        maskVariable = maskVariable | 4

                if ((self.command(channel, frame) != PATTERN_NULL_VALUE) or  \
                    (self.commandvalue(channel, frame) != PATTERN_NULL_VALUE)):

                    if ((self.command(channel, frame) == row[channel].getCommand()) and    \
                        (self.commandvalue(channel, frame) == row[channel].getCommandValue())):
                        maskVariable = maskVariable | 128
                    else:
                        maskVariable = maskVariable | 8


                if (maskVariable != lastMask[channel]):
                    channelVariable = channelVariable | 128

                # update "last" values for this channel
                if (maskVariable != 0):
                    lastMask[channel] = maskVariable
                if (self.note(channel, frame) != 0):
                    row[channel].setNote(self.note(channel, frame))
                if (self.instrument(channel, frame) != 0):
                    row[channel].setInstrument(self.instrument(channel, frame))
                if (self.volpan(channel, frame) != PATTERN_NULL_VALUE):
                    row[channel].setVolPan(self.volpan(channel, frame))
                if (self.command(channel, frame) != PATTERN_NULL_VALUE):
                    row[channel].setCommand(self.command(channel, frame))
                if (self.commandvalue(channel, frame) != PATTERN_NULL_VALUE):
                    row[channel].setCommandValue(self.commandvalue(channel, frame))

                if (maskVariable == 0):
                    continue  # no info needed.
                
                data = data + chr(channelVariable)
                curPos = curPos + 1

                if (channelVariable & 128):
                    data = data + chr(maskVariable)
                    curPos = curPos + 1

                if (maskVariable & 1):
                    data = data + chr(self.note(channel, frame))
                    curPos = curPos + 1

                if (maskVariable & 2):
                    data = data + chr(self.instrument(channel, frame))
                    curPos = curPos + 1

                if (maskVariable & 4):
                    data = data + chr(self.volpan(channel, frame))
                    curPos = curPos + 1

                if (maskVariable & 8):
                    data = data + chr(self.command(channel, frame))
                    curPos = curPos + 1
                    data = data + chr(self.commandvalue(channel, frame))
                    curPos = curPos + 1

            # end of row

            data = data + chr(0)
            curPos = curPos + 1

        # end of pattern

        packed.data = data
        packed.length = len(data)
        return packed


    



class ITPackedPattern(object):
    def __init__(self):
        self.length = 0     # short, length of packed pattern in bytes, not including 8-byte header (ie, length of self.data)
        self.rows = 0       # short, number of rows
        self.extra = 0      # int

        self.data = ""      # packed data

        self.formats = {}
        self.formats["length"] = "<h"
        self.formats["rows"] = "<h"
        self.formats["extra"] = "<i"
        self.formats["data"] = "<%ds" % self.length

        self.vars = ["length", "rows", "extra"]

        self.beginHeaderPos = 0
        self.endHeaderPos = 0

    def copy(self):
        cop = ITPackedPattern()
        cop.length = self.length
        cop.rows = self.rows
        cop.extra = self.extra
        cop.data = self.data
        cop.formats = copy.copy(self.formats)
        cop.vars = copy.copy(self.vars)
        cop.beginHeaderPos = self.beginHeaderPos
        cop.endHeaderPos = self.endHeaderPos
        return cop
        


    def load(self, fp, pos=-1):
        """loads from an open file."""
        if pos <> -1:
            fp.seek(pos)
        self.beginHeaderPos = fp.tell()
        autoload(fp, self)
        self.data = fp.read(self.length)
        self.endHeaderPos = fp.tell()

    def save(self, fp, pos=-1, header=None, headIndex=0):
        """saves to an open file."""
        if pos <> -1:
            fp.seek(pos)
        curpos = fp.tell()
        self.beginHeaderPos = curpos
        autosave(fp, self)
        fp.write(self.data)
        self.endHeaderPos = fp.tell()

        if not self.data:
            curpos = 0
            self.beginHeaderPos = self.endHeaderPos = 0

        if header != None:
            header.set_pattern_offset(headIndex, curpos)
            header.changedSinceSave = 1

        self.changedSinceSave = 0            

    def isBlank(self):
        # pattern is blank if data is blank or has no non-0 characters
        minuszeroes = string.replace(self.data, "\x00", "")
        return not bool(minuszeroes)

    def clear(self):
        self.data = '\x00'
        #TODO: check to make sure this is the right way to clear a packed pattern.

    def dump(self):
        autodump(self)
        print "data", len(self.data)


    def unpack(self):
        # optimized
        # return unpacked pattern - ITPattern

        length = len(self.data)
        
        channelVariable = 0
        channel = 0
        maskVariable = 0

        note = 0
        curPos = 0
        done = 0

        #currentRow = ITRowData()
        currentRow = []
        #for i in xrange(0, MAX_PATTERN_CHANNELS):
        #    currentRow.append(ITEventData())


        lastMask = []
        for i in xrange(0, MAX_PATTERN_CHANNELS):
            lastMask.append(0)

        frame = 0

        pattern = ITPattern(self.rows)
        # TODO: make sure channels are allocated with enough rows.

        # if data length is 0, return blank pattern
        if length == 0:
            return pattern

        while (False):

            channelVariable = 1

            # unpack a row
            while ((channelVariable > 0) and (curPos <= length)):
                channelVariable = ord(self.data[curPos])
                curPos = curPos + 1

                if (channelVariable == 0):
                    break

                channel = (channelVariable - 1) & 63;

                if (channelVariable & 128):
                    maskVariable = ord(self.data[curPos])
                    curPos = curPos + 1

                    lastMask[channel] = maskVariable
        
                else:
                    maskVariable = lastMask[channel]
                

                if (maskVariable & 1):
                    currentRow[channel].setNote(ord(self.data[curPos]))
                    curPos = curPos + 1

                    #pattern.SetChannelNote(channel, frame, currentRow[channel].note)
                    while (pattern.numchannels <= channel):
                        pattern.AddChannel(None, 1)
                    pattern.channels[channel].SetNote(frame, currentRow[channel].getNote())

                    #print "note set", channel,frame,"to",currentRow.channels[channel].note
                

                if (maskVariable & 2):
                    currentRow[channel].setInstrument(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelInstrument(channel, frame, \
                                    currentRow[channel].getInstrument())
                    #print "ins set", channel,frame,"to",currentRow.channels[channel].instrument
                

                if (maskVariable & 4):
                    currentRow[channel].setVolPan(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelVolPan(channel, frame, \
                                    currentRow[channel].getVolPan())
                    #print "vol set", channel,frame,"to",currentRow.channels[channel].volpan
                

                if (maskVariable & 8):
                    currentRow[channel].setCommand(ord(self.data[curPos]))
                    curPos = curPos + 1
                    currentRow[channel].setCommandValue(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelCommand(channel, frame, \
                                    currentRow[channel].getCommand(), \
                                    currentRow[channel].getCommandValue())
                    #print "cmnd set", channel,frame,"to",currentRow.channels[channel].command,currentRow.channels[channel].commandvalue
                

                if (maskVariable & 16):
                    pattern.SetChannelNote(channel, frame, \
                                    currentRow[channel].getNote())
                    #print "16 note set", channel,frame,"to",currentRow.channels[channel].note
                

                if (maskVariable & 32): 
                    pattern.SetChannelInstrument(channel, frame, \
                                    currentRow[channel].getInstrument())
                    #print "32 ins set", channel,frame,"to",currentRow.channels[channel].instrument
                

                if (maskVariable & 64):
                    pattern.SetChannelVolPan(channel, frame, \
                                    currentRow[channel].getVolPan())
                    #print "64 vol set", channel,frame,"to",currentRow.channels[channel].volpan
                

                if (maskVariable & 128):
                    pattern.SetChannelCommand(channel, frame, \
                                    currentRow[channel].getCommand(), \
                                    currentRow[channel].getCommandValue())
                    #print "128 cmnd set", channel,frame,"to",currentRow.channels[channel].command,currentRow.channels[channel].commandvalue
                
            frame = frame + 1

            if ((frame >= self.rows) or (curPos >= length)):
                done = 1

        return pattern


    #TODO: obsolete
    def unpackOld(self):
        # return unpacked pattern - ITPattern

        length = len(self.data)
        
        channelVariable = 0
        channel = 0
        maskVariable = 0

        note = 0
        curPos = 0
        done = 0

        currentRow = ITRowData()
        lastMask = []
        for i in xrange(0, MAX_PATTERN_CHANNELS):
            lastMask.append(0)

        frame = 0

        pattern = ITPattern(self.rows)
        # TODO: make sure channels are allocated with enough rows.

        # if data length is 0, return blank pattern
        if length == 0:
            return pattern

        while (not done):

            channelVariable = 1

            # unpack a row
            while ((channelVariable > 0) and (curPos <= length)):
                channelVariable = ord(self.data[curPos])
                curPos = curPos + 1

                if (channelVariable == 0):
                    break

                channel = (channelVariable - 1) & 63;

                if (channelVariable & 128):
                    maskVariable = ord(self.data[curPos])
                    curPos = curPos + 1

                    lastMask[channel] = maskVariable
        
                else:
                    maskVariable = lastMask[channel]
                

                if (maskVariable & 1):
                    currentRow.channels[channel].setNote(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelNote(channel, frame, currentRow.channels[channel].getNote())
                    #print "note set", channel,frame,"to",currentRow.channels[channel].note
                

                if (maskVariable & 2):
                    currentRow.channels[channel].setInstrument(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelInstrument(channel, frame, \
                                    currentRow.channels[channel].getInstrument())
                    #print "ins set", channel,frame,"to",currentRow.channels[channel].instrument
                

                if (maskVariable & 4):
                    currentRow.channels[channel].setVolPan(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelVolPan(channel, frame, \
                                    currentRow.channels[channel].getVolPan())
                    #print "vol set", channel,frame,"to",currentRow.channels[channel].volpan
                

                if (maskVariable & 8):
                    currentRow.channels[channel].setCommand(ord(self.data[curPos]))
                    curPos = curPos + 1
                    currentRow.channels[channel].setCommandValue(ord(self.data[curPos]))
                    curPos = curPos + 1

                    pattern.SetChannelCommand(channel, frame, \
                                    currentRow.channels[channel].getCommand(), \
                                    currentRow.channels[channel].getCommandValue())
                    #print "cmnd set", channel,frame,"to",currentRow.channels[channel].command,currentRow.channels[channel].commandvalue
                

                if (maskVariable & 16):
                    pattern.SetChannelNote(channel, frame, \
                                    currentRow.channels[channel].getNote())
                    #print "16 note set", channel,frame,"to",currentRow.channels[channel].note
                

                if (maskVariable & 32): 
                    pattern.SetChannelInstrument(channel, frame, \
                                    currentRow.channels[channel].getInstrument())
                    #print "32 ins set", channel,frame,"to",currentRow.channels[channel].instrument
                

                if (maskVariable & 64):
                    pattern.SetChannelVolPan(channel, frame, \
                                    currentRow.channels[channel].getVolPan())
                    #print "64 vol set", channel,frame,"to",currentRow.channels[channel].volpan
                

                if (maskVariable & 128):
                    pattern.SetChannelCommand(channel, frame, \
                                    currentRow.channels[channel].getCommand(), \
                                    currentRow.channels[channel].getCommandValue())
                    #print "128 cmnd set", channel,frame,"to",currentRow.channels[channel].command,currentRow.channels[channel].commandvalue
                
            frame = frame + 1

            if ((frame >= self.rows) or (curPos >= length)):
                done = 1

        return pattern


#TODO: make sure save methods header, headIndex grow offset lists if necessary


class ITModule(object):
    def __init__(self, fname="", unpack=1, loadSampleData=1):
        self.header = ITHeader()
        self.patterns = []      # unpacked patterns
        self.ppatterns = []     # packed patterns
        self.samples = []
        self.instruments = []
        self.message = ""

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

        self.__patternsInOrdersCache = None

        self.__silentSample = None
        self.__silentInstrument = None

        # for iteration
        self.__track = 0
        self.__pattern = 0
        self.__row = 0

        self.__trackmap = None

        self.modtype = "IT"
        self.ext = ".it"
        self.MAX_TRACKS = MAX_TRACKS


        # for parsed header flags
        self.stereo = 1             # 1
        self.vol0MixOptimize = 0    # 2
        self.usesInstruments = 0    # 4
        self.linearSlides = 1       # 8
        self.oldEffects = 0         # 16
        self.linkGEF = 0            # 32
        self.useMidiPitchCC = 0     # 64
        self.embedMidiConfig = 0    # 128

        if fname != "":
            self.load(fname, unpack, loadSampleData)            

    def parseFlags(self):
        flags = self.header.flags
        self.stereo = flags & 1
        self.vol0MixOptimize = flags & 2
        self.usesInstruments = flags & 4
        self.linearSlides = flags & 8
        self.oldEffects = flags & 16
        self.linkGEF = flags & 32
        self.useMidiPitchCC = flags & 64
        self.embedMidiConfig = flags & 128

    def setFlags(self):
        flags = 0
        if self.stereo:
            flags = flags | 1
        if self.vol0MixOptimize:
            flags = flags | 2
        if self.usesInstruments:
            flags = flags | 4
        if self.linearSlides:
            flags = flags | 8
        if self.oldEffects:
            flags = flags | 16
        if self.linkGEF:
            flags = flags | 32
        if self.useMidiPitchCC:
            flags = flags | 64
        if self.embedMidiConfig:
            flags = flags | 128
        self.header.flags = flags

    def setTrackVolumes(self, volumes):
        # volumes needs to be a list of 64 volume values.
        #print "-- it setting volumes to", volumes
        self.header.channelVolume = volumes

    def setTrackPannings(self, pannings):
        # volumes needs to be a list of 64 volume values.
        #print "-- it setting pannings to", pannings
        self.header.channelPan = pannings

    def __call__(self, p, t, r):
        return self.get(p, t, r)

    def __iter__(self):
        return self

    def next(self):
        #print "next", self.__pattern, self.__track, self.__row
        position = (self.__pattern, self.__track, self.__row)
        #print position
        try:
            event = self.patterns[self.__pattern].channels[self.__track].events[self.__row]
        except:
            event = None
            
        self.__track += 1
        if self.__track >= self.patterns[self.__pattern].numchannels or self.patterns[self.__pattern].channels[self.__track] == None:
            self.__track = 0
            self.__row += 1
            if self.__row >= self.patterns[self.__pattern].numrows:
                self.__row = 0
                self.__pattern += 1
                if self.__pattern >= self.numPatterns():
                    self.__pattern = 0
                    raise StopIteration
        return event, position

    def getPatternOrder(self, pattern):
        # return orderlist index of specified pattern, or None
        try:
            return self.header.orders.index(pattern)
        except ValueError:
            return None

    def getLastRow(self, pattern):
        return self.patterns[pattern].getLastRow()

    def load(self, path, unpack=1, loadSampleData=1, checkValid=1, checkpack=1):
        try:
            assert debug("loading " + path)
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
            assert debug("loading header")

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

            f.seek(0)
                    
            try:            
                self.header.load(f)
                self.parseFlags()
            except:
                print path, "header is corrupt, or is not an IT file."
                self.corruption += 1
                self.corrupt = 1
                traceback.print_exc()
                return 0
            
            if checkValid and not self.header.isValid():
                print path, "header is corrupt, or is not an IT file."
                self.corruption = self.corrupt + 1
                self.corrupt = 1
                return 0

            assert debug("loading samples")
            
            self.samples = []
            for i in self.header.sampleOffsets:
                self.samples.append(ITSample())
                if i:
                    #print "loading sample from", i
                    if not self.samples[len(self.samples)-1].load(f, i, loadSampleData):
                        assert debug("sample %s corrupt" % len(self.samples))
                        self.corruption = self.corruption + 1
                        self.corruptSamples = self.corruptSamples + 1

            self.instruments = []
            for i in self.header.instrumentOffsets:
                self.instruments.append(ITInstrument())
                if i:
                    if not self.instruments[len(self.instruments)-1].load(f, i):
                        self.corruption = self.corruption + 1
                        self.corruptInstruments = self.corruptInstruments + 1

            if self.corruptSamples and self.corruptSamples >= len(self.samples):
                self.corrupt = 1

            if self.corrupt:
                print "failed loading, module is corrupt"
                return 0
                
            self.ppatterns = []
            for ppos in self.header.patternOffsets:
                self.ppatterns.append(ITPackedPattern())
                # if offset is 0, the pattern is blank
                if ppos > 0:
                    self.ppatterns[-1].load(f, ppos)

            # set endfilepos
            f.seek(0, 2)
            self.header.endFilePos = f.tell()

            # load song message
            if self.header.messageOffset and self.header.messageLength:
                f.seek(self.header.messageOffset)
                format = "<" + str(self.header.messageLength) + "s"
                temp = f.read(struct.calcsize(format))
                temp = struct.unpack(format, temp)
                if len(temp) == 1:
                    temp = temp[0]
                self.message = temp
                #print "song message", self.message
                #print "smc", ord(self.message[-1])

            # load header extra data, if any
            chunk = self.headerExtraChunk()
            if chunk[1]-chunk[0] > 0:
                self.header.loadExtra(f, chunk[0], chunk[1])
                
            f.close()

            self.packed = 1
            self.unpacked = 0
            if unpack:
                try:
                    self.unpack(checkpack)
                except:
                    print "-- Failed unpacking"
                    traceback.print_exc()

            #if unpack:
            #    for p in self.patterns:
            #        print p.getLastRow()

            """
            print "sample offsets", self.header.sampleOffsets
            do = [x.sampleOffset for x in self.samples]
            bl = [x.lengthInBytes for x in self.samples]
            print "data offsets", do
            print "bytelengths", bl
            for i in xrange(1, len(do)):
                print "diff", do[i]-do[i-1]
            """
            
            self.path = path
            return 1


        except:
            print "-- Failed loading", path
            self.corrupt = 1
            self.corruption = 100
            traceback.print_exc()
            return 0

    def save(self, path, pack=1, checkpack=1):
        if pack:
            self.pack(checkpack)

        self.header.resize(len(self.samples), len(self.instruments), len(self.ppatterns))
        self.header.prepareForSave()

        # calc stuff for song message
        if self.message:
            if self.message[-1] != chr(0):
                self.message = self.message + chr(0)
        self.messageLength = len(self.message)
            
        f = open(path, "wb")
        self.setFlags()
        self.header.save(f)
        #x = raw_input()
        f.seek(0, 2)    # seek to end
        idx = 0
        for i in self.instruments:
            i.save(f, header=self.header, headIndex=idx)
            #print "i",idx
            idx = idx + 1
        idx = 0
        for s in self.samples:
            s.saveheader(f, pos=-1, header=self.header, headIndex=idx)
            idx = idx + 1
            #print "s",idx
            #f.flush()
            #x = raw_input()
        idx = 0
        for p in self.ppatterns:
            p.save(f, header=self.header, headIndex=idx)
            #print "p",idx
            idx = idx + 1
        idx = 0
        for s in self.samples:
            s.savedata(f, pos=-1, header=self.header, headIndex=idx)
            idx = idx + 1
            #print "sd",idx

        # save song message
        # MOVED TO HEADER
        #if self.message:
        #    pos = f.tell()
        #    format = "<" + str(len(self.message)) + "s"
        #    temp = struct.pack(format, self.message)
        #    f.write(temp)
        #    self.header.messageOffset = pos

        # resave header
        self.header.save(f, 0)
        f.close()

        self.path = path        

    def numOrders(self):
        return self.header.numOrders

    def get(self, pattern, track, row):
        """return event at specified position"""
        try:
            return self.patterns[pattern].channels[track].events[row]
        except:
            return None

    def set(self, pattern, track, row, event):
        print "Not Implemented yet"

    def deletePatterns(self, indexes):
        newpatterns = []
        i = 0
        if self.packed:
            for p in self.ppatterns:
                if i not in indexes:
                    newpatterns.append(p)
                i += 1
                self.ppatterns = newpatterns
        else:
            for p in self.patterns:
                if i not in indexes:
                    newpatterns.append(p)
                i += 1
                self.patterns = newpatterns
        #TODO: update orderlist
                
    def deletePatternsData(self, indexes):
        for i in indexes:
            if self.unpacked:
                if i < len(self.patterns):
                    self.patterns[i].clear()
            else:
                if i < len(self.ppatterns):
                    self.ppatterns[i].clear()

    def patternsInOrders(self, usecache=1):
        # return list of packed patterns that appear in order list.
        # if order list empty, returns all
        # this returns the actual patterns, not indexes.
        # optional cache of results.
        
        if self.isOrderListEmpty():
            return self.ppatterns
        else:
            if usecache and self.__patternsInOrdersCache:
                return self.__patternsInOrdersCache
            else:
                plist = []
                for o in self.header.orders:
                    if o != 255:
                        if o < len(self.ppatterns):
                            plist.append(self.ppatterns[o])
                        else:
                            plist.append(ITPackedPattern())
                self.__patternsInOrdersCache = plist
                return plist                    
        

    def unfold(self, pack=1):
        # do unfolding

        if self.unpacked:
            wasunpacked = 1
        else:
            wasunpacked = 0

        # pack patterns
        if self.unpacked and pack:
            self.pack()
            #debug("packed patterns for unfold")

        # if no order list exists currently, make order list from existing patterns.
        if self.isOrderListEmpty():
            self.header.orders = range(0, len(self.ppatterns))
            self.header.orders.append(255)
            return
            #debug("made new orderlist with" + str(len(self.ppatterns)) + "entries.")
                    
        newpatterns = []
        usedPatterns = []
        idx = 0
        for o in self.header.orders:
            #debug("processing order" + str(idx))
            #if o < len(self.ppatterns) and o != 255:
            if o < len(self.ppatterns) and o <= 255:
                #debug("copying pattern" + str(o))
                #p = copy.deepcopy(self.ppatterns[o])
                p = self.ppatterns[o].copy()
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
            if i < 255:
                self.header.orders.append(i)
        #debug("new orders: " + str(self.header.orders))

        self.header.orders.append(255)

        # now add unused patterns onto end
        for pp in xrange(0, len(self.ppatterns)):
            if pp not in usedPatterns:
                newpatterns.append(self.ppatterns[pp])

        self.ppatterns = newpatterns
        self.header.resize(len(self.samples), len(self.instruments), len(self.ppatterns))

        if wasunpacked:
            self.unpack()


    def unpack(self, check=1):
        """ unpack patterns.  threadsafe, checks self.unpacking, a second call will wait til it completes.
        so you can start unpacking in a thread, and future calls will wait for it to complete if it hasn't yet."""

        if self.unpacking:
            while self.unpacking:
                time.sleep(0.2)
                #print "-- unpack waiting"
            # should be all done now
            return
                        
        if check and self.unpacked:
            return

        self.unpacking = 1

        self.patterns = []
        idx = 0
        for p in self.ppatterns:
            self.patterns.append(p.unpack())
            idx += 1
        self.unpacked = 1
        self.packed = 0

        self.unpacking = 0        


    def pack(self, check=1):
        """ pack patterns """
        if check and self.packed:
            return

        self.ppatterns = []
        for p in self.patterns:
            #print p, p.pack
            self.ppatterns.append(p.pack())
        self.packed = 1
        self.unpacked = 0

    def growIfNeeded(self, pattern, track=0, row=DEFAULT_NUM_ROWS):
        while len(self.patterns) < pattern+1:
            self.patterns.append(ITPattern())

    def setOrderList(self, newlist):
        # should be ints, or 'END'. 'END' will be ignored.
        newlist = [i for i in newlist if i != 'END']
        # ensure 255 end
        if (not newlist) or (newlist[-1] != 255):
            newlist.append(255)
            
        self.header.orders = newlist
        self.header.resize(len(self.samples), len(self.instruments), len(self.patterns))


    def appendOrderList(self, appendlist):
        appendlist = utilx.tolist(appendlist)
        if not appendlist:
            return
        while self.header.orders[-1] == 255:
            self.header.orders = self.header.orders[:-1]
        while appendlist[-1] == 255:
            appendlist = appendlist[:-1]
        self.header.orders += appendlist
        self.header.orders += [255]
        return self.header.orders

    def repeatOrderList(self, count):
        ol = copy.deepcopy(self.header.orders)
        for i in range(count-1):
            self.appendOrderList(ol)



    def getNumRealOrders(self):
        ords = copy.deepcopy(self.header.orders)
        while ords[-1] == 255:
            ords = ords[:-1]
        return len(ords)
            
    def isOrderListEmpty(self):
        numreal = 0
        for x in self.header.orders:
            if x != 255:
                numreal += 1
        if numreal == 0:
            return 1
        else:
            return 0
            
            

    def clearNote(self, pattern, track, row):
        if not self.unpacked:
            self.unpack()
        self.growIfNeeded(pattern, track, row)
        self.patterns[pattern].clearNote(track, row)
        

    def setNote(self, pattern, track, row, value):
        if not self.unpacked:
            self.unpack()
        self.growIfNeeded(pattern, track, row)
        self.patterns[pattern].setNote(track, row, value)

    def setInstrument(self, pattern, track, row, value):
        if not self.unpacked:
            self.unpack()
        self.growIfNeeded(pattern, track, row)
        self.patterns[pattern].setInstrument(track, row, value)

    def setSample(self, pattern, track, row, value):
        self.patterns[pattern].setInstrument(track, row, value)

    def setCommand(self, pattern, track, row, command, value):
        self.growIfNeeded(pattern, track, row)
        self.patterns[pattern].setCommand(track, row, command, value)

    def disableTrack(self, track):
        if self.header.channelPan[track] < 128:
            self.header.channelPan[track] += 128

    def enableTrack(self, track):
        if self.header.channelPan[track] >= 128:
            self.header.channelPan[track] -= 128

    def toggleTrack(self, track):
        if self.header.channelPan[track] < 128:
            self.header.channelPan[track] += 128
            print "disabled"
        else:
            self.header.channelPan[track] -= 128
            print "enabled"

    def toggleTracks(self, tracks):
        for track in tracks:
            if self.header.channelPan[track] < 128:
                self.header.channelPan[track] += 128
                print "disabled", track
            else:
                self.header.channelPan[track] -= 128
                print "enabled", track

    def getDisabledTracks(self):
        return [i for i in range(len(self.header.channelPan)) if self.header.channelPan[i]>=128]

    def enableAllTracks(self):
        panlist = self.header.channelPan
        for i in range(len(panlist)):
            if panlist[i] >= 128:
                panlist[i] -= 128
            

    def getTrackSettings(self, track):
        # return volume, pan, enabled, surround
        vol, pan = self.header.channelVolume[track], self.header.channelPan[track]
        if pan > 128:
            enabled = 0
            pan -= 128
        else:
            enabled = 1
        if pan == 100:
            pan = 32
            surround = 1
        else:
            surround = 0
        return vol, pan, enabled, surround
        

    def setTrackVolume(self, track, volume):
        self.header.channelVolume[track] = volume

    setDefaultTrackVolume = setTrackVolume

    def setTrackPan(self, track, pan):
        self.header.channelPan[track] = pan

    setDefaultTrackPan = setTrackPan
        
    
    def getTempo(self):
        return self.header.initialTempo

    def getSpeed(self):
        return self.header.initialSpeed

    def getGlobalVolume(self):
        return self.header.globalVolume

    def getMixingVolume(self):
        return self.header.mixVolume

    def getName(self):
        return self.header.songName

    def setSpeed(self, speed):
        self.header.initialSpeed = speed
        #TODO: range checking

    def setTempo(self, tempo):
        self.header.initialTempo = tempo
        #TODO: range checking

    def setGlobalVolume(self, volume):
        self.header.globalVolume = volume
        #TODO: range checking

    def setMixingVolume(self, volume):
        self.header.mixVolume = volume
        #TODO: range checking

    def setName(self, name):
        self.header.songName = name
        #TODO: it format string?

    def clearPatterns(self):
        self.ppatterns = []
        self.patterns = []
        self.header.orders = []
        self.header.numPatterns = 0
        self.header.numOrders = 0 

    def numInstruments(self):
        if self.header.numIns:
            return self.header.numIns
        else:
            return self.header.numSamples
        #return max((self.header.numIns, self.header.numSamples))

    def numChannels(self):
        maxchannels = 0
        self.unpack()
        for p in self.patterns:
            if p.numchannels > maxchannels:
                maxchannels = p.numchannels
        return maxchannels

    numTracks = numChannels

    def numSamples(self):
        return len(self.samples)

    def patternList(self):
        return range(0, len(self.patterns))

    def numPatterns(self):
        return (max((len(self.ppatterns), len(self.patterns))))

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

        #names = ["Track "] * trks
        #for i in xrange(0, trks):
        #    names[i] += str(i+1)

        names = [self.getTrackName(i) for i in xrange(0, trks)]
        
        return names

    def patternNames(self):
        patterns = self.numPatterns()
        names = [self.getPatternName(i) for i in xrange(0, patterns)]
        #names = ["Pattern "] * patterns
        #for i in xrange(0, patterns):
        #    names[i] += str(i)
        return names

    def getBlankPatterns(self):
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


    def translateTrack(self, track):
        # translate track ignoring blank tracks, similar to BASS
        # returns -1 if track is blank.
        
        if not self.__trackmap:
            self.__trackmap = {}
            blanks = self.getBlankTracks()
            tracks = range(self.numTracks())
            i = 0
            for t in tracks:
                if t not in blanks:
                    self.__trackmap[t] = i
                    i += 1
        return self.__trackmap.get(track, -1)


    def getBlankTracks(self):
        if not self.patterns:
            return []
        nt = self.numTracks()
        blanks = sets.Set(self.patterns[0].getBlankTracks(nt))
        if len(self.patterns) > 1:
            for p in self.patterns:
                blanks = blanks.intersection(sets.Set(p.getBlankTracks(nt)))
        return list(blanks)
        

    def orderList(self):
        return self.header.orders

    getOrderList = orderList

    def setTrackFromSeq(self, pattern, track, seq):
        self.growIfNeeded(pattern, track)
        self.patterns[pattern].setChannelFromSeq(track, seq)

    def setPatternFromSeq(self, pattern, seq):
        self.growIfNeeded(pattern)
        self.patterns[pattern].setFromSeq(seq)

    def noteAdd(self, pattern, value):
        self.growIfNeeded(pattern)
        self.patterns[pattern].noteAdd(value)

    def AllowUnlimitedSamples(self):
        self.unlimitedSamples = 1

    def DisallowUnlimitedSamples(self):
        self.unlimitedSamples = 0

    def setTrackSamples(self, pattern, samples):
        """given a pattern and list of sample numbers, sets tracks to those sample numbers.
        this method is intended to be used on new sequences only, that do not already have assigned
        sample/instrument events.  this method only sets the sample numbers on the first row of
        the specified pattern.
        from the given sample list, they are placed starting on track 0 and ascending until the end of the
        list."""
        track = 0
        for s in samples:
            self.setInstrument(pattern, track, 0, s)
            track = track + 1

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
        exported = []
        for s in self.samples:
            if s.filename != "":
                ret = s.savefile(filex.pathjoin(path, s.filename))
                if ret != 0:
                    exported.append(filex.pathjoin(path, s.filename))
            else:
                ret = s.savefile(filex.pathjoin(path, os.path.basename(self.path) + str(i)))
                if ret != 0:
                    exported.append(filex.pathjoin(path, os.path.basename(self.path) + str(i)))
            i = i + 1
        return exported

    def makeSolo(self, track, useVolumes=0):
        # solos a track
        if useVolumes:
            for t in range(64):
                if t != track:
                    self.disableTrack(t)
                    #self.setTrackVolume(t)
                else:
                    self.enableTrack(t)
        else:
            self.unpack()
            for p in self.patterns:
                p.makeSolo(track)

    def createSilentSample(self, s=None):
        if not s:
            s = ITSample()
        s.setData(SILENCEDATA)
        s.setLoopPoints()
        s.setLoopNormal()
        s.setFileName("__MFSILENCE")
        return s
        

    def getSilentSample(self, force=1):
        # returns index of a silent sample, creating a new one if none exists.
        # a silent sample is not the same thing as a blank sample entry; it has actual
        # sample data of silence.
        #
        # if force is true, the last current sample will be overwritten if all samples
        # are already taken.
        
        if not self.__silentSample:
            s = self.addNewSample(force=force)
            self.createSilentSample(s)
            self.__silentSample = len(self.samples)-1

        return self.__silentSample

    def getSilentInstrument(self, force=1):
        if not self.__silentInstrument:
            if self.usesInstruments:
                ss = self.getSilentSample()
                i = self.addNewInstrument(force=force)
                i.setAllSamples(ss+1)   # index is 0-based, sample nums are 1-based
                i.setFileName("__MFSILENCE")
                self.__silentInstrument = len(self.instruments)-1
            else:
                self.__silentInstrument = self.getSilentSample()

        return self.__silentInstrument        

        
    def soloInstrumentsBySilentSample(self, instruments):
        instruments = utilx.tolist(instruments)

        if self.usesInstruments:
            sindex = self.getSilentInstrument(force=1)
            # change all instruments that should be silent to use the silent sample
            n = 0
            for i in self.instruments:
                if (n+1) not in instruments:
                    print "-- setallsamples for", n+1, "to", sindex+1
                    i.setAllSamples(sindex+1)
                n += 1
        else:
            sindex = self.getSilentSample(force=1)
            ssamp = self.samples[sindex]

            n = 0
            for s in self.samples:
                if (n+1) not in instruments:
                    print "creating silent sample in pos", n, n+1
                    self.samples[n] = self.createSilentSample()
                n += 1

    def soloInstrumentsByVolume(self, instruments):
        instruments = utilx.tolist(instruments)
        if self.usesInstruments:
            for i in range(len(self.instruments)):
                if (i+1) not in instruments:
                    self.instruments[i].setGlobalVolume(0)
        else:
            for i in range(len(self.samples)):
                if (i+1) not in instruments:
                    self.samples[i].setGlobalVolume(0)

    def getInstrumentGlobalVolume(self, instrument):
        if self.usesInstruments:
            return self.instruments[instrument].getGlobalVolume()
        else:
            return self.samples[instrument].getGlobalVolume()

    def setInstrumentGlobalVolume(self, instrument, volume):
        if self.usesInstruments:
            self.instruments[instrument].setGlobalVolume(volume)
        else:
            self.samples[instrument].setGlobalVolume(volume)


            

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

    def uncompress(self):
        for sample in self.samples:
            sample.uncompress(self.path)
        self.header.formatVersion = 514

    # Analysis methods

    def allOffsets(self, includeEnd=1):
        # returns list of all offsets in the module.  this is a list of positions where "chunks" of various types begin.
        # if includeEnds, the end position of the file is included.
        all = self.header.instrumentOffsets + self.header.sampleOffsets + self.header.patternOffsets + [self.header.messageOffset]
        # add sample data offsets
        for s in self.samples:
            all.append(s.sampleOffset)

        if includeEnd:
            all.append(self.header.endFilePos)

        #all.sort()
        return all

    def allOffsetsTyped(self, includeEnd=1):
        # returns list of all offsets in the module.  this is a list of positions where "chunks" of various types begin.
        # if includeEnds, the end position of the file is included.
        all = map(lambda x: "I-" + str(x), self.header.instrumentOffsets)
        all = all + map(lambda x: "S-" + str(x), self.header.sampleOffsets)
        all = all + map(lambda x: "P-" + str(x), self.header.patternOffsets)
        all.append("M-" + str(self.header.messageOffset))

        # add sample data offsets
        for s in self.samples:
            all.append("D-" + str(s.sampleOffset))

        if includeEnd:
            all.append("E-" + str(self.header.endFilePos))

        #all.sort()
        return all

    def allChunks(self):
        chunks = []
        chunks.append((self.header.beginHeaderPos, self.header.endHeaderPos, "H"))
        for s in self.samples:
            chunks.append((s.beginHeaderPos, s.endHeaderPos, "S"))
            chunks.append((s.beginDataPos, s.endDataPos, "D"))
        for i in self.instruments:
            chunks.append((i.beginHeaderPos, i.endHeaderPos, "I"))
        for p in self.ppatterns:
            chunks.append((p.beginHeaderPos, p.endHeaderPos, "P"))
        chunks.append((self.header.messageOffset, self.header.messageOffset+self.header.messageLength, "M"))

        # remove empty chunks
        final = []
        for chunk in chunks:
            if chunk[1] - chunk[0] != 0:
                final.append(chunk)
        
        return final

    def headerExtraChunk(self):
        start = self.header.endHeaderPos
        chunks = self.allChunks()
        chunks.sort()
        # since the header comes first, the second chunk SHOULD be the first chunk in the file after the header,
        # and the header extra should end at the beginning position of that second chunk.
        try:
            end = chunks[1][0]
        except IndexError:
            end = start
        #if not end:
        #    print "end", start, end
        #    print chunks
        return (start, end)

    def areNotesEmpty(self):
        """returns true if all note data in all patterns are empty"""
        if not self.unpacked:
            self.unpack()
        for p in self.patterns:
            if not p.areNotesEmpty():
                return 0
        return 1

    def areTrackNotesEmpty(self, track):
        """returns true if all note data in specified track in all patterns are empty"""
        if not self.unpacked:
            self.unpack()
        for p in self.patterns:
            if not p.areTrackNotesEmpty(track):
                return 0
        return 1

    def usedInstruments(self):
        """return list of all instruments used in all patterns"""
        ignore = self.getDisabledTracks()
        instruments = []
        self.unpack()
        for p in self.patterns:
            instruments = instruments + p.usedInstruments(ignoreTracks=ignore)
        instruments = utilx.unique_seq(instruments)
        instruments.sort()
        return instruments

    def trackUsedInstruments(self, track):
        """return list of all instruments used in specified track, all patterns"""
        instruments = []
        self.unpack()
        for p in self.patterns:
            instruments = instruments + p.trackUsedInstruments(track)
        instruments = utilx.unique_seq(instruments)
        instruments.sort()
        return instruments

    def getMaxSamples(self):
        # differs depending on whether we're set to allow 100+ samples
        if self.unlimitedSamples:
            return MAX_SAMPLES_UNLIMITED
        else:
            return MAX_SAMPLES

    def getMaxInstruments(self):
        if self.unlimitedSamples:
            return MAX_INSTRUMENTS_UNLIMITED
        else:
            return MAX_INSTRUMENTS

    def addNewSample(self, overwrite=0, force=0):
        # if overwrite is true, sample will be placed in first available blank spot.
        # OVERWRITE NOT IMPLEMENTED YET.
        
        # if force is true, overwrite last sample if we already have max samples
        # returns None if the sample couldn't be added.
        if len(self.samples) < self.getMaxSamples():
            self.samples.append(ITSample())
        elif force:
            self.samples[self.getMaxSamples()] = ITSample()
        else:
            return None

        return self.samples[-1]


    def addNewInstrument(self, overwrite=0, force=0):
        # if overwrite is true, instrument will be placed in first available blank spot.
        # OVERWRITE NOT IMPLEMENTED YET.
        
        # if force is true, overwrite last instrument if we already have max instruments
        # returns None if the instrument couldn't be added.
        if len(self.instruments) < self.getMaxInstruments():
            self.instruments.append(ITInstrument())
        elif force:
            self.instruments[self.getMaxInstruments()] = ITInstrument()
        else:
            return None

        return self.instruments[-1]




    def usedSamples(self):
        """return list of all samples used by all instruments used"""
        # if this module doesn't use instruments, usedSamples will be identical to usedInstruments
        if not self.usesInstruments:
            return self.usedInstruments()
        else:        
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

    def patternUsedSamples(self, patternidx):
        """return list of all samples used by all instruments used in specified pattern"""
        # if this module doesn't use instruments, usedSamples will be identical to usedInstruments
        if not self.usesInstruments:
            return self.patterns[patternidx].usedInstruments()
        else:
            samples = []
            instruments = self.patterns[patternidx].usedInstruments()
            for i in instruments:
                samples = samples + self.instruments[i-1].usedSamples()
            samples = utilx.unique_seq(samples)
            samples.sort()
            return samples
            
            

class ITEditor(ITModule):
    def __init__(self, fname="", unpack=1, loadSampleData=1):
        ITModule.__init__(self, fname, unpack, loadSampleData=loadSampleData)
        self.pattern = 0
        self.track = 0
        self.row = 0

    def __getitem__(self, key):
        # key = (pattern, track, row)
        pattern, track, row = key
        try:
            return self.get(pattern, track, row)
        except:
            raise IndexError

    def setcursor(self, pattern=-1, track=-1, row=-1):
        if pattern != -1:
            self.pattern = pattern
        if track != -1:
            self.track = track
        if row != -1:
            self.row = row

    def afteredit(self):
        self.row = self.row + 1
        pass

    def cursorDown(self):
        self.row = self.row + 1

    def note(self, n):
        """sets note at current cursor position and moves cursor."""
        self.setNote(self.pattern, self.track, self.row, n)
        self.afteredit()

    def instrument(self, x):
        """sets instrument at current cursor position and moves cursor."""
        self.setInstrument(self.pattern, self.track, self.row, x)
        self.afteredit()

    def sample(self, x):
        """same as instrument"""
        self.instrument(x)

    def command(self, x, y):
        """sets command and command value at current cursor position and move cursor."""
        self.setCommand(self.pattern, self.track, self.row, x, y)
        self.afteredit()

    def endPattern(self):
        self.command(ITCMD_C, 0)

    def setCurNote(self, x):
        """set note value at current cursor position."""
        self.setNote(self.pattern, self.track, self.row, x)

    def setCurInstrument(self, x):
        """set instrument value at current cursor position."""
        self.setInstrument(self.pattern, self.track, self.row, x)

    def setCurSample(self, x):
        """same as setCurInstrument"""
        self.setInstrument(self.pattern, self.track, self.row, x)

    def setCurCommand(self, x, y):
        """set command and command value at current cursor position."""
        self.setCommand(self.pattern, self.track, self.row, x, y)        

    def loadSample(self, path=None, data=None, sample=None, name=None, params=None, pos=None, forceMono=1):
        """load new sample into module, returns sample number (new length of list)"""

        if pos:
            while len(self.samples)-1 < pos:
                self.samples.append(ITSample())
                    
        if (self.unlimitedSamples or len(self.samples) < 99):
            if path:
                if pos:
                    self.samples[pos] = ITSample(path, forceMono=forceMono)
                else:
                    self.samples.append(ITSample(path, forceMono=forceMono))
                #print "appended", path, "to sample position", len(self.samples)-1
            elif (data != None):
                if pos:
                    self.samples[pos] = ITSample(data=data, params=params, forceMono=forceMono)
                else:
                    self.samples.append(ITSample(data=data, params=params, forceMono=forceMono))
            elif (sample != None):
                if pos:
                    self.samples[pos] = sample
                else:
                    self.samples.append(sample)
                
            if name:
                self.samples[-1].setName(name)
        else:
            # can't load
            return -1

        return len(self.samples)-1

    def loadSampleList(self, samplist, overwrite=0):
        """load list of sample filenames into module, appending or overwriting.
        returns num successfully loaded, and list of samples that fail to load."""
        failed = []
        numLoaded = 0
        pos = None
        if overwrite:
            pos = 0
            
        for x in samplist:
            try:
                self.loadSample(x, pos=pos)
                numLoaded = numLoaded + 1
                if overwrite:
                    pos = pos + 1
                    # ensure we are skipping to the next real sample for overwrite
                    while (len(self.samples)-1 >= pos) and self.samples[pos].isEmpty():
                        #xx = raw_input()
                        pos = pos + 1
            except:
                traceback.print_exc()
                failed.append(x)
        return numLoaded, failed

    def loadSampleDir(self, path, mask="*.wav"):
        """load directory full of samples into module.
        returns number of samples loaded."""
        samplist = filex.getdir(path, mask)
        for s in samplist:
            self.loadSample(filex.pathjoin(path, s))
        return len(samplist)

    def makePlayableCopy(self, *args, **kwargs):
        return makePlayableCopy(*args, **kwargs)

    def getPlugins(self):
        return self.header.plugins

    def getTrackName(self, track, number=0, nameBlanks=1):
        if number:
            numst = str(track+1) + ". "
        else:
            numst = ""
        name = ""
        if track+1 in self.header.trackNames:
            name = self.header.trackNames[track+1]
        name = utilx.stripnulls(name)
        if not name and nameBlanks:
            name = "Track " + str(track+1)
        name = numst + name
    
        return name

    def getPatternName(self, pattern, number=0, nameBlanks=1):
        if number:
            numst = str(pattern) + ". "
        else:
            numst = ""
        name = ""
        if pattern in self.header.patternNames:
            name = self.header.patternNames[pattern]
        name = utilx.stripnulls(name)
        if not name and nameBlanks:
            name = "Pattern " + str(pattern)
        name = numst + name
    
        return name


                    


def transoctPattern(module, pattern, multiplier=1):
    module.noteAdd(pattern, 12*multiplier)

def transposePattern(module, pattern, value):
    module.noteAdd(pattern, value)

def doublewidePattern(module, pattern):
    """returns range of new tracks"""
    pass

def thickenPattern(module, pattern, multiplier=-1):
    module.noteAdd(pattern, 12*multiplier)

def samplify(module, smpdir):
    """replace all samples in module with random samples from a directory"""
    newsamps = filex.randombatchfromdir(smpdir, module.header.numSamples, mask="*.wav", allowduplicates=1)
    for i in xrange(0, module.header.numSamples):
        #print "replacing sample", i, "with", newsamps[i]
        module.samples[i].loadfile(newsamps[i])
    

Cmaj = [c,e,g]
Fmaj = [f,a,c]
Gmaj = [g,b,d]
Amaj = [a,c,e]

def randomit(path):
    it = filex.randombatchfromdir("c:\\it", 1, mask="*.it")[0]
    m = ITEditor(it)
    return it, m

def randomITTemplate(path):
    """gets random it file, loads it, clears the patterns, and returns it and its filename"""
    it = filex.randombatchfromdir("c:\\it", 1, mask="*.it")[0]
    m = ITEditor(it)
    m.clearPatterns()
    return it, m


def makePlayableCopy(fname, newname, copyAlways=1, mod=None, settingsFunc=None, checkValid=0):
    """makes a playable copy from fname and saves to newname.
    this makes a linear sequence if there is no sequence.  if no changes are necessary,
    newname will simply be a copy of fname.
    if copyAlways is false, a copy will only be created if changes are made. default is true.
    returns filename of new copy (or returns fname if copyAlways is false and no changes made), and numorders
    settingsFunc optionally gets different track volume and pan settings to use in the copy.
    """

    if not mod:    
        mod = ITModule(fname=fname, unpack=0)
    corrupt = mod.corrupt

    empty = mod.isOrderListEmpty()
    if empty or settingsFunc or checkValid:
        #print "unfolding", fname, "to", newname

        pack=0
        if settingsFunc:
            #print ".. settingsFunc", settingsFunc
            tv, tp = settingsFunc()
            print tv
            print tp
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



def outfname(path, fname, prefix=""):
    outname = filex.pathjoin(path, prefix+os.path.basename(fname))
    while os.path.exists(outname):
        root, ext = os.path.splitext(outname)
        outname = root + str(random.randrange(0,9)) + ext
    return outname

def notefilterwithresidue(module, notelist):
    """ removes notes not in filter, but leaves behind instrument changes, which translate into new note ons"""
    notelist = notelist + [0]
    print "patlist", module.patternList()
    for p in module.patternList():
        print "channellist", module.patterns[p].channelList()
        print "pattern", p
        for t in module.patterns[p].channelList():
            if module.patterns[p].channels[t] != None:
                print "   track", t
                for r in module.patterns[p].channels[t].rowList():
                    #print "      row", r
                    event = module.get(p, t, r)
                    basenote = event.getNote() % 12
                    if not (basenote in notelist):
                        module.setNote(p, t, r, 0)

def notefilter(module, notelist):
    notelist = notelist + [0]
    print "patlist", module.patternList()
    for p in module.patternList():
        print "channellist", module.patterns[p].channelList()
        print "pattern", p
        for t in module.patterns[p].channelList():
            if module.patterns[p].channels[t] != None:
                print "   track", t
                for r in module.patterns[p].channels[t].rowList():
                    #print "      row", r
                    event = module.get(p, t, r)
                    basenote = event.getNote() % 12
                    if not (basenote in notelist):
                        module.setNote(p, t, r, 0)
                        module.setInstrument(p, t, r, 0)

def nearestNote(sourcenote, basenotelist):
    """returns note closest to a note present in basenotelist.
    the returned note will retain the octave that sourcenote has.
    this will not work correctly if basenotelist has notes that are not octave 0.
    to match strict octave values, use nearestValue()."""
    #TODO: note distances go up too!  b is only 1 step from c.
    distances = []
    for x in basenotelist:
        distances.append(abs((sourcenote % 12) - x))
    #print "d",distances
    index = distances.index(min(distances))
    #print "i",index
    octave = sourcenote / 12
    newnote = (octave+1) * basenotelist[index]
    return newnote
    

def coercenotes(module, notelist):
    notelist = notelist + [0]
    print "patlist", module.patternList()
    for p in module.patternList():
        print "channellist", module.patterns[p].channelList()
        print "pattern", p
        for t in module.patterns[p].channelList():
            if module.patterns[p].channels[t] != None:
                print "   track", t
                for r in module.patterns[p].channels[t].rowList():
                    #print "      row", r
                    event = module.get(p, t, r)
                    basenote = event.getNote() % 12
                    if not (basenote in notelist):
                        newnote = nearestNote(event.getNote(), notelist)
                        print "coercing",event.getNote(),basenote,"to",newnote
                        module.setNote(p, t, r, newnote)
                    
                    
            
        

def testfilter():
    fname, m = randomit("c:\\it")
    notefilter(m, Cmaj)
    m.unfold()
    m.save(outfname("c:\\it\\twink", fname, "flt-"))

def testfilter2():
    import winamp
    fname, m = randomit("c:\\it")
    coercenotes(m, keyF)
    m.unfold()
    m.save(outfname("c:\\it\\twink", fname, "kf-"))
    winamp.play(m.path)

def testnear():
    n = [c,e,f,g,a]
    print n
    print "c =",nearestNote(c,n)
    print "cs =",nearestNote(cs,n)
    print "d =",nearestNote(d,n)
    print "f =",nearestNote(f,n)
    print "fs =",nearestNote(fs,n)
    print "as =",nearestNote(as,n)
    print "b =",nearestNote(b,n)

#testfilter2()
#testnear()

def openit(fname, unpack=1):
    return ITModule(fname=fname, unpack=unpack)

def testchunks():
    #x = ITModule(fname="c:\\it\\chris31b.it", unpack=0)
    x = ITModule(fname="c:\\it\\orco.it", unpack=0)
    #for o in x.allOffsetsTyped():
    #    print o
    poo = x.allChunks()
    poo.sort()
    memory = None
    for c in poo:
        print c
        if memory and memory[1] and memory[1] != c[0]:
            print "gap", memory[1], c[0]+1
        memory = c


def fxstats(fname=None, mod=None):
    if mod:
        x = mod
        fname = mod.path
    else:
        x = ITModule(fname)
    num = 0
    fx = {}
    for e, position in x:
        num += 1
        if e:
            if (e.getCommand(), e.getCommandValue()) != (255,255):
                if not e.getCommand() in fx:
                    fx[e.getCommand()] = {}
                if e.getCommandValue() in fx[e.getCommand()]:
                    fx[e.getCommand()][e.getCommandValue()] += 1
                else:
                    fx[e.getCommand()][e.getCommandValue()] = 1
    output = fname + " effect statistics, " + str(num) + " events total\n"
    for key in fx:
        sorted = zip(fx[key].values(), fx[key].keys())
        sorted.sort()
        sorted.reverse()
        for count, cvalue in sorted:
            output = output + chr(64+key) + "-" + string.upper(hex(cvalue)[2:]) + ":" + str(count) + "\n"
    return output



def load(fname):
    return ITModule(fname)

def testSave(infile, outfile="c:\\tests\\out.it"):
    mod = load(infile)
    mod.unpack()
    mod.pack()
    mod.save(outfile)
    return filex.areSame(infile, outfile)
    
    

if __name__ == "__main__":
    # causing hang on load
    #x = ITModule(fname="c:\\it\\bent\\midnayl.it")
    #print x.numSamples()
    if 0:
        import filex
        reload(filex)
        print 
        for x in filex.dirtree("d:\\inpuj\\", "*.it"):
            print x
            fxstats(x)
            print "----------------------------------"
