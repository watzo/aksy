
from libmodplug2 import *
import observer, utilx

from options import *

# NOTES:
# modplug mixing occurs in fastmix.cpp, CreateStereoMix, in the block after // Do mixing
# doesn't store weird pan values to disable tracks

# basslib is used for playback
import time, traceback, weakref, os
import basslib, threadx, wavex, renderers

from ctypes import *


    

   
"""
enum _ModPlug_Flags
{
	MODPLUG_ENABLE_OVERSAMPLING     = 1 << 0,  /* Enable oversampling (*highly* recommended) */
	MODPLUG_ENABLE_NOISE_REDUCTION  = 1 << 1,  /* Enable noise reduction */
	MODPLUG_ENABLE_REVERB           = 1 << 2,  /* Enable reverb */
	MODPLUG_ENABLE_MEGABASS         = 1 << 3,  /* Enable megabass */
	MODPLUG_ENABLE_SURROUND         = 1 << 4   /* Enable surround sound. */
};

enum _ModPlug_ResamplingMode
{
	MODPLUG_RESAMPLE_NEAREST = 0,  /* No interpolation (very fast, extremely bad sound quality) */
	MODPLUG_RESAMPLE_LINEAR  = 1,  /* Linear interpolation (fast, good quality) */
	MODPLUG_RESAMPLE_SPLINE  = 2,  /* Cubic spline interpolation (high quality) */
	MODPLUG_RESAMPLE_FIR     = 3   /* 8-tap fir filter (extremely high quality) */
};

typedef struct _ModPlug_Settings
{
	int mFlags;  /* One or more of the MODPLUG_ENABLE_* flags above, bitwise-OR'ed */
	
	/* Note that ModPlug always decodes sound at 44100kHz, 32 bit, stereo and then
	 * down-mixes to the settings you choose. */
	int mChannels;       /* Number of channels - 1 for mono or 2 for stereo */
	int mBits;           /* Bits per sample - 8, 16, or 32 */
	int mFrequency;      /* Sampling rate - 11025, 22050, or 44100 */
	int mResamplingMode; /* One of MODPLUG_RESAMPLE_*, above */
	
	int mReverbDepth;    /* Reverb level 0(quiet)-100(loud)      */
	int mReverbDelay;    /* Reverb delay in ms, usually 40-200ms */
	int mBassAmount;     /* XBass level 0(quiet)-100(loud)       */
	int mBassRange;      /* XBass cutoff in Hz 10-100            */
	int mSurroundDepth;  /* Surround level 0(quiet)-100(heavy)   */
	int mSurroundDelay;  /* Surround delay in ms, usually 5-40ms */
	int mLoopCount;      /* Number of times to loop.  Zero prevents looping.
	                        -1 loops forever. */
} ModPlug_Settings;
"""


# set global settings with defaults
settings = ModPlug_Settings()
settings.mFlags = MODPLUG_ENABLE_OVERSAMPLING | MODPLUG_ENABLE_NOISE_REDUCTION
settings.mChannels = 2
settings.mBits = 16
settings.mFrequency = 44100
settings.mResamplingMode = MODPLUG_RESAMPLE_LINEAR
settings.mReverbDepth = 0
settings.mReverbDelay = 0
settings.mBassAmount = 0
settings.mBassRange = 0
settings.mSurroundDepth = 0
settings.mSurroundDelay = 0
settings.mLoopCount = 0

# global sample size
sampleSize = 0

DEFAULTSR = 44100

def GetSettings():
    return settings

#def GetSampleSize():
#    return sampleSize

import utilx

def UpdateSettings(updateBasicConfig=0):
    global settings, sampleSize

    #ModPlug_SetSettings(settings)

    
    if settings.mFlags & MODPLUG_ENABLE_REVERB:
        CSoundFile_SetReverbParameters(settings.mReverbDepth, settings.mReverbDelay)
    if settings.mFlags & MODPLUG_ENABLE_MEGABASS:
        CSoundFile_SetXBassParameters(settings.mBassAmount, settings.mBassRange)
    else:
        CSoundFile_SetXBassParameters(0, 0)

    if settings.mFlags & MODPLUG_ENABLE_SURROUND:
        CSoundFile_SetSurroundParameters(settings.mSurroundDepth, settings.mSurroundDelay)

    if updateBasicConfig:
        CSoundFile_SetWaveConfig(settings.mFrequency, settings.mBits, settings.mChannels)

        sampleSize = settings.mBits / 8 * settings.mChannels
        SetSampleSize(sampleSize)

    CSoundFile_SetWaveConfigEx(settings.mFlags & MODPLUG_ENABLE_SURROUND,
                               (settings.mFlags & MODPLUG_ENABLE_OVERSAMPLING),
                               settings.mFlags & MODPLUG_ENABLE_REVERB,
                               1,
                               settings.mFlags & MODPLUG_ENABLE_MEGABASS,
                               settings.mFlags & MODPLUG_ENABLE_NOISE_REDUCTION,
                               0)

    CSoundFile_SetResamplingMode(settings.mResamplingMode)    



#My Computer\HKEY_LOCAL_MACHINE\SOFTWARE\VST\VSTPluginsPath = C:\Program Files\Steinberg\VstPlugIns

