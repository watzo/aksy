
from wxPython.wx import wxPySimpleApp, wxFrame, wxPanel, wxID_ANY, wxDEFAULT_FRAME_STYLE, wxNO_FULL_REPAINT_ON_RESIZE, wxTR_DEFAULT_STYLE, wxART_FOLDER, wxART_FILE_OPEN, wxART_OTHER, EVT_SIZE, wxImageList, wxArtProvider_GetBitmap, wxTreeItemIcon_Normal, wxTreeItemIcon_Expanded, wxART_REPORT_VIEW, wxTreeItemIcon_Selected, wxMenu, wxMenuBar, EVT_MENU, wxMessageDialog, wxOK, wxPopupWindow, EVT_RIGHT_DOWN, EVT_RIGHT_UP, wxSIMPLE_BORDER, wxPopupTransientWindow, wxStaticText
from wxPython.wx import wxImage, wxBITMAP_TYPE_PNG,wxDF_TEXT, wxPlatform
from wxPython.gizmos import wxTreeListCtrl
from wxPython.wx import wxID_CUT, wxID_COPY, wxID_PASTE, wxNewId, wxID_OK, wxPyDataObjectSimple, wxTextDataObject, wxFileDropTarget
from wxPython.wx import EVT_CLOSE,EVT_TREE_BEGIN_LABEL_EDIT, EVT_TREE_END_LABEL_EDIT, EVT_TREE_ITEM_EXPANDING, EVT_TREE_ITEM_ACTIVATED
from wxPython.wx import EVT_TREE_SEL_CHANGED, EVT_KEY_UP, EVT_TREE_KEY_DOWN, WXK_DELETE, EVT_TREE_BEGIN_DRAG, EVT_TREE_END_DRAG, WXK_F2, wxYES_NO, wxID_YES
from wxPython.wx import wxDirDialog, wxDD_NEW_DIR_BUTTON, wxDD_DEFAULT_STYLE, wxTR_MULTIPLE,wxTR_EDIT_LABELS, wxTR_HIDE_ROOT 
from wxPython.wx import wxFileDialog, wxTheClipboard, wxFileDataObject,wxDF_FILENAME,wxDialog,wxDataObject, wxConfig, wxFileConfig, wxCONFIG_USE_LOCAL_FILE

from aksy import model
from aksy.device import Device, Devices
import os.path, traceback, sys, copy

ID_ABOUT=wxNewId()
ID_EXIT=wxNewId()
ID_MAIN_PANEL = wxNewId()

class Frame(wxFrame):
    def __init__(self,parent,title):
        wxFrame.__init__(self,parent,wxID_ANY, title, size = ( 200,100),
                         style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE) 
       
        filemenu= wxMenu()
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit\tCtrl+Q"," Terminate the program")

        self.action_menu = ActionMenu(self, wxSIMPLE_BORDER)
        helpmenu = wxMenu()
        helpmenu.Append(ID_ABOUT, "&About"," Information about this program")

        menuBar = wxMenuBar()
        menuBar.Append(filemenu,"&File") 
        menuBar.Append(self.action_menu,"&Actions") 
        menuBar.Append(helpmenu,"&Help") 
        self.SetMenuBar(menuBar) 
        self.SetSize((800, 600))
        self.Show(True)
        EVT_MENU(self, ID_EXIT, self.OnExit)
        EVT_MENU(self, ID_ABOUT, self.OnAbout) 

        EVT_CLOSE(self, self.OnExit)

        try:
            self.sampler = Devices.get_instance('akai', 'usb', debug=0)
            self.sampler.init()
        except Exception, e:
		    # if e[0] == "No sampler found":
            self.sampler = Devices.get_instance('mock_z48', debug=1)
            self.sampler.init()
            self.reportException(e)
            return

    def OnAbout(self,e):
        d= wxMessageDialog(self, " Aksy, controlling your Z48 sampler\n", "About Aksy", wxOK)
        d.ShowModal() 
        d.Destroy() 

    def OnExitMenu(self,e):
        self.on_exit()
        self.Close(True)

    def OnExit(self,e):
        self.on_exit()
        self.Destroy() 

    def on_exit(self):
        self.FindWindowById(ID_MAIN_PANEL).store_config()
        try:
            self.sampler.close()
        except Exception, e:
            pass

    def set_edit_menu(self, menu):
        self.GetMenuBar().Replace(1, menu, "Actions")

    def reportException(self, exception):
        traceback.print_exc()
        d= wxMessageDialog( self, "%s\n" % exception[0], "An error occurred", wxOK)
        d.ShowModal() 
        d.Destroy() 

