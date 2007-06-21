
import sys, time

LOGSTDOUT = 1
SHOWSTDOUT = 1

class DebugOutput:
    def __init__(self, console, fname):
        self.console = console
        if LOGSTDOUT:
            try:
                self.fp = open(fname, "a")
                self.fp.write("\n----- POSTMOD LOG OPENED %s -----\n" % (str(time.ctime())))
                #self.fp.write(str(sys.argv) + "\n")
            except:
                self.fp = None

    def __del__(self):
        if LOGSTDOUT:
            try:
                self.fp.write("----- POSTMOD LOG CLOSED %s -----\n" % (str(time.ctime())))
                self.fp.close()
            except:
                pass


    def write(self, st):
        try:
            if LOGSTDOUT:
                self.fp.write(st)
                self.fp.flush()
        except:
            # oh well, this needs to be safe
            pass

        try:        
            if SHOWSTDOUT:
                self.console.write(st)
        except:
            # oh well, this needs to be safe
            pass


def init(fname="postmod.log"):
    debugoutput = DebugOutput(sys.stdout, fname)
    sys.stdout = debugoutput
    sys.stderr = debugoutput
    return debugoutput

