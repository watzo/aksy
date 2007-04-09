
import os, string, traceback
import threadx, processx, filex

from options import *
from generic_processor import *
from itx import *
import renderers, modplayer, normalize

DEFAULT_OPTIONS = {'renderer': options.DefaultRenderer, 'amplify': 50, 'normalize': 1, 'interpolation': 1, 'samplerate': 44100, 'usefloat': 0, 'volramp': 1}

PROGRESS_SLEEPTIME = .5 # in seconds


class ITRenderer(GenericProcessor):

    def __init__(self, *args, **kwargs):        
        GenericProcessor.__init__(self, *args, **kwargs)
        self.Renderer = 0
        self.progressCallback = None
        self.numOrders = 100
        self.init()

    def SetCurrentTrackSettingsFunc(self, func):
        self.currentTrackSettingsFunc = func

    def init(self, renderer=None, callback=None, numorders=100, amplify=50, normalize=1, outext=".wav", normalizeFile=None, interpolation=1, samplerate=44100, usefloat=0, volramp=1):
        # if normalizeFile is specified, manual amplification settings will be ignored!

        self.SetCurrentTrackSettingsFunc(None)

        # self.Renderer is the int index number of the renderer defined in renderers.py
        # self.__renderer is the actual Renderer object
        
        if renderer == None:
            self.Renderer = options.DefaultRenderer
        else:
            self.Renderer = renderer

        self.__renderer = renderers.getRenderer(self.Renderer)            
            
        self.progressCallback = callback
        self.numOrders = numorders
        self.amplify = amplify
        self.normalize = normalize
        self.interpolation = interpolation
        self.samplerate = samplerate
        self.usefloat = usefloat
        self.volramp = volramp

        # if a normalization file is specified, amplify will be retrieved as that files normalized amplify, then the amplification
        # will be set staticly to that value for all future files
        self.normalizeFile = normalizeFile
        self.normalized = 0   # flag for normalizeFile, denoting whether self.amplify has been calculated and set yet.
        self.SetOutExt(outext)

        #TODO: use renderers module
        self.amplifyOptions = 1 # are amplification options available?
        if string.find(string.upper(self.__renderer.filename), "MIKWAV") > -1:
            self.amplifyOptions = 0

        #print "initialized renderer:", self.Renderer, self.amplify, self.normalize, self.normalizeFile, self.amplifyOptions
        

    def SetAmplify(self, amplify):
        self.amplify = amplify

    def SetNormalize(self):
        self.amplify = -1

    def SetRenderer(self, renderer=None):
        if renderer:
            self.Renderer = renderer
        else:
            self.Renderer = options.DefaultRenderer

    def DefaultProgressCallback(self, progress):
        if self.progressCallback:
            self.progressCallback(None, progress)

    def SetProgressCallback(self, progressCallback):
        """ set function to be called when rendering progress updates """
        self.progressCallback = progressCallback

    def SetNumOrders(self, numorders):
        """ set total number orders of file to be rendered.  used to update progress bar. """
        self.numOrders = numorders

    def OnRenderFinished(self, fname, console=None):
        #print "OnRenderFinished"
        pass

    def WatchProgress(self, progressFile, fileprogress=None, progressCallback=None):
        """ get latest progress value from progress file and set progress bar accordingly"""
        try:
            f = open(progressFile)
        except IOError:
            f = None
            #print "no file", progressFile

        if not progressCallback:
            progressCallback = self.progressCallback

        if f:
            stuff = f.readlines()
            if stuff:
                lastline = string.strip(stuff[-1])
                progress = int(lastline)
                progress = int(100 * (float(progress) / float(self.numOrders)))
                if progress > 0 and progressCallback:
                    progressCallback(fileprogress, progress)
                #print "progress", progress

    def ProgressCallback(self, progress):
        self.progressCallback(None, progress)

    def CallbackAdapter(self, progress):
        if self.progressCallback:
            self.progressCallback(None, progress)

    def RenderInternal(self, itfile, outname, callback=None):

        #TODO: when using from batch mode, we have to make sure it's a valid it file first.


        # make sure output path exists
        filex.ensurePath(os.path.dirname(outname))

        if self.progressCallback:
            self.progressCallback(None, 0)            

        player = modplayer.getPlayerByCode(self.__renderer.getCode())
        #print ". got player", player

        # start renderer if not already started
        player.start(wx=0)

        newname = filex.baseAppend(itfile, "-render")
        newname = filex.pathjoin(filex.GetPath83(options.TempPath), os.path.basename(newname))

        fname, numorders, corrupt = it.makePlayableCopy(itfile, newname, settingsFunc=self.currentTrackSettingsFunc, checkValid=1)

        if corrupt:
            return 0
        
        self.SetNumOrders(numorders)

        amplify = self.amplify

        # set amplification with a normalization pass, if necessary
        if (self.amplifyOptions) and (not self.normalized) and (self.normalizeFile):
            # normalize according to self.normalizeFile
            print "-- Normalizing according to", self.normalizeFile
            amplify = -2    # -2 means to get normalization value without rendering
            newname = filex.pathjoin(filex.GetPath83(options.TempPath), os.path.basename(filex.baseAppend(self.normalizeFile, "-amp")))
            nf, numOrders = it.makePlayableCopy(self.normalizeFile, newname, settingsFunc=self.currentTrackSettingsFunc)

            if self.progressCallback:
                self.progressCallback(None, 0)


            # get normalization value
            try:
                #usefloat = self.usefloat
                usefloat = 0  # let's try normal method plz
                amplify = player.getNormalizationFromFile(nf, self.DefaultProgressCallback, interpolation=self.interpolation, samplerate=self.samplerate, usefloat=usefloat, volramp=self.volramp)
                print "-- Got amplification value", amplify
                self.normalized = 1
                self.normalize = 0  # don't normalize each file
                self.amplify = amplify

                if self.progressCallback:
                    self.progressCallback(None, 100)            
            except:
                print "-- Failed normalization of", nf
                self.normalized = 1
                self.normalize = 1  # each file will be normalized instead
                amplify = self.amplify
                            
        elif self.normalize:
            amplify = -1

        #BASS.renderFile(itfile, outname, callback=self.ProgressCallback, normalize=self.normalize)
        #print "info", self.samplerate, self.usefloat

        #print ". amplify is", amplify, self.normalize
        player.renderFile(fname, outname, callback=self.ProgressCallback, amp=amplify, normalize=self.normalize, interpolation=self.interpolation, samplerate=self.samplerate, usefloat=self.usefloat, volramp=self.volramp)

        if self.__renderer.usesPostNormalize() and self.normalize:
            #print ".. post normalizing", outname
            result = normalize.normalizeFile(outname, outname+".nrm", callback=self.CallbackAdapter)
            if result:
                os.remove(outname)
                os.rename(outname+".nrm", outname)
            else:
                os.remove(outname+".nrm")


    def Render(self, itfile, outname, callback=None):

        #print ". renderer", self.__renderer

        #if string.find(string.upper(self.__renderer.name), "BASS") > -1:
        if self.__renderer.supportsInternalRender():
            self.RenderInternal(itfile, outname, callback)
            return

        # filenames that results are output to from commandline programs.
        ampFile = filex.replaceExt(os.path.basename(self.__renderer.filename), ".amp")
        ampFile = filex.pathjoin(os.getcwd(), ampFile)
        
        progressFile = filex.replaceExt(self.__renderer.filename, ".txt")
            
        if self.progressCallback:
            self.progressCallback(None, 0)            

        fname = itfile

        newname = filex.baseAppend(fname, "-render")
        newname = filex.pathjoin(filex.GetPath83(options.TempPath), os.path.basename(newname))

        fname, numorders = it.makePlayableCopy(fname, newname, settingsFunc=self.currentTrackSettingsFunc)
        self.SetNumOrders(numorders)

        fname83 = filex.GetPath83(fname)

        amplify = self.amplify

        #print ".. normalizeFile", self.normalizeFile, self.normalized, self.amplifyOptions

        # set amplification with a normalization pass, if necessary
        if (self.amplifyOptions) and (not self.normalized) and (self.normalizeFile):
            # set full program path
            print "-- Getting amplify from", self.normalizeFile
            amplify = -2
            newname = filex.pathjoin(filex.GetPath83(options.TempPath), os.path.basename(filex.baseAppend(self.normalizeFile, "-amp")))
            nf, numo = it.makePlayableCopy(self.normalizeFile, newname, settingsFunc=self.currentTrackSettingsFunc)
            nf83 = filex.GetPath83(nf)

            fpp = self.__renderer.getCommandLine(options.ToolsPath, nf83, normalize=1, getNormalize=1, interpolation=self.interpolation, sampleRate=self.samplerate)
            #fpp = self.Renderer + " " + nf83 + " " + nf83 + " " + str(amplify)
            filex.remove(ampFile)

            if self.progressCallback:
                self.progressCallback(None, 0)
            progressFile = os.path.basename(progressFile)
            progressWatcher = threadx.LoopThread(self.WatchProgress, (progressFile,None,callback))
            progressWatcher.setSleepTime(PROGRESS_SLEEPTIME)
            progressWatcher.start()

            try:

                processx.RunSimpleProcess(fpp)
            except:
                print "-- Error while executing", fpp
                traceback.print_exc()

            progressWatcher.stop()
            if self.progressCallback:
                self.progressCallback(None, 100)            

                
            # now get amplify from basswav.amp
            if os.path.exists(ampFile):
                ampf = open(ampFile, "r")
                ampst = string.strip(ampf.readlines()[0])
                amp = int(ampst)
                #print "amp set to", amp

                self.amplify = amp
                amplify = amp
                self.normalized = 1
                self.normalize = 0
                print "-- Setting amplification to", amplify
            else:
                print "-- Couldn't find", ampFile
                self.normalized = 1
                self.normalize = 1  # each file will be normalized instead
                amplify = self.amplify
                #print "set amplify to", amplify
            
        elif self.normalize:
            amplify = -1

        filex.ensurePath(os.path.dirname(outname))

        progpath = self.__renderer.filename
        #print "!! progpath is", progpath

        progressFile = os.path.basename(progressFile)
        try:
            filex.remove(progressFile)
        except:
            pass
        
        # use filex.GetPath83 to convert each path to 8.3 format.  otherwise directories with spaces won't work.
        outname = filex.pathjoin( filex.GetPath83(os.path.dirname(outname)) , os.path.basename(outname) )

        # mikmod:
        #fullprogpath = filex.GetPath83(progpath) + " " + fname83 + " " + outname + " " + str(amplify)

        fullprogpath = self.__renderer.getCommandLine(options.ToolsPath, fname83, outname, normalize=self.normalize, volume=amplify, interpolation=self.interpolation, sampleRate=self.samplerate)
        #print ".. fpp", fullprogpath

        # run progress watcher thread (watches progress text file and reports progress to progress bar)
        progressWatcher = threadx.LoopThread(self.WatchProgress, (progressFile,))
        progressWatcher.setSleepTime(PROGRESS_SLEEPTIME)
        progressWatcher.start()

        # no thread necessary, this will be called from a thread
        try:
            processx.RunSimpleProcess(fullprogpath)
        except:
            print "!! Error while executing", fullprogpath
            traceback.print_exc()
            
        # if we pass it the callback, output from the piped command will be sent to the callback (ie, appear in the listbox display)
        # processx.PipeSimpleCommand(fullprogpath, callback)

        # now render has finished
        progressWatcher.stop()
        self.OnRenderFinished(outname, None)
        if self.progressCallback:
            self.progressCallback(None, 100)            

        try:
            #pass
            filex.remove(progressFile)
        except:
            pass

        if self.__renderer.usesPostNormalize() and self.normalize:
            #print ".. post normalizing", outname
            normalize.normalizeFile(outname, outname+".nrm", callback=self.CallbackAdapter)
            #print ".. done normalize"
            os.remove(outname)
            #print ".. done remove"
            os.rename(outname+".nrm", outname)
            #print ".. done rename"


    
    def ProcessFiles(self, callback=None):

        #print "rendering filelist", self.filelist

        processed = []
        errors = []
        
        idx = 0
        running = 1

        while (running) and (idx < len(self.filelist)):

            try:
                itfile = self.filelist[idx]

                if self.__dict__.has_key("outfile") and self.outfile:
                    outname, ignore = self.outfile, 0
                    #print "-1", outname
                else:
                    outname, ignore = self.GetOutputFilename(itfile, ".wav", checkIgnore=1)
                    #print "-2", outname
                if outname and not ignore:
                    # if outname is valid, do the processing and save to it
                    filex.ensurePath(os.path.dirname(outname))
                    print "-- Rendering", itfile, "to", outname
                    try:
                        #TODO: set numorders
                        self.Render(itfile, outname, callback)
                    except:
                        #print "!! o nos!"
                        traceback.print_exc()
                        errors.append(outname)
                    
                # calculate overall progress through filelist, to be passed to the callback
                progress = (float(idx) / float(len(self.filelist))) * 100
                progress = int(progress)
                
                if outname and callback:
                    running = apply(callback, (outname, progress))

            except:
                exit = apply(sys.excepthook, sys.exc_info(), {'inthread':1})
                if exit:
                    running = 0

            idx = idx + 1



        #print "done rendering", idx            

        if len(errors) > 0:
            print "Errors occured while trying to render these files:", errors
        return processed, errors