class PluginManager:
    def __init__(self, paths=["C:\\Program Files\\Steinberg\\Vstplugins"]):
        self.paths = paths
        self.loaded = []
        self.__dlls = []

        # full pathname of dlls are keys, handles are values
        self.pluginHandles = {}

        # refcounts used for loadPlugin / removePlugin, with handles as keys
        self.refcounts = {}

        InitializePlugins()
        #self.loadPlugin("trimate")
        #self.loadPlugin("quadrafuzz")

        #dlls = self.getDLLs()
        #for d in dlls:
        #    if d.lower().find("spark") == -1:
        #        handle = self.loadPlugin(d)
        #        print "unloading", handle
        #        RemovePlugin(handle)

    def __del__(self):
        self.close()

    def scanDLLs(self):
        print ".. scanning DLLs"
        self.__dlls = []
        for path in self.paths:
            files = filex.dirtree(path, "*.dll")
            self.__dlls += files

    def getDLLs(self, rescan=0):
        if rescan or not self.__dlls:
            self.scanDLLs()
        return self.__dlls

    def removePlugin(self, handle):
        # don't remove if we still have refcounts
        if handle in self.refcounts:
            self.refcounts[handle] -= 1
            if self.refcounts[handle] > 0:
                return 0

        # remove from self.loaded and self.pluginHandles            
        if handle in self.pluginHandles.values():
            for key, value in self.pluginHandles.items():
                if handle == value:
                    del self.pluginHandles[key]
                    if key in self.loaded:
                        self.loaded.remove(key)

        # now actually remove the plugin
        RemovePlugin(handle)
        if handle in self.refcounts:
            del self.refcounts[handle]

        return 1
            
        
            
    def loadPlugin(self, fname):
        a = time.time()
        if not fname:
            return None
        if len(fname) < 4 or fname[-4:].lower() != ".dll":
            fname += ".dll"
        fullpath = None

        if os.path.exists(fname):
            fullpath = fname
        
        if not fullpath:
            for path in self.paths:
                if os.path.exists(filex.pathjoin(path, fname)):
                    fullpath = filex.pathjoin(path, fname)
                    break

        if not fullpath:
            # search subdirs
            print ".. searching for", fname
            files = self.getDLLs()
            for ff in files:
                if fname.lower() == os.path.basename(ff).lower():
                    fullpath = ff
                    break

        if not fullpath:
            print fname, "not found"
            return None

        print ".. loading plugin", fname, fullpath            
            
        if fullpath not in self.loaded:
            p = AddPlugin(fullpath)
            self.loaded.append(fullpath)
            self.pluginHandles[fullpath] = p
        else:
            p = self.pluginHandles[fullpath]
            print ".. already loaded", fname

        if p in self.refcounts:
            self.refcounts[p] += 1
        else:
            self.refcounts[p] = 1

        return p        

    def addPath(self, path):
        self.paths.append(path)

    def close(self):
        UninitializePlugins()
    

PLUGINMANAGER = None

def getPluginManager():
    return PLUGINMANAGER


class MODPLUGSettings:
    def __init__(self):
        self.sampleRate = 44100
        self.bitRate = 16
        self.interpolation = 0
        


ALLMUSICS = []

