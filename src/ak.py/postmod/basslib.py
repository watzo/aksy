#from options import *
#import renderers, observer
import observer

class BasslibOptions:
    def __init__(self):
        self.SongVolume = 100
        self.SampleVolume = 100

options = BasslibOptions()


from pybass import *

import wave, array, time, struct, random
#import threadx, wavex, wxx

from ctypes import *

#-------------- FUNCTION WRAPPERS ------------------

#SetInstrumentSyncFunc = bassc.SetInstrumentSyncFunc

#MusicSetInstrumentSync = bassc.MusicSetInstrumentSync

#MusicSetLoop = bassc.MusicSetLoop

#MusicLoopOrder = bassc.MusicLoopOrder


DEFAULTSR = 44100
BITRATE = 16    # default bitrate of module.  new files are loaded based on this setting (if no explicit bitrate is passed)


class SamplePlayer:
    def __init__(self, engine=None):
        if engine:
            self.engine = engine
        else:
            self.engine = BASS()

        self.filenames = []
        self.samples = {}   # keys are filenames, values are loaded samples
        self.looping = []
        self.channels = []
        self.max = 10

    def playSample(self, fname, freq=-1, volume=-1, pan=-101, loop=0, startpos=0):
        #dprint "fname", fname
        if fname in self.samples:
            sample = self.samples[fname]
        else:
            sample = self.engine.loadSample(fname, max=self.max)
            self.samples[fname] = sample
            
        self.engine.playSample(sample, freq, volume, pan, loop, startpos)
        if loop:
            self.looping.append(sample)        

    def stop(self):
        for sample in self.samples.values():
            self.engine.stopSample(sample)
        self.looping = []

    def close(self):
        self.stop()
        for sample in self.samples.values():
            self.engine.freeSample(sample)

    def stopLooping(self):
        # stop any looping samples
        for sample in self.looping:
            self.engine.stopSample(sample)
        self.looping = []
            


def MAKELONG(lo, hi):
    lo = struct.pack("<H", lo)
    hi = struct.pack("<H", hi)
    num = struct.unpack("<i", lo+hi)[0]
    return num

def LOWORD(num):
    lo = struct.unpack("<H", struct.pack("<H", num))[0]
    return lo
    
def HIWORD(num):
    #lo = LOWORD(num)
    #hi = num-lo
    dat = struct.pack("<i", num)
    dat = dat[2:]
    hi = struct.unpack("<H", dat)[0]
    return hi

FXLIST = [BASS_FX_CHORUS, BASS_FX_COMPRESSOR, BASS_FX_DISTORTION, BASS_FX_ECHO, BASS_FX_FLANGER, BASS_FX_GARGLE, BASS_FX_I3DL2REVERB, BASS_FX_PARAMEQ, BASS_FX_REVERB]


