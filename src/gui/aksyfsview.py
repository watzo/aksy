
from wxPython.wx import wxPySimpleApp, wxFrame, wxPanel, wxID_ANY, wxDEFAULT_FRAME_STYLE, wxNO_FULL_REPAINT_ON_RESIZE, wxTR_DEFAULT_STYLE, wxART_FOLDER, wxART_FILE_OPEN, wxART_OTHER, EVT_SIZE, wxImageList, wxArtProvider_GetBitmap, wxTreeItemIcon_Normal, wxTreeItemIcon_Expanded, wxART_REPORT_VIEW, wxTreeItemIcon_Selected, wxMenu, wxMenuBar, EVT_MENU, wxMessageDialog, wxOK, wxPopupWindow, EVT_RIGHT_DOWN, EVT_RIGHT_UP, wxSIMPLE_BORDER, wxPopupTransientWindow, wxStaticText

from wxPython.gizmos import wxTreeListCtrl
from wxPython.wx import wxID_CUT, wxID_COPY, wxNewId, wxID_OK
from wxPython.wx import EVT_CLOSE,EVT_TREE_BEGIN_LABEL_EDIT, EVT_TREE_END_LABEL_EDIT, EVT_TREE_ITEM_EXPANDING, EVT_TREE_ITEM_ACTIVATED
from wxPython.wx import EVT_TREE_SEL_CHANGED, EVT_TREE_KEY_DOWN, WXK_DELETE
from wxPython.wx import wxDirDialog, wxDD_NEW_DIR_BUTTON, wxDD_DEFAULT_STYLE, wxTR_MULTIPLE,wxTR_EDIT_LABELS, wxTR_HIDE_ROOT 
from wxPython.wx import wxFileDialog, wxTheClipboard, wxFileDataObject,wxDF_FILENAME

import wrappers
import aksysdisktools, program_main, multi_main, sample_main
import aksy
import os.path, traceback

ID_ABOUT=wxNewId()
ID_EXIT=wxNewId()

USE_MOCK_OBJECTS = True

class Frame(wxFrame):
    def __init__(self,parent,title):
        wxFrame.__init__(self,parent,wxID_ANY, title, size = ( 200,100),
                         style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE) 
       
        filemenu= wxMenu()
        filemenu.Append(ID_ABOUT, "&About"," Information about this program")
        filemenu.Append(wxID_COPY, "Copy\tCtrl+C", "Copy") 
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit\tCtrl+Q"," Terminate the program")

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

        try:
            self.z.init()
        except Exception, e:
            self.reportException(e)
            return

    def OnAbout(self,e):
        d= wxMessageDialog(self, " Aksy, controlling your Z48 sampler\n", "About Aksy", wxOK)
        d.ShowModal() 
        d.Destroy() 
    def OnExitMenu(self,e):
        self.Close(True) 
    def OnExit(self,e):
        self.z.close()
        self.Destroy() 

          
    def reportException(self, exception):
        traceback.print_exc()
        d= wxMessageDialog( self, "%s\n" % exception[0], "An error occurred", wxOK)
        d.ShowModal() 
        d.Destroy() 