class MODPLUGMusic(CSoundFile, observer.Subject):
    def __init__(self, fname=None, noSamples=0):

        CSoundFile.__init__(self)
        observer.Subject.__init__(self)
        
        self.error = 0
        self.loaded = 0
        if fname:
            self.load(fname)

        self.trackVolumes = []

        self.notifier = None        

        self.loopStartOrder = 0
        self.loopStartRow = 0
        self.loopEndOrder = 0
        self.loopEndRow = 0
        self.loopSync = 0

        self.looping = 0

        self.position = 0, 0

        self.player = MODPLUG()

        #self.SetMasterVolume(512)

        global ALLMUSICS
        ALLMUSICS.append(self)

        self.trackVolumes = [64] * 64  # 64 = maximum number of tracks in an IT
        self.soloed = []    # list of currently soloed tracks
        self.muted = []


    def __call__(self):
        return self

    def __del__(self):
        #print "..deleting", self
        #if self.handle or self.notifier:
        self.stop()
        self.close()
        self.Destroy()

    def isActive(self):
        #print "active:", self.m_dwSongFlags, self.m_dwSongFlags & SONG_ENDREACHED
        return not (self.m_dwSongFlags & SONG_ENDREACHED)

    def setVolume(self, volume, adjustAGC=0):
        # scale from 1..100 to 1..128
        volume = int(volume / 100.0 * 128)
        return self.SetMasterVolume(volume * 2, adjustAGC)


    def setLoopPattern(self, pattern):
        CSoundFile.LoopPattern(self, pattern)
        self.looping = 1

    def setLoopOrder(self, order):
        self.setLoopPattern(self.GetOrder(order))
        
    
    def setLoopPoints(self, startOrder, startRow, endOrder, endRow):
        if self.loopSync:
            self.clearLoopPoints()
        self.loopSync = MusicSetLoop(self.handle, startOrder, startRow, endOrder, endRow)

    def clearLoopSync(self):
        if self.loopSync:
            BASS_ChannelRemoveSync(self.handle, self.loopSync)
            self.loopSync = 0
    clearLoopPoints = clearLoopSync

    def setPosition(self, order, row):
        #TODO: row
        self.SetCurrentOrder(order)


    loadFromString = CSoundFile.CreateFromString    #TODO: free first if needed.
            
    def load(self, fname, flags=0, offset=0, length=0, noSamples=0, floating=0, interpolation=None):

        #TODO: do i need to do anything if i was previously loaded? free anything?

        #print ".. mp loading", fname, utilx.showCallerInfo()

        self.handle = 0

        if self.loaded:
            self.free()

        data = file(fname, "rb").read()
        self.CreateFromString(data)

        self.loaded = 1
        self.startTime = 0  # playback start time

        #print "vols"
        #for i in range(10):
        #    print self.GetChannelVolume(i)

        #TODO: 32-bit?

        #print "setting repeat count"
        #self.SetRepeatCount(-1)

        self.setInterpolation(interpolation)

        #flags = flags | BASS_MUSIC_STOPBACK

        self.flags = flags
        
        #self.error = BASS_ErrorGetCode()
        #if self.error:
        #    print "-- BASS Load error, code", self.error

        #self.updateTrackVolumes()

        #for i in range(self.getNumTracks()):
        #    print "pan", i, self.getTrackPan(i)


        return self


    def free(self):
        self.stopNotifier()

        if self.handle:
            basslib.BASS.BASS_StreamFree(self.handle)
            self.handle = 0

        global ALLMUSICS
        if self in ALLMUSICS:
            ALLMUSICS.remove(self)
    
        #self.Destroy()
        #if self.handle in self.player.channels:
        #    self.player.channels.remove(self.handle)

    def close(self):
        #print "close", self.notifier
        self.stopNotifier()
        self.free()

    def stopNotifier(self):
        if self.notifier:
            self.notifier.stop()
            self.notifier = None

    def setFlags(self, flags):
        #TODO: does this mean anything?
        self.flags = flags

    def setInterpolation(self, state):
        # modplug interpolation can only be set globally, not per music,
        # but this will request the interpolation mode to be changed when playback
        # of this song begins.
        self.requestInterpolation = state

    def updateSettings(self):
        UpdateSettings(1)
        self.notify()
        
    def play(self, loop=0, volume=0, position=None, loopOrder=None, interpolation=1, loopPattern=None):
        # loopPattern takes precedence over loopOrder

        global settings

        self.stopNotifier()

        if self.requestInterpolation == None:
            self.requestInterpolation = interpolation


        if position:
            #TODO: make row work too
            #print "setting position order", position[0]
            self.SetCurrentOrder(position[0])

        self.looping = loop
        
        if loop:
            settings.mLoopCount = -1    # loop forever
        else:
            settings.mLoopCount = 0

        if self.requestInterpolation != None:
            #print "setting interpolation mode", interpolation
            settings.mResamplingMode = interpolation

        if volume:
            self.setVolume(volume)

        self.updateSettings()

        if loopPattern != None:
            self.LoopPattern(loopPattern)
            self.m_nNextRow = 0
            self.ResetTotalTickCount()
            self.looping = 1
        elif loopOrder != None:
            self.SetCurrentOrder(loopOrder)
            self.LoopPattern(self.GetOrder(loopOrder))
            self.m_nNextRow = 0
            self.ResetTotalTickCount()
            self.looping = 1
            
        #else:
        #    self.looping = 0

        #self.SetMasterVolume(256)
        #print "set to", self.GetMasterVolume()

        self.InitPlayer(1)

        #print "self", self
        global ALLMUSICS
        selfindex = ALLMUSICS.index(self)
        #b =  basslib.BASSEngine()
        #b.init()
        #print "init", b.initialized
        #TODO: create from bass engine
        self.handle = basslib.BASS.BASS_StreamCreate(settings.mFrequency, 2, 0, MODPLUGSTREAMPROCFUNC, selfindex)
        print "error", basslib.BASS.BASS_ErrorGetCode()
        print ".. stream", self.handle
        #basslib.BASS_SetConfig(basslib.BASS_CONFIG_BUFFER, 100) # 100 ms

        #basslib.BASS.BASS_StreamPlay(self.handle, 0, 0)
        basslib.BASS.BASS_ChannelPlay(self.handle, 0)

        self.error = basslib.BASS.BASS_ErrorGetCode()
        #if self.error:
        #    print "-- MODPLUG Playback Error:", self.error

        if self.error:
            print "-- MODPLUG Play error, code", self.error, "handle", self.handle


        #self.player.channels.append(self.handle)

        return self.handle
        



    def stop(self):        
        if self.handle:
            basslib.BASS.BASS_ChannelStop(self.handle)

        if self.notifier:
            self.notifier.stop()
            self.notifier = None

    def rewind(self):
        self.SetCurrentPos(0)
            

    def pause(self):
        if self.handle:
            basslib.BASS.BASS_ChannelPause(self.handle)

    getTrackVolume = CSoundFile.GetChannelVolume
    setTrackVolume = CSoundFile.SetChannelVolume
    #getTrackPan = CSoundFile.GetChannelPan
    #setTrackPan = CSoundFile.SetChannelPan

    def setTrackPan(self, track, pan):
        CSoundFile.SetChannelPan(self, track, pan*4)

    def getTrackPan(self, track):
        return CSoundFile.GetChannelPan(self, track) / 4


    getName = CSoundFile.GetTitle

    def setTrackVolume(self, track, volume):
        #print ". libmp.setTrackVolume", self.getTrackVolume(track), "to", volume
        CSoundFile.SetChannelVolume(self, track, volume)


    getNumTracks = CSoundFile.GetNumChannels

    def getNumOrders(self):
        i = 0
        while self.GetOrder(i) < 255:
            i += 1
        return i
            


    def notifyPositionFunc(self, callback):
        try:
            if self.m_dwSongFlags & SONG_PATTERNLOOP:
                order = self.m_nPattern
            else:
                order = self.GetCurrentOrder()
            row = self.m_nRow
            #print "notify", order, row
            
            #TODO: how to check end?
            #if pos == 0xFFFFFFFF or not BASS_ChannelIsActive(channel):
            if not self.isActive():
                if self.looping:
                    self.rewind()
                else:
                    self.stopNotifier()
                return
                    
            seconds = int(time.time()) - self.startTime
            callback(order, row, seconds)
        except:
            traceback.print_exc()
            #print "stopping notifier"
            self.stopNotifier()

        

    def notifyPosition(self, callback, freq=0.3):
        if self.notifier:
            self.notifier.stop()

        self.startTime = int(time.time())
        #TODO: delete startTimes when not needed anymore
        lt = threadx.LoopThread(self.notifyPositionFunc, (callback,))
        lt.setSleepTime(freq)
        lt.start()
        self.notifier = lt


    # LIVE PLAYBACK

    def setOrderList(self, orders):
        for i, o in enumerate(orders):
            if o == "END":
                o = 255
            self.SetOrder(i, o)

    def setTempo(self, tempo):
        if tempo:
            self.m_nMusicTempo = self.m_nDefaultTempo = tempo

    def setSpeed(self, speed):
        if speed:
            self.m_nMusicSpeed = self.m_nDefaultSpeed = speed

    def setGlobalVolume(self, volume, adjustAGC=0):
        self.m_nGlobalVolume = volume * 2
        self.SetMasterVolume(volume * 2, adjustAGC)

    def setMixingVolume(self, volume):
        self.m_nSongPreAmp = volume


    # MUTE/SOLO/VOLUME

    def setSoloedTracks(self, soloed):
        self.soloed = soloed

    def setMutedTracks(self, muted):
        self.muted = muted

    def soloTrack(self, track, append=1, toggle=1):
        #print "is it in", track, track in self.soloed
        if toggle and track in self.soloed:
            self.soloed.remove(track)
        elif append and track not in self.soloed:
            self.soloed.append(track)
        elif not append:
            self.soloed = [track]
        #if track in self.muted:
        #    self.muted.remove(track)
        self.setAllTrackVolumes()

    def soloTracks(self, tracks, append=1):
        for track in tracks:
            self.soloTrack(track, append)

    def isTrackMute(self, track):
        return track in self.muted

    def isTrackSolo(self, track):
        return track in self.soloed

    def muteTrack(self, track, toggle=0):
        # if it's soloed, just unsolo it
        if toggle and self.IsChannelMuted(track):
            self.UnmuteChannel(track)
            if track in self.muted:
                self.muted.remove(track)
        elif track in self.soloed:
            self.soloed.remove(track)
        else:
            self.MuteChannel(track)
            if track not in self.muted:
                self.muted.append(track)

    def unmuteTrack(self, track):
        if not self.soloed or track in self.soloed:
            self.UnmuteChannel(track)
            if track in self.muted:
                self.muted.remove(track)

    def toggleTrack(self, track):
        if self.IsChannelMuted(track):
            self.unmuteTrack(track)
        else:
            self.muteTrack(track)

    def toggleTracks(self, tracks):
        for track in tracks:
            self.toggleTrack(track)

    def muteTracks(self, tracks):
        for track in tracks:
            self.muteTrack(track, toggle=0)
            
    def unSoloTracks(self):
        # unsolo all tracks
        self.soloed = []
        self.setAllTrackVolumes()

    def unSoloTrack(self, track):
        if track in self.soloed:
            self.soloed.remove(track)
        self.setAllTrackVolumes()

    def unmuteTracks(self):
        # unmute all tracks
        self.muted = []
        self.setAllTrackVolumes()

    def resetTrackVolumes(self):
        # clear all solo and mute settings
        self.soloed = self.muted = []
        self.setAllTrackVolumes()

    def setAllTrackVolumes(self):
        # mute and unmute all tracks, taking solos and mutes into account
        # for solos, mod_document doesn't apply this to the it structure, just the modplug one,
        # so the mutes aren't saved with the file.

        #print "mpsatv"
        #print "!! soloed", self.soloed
        #print "!! muted", self.muted
        
        numTracks = self.getNumTracks()
        if self.soloed:
            for i in xrange(numTracks):
                if i in self.soloed:
                    self.UnmuteChannel(i)
                else:
                    self.MuteChannel(i)
        else:
            for i in xrange(numTracks):
                if i in self.muted:
                    self.MuteChannel(i)
                else:
                    self.UnmuteChannel(i)

    def getTrackName(self, track):
        name = "Track " + str(track+1)
        if track in self.soloed:
            name = "[" + name + "]"
        if self.IsChannelMuted(track):
            name = name + " - Mute"
        return name

        
        





