
import wx
import wxx

from postmod_wdr import *

import basslib
from options import *

import modplayer, renderers


AUDIODEVICES = []

class PreferencesDialog(wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        PreferencesDialogFunc( self, True )
        
        # WDR: handler declarations for PreferencesDialog
        #wx.EVT_BUTTON(self, ID_BUTTON_EXTERNALPLAYER, self.OnSelectExternalPlayer)
        wx.EVT_BUTTON(self, ID_BUTTON_BATCHFILE_PATH, self.OnBatchfilePath)
        wx.EVT_BUTTON(self, ID_BUTTON_WAV_PATH, self.OnWAVPath)
        wx.EVT_BUTTON(self, ID_BUTTON_RENDER_PATH, self.OnRenderPath)
        wx.EVT_BUTTON(self, ID_BUTTON_BACKUP_PATH, self.OnSelectBackupPath)
        wx.EVT_BUTTON(self, ID_BUTTON_TEMP_PATH, self.OnSelectTempPath)
        wx.EVT_BUTTON(self, ID_BUTTON_DEFAULT_EXPORT_PATH, self.OnSelectExportPath)
        wx.EVT_BUTTON(self, ID_BUTTON_DEFAULT_PATH, self.OnSelectDefaultPath)
        wx.EVT_BUTTON(self, ID_BUTTON_CANCEL, self.OnCancel)
        wx.EVT_BUTTON(self, ID_BUTTON_OK, self.OnOK)

        wx.EVT_CHOICE(self, ID_CHOICE_DEFAULTPLAYER, self.OnChooseDefaultPlayer)
        wx.EVT_CHOICE(self, ID_CHOICE_DEFAULTRENDERER, self.OnChooseDefaultRenderer)

        
        self.TransferDataToWindow()

        global AUDIODEVICES
        if not AUDIODEVICES:
            AUDIODEVICES = ["Default"] + basslib.Bass.getDevices()

        list = self.GetControl("AudioDeviceNum")
        list.Clear()
        for x in AUDIODEVICES:
            list.Append(str(x))
        list.SetSelection(options.AudioDeviceNum+1)

        list = self.GetControl("DefaultPlayer")
        wxx.updateSelectBox(list, modplayer.getPlayerNames())
        list.SetSelection(options.DefaultPlayer)

        list = self.GetControl("DefaultRenderer")
        wxx.updateSelectBox(list, renderers.getRendererNames())
        list.SetSelection(options.DefaultRenderer)

        



    # WDR: methods for PreferencesDialog

    def TransferDataToWindow(self):
        global options
        data = {}
        data["DefaultPath"] = options.DefaultPath
        data["ExportPath"] = options.ExportPath
        data["TempPath"] = options.TempPath
        data["BackupPath"] = options.BackupPath

        data["RenderPath"] = options.RenderPath
        data["WAVPath"] = options.WAVPath
        data["BatchfilePath"] = options.BatchfilePath
        data["CheckUpdates"] = options.CheckUpdates
        data["UnfoldEmptyOrderLists"] = options.UnfoldEmptyOrderLists

        data["ExternalPlayer"] = options.ExternalPlayer
        data["UseExternalPlayer"] = options.UseExternalPlayer

        data["AudioDevice"] = options.AudioDevice
        data["AudioDeviceNum"] = options.AudioDeviceNum
        data["DefaultPlayer"] = options.DefaultPlayer
        data["DefaultRenderer"] = options.DefaultRenderer

        self.SetControlData(data)

    def TransferDataFromWindow(self):
        global options
        data = self.GetControlData()
        options.DefaultPath = data["DefaultPath"]
        options.ExportPath = data["ExportPath"]
        options.TempPath = data["TempPath"]
        options.BackupPath = data["BackupPath"]

        options.RenderPath = data["RenderPath"]
        options.WAVPath = data["WAVPath"]
        options.BatchfilePath = data["BatchfilePath"]

        options.CheckUpdates = data["CheckUpdates"]
        options.UnfoldEmptyOrderLists = data["UnfoldEmptyOrderLists"]

        #options.ExternalPlayer = data["ExternalPlayer"]
        #options.UseExternalPlayer = data["UseExternalPlayer"]

        options.DefaultPlayer = data["DefaultPlayer"]
        options.DefaultRenderer = data["DefaultRenderer"]

        #options.AudioDevice = data["AudioDevice"]
        options.AudioDeviceNum = int(data["AudioDeviceNum"])-1
        basslib.Bass.setDevice(options.AudioDeviceNum)

        options.save()
        options.updatePathMemory()
    
    # WDR: handler implementations for PreferencesDialog

    def OnChooseDefaultPlayer(self, event):
        sel = event.GetSelection()
        if sel != options.DefaultPlayer:
            modplayer.switchPlayer(event.GetSelection())

    def OnChooseDefaultRenderer(self, event):
        options.DefaultRenderer = event.GetSelection()


    def OnSelectExternalPlayer(self, event):
        path = wxx.SelectFile(self, ext="*.exe", saving=0, multi=0)
        if path:
            self.SetControlLabel("ExternalPlayer", path)
        

    def OnBatchfilePath(self, event):
        path = SelectPath(self, self.GetControlLabel("BatchfilePath"))
        if path:
            self.SetControlLabel("BatchfilePath", path)
        

    def OnWAVPath(self, event):
        path = wxx.SelectPath(self, self.GetControlLabel("WAVPath"))
        if path:
            self.SetControlLabel("WAVPath", path)
        

    def OnRenderPath(self, event):
        path = wxx.SelectPath(self, self.GetControlLabel("RenderPath"))
        if path:
            self.SetControlLabel("RenderPath", path)
        

    def OnSelectBackupPath(self, event):
        path = wxx.SelectPath(self, self.GetControlLabel("BackupPath"))
        if path:
            self.SetControlLabel("BackupPath", path)
        
    def OnSelectTempPath(self, event):
        path = wxx.SelectPath(self, self.GetControlLabel("TempPath"))
        if path:
            self.SetControlLabel("TempPath", path)    

    def OnSelectExportPath(self, event):
        path = wxx.SelectPath(self, self.GetControlLabel("ExportPath"))
        if path:
            self.SetControlLabel("ExportPath", path)

    def OnSelectDefaultPath(self, event):
        path = wxx.SelectPath(self, self.GetControlLabel("DefaultPath"))
        if path:
            self.SetControlLabel("DefaultPath", path)

    def OnCancel(self, event):
        self.Close()

    def OnOK(self, event):
        self.TransferDataFromWindow()
        self.Close()
