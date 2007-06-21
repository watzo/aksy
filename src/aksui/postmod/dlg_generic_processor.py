
import threading, wx, wxx

from postmod_wdr import *
from postmod_events import *
from generic_processor import *

from options import *

MAX_PREVIEWS = 100

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
            GenericProcessor.Preview(*self.args)
            #print "%s ends" % (self.getName(),)
            self.postfunc(*self.postargs)
        except:
            apply(sys.excepthook, sys.exc_info(), {'inthread':1})



class GenericProcessorDialog(wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE, optionalFunc=None, filelist=None, dialogFunc = GenericProcessorDialogFunc, files=None, batch=0 ):

        #print "init", id, title, pos, size, style
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        # dialogFunc can optionally be specified for different variants, for example, GenericSimpleDialogFunc        
        gframe = dialogFunc( self, 0, 0 )

        # optionalFunc should be a wxDesigner generated dialog function, and its main sizer should be wxStaticBoxSizer horizontal.
        if optionalFunc:
            pframe = optionalFunc(self, 0, 0)        
            #gframe.AddSizer( pframe, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )
            #self.GenericDynamicSizer.AddSizer( pframe, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
            self.GenericDynamicSizer.Add( pframe, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
            
        self.SetAutoLayout(True)
        self.SetSizer(gframe)
        gframe.Fit(self)
        gframe.SetSizeHints(self)

        self.Centre()
        self.ShowSubProgress(0)
        
        # WDR: handler declarations for GenericProcessorDialog
        wx.EVT_BUTTON(self, ID_BUTTON_PROCESS, self.OnProcess)
        wx.EVT_BUTTON(self, ID_BUTTON_PREVIEW, self.OnPreview)
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT_PATH, self.OnSelectExportPath)
        wx.EVT_CLOSE(self, self.OnClose)

        box = self.GetExportModeBox()
        if box:
            box.SetSelection(0)

        #BEGIN_DEMO_INCLUDE
        #if batch:
        #    self.GetOutputBox().Set(["", "     The demo version of Postmod does", "not support batch operations.  Only the", "first file in the currently selected batch", "will be processed."])
        #END_DEMO_INCLUDE

        self.files = files
        if not filelist:
            filelist = files

        self.init(filelist)
        self.Config()
        self.SetCallbacks()
        try:
            self.RestoreSettings("GenericProcessorDialog", exclude=["ExportGauge","OutputBox","ProcessButton"])
        except:
            pass

        self.allowCancel = 1


    def init(self, filelist=None):
        """secondary init function to  handle non widget and event handling specific initialization"""
        self.processor = None  # the class that will handle the actual logic
        self.processThread = None  # the thread the processor method with run in
        self.processRunning = 0   # True if the process is running
        self.newWindow = None     # new window created by the process (if any)

        # a filelist can optionally be passed to the dialog constructor.
        # if none is specified, the file list will be retrieved from the parent window's GetFileList() method
        self.filelist = filelist

        self.SetExportPath(options.ExportPath)

    def Config(self, titleBase="Process", titleData="", buttonLabel="Process"):
        self.titleBase = titleBase
        self.titleData = titleData
        self.buttonLabel = buttonLabel
        
        if titleData != "":
            titleData = " - " + titleData
        self.SetTitle(titleBase + titleData)
        self.SetControlLabel("ProcessButton", buttonLabel)

    def SetCallbacks(self, process=None, pre=None, post=None):
        self.processCallback = process
        self.preProcessCallback = pre
        self.postProcessCallback = post

    def AllowCancel(self, allow):
        self.allowCancel = allow
        
    def PrepareProcessor(self, filelist):
        """Prepare the processor instance with the current dialog settings and given file list."""

        data = self.GetControlData()

        exportMode = data.get('ExportMode', None)
        if exportMode:
            exportMode = exportModes[exportMode]
        else:
            exportMode = None
        
        #print "pp", filelist
        self.processor = GenericProcessor(filelist, path=data.get('ExportPath', None), seperator=data.get('Seperator', None),
                                         createDir = data.get('CreateFilenameDir', None),
                                         filterExtensions = data.get('FilterExtensions', None),
                                          prefix = data.get('Prefix', None), suffix = data.get('Suffix', None),
                                          exportMode = exportMode)
        return data

    def PostPreview(self):
        """This method is a callback passed to the preview thread to be called when it finishes."""

        # change the preview button label back to "preview", since it was changed to "stop" at the beginning of the preview process.
        self.SetControlLabel("PreviewButton", "Preview")

    def PostProcess(self, results=None):
        """This method is a callback passed to the export thread to be called when it finishes."""

        try:

            # change the process button label back to "Process", since it was changed to "cancel" at the beginning of processing.
            self.SetControlLabel("ProcessButton", "Process")

            if self.postProcessCallback:
                apply(self.postProcessCallback)

            # update the thread monitor variables            
            self.processThread = None
            self.processRunning = 0
            
            self.SetGauge(100)
            self.SetSubGauge(100)

            self.EnablePreview()

            self.ProcessResultsCallback(results)
            
            event = wx.CloseEvent(wx.wxEVT_CLOSE_WINDOW)
            wx.PostEvent(self, event)
            #self.Close()
        except:
            pass

    def ProcessResultsCallback(self, results):
        # callback to receive results from ProcessFiles, which will be a list of processed files and a list of error files

        if not results:
            return
        
        processed, errors = results

        try:

            # send event to main frame telling it to show a new filebatch with the exported filenames
            if len(processed) > 1:
                #print "posting event for", processed
                event = NewFileBatchEvent("Processed Files", processed, "Processed")
                wx.PostEvent(self.GetParent(), event)

            if errors:
                #dlg = wxSingleChoiceDialog(self.GetParent(), 'Unknown errors occured while processing the following files.\nThey may be invalid or corrupt.\n', 'Errors Occured', \
                #                           errors, wxOK)
                #dlg.ShowModal()
                #dlg.Destroy()
                wx.CallAfter(wxx.showErrorList, self.GetParent(), errors)

        except:
            pass
        

    def ProcessCallback(self, fname, progress=None):
        """This callback is called by the processing thread for every file processed.
        It should return 1 or 0, which specifies whether the calling process should keep running.
        Also adds the passed filename to the preview box and a new window."""

        # append processed filename to preview box                
        box = self.GetOutputBox()
        if box and fname:
            box.Append(fname)
            box.SetFirstItem(box.GetSelection()-1)


        if self.processCallback:
            apply(self.processCallback, (fname,))
            
        # update the progress gauge if a progress value was specified
        if progress != None:
            gauge = self.GetGauge()
            if gauge:
                gauge.SetValue(progress)

        # self.processRunning determines whether the process should keep running or not.
        return self.processRunning


    def RunProcess(self, filelist):
        """Starts the processing thread, first initializing the processor with the current dialog settings and given file list."""

        self.DisablePreview()
        
        box = self.GetOutputBox()
        if box:
            box.Set(["Processing..."])

        self.PrepareProcessor(filelist)

        # change the process button label to "Cancel"
        if self.allowCancel:
            self.SetControlLabel("ProcessButton", "Cancel")
        else:
            self.SetControlLabel("ProcessButton", "Working")

        # make new file batch dialog window to show the results in.
        name = "Exported Files"

        if self.preProcessCallback:
            apply(self.preProcessCallback)

        self.StartProcessThread()

    def StartProcessThread(self):
        raise "Must subclass GenericProcessorDialog and implement StartProcessThread method"

    def CancelProcess(self):
        """stops the currently running process thread and update GUI."""
        self.processRunning = 0
        self.SetGauge(0)


    def SetPreviewData(self, filelist):
        """Run a preview of processed filenames according to current dialog settings,
           filling the preview box with the returned filenames.  Starts a new thread to run the preview."""
        box = self.GetOutputBox()
        if box:
            box.Set([])
            callback = box.Append
        else:
            callback = None

        self.PrepareProcessor(filelist)

        self.SetControlLabel("PreviewButton", "Stop")

        pt = PreviewThread(args=(self.processor, MAX_PREVIEWS, callback), postfunc=self.PostPreview, postargs=())
        pt.start()

    def ShowSubProgress(self, show):
        gauge = self.GetSubGauge()
        if gauge:
            gauge.Show(show)
    
        
    # WDR: methods for GenericProcessorDialog

    def GetSubGauge(self):
        return self.FindWindowById(ID_GAUGE_SUBPROGRESS)

    def GetCreateDirCheckbox(self):
        return self.FindWindowById(ID_CHECKBOX_FILENAMEDIR)

    def GetExportModeBox(self):
        return self.FindWindowById(ID_CHOICE_EXISTING_FILES)

    def GetUncompressCheckbox(self):
        return self.FindWindowById(ID_CHECKBOX_UNCOMPRESS_SAMPLES)

    def GetUnfoldCheckbox(self):
        return self.FindWindowById(ID_CHECKBOX_UNFOLD)

    def EnablePreview(self):
        pb = self.GetPreviewButton()
        if pb:
            pb.Enable(1)

    def DisablePreview(self):
        pb = self.GetPreviewButton()
        if pb:
            pb.Enable(0)
        wx.GetApp().Yield(1)

    def SetExportPath(self, path):
        ctrl = self.GetExportPathControl()
        ctrl.SetLabel(path)

    def SetProgress(self, progress):
        gauge = self.GetGauge()
        if gauge:
            gauge.SetValue(progress)
        else:
            pass
            #print "Warning: Progress Bar handle not found"

    SetGauge = SetProgress

    def SetSubProgress(self, progress):
        gauge = self.GetSubGauge()
        if gauge:
            gauge.SetValue(progress)
        else:
            print "-- Warning: SubProgress Bar handle not found"

    SetSubGauge = SetSubProgress

    def GetGauge(self):
        return self.FindWindowById(ID_GAUGE_EXPORT)

    def GetExportPathControl(self):
        return self.FindWindowById(ID_TEXTCTRL_EXPORTPATH)

    def GetPreviewButton(self):
        return self.FindWindowById(ID_BUTTON_PREVIEW)

    def GetOutputBox(self):
        return self.FindWindowById(ID_SAMPLE_EXPORT_PREVIEW_BOX)


    # WDR: handler implementations for GenericProcessorDialog        

    def OnSelectExportPath(self, event):
        dirdiag = wx.DirDialog(self, "Choose a directory", defaultPath = options.DefaultPath)
        if dirdiag.ShowModal() == wx.ID_OK:
            path = dirdiag.GetPath()
        else:
            path = ""
        dirdiag.Destroy()
        self.SetExportPath(path)
        

    def OnProcess(self, event):
        #print "OnProcess"
        buttonStatus = self.GetControlLabel("ProcessButton")
        if buttonStatus == self.buttonLabel:
            #print "calling RunProcess"
            if self.filelist:
                self.RunProcess(self.filelist)
            else:
                self.RunProcess(self.GetParent().GetFileList())
        elif buttonStatus == "Cancel":
            #print "calling CancelProcess"
            self.CancelProcess()

    def OnPreview(self, event):
        #print "OnPreview"
        buttonStatus = self.GetControlLabel("PreviewButton")
        if buttonStatus == "Preview":
            if self.filelist:
                self.SetPreviewData(self.filelist)
            else:
                self.SetPreviewData(self.GetParent().GetFileList())
        elif buttonStatus == "Stop":
            self.CancelProcess()
        
    def OnOk(self, event):
        event.Skip(True)

    def OnCancel(self, event):
        event.Skip(True)

    def OnClose(self, event):
        self.CancelProcess()
        
        self.Show(0)
        self.StoreSettings("GenericProcessorDialog")
        event.Skip(True)
        #self.Destroy()
        #strange: when destroy is called, everything works (except can't close it before process is done)
        # but when it's not called, we get the weird focus batch problem.


"""
class GenericSimpleProcessorDialog(GenericProcessorDialog):
    def __init__(self, *args, **kwargs):
        kwargs["dialogFunc"] = GenericSimpleDialogFunc
        GenericProcessorDialog(self, *args, **kwargs)
        
        
        # WDR: handler declarations for GenericSimpleProcessorDialog

    # WDR: methods for GenericSimpleProcessorDialog

    # WDR: handler implementations for GenericSimpleProcessorDialog
"""