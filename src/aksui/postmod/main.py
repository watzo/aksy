#import psyco
#from psyco.classes import *
#import psyco.classes

# don't move these, python thread issues
import nt, wavex

# redirect stdout and stderr to postmod.log
import sys, errorlog
DEBUGOUTPUT = errorlog.init("postmod.log")

#import moduletracer
#import basslib, libmp
#moduletracer.dotrace(basslib)
#moduletracer.dotrace(libmp)

# set up default error handler first thing, before other imports.
import traceback, binascii
#import wxerror

# this exception handler will be used until the main wxframe is created and sets up the wxerror handler
def exceptionHandler(type, value, tback):    
    try:
        print ""
        print "-- Initialization Exception --"
        tbmessage = "Type: " + str(type) + "\nValue: " + str(value) + "\nData:\n"
        tblist = traceback.extract_tb(tback)
        for x in tblist:
            #print str(x)
            tbmessage = tbmessage + str(x) + "\n"
        #print ""
        print "Error Code:", tbmessage
        
    except:
        traceback.print_exc()

    return 0

sys.excepthook = exceptionHandler

import app

APPNAME = app.NAME
APPVERSION = app.VERSION

MAINFRAME = None
MIXERDLG = None

print "-- starting", APPNAME, app.FULLVERSION


import pitchkeymap  # for playing samples

from options import *



#import Numeric

# just so installer catches these, part of numarray, but not caught by installer
#imxport libnumarray
#imxport _chararray

#raise StandardError, "FAKED ERROR ON STARTUP"

DEBUG = 0
DEFAULTCONSOLEIO = 0

#REDIRECTIO = 1

URL_REGISTER = "http://www.magicfish.net/postmod/register.php?version=" + app.VERSIONID
URL_MAGICFISH = "http://www.magicfish.net"
URL_SUPPORTFORUM = "http://www.magicfish.net/supportforum"

LOCALTEST = 0

import sys, os, gc, time, threading, string, webbrowser, win32api, shutil, zlib
import threadx, processx, filenamer, dirwalk, pathmemory, filex
import observer

#from mx.DateTime import *
from normalDate import NormalDate

#from wx.html import *
from wx.lib.ClickableHtmlWindow import PyClickableHtmlWindow


import wxx
from wxx import wxDialogX

from postmod_events import *
from mod_document import *
import mod_document, modplayer
import postmod_icons


from postmod_wdr import *

import it
#moduletracer.dotrace(it)

import itrender 

from filebatch import *
from postmod_app import *

from itx import *

import dlg_mixer
from dlg_filebatch import *
from dlg_generic_processor import *
from dlg_splitter import *

from dlg_plugin import PluginDialog
from dlg_mixer import MixerDialog
from dlg_modmixer import ModMixerDialog
from dlg_prefs import PreferencesDialog
from dlg_regs import *

from ctl_orderlist import OrderListControl


from sample_exporter import *
from itsplitter import *
import loop_importer

import pluginhandler, libmp

#import livedebug, liveupdate, liveorder


def SetStatusText(message):
    global MAINFRAME
    MAINFRAME.SetStatusText(message)



# WDR: classes

class PleaseWaitDialog(wx.Dialog):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        PleaseWaitDialogFunc( self, True )
        
        # WDR: handler declarations for PleaseWaitDialog
        wx.EVT_BUTTON(self, ID_BUTTON, self.OnOK)

    # WDR: methods for PleaseWaitDialog

    def GetText(self):
        return self.FindWindowById(ID_TEXT)

    def GetButton(self):
        return self.FindWindowById(ID_BUTTON)

    def SetText(self, msg):
        text = self.GetText()
        if text:
            text.SetLabel(msg)

    # WDR: handler implementations for PleaseWaitDialog

    def OnOK(self, event):
        self.Destroy()






class SliceWAVDialog(wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE,
        fname = None, realfile = None, mod=None, callback=None):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        WAVSlicerDialogFunc( self, True )
        
        # WDR: handler declarations for SliceWAVDialog
        wx.EVT_BUTTON(self, ID_BUTTON_SLICE, self.OnProcess)
        wx.EVT_BUTTON(self, ID_BUTTON_IT, self.OnSelectIT)
        wx.EVT_BUTTON(self, ID_BUTTON_WAV, self.OnSelectWAV)
        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOk)
        wx.EVT_BUTTON(self, wx.ID_CANCEL, self.OnCancel)

        # if realfile is specified, fname is not actually the filename, realfile is,
        # but only if fname is surrounded with brackets.
        self.realfile = realfile

        self.mod = mod
        self.callback = callback

        if mod:
            ctl = self.GetITFileControl()
            if ctl:
                ctl.SetValue("[" + "Current Selection" + "]")
                ctl.Enable(0)
            butt = self.GetControl("ITButton")
            if butt:
                butt.Enable(0)

        if fname:
            self.SetControlLabel("ITFile", fname)            


    def SetProgressBar(self, progress):
        bar = self.FindWindowById(ID_GAUGE_PROGRESS)
        bar.SetValue(progress)

    # WDR: methods for SliceWAVDialog

    def GetProgressBar(self):
        return self.FindWindowById(ID_GAUGE_PROGRESS)

    def GetITFileControl(self):
        return self.FindWindowById(ID_TEXTCTRL_ITFILE)

    def GetWAVFileControl(self):
        return self.FindWindowById(ID_TEXTCTRL_WAVFILE)

    # WDR: handler implementations for SliceWAVDialog        

    def OnProcess(self, event):
        inwav = self.GetControlLabel("WAVFile")
        outit = self.GetControlLabel("ITFile")

        if outit and outit[0] == '[' and self.realfile:
            outit = self.realfile
            targetOpen = 1
        else:
            targetOpen = 0
        
        if not (inwav and outit):
            return
        
        outit = filenamer.requireExt(outit, ".it")
       
        fractions = []
        if self.GetControlValue("Slice1"): fractions.append(1)
        if self.GetControlValue("Slice2"): fractions.append(2)
        if self.GetControlValue("Slice4"): fractions.append(4)
        if self.GetControlValue("Slice8"): fractions.append(8)
        if self.GetControlValue("Slice16"): fractions.append(16)
        if self.GetControlValue("Slice32"): fractions.append(32)
        if self.GetControlValue("Slice64"): fractions.append(64)

        loopFractions = []
        if self.GetControlValue("Loop1"): loopFractions.append(1)
        if self.GetControlValue("Loop2"): loopFractions.append(2)
        if self.GetControlValue("Loop4"): loopFractions.append(4)
        if self.GetControlValue("Loop8"): loopFractions.append(8)
        if self.GetControlValue("Loop16"): loopFractions.append(16)
        if self.GetControlValue("Loop32"): loopFractions.append(32)
        if self.GetControlValue("Loop64"): loopFractions.append(64)
                
        unlimitedSamples = self.GetControlValue("Allow100")
        forceMono = not (self.GetControlValue("AllowStereo"))
        #print "fmono", forceMono
        
        numslices = loop_importer.ImportLoops(outit, inwav, fractions, loopFractions, unlimitedSamples, callback=self.SetProgressBar, forceMono=forceMono, mod=self.mod)
        SetStatusText("Sliced " + inwav + " into " + outit + " - " + str(numslices) + " samples created.")

        if targetOpen:
            self.GetParent().ReloadActiveChild()

        #if self.mod:
        #    self.GetParent().UpdateActiveChild()

        if self.callback:
            #print ".. callback", self.callback
            self.callback(0)

        self.Close()


    def OnSelectIT(self, event):
        defaultpath = os.path.dirname(self.GetControlLabel("ITFile"))
        if not defaultpath:
            defaultpath = options.DefaultPath
            
        fname = wxx.SelectFile(self, ext="*.it", saving=1, pathtype="it")
        if fname:
            self.SetControlLabel("ITFile", fname)            

    def OnSelectWAV(self, event):
        defaultpath = os.path.dirname(self.GetControlLabel("WAVFile"))
        if not defaultpath:
            defaultpath = options.DefaultPath

        fname = wxx.SelectFile(self, ext="*.wav", saving=0, pathtype="wav")
        if fname and os.path.exists(fname):
            oldwavroot, ext = os.path.splitext(self.GetControlLabel("WAVFile"))
            olditroot, ext = os.path.splitext(self.GetControlLabel("ITFile"))
            self.SetControlLabel("WAVFile", fname)
            
            # if itfile has not been specified or modified, set it to selected wav root
            if (olditroot == oldwavroot) or (not self.GetControlLabel("ITFile")):
                newwavroot, ext = os.path.splitext(fname)
                itname = filex.pathjoin(options.ExportPath, os.path.basename(newwavroot)) + ".it"
                self.SetControlLabel("ITFile", itname)


    def OnOk(self, event):
        event.Skip(True)

    def OnCancel(self, event):
        event.Skip(True)


def GetAboutHTML():

    AboutHTML = """
    <center>
    <img src="%s/logo.gif">
    <h3>POSTMOD</h3><br>
    Version %s<br>
    Copyright 2003-2006 Austin Luminais<br><br>
    <a href="http://www.magicfish.net">http://www.magicfish.net</a><br><br>
    Modplug &copy 1997-2002 Olivier Lapicque<br>
    BASS sound system &copy; 1999-2006 Ian Luck<br>
    DUMB &copy 2001-2003 Ben Davis, Robert J Ohannessian and Julien Cugniere<br>
    Mikmod &copy; 2000 Jean-Paul Mikkers, Jake Stine<br>
    <!--IT2XM converter &copy; 1997 Andy Voss<br>-->
    Testing and Feedback: J. Misra and Felix Petrescu<br>
    Logo by Dan Haugh<br>
    <br>
    Support: <a href="mailto:support@magicfish.net">support@magicfish.net</a>
    </center>
    """ % (options.getImagePath(), str(app.FULLVERSION))

    return AboutHTML    


class AboutDialog(wx.Dialog):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        htmlwindow = PyClickableHtmlWindow(self, ID_HTMLWINDOW, size=(340,420))
        htmlwindow.SetPage(GetAboutHTML())
        
        AboutDialogFunc( self, True )


        
        # WDR: handler declarations for AboutDialog
        wx.EVT_BUTTON(self, ID_BUTTON, self.OnOK)
        #TODO: left down event needs to happen in statictext control
        wx.EVT_LEFT_DOWN(self, self.OnURL)

    # WDR: methods for AboutDialog

    # WDR: handler implementations for AboutDialog

    def OnOK(self, event):
        self.Close()

    def OnURL(self, event):
        pass
        #print "clicked url"