class BASSChannel:
    def __init__(self):
        self.handle = 0
        self.error = 0

    def bytes2Seconds(self, pos):
        result = BASS.BASS_ChannelBytes2Seconds(self.handle, pos)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def seconds2Bytes(self, pos):
        result = BASS.BASS_ChannelSeconds2Bytes(self.handle, pos)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def getData(self, length):
        #data = BASS.BASS_ChannelGetData(self.handle, "", length)
        data = ChannelGetData(self.handle, length)
        self.error = BASS.BASS_ErrorGetCode()
        return data

    def getFlags(self):
        flags = BASS.BASS_ChannelGetFlags(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return flags

    def getLevel(self):
        level = BASS.BASS_ChannelGetLevel(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return level

    def getPosition(self):
        pos = BASS.BASS_ChannelGetPosition(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return pos

    def isActive(self):
        return BASS.BASS_ChannelIsActive(self.handle)

    def isSliding(self):
        return BASS.BASS_ChannelIsSliding(self.handle)

    def pause(self):
        result = BASS.BASS_ChannelPause(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def resume(self):
        result = BASS.BASS_ChannelResume(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def stop(self):
        result = BASS.BASS_ChannelStop(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def removeDSP(self, dsp):
        result = BASS.BASS_ChannelRemoveDSP(self.handle, dsp)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def removeFX(self, fx):
        result = BASS.BASS_ChannelRemoveFX(self.handle, fx)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def removeLink(self, channel):
        result = BASS.BASS_ChannelRemoveLink(self.handle, channel)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def removeSync(self, sync):
        result = BASS.BASS_ChannelRemoveSync(self.handle, sync)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setAttributes(self, freq=-1, volume=-1, pan=-101):
        result = BASS.BASS_ChannelSetAttributes(self.handle, freq, volume, pan)
        self.error = BASS.BASS_ErrorGetCode()
        return result
        
    def setVolume(self, volume):
        # 0 - 100
        result = BASS.BASS_ChannelSetAttributes(self.handle, -1, volume, -101)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setFreq(self, freq):
        # 100 - 100000
        result = BASS.BASS_ChannelSetAttributes(self.handle, freq, -1, -101)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setPan(self, pan):
        # left -100 : 100 right
        result = BASS.BASS_ChannelSetAttributes(self.handle, -1, -1, pan)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def slide(self, freq=-1, volume=-01, pan=-101, time=0):
        # time in ms
        result = BASS.BASS_ChannelSlideAttributes(self.handle, freq, volume, pan, time)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setFX(self, fxtype):
        result = BASS.BASS_ChannelSetFX(self.handle, fxtype)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setLink(self, channel):
        result = BASS.BASS_ChannelSetLink(self.handle, channel)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setPosition(self, pos):
        result = BASS.BASS_ChannelSetPosition(self.handle, pos)
        self.error = BASS.BASS_ErrorGetCode()
        return result

        
        
        
    


def instrumentSync(instrument, note=0, volume=0):
    print "i got called"
    print "python:", instrument, note, volume


class BASSMusic:
    def __init__(self, fname=None, noSamples=0):
        self.handle = 0
        self.error = 0
        self.notifier = None        

        if fname:
            self.load(fname, noSamples=noSamples)

        self.trackVolumes = []


        self.loopStartOrder = 0
        self.loopStartRow = 0
        self.loopEndOrder = 0
        self.loopEndRow = 0
        self.loopSync = 0

        self.position = 0, 0

        self.player = BASSEngine()        

        # these are playback engine volumes for each track, 0-100, not related to the IT channel volumes.
        # these DO NOT change when tracks are muted or soloed.
        self.trackVolumes = [64] * 64  # 64 = maximum number of tracks in an IT
        self.soloed = []    # list of currently soloed tracks
        self.muted = []     # list of currently muted tracks


    def __call__(self):
        return self.handle

    def __del__(self):
        if self.handle or self.notifier:
            self.close()

    def isActive(self):
        return BASS.BASS_ChannelIsActive(self.handle)

    def setVolume(self, volume):
        BASS.BASS_ChannelSetAttributes(self.handle, -1, volume, -1)

    def setLoopOrder(self, order):
        if self.loopSync:
            self.clearLoopSync()
        self.loopSync = MusicLoopOrder(order)
        #dprint ".. looped order", order, self.loopSync

    def setLoopPoints(self, startOrder, startRow, endOrder, endRow):
        if self.loopSync:
            self.clearLoopPoints()
        self.loopSync = MusicSetLoop(self.handle, startOrder, startRow, endOrder, endRow)

    def clearLoopSync(self):
        if self.loopSync:
            BASS.BASS_ChannelRemoveSync(self.handle, self.loopSync)
            self.loopSync = 0
    clearLoopPoints = clearLoopSync

    def setPosition(self, order, row):
        BASS.BASS_ChannelSetPosition(self.handle, MAKELONG(order, row))
        self.position = order, row
            
    def load(self, fname, flags=BASS_MUSIC_FX, offset=0, length=0, noSamples=0, floating=None, interpolation=1, samplerate=0, volramp=1):
    #def load(self, fname, flags=0, offset=0, length=0, noSamples=0):
        # flags = BASS_MUSIC_FX

        if floating == None:
            global BITRATE
            floating = (BITRATE == 32)
        
        if self.handle:
            #dprint "bm freeing for new load", self.handle
            self.free()

        if floating:
            flags = 0
            flags = flags | BASS_MUSIC_FLOAT

        if not interpolation:
            flags = flags | BASS_MUSIC_NONINTER

        if noSamples:
            flags = flags | BASS_MUSIC_NOSAMPLE

        if volramp == 1:
            flags = flags | BASS_MUSIC_RAMPS
        elif volramp == 2:
            flags = flags | BASS_MUSIC_RAMP

        flags = flags | BASS_MUSIC_STOPBACK

        self.flags = flags

        self.handle = BASS.BASS_MusicLoad(0, fname, offset, length, flags, samplerate)
        #dprint ".. loaded handle", self.handle, BASS.BASS_ErrorGetCode()

        #SetInstrumentSyncFunc(instrumentSync)
        #MusicSetInstrumentSync(self.handle, 1, -1)
        #MusicSetInstrumentSync(self.handle, 2, -1)
        #MusicSetInstrumentSync(self.handle, 3, -1)
        #MusicSetInstrumentSync(self.handle, 4, -1)
        
        #dprint self.handle
        #dprint "bm loaded", self.handle, fname
        #dprint self.handle
        self.error = BASS.BASS_ErrorGetCode()
        if self.error:
            print "-- BASS Load error, code", self.error

        self.updateTrackVolumes()
        
        return self.handle

    def free(self):
        #dprint "bm freeing", self.handle
        BASS.BASS_MusicFree(self.handle)
        if self.handle in self.player.channels:
            self.player.channels.remove(self.handle)
        self.handle = 0

    def close(self):
        #dprint "bm closing", self.handle
        self.free()
        if self.notifier:
            self.notifier.stop()

    def setFlags(self, flags):
        BASS.BASS_ChannelSetFlags(self.handle, flags)
        self.flags = flags

    def setInterpolation(self, state):
        state = not state
        if (self.flags & BASS_MUSIC_NONINTER):
            if not state:
                self.flags = self.flags ^ BASS_MUSIC_NONINTER
        else:
            if state:
                self.flags = self.flags | BASS_MUSIC_NONINTER

    def setVolumeRamp(self, volramp):
        # 0=none, 1=BASS_MUSIC_RAMPS, 2=BASS_MUSIC_RAMP
        flags = self.flags
        if flags & BASS_MUSIC_RAMP:
            flags = flags ^ BASS_MUSIC_RAMP
        elif flags & BASS_MUSIC_RAMPS:
            flags = flags ^ BASS_MUSIC_RAMPS

        if volramp == 1:
            flags = flags | BASS_MUSIC_RAMPS
        elif volramp == 2:
            flags = flags | BASS_MUSIC_RAMP

        self.flags = flags            

    def rewind(self):
        pass
        
        
    def play(self, loop=0, volume=0, position=None, loopOrder=None, interpolation=1, volramp=None, loopPattern=None):
        if not position:
            position = MAKELONG(*self.position)
        else:
            position = MAKELONG(*position)
            #position = MAKELONG(0xFFFF, 0xFFFF)
            
        flags = -1
        if loop:
            self.flags = self.flags | BASS_MUSIC_LOOP
            flags = self.flags

        self.setInterpolation(interpolation)

        if volramp != None:
            self.setVolumeRamp(volramp)
        
        flags = self.flags
        
        if volume:
            BASS.BASS_ChannelSetAttributes(self.handle, -1, volume, -1)
        
        if loopOrder != None:
            MusicLoopOrder(self.handle, loopOrder)
            ChannelSetPosition(self.handle, loopOrder, 0)
            BASS.BASS_ChannelPreBuf(self.handle, 0)  # this makes sure any channelsetposition is registered
            position = MAKELONG(loopOrder, 0)
        else:
            BASS.BASS_ChannelPreBuf(self.handle, 0)  # this makes sure any channelsetposition is registered
            #startpos = BASS.BASS_ChannelGetPosition(self.music)

        #dprint "gonna play", self.handle, position, flags, 1
        self.setFlags(flags)
        if position:
            self.setPosition(position)
        BASS.BASS_ChannelPlay(self.handle, 1)
        self.error = BASS.BASS_ErrorGetCode()
        if self.error:
            print "-- BASS Play error, code", self.error, "handle", self.handle

        self.player.channels.append(self.handle)


    def stop(self):
        if self.handle:
            BASS.BASS_ChannelStop(self.handle)

    def pause(self):
        if self.handle:
            BASS.BASS_ChannelPause(self.handle)

    def getTrackVolume(self, track):
        
        result = BASS.BASS_MusicGetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + track)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def setTrackVolume(self, track, volume, scale=1):
        # input 0..64, scaled to 1..100
        if scale:
            volume = (volume * 100) / 64
        #dprint ".. setting track", track, "volume to", volume
        result = BASS.BASS_MusicSetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + track, volume)
        self.error = BASS.BASS_ErrorGetCode()
        #dprint "error", self.error, "in", self.handle, track, volume
        return result

    def getName(self):
        result = BASS.BASS_MusicGetName(self.handle)
        self.error = BASS.BASS_ErrorGetCode()
        return result

    def getNumTracks(self):
        channels = 0
        while BASS.BASS_MusicGetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + channels) != -1:
            channels += 1
        return channels

    def updateTrackVolumes(self):
        channels = 0
        volumes = []
        while 1:
            result = BASS.BASS_MusicGetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + channels)
            if result == -1:
                break
            volumes.append(result)
            channels += 1
        self.trackVolumes = volumes
        self.numTracks = channels

    def soloTrack(self, track):
        self.soloTracks([track])

    def soloTracks(self, tracks):
        for i in range(self.numTracks):
            if i not in tracks:
                BASS.BASS_MusicSetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + i, 0)
            else:
                BASS.BASS_MusicSetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + i, self.trackVolumes[i])
        self.error = BASS.BASS_ErrorGetCode()
        
    def muteTrack(self, track):
        BASS.BASS_MusicSetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + track, 0)
        self.error = BASS.BASS_ErrorGetCode()

    def muteTracks(self, tracks):
        for t in tracks:
            BASS.BASS_MusicSetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + t, 0)
        self.error = BASS.BASS_ErrorGetCode()

    def unmute(self):
        for i in range(self.numTracks):
            BASS.BASS_MusicSetAttribute(self.handle, BASS_MUSIC_ATTRIB_VOL_CHAN + i, self.trackVolumes[i])
        self.error = BASS.BASS_ErrorGetCode()

    # MUTE/SOLO/VOLUME

    def isTrackMute(self, track):
        return track in self.muted

    def isTrackSolo(self, track):
        return track in self.soloed

    def setSoloedTracks(self, soloed):
        self.soloed = soloed

    def setMutedTracks(self, muted):
        self.muted = muted

    def soloTrack(self, track, append=1, toggle=1):
        if toggle and track in self.soloed:
            self.soloed.remove(track)
        elif append and track not in self.soloed:
            self.soloed.append(track)
        elif not append:
            self.soloed = [track]
        #if track in self.muted:
        #    self.muted.remove(track)
        self.setAllTrackVolumes()

    def unSoloTrack(self, track):
        if track in self.soloed:
            self.soloed.remove(track)
        self.setAllTrackVolumes()

    def soloTracks(self, tracks, append=1):
        for track in tracks:
            self.soloTrack(track, append)

    def muteTrack(self, track, toggle=1):
        # if it's soloed, just unsolo it
        if toggle and track in self.muted:
            self.muted.remove(track)
        elif track in self.soloed:
            self.soloed.remove(track)
        elif track not in self.muted:
            self.muted.append(track)
        self.setAllTrackVolumes()

    def unmuteTrack(self, track):
        #dprint "..bass unmuting", track
        if track in self.muted:
            self.setTrackVolume(track, self.trackVolumes[track])
            self.muted.remove(track)

    def toggleTrack(self, track):
        if track in self.muted:
            self.unmuteTrack(track)
        else:
            self.muteTrack(track)

    def toggleTracks(self, tracks):
        for track in tracks:
            self.toggleTrack(track)

    def muteTracks(self, tracks):
        for track in tracks:
            self.muteTrack(track)
            
    def unSoloTracks(self):
        # unsolo all tracks
        self.soloed = []
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
        # sets all track volumes, taking solos and mutes into account
        #print ".. setting all track volumes"
        
        numTracks = self.getNumTracks()
        if self.soloed:
            for i in xrange(numTracks):
                if i in self.soloed:
                    self.setTrackVolume(i, self.trackVolumes[i])
                else:
                    self.setTrackVolume(i, 0)
        else:
            for i in xrange(numTracks):
                if i in self.muted:
                    self.setTrackVolume(i, 0)
                else:
                    self.setTrackVolume(i, self.trackVolumes[i])

    def getTrackName(self, track):
        name = "Track " + str(track+1)
        if track in self.soloed:
            name = "[" + name + "]"
        if track in self.muted:
            name = name + " - Mute"
        return name


    def notifyPositionFunc(self, callback):
        try:
            pos = BASS.BASS_ChannelGetPosition(self.handle)
            #if pos == 0xFFFFFFFF or not BASS.BASS_ChannelIsActive(channel):
            if pos == -1 or not BASS.BASS_ChannelIsActive(self.handle):
                if self.notifier:
                    self.notifier.stop()
                    self.notifier = None
                    #raise StandardError, "playback stopped"
                return
                    
            order, row = LOWORD(pos), HIWORD(pos)
            seconds = int(time.time()) - self.startTime
            callback(order, row, seconds)
        except:
            traceback.print_exc()
            #dprint "stopping notifier"
            self.stopNotifier()


    def stopNotifier(self):
        if self.notifier:
            self.notifier.stop()
            self.notifier = None
        
    def notifyPosition(self, callback, freq=0.3):
        # delete or modify notify functions in BASS class?
        
        if self.notifier:
            self.notifier.stop()

        self.startTime = int(time.time())

        lt = threadx.LoopThread(self.notifyPositionFunc, (callback,))
        lt.setSleepTime(freq)
        lt.start()
        self.notifier = lt






    # LIVE PLAYBACK

    def setMixingVolume(self, volume):
        pass

    def setSpeed(self, speed):
        pass

    def setTempo(self, tempo):
        pass

    def setGlobalVolume(self, gv):
        pass

    def setTrackPan(self, track, pan):
        pass

    def setOrderList(self, orders):
        pass

    

    



