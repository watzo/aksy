
# defines generic module type that can describe it, xm, psycle, buzz, fruityloops, etc

# target formats:# IT, XM, BMX/BMW, PSY, FLP, ACD, MID, Orion, Vegas, Bidule, FLAW
# also perhaps partials or combos, like GIG or MID/SF2

"""
Samples, Instruments, Patterns, and OrderLists all refer to the IT/XM meanings.

Samples are a collection of audio data files, with optional sample playback info.
Instruments define a way of playing sets of samples (or other things).
Patterns are patterns of sequenced note/effect/etc data.

OrderLists describe a sequence of patterns.  IT/XM/Psycle have only one order list,
while Buzz and FruityLoops have multiple parallel orderlists.

Plugins could refer to VST plugins, Buzz or Psycle machines, etc.

How will Plugins relate to instruments?
What about Effects?  should it be PluginEffects and PluginInstruments?

PluginGrid refers to modular setups of plugins, such as Buzz and Psycle have.
Could FruityLoops bus/effects setup be considered a PluginGrid?
maybe it should be PluginRouters?

"""

import os

class XMOD(object):
    def __init__(self):
        self.hasSamples = 1
        self.hasInstruments = 1
        self.hasPatterns = 1
        self.hasOrderLists = 1
        self.hasPlugins = 0
        self.hasPluginRouters = 0
        self.hasSeqTracks = 1
        self.hasSeqEvents = 1
        self.hasAudioTracks = 0

class Header:
    def __init__(self):
        pass

class Sample:
    def __init__(self):
        pass

class Instrument:
    def __init__(self):
        pass

class Envelope:
    def __init__(self):
        pass

class Pattern:
    def __init__(self):
        pass

class Event:
    def __init__(self):
        pass

class Track:
    def __init__(self):
        pass

    

class CompressedPattern:
    def __init__(self):
        pass

class Module:
    def __init__(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def next(self, fname):
        # event iterator
        raise NotImplementedError

    def load(self, fname):
        raise NotImplementedError

    def save(self, fname):
        raise NotImplementedError

    def get(self, pattern, track, row):
        raise NotImplementedError
        # return event

    def unfold(self, pack=1):
        raise NotImplementedError

    def setOrderList(self, newlist):
        raise NotImplementedError

    def isOrderListEmpty(self):
        raise NotImplementedError

    def setNote(self, pattern, track, row, value):
        raise NotImplementedError

    def setInstrument(self, pattern, track, row, value):
        raise NotImplementedError

    def setSample(self, pattern, track, row, value):
        # alias for setInstrument
        raise NotImplementedError

    def setCommand(self, pattern, track, row, command, value):
        raise NotImplementedError

    def getTempo(self):
        raise NotImplementedError
            #TODO: IT change


    def getSpeed(self):
        raise NotImplementedError
            #TODO: IT change


    def getGlobalVolume(self):
        raise NotImplementedError
            #TODO: IT change


    def getMixingVolume(self):
        raise NotImplementedError
            #TODO: IT change


    def getName(self):
        raise NotImplementedError
            #TODO: IT change


    def setSpeed(self, speed):
        raise NotImplementedError
            #TODO: IT change


    def setTempo(self, tempo):
        raise NotImplementedError
            #TODO: IT change


    def setGlobalVolume(self, volume):
        raise NotImplementedError
            #TODO: IT change


    def setMixingVolume(self, volume):
        raise NotImplementedError
            #TODO: IT change


    def setName(self, name):
        raise NotImplementedError
            #TODO: IT change


    def clearPatterns(self):
        raise NotImplementedError

    def numInstruments(self):
        raise NotImplementedError

    def numTracks(self):
        raise NotImplementedError
    numChannels = numTracks

    def numSamples(self):
        raise NotImplementedError

    def patternList(self):
        raise NotImplementedError

    def numPatterns(self):
        raise NotImplementedError

    def validSamples(self):
        raise NotImplementedError

    def sampleNames(self):
        raise NotImplementedError

    def instrumentNames(self):
        raise NotImplementedError
        
    def trackNames(self):
        raise NotImplementedError

    def patternNames(self):
        raise NotImplementedError

    def orderList(self):
        raise NotImplementedError
        
    def noteAdd(self, pattern, value):
        raise NotImplementedError

    def allowUnlimitedSamples(self):
        raise NotImplementedError
        #TODO: IT change

    def disallowUnlimitedSamples(self):
        raise NotImplementedError
        #TODO: IT change

    def setTrackSamples(self, pattern, samples):
        """given a pattern and list of sample numbers, sets tracks to those sample numbers.
        this method is intended to be used on new sequences only, that do not already have assigned
        sample/instrument events.  this method only sets the sample numbers on the first row of
        the specified pattern.
        from the given sample list, they are placed starting on track 0 and ascending until the end of the
        list."""
        raise NotImplementedError

    def exportSamples(self, path):
        raise NotImplementedError

    def makeSolo(self, track):
        raise NotImplementedError

    def optimizeSamples(self, usamples=None):
        raise NotImplementedError

    def uncompress(self):
        raise NotImplementedError

    def allOffsets(self, includeEnd=1):
        raise NotImplementedError

    def allOffsetsTyped(self, includeEnd=1):
        raise NotImplementedError

    def allChunks(self):
        raise NotImplementedError

    def areNotesEmpty(self):
        """returns true if all note data in all patterns are empty"""
        raise NotImplementedError

    def areTrackNotesEmpty(self, track):
        """returns true if all note data in specified track in all patterns are empty"""
        raise NotImplementedError

    def usedInstruments(self):
        """return list of all instruments used in all patterns"""
        raise NotImplementedError

    def trackUsedInstruments(self, track):
        """return list of all instruments used in specified track, all patterns"""
        raise NotImplementedError

    def usedSamples(self):
        """return list of all samples used by all instruments used"""
        raise NotImplementedError

    def patternUsedSamples(self, patternidx):
        """return list of all samples used by all instruments used in specified pattern"""
        raise NotImplementedError

    def loadSample(self, path=None, data=None, name=None, params=None, pos=None):
        """load new sample into module, returns sample number (new length of list)"""
        raise NotImplementedError

    def loadSampleList(self, samplist, overwrite=0):
        """load list of sample filenames into module, appending or overwriting.
        returns num successfully loaded, and list of samples that fail to load."""
        raise NotImplementedError

    def loadSampleDir(self, path, mask="*.wav"):
        """load directory full of samples into module.
        returns number of samples loaded."""
        raise NotImplementedError

    def makePlayableCopy(self, newname, copyAlways=1):
        """makes a playable copy from fname and saves to newname.
        this makes a linear sequence if there is no sequence.  if no changes are necessary,
        newname will simply be a copy of fname.
        if copyAlways is false, a copy will only be created if changes are made. default is true.
        returns filename of new copy (or returns fname if copyAlways is false and no changes made), and numorders
        """
        raise NotImplementedError


import itx, xm

def loadmod(fname, unpack=1, loadSampleData=1):
    ext = os.path.splitext(fname)[1].upper()
    if ext == ".IT":
        return itx.ITX(fname, unpack=unpack, loadSampleData=loadSampleData)
    elif ext == ".XM":
        return None
        return xm.XMModule(fname, unpack=unpack, loadSampleData=loadSampleData)
    else:
        return None


if __name__ == "__main__":
    x = Module()
    print x.usedSamples()


    