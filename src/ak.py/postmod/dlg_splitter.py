
MAX_SPLITTER_PREVIEWS = 1000

import threading

import wx

import wxx
from wxx import *
from postmod_wdr import *
from postmod_events import *

import gui_render, utilx

from itsplitter import *

from options import *

# the SELECT_SPLIT_ constants refer to the index of the option in the dialog pulldowns.
SELECT_SPLIT_TRACKS         = 0
SELECT_SPLIT_INSTRUMENTS    = 1
SELECT_SPLIT_PATTERNS       = 2
SELECT_SPLIT_NONE           = 3

SELECT_RENDER_BASS = 0
SELECT_RENDER_MIKMOD = 1


# export modes refer to what happens when a selected filename already exists.
# they are passed as strings to keep the GUI select box transfer simple.
exportModes = ["Overwrite","Ignore","Rename"]


class PreviewThread(threading.Thread):
    def __init__(self, args=(), postfunc=None, postargs=()):
        self.args = args
        self.postfunc = postfunc
        self.postargs = postargs
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            #print "PreviewThread %s starts" % (self.getName(),)
            ITSplitter.Preview(*self.args)
        except:
            apply(sys.excepthook, sys.exc_info())
        try:
            #print "%s ends" % (self.getName(),)
            self.postfunc(*self.postargs)
        except:
            apply(sys.excepthook, sys.exc_info())



class ITSplitThread(threading.Thread):
    def __init__(self, args=(), postfunc=None, postargs=()):
        self.args = args
        self.postfunc = postfunc
        self.postargs = postargs
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            #print "ITSplitThread %s starts" % (self.getName(),)
            #print "args", self.args
            split, errors = ITSplitter.SplitFiles(*self.args)
            #print "%s ends" % (self.getName(),)
            kwargs = {'split':split, 'errors':errors}
            #print "calling", self.postfunc
            self.postfunc(*self.postargs, **kwargs)

        except:
            apply(sys.excepthook, sys.exc_info())