Modplug = None    # global player instance    


# class MODPLUG is really just a replacement for the BASS player, that uses the
# modplug engine for rendering mod music.  everything else still uses the BASS engine.

from basslib import BASSEngine
#print "BASS", BASS

# notifies observers when playback parameters (samplerate, width, interpolation) change

class MODPLUG(BASSEngine, observer.Subject):

    __shared_state = {}    
    def __init__(self, samplerate=DEFAULTSR, init=0, start=0, device=-1):

        self.__dict__ = self.__shared_state
        self.startTimes = {}

        observer.Subject.__init__(self)

        if not hasattr(self, "did_init"):
            self.did_init = 1
            self.initialized = 0
            self.started = 0
            self.device = device
            self.initializedDevice = None
            self.initializedVolumes = 0

            self.mResamplingMode = 0

            self.channels = []
            
            self.music = None
            if init:
                self.init(samplerate)
            if start:
                self.start()

            self.watcher = None # watcher thread
            self.notifier = None

            global Modplug
            Modplug = self

            # init plugin manager
            global PLUGINMANAGER
            PLUGINMANAGER = PluginManager()

            
            

    def getRenderer(self):
        # an info record
        return renderers.getRenderer(0)

    def loadMusic(self, fname):
        music = MODPLUGMusic(fname=fname)
        return music
        
    def realtimeEditing(self):
        return 1

    def updateSettings(self):
        UpdateSettings(1)
        self.notify()

    def getSettings(self):
        return GetSettings()

    def init(self, samplerate=DEFAULTSR, wx=1, reinit=0):
        b = basslib.BASSEngine(device=options.AudioDeviceNum)
        if not samplerate:
            samplerate = b.getSampleRate()
        b.init(samplerate, wx, reinit)
        
        #settings.mChannels = 2
        #settings.mBits = 16

        #TODO:
        settings.mFrequency = samplerate
        settings.mResamplingMode = MODPLUG_RESAMPLE_NEAREST
        #settings.mFlags |= MODPLUG_ENABLE_REVERB
        #settings.mReverbDepth, settings.mReverbDelay = 5000, 5000
        self.updateSettings()

        self.initialized = 1
        if not self.initializedVolumes:
            #TODO: modplug volumes
            #BASS_SetGlobalVolumes(options.SongVolume,-1,-1)
            #BASS_SetGlobalVolumes(-1, options.SampleVolume,-1)
            self.initializedVolumes = 1

    def getName(self):
        return "Modplug 1.16"

    def getSettings(self):
        # samplerate, bitrate, interpolation mode
        #TODO: bitrate
        return settings.mFrequency, 16, settings.mResamplingMode

    def setSampleRate(self, samplerate):
        b = basslib.BASSEngine(device=options.AudioDeviceNum)

        if samplerate != b.getSampleRate() or samplerate != settings.mFrequency:
            #b.init(samplerate, wx=1, reinit=1)
            b.setSampleRate(samplerate)
                    
            settings.mFrequency = samplerate
            self.updateSettings()

    def setSampleWidth(self, samplewidth):
        #TODO
        self.updateSettings()

    def setInterpolation(self, mode=MODPLUG_RESAMPLE_NEAREST):
        if mode != self.mResamplingMode or mode != settings.mResamplingMode:
            self.mResamplingMode = mode
            settings.mResamplingMode = mode
            self.updateSettings()

    def getInterpolation(self):
        return settings.mResamplingMode
        


    def closeAllChannels(self, exclude=[]):
        global ALLMUSICS
        #print "CLOSING ALL CHANNELS", ALLMUSICS
        for music in ALLMUSICS:
            if music not in exclude:
                music.close()

    def stopAllChannels(self, exclude=[]):
        global ALLMUSICS
        #print "CLOSING ALL CHANNELS", ALLMUSICS
        for music in ALLMUSICS:
            if music not in exclude:
                music.stop()

    def getNormalizationAmp(self, channel, callback=None, rewind=1, usefloat=0):
        # first set amp to 100 using MusicSetAmplify (SetGlobalVolumes doesn't affect the mixing level)
        # Then decode the MOD block-by-block (without writing to disk). After decoding each block, check if there are 
        # any samples at 32767 or -32768 (ie. max level). If there are, reduce the amplification.

        if callback:
            callback(0)

        music = channel

        amplify = 100
        currentOrder = 0
        i = pos = 0

        if usefloat:
            dtype = "f"
            minval = 0.0
            maxval = 1.0
        else:
            dtype = "h"
            minval = -32768
            maxval = 32767

        BASS_MusicSetAmplify(channel, amplify)
        numOrders=BASS_MusicGetLength(channel, 0)

        curmax = 0


        while 1:

            cnt = music.Read(buf, 10000)
            st = music.BufferToString(buf, cnt*sampleSize)
            
            f.writeframes(st)
  
            pos = music.GetCurrentOrder()

            time.sleep(0.002)

            if not cnt:
                break



        while BASS_ChannelIsActive(channel):
            data = BASS_ChannelGetData(channel, "", 10000)
            #print "got", len(data)

            datan = array.array(dtype)
            datan.fromstring(data)

            if usefloat:
                if max(datan) > curmax:
                    curmax = max(datan)
                    #print "max", curmax

            if maxval in datan or minval in datan:
                amplify -= 1
                #print "setting amplify to", amplify
                BASS_MusicSetAmplify(channel, amplify)

            pos=BASS_ChannelGetPosition(channel);
            if (LOWORD(pos) != currentOrder):
                currentOrder = LOWORD(pos)

                progress = int((float(currentOrder) / numOrders) * 100)

                if callback:
                    callback(progress)


        if rewind:
            pass
            #TODO: will this work now?
            #print "rewinding"
            #BASS_ChannelSetPosition(channel, 0, 0)

        if callback:
            callback(100)

        #print "returning", amplify
        if usefloat:
            return curmax
        else:
            return amplify                

    def renderMPT(self, music, outfile, callback=None, normalize=1, amp=50, includenorm=1, samplerate=44100, usefloat=0):

        # renders to 24 bit, then converts to 16 bit on normalize process
        # i think the conversion happens in Normalize24BitBuffer

        oldVolume = music.GetMasterVolume()
        print "oldvolume", oldVolume
        oldRepeat = music.GetRepeatCount()
        music.gdwSoundSetup = music.gdwSoundSetup | SNDMIX_DIRECTTODISK # ignore CPU checks
        music.gdwSoundSetup |= SNDMIX_NOBACKWARDJUMPS

        music.gdwMixingFreq = samplerate
        music.dnBitsPerSample = bitrate
        music.gnChannels = 2    # num channels

        #if ((m_bNormalize) && (m_pWaveFormat->wBitsPerSample <= 16))
        if normalize:
            music.gnBitsPerSample = 24
            music.SetAGC(0)
            if oldVolume > 128:
                music.SetMasterVolume(128)
        else:
            # also if bitspersample is greater than 16, turn normalize off
            normalize = 0

        music.ResetChannels()        
        #CSoundFile::InitPlayer(TRUE); TODO
        music.SetRepeatCount(0)

        buf = music.GetBuffer(10000)

        # Process the conversion
        bytesPerSample = (music.gnBitsPerSample * music.gnChannels) / 8
        i = -1
        total = 0
        while 1:
            i += 1

            cnt = music.Read(buf, 10000)
            st = music.BufferToString(buf, cnt*sampleSize)
            if not cnt:
                break

            total += cnt
            if normalize:
                imax = cnt * 3 * music.gnChannels
                #for x=0; x < imax; x+=3:
                #    num = ((((buffer[i+2] << 8) + buffer[i+1]) << 8) + buffer[i]) << 8
                #    num = num / 256
                #    if num > lMax:
                #        lMax = 1
                #    if -num > lMax:
                #        lMax = -1
            elif format == WAVE_FORMAT_IEEE_FLOAT:
                    M2W_32ToFloat(buffer, cnt*(bytesPerSample>>2))

            #UINT lWrite = fwrite(buffer, 1, lRead*nBytesPerSample, f);
            #if (!lWrite) break;

        """
        if normalize:
            # now normalize with value gotten from lMax
            DWORD dwLength = datahdr.length;
            DWORD percent = 0xFF, dwPos, dwSize, dwCount;
            DWORD dwBitSize, dwOutPos;
                dwPos = dwOutPos = dwDataOffset;
            dwBitSize = m_pWaveFormat->wBitsPerSample / 8;
            datahdr.length = 0;
            ::SendMessage(progress, PBM_SETRANGE, 0, MAKELPARAM(0, 100));
            dwCount = dwLength;
            while (dwCount >= 3)
            {
                dwSize = (sizeof(buffer) / 3) * 3;
                if (dwSize > dwCount) dwSize = dwCount;
                fseek(f, dwPos, SEEK_SET);
                if (fread(buffer, 1, dwSize, f) != dwSize) break;
                CSoundFile::Normalize24BitBuffer(buffer, dwSize, lMax, dwBitSize);
                fseek(f, dwOutPos, SEEK_SET);
                datahdr.length += (dwSize/3)*dwBitSize;
                fwrite(buffer, 1, (dwSize/3)*dwBitSize, f);
                dwCount -= dwSize;
                dwPos += dwSize;
                dwOutPos += (dwSize * m_pWaveFormat->wBitsPerSample) / 24;
                UINT k = (UINT)( ((ULONGLONG)(dwLength - dwCount) * 100) / dwLength );
                if (k != percent)
                {
                    percent = k;
                    wsprintf(s, "Normalizing... (%d%%)", percent);
                    SetDlgItemText(IDC_TEXT1, s);
                    ::SendMessage(progress, PBM_SETPOS, percent, 0);
                }
            }
        }
        """



        



    def render(self, music, outfile, callback=None, normalize=1, amp=50, includenorm=1, samplerate=44100, usefloat=0):
        restorerate = 0

        if samplerate != settings.mFrequency:
            restorerate = settings.mFrequency
            self.init(samplerate, wx=0, reinit=1)

        if normalize:
            pass

        #TODO: set amp
        #BASS_MusicSetAmplify(channel, amp)
        
        numOrders = music.getNumOrders()

        currentOrder = 0
        f = wavex.open(outfile, "wb")
        f.setnchannels(2)
        if usefloat:
            f.setsampwidth(4)
            f.setformat(wavex.WAVE_FORMAT_IEEE_FLOAT)
        else:
            f.setsampwidth(2)

        f.setframerate(samplerate)        

        if callback:
            callback(0)

        buf = music.GetBuffer(10000)

        while 1:

            cnt = music.Read(buf, 10000)
            st = music.BufferToString(buf, cnt*sampleSize)
            
            f.writeframes(st)
  
            pos = music.GetCurrentOrder()
            if (pos != currentOrder):
                currentOrder = pos

                if normalize and includenorm:
                    progress = int(((float(currentOrder) / numOrders) * 100) / 2) + 50
                else:
                    progress = int((float(currentOrder) / numOrders) * 100)

                if callback:
                    callback(progress)

            time.sleep(0.002)

            if not cnt:
                break

        if callback:
            callback(100)

            

    def getNormalizationFromFile(self, fname, callback=None, interpolation=1, samplerate=DEFAULTSR, usefloat=0, restore=1, volramp=0):
        
        return 100

    def renderFile(self, fname, outname, callback=None, normalize=1, amp=50, interpolation=1, samplerate=DEFAULTSR, usefloat=0, volramp=0):

        restorerate = 0

        if samplerate != settings.mFrequency:
            restorerate = settings.mFrequency
            self.init(samplerate, wx=0, reinit=1)

        print "-- MODPLUG Rendering", fname, "to", outname


        if normalize:
            pass

        music = MODPLUGMusic(fname)
        music.SetAGC(1)
        music.SetMasterVolume(512, 1)
        #music.SetMasterVolume(21024, 1)
        music.SetAGC(1)

        #print "volumes", music.m_nGlobalVolume, music.m_nSongPreAmp

        #music.m_nSongPreAmp = 200
        #music.m_nGlobalVolume = 4096

        # m_nGlobalVolume is the song global volume * 2
        # m_nSongPreAmp is the mixing volume, it seems to have a minimal effect -


        #TODO: set options (float, agc, interpolation, samplerate)
            
        #print "calling render"
        self.render(music, outname, callback, normalize=0, amp=amp, samplerate=samplerate, usefloat=usefloat)

        if restorerate:
            self.init(restorerate, wx=0, reinit=1)



    def notifyPositionFunc(self, channel, callback):
        channel.notifyPositionFunc(callback)
        
    def notifyPosition(self, channel, callback, freq=0.3):
        channel.notifyPosition(callback, freq)


    def notifyChannelStop(self, channel, callback, freq=1):
        # calls specified function when channel stops playing.  uses watcher thread, checks every freq seconds.
        # should only be called after channel has started playing.

        if self.watcher:
            self.watcher.stop()
        
        lt = threadx.LoopThread(self.checkChannelActive, (channel, callback))
        lt.setSleepTime(freq)
        lt.start()
        self.watcher = lt

    def showVolumes(self, music):
        channels = 0
        while BASS_MusicGetChannelVol(music, channels) != -1:
            #print "vol", channels, BASS_MusicGetChannelVol(music, channels)
            channels += 1
        

    def numTracks(self, music):
        return music.getNumTracks()

    def soloTrack(self, music, track):
        for i in range(64):
            if i != track:
                BASS_MusicSetChannelVol(music, i, 0)

    def soloTracks(self, music, tracks):
        for i in range(64):
            if i not in tracks:
                BASS_MusicSetChannelVol(music, i, 0)
        

    def muteTrack(self, music, track):
        BASS_MusicSetChannelVol(music, track, 0)

    def muteTracks(self, music, tracks):
        for t in tracks:
            BASS_MusicSetChannelVol(music, t, 0)