def getNumTracks(fname):
    mod = BASSMusic(fname, noSamples=1)
    num = mod.getNumTracks()
    #dprint "BASS got", num, "tracks for", fname
    mod.free()
    return num


def modposition(order=0xFFFF, row=0xFFFF):
    if order==None:
        order = 0xFFFF
    if row==None:
        row = 0xFFFF
    return MAKELONG(order, row)


Bass = None    # global BASS instance    

class BASSEngine(observer.Subject):

    __shared_state = {}    
    def __init__(self, samplerate=DEFAULTSR, init=0, start=0, device=-1):
        self.__dict__ = self.__shared_state
        self.startTimes = {}

        #if hasattr(self, "initialized"):
        #    print "MYSELF", self.initialized

        if not hasattr(self, "did_init"):
            self.did_init = 1
            self.initialized = 0
            self.started = 0
            self.device = device
            self.initializedDevice = None
            self.initializedVolumes = 0

            self._observers = []

            self.channels = []

            self.samplerate = DEFAULTSR
            self.bitrate = 16
            self.interpolation = 1
            
            self.music = None
            if init:
                self.init(samplerate)
            if start:
                self.start()

            self.watcher = None # watcher thread
            self.notifier = None

            self.wx = 0

            global Bass
            Bass = self


    def realtimeEditing(self):
        return 0

    def getRenderer(self):
        # an info record
        return renderers.getRenderer(1)

    def getName(self):
        return "BASS 2.0"

    def getSettings(self):
        #TODO: bits and interpolation
        return self.samplerate, self.bitrate, self.interpolation


    def loadMusic(self, fname):
        music = BASSMusic(fname=fname)
        return music

    def setDevice(self, device):
        self.device = device
        if (self.initialized) and (self.initializedDevice != self.device):
            self.close()
            self.init()

    def getSampleWidth(self):
        return self.bitrate

    def setSampleWidth(self, samplewidth):
        #TODO: this is hacky because it is passed the pulldown number (0=16 bit, 1=32 bit)
        if samplewidth == 0:
            self.bitrate = 16
        elif samplewidth == 1:
            self.bitrate = 32
        global BITRATE
        BITRATE = self.bitrate
        self.init(self.samplerate, self.wx, 1)
        self.notify()

    def setSampleRate(self, samplerate):
        self.samplerate = samplerate
        self.init(samplerate, self.wx, 1)
        self.notify()

    def getSampleRate(self):
        return self.samplerate

    def setInterpolation(self, mode):
        self.interpolation = mode
        self.notify()

    def getInterpolation(self):
        return self.interpolation

    def init(self, samplerate=DEFAULTSR, wx=1, reinit=0):
        #dprint "init", self.device, self.initialized, self, reinit

        self.wx = wx

        if self.initialized and reinit:
            #print "basslib reinitializing", samplerate
            self.initialized = 0
            self.close()

        device = self.device
        if device == -1:
            device = 1

        if wx and not self.initialized:
            #wxx.PleaseWaitFunc("Initializing BASS Sound System...", BASS.BASS_Init, (device, samplerate, 0, 0, 0))
            if not self.initialized:
                BASS.BASS_Init(device, samplerate, 0, 0, 0)
                self.samplerate = samplerate
        else:

            #print "init", self.device, samplerate, 0, 0
            if not self.initialized:
                BASS.BASS_Init(device, samplerate, 0, 0, 0)
                self.samplerate = samplerate

        #print "basslib init returned", BASS.BASS_ErrorGetCode()

        self.initialized = 1
        self.initializedDevice = self.device
        self.samplerate = samplerate
        if not self.initializedVolumes:
            #BASS.BASS_SetGlobalVolumes(options.SongVolume,-1,-1)
            BASS.BASS_SetConfig(BASS_CONFIG_GVOL_MUSIC, options.SongVolume)
            #BASS.BASS_SetGlobalVolumes(-1, options.SampleVolume,-1)
            BASS.BASS_SetConfig(BASS_CONFIG_GVOL_SAMPLE, options.SampleVolume)
            self.initializedVolumes = 1
            


                
    def start(self, wx=1):
        if not self.initialized:
            self.init(wx=wx)
        if not self.started:
            BASS.BASS_Start()
            self.started = 1

    def pause(self):
        BASS.BASS_Pause()
        self.started = 0

    def stop(self):
        if self.notifier:
            self.notifier.stop()
        if self.watcher:
            self.watcher.stop()
        BASS.BASS_Stop()
        self.started = 0

    def stopIfNotPlaying(self):
        if not self.channels:
            self.stop()

    def closeIfNotPlaying(self):
        if not self.channels:
            self.stop()
            self.close()


    def getNumDevices(self):
        count = 0
        #dprint "Getting", count
        while BASS.BASS_GetDeviceDescription(count):
            #dprint "count", count
            count += 1
        return count

    def getDevices(self):
        devs = []
        count = 0
        while BASS.BASS_GetDeviceDescription(count):
            devs.append(BASS.BASS_GetDeviceDescription(count))
            count += 1
        return devs

    #def pause(self):    #    BASS.BASS_Pause()

    def close(self):
        self.stop()
        BASS.BASS_Free()
        self.initialized = 0

    def closeChannel(self, channel):
        #dprint "closing", channel
        BASS.BASS_ChannelStop(channel)
        BASS.BASS_MusicFree(channel)
        if channel in self.channels:
            self.channels.remove(channel)

    def stopChannel(self, channel):
        BASS.BASS_ChannelStop(channel)

    def closeChannels(self, chanlist):
        for channel in chanlist:
            self.closeChannel(channel)

    def closeAllChannels(self):
        #dprint "closing all channels", self.channels
        for channel in self.channels:
            self.closeChannel(channel)

    def stopAllChannels(self):
        for channel in self.channels:
            self.stopChannel(channel)

    def stopChannels(self, chanlist):
        for channel in chanlist:
            self.stopChannel(channel)

    def flushChannels(self):
        # stop and free and channels that aren't active
        for channel in self.channels:
            if not BASS.BASS_ChannelIsActive(channel):
                self.closeChannel(channel)

    def playSample(self, sample, freq=-1, volume=-1, pan=-101, loop=0, startpos=0):
        #dprint sample, startpos, freq, volume, pan, loop
        #dprint "playin", sample
        channel = BASS.BASS_SamplePlayEx(sample, startpos, freq, volume, pan, loop)
        return channel

    def stopSample(self, sample):
        BASS.BASS_SampleStop(sample)

    def freeSample(self, sample):
        BASS.BASS_SampleFree(sample)

    def loadSample(self, fname, max=100, flags=BASS_SAMPLE_OVER_POS):
        sample = BASS.BASS_SampleLoad(0, fname, 0, 0, max, flags)
        return sample
        
    def synchroPlay(self, flist):
        channels = []
        i = 0
        for file in flist:
            chan = BASS.BASS_MusicLoad(0, file, 0, 0, 0, 0)
            BASS.BASS_ChannelPreBuf(chan, 0)
            channels.append(chan)
            if i:
                BASS.BASS_ChannelSetLink(channels[0], chan)
            i += 1
        BASS.BASS_MusicPlay(channels[0])
        self.channels = self.channels + channels

    def getNormalizationAmp(self, channel, callback=None, rewind=1, usefloat=0):
        # first set amp to 100 using MusicSetAmplify (SetGlobalVolumes doesn't affect the mixing level)
        # Then decode the MOD block-by-block (without writing to disk). After decoding each block, check if there are 
        # any samples at 32767 or -32768 (ie. max level). If there are, reduce the amplification.

        if callback:
            callback(0)

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

        BASS.BASS_MusicSetAmplify(channel, amplify)
        numOrders=BASS.BASS_MusicGetLength(channel, 0)

        curmax = 0

        while BASS.BASS_ChannelIsActive(channel):
            #data = BASS.BASS_ChannelGetData(channel, "", 10000)

            prevpos = BASS.BASS_ChannelGetPosition(channel)
            #dprint "prevpos", prevpos
            data = ChannelGetData(channel, 1000)
            #dprint "got", len(data), BASS.BASS_ChannelIsActive(channel)
            
            datan = array.array(dtype)
            datan.fromstring(data)

            if usefloat:
                if max(datan) > curmax:
                    curmax = max(datan)
                    #dprint "max", curmax

            if maxval in datan or minval in datan:
                amplify -= 1
                #dprint "setting amplify to", amplify
                BASS.BASS_MusicSetAmplify(channel, amplify)
                BASS.BASS_ChannelSetPosition(channel, prevpos)
                #BASS.BASS_ChannelPreBuf(channel, 0)
                #dprint ". repeat", prevpos
                

            pos=BASS.BASS_ChannelGetPosition(channel);
            if (LOWORD(pos) != currentOrder):
                currentOrder = LOWORD(pos)

                progress = int((float(currentOrder) / numOrders) * 100)

                if callback:
                    callback(progress)

        if rewind:
            pass
            #TODO: will this work now?
            #dprint "rewinding"
            #BASS.BASS_ChannelSetPosition(channel, 0, 0)

        if callback:
            callback(100)

        #dprint "!!! got amp", amplify

        #dprint "returning", amplify
        if usefloat:
            return curmax
        else:
            return amplify                

    def render(self, channel, outfile, callback=None, normalize=1, amp=50, includenorm=1, samplerate=44100, usefloat=0):
        restorerate = 0
        if samplerate != self.samplerate:
            restorerate = self.samplerate
            #dprint "initting", samplerate
            self.init(samplerate, wx=0, reinit=1)

        if normalize:
            amp = self.getNormalizationAmp(channel, callback, usefloat=usefloat)

        BASS.BASS_MusicSetAmplify(channel, amp)        
        numOrders=BASS.BASS_MusicGetLength(channel, 0)

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

        got = 0                
        while BASS.BASS_ChannelIsActive(channel):
            #data = BASS.BASS_ChannelGetData(channel, "", 10000)
            data = ChannelGetData(channel, 10000)
            #dprint "got", len(data)
            got += len(data)
            f.writeframes(data)

            pos=BASS.BASS_ChannelGetPosition(channel);
            if (LOWORD(pos) != currentOrder):
                currentOrder = LOWORD(pos)

                if normalize and includenorm:
                    progress = int(((float(currentOrder) / numOrders) * 100) / 2) + 50
                else:
                    progress = int((float(currentOrder) / numOrders) * 100)

                if callback:
                    callback(progress)

            time.sleep(0.002)
        #dprint "!!!!! got total", got/4

        if callback:
            callback(100)
            

    def getNormalizationFromFile(self, fname, callback=None, interpolation=1, samplerate=DEFAULTSR, usefloat=0, restore=1, volramp=1):
        #print "!! gnff", samplerate, self.samplerate, fname, volramp
        restorerate = 0
        if samplerate != self.samplerate:
            restorerate = self.samplerate
            #dprint "gnff initting", samplerate
            self.init(samplerate, wx=0, reinit=1)


        flags = BASS_MUSIC_DECODE
        if not interpolation:
            flags = flags | BASS_MUSIC_NONINTER
        if usefloat:
            flags = flags | BASS_MUSIC_FLOAT

        flags = flags | BASS_MUSIC_STOPBACK

        if volramp:
            flags = flags | BASS_MUSIC_RAMPS
        else:
            flags = flags | BASS_MUSIC_RAMP
        
        music = BASS.BASS_MusicLoad(0, fname, 0, 0, flags, 0)
        amp = self.getNormalizationAmp(music, callback=callback, usefloat=usefloat)
        BASS.BASS_MusicFree(music)

        if restore and restorerate:
            self.init(restorerate, wx=0, reinit=1)

        return amp

    def renderFile(self, fname, outname, callback=None, normalize=1, amp=50, interpolation=1, samplerate=DEFAULTSR, usefloat=0, volramp=1):

        #dprint "renderFile volramp", volramp

        restorerate = 0
        if samplerate != self.samplerate:
            restorerate = self.samplerate
            #dprint "initting", samplerate
            self.init(samplerate, wx=0, reinit=1)

        print "-- Rendering", fname, "to", outname
        #flags = BASS_MUSIC_DECODE | BASS_MUSIC_FLOAT
        #flags = BASS_MUSIC_DECODE | BASS_MUSIC_NONINTER

        flags = BASS_MUSIC_DECODE
        #dprint ".. interpolation", interpolation
        if not interpolation:
            flags = flags | BASS_MUSIC_NONINTER

        if usefloat:
            #dprint "using float"
            flags = flags | BASS_MUSIC_FLOAT

        if volramp == 1:
            flags = flags | BASS_MUSIC_RAMPS
        elif volramp == 2:
            flags = flags | BASS_MUSIC_RAMP

        flags = flags | BASS_MUSIC_STOPBACK
        
        #dprint "music", music
        if normalize:
            # ninja no float
            tempflags = flags
            if flags & BASS_MUSIC_FLOAT:
                tempflags = flags ^ BASS_MUSIC_FLOAT
            music = BASS.BASS_MusicLoad(0, fname, 0, 0, tempflags, 0)
            tusefloat = usefloat
            tusefloat = 0    # :ninja:
            amp = self.getNormalizationAmp(music, callback=callback, usefloat=tusefloat)
            #dprint "got amp", amp
            BASS.BASS_MusicFree(music)

        music = BASS.BASS_MusicLoad(0, fname, 0, 0, flags, 0)
            
        #dprint "calling render"
        self.render(music, outname, callback, normalize=0, amp=amp, samplerate=samplerate, usefloat=usefloat)

        if restorerate:
            self.init(restorerate, wx=0, reinit=1)



    def checkChannelActive(self, channel, callback):
        if not BASS.BASS_ChannelIsActive(channel):
            callback()
            if self.watcher:
                self.watcher.stop()

    def notifyPositionFunc(self, channel, callback):
        try:
            pos = BASS.BASS_ChannelGetPosition(channel)
            #if pos == 0xFFFFFFFF or not BASS.BASS_ChannelIsActive(channel):
            if pos == -1 or not BASS.BASS_ChannelIsActive(channel):
                if self.notifier:
                    self.notifier.stop()
                    self.notifier = None
                    #raise StandardError, "playback stopped"
                return
                    
            order, row = LOWORD(pos), HIWORD(pos)
            seconds = int(time.time()) - self.startTimes.get(channel, 0)
            callback(order, row, seconds)
        except:
            traceback.print_exc()
            #dprint "stopping notifier"
            if self.notifier:
                self.notifier.stop()
                self.notifier = None

    def stopNotifier(self):
        if self.notifier:
            self.notifier.stop()
            self.notifier = None
        

    def notifyPosition(self, channel, callback, freq=0.3):
    #def notifyPosition(self, channel, callback, freq=0.1):
        if self.notifier:
            self.notifier.stop()

        self.startTimes[channel] = int(time.time())
        #TODO: delete startTimes when not needed anymore
        lt = threadx.LoopThread(self.notifyPositionFunc, (channel, callback))
        lt.setSleepTime(freq)
        lt.start()
        self.notifier = lt


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
        while BASS.BASS_MusicGetAttribute(music, BASS_MUSIC_ATTRIB_VOL_CHAN + channels) != -1:
            #dprint "vol", channels, BASS.BASS_MusicGetVolume(music, channels)
            channels += 1
        

    def numTracks(self, music):
        channels = 0
        while BASS.BASS_MusicGetAttribute(music, BASS_MUSIC_ATTRIB_VOL_CHAN + channels) != -1:
            channels += 1
        return channels

    def soloTrack(self, music, track):
        for i in range(64):
            if i != track:
                BASS.BASS_MusicSetAttribute(music, BASS_MUSIC_ATTRIB_VOL_CHAN + i, 0)

    def soloTracks(self, music, tracks):
        for i in range(64):
            if i not in tracks:
                BASS.BASS_MusicSetAttribute(music, BASS_MUSIC_ATTRIB_VOL_CHAN + i, 0)
        

    def muteTrack(self, music, track):
        BASS.BASS_MusicSetAttribute(music, BASS_MUSIC_ATTRIB_VOL_CHAN + track, 0)

    def muteTracks(self, music, tracks):
        for t in tracks:
            BASS.BASS_MusicSetAttribute(music, BASS_MUSIC_ATTRIB_VOL_CHAN + t, 0)