#class ITDocDialog(wx.MDIChildFrame, wxx.DialogX):
class ITDocDialog(wx.Panel, wxx.DialogX, psyco.classes.psyobj):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.TAB_TRAVERSAL, path=None, makenew=0):
        #style = wx.DEFAULT_FRAME_STYLE, path=None, makenew=0):
        #MDIChildFrame.__init__(self, parent, id, title, pos, size, style)
        #wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        wx.Panel.__init__(self, parent, id, pos, size, style)

        #self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        
        self.Show(0)
        ITDocument2Dialog2Func( self, True )
        self.Show(1)

        #self.orderListControl = None
        #self.orderListControl = OrderListControl(self, ID_ORDERLIST)
        self.orderListControl.SetLimitsFunc(self.getOrderLimits)
        self.orderListControl.SetActionFunc(self.PlayOrder)

        #self.SetIcon(app.icons.itfile)        

        self.tempfiles = []
        self.prepared = []

        self.mod = None
        if path:
            self.loadMod(path, makenew=makenew)
            #self.mod = getModDocument(path, makenew=makenew, player=BASS)
        else:
            self.mod = getModDocument(player=modplayer.getPlayer())
            #print path, self.mod
            self.Update()

        if self.orderListControl:
            # self.mod observes the order list control
            self.orderListControl.attach(self.mod)
            # and also us
            self.orderListControl.attach(self)

        self.focusControl = None

        self.newWindow = None
        self.changed = 0
        self.SettingFocus = 0
        self.keyinput = ""

        self.savework = 0

        self.samplePlayer = basslib.SamplePlayer(modplayer.getPlayer())
        self.__loadedSamples = {}   # keys are sample num indexes, values are filenames that sample has been exported to

        self.playingChannel = None
        self.channels = []  # associated BASS channels

        self.suggestedFile = None
        
        if self.mod.corrupt:
            wx.MessageBox(path + " cannot be loaded, it is corrupt!", "Corrupt Module", parent=self.GetParent())
            self.Close()
            return

        samplelist = self.GetSampleListControl()
        patternlist = self.GetPatternListControl()
        tracklist = self.GetTrackListControl()
        instrumentlist = self.GetInstrumentListControl()

        self.sampleList = samplelist
        self.patternList = patternlist
        self.trackList = tracklist
        self.instrumentList = instrumentlist
        
        #samplelist.ActivateListMode()

        self.closed = 0

        slider = self.GetControl("VolumeSlider")
        slider.SetValue(100)

        olc = self.GetOrderListControl()
        #TODO
        #wx.EVT_CHAR(olc, self.OnOrderListChar)        
        
        # WDR: handler declarations for ITDocDialog
        wx.EVT_SLIDER(self, ID_VOLUME_SLIDER, self.OnVolumeSlider)
        #wx.EVT_COMMAND_RIGHT_CLICK(samplelist, ID_LISTBOX_SAMPLES, self.OnRightClickSampleList)
        #wx.EVT_RIGHT_DOWN(self, self.OnRightDown)
        #wx.EVT_COMMAND_RIGHT_CLICK(samplelist, ID_LISTBOX_SAMPLES, self.OnRightDownSampleList)
        #wx.EVT_LIST_ITEM_SELECTED(samplelist, samplelist.GetId(), self.OnSamplesListbox)

        # samplelist events for context menus and playing samples
        wx.EVT_RIGHT_DOWN(samplelist, self.OnRightDownSampleList)
        wx.EVT_CHAR(samplelist, self.OnSampleChar)

        # patternlist events
        wx.EVT_CHAR(patternlist, self.OnPatternChar)
        wx.EVT_RIGHT_DOWN(patternlist, self.OnRightDownPatternList)

        # tracklist events
        wx.EVT_RIGHT_DOWN(tracklist, self.OnRightDownTrackList)
        wx.EVT_CHAR(tracklist, self.OnTrackChar)
        wx.EVT_KEY_DOWN(tracklist, self.OnTrackKeydown)

        # instrumentlist events        
        wx.EVT_CHAR(instrumentlist, self.OnInstrumentChar)
        wx.EVT_RIGHT_DOWN(instrumentlist, self.OnRightDownInstrumentList)

        #wx.EVT_BUTTON(self, ID_MENU_SLICEWAVTOIT, self.GetParent().OnSliceWAVIntoIT)
        #NOTE: this became GetGrandParent when this dialog was put into a notebook
        wx.EVT_BUTTON(self, ID_MENU_SLICEWAVTOIT, self.GetGrandParent().GetParent().OnSliceWAVIntoIT)


        wx.EVT_ACTIVATE(self, self.OnActivate)
        #wx.EVT_RADIOBOX(self, ID_RADIOBOX_PROCESSMODE, self.OnSelectProcessMode)
        wx.EVT_SET_FOCUS(self, self.OnSetFocus)
        wx.EVT_BUTTON(self, ID_MENU_REMOVE_UNUSED_SAMPLES, self.OnRemoveUnusedSamples)
        wx.EVT_TEXT(self, ID_SPINCTRL_GLOBAL_VOLUME, self.OnGlobalVolumeChanged)
        wx.EVT_TEXT(self, ID_SPINCTRL_MIXING_VOLUME, self.OnMixingVolumeChanged)
        wx.EVT_TEXT(self, ID_SPINCTRL_TEMPO, self.OnTempoChanged)
        wx.EVT_TEXT(self, ID_ITDOC_SPEED, self.OnSpeedChanged)
        wx.EVT_TEXT(self, ID_ITDOC_FNAME, self.OnTextChanged)
        wx.EVT_TEXT(self, ID_ITDOC_NAME, self.OnTextChanged)
        wx.EVT_LISTBOX(self, ID_LISTBOX_INSTRUMENTS, self.OnInstrumentsListbox)
        wx.EVT_LISTBOX(self, ID_LISTBOX_SAMPLES, self.OnSamplesListbox)
        wx.EVT_LISTBOX(self, ID_LISTBOX_PATTERNS, self.OnPatternsListbox)
        wx.EVT_LISTBOX(self, ID_LISTBOX_TRACKS, self.OnTracksListbox)
        wx.EVT_MENU(self, ID_MENU_FILE_SAVE_AS, self.OnSaveAs)
        wx.EVT_BUTTON(self, ID_BUTTON_RENDER, self.OnRender)
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT, self.OnExport)
        wx.EVT_BUTTON(self, ID_BUTTON_SPLIT, self.OnSplit)
        wx.EVT_MENU(self, ID_MENU_PROCESS_UNFOLD, self.OnUnfold)
        wx.EVT_BUTTON(self, ID_BUTTON_PLAY, self.OnPlay)
        wx.EVT_BUTTON(self, ID_BUTTON_STOP, self.OnStop)
        wx.EVT_BUTTON(self, ID_BUTTON_PLAY_PATTERN, self.OnPlayPattern)
        wx.EVT_BUTTON(self, ID_ITDOC_SAVE, self.OnSave)
        wx.EVT_BUTTON(self, ID_ITDOC_SAVEAS, self.OnSaveAs)
        wx.EVT_BUTTON(self, ID_ITDOC_UNFOLD, self.OnUnfold)
        wx.EVT_CLOSE(self, self.OnClose)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_CHAR(self, self.OnChar)

        #self.sampleListMenu = app.menus.GetSampleListContextMenu()
        # assign sample list context menu functions
        wx.EVT_MENU(self, app.menus.ID_SLC_EXPORT, self.OnContextExportSamples)
        wx.EVT_MENU(self, app.menus.ID_SLC_MIX, self.OnContextMixSamples)
        wx.EVT_MENU(self, app.menus.ID_SLC_DELETE, self.OnContextDeleteSamples)
        wx.EVT_MENU(self, app.menus.ID_SLC_SHUFFLE, self.OnContextShuffleSamples)
        wx.EVT_MENU(self, app.menus.ID_SLC_REMOVEUNUSED, self.OnRemoveUnusedSamples)

        # assign instrument list context menu functions
        wx.EVT_MENU(self, app.menus.ID_ILC_RENDER, self.OnContextRenderInstruments)
        wx.EVT_MENU(self, app.menus.ID_ILC_SPLIT, self.OnContextSplitInstruments)
        wx.EVT_MENU(self, app.menus.ID_ILC_SPLITLOAD, self.OnContextSplitLoadInstruments)
        wx.EVT_MENU(self, app.menus.ID_ILC_DELETE, self.OnContextDeleteInstruments)

        # assign pattern list context menu functions
        wx.EVT_MENU(self, app.menus.ID_PLC_RENDER, self.OnContextRenderPatterns)
        wx.EVT_MENU(self, app.menus.ID_PLC_SPLIT, self.OnContextSplitPatterns)
        wx.EVT_MENU(self, app.menus.ID_PLC_SPLITLOAD, self.OnContextSplitLoadPatterns)
        wx.EVT_MENU(self, app.menus.ID_PLC_DELETE, self.OnContextDeletePatterns)
        wx.EVT_MENU(self, app.menus.ID_PLC_PLAY, self.OnContextPlayPatterns)

        # assign track list context menu functions
        wx.EVT_MENU(self, app.menus.ID_TLC_RENDER, self.OnContextRenderTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_SPLIT, self.OnContextSplitTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_SPLITLOAD, self.OnContextSplitLoadTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_DELETE, self.OnContextDeleteTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_PLAY, self.OnContextPlayTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_SOLO, self.OnContextSoloTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_MUTE, self.OnContextMuteTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_UNMUTE_ALL, self.OnContextUnmuteTracks)
        wx.EVT_MENU(self, app.menus.ID_TLC_UNSOLO_ALL, self.OnContextUnsoloTracks)

        # set focus to order list control
        if olc:
            olc.SetFocus()
            self.focusControl = wx.Window_FindFocus()        

        self.StatusText, self.TimePosition = self.GetControl("StatusText"), self.GetControl("TimePosition")

        self.floating = 0
        self.parent = None

    psyco.bind(__init__)    


    def GetMainWindow(self):
        # when we're in a notebook, the main window is our grandparent.  otherwise, we are our own main window.
        return self.GetGrandParent()

    def GetMixerDialog(self):
        return self.GetGrandParent().mixer

    def GetITDialog(self):
        # for compatibility with ITDocDialogMulti
        return self

    def loadMod(self, path, makenew=0):
        if path:
            if self.mod and self.orderListControl:
                self.orderListControl.detach(self.mod)
                del self.mod
            self.mod = getModDocument(path, makenew=makenew, player=modplayer.getPlayer())
            if self.mod and self.orderListControl:
                self.orderListControl.attach(self.mod)
            self.mod.loadMusic(path)    #TODO: make playable copy
            #print path, self.mod
            self.Update()

        
    def OnPatternScreen(self, event):
        self.patternList.SetFocus()

    def OnTrackScreen(self, event):
        self.trackList.SetFocus()

    def OnInstrumentScreen(self, event):
        self.instrumentList.SetFocus()

    def OnSampleScreen(self, event):
        self.sampleList.SetFocus()


    def RestoreFocus(self, object):
        # sets the object that should receive focus when this window is switched to.
        self.focusControl = object

    def OnActivate(self, event):
        # if we're being activated, restore the saved focus object,
        # if we're being deactivated, store the saved focus object.mro
        # this is needed so the currently focused control is not changed
        # when switching back and forth between windows.
        active = event.GetActive()
        if active and self.focusControl:
            self.focusControl.SetFocus()
        else:
            self.focusControl = wx.Window_FindFocus()        


    def getOrderLimits(self):
        # return min and max of available patterns
        if not self.mod:
            return (0, 0)
        
        return (0, min(self.mod.numPatterns()-1, 254))

    def OnOrderListChar(self, event):
        ch = event.GetKeyCode()
        if ch < 255:
            ch = string.upper(chr(ch))
        if ch == ' ':
            self.OnPlay(event)            
            return

    def OnRightDown(self, event):
        self.x, self.y = event.GetX(), event.GetY()
        event.Skip()

    def OnRightDownInstrumentList(self, event):
        lst = self.GetInstrumentListControl()
        lstx, lsty = lst.GetPositionTuple()
        x, y = event.GetPositionTuple()
        self.PopupMenu(app.menus.instrumentListContextMenu, wx.Point(x+lstx,y+lsty))
        #event.Skip()       


    def OnRightDownTrackList(self, event):
        lst = self.GetTrackListControl()
        lstx, lsty = lst.GetPositionTuple()
        x, y = event.GetPositionTuple()
        self.PopupMenu(app.menus.trackListContextMenu, wx.Point(x+lstx,y+lsty))
        #event.Skip()       


    def OnRightDownPatternList(self, event):
        lst = self.GetPatternListControl()
        lstx, lsty = lst.GetPositionTuple()
        x, y = event.GetPositionTuple()
        #print "x,y", x, y, "lx, ly", lstx, lsty
        self.PopupMenu(app.menus.patternListContextMenu, wx.Point(x+lstx,y+lsty))
        #event.Skip()       

    def OnRightDownSampleList(self, event):
        lst = self.GetSampleListControl()
        lstx, lsty = lst.GetPositionTuple()
        x, y = event.GetPositionTuple()
        
        #print list.GetItemText(self.currentItem)
        self.PopupMenu(app.menus.sampleListContextMenu, wx.Point(x+lstx, y+lsty))
        #self.PopupMenu(menu, event.GetPosition())
        #event.Skip()       

    def update(self, subject):
        self.savework = 1
        self.ChangeNotify()

    def SetTrackNames(self):
        if not self.mod:
            return 0
        
        if self.mod.unpacked:
            self.SetTracks(self.mod.trackNames())
        else:
            self.SetTracks(["Loading..."])
        

    def Update(self, updateTitle=1):
        if not self.mod:
            return 0

        #if self.mod.music:
        #    print "IS1", self.mod.music.isTrackSolo(2)
        
        if updateTitle:
            if self.mod.realFile:
                self.SetTitle("Loading " + self.mod.realFile)
            else:
                self.SetTitle("New IT")
        self.SetFilename(self.mod.realFile)
        self.SetSamples(self.mod.sampleNames())
        self.SetInstruments(self.mod.instrumentNames())
        self.SetOrderList(self.mod.orderList())

        if (not self.mod and self.mod.music):
            self.SetTrackNames()
            
        self.SetPatterns(self.mod.patternNames())
        #wx.CallAfter(self.mod.getBlankPatterns)
        tempo = self.mod.getTempo()
        speed = self.mod.getSpeed()
        globalvol = self.mod.getGlobalVolume()
        mixingvol = self.mod.getMixingVolume()
        name = self.mod.getName()

        self.SetTempo(tempo)
        self.SetSpeed(speed)
        self.SetGlobalVolume(globalvol)
        self.SetMixingVolume(mixingvol)
        self.SetName(name)

        if self.mod.realFile and updateTitle:
            self.SetTitle(self.mod.realFile)

        #if not self.mod.unpacked:
        #    ut = threadx.GenericThread(self.mod.unpack, postfunc=self.UpdateTrackNames)
        #    ut.start()

        if self.mod and self.mod.music:
            self.SetTracks(self.mod.trackNames(numTracks=self.mod.music.getNumTracks()))
        wxx.Yield()

        # this is where we really do it
        ut = threadx.GenericThread(self.UpdateTrackNames)
        ut.start()

        for file in self.tempfiles:
            filex.remove(file)
        self.prepared = []

        #if self.mod.music:
        #    print "IS2", self.mod.music.isTrackSolo(2)




    def UpdateNames2(self):
        # called after pattern names are ready
        try:
            self.UpdatePatternNames()
        except:
            # if object is dead
            pass

        
    def UpdateTrackNames(self):        
        try:
            #try:
            #    raise "No"
            #    # try BASS method first
            #    BASS.init(wx=0)
            #    fname = self.mod.getEditFile()
            #    self.SetTracks(self.mod.trackNames(numTracks=basslib.getNumTracks(fname), ))
            #except:
            # then normal method
            #traceback.print_exc()

            #wx.CallAfter(self.SetTracks, self.mod.trackNames(numTracks=self.mod.music.getNumTracks()))
            #self.SetTracks(self.mod.trackNames())
            pass
        except:
            # since this is a callback, it could get called after the window has been closed and mod is deleted
            #traceback.print_exc()
            pass

        # now get and update pattern names
        if hasattr(self, "mod") and self.mod:

            #wxx.Yield()
            self.mod.unpack()
            #wxx.Yield()

            #pt = threadx.GenericThread(self.mod.getBlankPatterns, postfunc=wx.CallAfter, postargs=(self.UpdateNames2,))
            #pt.start()
            #wxx.Yield()
            self.mod.getBlankPatterns()
            #wxx.Yield()
            wx.CallAfter(self.UpdateNames2)

            


    def UpdatePatternNames(self):
        if not self.mod:
            return 0
        
        blanks = self.mod.blanks
        list = self.GetPatternListControl()
        for i in blanks:
            list.SetItemForegroundColour(i, wx.Colour(*options.Colors['emptyPatternName'])) # 200, 200, 200
        list.Refresh()
            
            #curst = list.GetString(i)
            #if curst.find("(Empty)") == -1:
            #    list.SetString(i, list.GetString(i) + " (Empty)")
            #    list.SetTextColour(i, 200, 200, 200)
            #    #list.SetBackgroundColour(i, 0, 0, 0)
            #    list.Update()
            #    list.Refresh()

    def TransferDataFromWindow(self):
        if not self.mod:
            return 0

        data = self.GetControlData()
        #print str(data)
        self.mod.setTempo(data["Tempo"])
        self.mod.setSpeed(data["Ticks"])
        self.mod.setGlobalVolume(data["GlobalVolume"])
        self.mod.setMixingVolume(data["MixingVolume"])
        self.mod.setName(data["SongName"])
        

    def CheckForModification(self):
        # checks to see if mod was modified on disk, and prompt to reload if it was.
        self.OnSetFocus()

    def ChangeNotify(self, changed=1):
        if not self.mod:
            return 0

        hasAst = (self.GetTitle()[-2:] == ' *')
        #print "changenotify", changed, self.changed, hasAst, self.GetTitle()
        if changed and not hasAst:
            self.mod.flagChange(1)
            self.SetTitle(self.GetTitle() + " *")
            self.changed = 1
        elif not changed and hasAst:
            self.mod.flagChange(0)
            title = self.GetTitle()
            if title[-2:] == " *":
                self.SetTitle(self.GetTitle()[:-2])
            self.changed = 0
        
    # WDR: methods for ITDocDialog

    def GetTrackListControl(self):
        return self.FindWindowById(ID_LISTBOX_TRACKS)

    def GetPatternListControl(self):
        return self.FindWindowById(ID_LISTBOX_PATTERNS)

    def GetSpeedControl(self):
        return self.FindWindowById(ID_ITDOC_SPEED)

    def GetTempoControl(self):
        return self.FindWindowById(ID_SPINCTRL_TEMPO)

    def GetGlobalVolumeControl(self):
        return self.FindWindowById(ID_SPINCTRL_GLOBAL_VOLUME)

    def GetMixingVolumeControl(self):
        return self.FindWindowById(ID_SPINCTRL_MIXING_VOLUME)

    def GetNameControl(self):
        return self.FindWindowById(ID_ITDOC_NAME)

    def GetOrderListControl(self):
        return self.FindWindowById(ID_TEXTCTRL_ORDERLIST)

    def GetOrderListControl(self):
        return self.orderListControl
        #return wx.PyTypeCast( self.FindWindowById(ID_ORDERLIST), "OrderListControl" )


    def GetInstrumentListControl(self):
        ctl = self.FindWindowById(ID_LISTBOX_INSTRUMENTS)
        return ctl

    def GetSampleListControl(self):
        ctl = self.FindWindowById(ID_LISTBOX_SAMPLES)
        #ctl.__class__ = wxListControl
        return ctl

    def GetNameControl(self):
        return self.FindWindowById(ID_ITDOC_NAME)

    def GetFnameControl(self):
        return self.FindWindowById(ID_ITDOC_FNAME)

    def SetSamples(self, samplelist):
        list = self.GetSampleListControl()
        list.Clear()
        i = 0
        for x in samplelist:
            list.Append(x)

    def SetInstruments(self, instrumentlist):
        list = self.GetInstrumentListControl()
        list.Clear()
        for x in instrumentlist:
            list.Append(x)

    def SetPatterns(self, patternlist):
        list = self.GetPatternListControl()
        list.Clear()
        for x in patternlist:
            list.Append(x)

    def SetTracks(self, tracklist):
        #print tracklist
        list = self.GetTrackListControl()
        list.Clear()

        i = 0
        for name in tracklist:
            if name[0] == "^":
                list.Append(name[4:])
                list.SetItemForegroundColour(i, wx.Colour(ord(name[1]), ord(name[2]), ord(name[3]))) # 200, 200, 200
            else:
                list.Append(name)
                list.SetItemForegroundColour(i, wx.Colour(*options.Colors["defaultTrackName"]))
            i += 1

        
    def SetOrderListText(self, st):
        ctl = self.GetOrderListControl()
        ctl.SetLabel(st)

    def SetOrderList(self, orderlist):
        ctl = self.GetOrderListControl()
        display = str(orderlist)[1:-1]
        display = string.replace(display, "255, 255", "255")
        display = string.replace(display, "255", "END")
        if display == "END":
            #display = "None"
            display = "END"
        
        if ctl:
            ctl.SetLabel(display)


    def SetTempo(self, tempo):
        ctl = self.GetTempoControl()
        ctl.SetValue(tempo)

    def SetSpeed(self, speed):
        ctl = self.GetSpeedControl()
        ctl.SetValue(speed)

    def SetGlobalVolume(self, vol):
        ctl = self.GetGlobalVolumeControl()
        ctl.SetValue(vol)

    def SetMixingVolume(self, vol):
        ctl = self.GetMixingVolumeControl()
        ctl.SetValue(vol)

    def SetName(self, name):
        ctl = self.GetNameControl()
        ctl.SetLabel(str(name))

    def SetFilename(self, fname):
        ctl = self.GetFnameControl()
        ctl.SetLabel(fname)

    def GetFilename(self):
        ctl = self.GetFnameControl()
        return ctl.GetLabel()

    def GetSelection(self):
        # returns patterns, tracks, instruments, and samples selected
        pass
        
    def Save(self):
        if not self.mod:
            return 0

        #print "Save"
        savetitle = self.GetTitle()
        newfname = self.GetFilename()
        newfname = filenamer.requireExt(newfname, ".it")
        self.SetTitle("saving " + newfname + "...")
        error = self.mod.save(newfname, backupPath=options.BackupPath)
        if error:
            wx.MessageBox( error, "Error saving file to " + newfname)
            self.SetTitle(savetitle)
        else:
            self.SetTitle(newfname)
            self.SetFilename(newfname)
            self.changed = 1
            self.ChangeNotify(changed=0)

        app.CleanBackups()        

    def Load(self, path):
        savetitle = self.GetTitle()
        self.SetTitle("Loading " + path + "...")
        try:
            newmod = ITDocument(path, player=modplayer.getPlayer())
        except IOError:
            newmod = None
            error = string.replace(str(sys.exc_value), "\\\\", "\\")
            self.SetTitle(savetitle)
            wx.MessageBox( error, "Error loading file " + path)

        if newmod:            
            del self.mod
            self.mod = newmod
            if self.orderListControl:
                self.orderListControl.attach(newmod)
            self.SetTitle(self.mod.realFile)
            self.SetFilename(self.mod.realFile)

    def SetTitle(self, title):
        self.GetGrandParent().SetTitle(title)

    def GetTitle(self):
        return self.GetGrandParent().GetTitle()

    # WDR: handler implementations for ITDocDialog

    def OnVolumeSlider(self, event):
        if self.mod:
            volume = event.GetInt()
            self.mod.setVolume(volume)

    def OnSelectProcessMode(self, event):
        return
        print event.GetString(), event.GetSelection()
        if event.GetString() == "Whole File":
            self.ITDocSelectionSizer.SetDimension(0,0,0,0)
            self.ITDocSelectionSizer.Layout()

    def Reload(self):
        # what about musics?
        if self.mod:
            self.mod.reloadEditFile()
            self.Update()
            self.ChangeNotify(1)        

    def OnSetFocus(self, event=None):
        if not self.SettingFocus:
            self.SettingFocus = 1
            if hasattr(self, "mod") and self.mod and self.mod.checkModified():
                # module has later modification time than it did when loaded
                reload = wx.MessageBox(self.mod.realFile + " was modified!  Reload it now?", self.mod.realFile, wxYES_NO)
                if reload == wxYES:
                    self.Reload()
                    self.ChangeNotify(0)
                self.mod.updateModification()
        self.SettingFocus = 0

    def OnTempoChanged(self, event):
        if self.mod:
            self.OnSpinChanged(event)
            self.mod.setTempo(self.GetControlValue("Tempo"))

    def OnSpeedChanged(self, event):
        if self.mod:
            self.OnSpinChanged(event)
            self.mod.setSpeed(self.GetControlValue("Ticks"))

    def OnGlobalVolumeChanged(self, event):
        if self.mod:
            self.OnSpinChanged(event)
            self.mod.setGlobalVolume(self.GetControlValue("GlobalVolume"))

    def OnMixingVolumeChanged(self, event):
        if self.mod:
            self.OnSpinChanged(event)
            self.mod.setMixingVolume(self.GetControlValue("MixingVolume"))


    def OnSpinChanged(self, event):
        self.ChangeNotify()
        self.savework = 1

    def OnTextChanged(self, event):
        self.ChangeNotify()
        self.savework = 1
        

    def ClearAllSelections(self, keep=[]):
        # if list controls in keep, they will not be cleared.
        lists = self.GetSampleListControl(), self.GetInstrumentListControl(), self.GetPatternListControl(), self.GetTrackListControl()
        for list in lists:
            if list and list not in keep:
                #list.DeselectAll()
                for i in list.GetSelections():
                    list.Deselect(i)


    def OnInstrumentsListbox(self, event):
        if not self.mod:
            return 0

        samplelist = self.GetSampleListControl()
        inslist = self.GetInstrumentListControl()
        instruments = inslist.GetSelections()

        self.ClearAllSelections(keep=[inslist])

        # deselect all selected samples
        #numsamps = samplelist.Number()
        #for x in range(numsamps):
        #    samplelist.Deselect(x)

        # now select all samples used by all selected instruments            
        for i in instruments:
            used = self.mod.instruments[i].usedSamples()
            vs = self.mod.validSamples()
            for u in used:
                if u-1 in vs:
                    idx = vs.index(u-1)
                    samplelist.SetSelection(idx, 1)
            #print i, "uses samples", self.mod.instruments[i].usedSamples()

    def OnSamplesListbox(self, event):
        samplelist = self.GetSampleListControl()
        self.ClearAllSelections(keep=[samplelist])

    def OnPatternsListbox(self, event):
        list = self.GetPatternListControl()
        self.ClearAllSelections(keep=[list])

    def OnTracksListbox(self, event):
        list = self.GetTrackListControl()
        self.ClearAllSelections(keep=[list])

    def OnSamplesListboxOld(self, event):
        if self.mod and self.mod.usesInstruments:
            self.OnInstrumentsListbox(event)
            return
        
        samplelist = self.GetSampleListControl()
        inslist = self.GetInstrumentListControl()
        samples = samplelist.GetSelections()

        # deselect all selected instruments
        numins = inslist.Number()
        for x in range(numins):
            inslist.Deselect(x)


    def OnSaveAs(self, event=None):
        if self.suggestedFile:
            defaultFile = self.suggestedFile
        elif self.mod:
            defaultFile = self.mod.getRealFile()
        else:
            defaultFile = None
        path = wxx.SelectFile(self, ext="*.it", defaultFile=defaultFile, saving=1, multi=0, pathtype="it")
        if path:
            error = self.mod.save(path, backupPath=options.BackupPath)
            self.suggestedFile = None
            if error:
                wx.MessageBox( error, "Error saving file to " + path)
            else:                
                self.SetTitle(path)
                self.SetFilename(self.mod.realFile)
                self.ChangeNotify(changed=0)
                app.CleanBackups()

                if path.find(options.TempPath) == -1:
                    options.addRecentFile(path)
                    #TODO: just get top level
                    self.GetParent().GetGrandParent().UpdateRecentFiles()            


    def OnRenderFinished(self, fname, console):
        console.SetTitle("Finished Rendering" + fname)
        self.GetParent().SetStatusText("Finished Rendering " + fname)
        console.Close()

    def OnRender(self, event):
        if not self.mod:
            return 0

        if not (self.mod.numPatterns() and self.mod.numSamples()):
            wx.MessageBox("Nothing to Render!", "Blank File", parent=self.GetParent())
            return 0
        
        self.TransferDataFromWindow()
        self.mod.saveWork()
        self.savework = 0


        #savefname = wxx.SelectFile(self, defaultFile=outname, ext="*.wav", pathtype="render")
        #if not savefname:
        #    return 0
        #outname = savefname

        fname = self.mod.getEditFile()
        
        if self.suggestedFile:
            outname = filex.pathjoin(pathmemory.get("render"), os.path.basename(self.suggestedFile))
        else:
            outname = self.mod.getRealFile()
            outname = filex.pathjoin(pathmemory.get("render"), os.path.basename(outname))

        outname = filex.replaceExt(outname, ".wav")

        # if orderlist is empty, create copy of mod and unfold the copy, and use that file for the render.
        fname, numorders = it.makePlayableCopy(fname, os.path.splitext(fname)[0]+"-render.it")

        currentTrackSettingsFunc = self.mod.getCurrentTrackSettings

        dlg = RenderSingleDialog(self.GetMainWindow().GetParent(), -1, "Render to WAV", filelist=[fname])
        dlg.SetCurrentTrackSettingsFunc(currentTrackSettingsFunc)
        dlg.SetCallbacks(self.RenderCallback, self.PreProcessCallback, self.PostProcessCallback)
        #dlg.SetCallbacks(None, None, None)
        dlg.SetOutfile(outname)
        dlg.ShowModal()
        pathmemory.set("render", os.path.dirname(dlg.outfile))


    def OnExport(self, event):
        self.OnExportSamples(event)

    def OnSplit(self, event):
        self.OnBatchSplit(event)

    def OnTrackKeydown(self, event):
        # ignore other space key downs on the track list
        if event.GetKeyCode() == 32:
            self.OnTrackChar(event, char=' ')
        else:
            event.Skip()

    def OnTrackChar(self, event, char=None):
        if not self.mod:
            return 0

        tracks = self.GetSelectedTracks()
        skip = 1

        if not char:
            char = event.GetKeyCode()

            if char <= 255:
                char = string.upper(chr(char))

        if char == chr(10):
            list = self.GetTrackListControl()
            self.focusControl = list
            self.OnContextSplitLoadTracks(None)

        elif char in (" ","T"):
            self.ChangeNotify()
            skip = 0
            self.mod.initPlayback()
            tracks = self.GetSelectedTracks()
            self.ToggleTracks(tracks)

        elif char == "M":
            self.ChangeNotify()
            self.mod.initPlayback()
            tracks = self.GetSelectedTracks()
            #print ".. muting", tracks
            self.MuteTracks(tracks)

        elif char == "S":
            #self.ChangeNotify()
            self.mod.initPlayback()
            tracks = self.GetSelectedTracks()
            #print ".. soloing", tracks
            self.SoloTracks(tracks)
            
        if skip:
            event.Skip()


    def UpdateTrackNamesWithColors(self, tracks):
        for track in tracks:
            name = self.mod.getTrackName(track)
            list = self.GetTrackListControl()
            if name[0] == "^":
                list.SetItemForegroundColour(track, wx.Colour(ord(name[1]), ord(name[2]), ord(name[3]))) # 200, 200, 200
                name = name[4:]
            else:
                list.SetItemForegroundColour(track, wx.Colour(*options.Colors["defaultTrackName"]))
            list.SetString(track, name)


    def ToggleTracks(self, tracks):
        self.mod.toggleTracks(tracks)
        self.GetMixerDialog().UpdateMixer(tracks)
        self.UpdateTrackNamesWithColors(tracks)
        
    def MuteTracks(self, tracks):
        self.mod.muteTracks(tracks)
        self.GetMixerDialog().UpdateMixer(tracks)
        list = self.GetTrackListControl()
        self.UpdateTrackNamesWithColors(tracks)


    def SoloTracks(self, tracks):
        self.mod.soloTracks(tracks)
        self.GetMixerDialog().UpdateMixer(tracks)
        lst = self.GetTrackListControl()
        for track in tracks:
            name = self.mod.getTrackName(track)
            if name[0] == "^":
                lst.SetString(track, name[4:])
                lst.SetItemForegroundColour(track, wx.Colour(ord(name[1]), ord(name[2]), ord(name[3]))) # 200, 200, 200
                name = name[4:]
            else:
                lst.SetString(track, name)
                lst.SetItemForegroundColour(track, wx.Colour(*options.Colors["defaultTrackName"]))
        



                
        
    def OnPatternChar(self, event):
        char = event.GetKeyCode()
        event.Skip()

        if char == 10:
            list = self.GetPatternListControl()
            self.focusControl = list
            self.OnContextSplitLoadPatterns(None)

        if char <= 255:
            char = string.upper(chr(char))

        if char == ' ':

            list = self.GetPatternListControl()
            selection = list.GetSelections()
            if selection:
                selection = selection[0]
                self.PlayPattern(selection, setfocus=1)

        
    def PlayPattern(self, pattern, setfocus=0):
        if not self.mod:
            return 0

        if self.savework:
            #print ".. saving work"
            self.TransferDataFromWindow()
            self.mod.saveWork()
            self.savework = 0

        self.mod.playPattern(pattern, notifyCallback = self.OnNotifyPosition)

        if setfocus:
            pl = self.GetPatternListControl()
            pl.SetFocus()

        return

    def OnInstrumentChar(self, event):
        char = event.GetKeyCode()
        event.Skip()

        if not self.mod:
            return

        if char == 10:
            list = self.GetInstrumentListControl()
            self.focusControl = list
            self.OnContextSplitLoadInstruments(None)
            return

        if char <= 255:
            char = chr(char).upper()
        list = self.GetSampleListControl()

        if char in pitchkeymap.keymap or char == ' ':
            instrus = list.GetSelections()
            if instrus:
                for index in instrus:
                    try:
                        note = pitchkeymap.itkeymap.get(char, 0)
                        notename = pitchkeymap.notenames[note]
                        SetStatusText(notename)
                    except:
                        pass

                    #print "playing instrument"
                    self.mod.playNote(note, index)
                    
            

    def OnSampleChar(self, event):
        char = event.GetKeyCode()
        event.Skip()

        if not self.mod:
            return

        
        if char <= 255:
            char = chr(char).upper()
        list = self.GetSampleListControl()

        if char in pitchkeymap.keymap or char == ' ':
            samples = list.GetSelections()
            validSamples = self.mod.validSamples()
            if samples:
                #samples = [samples[0]]
                for index in samples:
                    index = validSamples[index]
                    if not index in self.__loadedSamples:
                        #print "loading", index
                        fname = self.mod.exportSomeSamples(filex.GetPath83(options.TempPath), index)[0]
                        #print "loaded", fname
                        if fname:
                            self.__loadedSamples[index] = fname
                    if index in self.__loadedSamples:
                        fname = self.__loadedSamples[index]
                        #print "getting keymap for", self.mod.samples[index].c5speed
                        #keymap = pitchkeymap.getkeymap(self.mod.samples[index].c5speed)
                        try:
                            note = pitchkeymap.itkeymap.get(char, 0)
                            notename = pitchkeymap.notenames[note]
                            SetStatusText(notename)
                        except:
                            pass

                        try:
                            freq = pitchkeymap.itRateFromKey(char, self.mod.samples[index].c5speed)
                        except:
                            freq = -1
                        if not freq:
                            freq = -1
                        #freq = keymap.get(char, -1)
                        #print "playing", os.path.basename(fname), "freq", freq
                        modplayer.getPlayer().start()

                        # sample play                        
                        self.samplePlayer.stopLooping()
                        self.samplePlayer.playSample(fname, freq=freq, loop=options.LoopSamples)

        else:
            # handle other chars
            pass
                    
    def OnChar(self, event):
        #print "onchar"
        return
        #print chr(event.GetKeyCode())
        event.Skip()
        ch = event.GetKeyCode()
        if ch < 255:
            ch = string.upper(chr(ch))
        #print "char", ch
        if ch == ' ':
            self.OnPlay(event)            
            return
        
        try:
            self.keyinput += string.upper(ch)
            if len(self.keyinput) > 100:
                self.keyinput = self.keyinput[1:]
            if string.find(self.keyinput, "ANALYZE") > -1:
                self.keyinput = ""
                self.OnAnalyze()
            if string.find(self.keyinput, "FX") > -1:
                #print "FX"
                fx = -1
                if string.find(self.keyinput, "FX1") > -1:
                    fx = basslib.FXLIST[0]
                if string.find(self.keyinput, "FX2") > -1:
                    fx = basslib.FXLIST[1]
                if string.find(self.keyinput, "FX3") > -1:
                    fx = basslib.FXLIST[2]
                if string.find(self.keyinput, "FX4") > -1:
                    fx = basslib.FXLIST[3]
                if string.find(self.keyinput, "FX5") > -1:
                    fx = basslib.FXLIST[4]
                if string.find(self.keyinput, "FX6") > -1:
                    fx = basslib.FXLIST[5]
                if string.find(self.keyinput, "FX7") > -1:
                    fx = basslib.FXLIST[6]
                if string.find(self.keyinput, "FX8") > -1:
                    fx = basslib.FXLIST[7]
                if string.find(self.keyinput, "FX9") > -1:
                    fx = basslib.FXLIST[8]
                if fx > -1:
                    #print "FX", fx
                    modplayer.getPlayer().pause()
                    #print basslib.BASS_ChannelSetFX(self.playingChannel, fx)
                    modplayer.getPlayer().start()
                    self.keyinput = ""

        except:
            traceback.print_exc()
            pass

    def OnAnalyze(self):
        output = it.fxstats(mod=self.mod)
        print output

    def OnSize(self, event):
        if not self.closed:
            event.Skip()

    def OnClose(self, event):

        #if self.floating:
        #    print "floating"
        #    # don't close, just reparent
        #    self.floating = 0
        #    if self.parent:
        #        print "reparenting"
        #        self.Reparent(self.parent)
        #        self.parent.Refresh()
        #    return
        
        #if self.playingChannel:
        #    BASS.closeChannel(self.playingChannel)

        self.Show(0)

        if self.mod:
            self.mod.stop(1)
            self.mod.close()

        if self.channels:
            modplayer.getPlayer().closeChannels(self.channels)

        # stop any playing samples and free all loaded samples
        self.samplePlayer.close()            

            
        try:
            del self.mod
        except:
            pass

        self.mod = None

        event.Skip()
        self.closed = 1
        #self.Destroy()

    def SetPlayButton(self, label="play"):
        self.SetControlLabel("PlayButton", label)

    def GetPlayButtonLabel(self):
        return self.GetControlLabel("PlayButton")

    def OnPlayFinished(self):
        #print "stopped channel"
        #self.SetPlayButton("play")
        pass

    def OnStop(self, event):
        if not self.mod:
            return 0
        
        self.mod.stop()
        self.samplePlayer.stop()

    def OnNotifyPosition(self, order, row, seconds=0):
        #print order, row

        #TODO: threadsafe?
        
        try:
            self.orderListControl.highlight(order)

            self.TimePosition.SetLabel(string.zfill(seconds / 60, 2) + ":" + string.zfill(seconds % 60, 2))
            self.StatusText.SetLabel(string.zfill(order, 3) + ":" + string.zfill(row, 3))
        except:
            # dead object
            pass

    def OnPlay3(self, event):
        wxx.PleaseWaitFunc("Initializing playback...", self.OnPlay2, (event,))

    def PlayOrder(self, order, pattern, usepattern=0):
        self.OnPlay(None, order, pattern, usepattern=usepattern)

    def OnPlay(self, event, order=0, pattern=None, row=0, usepattern=0):
        if not self.mod:
            return 0
        if not (self.mod.numPatterns() and self.mod.numSamples()):
            wx.MessageBox("Nothing to Play!", "No Patterns and/or Samples", parent=self.GetParent())
            return 0
        #if self.mod.changed:
        self.TransferDataFromWindow()
        self.mod.saveWork()
        self.savework = 0

        if not options.UseExternalPlayer:
            if usepattern and pattern != None:
                if not order:
                    order = -1
                self.mod.playPattern(pattern, self.OnNotifyPosition, order=order)
            else:
                self.mod.play(self.OnNotifyPosition, order=order, row=row)
            return                

        fname = self.mod.getEditFile()
        fname, numorders = it.makePlayableCopy(fname, filenamer.uniqueFilename(fname))
                
        if options.UseExternalPlayer and options.ExternalPlayer:
            try:
                win32api.ShellExecute(0, "open", options.ExternalPlayer, fname, os.path.dirname(self.mod.realFile), 1)
            except:
                wx.MessageBox("Unable to execute " + options.ExternalPlayer + ".  Try selecting a different player in Options / Preferences.", "Error running player")
        elif options.UseExternalPlayer:
            try:
                win32api.ShellExecute(0, "open", fname, None, os.path.dirname(self.mod.realFile), 1)
            except:
                wx.MessageBox("Unable to play file with default system player.  Try specifying an external player in Options / Preferences.", "No Default Player")
        

    def OnSave(self, event=None):
        #print "OnSave", self.mod, self.mod.path
        #print ".. save", self.mod.orderList(), self.mod, self.mod.getName()
        if not self.mod or self.mod.path == "" or self.mod.realFile == "New IT":
            self.OnSaveAs(event)
        else:
            self.TransferDataFromWindow()
            self.Save()


    def ProcessCallback(self, st):
        # append processed filename to new batch window        
        try:
            if self.newWindow:
                self.newWindow.AddFile(st)
        except:
            pass

    def RenderCallback(self, st):
        # append processed filename to new batch window        
        try:
            if self.newWindow:
                if string.find(st, ".wav") > -1 and st[0:2] != "--":
                    self.newWindow.AddFile(st)
        except:
            pass


    def PreProcessCallback(self):
        #diag = self.GetParent().NewFileBatch("Exported Files", focus=0, show=0)
        #diag.Raise()
        #diag.Show(0)
        #self.newWindow = diag
        self.newWindow = None

    def PostProcessCallback(self):
        try:
            if self.newWindow:
                self.newWindow.Autosize()
                self.newWindow.Raise()
                self.newWindow.CentreOnParent()
                self.newWindow.SetFocus()
                self.newWindow.Show(1)
        except:
            pass

    def OnUnfold(self, event):
        if not self.mod:
            return 0
        if not self.mod.numPatterns():
            wx.MessageBox("Nothing to Unfold!", "No Patterns", parent=self.GetParent())
            return 0

        #self.SetOrderListText("Unfolding, Please Wait...")
        wxx.Yield()
        #TODO: seperate thread?
        wxx.PleaseWaitFunc("Unfolding, Please Wait...", self.mod.unfold)
        self.Update(0)
        self.ChangeNotify()

    def OnRemoveUnusedSamples(self, event=None):
        if not self.mod:
            return 0
        if not self.mod.numSamples():
            wx.MessageBox("Nothing to Remove!", "No Samples", parent=self.GetParent())
            return 0

        removed = self.mod.optimizeSamples()
        self.Update(0)
        wx.MessageBox("Removed " + str(removed) + " samples.", "Samples Removed", parent=self)

    # Context Menu Methods

    def OnContextSplitLoad(self, event, selection, mode, cache=0):
        # mode should be "Pattern", "Track" or "Instrument"
        savefocus = wx.Window_FindFocus()        

        if selection:
            selection = selection[0]
            if mode[0] + str(selection) not in self.prepared:
                wxx.PleaseWaitFunc("Extracting " + mode + " " + str(selection) + "...", self.OnContextSplitLoad2, (event,selection,mode))
                if cache:
                    self.prepared.append(mode[0] + str(selection))
            else:
                self.OnContextSplitLoad2(event, selection, mode)

        try:
            savefocus.GetParent().RestoreFocus(savefocus)
        except:
            try:
                savefocus.RestoreFocus(savefocus)
            except:
                pass

    def OnContextSplitLoad2(self, event, selection, mode):
        if not self.mod:
            return 0

        splitter = ITSplitter(filelist=[], path=options.TempPath, exportMode="Ignore", optimize=0, ordersOnly=0, splitPrefixes=[mode[0].lower()])
        if mode == 'Pattern':
            usename, outname = splitter.SplitByPatterns(self.mod, self.mod.path, x=selection)
        elif mode == 'Track':
            usename, outname = splitter.SplitByTrack(self.mod, self.mod.path, x=selection)
        elif mode == 'Instrument':
            usename, outname = splitter.SplitByInstrument(self.mod, self.mod.path, x=selection)

        newTitle = os.path.basename(self.mod.getRealFile()) + " - " + mode + " " + str(selection)
            
        if usename:
            if usename[0] == '*':
                usename = usename[1:]
            dlg = self.GetMainWindow().GetParent().FileOpen(event, path=usename, makenew=1)

            # set new song title
            dlg.mod.setName(newTitle)
            #dlg.Update(0) - not needed, it's already called.
            if mode in ('Track','Instrument'):
                selection += 1
            dlg.GetITDialog().suggestedFile = os.path.splitext(os.path.basename(self.mod.getRealFile()))[0] + "-" + mode[0].lower() + str(selection) + ".it"



    # Instrument Context Menu Methods
    
    def GetSelectedInstruments(self):
        list = self.GetInstrumentListControl()
        selections = list.GetSelections()
        return selections

    def GetSelectedInstrumentNames(self):
        list = self.GetInstrumentListControl()
        selections = list.GetSelections()
        names = [list.GetString(i) for i in selections]
        return names

    def OnContextSplitLoadInstruments(self, event):
        selection = self.GetSelectedInstruments()
        self.OnContextSplitLoad(event, selection, "Instrument")

    def OnContextRenderInstruments(self, event):
        self.OnContextSplitInstruments(event, render=1)

    def OnContextSplitInstruments(self, event, render=0):
        toSplit = self.GetSelectedInstruments()
        if render:
            title = "Render Instrument Sequences"
            selst = "Selected for Render:"
        else:
            title = "Split Instrument Sequences"
            selst = "Selected for Split:"
        if toSplit:
            names = self.GetSelectedInstrumentNames()
            startMessage = [selst] + names
            self.OnBatchSplit(event, toSplit=toSplit, startMessage=startMessage, render=render, title=title, split1=SELECT_SPLIT_INSTRUMENTS, solosplit=1)
        else:
            self.OnBatchSplit(event, startMessage=["All Instruments Selected"], render=render, split1=SELECT_SPLIT_INSTRUMENTS, solosplit=1)

    def OnContextDeleteInstruments(self, event):
        if not self.mod:
            return 0

        ins = self.GetSelectedInstruments()
        for index in ins:
            self.mod.instruments[index] = it.ITInstrument()
        self.Update(0)
        self.ChangeNotify()
        self.savework = 1   # request to savework before playback

        #TODO:MPEDIT: instead of this, make modplug handle samples updateable
        modplayer.lockPlayer()
        player = modplayer.getPlayer()
        if player.realtimeEditing():
            self.mod.saveWork()
            self.mod.reloadHandles()


    # Track Context Menu Methods

    def GetSelectedTracks(self):
        tlist = self.GetTrackListControl()
        selections = tlist.GetSelections()
        return selections

    def GetSelectedTrackNames(self):
        tlist = self.GetTrackListControl()
        selections = tlist.GetSelections()
        names = [tlist.GetString(i) for i in selections]
        return names

    def OnContextDeleteTracks(self, event):
        pass

    def OnContextPlayTracks(self, event):
        pass

    def OnContextSoloTracks(self, event):
        if not self.mod:
            return 0

        self.mod.initPlayback()
        tlist = self.GetTrackListControl()
        selections = tlist.GetSelections()
        self.SoloTracks(selections)

    def OnContextMuteTracks(self, event):
        if not self.mod:
            return 0

        self.mod.initPlayback()
        tlist = self.GetTrackListControl()
        selections = tlist.GetSelections()
        self.MuteTracks(selections)


    def OnContextUnmuteTracks(self, event):
        if not self.mod:
            return 0

        self.mod.initPlayback()
        self.mod.unmuteTracks()
        #self.UpdateTrackStatusNames()
        self.GetMixerDialog().UpdateMixer()

        tlist = self.GetTrackListControl()
        num = tlist.GetCount()
        self.UpdateTrackNamesWithColors(range(num))

    def OnContextUnsoloTracks(self, event):
        if not self.mod:
            return 0

        self.mod.initPlayback()
        self.mod.unSoloTracks()
        #self.UpdateTrackStatusNames()

        self.GetMixerDialog().UpdateMixer()

        tlist = self.GetTrackListControl()
        num = tlist.GetCount()
        self.UpdateTrackNamesWithColors(range(num))




    def UpdateTrackStatusNames(self):
        if not self.mod:
            return 0

        tlist = self.GetTrackListControl()
        num = tlist.GetCount()
        for i in range(num):
            name = self.mod.getTrackName(i)
            tlist.SetString(i, name)
        


    def OnContextSplitLoadTracks(self, event):
        selection = self.GetSelectedTracks()
        self.OnContextSplitLoad(event, selection, "Track")

    def OnContextRenderTracks(self, event):
        self.OnContextSplitTracks(event, render=1)

    def OnContextSplitTracks(self, event, render=0):
        toSplit = self.GetSelectedTracks()
        if render:
            title = "Render Track Sequences"
            selst = "Selected for Render:"
        else:
            title = "Split Track Sequences"
            selst = "Selected for Split:"
        if toSplit:
            names = self.GetSelectedTrackNames()
            startMessage = [selst] + names
            self.OnBatchSplit(event, toSplit=toSplit, startMessage=startMessage, render=render, title=title, split1=SELECT_SPLIT_TRACKS, solosplit=1)
        else:
            self.OnBatchSplit(event, startMessage=["All Tracks Selected"], render=render, split1=SELECT_SPLIT_TRACKS, solosplit=1)

    # Pattern Context Menu Methods

    def GetSelectedPatterns(self):
        plist = self.GetPatternListControl()
        selections = plist.GetSelections()
        return selections

    def GetSelectedPatternNames(self):
        plist = self.GetPatternListControl()
        selections = plist.GetSelections()
        names = [plist.GetString(i) for i in selections]
        return names


    def OnContextRenderPatterns(self, event):
        self.OnContextSplitPatterns(event, render=1)

    def OnContextSplitPatterns(self, event, render=0):
        toSplit = self.GetSelectedPatterns()
        if render:
            title = "Render Pattern Sequences"
            selst = "Selected for Render:"
        else:
            title = "Split Pattern Sequences"
            selst = "Selected for Split:"
        if toSplit:
            names = self.GetSelectedPatternNames()
            startMessage = [selst] + names
            self.OnBatchSplit(event, toSplit=toSplit, startMessage=startMessage, render=render, title=title, split1=SELECT_SPLIT_PATTERNS, solosplit=1)
        else:
            self.OnBatchSplit(event, startMessage=["All Patterns Selected"], render=render, split1=SELECT_SPLIT_PATTERNS, solosplit=1)

    def OnContextSplitLoadPatterns(self, event):
        selection = self.GetSelectedPatterns()
        self.OnContextSplitLoad(event, selection, "Pattern")

    def OnPlayPattern(self, event):
        self.OnContextPlayPatterns(event)

    def OnContextPlayPatterns(self, event):

        selection = self.GetSelectedPatterns()
        if selection:
            selection = selection[0]
            self.PlayPattern(selection)
        else:
            self.OnPlay(event)

    def OnContextDeletePatterns(self, event):
        if not self.mod:
            return 0

        patterns = self.GetSelectedPatterns()
        self.mod.deletePatternsData(patterns)
        self.Update(0)
        self.ChangeNotify()
        self.savework = 1   # request to savework before playback

    # Sample Context Menu Methods

    def GetSelectedSamples(self):
        if not self.mod:
            return 0

        samplelist = self.GetSampleListControl()
        selections = samplelist.GetSelections()
        valid = self.mod.validSamples()
        samples = [valid[i] for i in selections]
        return samples

    def GetSelectedSampleNames(self):
        samplelist = self.GetSampleListControl()
        selections = samplelist.GetSelections()
        names = [samplelist.GetString(i) for i in selections]
        return names

    def OnContextShuffleSamples(self, event):
        if not self.mod:
            return 0

        samples = self.GetSelectedSamples()
        self.mod.sampleShuffle(samples)
        self.Update(0)
        self.ChangeNotify()
        self.savework = 1   # request to savework before playback
        self.__loadedSamples = {}

        #TODO:MPEDIT: instead of this, make modplug handle samples updateable
        modplayer.lockPlayer()
        player = modplayer.getPlayer()
        if player.realtimeEditing():
            self.mod.saveWork()
            self.mod.reloadHandles()


        #self.mod.saveWork()

    def OnContextMixSamples(self, event):
        pass

    def OnContextDeleteSamples(self, event):
        if not self.mod:
            return 0

        samples = self.GetSelectedSamples()
        for index in samples:
            self.mod.samples[index] = it.ITSample()
        self.Update(0)
        self.ChangeNotify()
        self.savework = 1   # request to savework before playback

        #TODO:MPEDIT: instead of this, make modplug handle samples updateable
        modplayer.lockPlayer()
        player = modplayer.getPlayer()
        if player.realtimeEditing():
            self.mod.saveWork()
            self.mod.reloadHandles()


    
    def OnContextExportSamples(self, event):
        samples = self.GetSelectedSamples()
        if samples:
            names = self.GetSelectedSampleNames()
            startMessage = ["Selected for Export:"] + names
            self.OnExportSamples(event, samples, startMessage)
        else:
            self.OnExportSamples(event)

    # Other Methods

    def OnExportSamples(self, event, samples=[], startMessage=[""]):
        if not self.mod:
            return 0
        if not self.mod.numSamples():
            wx.MessageBox("Nothing to Export!", "No Samples", parent=self.GetParent())
            return 0

        title = self.GetTitle()
        if samples:
            title = "Export Selected Samples - " + title
        else:
            title = "Export Samples - " + title
            
        diag = SampleExportDialog(self.GetMainWindow().GetParent(), -1, title, samples=samples, startMessage=startMessage, files=self.GetFileList())
        diag.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
        diag.ShowModal()

    def PrepareForSplitting(self):
        if not self.mod:
            return 0

        # prepare ourself for splitting and return our edit file list and output filenames
        self.TransferDataFromWindow()
        self.mod.saveWork()
        self.savework = 0

        fname = self.mod.getEditFile()
        files = [fname]

        newfilenames = {fname: self.mod.getRealFile()}

        return files, newfilenames        
        

    def OnBatchSplit(self, event, toSplit=[], startMessage=[""], render=None, title="Split Sequences", split1=None, solosplit=0):
        if not self.mod:
            return 0
        if not self.mod.numPatterns():
            wx.MessageBox("Nothing to Split!", "No Patterns", parent=self.GetParent())
            return 0

        title2 = self.GetTitle()
        self.data = [self.mod.realFile]

        # getFilesFunc is passed to the splitter to do the prep work only once splitting has begun.
        # it is used by the splitter to get what otherwise would be passed as the "files" and "newfilenames" arguments.
        getFilesFunc = self.PrepareForSplitting

        #104DEL: files = self.GetFileList()
        #self.Enable(0)

        # this function will be used to get track volume and panning settings if the
        # UseCurrentVolumes option is used.
        currentTrackSettingsFunc = self.mod.getCurrentTrackSettings

        diag = ITSplitterDialog(self.GetMainWindow().GetParent(), -1, title + " - " + title2, toSplit=toSplit, startMessage=startMessage, render=render, split1=split1, solosplit=solosplit, getFilesFunc=getFilesFunc, currentTrackSettingsFunc=currentTrackSettingsFunc)
        diag.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
        #diag.Show(True)
        diag.ShowModal()
        #self.Lower()

    def GetFileList(self):
        if not self.mod:
            return []

        return [self.mod.getRealFile()]




