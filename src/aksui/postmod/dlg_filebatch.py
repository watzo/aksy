
# TabCtrl_GetItemRect( (HWND) GetHWND(), item, & rect)
# int item = TabCtrl_HitTest( (HWND) GetHWND(), & hitTestInfo ) ;

#int wxTabCtrl::HitTest(const wxPoint& pt, long& flags)
#{
#    TC_HITTESTINFO hitTestInfo;
#    hitTestInfo.pt.x = pt.x;
#    hitTestInfo.pt.y = pt.y;
#    int item = TabCtrl_HitTest( (HWND) GetHWND(), & hitTestInfo ) ;



import app, dirwalk, filex

import wx
from wxx import *
from postmod_wdr import *

from postmod_dialogs import *
from postmod_events import *

import win32api #MOD104

import os.path

# WDR: classes



class FileBatchDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            if os.path.isdir(file):
                self.window.OnAddDirTree(None, file)
            elif file[-2:].lower() == "it":
                self.window.OnAddFiles(None, [file])

        #TODO: add directory dragging
                
        #self.window.OnAddFiles(None, filenames)
        if not self.window.autosized:
            self.window.Autosize()



# FileBatchMultiDialog has a notebook of FileBatchDialogs
# operations on it affect the currently selected FileBatchDialog.
class FileBatchMultiDialog(wx.MDIChildFrame):
    def __init__(self, parent, id, title,
        #pos = wx.DefaultPosition, size = wx.DefaultSize,
        pos = wx.DefaultPosition, size = (10,10),
        style = wx.DEFAULT_FRAME_STYLE, fname=None, mainframe=None ):
        wx.MDIChildFrame.__init__(self, parent, id, title, pos, size, style)
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        self.Show(0)
        
        FileBatchMultiDialogFunc( self, True )

        self.notebook = self.GetNotebook()
        
        wx.EVT_RIGHT_UP(self.notebook, self.OnRightUp)
        #wx.EVT_NOTEBOOK_PAGE_CHANGED(self, ID_NOTEBOOK, self.OnNotebookPageChanged) 
        #wx.EVT_NOTEBOOK_PAGE_CHANGING(self, ID_NOTEBOOK, self.OnNotebookPageChanging) 

        EVT_POSTMOD_NEW_FILEBATCH(self.notebook, self.OnNewFileBatch)


        # i think these are no longer needed in 2.3.3.1...
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_CLOSE(self, self.OnClose)

        self.SetIcon(app.icons.greenwav)

        # dict of FileBatchPanel objects that correspond to wxPanels in the notebook
        self.children = {}

        self.closed = 0        

        dt = FileBatchDropTarget(self)
        self.SetDropTarget(dt)

        self.autosized = 0

        panel = self.AddNewBatch(fname=fname)
        #panel.Show(1)
        #self.AddNewBatch("poop")

    def OnNewFileBatch(self, event):
        fbpanel = self.AddNewBatch(event.name)
        self.AdvanceSelection()
        fbpanel.AddFilesNoDuplicates(event.files)
        fbpanel.Raise()
        fbpanel.SetFocus()
        self.Autosize()
        self.Raise()


    def AddNewBatch(self, name="Batch", fname=None):
        #print "! adding new batch", name, fname

        nb = self.notebook
        #print nb
        if nb:
            fbpanel = FileBatchPanel(nb, -1, fname=fname, mainframe=self.GetParent(), autosizeCallback=self.Autosize, multiparent=self)
            #print fbpanel
            nb.AddPage(fbpanel, name)
            self.children[fbpanel.GetId()] = fbpanel
            #print "set", fbpanel.GetId(), "to", fbpanel
        else:
            fbpanel = None
            
        return fbpanel

    def AddBatch(self, fbpanel, name="Batch"):
        # fbpanel should be an instance of FileBatchPanel, which itself is a wxPanel
        nb = self.notebook
        nb.AddPage(fbpanel, name)
        self.children[fbpanel.GetId()] = fbpanel

    def AdvanceSelection(self, forward=1):
        #print "! Advancing selection..."
        nb = self.notebook
        if nb:
            nb.AdvanceSelection(forward)
        
    def Autosize(self):
        #print "! multi autosizing..."
        dlg = self.GetMainBatch()
        if not dlg:
            return
        dlg.SetIconByBatchType()
        
        list = dlg.list
        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        sz = list.GetBestSize()
        #diag.sizer.SetItemMinSize(list, sz.width, sz.height)

        count = list.GetItemCount()
        maxl = dlg.GetMaxItemLength()
        newx = (maxl * 8) + 20
        newy = (count * 10) + 125
        if newy > 500:
            newy = 500
        if newx < 130:
            newx = 130

        dlg.sizer.SetItemMinSize(list, newx, newy)
        dlg.sizer.Fit(self)
        nb = self.notebook
        nb.Layout()

        if count:
            self.autosized = 1
        
        #print "! done autosizing..."
        
    def GetMainBatch(self):
        #print "! getting main batch"
        nb = self.notebook
        if nb.GetPageCount():
            dlg = nb.GetPage(0)
            fbp = self.children[dlg.GetId()]
            #dlg.__class__ = FileBatchPanel
            #print fbp
            return fbp
        else:
            #print "no batch"
            return None

    def GetCurrentBatch(self):
        #print "! getting current batch"
        nb = self.notebook
        sel = nb.GetSelection()
        if sel > -1:
            dlg = nb.GetPage(sel)
            #print "try to get", dlg.GetId(), "sel", sel
            fbp = self.children[dlg.GetId()]
            #print "fbp", fbp
            #dlg.__class__ = FileBatchPanel
            dlg = fbp
        else:
            dlg = None
        #print fbp
        return fbp

    def SetName(self, name):
        dlg = self.GetCurrentBatch()
        dlg.SetName(name)

    def GetListControl(self):
        dlg = self.GetCurrentBatch()
        list = dlg.list
        return list



    # WDR: methods for FileBatchMultiDialog

    def GetNotebook(self):
        return self.FindWindowById(ID_NOTEBOOK)

    # WDR: handler implementations for FileBatchMultiDialog

    def OnNotebookPageChanged(self, event):
        #print "! notebook page changed"
        #print event.GetOldSelection(), event.GetSelection()
        pass
        #print "changed"

    def OnNotebookPageChanging(self, event):
        #print "! notebook page changing"
        #print event.GetOldSelection(), event.GetSelection()
        pass
        #print "changing"
        

    def OnRightUp(self, event):
        #print "on right up", event.GetId(), event.GetEventObject()
        event.Skip()
        pass
        # this is called when you click on the bottom tab area, but not an actual tab
        #print "right up d00d"

    # these methods simply echo the currently selected FileBatchDialog (actual FileBatchPanel)
    def Save(self, *args, **kwargs):
        self.GetCurrentBatch().Save(*args, **kwargs)
    def Load(self, *args, **kwargs):
        self.GetCurrentBatch().Load(*args, **kwargs)
    def AppendBatchFile(self, *args, **kwargs):
        self.GetCurrentBatch().AppendBatchFile(*args, **kwargs)
    def OnSaveAs(self, *args, **kwargs):
        self.GetCurrentBatch().OnSaveAs(*args, **kwargs)
    def OnAddFiles(self, *args, **kwargs):
        #print self, args, kwargs
        self.GetCurrentBatch().OnAddFiles(*args, **kwargs)
    def OnAddDir(self, *args, **kwargs):
        self.GetCurrentBatch().OnAddDir(*args, **kwargs)
    def OnAddDirTree(self, *args, **kwargs):
        self.GetCurrentBatch().OnAddDirTree(*args, **kwargs)
    def OnItemActivated(self, *args, **kwargs):
        self.GetCurrentBatch().OnItemActivated(*args, **kwargs)
    def GetListItem(self, *args, **kwargs):
        self.GetCurrentBatch().GetListItem(*args, **kwargs)
    def GetListFile(self, *args, **kwargs):
        self.GetCurrentBatch().GetListFile(*args, **kwargs)
    def SetIconByBatchType(self, *args, **kwargs):
        self.GetCurrentBatch().SetIconByBatchType(*args, **kwargs)
    def BatchTypeName(self, *args, **kwargs):
        self.GetCurrentBatch().BatchTypeName(*args, **kwargs)
    def GetITFileList(self, *args, **kwargs):
        self.GetCurrentBatch().GetITFileList(*args, **kwargs)
    def GetWAVFileList(self, *args, **kwargs):
        self.GetCurrentBatch().GetWAVFileList(*args, **kwargs)
    def GetFileList(self, *args, **kwargs):
        self.GetCurrentBatch().GetFileList(*args, **kwargs)
    def GetMaxItemLength(self, *args, **kwargs):
        self.GetCurrentBatch().GetMaxItemLength(*args, **kwargs)
    def ProcessCallback(self, *args, **kwargs):
        self.GetCurrentBatch().ProcessCallback(*args, **kwargs)
    def RenderCallback(self, *args, **kwargs):
        self.GetCurrentBatch().RenderCallback(*args, **kwargs)
    def PreProcessCallback(self, *args, **kwargs):
        self.GetCurrentBatch().PreProcessCallback(*args, **kwargs)
    def PostProcessCallback(self, *args, **kwargs):
        self.GetCurrentBatch().PostProcessCallback(*args, **kwargs)
    def OnIT2XM(self, *args, **kwargs):
        self.GetCurrentBatch().OnIT2XM(*args, **kwargs)
    def OnRender(self, *args, **kwargs):
        self.GetCurrentBatch().OnRender(*args, **kwargs)
    def OnUnfold(self, *args, **kwargs):
        self.GetCurrentBatch().OnUnfold(*args, **kwargs)
    def OnRemoveUnusedSamples(self, *args, **kwargs):
        self.GetCurrentBatch().OnRemoveUnusedSamples(*args, **kwargs)
    def OnBatchSplit(self, *args, **kwargs):
        self.GetCurrentBatch().OnBatchSplit(*args, **kwargs)
    def OnExportSamples(self, *args, **kwargs):
        self.GetCurrentBatch().OnExportSamples(*args, **kwargs)
    def OnDeleteItem(self, *args, **kwargs):
        self.GetCurrentBatch().OnDeleteItem(*args, **kwargs)
    def OnSetFocus(self, *args, **kwargs):
        self.GetCurrentBatch().OnSetFocus(*args, **kwargs)
    def OnImportSamples(self, *args, **kwargs):
        self.GetCurrentBatch().OnImportSamples(*args, **kwargs)
    def AddFile(self, *args, **kwargs):
        self.GetCurrentBatch().AddFile(*args, **kwargs)
    def AddFilesNoDuplicates(self, *args, **kwargs):
        self.GetCurrentBatch().AddFilesNoDuplicates(*args, **kwargs)

    def OnClose(self, event):
        #print "! multi batch on close"
        event.Skip()
        self.closed = 1

    def OnSize(self, event):
        #print "! multi batch on size"
        if not self.closed:
            event.Skip()