def testrender(fname, outfile=None):
    if not outfile:
        outfile = "out.wav"
    import wavex, time, random

    #CreateFromString needs s#
    #BufferToString needs StringAndSize

    settings.mResamplingMode = MODPLUG_RESAMPLE_NEAREST
    UpdateSettings(1)
    print "sampleSize", sampleSize

    x = CSoundFile()
    data = file(fname, "rb").read()
    #print x.ReadITFromString(data)
    a = time.time()
    print "create", x.CreateFromString(data)
    print "loaded in", time.time() - a
    #print "up", lmp.UpdateSettings(1)
    print x

    print "xm", x.SaveXM("out.xm")

    #print "unused", x.DetectUnusedSamples()

    print x.GetNumPatterns(), x.GetNumSamples(), x.GetNumInstruments(), x.GetNumChannels()
    print x.GetCurrentOrder()
    #x.SetCurrentOrder(3)
    #print x.GetCurrentOrder()
    #print x.GetCurrentPos()
    #x.SetCurrentPos(100)
    print "new", x.GetCurrentPos()
    buf = x.GetBuffer(256)
    print buf
    #print len(x.BufferToString(buf))
    #out = open("out.wav", "wb")

    #NOTE: setting volume in ChnSettings[x].nVolume affects initial volume setting,
    # but not current mixer playback.
    # setting Chn[x].nGlobalVol seems to set it in the mixer.

    print "chan settings"
    print x.GetChannelVolume(0), x.GetChannelVolume(1)
    x.SetChannelVolume(0, 10)
    print x.GetChannelVolume(0), x.GetChannelVolume(1)
    print

    print "xm", x.SaveIT("out.it")
    

    write = 1

    print "order", x.Order, len(x.Order)
    print "maxord", x.m_nMaxOrderPosition

    lpos = -1
    lorder = -1

    #x.SetMasterVolume(512, 0)
    x.SetAGC(1)
    #x.ResetAGC()

    #x.m_nSongPreAmp = 10
    print "preamp", x.m_nSongPreAmp
    print "master, global", x.m_nMasterVolume, x.m_nGlobalVolume
    # m_nGlobalVolume is the song global volume * 2
    # m_nSongPreAmp is the mixing volume, it seems to have a minimal effect -
    # low values result in lower volume, but max value is nowhere near maximum volume

    # turning AGC off and using default global volume can result in very low output -
    # see bal_01.it

    # modplug uses it pan * 4 (0..256) instead of (0..64)

    # i think recommended settings will be AGC, global volume 256 (128),
    # and then normalize output wav afterwards. maybe not AGC
        

    # if AGC is on, volume will always be normalized in a sense    

    #tr = raw_input()
    
    if write:

        out = wavex.open(outfile, "wb")
        out.setnchannels(settings.mChannels)
        out.setsampwidth(settings.mBits / 8)
        out.setframerate(settings.mFrequency)


        print "master", x.GetMasterVolume()

        print "writing"
        total = 0
        maxval = 0
        
        while 1:

            #x.SetChannelVolume(random.randrange(0,5), random.randrange(0, 128))


            cpos, corder = x.GetCurrentPos(), x.GetCurrentOrder()
            if cpos != lpos:
                #print "pos", cpos
                lpos = cpos
            if corder != lorder:
                print "ord", corder
                lorder = corder


            cnt = x.Read(buf, 256)
            st = x.BufferToString(buf, cnt*sampleSize)
            mv = x.GetBufferMaxValue(buf, cnt*sampleSize)

            if abs(mv) > abs(maxval):
                print "max", mv
                maxval = mv
            

            clip = x.DoesBufferClip(buf, cnt*sampleSize)
            if clip:
                print "CLIP"
                newvol = x.GetMasterVolume()-1
                print "newvol", newvol
                x.SetMasterVolume(newvol)
            out.writeframes(st)
            total += cnt
            #print cnt
            #print "pos", x.GetCurrentPos(), x.GetCurrentOrder()
            #print x.BufferToString(buf, 4000)
            if not cnt:
                break
            
        out.close()
        print total