class ITDocDialogMulti(wx.MDIChildFrame, wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE, path=None, makenew=0):
        wx.MDIChildFrame.__init__(self, parent, id, title, pos, size, style  )
        # wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWFRAME)
        #print "wf", wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWFRAME), wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        #self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        #self.orderListControl = OrderListControl(self, ID_ORDERLIST) - now created in postmod_wdr
        
        self.Show(0)
        #ITDocument2Dialog2Func( self, True )
        sizer = ITDocumentMultiFunc( self, 0 )

        self.notebook = self.GetNotebook()

        wxx.Yield()
        #self.itmain = ITDocDialog(self.notebook, -1, "IT", path=path, makenew=makenew)
        self.itmain = ITDocDialog(self.notebook, -1, "IT", makenew=makenew)

        self.notebook.AddPage(self.itmain, "IT")

        sizer.Fit( self )
        sizer.SetSizeHints( self )

        wxx.Yield()

        #print "mod", self.itmain.mod
        #self.mixer = ModMixerDialog(self.notebook, -1, mod=self.itmain.mod)
        self.mixer = ModMixerDialog(self.notebook, -1)
        self.notebook.AddPage(self.mixer, "Mixer")

        self.Show(1)

        wxx.Yield()

        self.itmain.loadMod(path, makenew=makenew)

        wxx.Yield()

        self.mixer.Show(0)
        self.mixer.SetMod(self.itmain.mod)
        self.mixer.Layout()
        self.mixer.Update()
        #self.mixer.Show(1)

        self.mixer.UpdateMixer()


        
        self.SetIcon(app.icons.itfile)

        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_CLOSE(self, self.OnClose)
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self.notebook, -1, self.OnPageChanged)
        wx.EVT_RIGHT_DOWN(self.notebook, self.OnRightDown)
        #wx.EVT_LEFT_DCLICK(self.notebook, self.OnLeftDoubleClick)


        #self.notebook.SetPageSize((300,500))        

        self.closed = 0


    def OnLeftDoubleClick(self, event):
        # get tab selected and it's page
        t = self.notebook.GetSelection()
        g = self.notebook.GetPage(t)
        # create new window
        f = wx.MDIChildFrame(parent=wx.GetApp().GetTopWindow(), id=-1,
                  title=self.GetTitle() + ' - ' + self.notebook.GetPageText(t),
                  size=g.GetSize(), 
                  style=wx.DEFAULT_FRAME_STYLE
                       |wx.NO_FULL_REPAINT_ON_RESIZE)
        # tear the tab off and refresh
        self.notebook.RemovePage(t)
        self.notebook.Refresh()
        #XXX Reparent() causes errors on GTK
        g.Reparent(f)
        g.floating = 1
        g.parent = self.notebook
        
        # show the torn off page
        f.Show()
        


    def OnRightDown(self, event):

        x, y = event.GetPositionTuple()
        #self.PopupMenu(app.menus.instrumentListContextMenu, wx.Point(x+lstx,y+lsty))
        self.PopupMenu(app.menus.instrumentListContextMenu, wx.Point(x,y))
        return

        # get tab selected and it's page
        t = self.notebook.GetSelection()
        g = self.notebook.GetPage(t)
        # create new window
        f = wx.MDIChildFrame(parent=wx.GetApp().GetTopWindow(), id=-1,
                  title=self.GetTitle() + ' - ' + self.notebook.GetPageText(t),
                  size=g.GetSize(),
                  style=wx.DEFAULT_FRAME_STYLE
                       |wx.NO_FULL_REPAINT_ON_RESIZE)
        # tear the tab off and refresh
        self.notebook.RemovePage(t)
        self.notebook.Refresh()
        #XXX Reparent() causes errors on GTK
        g.Reparent(f)
        # show the torn off page
        f.Show()


    def OnPageChanged(self, event):
        newpage = event.GetSelection()
        if newpage == 0:
            # main page
            self.itmain.SetTrackNames()
        elif newpage == 1:
            # mixer
            self.mixer.UpdateMixer()            
        event.Skip()

    def OnClose(self, event):
        self.Show(0)
        self.itmain.OnClose(event)
        self.closed = 1
        #event.Skip()

    def OnSize(self, event):
        #print "multi", event.GetSize()
        if not self.closed:
            event.Skip()

    def GetNotebook(self):
        return self.FindWindowById(ID_NOTEBOOK)

    def GetCurrentDialog(self):
        #print "! getting current dialog"
        sel = self.notebook.GetSelection()
        if sel > -1:
            dlg = self.notebook.GetPage(sel)
            #fbp = self.children[dlg.GetId()]
            return dlg
        else:
            return None
        #return fbp

    def GetITDialog(self):
        return self.itmain


    def __getattr__(self, key):
        if self.__dict__.has_key('itmain'):
            try:
                return getattr(self.__dict__['itmain'], key)
            except KeyError:
                raise AttributeError
        else:
            return None
    



