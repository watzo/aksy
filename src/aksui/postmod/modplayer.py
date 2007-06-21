
# generic interface to a mod and music player that can use either BASS or Modplug for playback

import time
from options import *
import itrender

PLAYER = None
BASS = None
MODPLUG = None

LOCKED = 0

CALLBACK = None # switch player callback

OBSERVERS = []  # objects that observe setting changes


def loadPlayerModules():
    #PSYCO HAS NO LOCALS
    locals = {}
    global basslib, PLAYER, BASS, MODPLUG
    basslib = __import__("basslib", globals(), {})
    BASS = basslib.BASSEngine(device=options.AudioDeviceNum)
    itrender.BASS = BASS
    
    import basslib      # so installer will catch it
    import libmp

    libmp.MODPLUG
    MODPLUG = libmp.MODPLUG()
    itrender.MODPLUG = MODPLUG

    setPlayer(options.DefaultPlayer)

    global OBSERVERS
    for o in OBSERVERS:
        BASS.attach(o)
        MODPLUG.attach(o)
    
    #if options.DefaultPlayer == 0:
    #    PLAYER = MODPLUG
    #else:
    #    PLAYER = BASS
    #PLAYER = BASS

    #BASS.init()

def addObserver(observer):
    # if not loaded yet, keep for attaching later
    global OBSERVERS
    OBSERVERS.append(observer)

    for player in getPlayers():
        if player:
            player.attach(observer)

def removeObserver(observer):
    global OBSERVERS
    if observer in OBSERVERS:
        OBSERVERS.remove(observer)

    for player in getPlayers():
        if player:
            player.detach(observer)
    


def lockPlayer():
    global LOCKED
    LOCKED = 1

def unlockPlayer():
    global LOCKED
    LOCKED = 0

def getPlayer():
    return PLAYER

def getPlayers():
    return MODPLUG, BASS

def getBASS():
    return BASS

def getMODPLUG():
    return MODPLUG

def getPlayerNames():
    return ["Modplug 1.16", "BASS 2.0"]

def setPlayer(playernum):
    # 0 = modplug, 1 = BASS
    # use switchPlayer instead if you want to stop current player and notify main application of the switch

    while LOCKED:
        #print ". player locked, waiting..."
        time.sleep(0.1)

    lockPlayer()
    
    global PLAYER, MODPLUG, BASS
    if playernum == 0:
        PLAYER = MODPLUG
    else:
        PLAYER = BASS

    unlockPlayer()        


def switchPlayer(playernum):
    lockPlayer()
    PLAYER.stopAllChannels()
    unlockPlayer()

    setPlayer(playernum)

    if CALLBACK:
        CALLBACK(playernum)

    PLAYER.notify()


def setSwitchCallback(callback):
    global CALLBACK
    CALLBACK = callback
    


def getPlayerByCode(code):
    if code == "BASS":
        return getBASS()
    elif code == "MODPLUG":
        return getMODPLUG()
    else:
        return None

