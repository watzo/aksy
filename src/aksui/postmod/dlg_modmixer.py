#!/bin/env python
#----------------------------------------------------------------------------
# Name:         dlg_modmixer.py
# Author:       XXXX
# Created:      XX/XX/XX
# Copyright:    
#----------------------------------------------------------------------------

import wx, wxx
from postmod_wdr import *
from wxPython.lib.scrolledpanel import wxScrolledPanel
from aslider import *

VOLUME_SLIDER_IDX = 1000
VOLUME_EDIT_IDX = 3000
TRACK_MUTE_IDX = 5000
TRACK_SOLO_IDX = 7000
TRACK_NAME_IDX = 9000
PAN_SLIDER_IDX = 30000
PAN_EDIT_IDX = 31000



# WDR: classes

class ModMixerDialog(wxScrolledPanel, wxx.DialogX):
    def __init__(self, parent, id,
        #pos = wxPyDefaultPosition, size = wxPyDefaultSize,
        pos = wx.DefaultPosition, size = (100,100),
        style = wx.TAB_TRAVERSAL,
        mod = None):
        wxScrolledPanel.__init__(self, parent, id, pos, size, style)
        
        mixer = ModMixerFunc( self, False, False )

        self.volumeSliders = []
        self.panSliders = []
        
        # WDR: handler declarations for ModMixerDialog
        wx.EVT_SIZE(self, self.OnSize)

        parent = self
        parent.SetAutoLayout( True )
        parent.SetSizer( mixer )
        mixer.Fit( parent )
        mixer.SetVirtualSizeHints( parent )

        self.SetupScrolling(scroll_y=False)

        self.SetMod(mod)


    def SetMod(self, mod):
        self.mod = mod
        if mod:
            for i in range(mod.numTracks()):
                self.AddTrack(i)

            self.SetupScrolling(scroll_y=False)
            #self.UpdateSizer()
        

    def AddTrack(self, index):
        wx.FIXED_MINSIZE = 0
        parent = self
        item3 = wx.StaticBox( parent, -1, "" )
        item2 = wx.StaticBoxSizer( item3, wx.VERTICAL )
        
        item4 = wx.SpinCtrl( parent, PAN_EDIT_IDX+index, "0", wx.DefaultPosition, wx.Size(50,-1), 32, 0, 64, 0 )
        wx.EVT_SPINCTRL(self, PAN_EDIT_IDX+index, self.OnTrackPanEdit)
        item4.SetToolTip( wx.ToolTip("Pan") )
        item2.Add( item4, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        item5 = wx.Slider( parent, PAN_SLIDER_IDX+index, 32, 0, 64, wx.DefaultPosition, wx.Size(50,-1), wx.SL_HORIZONTAL )
        item5.SetToolTip( wx.ToolTip("Pan") )
        self.panSliders.append(item5)
        wx.EVT_SLIDER(self, PAN_SLIDER_IDX+index, self.OnTrackPan)
        item2.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.FIXED_MINSIZE, 0 )

        #item6 = wxSlider( parent, ID_SLIDER_TRACK, 0, 0, 100, wxDefaultPosition, wxDefaultSize, wxSL_VERTICAL )
        #item6 = wxSlider( parent, VOLUME_SLIDER_IDX+index, 0, 0, 64, wxDefaultPosition, wxDefaultSize, wxSL_VERTICAL )
        item6 = wxAudioSlider( parent, VOLUME_SLIDER_IDX+index, wx.DefaultPosition, (23,100), min=0, max=64 )
        self.volumeSliders.append(item6)
        wx.EVT_SLIDER(self, VOLUME_SLIDER_IDX+index, self.OnTrackVolume)

        item6.SetName( "TrackVolume" + str(index) )
        item2.Add( item6, 0, wx.ALIGN_CENTRE|wx.ALL|wx.FIXED_MINSIZE, 5 )

        item7 = wx.SpinCtrl( parent, VOLUME_EDIT_IDX+index, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 64, 0 )
        wx.EVT_SPINCTRL(self, VOLUME_EDIT_IDX+index, self.OnTrackVolumeEdit)
        item7.SetToolTip( wx.ToolTip("Volume") )
        item7.SetName( "TrackVolumeEdit" + str(index) )
        item2.Add( item7, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        item8 = wx.BoxSizer( wx.HORIZONTAL )
        
        item9 = wx.ToggleButton( parent, TRACK_MUTE_IDX+index, "M", wx.DefaultPosition, wx.Size(20,-1), 0 )
        wx.EVT_TOGGLEBUTTON(self, TRACK_MUTE_IDX+index, self.OnMuteButton)
        item9.SetFont( wx.Font( 12, wx.SWISS, wx.NORMAL, wx.BOLD ) )
        item8.Add( item9, 0, wx.ALIGN_CENTRE|wx.ALL|wx.FIXED_MINSIZE, 0 )

        item10 = wx.ToggleButton( parent, TRACK_SOLO_IDX+index, "S", wx.DefaultPosition, wx.Size(20,-1), 0 )
        wx.EVT_TOGGLEBUTTON(self, TRACK_SOLO_IDX+index, self.OnSoloButton)
        item10.SetFont( wx.Font( 12, wx.SWISS, wx.NORMAL, wx.BOLD ) )
        item8.Add( item10, 0, wx.ALIGN_CENTRE|wx.ALL|wx.FIXED_MINSIZE, 0 )

        item2.Add( item8, 0, wx.ALIGN_CENTRE|wx.ALL|wx.FIXED_MINSIZE, 5 )

        if self.mod:
            trackname = self.mod.getTrackName(index, number=0, colors=0)
        else:
            trackname = "Track " + str(index)            
        item11 = wx.StaticText( parent, TRACK_NAME_IDX+index, trackname, wx.DefaultPosition, wx.DefaultSize, 0 )
        item11.SetName( "TrackName" + str(index) )
        item2.Add( item11, 0, wx.ALIGN_CENTRE|wx.ALL|wx.FIXED_MINSIZE, 5 )

        self.MixerSizer.Add( item2, 0, wx.ALL|wx.FIXED_MINSIZE, 0 )


    def UpdateSizer(self, call_fit = True):
        parent = self
        parent.SetAutoLayout( True )
        parent.SetSizer( self.MixerSizer )
        if call_fit == True:
            self.MixerSizer.Fit( parent )
            self.MixerSizer.SetSizeHints( parent )
        
        



    # WDR: methods for ModMixerDialog

    def GetVolumeEdit(self, id):
        return self.FindWindowById(id)

    def GetVolumeSlider(self, index):
        #return wxPyTypeCast( self.FindWindowById(id), "wxSlider" )
        return self.volumeSliders[index]

    def GetPanEdit(self, id):
        return self.FindWindowById(id)

    def GetPanSlider(self, index):
        #return wxPyTypeCast( self.FindWindowById(id), "wxSlider" )
        return self.panSliders[index]

    def GetMuteButton(self, id):
        return self.FindWindowById(id)

    def GetSoloButton(self, id):
        return self.FindWindowById(id)


    # WDR: handler implementations for ModMixerDialog        

    def OnSize(self, event):
        #self.SetSize((100, 100))
        #event.Skip(1)
        return 1

    def OnTrackPan(self, event):
        id = event.GetId()
        val = event.GetInt()
        self.GetPanEdit(id + 1000).SetValue(val)
        if self.mod:
            self.mod.setDefaultTrackPan(id - PAN_SLIDER_IDX, val)

    def OnTrackPanEdit(self, event):
        id = event.GetId()
        val = event.GetInt()
        self.GetPanSlider(id - PAN_EDIT_IDX).SetValue(val)
        if self.mod:
            self.mod.setDefaultTrackPan(id - PAN_EDIT_IDX, val)
        

    def OnTrackVolumeEdit(self, event):
        #print event.GetId()
        id = event.GetId()
        val = abs(event.GetInt() - 64)
        self.volumeSliders[id - 3000].SetValue(val)
        if self.mod:
            self.mod.setDefaultTrackVolume(id - VOLUME_EDIT_IDX, val)

    def OnTrackVolume(self, event):        
        id = event.GetId()
        val = abs(event.GetInt() - 64)
        self.GetVolumeEdit(id + 2000).SetValue(val)
        if self.mod:
            self.mod.setDefaultTrackVolume(id - VOLUME_SLIDER_IDX, val)

    def OnMuteButton(self, event):
        if event.GetEventObject().GetValue():
            self.mod.muteTrack(event.GetId() - TRACK_MUTE_IDX)
        else:
            self.mod.unmuteTrack(event.GetId() - TRACK_MUTE_IDX)
        
    def OnSoloButton(self, event):
        if event.GetEventObject().GetValue():
            self.mod.soloTrack(event.GetId() - TRACK_SOLO_IDX, 1, 0)
        else:
            self.mod.unSoloTrack(event.GetId() - TRACK_SOLO_IDX)
            if not self.mod.soloed:
                # catch any mute changes made while soloed
                self.UpdateMixer()
                self.mod.setAllTrackVolumes()

    def SetTrackVolume(self, track, volume):
        a, b = self.volumeSliders[track], self.GetVolumeEdit(track + VOLUME_EDIT_IDX)
        a.SetValue(abs(volume - 64))
        b.SetValue(volume)

    def SetTrackPan(self, track, pan):
        a, b = self.panSliders[track], self.GetPanEdit(track + PAN_EDIT_IDX)
        a.SetValue(pan)
        b.SetValue(pan)

    def SetTrackMute(self, track, mute):
        self.GetMuteButton(track + TRACK_MUTE_IDX).SetValue(mute)

    def SetTrackSolo(self, track, solo):
        self.GetSoloButton(track + TRACK_SOLO_IDX).SetValue(solo)
        
    def UpdateMixer(self, tracks=None):
        # update all from mod
        #print "dlg_modmixer updating mixer from", self.mod
        if not tracks:
            tracks = range(self.mod.numTracks())
        if self.mod:
            for i in tracks:
                vol, pan, enabled, surround = self.mod.getTrackSettings(i)
                self.SetTrackVolume(i, vol)
                self.SetTrackPan(i, pan)
                self.SetTrackMute(i, not enabled)
                #self.SetTrackSolo(i, i in self.mod.soloed)
                self.SetTrackSolo(i, self.mod.isTrackSolo(i))

                