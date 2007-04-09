
import os, string, sys
import it, utilx, filex, filenamer

MAX_PREVIEWS = 100


class GenericProcessor:
    def __init__(self, filelist=[], path="", seperator="-", createDir=1, 
                 keepExtension=0, filterExtensions=1, makeLower=1, makeUpper=0, 
                 exportMode="Overwrite",
                 prefix="", suffix="", outfile=None):
        # list of IT files to be processed
        self.filelist = utilx.tolist(filelist)

        self.exportPath = path
        self.seperator = seperator
        self.keepExtension = keepExtension
        self.filterExtensions = filterExtensions
        self.createDir = createDir

        self.exportMode = exportMode

        self.makeLower = makeLower
        self.makeUpper = makeUpper

        self.prefix = prefix
        self.suffix = suffix

        # so we can call processors with one specific output file
        # if specified, GetOutputFilename will always return this.
        self.outfile = None

    def SetList(self, filelist):
        self.filelist = utilx.tolist(filelist)

    def GetOutputFilename(self, itfname, reqext=None, checkIgnore=0):
        """returns filename modified by current export settings.
        if checkIgnore is true, a tuple (filename, ignore) is returned, with the latter specifying whether
        this file should be ignored (if export mode is "Ignore" and the file already exists"""

        if self.__dict__.has_key("outfile") and self.outfile:
            return (self.outfile, 0)

        # if outext is defined, it will be used as the extension for all outputted files
        if self.__dict__.has_key("outext") and self.outext:
            outext = self.outext
        else:
            outext = None

        exportPath = self.exportPath
        if exportPath == "":
            exportPath = os.path.dirname(itfname)
        
        fname = exportPath
        if self.createDir:
            itfname = os.path.basename(itfname)
            root, ext = os.path.splitext(itfname)
            ext = string.replace(ext, ".", "_")
            fnamedir = root
            if self.keepExtension:
                fnamedir = fnamedir + ext
            fname = filex.pathjoin(fname, fnamedir)
        path = fname

        basename = os.path.basename(itfname)

        if self.filterExtensions:
            # remove all extensions
            splitup = string.split(basename, ".")
            basename = splitup[0]

        # add prefix and/or suffix to basename if they are specified
        if len(self.prefix) > 0:
            basename = self.prefix + self.seperator + basename
        if len(self.suffix) > 0:
            basename = basename + self.seperator + self.suffix

        fname = filex.pathjoin(path, basename)
        root, ext = os.path.splitext(fname)

        if outext:
            fname = root + outext
        elif reqext:
            if string.upper(ext) != string.upper(reqext):
                fname = fname + string.lower(reqext)

        if self.makeUpper:
            fname = string.upper(fname)
        if self.makeLower:
            fname = string.lower(fname)

        fname = filex.ensureValid(fname)

        if self.exportMode == "Rename":
            if os.path.exists(fname):
                newfname = filenamer.uniqueFilename(fname, seperator=self.seperator)
                #print "renaming", fname, "to", newfname
                fname = newfname

            
        if checkIgnore:
            ignore = (os.path.exists(fname) and self.exportMode == "Ignore")
            return (fname, ignore)
        else:
            return fname


    def ProcessFiles(self, callback=None, callbackList=0):
        processed = []
        
        idx = 0
        running = 1
        errors = []

        while (running) and (idx < len(self.filelist)):
            itfile = self.filelist[idx]
            #mod = it.ITModule(fname=itfile)

            outname, ignore = self.GetOutputFilename(itfile, ".it", checkIgnore=1)
            if outname and not ignore:
                # if outname is valid, do the processing and save to it
                filex.ensurePath(os.path.dirname(outname))
                #TODO: right now this is a dummy file
                fp = open(outname, "wb")
                fp.write("dummy")
                fp.close()
                
            # calculate overall progress through filelist, to be passed to the callback
            progress = (float(idx) / float(len(self.filelist))) * 100
            progress = int(progress)
            
            if outname and callback:
                if callbackList:
                    running = callback(*(utilx.tolist(outname), progress))
                else:
                    running = callback(*(outname, progress))
            #del mod
            idx = idx + 1

        return processed, errors
        

    def Preview(self, maxpreview=MAX_PREVIEWS, callback=None, callbackList=0):
        """Return a preview list of the files that will be exported/created with the
        current settings.  Calls optional callback function as each filename is determined.
        If callbackList is true, the filename is passed to the callback as a list of strings (usually only one string),
        if it is false, the filename is passed as a single string.  default is false.
        """

        if maxpreview == -1:
            maxpreview = 10000
            
        preview = []
        idx = 0
        while (len(preview) < maxpreview) and (idx < len(self.filelist)):
            itfile = self.filelist[idx]
            #mod = it.ITModule(fname=itfile, unpack=0, loadSampleData=0)
            outname, ignore = self.GetOutputFilename(itfile, reqext=".it", checkIgnore=1)
            if ignore:
                outname = "*" + outname
            preview.append(outname)
            if callback:
                if callbackList:
                    apply(callback, (utilx.tolist(outname),))
                else:
                    apply(callback, (outname,))
            #del mod
            idx = idx + 1

        return preview


    def SetOutExt(self, outext=".wav"):
        """ if an outext is set, all output filenames will use the specified extension, overriding any reqext """
        self.outext = outext

    def SetOutfile(self, outfile):
        """ setting an outfile filename overrides auto-generation of output filenames """
        #print "so", sys._getframe(1).f_code.co_name
        self.outfile = outfile

 