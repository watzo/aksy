
import win32pipe, win32process, win32event, win32con, os, string, time

def CreateSimpleProcess(commandPath, rect=None):
    si = win32process.STARTUPINFO()
    if rect:
        si.dwX, si.dwY, si.dwXSize, si.dwYSize = rect
        si.dwFlags = win32process.STARTF_USEPOSITION | win32process.STARTF_USESIZE

    pinfo = win32process.CreateProcess(
                            None, # AppName
                            commandPath, # command line
                            None,   # Process security
                            None,   # Thread security
                            0,      # Inherit handles?
                            win32process.NORMAL_PRIORITY_CLASS | win32con.CREATE_NO_WINDOW | win32con.DETACHED_PROCESS,
                            None,   # New environment
                            None,   # Current directory
                            si)     # startup info

    # info is tuple of (hProcess, hThread, processId, threadId)

    # return process handle
    return pinfo[0]


def RunSimpleProcess(commandPath, wait=1000, maxtries=None, rect=None):
    handle = CreateSimpleProcess(commandPath, rect)

    #hwnd = win32gui.FindWindow(None, "BASSWAV")
    #if hwnd:
        #win32api.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE, 0)
        #win32api.SendMessage(hwnd, win32con.WM_SHOWWINDOW, win32con.SW_HIDE, 0)

    loops = 0
    done = 0
    timedout = 0
    while not done:
        #print "waiting", wait, "for", maxtries
        rc = win32event.WaitForMultipleObjects([handle], 1, wait)
        if rc == win32event.WAIT_OBJECT_0:
            #print "process ended"
            done = 1
        loops = loops + 1
        if maxtries and loops >= maxtries:
            done = 1
            timedout = 1
            #print "timed out after", loops

    if timedout:
        # kill it!
        try:
            win32process.TerminateProcess(handle, 0)
            #print "stopped"
        except win32process.error:
            #print "no stop"
            # probably already stopped.
            pass

        
    


def SpawnSimpleCommand(commandPath, args=None):
    """
    runs command with spawnv.
    remember to convert any paths to 8.3 format, before passing it to this function.
    this is needed if any directories or files have spaces in them.
    """

    if not args:    
        splitpath = string.split(commandPath, " ")
        args = tuple(splitpath)
        commandPath = splitpath[0]

    #print "running", splitpath[0], args
    result = os.spawnv(os.P_WAIT, splitpath[0], args)

    """
    print "running", commandPath
    win32api.WinExec(commandPath, 0)
    """
    
    #print "done running"
    time.sleep(0.5)
    return result



def PipeSimpleCommand(commandPath, callback=None):
    """ remember to convert any paths to 8.3 format first.  this is needed if any directories or files have spaces in them.
        I don't think pipes (os.popen, win32pipe) are very reliable on Windows.  f.close causes IOError sometimes
        (possible workarounds are implemented here).  But also, w9xpopen has crashed.
    """

    #print "running", commandPath
    stuff = ""
    
    f = win32pipe.popen(commandPath, "r")
    for x in f.readlines():
        #print x
        stuff += x
        if callback:
            apply(callback, (string.strip(x),))

    stuff = None
    try:
        #f.flush()
        if not f.closed:
            time.sleep(0.1)
            stuff = f.close()
        else:
            #print "already closed"
            pass
            
    except IOError:
        print "-- Warning: IOError on pipe close"

    time.sleep(0.25)
    return stuff        
    

def show(st):
    print st

if __name__ == "__main__":
    PipeSimpleCommand(r"D:\DEV\POSTMOD\TOOLS\BASSWAV.EXE D:\DEV\POSTMOD\TEMP.IT C:\IT\Fish.wav", show)
    
    