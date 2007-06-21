
#TODO: review entire thread system

import threading, time, sys


class GenericThread(threading.Thread):
    """GenericThread provides a generic threading mechanism, with optional end of thread callback."""
    def __init__(self, func, args=(), kwargs={}, postfunc=None, postargs=(), postkwargs={}, debug=0, resultCallback=None):
        """
        func - the function that will be called when the main thread begins.
        args - arguments to func, default empty
        kwargs - kwargs to func, default empty
        postfunc - the function that will be called when thread execution ends, default None
        postargs - arguments to postfunc, default empty
        postkwargs - kwargs to postfunc, default empty
        resultfunc - callback to send the results from func, default None. called BEFORE postfunc
        """

        #print "!!-- init thread", func, args, kwargs
        
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.postfunc = postfunc
        self.postargs = postargs
        self.postkwargs = postkwargs
        self.debug = 0
        self.resultfunc = resultCallback
        threading.Thread.__init__(self)
        
    def run(self):
        result = None
        
        try:
            if self.debug:
                print "Thread %s starts" % (self.getName(),)
                pass

            if self.debug:
                print "running", self.func, self.args, self.kwargs
            result = self.func(*self.args, **self.kwargs)

            if self.debug:
                print "%s ends" % (self.getName(),)
                pass

        except:
            # we have to call sys.excepthook explicitly, otherwise it doesn't normally work within a thread.
            sys.excepthook(*sys.exc_info())

        try:
            if self.resultfunc:
                self.resultfunc(result)

            if self.postfunc:
                self.postfunc(*self.postargs, **self.postkwargs)
                
        except:
            sys.excepthook(*sys.exc_info())




class LoopThread(GenericThread):

    """LoopThread is like GenericThread, but it repeatedly runs the desired function, sleeping for the specified time between
        function calls.  You must call LoopThread.stop() to stop it.  This will stop after the currently executing function
        completes. """

    def __init__(self, *args, **kwargs):
        GenericThread.__init__(self, *args, **kwargs)        
        self.sleeptime = .5
        self.running = 1

    def setSleepTime(self, sleeptime):
        self.sleeptime = sleeptime
    
    def run(self):
        while self.running:
            try:
                self.func(*self.args, **self.kwargs)
                time.sleep(self.sleeptime)
                #print "looping", self.func, self.args, self.kwargs, self.sleeptime
            except:
                sys.excepthook(*sys.exc_info())
                

    def stop(self):
        self.running = 0



def runFunc(func, args=(), kwargs={}, postfunc=None, postargs=(), postkwargs={}):
    ut = GenericThread(func, args, kwargs, postfunc, postargs, postkwargs)
    ut.start()
    return ut

