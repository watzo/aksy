
from wxPython.wx import wxPySimpleApp, wxFrame, wxPanel, wxID_ANY, wxDEFAULT_FRAME_STYLE, wxNO_FULL_REPAINT_ON_RESIZE, wxTR_DEFAULT_STYLE, wxART_FOLDER, wxART_FILE_OPEN, wxART_OTHER, EVT_SIZE, wxImageList, wxArtProvider_GetBitmap, wxTreeItemIcon_Normal, wxTreeItemIcon_Expanded, wxART_REPORT_VIEW, wxTreeItemIcon_Selected, wxMenu, wxMenuBar, EVT_MENU, wxMessageDialog, wxOK, wxPopupWindow, EVT_RIGHT_DOWN, EVT_RIGHT_UP, wxSIMPLE_BORDER, wxPopupTransientWindow, wxStaticText

from wxPython.gizmos import wxTreeListCtrl
from wxPython.wx import wxID_CUT, wxID_COPY
from wxPython.wx import EVT_CLOSE 


import wrappers
import aksysdisktools
import aksy
ID_ABOUT=1001
ID_EXIT=1002
ID_TEST=1003
USE_MOCK_OBJECTS = False

class Frame(wxFrame):
    def __init__(self,parent,title):
        wxFrame.__init__(self,parent,wxID_ANY, title, size = ( 200,100),
                         style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE) 
       
        filemenu= wxMenu()
        filemenu.Append(ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")

        menuBar = wxMenuBar()
        menuBar.Append(filemenu,"&File") 
        self.SetMenuBar(menuBar) 
        self.SetSize((640, 480))
        self.Show(True)
        EVT_MENU(self, ID_EXIT, self.OnExitMenu)   
        EVT_MENU(self, ID_ABOUT, self.OnAbout) 

        EVT_CLOSE(self, self.OnExit)

        if not USE_MOCK_OBJECTS:
            self.z = aksy.Z48()
        else:
            self.z = aksy.MockZ48()

        self.z.init()

    def OnAbout(self,e):
        d= wxMessageDialog( self, " Aksy, controlling your Z48 sampler\n", "About Aksy", wxOK)
        d.ShowModal() 
        d.Destroy() 
    def OnExitMenu(self,e):
        self.Close(True) 
    def OnExit(self,e):
        self.Destroy() 

        if not USE_MOCK_OBJECTS:
            self.z.close()
            

class TestPanel(wxPanel):
    def __init__(self, parent):
        wxPanel.__init__(self, parent, -1)
        self.z = parent.z
        EVT_SIZE(self, self.OnSize)

        self.tree = wxTreeListCtrl(self, 5001, style = wxTR_DEFAULT_STYLE
                                   #| wxTR_ROW_LINES
                                   #| wxTR_NO_LINES | wxTR_TWIST_BUTTONS
                                   )
        isz = (16,16)
        il = wxImageList(isz[0], isz[1])
        fldridx     = il.Add(wxArtProvider_GetBitmap(wxART_FOLDER,      wxART_OTHER, isz))
        fldropenidx = il.Add(wxArtProvider_GetBitmap(wxART_FILE_OPEN,   wxART_OTHER, isz))
        fileidx     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))

        self.tree.SetImageList(il)
        self.il = il

        # create some columns
        self.tree.AddColumn("")
        self.tree.AddColumn("Name")
        self.tree.AddColumn("Used by")
        self.tree.AddColumn("Modified")
        self.tree.SetMainColumn(0) # the one with the tree in it...
        self.tree.SetColumnWidth(0, 175)


        # Move this stuff somewhere else...
        if not USE_MOCK_OBJECTS:
            disk = wrappers.Disk(self.z.disktools.get_disklist())   # not fool proof for multiple
                                                         # disks
            self.z.disktools.select_disk(disk.handle)    # TODO: handle exceptions
            rootfolder = wrappers.Folder(self.z.disktools, [""])
            rootfolder.get_children()

            programs = self.z.program_main.get_program_names()
            multis = self.z.multi_main.get_multi_names()
            samples = self.z.sample_main.get_sample_names()
        else:
            
            # Add some items
            disktools = aksysdisktools.DiskTools(self.z)
            storage = [ "disk", "memory"]
            children = { "disk": (wrappers.Folder(disktools,'Autoload'),
                wrappers.Folder(disktools, 'Mellotron'),
                wrappers.Folder(disktools, 'Songs'))}
            files = { "Autoload": ('Drums.AKP', 'Sample.wav', 'Songs')}
            

    

        self.root = self.tree.AddRoot("Z48")
        self.tree.SetItemImage(self.root, fldridx, which = wxTreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, which = wxTreeItemIcon_Expanded)
        EVT_RIGHT_UP(self.tree.GetMainWindow(), self.contextMenu)

        for item in storage: 
            child = self.tree.AppendItem(self.root, item)
            self.tree.SetItemImage(child, fldridx, which = wxTreeItemIcon_Normal)
            self.tree.SetItemImage(child, fldropenidx, which = wxTreeItemIcon_Expanded)

            if children.has_key(item):
                subfolders = children[item]
                for folder in subfolders:
                    last = self.tree.AppendItem(child, folder.name)
                    self.tree.SetItemText(last, folder.name, 1)
                    self.tree.SetItemText(last, folder.name, 2)
                    self.tree.SetItemImage(last, fldridx, which = wxTreeItemIcon_Normal)
                    self.tree.SetItemImage(last, fldropenidx, which = wxTreeItemIcon_Expanded)


        self.tree.Expand(self.root)

    def contextMenu(self, e):
        # dispatch on file type
        filemenu = FileMenu(self, wxSIMPLE_BORDER)

        self.PopupMenu(filemenu, e.GetPosition())

    def OnSize(self, e):
        self.tree.SetSize(self.GetSize())

class FileMenu(wxMenu):
    def __init__(self, parent, style):
         wxMenu.__init__(self)
         self.Append(wxID_CUT, 'Rename', 'Rename')
         self.Append(wxID_COPY, 'Transfer', 'Transfer to pc')

         EVT_MENU(parent, wxID_CUT, self.OnSelect)
         EVT_MENU(parent, wxID_COPY, self.OnSelect)
    def OnSelect(self, evt):
         print "EVENT"

    def setActions(self, actions):
        for action in actions:
            self.Append(hash(actions), action, action)
         

if __name__ == '__main__':
    app = wxPySimpleApp()
    frame = Frame(None, "Aksy")
    win = TestPanel(frame)
    app.MainLoop()

