
import threading, sys, traceback
from dlg_generic_processor import *
from generic_processor import *

class ITUnfolder(GenericProcessor):
    def Preview(self, *args, **kwargs):
        #print "ITUnfolder.Preview", args
        pass

    def ProcessFiles(self, callback=None):
        processed = []
        errors = []
        
        idx = 0
        running = 1

        while (running) and (idx < len(self.filelist)):
            try:
                itfile = self.filelist[idx]

                outname, ignore = self.GetOutputFilename(itfile, ".it", checkIgnore=1)
                if outname and not ignore:
                    # if outname is valid, do the processing and save to it
                    filex.ensurePath(os.path.dirname(outname))
                    #print "unfolding", itfile, "to", outname
                    mod = None
                    try:
                        mod = it.ITModule(fname=itfile, unpack=0)
                    except:
                        errors.append("Failed to load " + itfile)

                    success = 0
                    if mod:
                        try:
                            mod.unfold()
                            success = 1
                        except:
                            traceback.print_exc()
                            errors.append("Failed to unfold " + itfile)
                    if success:
                        try:
                            mod.save(outname, checkpack=1)
                        except:
                            errors.append("Failed to save " + itfile)
                    del mod
            except:
                exit = sys.excepthook(*sys.exc_info(), **{'inthread':1})
                if exit:
                    running = 0

                
            # calculate overall progress through filelist, to be passed to the callback
            progress = (float(idx) / float(len(self.filelist))) * 100
            progress = int(progress)
            
            if outname and callback:
                running = callback(*(outname, progress))
            idx = idx + 1

            processed.append(outname)            

        if len(errors) > 0:
            print "Errors occured while attempting to unfold these files:", errors
        return processed, errors

        

class UnfolderThread(threading.Thread):
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
            #print "UnfolderThread %s starts" % (self.getName(),)
            #print "args", self.args
            processed, errors = ITUnfolder.ProcessFiles(*self.args)
            kwargs={'results':(processed, errors)}

            self.postfunc(*self.postargs, **kwargs)
        except:
            apply(sys.excepthook, sys.exc_info())




class UnfolderDialog(GenericProcessorDialog):
    def __init__(self, *args, **kwargs):
        GenericProcessorDialog.__init__(self, *args, **kwargs)
        self.Config(titleBase="Unfold", titleData=self.GetTitle(), buttonLabel="Unfold")
        self.GetUnfoldCheckbox().Show(0)

    def PrepareProcessor(self, filelist):
        GenericProcessorDialog.PrepareProcessor(self, filelist)
        # cast processor instance from GenericProcessor to ITUnfolder
        self.processor.__class__ = ITUnfolder
        #self.processor.init()

    def StartProcessThread(self):
        #print "UnfolderDialog.StartProcessThread"
        # start the processing thread
        self.processThread = UnfolderThread(args=(self.processor, self.ProcessCallback), postfunc=self.PostProcess, postargs=())
        self.processRunning = 1
        self.processThread.start()

