
"""
ITSplitter is a high-level application class for splitting a batch of it files by different parameters,
such as pattern, track, instrument, octave, and rows.

Basic usage:
Create ITSplitter instance, set splitting options in constructor or ITSplitter.SetSplitSettings,
then call ITSplitter.SplitFiles().  ITSplitter.PreviewSplit() can be used to get a preview of what files
will be created.
"""

import os, sys, string, copy, time
import xmod, it, utilx, filex, filenamer
from options import *
import itrender, vegas, waveslice, opt

MAX_SPLIT_PREVIEWS = 1000

# split criteria constants
SPLITBY_PATTERNS = 1
SPLITBY_TRACKS = 2
SPLITBY_INSTRUMENTS = 3
SPLITBY_OCTAVES = 4
SPLITBY_ROWS = 5

"""
split criteria overview:
Split critera are specified as a list of constants describing what kind of splitting is to be done.
Each file is split by its first criteria, then each of the resultings files is split by the next criteria (if any),
and so on.

For example, if the split criteria is specified as [SPLITBY_PATTERNS, SPLITBY_INSTRUMENTS], and a file has 10
patterns and 4 instruments, then first the file will be split into 10 new files, each containing one of the
patterns.  Then each of those 10 files will be split into 4 new files, each containing the instrument events
of the particular instrument.  The final result will be 40 files, named with associated split prefixes in
the order the criteria were applied, for example: pat5-ins1.it
"""


SPLIT_PREFIXES = {}
SPLIT_PREFIXES[SPLITBY_PATTERNS] = "p"
SPLIT_PREFIXES[SPLITBY_TRACKS] = "t"
SPLIT_PREFIXES[SPLITBY_INSTRUMENTS] = "i"
SPLIT_PREFIXES[SPLITBY_OCTAVES] = "o"
SPLIT_PREFIXES[SPLITBY_ROWS]= "r"

SPLIT_NAMES = {}
SPLIT_NAMES[SPLITBY_PATTERNS] = "patterns"
SPLIT_NAMES[SPLITBY_TRACKS] = "tracks"
SPLIT_NAMES[SPLITBY_INSTRUMENTS] = "instruments"
SPLIT_NAMES[SPLITBY_OCTAVES] = "octaves"
SPLIT_NAMES[SPLITBY_ROWS] = "rows"


#TODO
"""
# cache analysis so we don't have to recalculate it for every split file
class ModStats:
    pass
#TODO: implement modstats
if self.optimize and 2==1:
    modstats = ModStats()
    modstats.usedInstruments = mod.usedInstruments()
    modstats.usedSamples = mod.usedSamples()
    modstats.patternSamples = {}
    modstats.patternInstruments = {}
    idx = 0
    for p in mod.patterns:
        modstats.patternSamples[idx] = mod.patternUsedSamples(idx)
        modstats.patternInstruments[idx] = p.usedInstruments()
        idx += 1
else:
    modstats = None
if modstats:
    print "usedInstruments", modstats.usedInstruments
    print "usedSamples", modstats.usedSamples
"""

DefaultSplitOptions = opt.OptionsNoCase(path="", seperator="-", createDir=1, 
                 splitCriteria=[SPLITBY_PATTERNS], splitPrefixes=None, splitOptions=None, 
                 prependFilename=0, makeLower=1, makeUpper=0, 
                 exportMode="Overwrite", optimize=1, keepIntermediate=0, keepITs=0, renderFiles=0, 
                 renderOptions=itrender.DEFAULT_OPTIONS, ordersOnly=1, toSplit=[], 
                 useTrackDisable=0, useInstrumentVolumes=0,
                 currentTrackSettingsFunc=None, exportVegas=0, filePrefix="", fileSuffix="",
                 newfilenames={}, loopCount=1, renderSlice=0, numSlices=0, keepSlices=[],
                 getFilesFunc=None, padZeroes=1)

class SplitOptions(opt.OptionsNoCase):
    def __init__(self):
        super(SplitOptions, self).__init__()
        self.update(DefaultSplitOptions)