#TODO: consider replacing all these copies with a different method.
#for example, a CallMethod method, such as CallMethod(OnUnfold, *args, **kwargs)
# it would call the method on the child, also checking to see whether it existed or not,
# and return (exists, (return values or None)
        
    
class FileBatchDialog(wx.MDIChildFrame):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE, fname=None, mainframe=None, autosizeCallback=None, multiparent=None ):
        wx.MDIChildFrame.__init__(self, parent, id, title, pos, size, style)
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        if not mainframe:
            mainframe = self.GetParent()
        self.mainframe = mainframe

        self.multiparent = multiparent

        self.autosizeCallback = autosizeCallback
        
        self.sizer = FileBatchDialogFunc( self, True )

        self.newTabName = "Processed"        

        #self.SetIcon(postmod_icons.bluefish)
        #self.SetIcon(app.icons.greenwav)
        
        # WDR: handler declarations for FileBatchDialog

        wx.EVT_MENU(self, ID_MENU_PROCESS_UNFOLD, self.OnUnfold)
        wx.EVT_LIST_ITEM_ACTIVATED(self, ID_FILEBATCHLISTCTRL, self.OnItemActivated)
        wx.EVT_LIST_DELETE_ITEM(self, ID_FILEBATCHLISTCTRL, self.OnDeleteItem)
        #wx.EVT_SET_FOCUS(self, self.OnSetFocus)

        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_CLOSE(self, self.OnClose)

        self.list = self.GetListControl()
        self.list.InsertColumn(0, "Path", format=wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(1, "File")

        self.newWindow = None
        self.switchFocus = 0
        self.path = None

        self.resizing = 0        

        if fname:
            self.Load(fname)

    def OnRightUp(self, event):
        #print "howdy", self, event
        event.Skip()

    def SetIcon(self, icon):
        # this dialog might be a child frame, or it might simply be a frame in a notebook.
        # try to set icon as if we are a child frame first.
        try:
            wx.MDIChildFrame.SetIcon(icon)
        except TypeError:
            # try the notebook's parent
            self.GetParent().GetParent().SetIcon(icon)

    # WDR: methods for FileBatchDialog

    # WDR: handler implementations for FileBatchDialog


    def OnSize(self, event):
        if not self.closed:
            event.Skip()

    def OnClose(self, event):
        event.Skip()
        self.closed = 1


    def OldOnSize(self, event):
        # currently not called and obsolete.
        #print "-- fbd OnSize"
        
        if self.resizing or self.closed:
            #print "already resizing!!"
            return
        self.resizing = 1
        
        newx, newy = event.GetSize()
        #newListWidth = newx-25
        #newListHeight = newy-25
        newListWidth = newx
        newListHeight = newy
        newColumnWidth = newListWidth / 2
        
        list = self.list
        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        #list.SetColumnWidth(0, newColumnWidth)
        #list.SetColumnWidth(1, newColumnWidth)
        #list.SetColumnWidth(2, 0)
        self.sizer.SetItemMinSize(list, newListWidth, newListHeight)
        self.sizer.Fit(self)
        self.sizer.Layout()
        self.SetClientSizeWH(newx, newy)
        self.Refresh()

        self.resizing = 0
        #print "-- fbd done resizing"


    # this is a duplicate of GetFileList - but without demo limitations. used by Save().
    def GetSaveFileList(self, extFilter=".it"):
        list = self.list
        numfiles = list.GetItemCount()
        sfl = []

        for x in xrange(0, numfiles):
            path = list.GetItem(x, 0).GetText()
            fname = list.GetItem(x, 1).GetText()
            fullpath = filex.pathjoin(path, fname)
            if not extFilter or string.upper(os.path.splitext(fullpath)[1]) == string.upper(extFilter):
                sfl.append(fullpath)

        return sfl


    def Save(self, path=None):
        if not path:
            path = self.path
        if path:
            f = open(path, "w")
            flist = self.GetSaveFileList(extFilter=None)
            for file in flist:
                f.write(file + "\n")
            f.close()

    def Load(self, path):
        if os.path.exists(path):
            f = open(path, "r")
            for x in f.xreadlines():
                self.AddFile(string.strip(x))
            f.close()
        self.Autosize()

    def AppendBatchFile(self, path):
        self.Load(path)
        self.Autosize()
                

    def OnSaveAs(self, event):
        path = SelectFile(self, ext="*.bch", saving=1, multi=0, pathtype="batch")
        if path:
            self.Save(path)
            self.mainframe.SetTitle(self.BatchTypeName() + " - " + os.path.basename(path))


    def OnAddFiles(self, event, filelist=None):
        if filelist:
            #print "adding flist", filelist
            self.AddFilesNoDuplicates(filelist)
        else:
            paths = SelectFile(self, ext="IT files (*.it)|*.it|WAV files (*.wav)|*.wav", saving=0, multi=1, pathtype="it")
            if paths:
                self.AddFilesNoDuplicates(paths)
            self.Autosize()

    def OnAddDir(self, event):
        path = SelectPath(self, pathtype="it")
        if path:
            flist = dirwalk.Walk(root=path, recurse=0, pattern="*.it")
            flist.sort()
            #print "sorted", flist
            self.AddFilesNoDuplicates(flist)
        self.Autosize()

    def OnAddDirTree(self, event, path=None):
        if not path:
            path = SelectPath(self, pathtype="it")
        if path:
            files = dirwalk.Walk(root=path, recurse=1, pattern="*.it")
            files.sort()
            #print "sorted", files
            self.AddFilesNoDuplicates(files)
        self.Autosize()

    def OnItemActivated(self, event):
        #print "-- activated", event.GetIndex(), event.GetData(), self.GetListControl().GetItem(event.GetIndex(), 1).GetText()
        path = self.list.GetItem(event.GetIndex(), 0).GetText()
        fname = self.list.GetItem(event.GetIndex(), 1).GetText()
        path = filex.pathjoin(path,fname)

        root, ext = os.path.splitext(fname)
        #print "ext", ext
        if string.upper(ext) == ".IT":
            self.mainframe.OpenITFile(path)
        elif string.upper(ext) == ".WAV":   #MOD104
            win32api.ShellExecute(0, "open", path, None, None, 1) #MOD104

    def GetListItem(self, index):
        path = self.list.GetItem(index, 0).GetText()
        fname = self.list.GetItem(index, 1).GetText()
        return [path, fname]

    def GetListFile(self, index):
        path = self.list.GetItem(index, 0).GetText()
        fname = self.list.GetItem(index, 1).GetText()
        fullpath = filex.pathjoin(path, fname)
        return fullpath

    def SetIconByBatchType(self):
        if self.GetWAVFileList():
            self.SetIcon(app.icons.greenwav)
        else:
            self.SetIcon(app.icons.itfile)

    def BatchTypeName(self):
        #TODO: make a function that returns a list of all available extensions in the filelist, and use that to determine name.
        wav = 1
        it = 1
        if self.GetWAVFileList():
            wav = 1
            name = "WAV Batch"
        if self.GetITFileList():
            it = 1
            name = "IT Batch"
        if wav and it:
            name = "File Batch"
        return name

    def GetITFileList(self):
        return self.GetFileList(".it")

    def GetWAVFileList(self):
        return self.GetFileList(".wav")

    def GetFileList(self, extFilter=".it"):
        list = self.list
        numfiles = list.GetItemCount()
        filelist = []

        #BEGIN_DEMO_EXCLUDE
        for x in xrange(0, numfiles):
            path = list.GetItem(x, 0).GetText()
            fname = list.GetItem(x, 1).GetText()
            fullpath = filex.pathjoin(path, fname)
            if not extFilter or string.upper(os.path.splitext(fullpath)[1]) == string.upper(extFilter):
                filelist.append(fullpath)
        #END_DEMO_EXCLUDE

        #BEGIN_DEMO_INCLUDE
        #if numfiles:
        #    path = list.GetItem(0, 0).GetText()
        #    fname = list.GetItem(0, 1).GetText()
        #    fullpath = filex.pathjoin(path, fname)
        #    filelist = [fullpath]
        #END_DEMO_INCLUDE            

        return filelist            
            
        
    def GetMaxItemLength(self):
        list = self.list
        count = list.GetItemCount()
        maxl = 0
        for x in xrange(0, count):
            item = self.GetListItem(x)
            if len(item[0]) + len(item[1]) > maxl:
                maxl = len(item[0]) + len(item[1])
        return maxl

    def ProcessCallback(self, st):
        # not currently used, maybe delete
        return
        # append processed filename to new batch window        
        if self.newWindow:
            self.newWindow.AddFile(st)

    def RenderCallback(self, st):
        # not currently used, maybe delete
        # append processed filename to new batch window        
        if self.newWindow:
            if string.find(st, ".wav") > -1 and st[0:2] != "--":
                self.newWindow.AddFile(st)

    def PreProcessCallback(self):
        # not currently used, maybe delete
        return
        if self.multiparent:
            diag = self.multiparent.AddNewBatch(self.newTabName)
            self.multiparent.AdvanceSelection()
            #diag.Raise()
        else:
            diag = self.mainframe.NewFileBatch(self.newTabName + " Files", focus=0, show=0)
            diag.Raise()
        self.newWindow = diag

    def PostProcessCallback(self):
        # not currently used, maybe delete
        if self.newWindow:
            if self.multiparent:
                self.multiparent.Autosize()
                self.multiparent.Raise()
                ##self.multiparent.CentreOnParent()
            else:
                self.newWindow.Autosize()
                self.newWindow.Raise()
                self.newWindow.CentreOnParent()
            self.switchFocus = 2
        else:
            #print "ppc no new window"
            pass
        
            

    def OnIT2XM(self, event=None):
        if self.GetITFileList():
            dlg = IT2XMDialog(self.GetParent(), -1, "Convert to XM", files=self.GetITFileList())
            #dlg.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
            dlg.ShowModal()
            
    def OnRender(self, event):
        if self.GetITFileList():
            dlg = RenderDialog(self.GetParent(), -1, "Render to WAV", files=self.GetITFileList(), batch=1)
            #dlg.SetCallbacks(self.RenderCallback, self.PreProcessCallback, self.PostProcessCallback)
            #dlg.Show(True)
            dlg.ShowModal()

    def OnUnfold(self, event):
        if self.GetITFileList():
            self.newTabName = "Unfolded"
            diag = UnfolderDialog(self.GetParent(), -1, "Unfold", files=self.GetITFileList(), batch=1)
            #diag.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
            #diag.Show(True)
            diag.ShowModal()

    def OnRemoveUnusedSamples(self):
        if self.GetITFileList():
            self.newTabName = "Optimized"
            diag = SampleRemoverDialog(self.GetParent(), -1, "Remove Unused Samples", files=self.GetITFileList(), batch=1)
            #diag.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
            diag.ShowModal()

                    
    def OnBatchSplit(self, event):
        if self.GetITFileList():
            self.newTabName = "Split"
            diag = ITSplitterDialog(self.GetParent(), -1, "Split Sequences - " + self.mainframe.GetTitle(), files=self.GetITFileList(), batch=1)
            #diag.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
            #diag.Show(True)
            diag.ShowModal()
                
    def OnExportSamples(self, event):
        if self.GetITFileList():
            self.newTabName = "Exported"
            title = self.mainframe.GetTitle()        
            diag = SampleExportDialog(self.GetParent(), -1, "Export Samples - " + title, files=self.GetITFileList(), batch=1)
            #diag.SetCallbacks(self.ProcessCallback, self.PreProcessCallback, self.PostProcessCallback)
            #diag.Show(True)
            diag.ShowModal()

    def GetListControl(self):
        return self.FindWindowById(ID_FILEBATCHLISTCTRL)

    def OnDeleteItem(self, event):
        pass

    def OnSetFocus(self, event):
        #print "crikey!"
        event.Skip()
        pass        

    def OnImportSamples(self):
        wavlist = self.GetWAVFileList()
        if wavlist:
            # get IT file to import wavs into
            fname = SelectFile(self, options.DefaultPath, ext="*.it", pathtype="it")
            if fname:
                overwrite = 0
                
                if os.path.exists(fname):
                    x = ITX(fname=fname, unpack=0)
                    # prompt whether to overwrite existing
                    overwrite = wx.MessageBox("Overwrite existing samples?", "Overwrite or Append", wx.YES_NO | wx.CANCEL)
                    if overwrite == wx.CANCEL:
                        return 0
                    else:
                        overwrite = (overwrite == wx.YES)
                else:
                    x = ITX()

                if len(wavlist) > 99:
                    allow100 = wx.MessageBox("Import more than 99 samples?  IT files with more than 99 samples cannot be loaded in Impulse Tracker,\nbut may be loaded in some other programs (such as Modplug Tracker).", "Allow Unlimited Samples", wx.YES_NO | wx.CANCEL)
                    if allow100 == wx.CANCEL:
                        return 0
                    else:
                        if allow100:
                            x.AllowUnlimitedSamples()

                numLoaded, failed = x.loadSampleList(wavlist, overwrite=overwrite)
                #print "nf", numLoaded, failed
                x.save(fname)

                wx.MessageBox(str(numLoaded) + " samples loaded into " + fname, "Samples loaded", style = wx.OK |wx.ICON_INFORMATION)
                
                
                    
                    

    def AddFile(self, path):
        if path and os.path.exists(path):
            path = path.lower()
            #print "adding", path
            list = self.list
            if list:
                fname = os.path.basename(path)
                pathname = os.path.dirname(path)
                count = list.GetItemCount()
                list.InsertStringItem(count, pathname)
                list.SetStringItem(count, 1, fname)
            #print ".added file"
        else:
            pass
            #print "not adding", path

    def AddFilesNoDuplicates(self, files):
        filelist = map(string.upper, self.GetFileList())
        for f in files:
            if not (string.upper(f) in filelist):
                self.AddFile(f)

    def Autosize(self):
        """careful, calling when we're in a notebook can cause crashes in some circumstances"""
        #print "!!!!!!!! fbd autosize!"
        if self.autosizeCallback:
            self.autosizeCallback()
        else:
            self.SetIconByBatchType()
           
            list = self.list
            list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            sz = list.GetBestSize()
            #diag.sizer.SetItemMinSize(list, sz.width, sz.height)

            count = list.GetItemCount()
            maxl = self.GetMaxItemLength()
            newx = maxl * 8
            newy = (count * 10) + 100
            if newy > 500:
                newy = 500
            
            self.sizer.SetItemMinSize(list, newx, newy)
            self.sizer.Fit(self)
            self.sizer.Layout()



class FileBatchPanel(wx.Panel, FileBatchDialog):
    def __init__(self, parent, id,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.TAB_TRAVERSAL, fname=None, mainframe=None, autosizeCallback=None, multiparent=None ):
        wx.Panel.__init__(self, parent, id, pos, size, style)

        self.autosizeCallback = autosizeCallback

        self.multiparent = multiparent

        if not mainframe:
            mainframe = self.GetParent()
        self.mainframe = mainframe

        self.sizer = FileBatchDialogFunc( self, False )

        self.newTabName = "Processed"        

        #FileBatchDialogFunc( self, True )
        
        # WDR: handler declarations for FileBatchPanel
        wx.EVT_MENU(self, ID_MENU_PROCESS_UNFOLD, self.OnUnfold)
        wx.EVT_LIST_ITEM_ACTIVATED(self, ID_FILEBATCHLISTCTRL, self.OnItemActivated)
        wx.EVT_LIST_DELETE_ITEM(self, ID_FILEBATCHLISTCTRL, self.OnDeleteItem)
        #wx.EVT_SET_FOCUS(self, self.OnSetFocus)

        self.list = self.GetListControl()
        self.list.InsertColumn(0, "Path", format=wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(1, "File")

        self.newWindow = None
        self.switchFocus = 0
        self.path = None

        self.resizing = 0        

        if fname:
            self.Load(fname)


    # WDR: handler implementations for FileBatchPanel

    def OnRightUp(self, event):
        #print "howdy", self, event
        event.Skip()
        