class AksyFSTree(wxTreeListCtrl):
    def __init__(self, parent, id, **kwargs):
        wxTreeListCtrl.__init__(self, parent, id, **kwargs)

        isz = (16,16)
        il = wxImageList(isz[0], isz[1])
        # add icons for programs, multis, samples

        self.fldridx     = il.Add(wxArtProvider_GetBitmap(wxART_FOLDER,      wxART_OTHER, isz))
        self.fldropenidx = il.Add(wxArtProvider_GetBitmap(wxART_FILE_OPEN,   wxART_OTHER, isz))
        self.fileidx     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        
        self.program_icon     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        self.multi_icon     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        self.sample_icon     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        self.SetImageList(il)
        self.il = il

        # create some columns
        self.AddColumn("")
        self.AddColumn("Size")
        self.AddColumn("Used by")
        self.AddColumn("Modified")
        self.SetMainColumn(0) 
        self.SetColumnWidth(0, 450)

        self.root = self.AddRoot("Z48")
        self.SetItemImage(self.root, self.fldridx, which = wxTreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, which = wxTreeItemIcon_Expanded)
        self._index = {}

        EVT_TREE_ITEM_EXPANDING(self, id, self.OnItemExpanding)
        EVT_TREE_ITEM_ACTIVATED(self, id, self.OnItemActivate)
        EVT_TREE_SEL_CHANGED(self, id, self.OnSelChanged)
        EVT_TREE_KEY_DOWN(self, id, self.OnKeyDown)

    def AppendAksyItem(self, parent, item, depth=1):

        """Appends an item to the tree. default is root
        """
        if parent is None:  
            parent = self.root

        child = wxTreeListCtrl.AppendItem(self, parent, item.name)
        if depth == 1 and item.has_children():
        
            print "Child %s.Name: %s Aksy children: " % (repr(child), item.name)
            for grandchild in item.get_children():
                print "Child %s.Name: %s Aksy children: " % (repr(child), grandchild.name)
                wx_grandchild = self.AppendAksyItem(child, grandchild, 0)
                self.SetPyData(wx_grandchild, grandchild)

        self.SetPyData(child, item)
        self.AddItemIndex(item.name, child)

        if isinstance(item, wrappers.File):
            if item.type == wrappers.File.MULTI:
                self.SetItemImage(child, self.multi_icon, which = wxTreeItemIcon_Normal)
            elif item.type == wrappers.File.PROGRAM:
                self.SetItemImage(child, self.program_icon, which = wxTreeItemIcon_Normal)
            elif item.type == wrappers.File.SAMPLE:
                self.SetItemImage(child, self.sample_icon, which = wxTreeItemIcon_Normal)
            elif item.type == wrappers.File.FOLDER:
                self.SetItemImage(child, self.fldridx, which = wxTreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, which = wxTreeItemIcon_Expanded)
            else:
                self.SetItemImage(child, self.fileidx, which = wxTreeItemIcon_Normal)
                self.SetItemImage(child, self.fileidx, which = wxTreeItemIcon_Expanded)
        else:
            self.SetItemImage(child, self.fldridx, which = wxTreeItemIcon_Normal)
            self.SetItemImage(child, self.fldridx, which = wxTreeItemIcon_Expanded)

        return child

    def AddItemIndex(self, name, wx_id):
        self._index[name] = wx_id

    def GetItemByName(self, name):
        return self._index[name]

    def OnSelChanged(self, evt):
        print "OnSelChanged: %s" % repr(evt.GetItem())

    def OnKeyDown(self, evt):
        id = self.GetSelection()
        item = self.GetPyData(id)
        print  repr(item)
        if evt.GetKeyCode() == WXK_DELETE:
            print "OnKeyDown delete: %s" % item.name
            self.Delete(id)

    def OnItemExpanding(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)
        print "OnItemExpanding: %s" % item.name

        cookie = 1
        """
        """
        wx_child, cookie = self.GetFirstChild(id, cookie)
        last_child = self.GetLastChild(id) 
            
        while 1:
            child_item = self.GetPyData(wx_child)
            if not self.ItemHasChildren(wx_child) and child_item.has_children():
                for child in child_item.get_children():
                    print "Appending Child %s.Name: %s Aksy children: %s" % (repr(wx_child), child_item.name, repr(child_item.get_children()))
                    # subfolders
                    self.AppendAksyItem(wx_child, child) 

            wx_child,cookie = self.GetNextChild(id, cookie)
            if wx_child == last_child: break

    def OnItemActivate(self, evt):
        # TODO: hookup the edit views here
        id = evt.GetItem()
        item = self.GetPyData(id)
        print "Item activated for item %s" % item.name

