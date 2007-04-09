
import threading, traceback
import threadx, processx, filex, utilx

from options import options

from dlg_generic_processor import *
from generic_processor import *
from postmod_wdr import *

from itrender import *
import renderers, gui_render

from itx import *

SELECT_RENDER_BASS = 0
SELECT_RENDER_DUMB = 1
SELECT_RENDER_MIKMOD = 2



class RenderDialog(GenericProcessorDialog, gui_render.HasRenderOptions):
    def __init__(self, *args, **kwargs):
        #kwargs["optionalFunc"] = RenderOptionsFunc
        kwargs["optionalFunc"] = RenderOptionsVerticalFunc
        GenericProcessorDialog.__init__(self, *args, **kwargs)

        wx.EVT_TEXT(self, ID_SPINCTRL_AMPLIFY, self.OnChangeAmplify)
        wx.EVT_CHECKBOX(self, ID_CHECKBOX_NORMALIZE, self.OnToggleNormalize)
        wx.EVT_CHOICE(self, ID_CHOICE_RENDERER, self.OnChooseRenderer)


        self.Config(titleBase="Render", titleData="", buttonLabel="Render")
        self.currentTrackSettingsFunc = None

        # don't assume controls exist, so we can support different kinds of render dialogs

        cb = self.GetUnfoldCheckbox()
        if cb:
            cb.Show(0)

        cb =  self.GetCreateDirCheckbox()
        if cb:
            cb.SetValue(0)

        sb = self.GetRendererSelectBox()
        if sb and sb.GetSelection()==-1:
            sb.SetSelection(options.DefaultRenderer)

        sr = self.GetControl("SampleRate")
        if sr and sr.GetSelection()==-1:
            sr.SetSelection(4)

        sr = self.GetControl("BitRate")
        if sr and sr.GetSelection()==-1:
            sr.SetSelection(0)

        sr = self.GetControl("InterpolationMode")
        if sr and sr.GetSelection()==-1:
            sr.SetSelection(1)



        self.UpdateRenderOptions()
        self.UpdateAmplifyControl()

        self.SetExportPath(options.RenderPath)        
        
        # optionally specify an output filename to override auto-output filename generation
        self.outfile = None        
       
        #self.GetUncompressCheckbox().Show(0)

    def SetCurrentTrackSettingsFunc(self, func):
        self.currentTrackSettingsFunc = func


    def OnChangeAmplify(self, event):
        pass
        

    def OnToggleNormalize(self, event):        
        self.UpdateAmplifyControl(event.IsChecked())
                
        
    def OnChooseRenderer(self, event):
        self.UpdateRenderOptions()
            


    def SetOutfile(self, outfile):
        self.outfile = outfile

    def ProgressCallback(self, progress=None, subprogress=None):
        if progress != None:
            self.SetProgress(progress)
        if subprogress != None:
            self.SetSubProgress(subprogress)

    def PrepareProcessor(self, filelist):
        #print "ppfl", filelist

        # the generic PrepareProcessor transfers data to a dict from the controls, based on names.
        data = GenericProcessorDialog.PrepareProcessor(self, filelist)
        
        # cast processor instance from GenericProcessor to ITRenderer
        self.processor.__class__ = ITRenderer

        #renderer = options.Renderers[data['Renderer']]
        print ".RENDERER", data['Renderer']
        renderer = data['Renderer'] # renderer number

        samplerate = int(self.GetControl("SampleRate").GetStringSelection())
        bitrate = self.GetControl("BitRate").GetStringSelection()
        volramp = self.GetControl("VolumeRampMode").GetSelection()
        self.processor.init(renderer, callback=self.ProgressCallback, amplify=data['Amplify'], normalize=data['Normalize'], interpolation=data['InterpolationMode'], samplerate=samplerate, usefloat=(bitrate=="32 bit IEEE"), volramp=volramp)

        if self.outfile:
            self.processor.SetOutfile(self.outfile)

        if data['UseCurrentVolumes']:
            self.processor.SetCurrentTrackSettingsFunc(self.currentTrackSettingsFunc)
        else:
            pass

        numfiles = len(filelist)

        # if there's only one file, set its explicit outpath, because this will be a RenderSingleDialog        
        if numfiles == 1 and self.__class__ == RenderSingleDialog:
            ofile = self.GetControlLabel("ExportPath")
            self.processor.SetOutfile(ofile)
            self.outfile = ofile

        self.ShowSubProgress((numfiles > 1))



    def ProcessCallback(self, *args, **kwargs):
        try:
            return GenericProcessorDialog.ProcessCallback(self, *args, **kwargs)
        except:
            return 0
        
        #box = self.GetOutputBox()
        #box.Refresh()

    def StartProcessThread(self):
        #print "RenderDialog.StartProcessThread"
        # start the processing thread
        self.processThread = threadx.GenericThread(ITRenderer.ProcessFiles, (self.processor, self.ProcessCallback,), {}, \
                                                   self.PostProcess, resultCallback=self.ProcessResultsCallback)
        self.processRunning = 1
        self.processThread.start()

    def GetRendererSelectBox(self):
        return self.FindWindowById(ID_CHOICE_RENDERER)



class RenderSingleDialog(RenderDialog):
    def __init__(self, *args, **kwargs):
        kwargs["dialogFunc"] = GenericSimpleDialogFunc
        RenderDialog.__init__(self, *args, **kwargs)

        wx.EVT_TEXT(self, ID_SPINCTRL_AMPLIFY, self.OnChangeAmplify)
        wx.EVT_CHECKBOX(self, ID_CHECKBOX_NORMALIZE, self.OnToggleNormalize)
        wx.EVT_CHOICE(self, ID_CHOICE_RENDERER, self.OnChooseRenderer)

        #self.Disconnect(ID_BUTTON_EXPORT_PATH, -1, wxwx.EVT_COMMAND_BUTTON_CLICKED)
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT_PATH, self.OnSelectExportPath)

        self.Config(titleBase="Render", titleData=self.GetTitle(), buttonLabel="Render")

        self.AllowCancel(0)

        self.UpdateRenderOptions()
        self.UpdateAmplifyControl()

        self.GetControl("PreviewButton").Show(0)        

        #self.SetExportPath(options.RenderPath)

        self.outfile = None    

    def SetOutfile(self, outfile):
        self.outfile = outfile
        self.SetExportPath(outfile)

    def OnSelectExportPath(self, event):
        path = SelectFile(self, ext="*.wav", pathtype="render")
        if path:
            self.SetOutfile(path)

    def ProgressCallback(self, progress=None, subprogress=None):
        try:
            if progress != None:
                self.SetProgress(progress)
            if subprogress != None:
                self.SetProgress(subprogress)
        except:
            pass

        

            