def test1():
    import sys
    numargs = len(sys.argv)
    infile = sys.argv[1]
    outfile = None
    if numargs > 2:
        outfile = sys.argv[2]
    test(infile, outfile)

def test2():
    import sys
    UpdateSettings(1)

    mod=MODPLUGMusic(sys.argv[1])
    print mod
    print mod.GetTitle()
    b = basslib.BASSEngine()
    b.init(wx=0)
    b.start()

    print "mix"
    print mod.m_nMixChannels, mod.m_nMixStat, mod.m_dwSongFlags
    mod.play()
    print mod.m_nMixChannels, mod.m_nMixStat, mod.m_dwSongFlags
    #x = raw_input()


    import time, random
    while 1:
        time.sleep(0.1)
        print mod.m_nMixChannels, mod.m_nMixStat, mod.m_nBufferCount, mod.m_dwSongFlags
        mod.m_nMusicTempo = random.randrange(50, 200)
        mod.m_nMusicSpeed = random.randrange(1, 10)
        #CSoundFile_SetResamplingMode(random.randrange(0,4))
        #CSoundFile_SetWaveConfig(random.randrange(11025,44100), settings.mBits, settings.mChannels)
        #CSoundFile_SetWaveConfig(random.randrange(8000,96000), settings.mBits, settings.mChannels)
        print ".."
        
    #x = raw_input()


