#TODO: review

import it, xmod, xm
from itx import ITX
import filenamer, filex, utilx
import shutil, time, os, stat, sys, random, tempfile, copy

from options import *

import basslib, libmp, modplayer

import observer


#awesome
# mod_document is an observer as well as a subject;
# it can receive updates from controls, but also send updates to dialogs.

        
class ModDocument(xmod.XMOD, observer.Subject):
    def __init__(self, fname="", makenew=0, player=None, music=None):
        #it.ITModule.__init__(self)
        #ITX.__init__(self)
        self.init(fname, makenew, player, music)

    def init(self, fname="", makenew=0, player=None, music=None):
        self.editFile = "New " + self.modtype
        self.realFile = self.editFile
        self.tempFile = fname
        self.lastModified = 0
        self.changed = 0

        self.player = player    # the playback engine (probably BASS)
        self.music = music      # current associated music object (such as BASSMusic class instance)
        self.loadedMusics = {}  # stores loaded music objects for different players.

        self.playingChannel = None
        self.channels = []
        self.volume = 100

            
        # these are playback engine volumes for each track, 0-100, not related to the IT channel volumes.
        # these DO NOT change when tracks are muted or soloed.
        self.trackVolumes = [100] * self.MAX_TRACKS
        self.soloed = []    # list of currently soloed tracks
        self.muted = []     # list of currently muted tracks

        self.plugins = []
        
        if fname:
            self.open(fname)
            #print "makenew", makenew

        if makenew:
            self.makeNew(fname)

    def update(self, subject):  # called by subjects
        # update order list
        olist = subject.getData()
        self.setOrderList(olist)
        #print "update set order list to", self.header.orders, self, self.getName()
        

    def getCurrentTrackSettings(self):
        # returns track volumes and pannings modified by current solo and mute settings
        # note that for ITs, track disable options are implemented in the panning values.
        # tracks must be disabled to properly mute them, as track volume is only an initial settings
        # that may be changed by volume events.

        modplayer.lockPlayer()
        player = modplayer.getPlayer()

        # a list of 64 volumes and pannings
        volumes = copy.deepcopy(self.header.channelVolume)
        pannings = copy.deepcopy(self.header.channelPan)

        handle = self.getMusicHandle()
        if handle and player.realtimeEditing():
            self.soloed = handle.soloed
            self.muted = handle.muted
        else:
            pass
            #handle.setSoloedTracks(self.soloed)
            #handle.setMutedTracks(self.muted)
            #handle.setAllTrackVolumes()

        if self.soloed:
            for i in range(len(volumes)):
                if i not in self.soloed:
                    volumes[i] = 0
                    if pannings[i] < 128:
                        pannings[i] += 128
        else:
            for i in range(len(volumes)):
                if i in self.muted:
                    volumes[i] = 0
                    if pannings[i] < 128:
                        pannings[i] += 128

        modplayer.unlockPlayer()

        return volumes, pannings
                

    def setVolume(self, volume):
        self.volume = volume
        music = self.getMusicHandle()
        if music:
            music.setVolume(volume)

    def getMusicHandle(self):
        music = self.loadedMusics.get(str(modplayer.getPlayer().__class__), None)
        return music
            
    def loadMusic(self, fname=None):
        # loads music object for playback

        modplayer.lockPlayer()
        player = modplayer.getPlayer()


        # if order list is empty modplug should not use the original file, but the edit file we have unfolded 
        #if self.isOrderListEmpty() or not fname:

        # actually, lets just always use the editfile if it exists; why wouldn't we?        
        if self.editFile != "New IT":
            fname = self.editFile

        if not fname:
            modplayer.unlockPlayer()
            return 0

        #print ".. loading", fname, "for", player, "and", self.editFile
            
        if self.loadedMusics.get(str(player.__class__), None):
            self.loadedMusics[str(player.__class__)].free()
            
        #self.music = basslib.BASSMusic(fname=fname)
        #self.music = libmp.MODPLUGMusic(fname=fname)

        self.music = player.loadMusic(fname=fname)
        self.loadedMusics[str(player.__class__)] = self.music

        self.setVolume(self.volume)

        # call handle mute for tracks muted in mod.  need to do this before calling setAllTrackVolumes.
        if self.music:
            for i in range(self.numTracks()):
                vol, pan, enabled, surround = self.getTrackSettings(i)
                if not enabled:
                    self.music.muteTrack(i)
        
        self.setAllTrackVolumes()

        modplayer.unlockPlayer()

        return self.music        


    def initPlayback(self, force=0):
        # inits playback if necessary
        if force or not self.getMusicHandle():
            self.loadMusic()

    def stop(self, close=0):

        modplayer.lockPlayer()
        player = modplayer.getPlayer()

        music = self.getMusicHandle()        
        if music:
            #print "stopping music", self.music
            music.stop()
            if close:
                music.close()
                
        #TODO: does BASS need this?
        #if self.channels:
        #    #print "stopping channels", self.channels
        #    for channel in self.channels:
        #        channel.stop()
        #        self.channels.remove(channel)

        #TODO: obsolete?
        player.stopNotifier()
        modplayer.unlockPlayer()


    def playNote(self, note, instrument):
        modplayer.lockPlayer()
        player = modplayer.getPlayer()
        music = self.getMusicHandle()
        if player.realtimeEditing():
            music.PlayNote(note, instrument, 0, 1)
        modplayer.unlockPlayer()
        

    def playPattern(self, pattern, notifyCallback=None, order=-1):
        # order can be specified to override default getPatternOrder

        modplayer.lockPlayer()
        player = modplayer.getPlayer()
        music = self.getMusicHandle()

        if player:
            player.start()


        if (not music) or (not player.realtimeEditing()):
            fname = self.getEditFile()
            if self.modtype == "IT":
                fname, numorders = self.makePlayableCopy(fname, filenamer.uniqueFilename(fname))

            music = self.loadMusic(fname)
            if self.modtype == "IT":
                filex.remove(fname)

        if order < 0:
            order = self.getPatternOrder(pattern)
        if order == None:
            order = pattern

        if player:
            player.start()

            player.stopAllChannels()            

            if not player.realtimeEditing():
                player.closeAllChannels()            

            #self.music.stop()
            if music:
                music.rewind()  # rewind to reset volume and pan settings
                #print "playing looping pattern", pattern, order
                music.play(options.LoopPatterns, self.volume, loopOrder=order, interpolation=player.getInterpolation(), loopPattern=pattern)
                if notifyCallback:
                    music.notifyPosition(notifyCallback)

        modplayer.unlockPlayer()


    def reloadHandles(self):
        fname = self.getEditFile()
        #if self.modtype == "IT":
        fname, numorders = self.makePlayableCopy(fname, filenamer.uniqueFilename(fname))

        restore = 0
        if self.music:
            restore = 1
            soloed, muted = self.music.soloed, self.music.muted

        music = self.loadMusic(fname)
        if self.modtype == "IT":
            filex.remove(fname)
        #print "removing", fname, filex.remove(fname)

        #if hasattr(music, "setSoloedTracks"):
        #    music.setSoloedTracks(self.soloed)
        #    music.setMutedTracks(self.muted)
        #    music.setAllTrackVolumes()

        if restore:
            music.soloed = soloed
            music.muted = muted
            music.setAllTrackVolumes()
            
        return music
        
                                        

    def play(self, notifyCallback=None, order=0, row=0):
        ##self.saveWork()

        result = 0
        
        modplayer.lockPlayer()  # ensure we can run this block of code without the player switching on us
        player = modplayer.getPlayer()
        music = self.getMusicHandle()

        #print "!! playing with", player, music

        if player:
            player.start()


        if (not music) or (not player.realtimeEditing()):
            # if no realtime editing, then we have to export and reload
            # each time to catch any changes that were made.

            music = self.reloadHandles()            


        if player:

            if not player.realtimeEditing():
                player.closeAllChannels()            
            
                # playfile will close the current playing channel, so we can remove it from the list
                if self.playingChannel in self.channels:
                    self.channels.remove(self.playingChannel)
                #self.playingChannel = self.player.playFile(fname, loop=options.LoopSongs, volume=self.volume)
                self.playingChannel = music
            else:
                player.stopAllChannels()
                #self.music.stop()
                music.rewind()

            #print "pos", order, row
            music.play(options.LoopSongs, self.volume, position=(order,row), interpolation=player.getInterpolation())
            #self.music.play(options.LoopSongs, self.volume, interpolation=options.PlaybackInterpolation)
            self.channels.append(self.playingChannel)

            if notifyCallback:
                music.notifyPosition(notifyCallback)

            result = 1

        modplayer.unlockPlayer()

        return result


    def makeNew(self, fname=None):
        # makes a new it file editable, with either a temp filename or specified tempfile name
        self.editFile = "New IT"
        self.realFile = self.editFile
        if fname:
            self.tempFile = fname
        else:
            self.tempFile = filex.pathjoin(options.TempPath, os.path.basename(tempfile.mktemp())) + self.ext
        self.lastModified = 0
        self.changed = 0
        self.path = ""
                            

    def updateModification(self):
        self.lastModified = os.stat(self.realFile)[stat.ST_MTIME]        

    def open(self, fname):
        #print "mod_document open", fname
        """ returns IOError if any """
        error = None
        try:
            self.realFile = fname
            self.editFile = os.path.splitext(os.path.basename(fname))[0] + "-edit" + self.ext
            self.editFile = filex.pathjoin(filex.GetPath83(options.TempPath), self.editFile)
            try:
                filex.remove(self.editFile)
                #print "removed", self.editFile
            except:
                pass
                #print "no remove"
            
            loaded = self.load(fname, unpack=0)
            if loaded and fname:

                # try loading vst plugins
                self.plugins = []
                plugins = self.getPlugins()
                if plugins:
                    pmanager = libmp.getPluginManager()
                    for p in plugins:
                        dllname = p.getDLLName()
                        plug = pmanager.loadPlugin(dllname)
                        if plug:
                            self.plugins.append(plug)
                            
                
                self.changed = 0
                self.lastModified = os.stat(fname)[stat.ST_MTIME]
                #print "last modified at", self.lastModified
                #print time.time()
                
                #ITModule.save(self, self.editFile)
                filex.copy(self.realFile, self.editFile)

                if self.isOrderListEmpty() and options.UnfoldEmptyOrderLists:
                    self.unfold()
                    self.saveWork()
            else:
                print "-- Failed to load", fname
        except IOError:
            error = string.replace(str(sys.exc_value), "\\\\", "\\")

        return error

    def close(self):
        # should be called when file is closed
        # we unload loaded plugins here
        if self.plugins:
            pmanager = libmp.getPluginManager()
            if pmanager:
                for p in self.plugins:
                    pmanager.removePlugin(p)
            self.plugins = []
            
            


    def save(self, fname="", backupPath=options.BackupPath):
        """save temp work file as real file. make auto-backup if desired."""
        """ returns IOError if any """

        error = None

        try:
            if fname == "":
                fname = self.realFile
            fname = filenamer.requireExt(fname, self.ext)
            
            if self.realFile:
                backupFilename = os.path.splitext(self.realFile)[0] + "-backup" + self.ext
                if backupPath:
                    backupFilename = filex.pathjoin(backupPath, os.path.basename(backupFilename))
                
                #print "copying", self.realFile, "to", backupFilename
                if os.path.exists(self.realFile):
                    filex.copy(self.realFile, backupFilename)
            
            #print ".. olist", self.orderList()
            self.moduleclass.save(self, fname, checkpack=1)
            self.realFile = fname
            self.lastModified = os.stat(fname)[stat.ST_MTIME]
            self.changed = 0
            self.open(fname)  # call self.open to refresh the edit file
        except IOError:
            error = string.replace(str(sys.exc_value), "\\\\", "\\")

        return error
            
    def reload(self):
        return self.open(self.realFile)

    def reloadEditFile(self):
        # reload the temp edit file, for when another process changes it directly
        self.loadWork()

    def saveWork(self):
        #utilx.showCallerInfo()
        # save to temp work file
        if self.editFile == ("New " + self.modtype):
            self.editFile = filenamer.uniqueFilename("New" + self.modtype + str(random.randrange(1000,1000000)) + self.ext)
            self.editFile = filex.pathjoin(options.TempPath, self.editFile)
        self.moduleclass.save(self, self.editFile)
        #print "saveWork saved", self.editFile

    def saveChangesAndReloadEdit(self):
        self.saveWork()
        self.reloadHandles()

    def loadWork(self):
        # reload from temp work file
        self.moduleclass.load(self, self.editFile)
        self.markChanged()
        
    def flagChange(self, changed=1):
        self.changed = changed

    def markChanged(self):
        self.flagChange(1)

    def markUnchanged(self):
        self.flagChange(0)
        
    def getEditFile(self):
        # return the full path to the temporary edit file
        if self.editFile == ("New " + self.modtype) or not self.editFile:
            if not self.tempFile:
                # if there isn't already a tempfile, create one.
                self.makeNew()                
            f = filex.abspath(self.tempFile)
        else:
            f = filex.abspath(self.editFile)
            #f = self.editFile
        return f

    def getRealFile(self):
        if self.realFile == "New " + self.modtype:
            return filex.abspath(self.tempFile)
        else:
            return filex.abspath(self.realFile)

    def checkModified(self):
        if not self.realFile or self.realFile == ("New " + self.modtype):
            return 0
        if not os.path.exists(self.realFile):
            return 0
        modified = os.stat(self.realFile)[stat.ST_MTIME]
        return (modified > self.lastModified)

    # LIVE PLAYBACK

    def unfold(self):
        music = self.getMusicHandle()
        super(ModDocument, self).unfold()
        if music:
            music.setOrderList(self.getOrderList())
            self.saveChangesAndReloadEdit()

    def setOrderList(self, olist):
        music = self.getMusicHandle()
        super(ModDocument, self).setOrderList(olist)
        if music:
            music.setOrderList(olist)
        

    def setTempo(self, tempo):
        music = self.getMusicHandle()
        super(ModDocument, self).setTempo(tempo)
        if music:
            music.setTempo(tempo)

    def setSpeed(self, speed):
        music = self.getMusicHandle()
        super(ModDocument, self).setSpeed(speed)
        if music:
            music.setSpeed(speed)

    def setGlobalVolume(self, gv):
        music = self.getMusicHandle()
        super(ModDocument, self).setGlobalVolume(gv)
        if music:
            music.setGlobalVolume(gv)

    def setMixingVolume(self, mv):
        music = self.getMusicHandle()
        super(ModDocument, self).setMixingVolume(mv)
        if music:
            music.setMixingVolume(mv)

    def setDefaultTrackPan(self, track, pan):
        music = self.getMusicHandle()
        if music:
            music.setTrackPan(track, pan)
        super(ModDocument, self).setDefaultTrackPan(track, pan)

    def setDefaultTrackVolume(self, track, volume):
        music = self.getMusicHandle()
        self.setTrackVolume(track, volume)
        super(ModDocument, self).setDefaultTrackVolume(track, volume)

        if music:
            music.setTrackVolume(track, volume)


    # MUTE/SOLO/VOLUME

    def soloTrack(self, track, append=1, toggle=1):
        #print "solo", track, append, toggle
        if track not in self.soloed:
            self.soloed.append(track)
            
        self.getMusicHandle().soloTrack(track, append, toggle)
        
    def unSoloTrack(self, track):
        if track in self.soloed:
            self.soloed.remove(track)
            
        self.getMusicHandle().unSoloTrack(track)
        
    def soloTracks(self, tracks, append=1):
        for t in tracks:
            if t not in self.soloed:
                self.soloed.append(t)
            else:
                #print "dur", t
                pass
                
        self.getMusicHandle().soloTracks(tracks, append)
        
    def muteTrack(self, track, toggle=0):
        if track not in self.muted:
            self.muted.append(track)

        self.disableTrack(track)

        self.getMusicHandle().muteTrack(track, toggle=toggle)
        
    def unmuteTrack(self, track):
        
        if track in self.muted:
            self.muted.remove(track)
            
        self.enableTrack(track)

        if self.soloed:
            pass
        else:
            self.getMusicHandle().unmuteTrack(track)
        
    def toggleTrack(self, track):
        if track in self.muted:
            self.muted.remove(track)
        else:
            self.muted.append(track)
            
        self.moduleclass.toggleTrack(self, track)
        self.getMusicHandle().toggleTrack(track)
        
    def toggleTracks(self, tracks):
        for track in tracks:
            if track in self.muted:
                self.muted.remove(track)
            else:
                self.muted.append(track)

        self.moduleclass.toggleTracks(self, tracks)
        self.getMusicHandle().toggleTracks(tracks)
        
    def muteTracks(self, tracks):
        for t in tracks:
            if t not in self.muted:
                self.muted.append(t)
            self.disableTrack(t)
        self.getMusicHandle().muteTracks(tracks)
        
    def unSoloTracks(self):
        self.soloed = []
        self.getMusicHandle().unSoloTracks()
        
    def unmuteTracks(self):
        self.muted = []
        self.enableAllTracks()
        self.getMusicHandle().unmuteTracks()
        
    def resetTrackVolumes(self):
        self.getMusicHandle().resetTrackVolumes()
        
    def setAllTrackVolumes(self):
        self.getMusicHandle().setAllTrackVolumes()

    def getTrackName(self, track, number=1, colors=1):
        #TODO: here the colors
        name = self.moduleclass.getTrackName(self, track, number=number)
        handle = self.getMusicHandle()
        # for colors: first character is ^, then chr(r) chr(g) chr(b)
        if handle:
            if handle.isTrackSolo(track):
                col = options.Colors["soloTrackName"]
                name = "[" + name + "]"
                if colors:
                    name = "^" + chr(col[0]) + chr(col[1]) + chr(col[2]) + name
            elif handle.isTrackMute(track):
                #name += " - Mute"
                col = options.Colors["muteTrackName"]
                if colors:
                    name = "^" + chr(col[0]) + chr(col[1]) + chr(col[2]) + name
        return name

    def isTrackSolo(self, track):
        handle = self.getMusicHandle()
        if handle:
            return handle.isTrackSolo(track)
        else:
            return 0

    def isTrackMute(self, track):
        handle = self.getMusicHandle()
        if handle:
            return handle.isTrackMute(track)
        else:
            return 0


        


    def getPatternName(self, pattern, number=1):
        return self.moduleclass.getPatternName(self, pattern, number=number)

            

class ITDocument(ModDocument, ITX):
    def __init__(self, *args, **kwargs):
        ITX.__init__(self)
        self.moduleclass = ITX
        ModDocument.__init__(self, *args, **kwargs)

class XMDocument(ModDocument, xm.XMModule):
    def __init__(self, *args, **kwargs):
        xm.XMModule.__init__(self)
        self.moduleclass = xm.XMModule
        ModDocument.__init__(self, *args, **kwargs)

def getModDocument(fname="", makenew=0, player=None, music=None):
    if fname:
        ext = os.path.splitext(fname)[1].upper()
    else:
        ext = ".IT"
        
    if ext == ".IT":
        return ITDocument(fname, makenew, player, music)
    elif ext == ".XM":
        return XMDocument(fname, makenew, player, music)
    else:
        return None
    
