
import wx
from postmod_wdr import *

import app, basslib, wxx, modplayer, renderers
from options import *

#TODO: maybe move HasMixerSelection somewhere. gui_mixer.py?

class HasMixerSelection:

    def __init__(self):
        wx.EVT_CHOICE(self, ID_CHOICE_INTERPOLATION, self.OnSelectInterpolation)
        wx.EVT_CHOICE(self, ID_CHOICE_BITRATE, self.OnSelectSampleWidth)
        wx.EVT_CHOICE(self, ID_CHOICE_SAMPLERATE, self.OnSelectSampleRate)
        wx.EVT_CHOICE(self, ID_CHOICE_RENDERER, self.OnSelectRenderer)
        
    
    def updatePlayerControls(self):
        #r, s, b, i = self.GetControl("Renderer"), self.GetControl("SampleRate"), self.GetControl("BitRate"), self.GetControl("InterpolationMode")
        r, s, b, i = self.FindWindowById(ID_CHOICE_RENDERER), self.FindWindowById(ID_CHOICE_SAMPLERATE), self.FindWindowById(ID_CHOICE_BITRATE), self.FindWindowById(ID_CHOICE_INTERPOLATION)

        wxx.updateSelectBox(r, modplayer.getPlayerNames(), cache=1)
        renderer = modplayer.getPlayer().getRenderer()
        wxx.updateSelectBox(s, [x[0] for x in renderer.getSupportedSampleRates()], renderer.getDefaultSampleRate()[0], cache=1)
        wxx.updateSelectBox(b, [x[0] for x in renderer.getSupportedBitRates()], renderer.getDefaultBitRate()[0], cache=1)
        wxx.updateSelectBox(i, [x[0] for x in renderer.getInterpolationSettings()], renderer.getDefaultInterpolation()[0], cache=1)

        settings = modplayer.getPlayer().getSettings()
        sr = renderer.getSampleRateName(settings[0])
        br = renderer.getBitRateName(settings[1])

        r.SetStringSelection(modplayer.getPlayer().getName())
        s.SetStringSelection(sr)
        b.SetStringSelection(br)
        i.SetSelection(settings[2])

        try:
            sl = self.GetSongSlider()
            if renderer.getCode() == "MODPLUG":
                sl.Enable(0)
            else:
                sl.Enable(1)
        except:
            pass

    def setInterpolation(self, interpolation):
        player = modplayer.getPlayer()
        player.setInterpolation(interpolation)

    def setSampleWidth(self, samplewidth):
        player = modplayer.getPlayer()
        player.setSampleWidth(samplewidth)

    def setSampleRate(self, samplerate):        
        player = modplayer.getPlayer()
        player.setSampleRate(int(samplerate))
        
    def OnSelectInterpolation(self, event):
        self.setInterpolation(event.GetSelection())
        
    def OnSelectSampleWidth(self, event):
        self.setSampleWidth(event.GetSelection())
        
    def OnSelectSampleRate(self, event):
        self.setSampleRate(int(event.GetString()))
        
    def OnSelectRenderer(self, event):
        #print ". selected renderer", event.GetSelection()
        modplayer.switchPlayer(int(event.GetSelection()))
        player = modplayer.getPlayer()
        s = self.FindWindowById(ID_CHOICE_SAMPLERATE)
        player.setSampleRate(int(s.GetStringSelection()))

        #self.updatePlayerControls() - don't need because will be called back by subject on change (setSampleRate)
        



class MixerDialog(wxx.DialogX, HasMixerSelection):
    def __init__(self, parent, id, title="Playback Mixer",
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        #style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP):
        style = wx.DEFAULT_FRAME_STYLE):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        self.Show(0)

        self.SetIcon(app.icons.greenwav)        
        MixerFunc( self, True )
        self.setVolumes()

        #slider = self.GetHardwareSlider()
        #slider.SetThumbLength(500)
        
        # WDR: handler declarations for MixerDialog
        wx.EVT_CHOICE(self, ID_CHOICE_RENDERER, self.OnSelectRenderer)
        wx.EVT_CLOSE(self, self.OnClose)
        wx.EVT_SET_FOCUS(self, self.OnSetFocus)
        wx.EVT_SLIDER(self, ID_SLIDER_HARDWARE, self.OnHardwareSlider)
        wx.EVT_SLIDER(self, ID_SLIDER_SONGS, self.OnSongSlider)
        #wx.EVT_SLIDER(self, ID_SLIDER_AMP, self.OnAmpSlider)
        wx.EVT_SLIDER(self, ID_SLIDER_SAMPLES, self.OnSampleSlider)

        HasMixerSelection.__init__(self)

        self.updatePlayerControls()

        modplayer.addObserver(self)
        #players = modplayer.getPlayers()
        #for player in players:
        #    player.attach(self)

    # WDR: methods for MixerDialog

    def OnHardwareSlider(self, event):
        vol = event.GetInt()
        basslib.BASS.BASS_SetVolume(vol)

    def OnSongSlider(self, event):
        vol = event.GetInt()
        basslib.BASS.BASS_SetConfig(basslib.BASS_CONFIG_GVOL_MUSIC, vol)
        options.SongVolume = vol

    def OnAmpSlider(self, event):
        vol = event.GetInt()
        basslib.BASS.BASS_SetVolume(vol)
        options.SongAmp = vol

    def OnSampleSlider(self, event):
        vol = event.GetInt()
        basslib.BASS.BASS_SetConfig(basslib.BASS_CONFIG_GVOL_SAMPLE, vol)
        options.SampleVolume = vol

    def setVolumes(self):
        slider = self.GetHardwareSlider()
        if slider:
            vol = basslib.BASS.BASS_GetVolume()
            #print "volume is", vol
            slider.SetValue(vol)

        slider2 = self.GetSongSlider()
        if slider2:
            slider2.SetValue(options.SongVolume)
            basslib.BASS.BASS_SetConfig(basslib.BASS_CONFIG_GVOL_MUSIC, options.SongVolume)            
            #vol = basslib.BASS_GetGlobalVolumes()[0]
            #slider.SetValue(vol)

        #slider3 = self.GetAmpSlider()
        #if slider3:
        #    slider3.SetValue(options.SongAmp)
            #slider3.SetValue(50)

        slider4 = self.GetSampleSlider()
        if slider4:
            slider4.SetValue(options.SampleVolume)
            basslib.BASS.BASS_SetConfig(basslib.BASS_CONFIG_GVOL_SAMPLE, options.SampleVolume)
            #slider4.SetValue(50)


    def update(self, subject):
        # called by subject when settings change
        settings = subject.getSettings()
        #self.setSampleRate(settings[0])
        #self.setSampleWidth(settings[1])
        #self.setInterpolation(settings[2])
        self.updatePlayerControls()


    def GetSampleSlider(self):
        return self.FindWindowById(ID_SLIDER_SAMPLES)

    def GetAmpSlider(self):
        return self.FindWindowById(ID_SLIDER_AMP)

    def GetSongSlider(self):
        return self.FindWindowById(ID_SLIDER_SONGS)

    def GetHardwareSlider(self):
        return self.FindWindowById(ID_SLIDER_HARDWARE)

    # WDR: handler implementations for MixerDialog        

    def OnSetFocus(self, event):
        self.update()
        event.Skip(True)

    def OnClose(self, event):
        options.save()
        event.Skip(True)