class ITSplitter:
    def __init__(self, filelist=[], options=SplitOptions(), **kwargs):

        if kwargs:
            options.update(kwargs)        

        self.options = options
                
        # list of IT files to be split
        self.filelist = utilx.tolist(filelist)
        self.newfilenames = options.newfilenames
        self.getFilesFunc = options.getFilesFunc
        self.__filesFromFilesFunc = None

        self.exportPath = options.path

        #opt.copy(options, self)
        
        self.seperator = options.seperator
        self.prependFilename = options.prependFilename
        self.createDir = options.createDir

        self.splitCriteria = options.splitCriteria
        self.splitOptions = options.splitOptions
        self.splitPrefixes = options.splitPrefixes

        self.exportMode = options.exportMode

        self.makeLower = options.makeLower
        self.makeUpper = options.makeUpper

        # remove unused samples?
        self.optimize = options.optimize

        # keep previous levels? (ex: if rendering track then pattern, this will keep the track files too)        
        self.keepIntermediate = options.keepIntermediate

        # keep it files when rendering to wav?  if not, they will be deleted.
        self.keepITs = options.keepITs

        # split tracks by disabling them?
        self.useTrackDisable = options.useTrackDisable

        # split instruments by setting global instrument volumes?
        self.useInstrumentVolumes = options.useInstrumentVolumes

        # if currentTrackSettingsFunc is passed, it will be used to retrieve volume and panning
        # settings for all tracks, which will be used in place of the files' current settings.
        # this is to allow currently opened documents to change them via solo and muting,
        # without saving the changes.
        self.currentTrackSettingsFunc = options.currentTrackSettingsFunc

        self.exportVegas = options.exportVegas

        self.filePrefix = options.filePrefix
        self.fileSuffix = options.fileSuffix
        
        # render the generated it files to WAV?        
        self.renderFiles = options.renderFiles
        self.renderOptions = options.renderOptions

        self.ordersOnly = options.ordersOnly

        self.loopCount = options.loopCount

        self.renderSlice = options.renderSlice
        self.numSlices = options.numSlices
        self.keepSlices = options.keepSlices

        self.padZeroes = options.padZeroes
        self.numPadZeroes = 2

        self.normalizeByParent = options.normalizeByParent

        #raise StandardError, "OH NO AN ERROR"

        # optional limited list; for example, if you only want to split certain patterns,
        # set toSplit to a list of the selected pattern numbers.
        self.toSplit = options.toSplit

        self.useTempDir = 0        
        self.savedSplitPath = None

        if not self.splitPrefixes:
            self.splitPrefixes = []
            for x in self.splitCriteria:
                self.splitPrefixes.append(SPLIT_PREFIXES[x])

        # define SPLIT_FUNCTIONS dict to call appropriate functions based on split criteria constants
        SPLIT_FUNCTIONS = {}
        SPLIT_FUNCTIONS[SPLITBY_PATTERNS] = self.SplitByPatterns
        SPLIT_FUNCTIONS[SPLITBY_TRACKS] = self.SplitByTrack
        SPLIT_FUNCTIONS[SPLITBY_INSTRUMENTS] = self.SplitByInstrument
        SPLIT_FUNCTIONS[SPLITBY_OCTAVES] = self.SplitByOctave
        SPLIT_FUNCTIONS[SPLITBY_ROWS]= self.SplitByRows
        self.SPLIT_FUNCTIONS = SPLIT_FUNCTIONS

        self.newmod = None  # used to store a temp working copy ITModule for making splits from

        self.exit = 0
        self.running = 0

        # used to keep track during ordersOnly pattern split
        self.__didPatterns = []


    def GetFiles(self, overridecache=0):
        if self.getFilesFunc:
            if (not self.__filesFromFilesFunc) or (overridecache):
                self.__filesFromFilesFunc = self.getFilesFunc()
            return self.__filesFromFilesFunc
        else:
            return self.filelist, self.newfilenames

    def SetSplitSettings(self):
        pass

    def SetList(self, filelist):
        self.filelist = utilx.tolist(filelist)


    def getFullExportPath(self, itfname):
        #translate filename
        itfname = self.newfilenames.get(itfname, itfname)

        exportPath = self.exportPath
        #print "export path is", exportPath
        if exportPath == "":
            exportPath = os.path.dirname(itfname)
            #print "set exportpath to", exportPath
        
        # add necessary subdirs to export path
        path = exportPath
        if self.createDir:
            itfnamebase = os.path.basename(itfname)
            root, ext = os.path.splitext(itfnamebase)
            ext = string.replace(ext, ".", "_")
            fnamedir = root
            path = filex.pathjoin(path, fnamedir)
            
        return path
        

    def GetSplitFilename(self, itfname, criteria, critOrder, critindex, checkIgnore=0, modext=".it", newext=""):
        """
        itfname - filename of file being split
        criteria - constant describing the split criteria (SPLITBY_TRACKS, SPLITBY_PATTERNS, etc)
        critOrder - the order of the criteria in the split process.  a split process can have more than one criteria, in
                  sequence.  example: if the criteria are [SPLITBY_INSTRUMENTS, SPLITBY_TRACKS], then the critOrders for
                  those criteria will be [0,1]
        critindex - number in sequence of the split - for example, if criteria is SPLITBY_PATTERNS, critindex will range from
                  0 to the maximum number of patterns.
        """

        #translate filename
        itfname = self.newfilenames.get(itfname, itfname)


        #print ".. getting splitfilename for", itfname, criteria, critOrder, critindex

        #print self.splitPrefixes

        if self.renderFiles and not newext:
            newext = ".wav"

        # instruments and tracks are 1-based, other criteria are 0-based
        if criteria == SPLITBY_INSTRUMENTS or criteria == SPLITBY_TRACKS:
            critindex = critindex + 1

        # calculate basename            
        basename = os.path.basename(itfname)
        root, ext = os.path.splitext(basename)
        if self.prependFilename or critOrder > 0:
            basename = root
        else:
            basename = ""

        # if fileSuffix has already been appended, remove it
        if critOrder > 0 and self.fileSuffix:
            suffix = self.seperator + self.fileSuffix
            lensuffix = len(suffix)
            if len(basename) >= lensuffix:
                if basename[-lensuffix:].lower() == suffix.lower():
                    basename = basename[:-lensuffix]
            

        # calculate path

        exportPath = self.exportPath
        #print "export path is", exportPath
        if exportPath == "":
            exportPath = os.path.dirname(itfname)
            #print "set exportpath to", exportPath
        
        # add necessary subdirs to export path
        fname = exportPath
        if self.createDir:
            itfnamebase = os.path.basename(itfname)
            root, ext = os.path.splitext(itfnamebase)
            ext = string.replace(ext, ".", "_")
            fnamedir = root
            fname = filex.pathjoin(fname, fnamedir)
        path = fname

        # if this is the first split, save the export path for later splits
        if critOrder == 0:
            self.savedSplitPath = path

        # if this isn't the first split, simply use saved dir
        if critOrder > 0:
        #    path = os.path.dirname(itfname)
            if self.savedSplitPath:
                path = self.savedSplitPath

        # append prefixes and/or suffixes to basename
        if self.prependFilename or critOrder > 0:
            basename = basename + self.seperator + self.splitPrefixes[critOrder] + str(critindex).zfill(self.numPadZeroes)
        else:
            basename = self.splitPrefixes[critOrder] + str(critindex).zfill(self.numPadZeroes)

        if critOrder == 0:
            if self.filePrefix:
                basename = self.filePrefix + self.seperator + basename

        if self.fileSuffix:
            basename += self.seperator + self.fileSuffix


        # calculate final filename by joining path, basename, and verifying extension
        fname = filex.pathjoin(path, basename)
        root, ext = os.path.splitext(fname)
        if ext.upper() != modext.upper():
            fname = fname + modext

        # make upper or lowercase if necessary
        if self.makeUpper:
            fname = string.upper(fname)
        if self.makeLower:
            fname = string.lower(fname)

        fname = filex.ensureValid(fname)

        if newext:
            checkfname = filex.replaceExt(fname, newext)
        else:
            checkfname = fname

        if self.exportMode == "Rename":
            if os.path.exists(checkfname):
                newfname = filenamer.uniqueFilename(checkfname, seperator=self.seperator)
                #print "renaming", fname, "to", newfname
                fname = filex.replaceExt(newfname, modext)
                checkfname = newfname

        # temp name is temp path plus normal path minus drive
        # for example, if normal path is c:\it\export\test\a.it,
        # then temp path is c:\postmod\temp\it\export\test\a.it
        
        temppath = filex.pathjoin(filex.GetPath83(options.TempPath), os.path.dirname(fname))
        tempname = filex.pathjoin(temppath, os.path.basename(fname))

        #print "fname, tempname:", (fname, tempname)

        if checkIgnore:
            ignore = ((self.exportMode == "Ignore") and os.path.exists(checkfname))
            return (fname, tempname, ignore)
        else:
            return (fname, tempname)

    # the split functions return (outputname, exportname)
    # outputname the is the filename actually used and created for the split file
    # exportname is the filename that would have been used (or was used) according to user export options
    # sometimes these will be the same, other times outputname will be exportname except using
    # the options.TempPath path.

    def SplitByPatterns(self, mod, modfname, modstats=None, criteria=SPLITBY_PATTERNS, critorder=0, x=0):

        # mod is the loaded module, modfname is its filename. critorder is the order of pattern in multi split -
        # used for filename only.  and x is the order or pattern index.

        #what = nothing
                
        if self.ordersOnly and not self.toSplit:
            if mod.isOrderListEmpty():
                mod.unfold()
            #print "lenorders", len(mod.header.orders), mod.header.orders
            if x < len(mod.header.orders):
                tx = mod.header.orders[x]
            else:
                return None, None
        else:
            tx = x

        outname, tempname, ignore = self.GetSplitFilename(mod.path, criteria, critorder, tx, checkIgnore=1, modext=mod.ext)

        if tx in self.__didPatterns:
            # already did this pattern (used by ordersOnly)
            return None, None
            
        self.__didPatterns.append(tx)        

        if self.useTempDir:
            usename = tempname
        else:
            usename = outname

        if not ignore:

            if not os.path.exists(modfname):
                realfile = filex.pathjoin(filex.GetPath83(options.TempPath), modfname)
            else:
                realfile = modfname

            if not self.newmod:
                self.newmod = xmod.loadmod(realfile, unpack=0)

            if usename:
                if self.ordersOnly and not self.toSplit:
                    try:
                        onlyPattern = mod.patternsInOrders()[x]
                    except IndexError:
                        onlyPattern = None
                else:
                    try:
                        onlyPattern = mod.ppatterns[x]
                    except IndexError:
                        onlyPattern = None

                # if this is a blank pattern, return without saving this file
                if (not onlyPattern) or (onlyPattern.isBlank()):
                    root, ext = os.path.splitext(usename)
                    return None, None

                self.newmod.ppatterns = [onlyPattern]
                self.newmod.setOrderList([0])

                if critorder == 0 and self.currentTrackSettingsFunc:
                    tv, tp = self.currentTrackSettingsFunc()
                    self.newmod.setTrackVolumes(tv)
                    self.newmod.setTrackPannings(tp)

                print "-- saving", usename
                filex.ensurePath(os.path.dirname(usename))
                self.newmod.save(usename, pack=0)

            if self.optimize:
                optmod = xmod.loadmod(fname=usename)
                #optmod.optimizeSamples(usamples=modstats.patternSamples[x])
                optmod.optimizeSamples()
                optmod.save(usename)
                del optmod
        else:
            if not self.keepIntermediate:
                usename = "*" + usename
                    
        return usename, outname



    def SplitByTrack(self, mod, modfname, modstats=None, criteria=SPLITBY_TRACKS, critorder=0, x=0):
        #print "split by track", mod, criteria, critorder, x
        origpath = mod.path
        outname, tempname, ignore = self.GetSplitFilename(mod.path, criteria, critorder, x, checkIgnore=1, modext=mod.ext)
        if self.useTempDir:
            usename = tempname
        else:
            usename = outname

        if not ignore:

            mod.unpack()

            if not os.path.exists(modfname):
                realfile = filex.pathjoin(filex.GetPath83(options.TempPath), modfname)
            else:
                realfile = modfname

            if mod.areTrackNotesEmpty(x):
                return None, None

            if usename and not ignore:
                if self.useTrackDisable:
                    mod.makeSolo(x, useVolumes=1)

                    #no need to optimize if soloing by volume

                    if critorder == 0 and self.currentTrackSettingsFunc:
                        # since we're using a solo track disable, the custom volumes and pannings
                        # do not apply - but we should skip this track entirely if it doesn't
                        # exist according to custom settings.
                        #TODO: this might change if an actual volume and panning mixer is implemented,
                        # right now it only deals with mute and solo.
                        
                        tv, tp = self.currentTrackSettingsFunc()
                        if tp[x] >= 128:
                            # we're disabled, so skip this track
                            #print "-- SKIPPING track", x
                            return None, None
                        #mod.setTrackVolumes(tv)
                        #mod.setTrackPannings(tp)

                    print "-- saving", usename
                    filex.ensurePath(os.path.dirname(usename))
                    mod.save(usename, pack=0)
                    mod.path = origpath

                else:   # not self.useTrackDisable
                    newmod = xmod.loadmod(realfile)
                    newmod.makeSolo(x)

                    if self.optimize:
                        newmod.optimizeSamples()

                    if critorder == 0 and self.currentTrackSettingsFunc:
                        tv, tp = self.currentTrackSettingsFunc()
                        if tp[x] >= 128:
                            #we're disabled, so skip this track
                            #print "-- nv SKIPPING track", x
                            return None, None
                            
                        newmod.setTrackVolumes(tv)
                        newmod.setTrackPannings(tp)

                    print "-- saving", usename
                    filex.ensurePath(os.path.dirname(usename))
                    newmod.save(usename)
                    del newmod

        else:
            if not self.keepIntermediate:
                usename = "*" + usename
                    
        return usename, outname


    def SplitByInstrument(self, mod, modfname, modstats=None, criteria=SPLITBY_INSTRUMENTS, critorder=0, x=0):
        origpath = mod.path
        outname, tempname, ignore = self.GetSplitFilename(mod.path, criteria, critorder, x, checkIgnore=1, modext=mod.ext)
        if self.useTempDir:
            usename = tempname
        else:
            usename = outname

        if not ignore:

            mod.unpack()            

            if not os.path.exists(modfname):
                realfile = filex.pathjoin(filex.GetPath83(options.TempPath), modfname)
            else:
                realfile = modfname

            if critorder == 0 and self.currentTrackSettingsFunc:
                tv, tp = self.currentTrackSettingsFunc()
                mod.setTrackVolumes(tv)
                mod.setTrackPannings(tp)

            #print "Getting used instruments"
            usedInstruments = mod.usedInstruments()
            if x+1 not in usedInstruments:
                return None, None
            
            if usename:
                if self.useInstrumentVolumes:
                    mod.soloInstrumentsByVolume(x+1)
                    # set the soloed instrument to its initial volume
                    mod.setInstrumentGlobalVolume(x, self.initialVolumes[x])

                    if critorder == 0 and self.currentTrackSettingsFunc:
                        tv, tp = self.currentTrackSettingsFunc()
                        mod.setTrackVolumes(tv)
                        mod.setTrackPannings(tp)

                    print "-- saving", usename
                    filex.ensurePath(os.path.dirname(usename))
                    mod.save(usename, pack=0)
                    mod.path = origpath
                else:
                    print "-- loading", realfile
                    newmod = xmod.loadmod(realfile)
                    
                    #print "orders:", newmod.header.orders
                    # instruments are 1-based
                    newmod.makeSoloInstruments(x+1)

                    if self.optimize:
                        newmod.optimizeSamples()

                    if critorder == 0 and self.currentTrackSettingsFunc:
                        tv, tp = self.currentTrackSettingsFunc()
                        newmod.setTrackVolumes(tv)
                        newmod.setTrackPannings(tp)
                        
                    print "-- saving", usename
                    filex.ensurePath(os.path.dirname(usename))
                    newmod.save(usename)
                    del newmod
        else:
            if not self.keepIntermediate:
                usename = "*" + usename
                    
        return usename, outname

    def SplitByOctave(self, mod, criteria=SPLITBY_OCTAVES, critorder=0, x=0):
        return ""

    def SplitByRows(self, mod, criteria=SPLITBY_ROWS, critorder=0, x=0):
        return ""

    def SplitFiles(self, callback=None, renderCallback=None):
        a = time.time()
        #print "callback", str(callback)
        split = []

        self.filelist, self.newfilenames = self.GetFiles()

        # the callback returns 1 if we should keep running, 0 if we should stop.        
        self.running = 1

        startLen = len(self.filelist)
        #print "looplist", self.filelist        
        looplist = self.filelist
        theListLength = len(looplist)
        if theListLength == 1:
            singleFile = 1
        else:
            singleFile = 0

        totCrits = len(self.splitCriteria)
        theListLength = theListLength * totCrits
            
        cx = 0  # current criteria index
        fileIdx = 0
        cacheCrits = {}  # used to cache number of patterns, tracks, or instruments in each mod (num criteria data)

        intermediate = []
        final = []
        rendered = []
        errors = []

        toplist = 1   # are we still on the first iteration?        

        outname = ""
        
        for criteria in self.splitCriteria:
            
            processedList = []
            startLen = len(looplist)
            fnum = 0
            for itfile in looplist:
                transitfile = self.newfilenames.get(itfile, itfile)
                fnum += 1

                print "--- Splitting", itfile, "by", SPLIT_NAMES[criteria], "---"

                # if this is the first iteration, initialize the renderer if necessary.
                if toplist:
                    if self.renderFiles:
                        #print "setting up renderer with normfile", itfile
                        renderer = itrender.ITRenderer()
                        kwargs = self.renderOptions
                        if self.renderOptions['normalize'] and self.normalizeByParent:
                            kwargs['normalizeFile'] = itfile
                            callback("*Normalizing...")
                            #kwargs['callback'] = callback
                        elif self.renderOptions['normalize']:
                            # not normalizing by parent
                            pass
                        if renderCallback:
                            kwargs['callback'] = renderCallback
                        renderer.init(**kwargs)
                    else:
                        renderer = None
                else:
                    # otherwise just use the existing renderer
                    pass
                
                try: #itfile loop

                    if not self.running:
                        break

                    #doerrortest = errortestervar
                    
                    fileIdx += 1

                    if not os.path.exists(itfile):
                        realfile = filex.pathjoin(filex.GetPath83(options.TempPath), itfile)
                    else:
                        realfile = itfile

                    #print "realfile", realfile, itfile
                    
                    self.newmod = None
                    mod = xmod.loadmod(realfile, unpack=0)
                    # it is the split functions responsibility to unpack the mod if necessary

                    # save initial instrument volumes
                    self.initialVolumes = [mod.getInstrumentGlobalVolume(i) for i in range(mod.numInstruments())]
                        

                    #print "corruption", mod.corrupt, mod.corruption                    
                    if mod.corruption:
                        errors.append(transitfile)
                        continue
                        #raise StandardError, "Module is corrupt or unsupported"

                    modstats = None
                    #TODO: see cache analysis notes above
                    
                    # get all needed crits from cache.  if not cached, get them and cache them now.
                    # (this refers to the number of crit data - such as number of patterns, tracks, and instruments)
                    crits = cacheCrits.get(mod.path, None)
                    if not crits:
                        totalgen = 1
                        crits = []
                        ix = 0
                        for crit in self.splitCriteria:
                            # if this criteria actually applies to this mod, get the numcrits, else set to 0
                            # cx is the index of the current criteria, so all criteria in the list >= to its index apply.
                            if ix >= cx:
                                xx = self.GetNumCriteriaData(crit, mod)
                            else:
                                xx = 0
                                
                            crits.append(xx)
                            
                            if cx == 0:
                                totalgen = totalgen * xx
                                
                            ix += 1
                        cacheCrits[mod.path] = tuple(crits)

                        # theListLength is used for the progress calculation (1-100)
                        if cx == 0:
                            theListLength = theListLength + totalgen
                        
                        
                    #numCrits = self.GetNumCriteriaData(criteria, mod)
                    numCrits = crits[cx]

                    if self.padZeroes:
                        self.numPadZeroes = len(str(numCrits))
                    else:
                        self.numPadZeroes = 0

                    # for example, if we're splitting by patterns and there are 5 patterns,
                    # numCrits will be set to 5.  if by tracks and 8 tracks, numCrits will
                    # be 8.

                    #theListLength = theListLength + numCrits
                    
                    self.__didPatterns = []

                    if self.toSplit:
                        loopRange = self.toSplit
                    else:
                        loopRange = xrange(0, numCrits)

                    #print "loopRange", loopRange, "numCrits", numCrits

                    progress = 0
                    outname = ""
                    
                    #for x in xrange(0, numCrits): # numCrits loop (splitting of a single file)
                    for x in loopRange: # numCrits loop (splitting of a single file)
                        if not self.running:
                            break

                        self.useTempDir = 0
                        if self.renderFiles and not self.keepITs:
                            # IT files are not our final output, so keep the it files in the temp directory
                            self.useTempDir = 1
                        elif (cx < len(self.splitCriteria)-1) and not self.keepIntermediate:
                            # these particular IT files are not part of the final output, so keep them in the temp directory
                            self.useTempDir = 1
                        
                        #outname = self.GetSplitFilename(itfile, criteria, cx, x)

                        # now call the appropriate split function to create one single it file of the current criteria.
                        # the split functions (listed in self.SPLIT_FUNCTIONS) return (outname, exportname)

                        # outname is the actual filename created, exportname is the filename according to export
                        # options.  these will be the same UNLESS the file is created in the temp directory,
                        # in which case outname will be the temp path, and exportname will be the user-requested
                        # path.  this is used for multi-criteria splits where only the non-intermediate files
                        # are to be kept.
                        #outname, exportname = apply(self.SPLIT_FUNCTIONS[criteria], (mod, itfile, modstats, criteria, cx, x))
                        outname, exportname = self.SPLIT_FUNCTIONS[criteria](mod, itfile, modstats, criteria, cx, x)
                        wavoutname = exportname
                        #print "wavout", wavoutname, outname
                        
                        fileIdx += 1
                        
                        if outname:
                            split.append(outname)
                            processedList.append(outname)

                            # if this is not the last criteria, this is an intermediate file
                            if (cx < len(self.splitCriteria)-1):
                                intermediate.append(outname)
                                if self.keepIntermediate:
                                    final.append(exportname)
                                isintermediate = 1
                            else:
                                #final.append(outname)
                                if not renderer:
                                    final.append(exportname)
                                isintermediate = 0

                            # if using loop count, now we modify the file's order list
                            if (not isintermediate) and self.loopCount > 1:
                                tempmod = xmod.loadmod(outname, 0)
                                tempmod.repeatOrderList(self.loopCount)
                                tempmod.save(outname, 0)

                            # now render the output file, if we are rendering
                            didrender = 0
                            #print "rcheck", renderer, self.keepIntermediate, isintermediate
                            if renderer and ((self.keepIntermediate) or (not isintermediate)):
                                outx = os.path.splitext(wavoutname)[0] + ".wav"
                                print "-- Rendering", outname, "to", outx
                                renderer.Render(outname, outx)
                                #print "-- Done rendering", outname

                                rendered.append(outname)
                                final.append(outx)
                                didrender = 1

                            # now slice if appropriate
                            if didrender and self.renderSlice:
                                print "-- Slicing", outx, self.keepSlices
                                sliced = waveslice.sliceFile(outx, outx, self.numSlices, callback=None, slices=self.keepSlices)
                                #final.remove(outx)  # we don't keep the original
                                final += sliced
                                filex.remove(outx)
                                                                                            
                            # progress is the progress over the whole file list
                            progress = (float(fileIdx) / float(theListLength)) * 100
                            progress = int(progress)

                            # subprogress is the progress over the current file
                            subprogress = (float(x) / float(numCrits)) * 100

                            if singleFile:
                                #progress = subprogress
                                pass
                            else:
                                #print fileIdx, startLen
                                progsec = 100 / totCrits
                                progress = (progsec * (cx))
                                progress += (float(fnum) / float(startLen)) * progsec
                                

                            #outname = ""                            
                            if callback:
                                if didrender:
                                    outname = outx
                                elif isintermediate and not self.keepIntermediate:
                                    outname = "*" + os.path.basename(outname)
                                self.running = apply(callback, (outname,progress,subprogress))
                                #if outname == "*" or outname == "":
                                #    print "!!!", outname, "!!!", 
        
                    # end numCrits loop (splitting of a single file)

                    self.running = apply(callback, (outname,progress,100))
                    
                    del mod
                    del self.newmod
                except: #itfile loop
                    self.exit = 999
                    apply(sys.excepthook, sys.exc_info(), {'inthread':1, 'onExit':self.OnExit})

                    # wait for exit
                    #while self.exit == 999:
                    #    time.sleep(0.2)
                    #print "self.exit is", self.exit
                    #if self.exit:
                    #    running = 0

                    errors.append(transitfile)

                if self.exportVegas:
                    vegasout = filex.pathjoin(self.getFullExportPath(itfile), filex.filebase(transitfile)+".veg")
                    print "-- Exporting Vegas EDL", vegasout
                    vegas.writeEDL(vegasout, final, multi=0)

                print "--- Done splitting", itfile, "by", SPLIT_NAMES[criteria], "---"


            # set looplist to the list we just generated, so we can loop over the new batch in the next iteration.

            #print "processed", processedList
            if errors:
                print "Errors occured while trying to split the following files:"
                print errors
            looplist = processedList
            toplist = 0
            
            #theListLength = theListLength + len(looplist)
            cx = cx + 1


        del cacheCrits

        if not self.keepIntermediate:
            #print "Deleting intermediate files..."
            for x in intermediate:
                filex.remove(x)

        if not self.keepITs:
            #print "Deleting temp it files..."
            for x in rendered:
                filex.remove(x)
                
        #return split, errors
        #print final, errors
        #print "timed", time.time() - a
        return final, errors

    def OnExit(self):
        # method that external threads can call to end our process
        #print "onexit setting running to 0"
        self.running = 0

    
    def GetNumCriteriaData(self, criteria, mod=None, fname=None):

        if fname:
            mod = xmod.loadmod(fname)
        
        if criteria == SPLITBY_PATTERNS:
            if self.ordersOnly and not self.toSplit:
                numCrits = len(mod.patternsInOrders())
            else:
                numCrits = len(mod.ppatterns)
        elif criteria == SPLITBY_TRACKS:
            mod.unpack()
            numCrits = mod.numTracks()
        elif criteria == SPLITBY_INSTRUMENTS:
            numCrits = mod.numInstruments()
        else:
            numCrits = 0

        return numCrits            


    def Preview(self, maxpreview=MAX_SPLIT_PREVIEWS, callback=None):
        """Return a preview list of the IT files that will be created with the
        current settings."""
        if maxpreview == -1:
            maxpreview = 10000

        self.filelist, self.newfilenames = self.GetFiles()
            
        mod = None
        running = 1
        preview = []

        looplist = self.filelist
        cx = 0
        #print "self.splitCriteria", self.splitCriteria
        for criteria in self.splitCriteria:
            #print looplist
            
            processedList = []
            idx = 0
            for itfile in looplist:
                if len(preview) >= maxpreview or not running:
                    break
                
                # since this is a preview, we only load the topmost mod once.
                # filenames will be inaccurate, especially for batches, but will still give a good preview of how
                # the output files will look.
                if not mod:
                    mod = xmod.loadmod(itfile, unpack=0)
                numCrits = self.GetNumCriteriaData(criteria, mod)
                if self.padZeroes:
                    self.numPadZeroes = len(str(numCrits))
                else:
                    self.numPadZeroes = 0
                #print itfile, "crits: ", numCrits
                if self.toSplit:
                    loopRange = self.toSplit
                else:
                    loopRange = xrange(0, numCrits)
                for x in loopRange:
                    if len(preview) >= maxpreview or not running:
                        break
                    
                    outname, tempname, ignore = self.GetSplitFilename(itfile, criteria, cx, x, checkIgnore=1, modext=mod.ext)
                    if ignore:
                        outname = "*" + outname
                    preview.append(outname)
                    processedList.append(outname)
                    if self.renderFiles:
                        outname = os.path.splitext(outname)[0] + '.wav'

                    if callback:
                        running = apply(callback, (outname,))
            looplist = processedList
            cx = cx + 1

        del mod
        return preview        

