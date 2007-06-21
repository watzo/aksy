
MAX_SAMPLE_EXPORT_PREVIEWS = 2000

import threading

import wx
import wxx
from wxx import *
from postmod_wdr import *
from postmod_events import *
import postmod_menus

from sample_exporter import *

from options import *


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
            #print "args", self.args
            ITSampleExporter.PreviewExport(*self.args)
            #print "%s ends" % (self.getName(),)
            self.postfunc(*self.postargs)
        except:
            apply(sys.excepthook, sys.exc_info())


class SampleExportThread(threading.Thread):
    def __init__(self, args=(), postfunc=None, postargs=()):
        self.args = args
        self.postfunc = postfunc
        self.postargs = postargs

        threading.Thread.__init__(self)
        
    def run(self):
        try:
            #print "SampleExportThread %s starts" % (self.getName(),)
            #print "args", self.args
            exported, errors = ITSampleExporter.ExportSamples(*self.args)
            #print "%s ends" % (self.getName(),)
            kwargs={'exported':exported, 'errors':errors}
            self.postfunc(*self.postargs, **kwargs)
        except:
            apply(sys.excepthook, sys.exc_info())




class SampleExportDialog(wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE, samples=[], startMessage=[""], files=[], batch=0 ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)

        # samples is an optional list, if provided it is the index numbers of samples to export.
        # it can be used to only export certain samples, rather than all of them.

        # startmessage is an optional list of strings to display in the output listbox.        
        
        SampleExportFunc( self, True )

        self.Centre()        
        
        # WDR: handler declarations for SampleExportDialog
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT_PATH, self.OnSelectExportPath)
        wx.EVT_BUTTON(self, ID_SAMPLE_EXPORT_EXPORT_BUTTON, self.OnExport)
        wx.EVT_BUTTON(self, ID_SAMPLE_EXPORT_PREVIEW_BUTTON, self.OnPreview)
        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOk)
        wx.EVT_BUTTON(self, wx.ID_CANCEL, self.OnCancel)
        wx.EVT_CLOSE(self, self.OnClose)
        
        self.exporter = None
        self.exportThread = None
        self.exportRunning = 0
        self.newBatch = None

        self.files = files

        self.samplesToExport = samples

        self.SetExportPath(options.ExportPath)
        self.SetCallbacks()

        self.GetExportModeBox().SetSelection(0)

        self.SetFocus()

        self.startMessage = startMessage
        self.GetPreviewBox().Set(self.startMessage)

        #BEGIN_DEMO_INCLUDE
        #if batch:
        #    self.GetPreviewBox().Set(["", "     The demo version of Postmod does", "not support batch operations.  Only the", "first file in the currently selected batch", "will be processed."])
        #END_DEMO_INCLUDE
        
        try:
            self.RestoreSettings("SampleExportDialog", exclude=["ExportGauge","OutputBox","ExportButton"])
        except:
            pass

    def SetSamplesToExport(self, samples=[]):
        # pass list of sample indexes, or empty for all.
        self.samplesToExport = samples

    def EnablePreview(self, enable=1):
        pb = self.GetControl("PreviewButton")
        if pb:
            pb.Enable(enable)

    def SetCallbacks(self, process=None, pre=None, post=None):
        self.processCallback = process
        self.preProcessCallback = pre
        self.postProcessCallback = post        

    def ShowChildren(self):
        #print "children"
        children = self.GetChildren()
        for x in children:
            print "name", x.GetName(), "label", x.GetLabel(), "id", self.GetId()

    def PrepareExporter(self, filelist):
        """prepares the sample exporter with the given file list and the current dialog settings"""
        #print "preparing exporter"
        data = self.GetControlData()
        self.exporter = ITSampleExporter(filelist, path=data['ExportPath'], seperator=data['Seperator'],
                                         createDir = data['CreateFilenameDir'],
                                         useSampleNames = data['UseSampleNames'],
                                         useSampleFilenames = data['UseSampleFilenames'],
                                         useSampleNumbers = data['UseSampleNumbers'],
                                         filterExtensions = data['FilterExtensions'],
                                         exportMode = exportModes[data['ExportMode']],
                                         samplesToExport=self.samplesToExport)
        
    def PostPreview(self):
        """This method is passed to the preview thread to be called when the thread finishes"""
        prevbutton = self.GetPreviewButton()
        prevbutton.SetLabel("Preview")

    def PostExport(self, exported=None, errors=None):
        """This method is passed to the export thread to be called when the thread finishes"""
        self.EnablePreview(1)
        self.SetControlLabel("ExportButton", "Export")
        if self.newBatch:
            self.newBatch.Autosize()
            self.newBatch.Raise()
            self.newBatch.CentreOnParent()
            self.newBatch.SetFocus()
        self.exportThread = None
        self.exportRunning = 0
        self.SetGauge(100)
        if self.postProcessCallback:
            apply(self.postProcessCallback)

        # send event to main frame telling it to show a new filebatch with the exported filenames
        event = NewFileBatchEvent("Exported Samples", exported, "Exported")
        wx.PostEvent(self.GetParent(), event)
        
        if errors:
            #dlg = wxSingleChoiceDialog(self.GetParent(), 'Unknown errors occured while processing the following files.\nThey may be invalid or corrupt.\n', 'Errors Occured', \
            #                           errors, wxOK)
            #dlg.ShowModal()
            #dlg.Destroy()             
            wx.CallAfter(wxx.showErrorList, self.GetParent(), errors)
            
        #self.Close()
        event = wx.CloseEvent(wx.wxEVT_CLOSE_WINDOW)
        wx.PostEvent(self, event)

            

    def ExportCallback(self, st, progress):
        """This callback adds filename to the processed list, updates progress gauge, and returns 1 or 0 telling the calling process
        whether to keep running"""
        box = self.GetPreviewBox()
        if st:
            box.Append(st)
        box.SetFirstItem(box.GetCount()-1)
        
        if self.newBatch:
            self.newBatch.AddFile(st)    
        self.SetGauge(progress)

        if self.processCallback:
            apply(self.processCallback, (st,))

        return self.exportRunning
    

    def DoExport(self, filelist):
        """Do the sample export based on current dialog settings, and the given file list (usually the parent window's).
            Starts a new thread to do the export."""
        box = self.GetPreviewBox()
        box.Set(["Exporting..."])

        self.EnablePreview(0)

        self.PrepareExporter(filelist)

        self.SetControlLabel("ExportButton", "Cancel")

        wx.GetApp().Yield(1)

        # make new file batch dialog to show the results in.
        name = "Exported WAVs"

        if self.preProcessCallback:
            apply(self.preProcessCallback)

        self.exportThread = SampleExportThread(args=(self.exporter, self.ExportCallback), postfunc=self.PostExport, postargs=())
        self.exportRunning = 1
        self.exportThread.start()

    def CancelExport(self):
        self.exportRunning = 0
        self.SetGauge(0)

    def PreviewCallback(self, st):
        if st:
            self.GetPreviewBox().Append(st)
        return self.exportRunning

    def SetPreviewData(self, filelist):
        """Run a preview of  exported filenames according to current dialog settings,
           filling the preview box with the returned filenames.  Starts a new thread to run the preview."""
        box = self.GetPreviewBox()
        box.Set([])

        self.PrepareExporter(filelist)

        self.SetControlLabel("PreviewButton", "Stop")

        self.exportRunning = 1
        pt = PreviewThread(args=(self.exporter, MAX_SAMPLE_EXPORT_PREVIEWS, self.PreviewCallback), postfunc=self.PostPreview, postargs=())
        pt.start()
        #preview = self.exporter.PreviewExport(MAX_SAMPLE_EXPORT_PREVIEWS, box.Append)
        #box.Set(preview)

    def SetExportPath(self, path):
        ctrl = self.GetExportPathControl()
        ctrl.SetLabel(path)

    def SetGauge(self, progress):
        gauge = self.GetGauge()
        gauge.SetValue(progress)


    # WDR: methods for SampleExportDialog

    def GetExportModeBox(self):
        return self.FindWindowById(ID_CHOICE_EXISTING_FILES)

    def GetGauge(self):
        return self.FindWindowById(ID_GAUGE_EXPORT)

    def GetExportPathControl(self):
        return self.FindWindowById(ID_TEXTCTRL_EXPORTPATH)

    def GetPreviewButton(self):
        return self.FindWindowById(ID_SAMPLE_EXPORT_PREVIEW_BUTTON)

    def GetPreviewBox(self):
        return self.FindWindowById(ID_SAMPLE_EXPORT_PREVIEW_BOX)

    def Validate(self, win):
        return True

    # WDR: handler implementations for SampleExportDialog

    def OnSelectExportPath(self, event):
        path = SelectPath(self, pathtype="export")
        if path:
            self.SetExportPath(path)
        

    def OnExport(self, event):
        buttonStatus = self.GetControlLabel("ExportButton")
        if buttonStatus == "Export":
            #self.DoExport(self.GetParent().GetFileList())
            self.DoExport(self.files)
        elif buttonStatus == "Cancel":
            self.CancelExport()


    def OnPreview(self, event):
        buttonStatus = self.GetControlLabel("PreviewButton")
        #print "buttonStatus is", buttonStatus
        if buttonStatus == "Preview":
            #self.SetPreviewData(self.GetParent().GetFileList())
            self.SetPreviewData(self.files)
        elif buttonStatus == "Stop":
            #print "stopping"
            self.CancelExport()
        

    def OnOk(self, event):
        event.Skip(True)

    def OnCancel(self, event):
        event.Skip(True)

    def OnClose(self, event):
        self.CancelExport()
        
        self.Show(0)
        self.StoreSettings("SampleExportDialog")
        event.Skip(True)
        #self.Destroy()

