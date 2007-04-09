
# ALWAYS INCREASE CONFIG_VERSION WHEN NEW SETTINGS ARE ADDED

import sys, os, traceback, string, copy
import filex
import pathmemory, vstlib
from ConfigParser import ConfigParser
import regoptions

try:
    import cPickle as pickle
except:
    import pickle

import postmod_globals

APP_VERSION = postmod_globals.VERSIONID
# 1.04 config version is 5
CONFIG_VERSION = 8

EXPORTMODE_OVERWRITE = 1
EXPORTMODE_IGNORE = 2
EXPORTMODE_RENAME = 3

#print "isMainApp is", postmod_globals.isMainApp

DEFAULT_COLORS = {
    'emptyPatternName': (200,200,200),
    'defaultTrackName': (0,0,0),
    'soloTrackName': (0,0,255),
    'muteTrackName': (200,200,200)
    }    # values are 3-tuples R,G,B        


# try to get DefaultProgramPath from registry; otherwise, use DefaultProgramPath
DefaultProgramPath = None
try:
    DefaultProgramPath = regoptions.getInstallPath()
except:
    pass

if not DefaultProgramPath:
    DefaultProgramPath = os.getcwd()
else:
    #os.chdir(DefaultProgramPath)
    pass

if os.path.exists("c:\\it"):
    DefaultPath = "c:\\it"
    DefaultExportPath = filex.pathjoin(DefaultPath, "export")
else:
    DefaultPath = "c:\\"
    DefaultExportPath = filex.pathjoin(DefaultProgramPath, "export")
DefaultTempPath = filex.pathjoin(DefaultProgramPath, "temp")
DefaultBackupPath = filex.pathjoin(DefaultProgramPath, "backups")
DefaultToolsPath = filex.pathjoin(DefaultProgramPath, "tools")
DefaultBatchesPath = filex.pathjoin(DefaultProgramPath, "batches")
DefaultRenderPath = DefaultExportPath
DefaultDownloadPath = filex.pathjoin(DefaultProgramPath, "downloads")
DefaultPluginPath = filex.pathjoin(DefaultProgramPath, "plugins")

DefaultSampleVolume = 40
DefaultSongVolume = 100
DefaultSongAmp = 50

CONFIG_FILENAME = filex.pathjoin(DefaultProgramPath, "postmod.cfg")


def getProgramPath():
    global DefaultProgramPath
    return filex.GetPath83(DefaultProgramPath)

def getImagePath():
    return filex.GetPath83(filex.pathjoin(getProgramPath(), "images"))


