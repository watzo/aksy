
import os, sys, string, time

import it, utilx, filex, filenamer
import xmod


class ITSampleExporter:
    def __init__(self, filelist=[], path="", seperator="-", createDir=1, \
                 useSampleNames=0, useSampleFilenames=1, useSampleNumbers=1, \
                 keepExtension=0, filterExtensions=1, makeLower=1, makeUpper=0, \
                 exportMode="Overwrite", samplesToExport=[]):
        # list of IT files to be exported
        self.filelist = utilx.tolist(filelist)

        self.exportPath = path
        self.seperator = seperator
        self.useSampleNames = useSampleNames
        self.useSampleFilenames = useSampleFilenames
        self.useSampleNumbers = useSampleNumbers
        self.keepExtension = keepExtension
        self.filterExtensions = filterExtensions
        self.createDir = createDir

        self.exportMode = exportMode

        self.makeLower = makeLower
        self.makeUpper = makeUpper

        self.samplesToExport = samplesToExport

    def SetList(self, filelist):
        self.filelist = utilx.tolist(filelist)

    def GetExportSampleFilename(self, itfname, itsample, sampleindex=0, checkIgnore=0):

        sampleName = utilx.stripnulls(itsample.name)
        sampleFilename = utilx.stripnulls(itsample.filename)
        sampleName = string.strip(sampleName)
        sampleFilename = string.strip(sampleFilename)

        sampleFilename = string.replace(sampleFilename, "/", "")
        sampleFilename = string.replace(sampleFilename, "\\", "")

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

        basename = ""
        if self.useSampleNumbers:
            basename = basename + str(sampleindex)
        if self.useSampleNames and sampleName != "":
            if basename != "":
                basename = basename + self.seperator
            basename = basename + sampleName
        if self.useSampleFilenames and sampleFilename != "":
            if basename != "":
                basename = basename + self.seperator
            basename = basename + sampleFilename

        if self.filterExtensions:
            # remove all extensions
            splitup = string.split(basename, ".")
            basename = splitup[0]

        # if there is no basename (most likely because it has no filename or samplename, and numbers are not selected),
        # then make the name the itfname base plus sample number
        if not basename:
            basename = os.path.splitext(os.path.basename(itfname))[0] + self.seperator + str(sampleindex)
            

        fname = filex.pathjoin(path, basename)
        root, ext = os.path.splitext(fname)
        if string.upper(ext) != ".WAV":
            fname = fname + ".wav"

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


    def ExportSamples(self, callback=None):
        exported = []
        errors = []
        
        idx = 0
        running = 1

        while (running) and (idx < len(self.filelist)):
            try:
                itfile = self.filelist[idx]
                print "--- Exporting samples from", itfile, "---"
                #mod = it.ITModule(fname=itfile, unpack=0)
                mod = xmod.loadmod(itfile, 0)
                sx = 0
                while (running) and (sx < len(mod.samples)):
                    if sx in self.samplesToExport or not self.samplesToExport:
                        outname, ignore = self.GetExportSampleFilename(itfile, mod.samples[sx], sx, checkIgnore=1)
                        if outname and not ignore:
                            filex.ensurePath(os.path.dirname(outname))
                            if mod.samples[sx].lenData() > 0:
                                #print "signed", mod.samples[sx].signed
                                mod.samples[sx].savefile(outname, modpath=itfile)
                                exported.append(outname)
                            else:
                                outname = None

                        time.sleep(0.01)                    

                        progress = (float(idx) / float(len(self.filelist))) * 100
                        progress = int(progress)
                        
                        if outname and callback:
                            if ignore:
                                outname = "*" + outname
                            running = apply(callback, (outname, progress))
                    sx = sx + 1
                del mod
            except:
                exit = apply(sys.excepthook, sys.exc_info(), {'inthread':1})
                if exit:
                    running = 0
                errors.append(itfile)

            idx = idx + 1

        if errors:
            print "Errors occured trying to export samples from:"
            print errors

        return exported, errors
        

    def PreviewExport(self, maxpreview=20, callback=None):
        """Return a preview list of the sample files that will be exported with the
        current settings."""

        if maxpreview == -1:
            maxpreview = 10000

        running = 1            
            
        preview = []
        idx = 0
        while (len(preview) < maxpreview) and (idx < len(self.filelist) and running):
            itfile = self.filelist[idx]
            #mod = it.ITModule(fname=itfile, unpack=0, loadSampleData=0)
            mod = xmod.loadmod(itfile, 0, loadSampleData=0)            
            sx = 0
            while (len(preview) < maxpreview) and (sx < len(mod.samples) and running):
                if sx in self.samplesToExport or not self.samplesToExport:
                    outname, ignore = self.GetExportSampleFilename(itfile, mod.samples[sx], sx, checkIgnore=1)
                    if ignore:
                        outname = "*" + outname
                    preview.append(outname)
                    if callback:
                        running = apply(callback, (outname,))
                sx = sx + 1
            del mod
            idx = idx + 1

        return preview

        

    
            