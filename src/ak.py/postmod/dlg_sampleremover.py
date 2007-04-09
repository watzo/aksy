
import threading, sys
from dlg_generic_processor import *
from generic_processor import *

class ITSampleRemover(GenericProcessor):
    def Preview(self, *args, **kwargs):
        #print "ITSampleRemover.Preview", args
        pass

    def ProcessFiles(self, callback=None):
        processed = []
        errors = []
        
        idx = 0
        running = 1

        totalRemoved = 0        

        while (running) and (idx < len(self.filelist)):
            try:
                itfile = self.filelist[idx]

                outname, ignore = self.GetOutputFilename(itfile, ".it", checkIgnore=1)
                if outname and not ignore:
                    # if outname is valid, do the processing and save to it
                    filex.ensurePath(os.path.dirname(outname))
                    mod = None
                    try:
                        mod = it.ITModule(fname=itfile, unpack=0)
                    except:
                        errors.append("Failed to load " + itfile)
                        
                    success = 0
                    if mod:
                        try:
                            removed = mod.optimizeSamples()
                            #print "removed", removed
                            totalRemoved = totalRemoved + removed
                            success = 1
                        except:
                            errors.append("Failed to optimize " + itfile)
                    if success:
                        try:
                            #print "save to", outname
                            mod.save(outname, checkpack=1)
                        except:
                            errors.append("Failed to save " + itfile)
                    del mod
                
            except:
                exit = apply(sys.excepthook, sys.exc_info(), {'inthread':1})
                if exit:
                    running = 0


            # calculate overall progress through filelist, to be passed to the callback

            progress = (float(idx) / float(len(self.filelist))) * 100
            progress = int(progress)
            
            if outname and callback:
                running = apply(callback, (outname, progress))
            idx = idx + 1

            processed.append(outname)            

        if len(errors) > 0:
            print "Errors occured in these files while optimizing samples:", errors

        #print "total removed:", totalRemoved
            
        return processed, errors

        

class SampleRemoverThread(threading.Thread):
    def __init__(self, args=(), postfunc=None, postargs=()):
        self.args = args
        self.postfunc = postfunc
        self.postargs = postargs

        threading.Thread.__init__(self)

    def init(self):
        """ manual init method - because the subclassed __init__ might not be called """
        pass
        
        
    def run(self):
        try:
            #print "SampleRemoverThread %s starts" % (self.getName(),)
            #print "args", self.args
            processed, errors = ITSampleRemover.ProcessFiles(*self.args)
            kwargs={'results':(processed, errors)}
            self.postfunc(*self.postargs, **kwargs)
        except:
            apply(sys.excepthook, sys.exc_info())




class SampleRemoverDialog(GenericProcessorDialog):
    def __init__(self, *args, **kwargs):
        GenericProcessorDialog.__init__(self, *args, **kwargs)
        self.Config(titleBase="Remove Samples", titleData=self.GetTitle(), buttonLabel="Remove")
        self.GetUnfoldCheckbox().Show(0)

    def PrepareProcessor(self, filelist):
        GenericProcessorDialog.PrepareProcessor(self, filelist)
        # cast processor instance from GenericProcessor to ITSampleRemover
        self.processor.__class__ = ITSampleRemover
        #self.processor.init()

    def StartProcessThread(self):
        #print "SampleRemoverDialog.StartProcessThread"
        # start the processing thread
        self.processThread = SampleRemoverThread(args=(self.processor, self.ProcessCallback), postfunc=self.PostProcess, postargs=())
        self.processRunning = 1
        self.processThread.start()