class TestPanel(wxPanel):
    def __init__(self, parent):
        # TODO:config item!

        self.lastdir = os.path.expanduser("~")
        if len(self.lastdir) == 1:
            self.lastdir = ""

        wxPanel.__init__(self, parent, -1)
        self.z = parent.z
        EVT_SIZE(self, self.OnSize)

        self.tree = AksyFSTree(self, 5001, style=wxTR_EDIT_LABELS|wxTR_HIDE_ROOT|wxTR_DEFAULT_STYLE|wxTR_MULTIPLE)
        self.actions = {}
        self.register_menu_actions(wrappers.Folder.actions)
        self.register_menu_actions(wrappers.File.actions)
        self.register_menu_actions(wrappers.Program.actions)
        self.register_menu_actions(wrappers.Multi.actions)
        self.register_menu_actions(wrappers.InMemoryFile.actions)

        EVT_TREE_BEGIN_LABEL_EDIT(self, self.tree.GetId(), self.CheckRenameAction)
        EVT_TREE_END_LABEL_EDIT(self, self.tree.GetId(), self.RenameAction)
        EVT_RIGHT_UP(self.tree.GetMainWindow(), self.contextMenu)
        EVT_MENU(self, wxID_COPY, self.OnCopy)   
        EVT_MENU(parent, wxID_COPY, self.OnCopy)   

        disks = wrappers.Storage("disk")
        mem = wrappers.Storage("memory")

        storage = [disks, mem]

        disks_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), disks)
        mem_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), mem)

        program_module = self.z.program_module
        sample_module = self.z.sample_module
        multi_module = self.z.multi_module
        wrappers.File.init_modules(
            {wrappers.File.MULTI: multi_module,
             wrappers.File.PROGRAM: program_module,
             wrappers.File.SAMPLE: sample_module, })

        # Move this stuff somewhere else...
        if not USE_MOCK_OBJECTS:
            try:  
                # not fool proof for multiple disks   
                disk = wrappers.Disk(self.z.disktools.get_disklist())
                self.z.disktools.select_disk(disk.handle)
                rootfolder = wrappers.Folder(self.z.disktools, ("",))
                folders = rootfolder.get_children()
                disks.set_children(folders)
                for folder in folders:
                    self.tree.AppendAksyItem(disks_id, folder)

                # programs = self.z.program_main.get__names()
                # multis = self.z.multi_main.get_names()
                # samples = self.z.sample_main.get_names()
            except Exception, e:
                parent.reportException(e)
                return
        else:
            
            # Setup some items
            disktools = self.z.disktools

            rootfolder = wrappers.Folder(disktools, ("",))
            rootfolder.children.append(wrappers.Folder(disktools,('', 'Autoload',)))
            rootfolder.children.append(wrappers.Folder(disktools,('', 'Songs',)))
            mellotron_folder = wrappers.Folder(disktools,('', 'Mellotron',))
            choir_folder = wrappers.Folder(disktools,('', 'Choir',))
            choir_folder.children.extend(
                (wrappers.File(disktools, ('', 'Mellotron', 'Choir', 'Choir.AKP',)),
                wrappers.File(disktools, ('', 'Mellotron', 'Choir', 'Vox1.wav',)),))

            mellotron_folder.children.extend(
                (choir_folder,
                wrappers.File(disktools, ('', 'Mellotron', 'Sample.AKP',)),
                wrappers.File(disktools, ('', 'Mellotron', 'Sample.wav',)),))
            rootfolder.children.append(mellotron_folder)
            disks.set_children(rootfolder.get_children())

            for folder in rootfolder.get_children():
                 item = self.tree.AppendAksyItem(disks_id, folder)

        self.tree.Expand(self.tree.root)

    """Copy and paste operations.
    2 types: 
        -copy/paste aksy items in the tree
        -copy/paste filenames between aksy 
    """

    def OnCopy(self, evt):
        # this is always a node to be copied.
        id = self.tree.GetSelection()

        item = self.tree.GetPyData(id)
        print repr(item.name)
        if wxTheClipboard.Open():
            data = wxFileDataObject()
            if wxTheClipboard.GetData(data):
                print repr(data)
            wxTheClipboard.Close()

    def OnCut(self, evt):
        # this is always a node
        # hide it
        if wxTheClipboard.Open():
            data = wxFileDataObject()
            if wxTheClipboard.GetData(data):
                # get the filenames 
                pass
            wxTheClipboard.Close()
        
    def OnPaste(self, evt):
        if wxTheClipboard.Open():
            data = wxFileDataObject()
            if wxTheClipboard.GetData(data):
               pass 
            # or a cut/copied node
            # if cut -> paste the node to the new location
            # and remove the old node
            # otherwise create the new node

 

    def register_menu_actions(self, actions):

        # hook into actions
        if actions.has_key('transfer') and actions == wrappers.Folder.actions:
            actions['transfer'].prolog = self.select_directory

        if actions.has_key('transfer') and actions == wrappers.File.actions:
            actions['transfer'].prolog = self.select_file

        if actions.has_key('load'):
            actions['load'].epilog = self.add_to_memory_branch

        if actions.has_key('delete') and actions == wrappers.InMemoryFile.actions:
            actions['delete'].epilog = self.remove_from_memory_branch

        action = wrappers.Action('copy','Copy\tCtrl+C')
        actions['copy'] = action

        for key in actions.keys():
            id = wxNewId()
            actions[key].id = id
            self.actions[id] = actions[key]
            print key 
            EVT_MENU(self, id, self.ExecuteAction)

    def RenameAction(self, evt):
        new_name = evt.GetLabel()
        # TODO: implement decent checks
        if len(new_name) == 0:
            evt.Veto()
        
        id = self.tree.GetSelection()
        item = self.tree.GetPyData(id)
        item.rename(new_name)

    def CheckRenameAction(self, evt):
        id = self.tree.GetSelection()
        item = self.tree.GetPyData(id)
        if not hasattr(item, 'rename'):
            evt.Veto()

    def ExecuteAction(self, evt):
        action = self.actions[evt.GetId()]
        # TODO: multiple select
        id = self.tree.GetSelection()
        item = self.tree.GetPyData(id)
        item.id = id

        print "Action %s, item: %s" % (action.display_name, repr(item))
        if action.prolog is None:
            args = ()
        else:
            args = action.prolog(item)
                
        if args is None:
            return

        if len(args) == 0:
            result = action.execute(item)
        else:
            result = action.execute(item, args)

        if action.epilog is not None:
            if result is None:
                action.epilog(item)
            else:
                action.epilog(item, result)

    def select_directory(self, item):
        dir_dialog = wxDirDialog(self, "Choose a destination for %s" %item.name, 
            style=wxDD_DEFAULT_STYLE|wxDD_NEW_DIR_BUTTON)
        dir_dialog.SetPath(self.lastdir)
        if dir_dialog.ShowModal() == wxID_OK:
            self.lastdir = dir_dialog.GetPath()
            retval = (self.lastdir,)
        else:
            retval = None

        dir_dialog.Destroy()
        return retval
        
    def select_file(self, item):
        # TODO: cache this dialog as it is heavy...
        filedialog = wxFileDialog(self, "Choose a destination for %s" %item.name, 
            style=wxDD_DEFAULT_STYLE)
        filedialog.SetDirectory(self.lastdir)
        filedialog.SetFilename(item.name)
        if filedialog.ShowModal() == wxID_OK:
            path = filedialog.GetPath() 
        else:
            path = None

        filedialog.Destroy()
        return (path)
        
    def contextMenu(self, e):
        # TODO: multi-select
        # items = self.tree.GetSelections()
        # make an intersection of the actions
        # show the menu

        # dispatch on file type
        item = self.tree.GetSelection()
        aksy_object = self.tree.GetPyData(item)
        if aksy_object is None or aksy_object.actions is None:
            return
        filemenu = FileMenu(self, wxSIMPLE_BORDER)
        filemenu.set_actions(aksy_object.actions.values())

        self.PopupMenu(filemenu, e.GetPosition())

    def add_to_memory_branch(self, item, result):
        """Updates the memory branch when an item has been loaded
        """
        memory_folder = self.tree.GetItemByName('memory')
        self.tree.AppendAksyItem(memory_folder, result)
        self.tree.Expand(memory_folder)

    def remove_from_memory_branch(self, item):
        memory_folder = self.tree.GetItemByName('memory')
        self.tree.Delete(item.id)

    def OnSize(self, e):
        self.tree.SetSize(self.GetSize())

class FileMenu(wxMenu):
    def __init__(self, parent, style):
         wxMenu.__init__(self)

    def set_actions(self, actions):
        for index, action in enumerate(actions):
            self.Append(action.id, action.display_name, action.display_name)
         

if __name__ == '__main__':
    app = wxPySimpleApp()
    frame = Frame(None, "Aksy")
    win = TestPanel(frame)
    app.MainLoop()