class WindowHandler:
    def __init__(self, frame=None):
        if frame:
            self.frame = frame
        else:
            global MAINFRAME
            self.frame = MAINFRAME

    def ErrorDialog(self, message=None, send=None, title="I AM ERROR"):
        if send:
            dlg = ErrorSendDialog(self.frame, -1, title, message=message, send=send)
        else:
            dlg = ErrorDialog(self.frame, -1, "I AM ERROR", message=message)
        dlg.ShowModal()
        exit = dlg.exit
        return exit

    def ShowDialog(self, dialogType):
        raise NotImplementedError

    def ShowDialogModal(self, dialogType):
        raise NotImplementedError

    def AddMDIChild(self, dialogType, title="", show=1, focus=1, autosize=0):
        dialog = dialogType(self.frame, -1, title)
        dialog.SetName(title)
        dialog.Autosize()
        dialog.Show(show)
        self.frame.AddChild(dialog)
        return dialog

    # MDI Child
    def NewFileBatch(self, title="File Batch", show=1, fname=None, files=[], focus=1):
        dialog = self.AddMDIChild(FileBatchMultiDialog, title, show, focus, autosize=0)
        if fname:
            dialog.Load(fname)
        if files:
        #    print "adding", files
            dialog.OnAddFiles(None, filelist=files)
            dialog.Autosize()
        return dialog


