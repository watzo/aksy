
from postmod_globals import *   # accessed by external modules

import postmod_globals

import shutil

from options import *
import filex


import postmod_icons as icons
import postmod_menus as menus
import postmod_images as images



def CleanBackups():
    #TODO: implement file threshold
    path = options.BackupPath
    threshold = options.BackupsDiskThreshold
    BackupsFileThreshold = options.BackupsFileThreshold

    #print "cleaned backups"    
    #print filex.delBackupsThreshold(path, threshold, "*.it")
    filex.delBackupsThreshold(path, threshold, "*.it")

def CleanTemp():
    shutil.rmtree(options.TempPath, 1)
    filex.ensurePath(options.TempPath)

def CleanLogs():
    if postmod_globals.VERSIONID != "DEV":
        filex.truncateLog("postmod.log", 500000)

def Cleanup():
    CleanTemp()
    CleanLogs()


def Toolbar(index):
    return images.__dict__["getToolbar1_" + str(index) + "Bitmap"]()

import postmod_wdr
postmod_wdr.Toolbar1 = Toolbar