class BASSStream(BASSChannel):
    def __init__(self):
        self.handle = 0
        self.error = 0

    def create(self, proc, freq=DEFAULTSR, flags=0, user=0):
        # HSTREAM WINAPI BASS.BASS_StreamCreate(DWORD freq, DWORD flags, void *proc, DWORD user)

        self.handle = BASS.BASS_StreamCreate(freq, flags, proc, user)
        #print "stream created", self.handle, freq, flags, proc, user
        if not self.handle:
            self.error = BASS.BASS_ErrorGetCode()

    def free(self):
        BASS.BASS_StreamFree(self.handle)
        self.handle = 0

    def prebuffer(self):
        BASS.BASS_StreamPreBuf(self.handle)

    def play(self, flush=0, flags=0):
        print "Trying to play", self.handle
        if not BASS.BASS_StreamPlay(self.handle, flush, flags):
            self.error = BASS.BASS_GetErrorCode()
            print "Sterror", self.error
            
        
#from ctypes import *
#class STREAMPROC(CFunction):
#    _types_ = "iiii",
#    _stdcall_ = 0

def DecodeStream(handle, buffer, length, user):
    print "decoder", num, buffer
    #num = BASS.BASS_ChannelGetData(handle, buffer, length)
    return 0

#DecodeStreamCallback = STREAMPROC(DecodeStream)    
               
#DWORD CALLBACK YourStreamProc(
#    HSTREAM handle,
#    void *buffer,
#    DWORD length,
#    DWORD user
#);


    

"""
handle Handle of the sample to play. 
start Playback start position in samples (not bytes). 
freq The sample rate... 100 (min) - 100000 (max), -1 = use sample's default. 
volume The volume... 0 (silent) - 100 (max), -1 = use sample's default. 
pan The panning position... -100 (left) - 100 (right), -101 = use sample's default. 
loop TRUE = Loop the sample... -1 = use sample's default. 
"""


if __name__ == "__main__":
    test7()