#from wx.Python.lib import floatbar

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            if file[-2:].lower() == "it":
                wx.GetApp().GetTopWindow().FileOpen(path=file)
            


#PYCRUST:
#from wx.py import shell
#from wx.py.crust import CrustFrame


class PostmodToolBar(wx.ToolBar, dlg_mixer.HasMixerSelection):
    def __init__(self, parent, id, style=wx.CLIP_CHILDREN):
        wx.ToolBar.__init__(self, parent, id, style=style)
        dlg_mixer.HasMixerSelection.__init__(self)
        MainToolBarFunc(self)

        modplayer.addObserver(self)

        r = self.FindWindowById(ID_CHOICE_RENDERER)
        r.SetSelection(0)
        wx.CallAfter(self.updatePlayerControls)

    def update(self, subject):
        wx.CallAfter(self.updatePlayerControls)

        
        
class MainDialog(wx.MDIParentFrame, PostmodApplication):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE, maximize=0 ):
        if not size:
            size = (960, 720)
        if not pos:
            pos = wx.DefaultPosition
        wx.MDIParentFrame.__init__(self, parent, id, title, pos, size, style)
        if maximize:
            self.Maximize()

        wx.InitAllImageHandlers()

        #hwnd = self.GetHandle()
        #import winampsdk2
        #winampsdk2.test2(hwnd)
        
        #print "HWND", hwnd
        #import win32gui
        #win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 2 | 1)

        #MainDialogFunc( self, True )

        #splitter = self.GetSplitter()
        #splitter.SplitHorizontally(wx.Panel(self, -1), wx.Panel(self, -1))

        # set up GUI error handler
        #wxerror.init(self)

        self.menubar = MenuBarFunc()
        self.SetMenuBar(self.menubar)

        #toolbar = self.CreateToolBar(wx.CLIP_CHILDREN)
        #MainToolBarFunc(toolbar)
        toolbar = PostmodToolBar(self, -1)
        self.SetToolBar(toolbar)

        #toolbar = floatbar.wxFloatBar(self, -1)
        #toolbar.SetFloatable(True)
        #toolbar.Float(True)
        #self.SetToolBar(toolbar)

        self.egg = ""
        self.kittens = 0

        #crust = ShellFrame(self, -1, app=self)
        #crust.Show(1)
        
        #menubar.Enable(menubar.FindMenuItem("Process", "Import Samples"), 0)
        #menubar.Enable(menubar.FindMenuItem("Tools", "Convert to XM"), 0)

        #icon = wx.Icon('magicfish2.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(app.icons.redfish)

        # handles creation of various dialogs and MDI Children
        self.windowHandler = WindowHandler(self)

        self.SetCursor(wx.STANDARD_CURSOR)

        dt = MyFileDropTarget(self)
        self.SetDropTarget(dt)

        # WDR: handler declarations for MainDialog

        EVT_POSTMOD_NEW_FILEBATCH(self, self.OnNewFileBatch)
        EVT_POSTMOD(self, self.OnPostmodEvent)

        wx.EVT_MENU(self, ID_MENU_PATSCREEN, self.OnPatternScreen)
        wx.EVT_MENU(self, ID_MENU_TRACKSCREEN, self.OnTrackScreen)
        wx.EVT_MENU(self, ID_MENU_SAMPSCREEN, self.OnSampleScreen)
        wx.EVT_MENU(self, ID_MENU_INSTSCREEN, self.OnInstrumentScreen)

        cw = self.GetClientWindow()
        wx.EVT_ERASE_BACKGROUND(cw, self.OnEraseBackground)
        wx.EVT_MENU(self, ID_BUTTON_PLAY_PATTERN, self.OnPlayPattern)
        wx.EVT_MENU(self, ID_BUTTON_PLAY, self.OnPlay)
        wx.EVT_MENU(self, ID_BUTTON_STOP, self.OnStop)
        #wx.EVT_MENU(self, ID_MENU_OPTIONS_INTERPOLATION, self.OnOptionsInterpolation)
        wx.EVT_MENU(self, ID_MENU_LOOP_SONGS, self.OnOptionsLoopSongs)
        wx.EVT_MENU(self, ID_MENU_LOOP_SAMPLES, self.OnOptionsLoopSamples)
        wx.EVT_MENU(self, ID_MENU_LOOP_PATTERNS, self.OnOptionsLoopPatterns)
        wx.EVT_MENU(self, ID_MENU_MIXER, self.OnViewMixer)
        #wx.EVT_MENU(self, ID_MENU_SEND_BASSWAV_LOG, self.OnSendBASSLog)
        wx.EVT_SET_FOCUS(self, self.OnSetFocus)
        #wx.EVT_MENU(self, ID_MENU_DEV_RELOAD, self.OnReloadModules)
        wx.EVT_MENU(self, ID_MENU_REMOVE_UNUSED_SAMPLES, self.OnRemoveUnusedSamples)
        wx.EVT_MENU(self, ID_MENU_BATCH_APPENDFILE, self.OnAppendBatchFile)
        wx.EVT_MENU(self, ID_MENU_BATCH_OPENFILE, self.OnOpenBatchFile)
        #wx.EVT_MENU(self, ID_MENU_WAVBATCH_DIRTREE, self.WAVBatchFromDirTree)
        #wx.EVT_MENU(self, ID_MENU_WAVBATCH_FROMDIR, self.WAVBatchFromDir)
        #wx.EVT_MENU(self, ID_MENU_PROCESS_IMPORT_SAMPLES, self.OnImportSamples)
        wx.EVT_MENU(self, ID_MENU_NEWBATCH, self.OnNewBatch)
        wx.EVT_MENU(self, ID_MENU_HELP_MAGICFISH, self.OnHelpMagicfishSoftware)
        wx.EVT_MENU(self, ID_MENU_HELP_SUPPORTFORUM, self.OnHelpSupportForum)
        wx.EVT_MENU(self, ID_MENU_BUYNOW, self.OnRegisterNow)
        wx.EVT_MENU(self, ID_MENU_SLICEWAVTOIT, self.OnSliceWAVIntoIT)
        wx.EVT_MENU(self, ID_MENU_HELP_CONTENTS, self.OnHelpContents)
        wx.EVT_MENU(self, ID_MENU_BATCH_ADD_DIR_TREE, self.OnBatchAddDirTree)
        wx.EVT_MENU(self, ID_MENU_BATCH_ADD_DIR, self.OnBatchAddDir)
        wx.EVT_MENU(self, ID_MENU_BATCH_ADD, self.OnBatchAddFiles)
        wx.EVT_MENU(self, ID_MENU_HELP_ABOUT, self.OnAbout)
        #wx.EVT_MENU(self, ID_MENU_HELP_ABOUT, self.OnScreenshot)
        wx.EVT_MENU(self, ID_MENU_BATCH_OPENDIR, self.OnOpenDir)
        wx.EVT_MENU(self, ID_MENU_BATCH_OPENDIR_TREE, self.OnOpenDirTree)
        wx.EVT_MENU(self, ID_MENU_OPTIONS_PREFERENCES, self.OnPreferences)
        #wx.EVT_MENU(self, ID_MENU_RESET_LOG, self.OnResetLog)
        #wx.EVT_MENU(self, ID_MENU_SEND_ERRORLOG, self.OnSendErrorLog)
        wx.EVT_MENU(self, ID_MENU_PROCESS_SPLIT_SEQ, self.OnSplitSequences)
        wx.EVT_MENU(self, ID_MENU_PROCESS_UNFOLD, self.OnUnfoldSequences)
        wx.EVT_MENU(self, ID_MENU_PROCESS_RENDER_WAV, self.OnRenderWAV)
        #wx.EVT_MENU(self, ID_MENU_PROCESS_EXPORT_MIDI, self.OnExportMidi)
        wx.EVT_MENU(self, ID_MENU_PROCESS_EXPORT_SAMPLES, self.OnExportSamples)
        #wx.EVT_LISTBOX(self, ID_LISTBOX_SOURCEFILES, self.SourceFileDblClick)
        #wx.EVT_LISTBOX(self, ID_LISTBOX_SOURCEFILES, self.SourceFileSelected)
        wx.EVT_MENU(self, ID_MENU_EXIT, self.Exit)
        #wx.EVT_MENU(self, ID_MENU_FILE_SAVE_ALL, self.SaveAll)
        wx.EVT_MENU(self, ID_MENU_FILE_SAVE_AS, self.SaveAs)
        wx.EVT_MENU(self, ID_MENU_FILE_SAVE, self.Save)
        wx.EVT_MENU(self, ID_MENU_FILE_Close, self.FileClose)
        wx.EVT_MENU(self, ID_MENU_FILE_OPEN, self.FileOpen)
        wx.EVT_MENU(self, ID_MENU_FILE_NEW, self.FileNew)
        wx.EVT_CHAR(self, self.OnChar)
        #wx.EVT_KILL_FOCUS(self, self.OnKillFocus)
        wx.EVT_ACTIVATE(self, self.OnActivate)

        wx.EVT_CLOSE(self, self.OnClose)


        for i in range(options.MaxRecentFiles):
            wx.EVT_MENU(self, app.menus.ID_RECENT + i, self.OnRecentFile)
        
        self.CreateStatusBar()
        self.SetStatusText(APPNAME + " " + APPVERSION)

        self.RMENU = 0  # flag for adding register now under file menu

        self.childMap = {}  # a dictionary to hold pointers to created child windows

        #TODO: TESTING
        if LOCALTEST:
            self.BatchOpenDir(path="c:\\it")

        self.UpdateOptionMenu()
        self.UpdateRecentFiles()
        self.UpdateRecentFiles()

        if os.path.exists("background.jpg"):
            self.bkg = wx.Bitmap("background.jpg")
        else:
            self.bkg = None

        if os.path.exists("catinfo.dat"):
            self.bg_bmp = wx.Bitmap("catinfo.dat")
        else:
            self.bg_bmp = None

        pluginhandler.loadPlugins(options.PluginPath)

        postmod_menus.init()
        
        self.ModifyMenus()

        modplayer.setSwitchCallback(self.OnPlayerChanged)



    def ReloadMusicHandles(self):
        for child in self.childMap.values():
            if hasattr(child, "GetITDialog"):
                itd = child.GetITDialog()
                if itd and itd.mod:
                    itd.mod.reloadHandles()


    # switch callback for modplayer module
    def OnPlayerChanged(self, playernum):
        self.SetStatusText("Initializing new player...")
        self.ReloadMusicHandles()
        self.SetStatusText("")
                

    def OnClose(self, event):
        for child in self.childMap.values():
            try:
                child.OnClose(event)
            except:
                # might already be dead
                pass

        pmanager = libmp.getPluginManager()
        if pmanager:
            pmanager.close()

        self.SaveWindowPosition()
            
        event.Skip()

    def SaveWindowPosition(self):
        size, pos, maxed = self.GetSize(), self.GetPosition(), self.IsMaximized()
        if not maxed:
            options.LastSize = size.x, size.y
            options.LastPosition = pos.x, pos.y
        options.LastMaximized = maxed
        options.save()
        

    def ChildCall(self, funcname, *args, **kwargs):
        child = self.ActiveChild()
        if hasattr(child, funcname):
            getattr(child, funcname)(*args, **kwargs)

    def OnPatternScreen(self, event):
        self.ChildCall("OnPatternScreen", event)

    def OnTrackScreen(self, event):
        self.ChildCall("OnTrackScreen", event)

    def OnInstrumentScreen(self, event):
        self.ChildCall("OnInstrumentScreen", event)

    def OnSampleScreen(self, event):
        self.ChildCall("OnSampleScreen", event)


    def OnScreenshot( self, event ): 
        context = wx.WindowDC( self ) 
        memory = wx.MemoryDC( ) 
        x,y = self.GetClientSizeTuple() 
        bitmap = wx.EmptyBitmap( x,y, -1 ) 
        memory.SelectObject( bitmap ) 
        memory.Blit( 0,0,x,y, context, 0,0) 
        memory.SelectObject( wx.NullBitmap) 
        bitmap.SaveFile( "postmod.bmp", wx.BITMAP_TYPE_BMP ) 


    def OnEraseBackground(self, evt):
        if not self.bkg:
            evt.Skip()
            return
        
        dc = None
        if evt:
            dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRegion(rect.x, rect.y, rect.width, rect.height)
        self.TileBackground(dc)

    def TileBackground(self, dc):
        # tile the background bitmap
        sz = self.GetClientSize()
        w = self.bkg.GetWidth()
        h = self.bkg.GetHeight()

        x = 0
        while x < sz.width:
            y = 0
            while y < sz.height:
                #print "Drawing"
                dc.DrawBitmap(self.bkg, x, y)
                y = y + h
            x = x + w

    def OnPostmodEvent(self, event):
        if event.func:
            event.func(*event.args, **event.kwargs)
        
    def OnRecentFile(self, event):
        id = event.GetId() - app.menus.ID_RECENT
        fname = options.RecentFiles[id]
        if os.path.exists(fname):
            self.FileOpen(path=fname)
        else:
            wx.MessageBox(fname + " does not exist.", "File Not Found", parent=self)

    def OnPlugin(self, event):
        id = event.GetId() - app.menus.ID_PLUGINS
        print "plugin", id
        dlg = PluginDialog(self, -1, "Plugin")
        dlg.ShowModal()
        dlg.Destroy()
        
    def Updatey(self, event):
        #print "updatey", random.randrange(0,1000)
        event.Skip()

    def OnActivate(self, event):
        pass
        #if not event.GetActive():
        #    if BASS:
        #        pass
        #        #BASS.closeIfNotPlaying()

    def OnKittens(self):
        self.kittens = 1
        self.bkg = self.bg_bmp
        dc = wx.ClientDC(self.GetClientWindow())
        self.TileBackground(dc)
            
    def OnChar(self, event):
        event.Skip()
        try:
            if event.GetKeyCode() < 255:
                self.egg += chr(event.GetKeyCode())
                if self.egg.lower().find("kittens") > -1:
                    self.OnKittens()
                    self.egg = ""
                if len(self.egg) > 100:
                    self.egg = ""
        except:
            traceback.print_exc()
            pass

    def AddChild(self, dialog):
        self.childMap[dialog.GetId()] = dialog

                                           
    # WDR: methods for MainDialog

    def GetSplitter(self):
        return self.FindWindowById(ID_SPLITTER)

    # WDR: handler implementations for MainDialog

    def ModifyMenus(self):
        # hack - remove menu items, they're only there for their keyboard accelerators.
        menu = self.menubar.FindMenu("Tools")
        menu = self.menubar.GetMenu(menu)
        menu.Remove(ID_MENU_PATSCREEN)        
        menu.Remove(ID_MENU_TRACKSCREEN)        
        menu.Remove(ID_MENU_SAMPSCREEN)        
        menu.Remove(ID_MENU_INSTSCREEN)

        self.UpdatePluginMenu()        


    def UpdatePluginMenu(self):
        return 0
        
        menu = self.menubar.FindMenu("Plugins")
        menu = self.menubar.GetMenu(menu)

        idx = 0
        shortcuts = {}
        for plugin in pluginhandler.PLUGINLIST:
            idx += 1
            #(id, name, author, version, plugin)
            name = plugin[1]
            i = 0
            while i < len(name):
                ch = name[i].upper()
                if ch not in shortcuts:
                    shortcuts[ch] = 1
                    name = name[:i] + "&" + name[i:]
                    print name, i
                    break
                i += 1
            item = wx.MenuItem(menu, app.menus.ID_PLUGINS + idx, name)
            menu.InsertItem(menu.GetMenuItemCount(), item)

            wx.EVT_MENU(self, app.menus.ID_PLUGINS + idx, self.OnPlugin)            
        
        

    def UpdateRecentFiles(self):
        menu = self.menubar.FindMenu("File")
        menu = self.menubar.GetMenu(menu)

        for i in range(options.MaxRecentFiles):
            found = menu.FindItemById(app.menus.ID_RECENT + i)
            if found:
                menu.Remove(app.menus.ID_RECENT + i)

        pass
                                
        for i in range(len(options.RecentFiles)):
            numst = str(i+1)
            if (i+1) > 9:
                numst = numst[1]
            item = wx.MenuItem(menu, app.menus.ID_RECENT + i, "&" + numst + " " + options.RecentFiles[i])
            menu.InsertItem(menu.GetMenuItemCount()-2, item)

        options.save()


    def UpdateOptionMenu(self):
        item = self.menubar.FindMenuItem("Options", "Loop Songs")
        self.menubar.Check(item, bool(options.LoopSongs))
        item = self.menubar.FindMenuItem("Options", "Loop Patterns")
        self.menubar.Check(item, bool(options.LoopPatterns))
        item = self.menubar.FindMenuItem("Options", "Loop Samples")
        self.menubar.Check(item, bool(options.LoopSamples))
        #item = self.menubar.FindMenuItem("Options", "Use Interpolation")
        #self.menubar.Check(item, bool(options.PlaybackInterpolation))

    def OnOptionsInterpolation(self, event):
        options.PlaybackInterpolation = event.IsChecked()
        options.save()
            
    def OnOptionsLoopSongs(self, event):
        options.LoopSongs = event.IsChecked()
        options.save()

    def OnOptionsLoopSamples(self, event):
        options.LoopSamples = event.IsChecked()
        options.save()

    def OnOptionsLoopPatterns(self, event):
        options.LoopPatterns = event.IsChecked()
        options.save()


    def OnViewMixer(self, event):
        global MIXERDLG
        if MIXERDLG:
            MIXERDLG.updatePlayerControls()
            MIXERDLG.Show(1)
            MIXERDLG.SetFocus()
        else:
            MIXERDLG = MixerDialog(self, -1)
            MIXERDLG.Show(1)
            wxx.Yield()
            if not modplayer.getPlayer().initialized:
                MIXERDLG.SetTitle("Initializing BASS Sound System...")
                modplayer.getPlayer().init()
                modplayer.getPlayer().start()
                MIXERDLG.SetTitle("Playback Mixer")
                MIXERDLG.setVolumes()

    def OnSendBASSLog(self, event):
        self.OnSendErrorLog(logfile="tools\basswav.log")
        


    def OnSetFocus(self, event):
        # call active child's onsetfocus, if any - so that they can be aware of application switches.
        child = self.ActiveChild()
        if hasattr(child, "OnSetFocus"):
            child.OnSetFocus(event)            

    def OnReloadModules(self, event):
        #exec (GLOBAL_RELOADER (globals ()))
        pass

    def OnPlayPattern(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnPlayPattern"):
            child.OnPlayPattern(event)

    def OnPlay(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnPlay"):
            child.OnPlay(event)

    def OnStop(self, event):
        #child = self.ActiveChild()
        for child in self.childMap.values():
            if hasattr(child, "OnStop"):
                child.OnStop(event)

    def OnRemoveUnusedSamples(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnRemoveUnusedSamples"):
            child.OnRemoveUnusedSamples()

    def OnAppendBatchFile(self, event):
        path = wxx.SelectFile(self, ext="*.bch", saving=0, pathtype="batch")
        if path:
            child = self.ActiveChild()
            if hasattr(child, "AppendBatchFile"):
                child.AppendBatchFile(path)

    def OnOpenBatchFile(self, event):
        #TODO: default batch path. maybe system for keeping track of current directories of different types.
        path = wxx.SelectFile(self, ext="*.bch", saving=0, pathtype="batch")
        if path:
            self.NewFileBatch(fname=path)
            

    def WAVBatchFromDirTree(self, event):
        self.BatchOpenDir(recurse=1, ext="*.wav", name="WAV Batch")
        
    def WAVBatchFromDir(self, event):
        self.BatchOpenDir(recurse=0, ext="*.wav", name="WAV Batch")

    def OnImportSamples(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnImportSamples"):
            child.OnImportSamples()
        else:
            wx.MessageBox("To import samples into an IT file, first create a new batch of WAV files.", "Import Samples", style = wx.OK |wx.ICON_INFORMATION, parent=self)


    def OnNewBatch(self, event):
        self.NewFileBatch()

    def OnHelpMagicfishSoftware(self, event):
        webbrowser.open(URL_MAGICFISH)

    def OnHelpSupportForum(self, event):
        webbrowser.open(URL_SUPPORTFORUM)

    def OnRegisterNow(self, event):
        webbrowser.open(URL_REGISTER)

    def OnSliceWAVIntoIT(self, event):
        child = self.ActiveChild()
        fname = None
        realfile = None
        mod = None
        callback = None
        if hasattr(child, "mod"):
            #fname = "[" + os.path.basename(child.mod.getRealFile()) + "]"
            #realfile = child.mod.getEditFile()
            #child.mod.saveWork()
            mod = child.mod
            callback = child.GetITDialog().Update
        
        diag = SliceWAVDialog(self, -1, "Slice WAV", fname=fname, realfile=realfile, mod=mod, callback=callback)
        diag.CentreOnParent()
        diag.Show(True)
        self.childMap[diag.GetId()] = diag
        return diag

    def OnHelpContents(self, event):
        win32api.ShellExecute(0, "open", "help\postmod.chm", None, None, 1)
        

    def OnBatchAddDirTree(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnAddDirTree"):
            child.OnAddDirTree(event)
        else:
            self.OnOpenDirTree(event)

    def OnBatchAddDir(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnAddDir"):
            child.OnAddDir(event)
        else:
            self.OnOpenDir(event)
        

    def OnBatchAddFiles(self, event):
        child = self.ActiveChild()
        if hasattr(child, "OnAddFiles"):
            child.OnAddFiles(event)
        

    def OnAbout(self, event):
        diag = AboutDialog(self, -1, "About POSTMOD")
        diag.CentreOnParent()
        diag.ShowModal()
        diag.Destroy()


    def OnTest(self, event):
        #diag = TestDialog(self, -1, "Test")
        #diag.ShowModal()
        #diag.Destroy()
        print self.GetChildren()
        print str(self.childMap)
        self.__del__()
        print str(self.childMap)


    def OnPreferences(self, event, title="Preferences"):
        diag = PreferencesDialog(self, -1, title)
        diag.CentreOnParent()
        diag.ShowModal()
        diag.Destroy()
        

    def OnResetLog(self, event):
        print "-- Resetting postmod.log..."
        try:
            fp = open("postmod.log", "w")
            fp.write("")
            fp.close()
        except:
            pass
        

    def OnSendErrorLog(self, event=None, logfile="postmod.log"):
        print "Sending Error Log to magicfish software..."
        """print "zipping log..."
        from zipfile import *
        zf = ZipFile("postmodlog.zip", "w", ZIP_DEFLATED)
        zf.write(logfile)
        zf.close()
        print "mailing postmodlog.zip..."""
        print "building message..."
        fp = open(logfile, "r")
        plog = fp.read()
        fp.close()
        #import smtplib
        fromaddr = "betatest@68k.org"
        toaddrs  = ["magicfish@magicfish.net"]
        msg = ("From: %s\r\nTo: %s\r\n\r\n"
               % (fromaddr, string.join(toaddrs, ", ")))
        msg = msg + plog
        print "mailing log..."
        try:
            server = smtplib.SMTP('mail.magicfish.net')
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
        except:
            print "Error sending mail."
        print "Done."

    def UpdateActiveChild(self):
        child = self.ActiveChild()
        if hasattr(child, "ChangeNotify"):
            child.ChangeNotify(1)
        if hasattr(child, "GetITDialog"):
            #print "calling update for", child
            child.GetITDialog().Update(0)

    def ReloadActiveChild(self):
        child = self.ActiveChild()
        if hasattr(child, "Reload"):
            #print "reloading..."
            child.Reload()


    def OnSplitSequences(self, event):
            
        child = self.ActiveChild()
        if not child:
            self.FileOpen(None)
            child = self.ActiveChild()

        if child and hasattr(child, "OnBatchSplit"):
            #print "title", child.GetTitle()
            child.OnBatchSplit(event)
        else:
            pass
            #print "child has no method OnBatchSplit()"

    def OnUnfoldSequences(self, event):

        child = self.ActiveChild()
        if not child:
            self.FileOpen(None)
            child = self.ActiveChild()
            
        if child and hasattr(child, "OnUnfold"):
            child.OnUnfold(event)
            #self.UpdatePatternNames()
        else:
            pass
            #print "child has no method OnUnfold()"

    def OnRenderWAV(self, event):

        child = self.ActiveChild()
        if not child:
            self.FileOpen(None)
            child = self.ActiveChild()

        if child and hasattr(child, "OnRender"):
            child.OnRender(event)
        else:
            pass
            #print "child has no method OnRender()"

    def OnExportMidi(self, event):
        pass

    def OnExportSamples(self, event):

        child = self.ActiveChild()
        if not child:
            self.FileOpen(None)
            child = self.ActiveChild()

        if child and hasattr(child, "OnExportSamples"):
            #print "OnExportSamples()"
            child.OnExportSamples(event)
        else:
            pass
            #print "child has no method OnExportSamples()"

    def ActiveChild(self):
        try:
            child = self.childMap[self.GetActiveChild().GetId()]
        except:
            child = None
        return child


    def OnOpenDirTree(self, event):
        self.BatchOpenDir(recurse=1)
        
    def OnOpenDir(self, event):
        self.BatchOpenDir(recurse=0)        

    def NewFileBatch(self, title="File Batch", show=1, fname=None, focus=1, files=[]):
        dialog = self.windowHandler.NewFileBatch(title=title, show=show, fname=fname, focus=focus, files=files)
        return dialog

    def OnNewFileBatch(self, event):
        batch = self.NewFileBatch(title=event.title, files=event.files)
        batch.Raise()
        batch.SetFocus()
        #for child in self.childMap.values():
        #    if child != batch:
        #        child.Lower()

    def BatchOpenDir(self, recurse=0, path=None, ext="*.it", name="IT Batch"):
        if not path:
            path = wxx.SelectPath(self, pathtype="it")
            if not path:
                return 0

        flist = dirwalk.Walk(root=path, recurse=recurse, pattern=ext)
        flist.sort()
        #fb = FileBatch(dir=path, mask="*.it")
        name = name + " - " + path
        dlg = FileBatchMultiDialog(self, -1, name)
        #diag = dlg.GetCurrentBatch()
        dlg.SetName(name)
        
        dlg.Show(True)
        self.childMap[dlg.GetId()] = dlg
        list = dlg.GetListControl()
        #list.InsertColumn(0, "Path")
        #list.InsertColumn(1, "File")
        i = 0
        #for x in fb.data:
        #diag.data = flist
        for x in flist:
            #print x
            fname = os.path.basename(x)
            pathname = os.path.dirname(x)
            list.InsertStringItem(i, pathname)
            list.SetStringItem(i, 1, fname)
            #self.list.SetStringItem(i, 2, data[2])
            i = i + 1
        #diag.Autosize()
        dlg.Autosize()

            
    
    def SourceFileDblClick(self, event):
        pass

    def SourceFileSelected(self, event):
        pass

    def Exit(self, event):
        #x = raw_input("press a key")
        self.Close()

    def Properties(self, event):
        for key in self.childMap.keys():
            child = self.childMap[key]
            print "name", child.GetName()
            print "title", child.GetTitle()
            print "id", child.GetId()
            print "data", child.data
        print gc.garbage
        print gc.collect()
        pass

    def SaveAll(self, event):
        pass

    def SaveAs(self, event):
        child = self.ActiveChild()
        if child and hasattr(child, "OnSaveAs"):
            child.OnSaveAs(event)
        

    def Save(self, event):
        child = self.ActiveChild()
        if child and hasattr(child, "OnSave"):
            child.OnSave()
        
    def SaveWorkspace(self, event):
        fpath = "workspace.pmd"
        f = open(fpath, "w")
        pickle.dump(self.__dict__, f)
        f.close()
        

    def OpenWorkspace(self, event):
        fpath = "workspace.pmd"
        f = open(fpath, "r")
        self.__dict__ = pickle.load(f)
        f.close()
        

    def FileClose(self, event):
        child = self.ActiveChild()
        if child:
            if hasattr(child, "Close"):
                child.Close()

    def OpenITFile(self, path, makenew=0):
        mp = modplayer.getPlayer()
        mp.init(samplerate=0)
        mp.start()
        
        diag = ITDocDialogMulti(self, -1, "New IT", path=path, makenew=makenew)
        #diag.Load(path)
        diag.Show(True)
        self.childMap[diag.GetId()] = diag
        return diag
        
    def FileOpen(self, event=None, path=None, paths=None, makenew=0):
        if path:
            paths=[path]
        if not paths:
            paths = wxx.SelectFile(self, ext="*.it", saving=0, multi=1, pathtype="it")
            #paths = wxx.SelectFile(self, ext="*.*", saving=0, multi=1, pathtype="it")
        if not paths:
            return 0
        
        # if only one file selected, we'll open the actual IT document, otherwise we'll just add the files to the current batch.
        if len(paths) == 1:
            dlg = self.OpenITFile(paths[0], makenew=makenew)
            if paths[0].find(options.TempPath) == -1:
                options.addRecentFile(paths[0])
                self.UpdateRecentFiles()
        else:
            child = self.NewFileBatch(files=paths)
            #child.OnAddFiles(None, filelist=paths)
            #child.Autosize()
            dlg = child
        return dlg
            
        

    def FileNew(self, event):
        diag = ITDocDialogMulti(self, -1, "New IT")
        diag.Show(True)
        self.childMap[diag.GetId()] = diag
        return True



class MyApp(wx.App):
    
    def OnInit(self):

        postmod_icons.initIcons()
        
        global MAINFRAME
                
        if options.LastPosition:
            pos = wx.Point(*options.LastPosition)
        else:
            pos = wx.DefaultPosition

        if options.LastSize:
            size = wx.Size(*options.LastSize)
        else:
            size = wx.Size(800, 600)

        maxed = options.LastMaximized
        frame = MainDialog(None, -1, app.TITLE, pos=pos, size=size, maximize=maxed)
        frame.Show(True)
        self.SetTopWindow(frame)


        # load bas
        frame.SetStatusText("Initializing BASS Sound System...")
        #loadBASS()
        modplayer.loadPlayerModules()
        frame.SetStatusText("")
        #lbt = threadx.GenericThread(loadBASS)
        #lbt.start()

        if options.FirstRun:
            frame.OnPreferences(None, "Welcome to Magicfish Postmod")
            options.FirstRun = 0
            options.save()

        try:
            if len(sys.argv) > 1:
                # first check for dirs
                paths = sys.argv[1:]
                for path in sys.argv[1:]:
                    if os.path.isdir(path):
                        files = filex.dirtree(path, "*.it")
                        sys.argv.remove(path)
                        sys.argv += files
                    
                # load files
                if len(sys.argv) == 2:
                    frame.FileOpen(path=sys.argv[1])
                else:
                    frame.FileOpen(paths=sys.argv[1:])
        except:
            # we never want to fail here.
            pass
                                                
        #console = ConsoleDialog(frame, -1, "Console")
        #console.Show(True)
        #sys.stdout = console
        MAINFRAME = frame
        return True

    def OnAssert(self, file, line, condition, message):
        print "--- Assert Failure:", file, line, condition, message, "---"

def OnAssert(file, line, condition, message="No Message"):
        print "--- Assert Failure:", file, line, condition, message, "---"

wx.OnAssert = OnAssert    



def app_main():
    global APP
    theapp = MyApp(DEFAULTCONSOLEIO)
    APP = theapp
    theapp.MainLoop()
    # clean temp directory
    app.Cleanup()


def main():
    
    app_main()

    modplayer.getPlayer().stop()
    modplayer.getPlayer().close()
    # TODO: both players?


if __name__ == "__main__":
    main()

