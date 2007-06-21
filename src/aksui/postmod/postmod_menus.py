
from wxPython.wx import wxMenu

# SLC = sample list context
# PLC = pattern list context
# TLC = track list context
# ILC = instrument list context

ID_RECENT = 30000   # for recent file list

ID_PLUGINS = 40000  # for plugin menu

ID_SLCMENU = 20000
ID_PLCMENU = 20100
ID_TLCMENU = 20200
ID_ILCMENU = 20300

ID_SLC_EXPORT   = ID_SLCMENU + 0
ID_SLC_MIX      = ID_SLCMENU + 1
ID_SLC_DELETE   = ID_SLCMENU + 2
ID_SLC_SHUFFLE  = ID_SLCMENU + 3
ID_SLC_REMOVEUNUSED = ID_SLCMENU + 4

ID_PLC_RENDER       = ID_PLCMENU + 0
ID_PLC_SPLIT        = ID_PLCMENU + 1
ID_PLC_SPLITLOAD    = ID_PLCMENU + 2
ID_PLC_DELETE       = ID_PLCMENU + 3
ID_PLC_PLAY         = ID_PLCMENU + 4

ID_TLC_RENDER       = ID_TLCMENU + 0
ID_TLC_SPLIT        = ID_TLCMENU + 1
ID_TLC_SPLITLOAD    = ID_TLCMENU + 2
ID_TLC_DELETE       = ID_TLCMENU + 3
ID_TLC_PLAY         = ID_TLCMENU + 4
ID_TLC_SOLO         = ID_TLCMENU + 5
ID_TLC_MUTE         = ID_TLCMENU + 6
ID_TLC_UNMUTE_ALL   = ID_TLCMENU + 7
ID_TLC_UNSOLO_ALL   = ID_TLCMENU + 8

ID_ILC_RENDER       = ID_ILCMENU + 0
ID_ILC_SPLIT        = ID_ILCMENU + 1
ID_ILC_SPLITLOAD    = ID_ILCMENU + 2
ID_ILC_DELETE       = ID_ILCMENU + 3
ID_ILC_PLAY         = ID_ILCMENU + 4



def GetInstrumentListContextMenu():
    menu = wxMenu()
    menu.Append(ID_ILC_RENDER, "Split and Render to WAV")
    menu.Append(ID_ILC_SPLIT, "Split to IT File(s)")
    menu.Append(ID_ILC_SPLITLOAD, "Split to New")

    menu.AppendSeparator()
    menu.Append(ID_ILC_DELETE, "Delete")

    #menu.AppendSeparator()
    #menu.Append(ID_ILC_DELETE, "Delete Track Data")
    #menu.AppendSeparator()
    #menu.Append(ID_ILC_PLAY, "Play")
    return menu


def GetTrackListContextMenu():
    menu = wxMenu()
    menu.Append(ID_TLC_RENDER, "Split and Render to WAV")
    menu.Append(ID_TLC_SPLIT, "Split to IT File(s)")
    menu.Append(ID_TLC_SPLITLOAD, "Split to New")

    #menu.AppendSeparator()
    #menu.Append(ID_TLC_DELETE, "Delete Track Data")
    menu.AppendSeparator()
    #menu.Append(ID_TLC_PLAY, "Play")
    menu.Append(ID_TLC_SOLO, "Solo")
    menu.Append(ID_TLC_MUTE, "Mute")
    menu.AppendSeparator()
    menu.Append(ID_TLC_UNMUTE_ALL, "Unmute All")
    menu.Append(ID_TLC_UNSOLO_ALL, "Unsolo All")
    return menu

def GetPatternListContextMenu():
    menu = wxMenu()
    menu.Append(ID_PLC_RENDER, "Split and Render to WAV")
    menu.Append(ID_PLC_SPLIT, "Split to IT File(s)")
    menu.Append(ID_PLC_SPLITLOAD, "Split to New")
    menu.AppendSeparator()
    menu.Append(ID_PLC_DELETE, "Delete Pattern Data")
    menu.AppendSeparator()
    menu.Append(ID_PLC_PLAY, "Play")
    return menu

def GetSampleListContextMenu():
    menu = wxMenu()
    menu.Append(ID_SLC_EXPORT, "Export Selected")
    menu.Append(ID_SLC_REMOVEUNUSED, "Remove Unused")
    #menu.Append(ID_SLC_MIX, "Mix Selected to New")
    menu.AppendSeparator()
    menu.Append(ID_SLC_DELETE, "Delete")
    menu.Append(ID_SLC_SHUFFLE, "Shuffle")
    return menu

def init():
    global sampleListContextMenu, patternListContextMenu, trackListContextMenu, instrumentListContextMenu
    sampleListContextMenu = GetSampleListContextMenu()
    patternListContextMenu = GetPatternListContextMenu()
    trackListContextMenu = GetTrackListContextMenu()
    instrumentListContextMenu = GetInstrumentListContextMenu()