def testyikes():
    import sys
    UpdateSettings(1)

    mod=MODPLUGMusic(sys.argv[1])
    print mod
    print mod.GetTitle()
    b = basslib.BASSEngine()
    b.init(wx=0)
    b.start()

    mod.play()

    import time, random
    while 1:
        #time.sleep(0.1)
        CSoundFile_SetResamplingMode(random.randrange(0,4))
        #CSoundFile_SetWaveConfig(random.randrange(11025,44100), settings.mBits, settings.mChannels)
        CSoundFile_SetWaveConfig(random.randrange(11025,44100), settings.mBits, settings.mChannels)
        print ".."
        
    #x = raw_input()


"""
DWORD CALLBACK ModplugStreamProc(
    Bass::HSTREAM handle,
    void *buffer,
    DWORD length,
    DWORD user
) {
    // user should be CSoundFile*
    return (((CSoundFile*)(user))->Read(buffer, length)) * gSampleSize;
};
"""

def ModplugStreamProc(handle, buffer, length, user):
    global ALLMUSICS, sampleSize
    mod = ALLMUSICS[user]

    #print "user", user, mod

    return mod.Read(buffer, length) * sampleSize
    

MODPLUGSTREAMPROCFUNC = basslib.STREAMPROC(ModplugStreamProc)


    

if __name__ == "__main__":
    test2()
    import sys
    #testrender(sys.argv[1])
    