class ITSplitterDialog(wxx.DialogX, gui_render.HasRenderOptions):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE,
        toSplit=[], startMessage=[""], render=None, split1 = None, solosplit=0, files=[], newfilenames={}, currentTrackSettingsFunc=None, batch=0, getFilesFunc=None ):    
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        ITSplitterDialogFunc( self, True )

        self.Centre()
        self.ShowSubProgress(0)
        self.ShowRenderProgress(0)
        
        # WDR: handler declarations for ITSplitterDialog
        wx.EVT_CHOICE(self, ID_SPLIT3_CHOICE, self.OnChoice3)
        wx.EVT_CHOICE(self, ID_SPLIT2_CHOICE, self.OnChoice2)
        wx.EVT_CHOICE(self, ID_SPLIT1_CHOICE, self.OnChoice1)
        wx.EVT_CHECKBOX(self, ID_CHECKBOX_RENDER, self.OnToggleRender)
        wx.EVT_BUTTON(self, ID_GAUGE_EXPORT, self.OnGauge)
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT_PATH, self.OnSelectExportPath)
        wx.EVT_BUTTON(self, ID_SPLITTER_SPLIT_BUTTON, self.OnSplit)
        wx.EVT_BUTTON(self, ID_SPLITTER_PREVIEW_BUTTON, self.OnPreview)
        wx.EVT_BUTTON(self, wx.ID_CANCEL, self.OnCancel)
        #wx.EVT_CHAR(self, self.OnChar)
        wx.EVT_CLOSE(self, self.OnClose)

        wx.EVT_TEXT(self, ID_SPINCTRL_AMPLIFY, self.OnChangeAmplify)
        wx.EVT_CHECKBOX(self, ID_CHECKBOX_NORMALIZE, self.OnToggleNormalize)
        wx.EVT_CHECKBOX(self, ID_CHECKBOX_LOOPCOUNT, self.OnToggleUseLoopCount)    
        wx.EVT_CHECKBOX(self, ID_CHECKBOX_SLICE, self.OnToggleRenderSlice)    
        wx.EVT_CHOICE(self, ID_CHOICE_RENDERER, self.OnChooseRenderer)

        self.splitter = None
        self.newBatch = None
        self.splitRunning = 0

        self.files = files
        self.newfilenames = newfilenames

        self.getFilesFunc = getFilesFunc    # if specified, this will be called back to get files and newfilenames

        self.toSplit = toSplit

        self.currentTrackSettingsFunc = currentTrackSettingsFunc

        sb = self.GetRendererSelectBox()
        if sb:
            sb.SetSelection(options.DefaultRenderer)

        sr = self.GetControl("SampleRate")
        if sr:
            sr.SetSelection(4)

        br = self.GetControl("BitRate")
        if br:
            br.SetSelection(0)

        sr = self.GetControl("InterpolationMode")
        if sr and sr.GetSelection()==-1:
            sr.SetSelection(1)

        sr = self.GetControl("VolumeRampMode")
        if sr and sr.GetSelection()==-1:
            sr.SetSelection(0)


        self.SetCallbacks()
        self.SetExportPath(options.ExportPath)

        if split1 != None:
            self.GetSplit1Choice().SetSelection(split1)
        else:
            self.GetSplit1Choice().SetSelection(SELECT_SPLIT_TRACKS)

        self.GetExportModeBox().SetSelection(0)

        self.startMessage = startMessage
        self.GetPreviewBox().Set(startMessage)

        #BEGIN_DEMO_INCLUDE
        #if batch:
        #    self.GetPreviewBox().Set(["", "     The demo version of Postmod does", "not support batch operations.  Only the", "first file in the currently selected batch", "will be processed."])
        #END_DEMO_INCLUDE

        try:
            self.RestoreSettings("ITSplitterDialog", exclude=["ExportGauge","OutputBox","SplitButton"])
            if render != None:
                rf = self.GetControl("RenderFiles")
                rf.SetValue(render)
                
            self.UpdateRenderOptions()
        except:
            pass

        if split1 != None:
            self.GetSplit1Choice().SetSelection(split1)
        if solosplit:
            self.GetSplit2Choice().SetSelection(SELECT_SPLIT_NONE)
            self.GetSplit3Choice().SetSelection(SELECT_SPLIT_NONE)

        if render != None:
            rf = self.GetControl("RenderFiles")
            rf.SetValue(render)

        self.UpdateRenderOptions()


    def EnablePreview(self, enable=1):
        pb = self.GetControl("PreviewButton")
        if pb:
            pb.Enable(enable)

    def SetSplitterSelection(self, controlname, selection):
        if controlname == 'Split1':
            ctl = self.GetSplit1Choice()
        elif controlname == 'Split2':
            ctl = self.GetSplit2Choice()
        elif controlname == 'Split3':
            ctl = self.GetSplit3Choice()
        if ctl:
            ctl.SetSelection(selection)
            

    def SetCallbacks(self, process=None, pre=None, post=None):
        self.processCallback = process
        self.preProcessCallback = pre
        self.postProcessCallback = post        

    def PrepareSplitter(self, filelist, newfilenames={}):   
        """prepares the sequence splitter with the given file list and the current dialog settings"""
        #print "preparing splitter"
        data = self.GetControlData()
        
        #print "filelist", filelist
        # build keyword argument dict for ITSplitter init.
        # at this point, the "data" dict holds the values of all the dialog's controls, with the
        # keys being the names assigned to the controls.
        # we'll transfer these values, with appropriate changes, to a kwargs dict which will be
        # passed directly to ITSplitter.__init__

        #print "setting progress bars"

        if len(filelist) == 1:
            self.ShowSubProgress(0)
        else:
            self.ShowSubProgress(1)

        if data["RenderFiles"]:
            self.ShowRenderProgress(1)
        else:
            self.ShowRenderProgress(0)

        kwargs = {}
        kwargs["path"] = data["ExportPath"]
        kwargs["seperator"] = data["Seperator"]
        kwargs["createDir"] = data["CreateFilenameDir"]
        kwargs["prependFilename"] = data["PrependFilename"]
        kwargs["optimize"] = data["Optimize"]
        kwargs["exportMode"] = exportModes[data["ExportMode"]]

        kwargs["keepIntermediate"] = data["KeepIntermediate"]
        kwargs["keepITs"] = data["KeepITs"]
        kwargs["renderFiles"] = data["RenderFiles"]

        kwargs["ordersOnly"] = data["OrdersOnly"]        
        kwargs["useTrackDisable"] = data["UseTrackDisable"]
        kwargs["useInstrumentVolumes"] = data["UseInstrumentVolumes"]

        kwargs["exportVegas"] = data["ExportVegas"]

        kwargs["filePrefix"] = data["FilePrefix"]
        kwargs["fileSuffix"] = data["FileSuffix"]

        kwargs["newfilenames"] = newfilenames   
        kwargs["getFilesFunc"] = self.getFilesFunc

        kwargs["padZeroes"] = data["PadZeroes"]
        
        kwargs["renderSlice"] = data["RenderSlice"]
        kwargs["numSlices"] = data["NumSlices"]
        # parse keepslices, convert to list of slice numbers
        ks = data["KeepSlices"]
        if ks:
            ks = ks.replace("-", ":")
            ks = ks.split(":", 1)
            ks = [utilx.stripNonNumerics(i) for i in ks]
            # now ks[0] = fromSlice, ks[1] = toSlice
            if len(ks) < 2:
                ks.append(ks[0])
            if not ks[0]:
                ks[0] = ks[1]
                if not ks[0]:
                    ks[0] = 1
            if not ks[1]:
                ks[1] = ks[0]
            # convert to 0-based, and make it a range.
            ks = range(int(ks[0])-1, int(ks[1]))
            
            kwargs["keepSlices"] = ks


        if data["UseLoopCount"]:    # 104MOD
            kwargs["loopCount"] = data["LoopCount"]
        else:
            kwargs["loopCount"] = 1     # 1 = no looping.

        kwargs["normalizeByParent"] = data["NormalizeByParent"]
        
        currentTrackSettingsFunc = None        
        if data["UseCurrentVolumes"]:
            # if func is passed, current settings will be used.
            currentTrackSettingsFunc = self.currentTrackSettingsFunc
            
        kwargs["currentTrackSettingsFunc"] = currentTrackSettingsFunc
        #print "-- currentTrackSettingsFunc", currentTrackSettingsFunc

        #renderer = options.Renderers[data['Renderer']]
        renderer = data['Renderer']
        #renderOptions = (renderer, data['Amplify'], data['Normalize'])
        samplerate = self.GetControl("SampleRate").GetStringSelection()
        samplerate = int(samplerate)
        bitrate = self.GetControl("BitRate").GetStringSelection()
        volramp = self.GetControl("VolumeRampMode").GetSelection()
        usefloat = (bitrate == "32 bit IEEE")
        renderOptions = {'renderer': renderer, 'amplify': data['Amplify'], 'normalize': data['Normalize'], 'interpolation': data['InterpolationMode'], 'samplerate':samplerate, 'usefloat':usefloat, 'volramp':volramp}
        #print "render options:", renderOptions
        kwargs["renderOptions"] = renderOptions        
        
        splitCriteria = []
        for splitField in ['Split1','Split2','Split3']:
            if data[splitField] == SELECT_SPLIT_PATTERNS:
                splitCriteria.append(SPLITBY_PATTERNS)
            elif data[splitField] == SELECT_SPLIT_TRACKS:
                splitCriteria.append(SPLITBY_TRACKS)
            elif data[splitField] == SELECT_SPLIT_INSTRUMENTS:
                splitCriteria.append(SPLITBY_INSTRUMENTS)
        kwargs["splitCriteria"] = splitCriteria

        splitPrefixes = []
        for crit in splitCriteria:
            if crit == SPLITBY_PATTERNS:
                splitPrefixes.append(data["PatternPrefix"])
            elif crit == SPLITBY_TRACKS:
                splitPrefixes.append(data["TrackPrefix"])
            elif crit == SPLITBY_INSTRUMENTS:
                splitPrefixes.append(data["InstrumentPrefix"])
        kwargs["splitPrefixes"] = splitPrefixes
        kwargs["toSplit"] = self.toSplit

        self.splitter = ITSplitter(filelist, **kwargs)


    def PostPreview(self):
        """This method is passed to the preview thread to be called when the thread finishes"""
        self.SetControlLabel("PreviewButton", "Preview")

    def PostSplit(self, split=None, errors=None):
        """This method is passed to the splitter thread, and is called when the thread finishes"""
        try:
            self.EnablePreview(1)
            self.SetControlLabel("SplitButton", "Split")
            if self.newBatch:
                #print "autosizin"
                #TODO: thread safety
                self.newBatch.Autosize()
            self.splitRunning = 0
            self.SetProgress(100)
            self.SetSubProgress(100)
            if self.postProcessCallback:
                apply(self.postProcessCallback)

            # send event to main frame telling it to show a new filebatch with the exported filenames
            #print "split", split

            if split:
                if split[0][-3:].upper() == "WAV":
                    title = "Rendered WAV Files"
                else:
                    title = "Exported IT Files"
                event = NewFileBatchEvent(title, split, "Split")
                #print "posting", event, "to", self.GetParent()
                #wxPostEvent(self.GetParent().GetMainWindow(), event)
                wx.PostEvent(self.GetParent(), event)
                #print self.GetParent()

            if errors:
                # show errors thread safely
                #wxCallAfter(ShowErrors, self.GetParent(), errors)
                wx.CallAfter(wxx.showErrorList, self.GetParent(), errors)


            # close self thread safely
            event = wx.CloseEvent(wx.wxEVT_CLOSE_WINDOW)
            wx.PostEvent(self, event)
        except:
            # probably destroyed
            pass
        
            
            

    def SplitCallback(self, st, progress=None, subprogress=None):
        """This method is called after every new file is created by the splitter.
        It is used to update the output box (preview box) as well as the new batch window, and the progress gauges."""

        try:
            box = self.GetPreviewBox()
            if box:
                if st:
                    box.Append(st)
                box.SetFirstItem(box.GetCount()-1)

            if self.newBatch:
                self.newBatch.AddFile(st)    

            if progress:
                self.SetProgress(progress)
            if subprogress:
                self.SetSubProgress(subprogress)

            if self.processCallback:
                apply(self.processCallback, (st,))

                
            return self.splitRunning
        except:
            print "-- Error while splitting:"
            traceback.print_exc()
            return 0

    def RenderCallback(self, fileprogress, progress):
        """callback called by the renderer (if any)"""
        try:
            self.SetRenderProgress(progress)
        except:
            # probably destroyed
            pass

    def PreviewCallback(self, st):
        try:
            if st:
                self.GetPreviewBox().Append(st)
            return self.splitRunning
        except:
            return 0


    def DoSplit(self, filelist, newfilenames):  
        """Do the sequence split based on current dialog settings, and the given file list (usually the parent window's).
            Starts a new thread to do the export."""
        #print "DoSplit", filelist
        self.EnablePreview(0)
        
        box = self.GetPreviewBox()
        box.Set(["Splitting..."])

        self.PrepareSplitter(filelist, newfilenames)    

        self.SetControlLabel("SplitButton", "Cancel")
        wx.GetApp().Yield(1)

        # make new file batch dialog to show the results in.
        name = "Exported IT Files"

        if self.preProcessCallback:
            apply(self.preProcessCallback)

        splitterThread = ITSplitThread(args=(self.splitter, self.SplitCallback, self.RenderCallback), postfunc=self.PostSplit, postargs=())
        self.splitRunning = 1
        splitterThread.start()

    def CancelSplit(self):
        self.splitRunning = 0
        self.SetProgress(0)
        

    def SetPreviewData(self, filelist, newfilenames):   
        #print "SetPreviewData", filelist

        box = self.GetPreviewBox()
        box.Set([])

        self.PrepareSplitter(filelist, newfilenames)    
        self.SetControlLabel("PreviewButton", "Stop")

        # box.Append will be used as the callback to add filenames to the box as they are processed (previewed)
        self.splitRunning = 1
        pt = PreviewThread(args=(self.splitter, MAX_SPLITTER_PREVIEWS, self.PreviewCallback), postfunc=self.PostPreview, postargs=())
        pt.start()
        
  
    def SetExportPath(self, path):
        ctrl = self.GetExportPathControl()
        ctrl.SetLabel(path)

    def SetProgress(self, progress):
        gauge = self.GetGauge()
        if gauge:
            gauge.SetValue(progress)


    def SetRenderProgress(self, progress):
        gauge = self.GetRenderGauge()
        if gauge:
            gauge.SetValue(progress)

    def ShowRenderProgress(self, show):
        gauge = self.GetRenderGauge()
        if gauge:
            gauge.Show(show)

    def SetSubProgress(self, progress):
        gauge = self.GetSubGauge()
        if gauge:
            gauge.SetValue(progress)

    def ShowSubProgress(self, show):
        gauge = self.GetSubGauge()
        if gauge:
            gauge.Show(show)

    def ValidateCriteria(self):
        # don't let the user select the same criteria more than once
        data = self.GetControlData()

        cursplits = [data['Split1'], data['Split2'], data['Split3']]        
        criteria = []
        for splitField in ['Split1','Split2','Split3']:
            if data[splitField] == SELECT_SPLIT_PATTERNS:
                if SPLITBY_PATTERNS in criteria:
                    self.SetSplitterSelection(splitField, -1)
                else:
                    criteria.append(SPLITBY_PATTERNS)
                    
            elif data[splitField] == SELECT_SPLIT_TRACKS:
                if SPLITBY_TRACKS in criteria:
                    self.SetSplitterSelection(splitField, -1)
                else:
                    criteria.append(SPLITBY_TRACKS)
                    
            elif data[splitField] == SELECT_SPLIT_INSTRUMENTS:
                if SPLITBY_INSTRUMENTS in criteria:
                    self.SetSplitterSelection(splitField, -1)
                else:
                    criteria.append(SPLITBY_INSTRUMENTS)

        # check vegasedl availability
        # cursplits: 0=track, 1=instrument, 2=pattern, 3=none, -1=none
        while -1 in cursplits:
            cursplits.remove(-1)
        while 3 in cursplits:
            cursplits.remove(3)
        ctl = self.GetControl("ExportVegas")
        if ctl:
            available = (cursplits in ([0],[1]))
            if not available:
                ctl.SetValue(0)
            ctl.Enable(available)
        
        




    # Render Options methods

    """
    def UpdateAmplifyControl(self, normalize=-1):
        if normalize < 0:
            norm = self.GetControl("Normalize")
            normalize = norm.GetValue()
            
        ampcontrol = self.GetControl("Amplify")
        if ampcontrol:
            if normalize:
                ampcontrol.Enable(0)
            else:
                ampcontrol.Enable(1)

    def UpdateRenderOptions(self):
        dorender = self.GetControl("RenderFiles")
        #print "dorender", dorender.GetValue()
        render = self.GetControl("Renderer")
        amp = self.GetControl("Amplify")
        norm = self.GetControl("Normalize")
        inter = self.GetControl("UseInterpolation")
        srate = self.GetControl("SampleRate")
        brate = self.GetControl("BitRate")
        
        if not dorender.GetValue():
            render.Enable(0)
            norm.Enable(0)
            amp.Enable(0)
            inter.Enable(0)
            srate.Enable(0)
            brate.Enable(0)
            return 0
        else:
            render.Enable(1)

        if render.GetSelection() == SELECT_RENDER_BASS:
            norm.Enable(1)
            inter.Enable(1)
            srate.Enable(1)
            brate.Enable(1)
            self.UpdateAmplifyControl()
        else:
            amp.Enable(0)
            norm.Enable(0)
            inter.Enable(0)
            srate.Enable(0)
            brate.Enable(0)
    """
        

    def OnChangeAmplify(self, event):
        pass

    #MOD104
    def OnToggleUseLoopCount(self, event):
        self.UpdateLoopControls()

    #MOD104
    def OnToggleRenderSlice(self, event):
        self.UpdateSliceControls()

    def OnToggleNormalize(self, event):        
        self.UpdateAmplifyControl(event.IsChecked())
                
        
    def OnChooseRenderer(self, event):
        self.UpdateRenderOptions()


    # WDR: methods for ITSplitterDialog

    def GetRenderGauge(self):
        return self.FindWindowById(ID_GAUGE_RENDER)

    def GetSubGauge(self):
        return self.FindWindowById(ID_GAUGE_SUBPROGRESS)

    def GetExportModeBox(self):
        return self.FindWindowById(ID_CHOICE_EXISTING_FILES)

    def GetGauge(self):
        return self.FindWindowById(ID_GAUGE_EXPORT)

    def GetExportPathControl(self):
        return self.FindWindowById(ID_TEXTCTRL_EXPORTPATH)

    def GetSplit3Choice(self):
        return self.FindWindowById(ID_SPLIT3_CHOICE)

    def GetSplit2Choice(self):
        return self.FindWindowById(ID_SPLIT2_CHOICE)

    def GetSplit1Choice(self):
        return self.FindWindowById(ID_SPLIT1_CHOICE)

    def GetPreviewBox(self):
        return self.FindWindowById(ID_SPLITTER_PREVIEW_BOX)

    def GetGauge(self):
        return self.FindWindowById(ID_GAUGE_EXPORT)

    def GetRendererSelectBox(self):
        return self.FindWindowById(ID_CHOICE_RENDERER)


    # WDR: handler implementations for ITSplitterDialog

    def OnChoice3(self, event):
        self.ValidateCriteria()

    def OnChoice2(self, event):
        self.ValidateCriteria()
        
    def OnChoice1(self, event):
        self.ValidateCriteria()
        

    def OnToggleRender(self, event):
        keepits = self.GetControl("KeepITs")
        keepits.Enable(event.IsChecked())
        self.UpdateRenderOptions()
        

    def OnGauge(self, event):
        pass

    def OnSelectExportPath(self, event):
        path = SelectPath(self, pathtype="export")
        if path:
            self.SetExportPath(path)

    def OnSplit(self, event):
        buttonStatus = self.GetControlLabel("SplitButton")
        if buttonStatus == "Split":
            self.DoSplit(self.files, self.newfilenames) 
            #self.DoSplit(self.GetParent().GetFileList())
        elif buttonStatus == "Cancel":
            self.CancelSplit()
        
    def OnPreview(self, event):
        buttonStatus = self.GetControlLabel("PreviewButton")
        if buttonStatus == "Preview":
            self.SetPreviewData(self.files, self.newfilenames)  
            #self.SetPreviewData(self.GetParent().GetFileList())
        elif buttonStatus == "Stop":
            self.CancelSplit()

    def OnChar(self, event):
        event.Skip(True)

    def OnCancel(self, event):
        event.Skip(True)

    def OnClose(self, event):
        self.CancelSplit()

        self.Show(0)
        self.StoreSettings("ITSplitterDialog")
        event.Skip(True)
        self.Destroy()