class AksyFSTree(wxTreeListCtrl):
    def __init__(self, parent, id, **kwargs):
        wxTreeListCtrl.__init__(self, parent, id, **kwargs)
        target = AksyFileDropTarget(self)
        self.SetDropTarget(target)

        isz = (16,16)
        il = wxImageList(isz[0], isz[1])
        # add icons for programs, multis, samples

        # self.fldridx     = il.Add(wxArtProvider_GetBitmap(wxART_FOLDER,      wxART_OTHER, isz))
        #self.fldropenidx = il.Add(wxArtProvider_GetBitmap(wxART_FILE_OPEN,   wxART_OTHER, isz))
        self.fileidx     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        
        img_path = test_dir = os.path.join(os.path.split(__file__)[0], 'img')
        self.diskidx = il.Add(wxImage(os.path.join(img_path, 'harddisk.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())
        self.memidx = il.Add(wxImage(os.path.join(img_path, 'memory.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())
        self.fldridx = il.Add(wxImage(os.path.join(img_path, 'folder.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())
        self.fldropenidx = il.Add(wxImage(os.path.join(img_path, 'folder-open.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())

        #self.program_icon     = il.Add(wxArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        self.program_icon     = il.Add(wxImage(os.path.join(img_path, 'program.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())
        self.multi_icon     = il.Add(wxImage(os.path.join(img_path, 'multi.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())
        self.sample_icon     = il.Add(wxImage(os.path.join(img_path, 'sample.png'), wxBITMAP_TYPE_PNG).ConvertToBitmap())
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
        self._item_to_id = {}

        EVT_TREE_ITEM_EXPANDING(self, id, self.OnItemExpanding)
        EVT_TREE_ITEM_ACTIVATED(self, id, self.OnItemActivate)
        EVT_TREE_BEGIN_DRAG(self, id, self.OnItemBeginDrag)
        EVT_TREE_END_DRAG(self, id, self.OnItemEndDrag)
        EVT_TREE_SEL_CHANGED(self, id, self.OnSelChanged)
        EVT_TREE_KEY_DOWN(self, id, self.OnKeyDown)

    def OnItemBeginDrag(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)
        if isinstance(item, model.File):
            self.draggedItem = item
            print "BeginDrag ", self.draggedItem.get_name()
            evt.Allow()

    def OnItemEndDrag(self, evt):
        dest = evt.GetItem()
        item = self.GetPyData(dest)
        print "EndDrag %s, Mod: %s" % (repr(item), repr(evt.GetKeyCode()))
        if not isinstance(item, model.Folder):
            return
        # do copy operation
        self.AppendAksyItem(dest, self.draggedItem)

    def AppendAksyItem(self, parent, item):

        """Appends an item to the tree. default is root
        """
        if parent is None:  
            parent = self.root

        print "AppendAksyItem: Child name: %s has children: %s" % (item.get_name(), item.has_children())
        child = wxTreeListCtrl.AppendItem(self, parent, item.get_name())
        if item.has_children():
            self.SetItemHasChildren(child)

        self.SetPyData(child, item)
        self.AddItemIndex(item.get_handle(), child)

        if not isinstance(item, model.Storage):
            self.SetItemText(child, str(item.get_size()), 1)
            self.SetItemText(child, str(item.get_used_by()), 2)
            self.SetItemText(child, str(item.get_modified()), 3)

        if isinstance(item, model.File):
            if item.type == model.File.MULTI:
                self.SetItemImage(child, self.multi_icon, which = wxTreeItemIcon_Normal)
            elif item.type == model.File.PROGRAM:
                self.SetItemImage(child, self.program_icon, which = wxTreeItemIcon_Normal)
            elif item.type == model.File.SAMPLE:
                self.SetItemImage(child, self.sample_icon, which = wxTreeItemIcon_Normal)
            elif item.type == model.File.FOLDER:
                self.SetItemImage(child, self.fldridx, which = wxTreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, which = wxTreeItemIcon_Expanded)
            else:
                self.SetItemImage(child, self.fileidx, which = wxTreeItemIcon_Normal)
                self.SetItemImage(child, self.fileidx, which = wxTreeItemIcon_Expanded)
        elif isinstance(item, model.Storage):
            if isinstance(item, model.Memory):
                self.SetItemImage(child, self.memidx, which = wxTreeItemIcon_Normal)
                self.SetItemImage(child, self.memidx, which = wxTreeItemIcon_Expanded)
            else:
                self.SetItemImage(child, self.diskidx, which = wxTreeItemIcon_Normal)
                self.SetItemImage(child, self.diskidx, which = wxTreeItemIcon_Expanded)
        else:
            self.SetItemImage(child, self.fldridx, which = wxTreeItemIcon_Normal)
            self.SetItemImage(child, self.fldridx, which = wxTreeItemIcon_Expanded)

        return child

    def AddItemIndex(self, handle, wx_id):
        self._item_to_id[handle] = wx_id

    def get_item_by_name(self, name):
        return self._item_to_id[name]

    def OnSelChanged(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)
        self.GetParent().GetParent().action_menu.set_actions(item.get_actions())

    def OnKeyDown(self, evt):
        if evt.GetKeyCode() == WXK_F2 and self.GetParent().is_rename_ok():
            id = self.GetSelection()
            item = self.GetPyData(id)
            self.EditLabel(id)
            return
        elif evt.GetKeyCode() == WXK_DELETE:
            id = self.GetSelection()
            item = self.GetPyData(id)
            if not evt.GetKeyEvent().ShiftDown():
                dialog = wxMessageDialog(self, "Are you sure to delete %s" %item.get_name(),"Delete", wxYES_NO)
                if dialog.ShowModal() == wxID_YES:
                    if hasattr(item, "delete"):
                        item.delete()
                        self.Delete(id)
                dialog.Destroy()
                return
        else:
            # event skip should be the only statement
            evt.Skip()

    def OnItemExpanding(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)

        print "OnItemExpanding %s %s" % (id, repr(item.get_name()))
        for item in item.get_children():
            if item.get_handle() not in self._item_to_id:
                self.AppendAksyItem(id, item)

    def OnItemActivate(self, evt):
        # TODO: hookup the edit views here
        id = evt.GetItem()
        item = self.GetPyData(id)

class TreePanel(wxPanel):
    def __init__(self, parent):

        # the default implementation seems to be in-memory
        if wxPlatform == "__WXGTK__":
            self.config = wxFileConfig("Aksy", style=wxCONFIG_USE_LOCAL_FILE)
        else:
            self.config = wxConfig("Aksy")
        self.lastdir = self.config.Read("/LastRun/Lastdir")
        print "Config object" , repr(self.lastdir)
        if self.lastdir is '':
            self.lastdir = os.path.expanduser("~")
        if len(self.lastdir) == 1:
            self.lastdir = ""

        wxPanel.__init__(self, parent, ID_MAIN_PANEL)
        self.sampler = parent.sampler
        EVT_SIZE(self, self.OnSize)

        self.tree = AksyFSTree(self, wxNewId(), style=wxTR_EDIT_LABELS|wxTR_HIDE_ROOT|wxTR_DEFAULT_STYLE|wxTR_MULTIPLE)
        self.actions = {}
        self._action_item = None
        self._action = None
        self.recordedActions = []
        self.register_menu_actions(model.File.actions)

        for action in ( model.Action('cut','Cut\tCtrl+X', wxID_CUT),
                        model.Action('copy','Copy\tCtrl+C', wxID_COPY),
                        model.Action('save','Paste\tCtrl+V', wxID_PASTE)):
            model.File.actions.append(action)
            self.register_menu_action(action)

        EVT_MENU(parent, wxID_CUT, self.OnCut)   
        EVT_MENU(parent, wxID_COPY, self.OnCopy)   
        EVT_MENU(parent, wxID_PASTE, self.OnPaste)   
        EVT_CLOSE(self, self.store_config)   

        EVT_TREE_BEGIN_LABEL_EDIT(self, self.tree.GetId(), self.CheckRenameAction)
        EVT_TREE_END_LABEL_EDIT(self, self.tree.GetId(), self.RenameAction)
        EVT_RIGHT_UP(self.tree.GetMainWindow(), self.contextMenu)

        # replace by get_system_objects
        disks = self.sampler.disks
        mem = self.sampler.memory

        storage = [disks, mem]

        mem_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), mem)
        disks_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), disks)

        self.tree.Expand(self.tree.root)

    def store_config(self):
        print "store_config"
        self.config.Write("/LastRun/Lastdir", self.lastdir)
        self.config.Flush()

    """Copy and paste operations.
    2 types: 
        -copy/paste aksy items in the tree
        -copy/paste filenames between aksy 
    """
    def OnCopy(self, evt):
        # this is always a node to be copied.
        id = self.tree.GetSelection()

        item = self.tree.GetPyData(id)
        assert hasattr(item, "copy")
        self.prepare_edit_action(item, 'copy')

    def undo_action(self):
        """XXX: make generic by adding it to the action class
        """
        item = self._item
        id = self.tree.get_item_by_name(item)
        if self._action == "cut":
            # XXX: retain position within leaf
            self.tree.AppendAksyItem(self.Tree.GetItemParent(id), item)
        self._action_item = None
        self._action = None

    def prepare_edit_action(self, item, action):
        self._action_item = item
        self._action = action
    
    def complete_edit_action(self, dest_id, dest_item):
        if self._action is None or self._action_item is None:
            return False
        
        new_item = self._action_item.copy(dest_item.path)
        self.tree.AppendAksyItem(dest_id, new_item)

        if self._action == "cut":
            self._action_item.delete()

    def OnCut(self, evt):
        # this is always a node
        # hide it
        id = self.tree.GetSelection()
        item = self.tree.GetPyData(id)
        self.prepare_edit_action(item, 'cut')
        # XXX: check if this removes the pyData as well
        self.tree.Delete(id)
        
    def OnPaste(self, evt):
        dest_id = self.tree.GetSelection()
        dest_item = self.tree.GetPyData(dest_id)
        # internal copy/paste
        if not self.complete_edit_action(dest_id, dest_item):
            if wxTheClipboard.Open():
                # assume a path is pasted
                data = wxTextDataObject()
                if wxTheClipboard.GetData(data):
                    print "Clipboard data ", repr(data.GetText())
                    data = wxFileDataObject()
                elif wxTheClipboard.GetData(data):
                     print "Clipboard data ", repr(data.GetFilenames())
                wxTheClipboard.Close()

    def register_menu_actions(self, actions):

        # hook into actions
        for action in actions:
            if action.function_name == 'transfer':
                action.display_name +=  '\tCtrl+T'
                action.prolog = self.select_directory
                file_transfer_action = copy.copy(action)
                file_transfer_action.prolog = self.select_file
                self.register_menu_action(file_transfer_action)
            elif action.function_name == 'load':
                action.display_name +=  '\tCtrl+L'
                # should be a notification of some sort
                action.epilog = self.add_to_memory_branch

            if action.function_name == 'delete':
                action.display_name +=  '\tCtrl+D'
                inmem_file_delete = copy.copy(action)
                inmem_file_delete.epilog = self.remove_from_memory_branch
                self.register_menu_action(inmem_file_delete)

            self.register_menu_action(action)

    def register_menu_action(self, action):
        if action.id is None:
            id = wxNewId()
            action.id = id
        else:
            id = action.id
        self.actions[id] = action
        EVT_MENU(self, id, self.ExecuteAction)
        EVT_MENU(self.GetParent(), id, self.ExecuteAction)   

    def RenameAction(self, evt):
        new_name = evt.GetLabel()
        # TODO: implement decent checks
        if len(new_name) == 0:
            evt.Veto()
        
        id = self.tree.GetSelection()
        item = self.tree.GetPyData(id)
        item.rename(new_name)

    def CheckRenameAction(self, evt):
        """Handles begin label edit
        """
        if not self.is_rename_ok():
            evt.Veto()

    def is_rename_ok(self):
        id = self.tree.GetSelection()
        item = self.tree.GetPyData(id)
        if hasattr(item, 'rename'):
            return True

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
            result = getattr(item, action.function_name)()
        elif len(args) == 1:
            result = getattr(item, action.function_name)(args[0])
        else:
            result = getattr(item, action.function_name)(args)

        if action.epilog is not None:
            if result is None:
                action.epilog(item)
            else:
                action.epilog(item, result)

        self.recordedActions.append((action, args,))

    def select_directory(self, item):
        dir_dialog = wxDirDialog(self, "Choose a destination for %s" %item.get_name(), 
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
        filedialog = wxFileDialog(self, "Choose a destination for %s" %item.get_name(), 
            style=wxDD_DEFAULT_STYLE)
        filedialog.SetDirectory(self.lastdir)
        filedialog.SetFilename(item.get_name())
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
        action_menu = self.GetParent().action_menu

        self.PopupMenu(action_menu, e.GetPosition())

    def add_to_memory_branch(self, item, result):
        """Updates the memory branch when an item has been loaded
        Should be factored out
        """
        memory_folder = self.tree.get_item_by_name('memory')
        if not isinstance(result, list):
            self.tree.AppendAksyItem(memory_folder, result)
        else:
            for item in result:
                self.tree.AppendAksyItem(memory_folder, item)

        self.tree.Expand(memory_folder)

    def remove_from_memory_branch(self, item):
        memory_folder = self.tree.get_item_by_name('memory')
        self.tree.Delete(item.id)

    def OnSize(self, e):
        self.tree.SetSize(self.GetSize())

class ActionMenu(wxMenu):
    def __init__(self, parent, style):
         wxMenu.__init__(self)

    def set_actions(self, actions):
        for item in self.GetMenuItems():
            self.Remove(item.GetId())
        for index, action in enumerate(actions):
            self.Append(action.id, action.display_name, action.display_name)
         
class AksyFileDropTarget(wxFileDropTarget):
    def __init__(self, window):
        wxFileDropTarget.__init__(self)
        self.tree = window
                                                                                                                                                            
    def OnDropFiles(self, x, y, filenames):
        id, flag1, flag2 = self.tree.HitTest((x,y))
        print repr(id)
        item = self.tree.GetPyData(id)
        if item is None or not hasattr(item, "append_child"): 
            return

        sys.stderr.writelines("\n%d file(s) dropped on %s:\n" % (len(filenames), item.get_name()))
        # start upload
        for file in filenames:
            item.append_child(file, 'file_element_of_path')

        # append items

if __name__ == '__main__':
    app = wxPySimpleApp()
    frame = Frame(None, "Aksy")
    win = TreePanel(frame)
    app.MainLoop()