class AppPreferences:
    def __init__(self):
        self.ProgramPath = DefaultProgramPath
        self.DefaultPath = DefaultPath
        self.ExportPath = DefaultExportPath
        self.TempPath = DefaultTempPath
        self.BackupPath = DefaultBackupPath
        self.ToolsPath = DefaultToolsPath
        self.BatchfilePath = DefaultBatchesPath
        self.DownloadPath = DefaultDownloadPath
        self.PluginPath = DefaultPluginPath

        self.VSTPaths = [vstlib.getVSTPath()]

        self.SongVolume = DefaultSongVolume
        self.SongAmp = DefaultSongAmp
        self.SampleVolume = DefaultSampleVolume

        self.LoopPatterns = 1
        self.LoopSamples = 0
        self.LoopSongs = 0
        self.UseInterpolation = 1

        self.WAVPath = ""
        self.RenderPath = self.ExportPath

        self.setDefaultRenderers()

        self.Tools = []

        self.Colors = {}

        self.ExternalPlayer = ""

        self.BackupsDiskThreshold = 20000000
        self.BackupsFileThreshold = 0

        self.AppVersion = APP_VERSION
        self.AppTitle = postmod_globals.TITLE
        #print "default AppVersion is", self.AppVersion
        self.ConfigVersion = CONFIG_VERSION
        self.FirstRun = 1

        self.CheckUpdates = 1        
        self.LiveDebug = 0

        self.UnfoldEmptyOrderLists = 1

        self.VersionNotifications = []        

        self.AudioDevice = "Default"
        self.AudioDeviceNum = -1
        self.UseExternalPlayer = 0

        self.RecentFiles = ["pumpkin.it"]
        self.MaxRecentFiles = 10

        self.DefaultRenderer = 0
        self.DefaultPlayer = 0
        

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None

    def param(self, key, defaultValue):
        """ensures key exists in AppPreferences.  does nothing if key already exists, adds it with defaultValue if it doesn't."""
        if not hasattr(self.__dict__, key):
            self.__dict__[key] = defaultValue

    def verifyPath(self, pathvar, default):
        if not os.path.exists(self.__dict__[pathvar]):
            self.__dict__[pathvar] = default

    def setDefaultRenderers(self):
        # have to do this to update previous installations.
        #self.DefaultRenderer = 0
        self.DefaultRenderProgram = filex.pathjoin(self.ToolsPath, "basswav.exe")
        self.Renderers = []
        self.Renderers.append(self.DefaultRenderProgram)
        self.Renderers.append(filex.pathjoin(self.ToolsPath, "dumbwav.exe"))
        self.Renderers.append(filex.pathjoin(self.ToolsPath, "mikwav.exe"))
        

    def initAfterLoad(self, fname=CONFIG_FILENAME):

        if not postmod_globals.isMainApp:
            return
        
        if self.AppVersion != APP_VERSION:
            # only update version if this is not the updater program (mfupdate.exe)
            if postmod_globals.isMainApp:
                print "-- Updating Application Version from", self.AppVersion, "to", APP_VERSION
                self.AppVersion = APP_VERSION
                self.save()

        if self.AppTitle != postmod_globals.TITLE:
            if postmod_globals.isMainApp:
                #print "!! updating title", postmod_globals.TITLE
                self.AppTitle = postmod_globals.TITLE
                self.save()

        self.verifyPath("ToolsPath", DefaultToolsPath)
        self.verifyPath("DownloadPath", DefaultDownloadPath)
        self.verifyPath("ProgramPath", DefaultProgramPath)
        self.verifyPath("DefaultPath", DefaultPath)
        self.verifyPath("ExportPath", DefaultExportPath)
        self.verifyPath("TempPath", DefaultTempPath)
        self.verifyPath("BackupPath", DefaultBackupPath)
        self.verifyPath("BatchfilePath", DefaultBatchesPath)
        self.verifyPath("PluginPath", DefaultPluginPath)

        self.setDefaultRenderers()

        for key, value in DEFAULT_COLORS.items():
            if key not in self.Colors:
                self.Colors[key] = value

        self.updatePathMemory()

        self.UseExternalPlayer = 0  # legacy


    def updatePathMemory(self):
        # set current pathmemory directories
        pathmemory.set("it", self.DefaultPath)
        pathmemory.set("itload", self.DefaultPath)
        pathmemory.set("itsave", self.DefaultPath)
        pathmemory.set("export", self.ExportPath)
        pathmemory.set("batch", self.BatchfilePath)
        pathmemory.set("wav", self.WAVPath)
        pathmemory.set("wavload", self.WAVPath)
        pathmemory.set("wavsave", self.WAVPath)
        pathmemory.set("render", self.RenderPath)
        

    def ensurePaths(self):
        # ensure paths exist (create if they don't)
        #TODO: dunno about this
        if not filex.ensurePath(self.DefaultPath):
            self.DefaultPath = DefaultPath
        if not filex.ensurePath(self.ExportPath):
            self.ExportPath = DefaultExportPath
        if not filex.ensurePath(self.TempPath):
            self.TempPath = DefaultTempPath
        if not filex.ensurePath(self.BackupPath):
            self.BackupPath = DefaultBackupPath
        if not filex.ensurePath(self.BatchfilePath):
            self.BatchfilePath = DefaultBatchesPath
        if not filex.ensurePath(self.RenderPath):
            self.RenderPath = DefaultRenderPath
        if not filex.ensurePath(self.DownloadPath):
            self.DownloadPath = DefaultDownloadPath
        if not filex.ensurePath(self.PluginPath):
            self.PluginPath = DefaultPluginPath

    def loadcfg(self, fname=CONFIG_FILENAME):
        try:
            cfg = ConfigParser()
            cfg.read([fname])
            print cfg.sections()
            settings = cfg.options("postmod")
            print settings
            for x in settings:
                self.__dict__[x] = cfg.get("postmod", x)
            return 1
        except:
            return 0

    def savecfg(self, fname=CONFIG_FILENAME):
        self.ensurePaths()

        cfg = ConfigParser()
        cfg.add_section("postmod")
        keys = self.__dict__.keys()
        for key in keys:
            cfg.set("postmod", key, self.__dict__[key])
        
        f = open(fname, "w")
        cfg.write(f)
        f.close()
        
    def save(self, fname=CONFIG_FILENAME):

        if not postmod_globals.isMainApp:
            return

        self.ensurePaths()

        # now save
        try:
            f = open(fname, "w")
            pickle.dump(self.__dict__, f)
            f.close()
            return 1
        except:
            return 0

    def load(self, fname=CONFIG_FILENAME):
        """loads keys gracefully (keys not present in loaded file will still remain afterwards)"""
        try:
            f = open(fname, "r")
            #self.__dict__ = pickle.load(f)
            try:
                thedict = pickle.load(f)
            except:
                print "-- Error loading config file", CONFIG_FILENAME
                traceback.print_exc()
                f.close()
                return 0
            f.close()
            for key in thedict.keys():
                self.__dict__[key] = thedict[key]
            self.initAfterLoad(fname)
            return 1
        except IOError:
            print "-- Error loading config file", CONFIG_FILENAME
            traceback.print_exc()
            return 0


    def addRecentFile(self, fname):
        if fname.find(options.TempPath.lower()) == -1:
            if fname in self.RecentFiles:
                self.RecentFiles.remove(fname)
            self.RecentFiles = [fname] + self.RecentFiles
            if len(self.RecentFiles) > self.MaxRecentFiles:
                self.RecentFiles = self.RecentFiles[:self.MaxRecentFiles]

    def getProgramPath(self):
        return getProgramPath()

    def getImagePath(self):
        return getImagePath()

            
                
options = AppPreferences()
if not options.load():
    print "-- Postmod config data failed to load"
    options.save()
    options.initAfterLoad()
else:
    pass
    #print "after load, appversion is", options.AppVersion

if options.ConfigVersion < CONFIG_VERSION:
    print "-- Updating config version from", options.ConfigVersion, "to", CONFIG_VERSION
    options.ConfigVersion = CONFIG_VERSION
    # because of the way we load, new attributes should already be present with defaults, so we can just save now.    
    options.save()
    options.initAfterLoad()


if __name__ == "__main__":
    options.load("\\dev\\postmod\\postmod.cfg")
    print options.wak
    print options.piddle
    print options.argh
    options.save("test.cfg")
    