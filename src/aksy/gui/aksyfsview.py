import wx
from wx.gizmos import TreeListCtrl

from aksy import model
from aksyx import USBException
from aksy.device import Device, Devices
import os.path, traceback, sys, copy

ID_ABOUT=wx.NewId()
ID_EXIT=wx.NewId()
ID_MAIN_PANEL = wx.NewId()

class Frame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = ( 200,100),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        filemenu= wx.Menu()
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit\tCtrl+Q"," Terminate the program")

        self.action_menu = ActionMenu(self, wx.SIMPLE_BORDER)
        helpmenu = wx.Menu()
        helpmenu.Append(ID_ABOUT, "&About"," Information about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(self.action_menu,"&Actions")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar)
        self.SetSize((800, 600))
        img_path = test_dir = os.path.join(os.path.split(__file__)[0], 'img')
        self.SetIcon(wx.IconFromBitmap(wx.Image(os.path.join(img_path, 'aksy.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()))

        self.Show(True)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)

        wx.EVT_CLOSE(self, self.OnExit)

        try:
            self.sampler = Devices.get_instance('z48', 'usb', debug=0)
        except USBException, e:
		    # if e[0] == "No sampler found":
            self.sampler = Devices.get_instance('mock_z48', debug=1)
            # self.reportException(e)
        panel = TreePanel(self)
        panel.SetSize(self.GetSize())

    def OnAbout(self,e):
        d= wx.MessageDialog(self, " Aksy, fresh action for your sampler\n", "About Aksy", wxOK)
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

    def set_edit_menu(self, menu):
        self.GetMenuBar().Replace(1, menu, "Actions")

    def reportException(self, exception):
        traceback.print_exc()
        d= wx.MessageDialog( self, "%s\n" % exception[0], "An error occurred", wxOK)
        d.ShowModal()
        d.Destroy()

class AksyFSTree(TreeListCtrl):
    def __init__(self, parent, id, **kwargs):
        TreeListCtrl.__init__(self, parent, id, **kwargs)

        target = AksyFileDropTarget(self)
        self.SetDropTarget(target)

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        # add icons for programs, multis, samples

        # self.fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        #self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        self.fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, isz))

        img_path = test_dir = os.path.join(os.path.split(__file__)[0], 'img')
        self.diskidx = il.Add(wx.Image(os.path.join(img_path, 'harddisk.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.memidx = il.Add(wx.Image(os.path.join(img_path, 'memory.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.fldridx = il.Add(wx.Image(os.path.join(img_path, 'folder.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.fldropenidx = il.Add(wx.Image(os.path.join(img_path, 'folder-open.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())

        #self.program_icon     = il.Add(wx.ArtProvider_GetBitmap(wxART_REPORT_VIEW, wxART_OTHER, isz))
        self.program_icon     = il.Add(wx.Image(os.path.join(img_path, 'program.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.multi_icon     = il.Add(wx.Image(os.path.join(img_path, 'multi.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.sample_icon     = il.Add(wx.Image(os.path.join(img_path, 'sample.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.SetImageList(il)
        self.il = il

        # create some columns
        self.AddColumn("")
        self.AddColumn("Size")
        self.AddColumn("Used by")
        self.AddColumn("Modified")
        # self.SetMainColumn(0)
        #self.SetColumnWidth(0, 450)

        self.root = self.AddRoot("Z48")
        self.SetItemImage(self.root, self.fldridx, which = wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, which = wx.TreeItemIcon_Expanded)
        self._item_to_id = {}

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate, self)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnItemBeginDrag, self)
        self.Bind(wx.EVT_TREE_END_DRAG, self.OnItemEndDrag, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self)
        self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnKeyDown, self)

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
        child = self.AppendItem(parent, item.get_name())
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
                self.SetItemImage(child, self.multi_icon, which = wx.TreeItemIcon_Normal)
            elif item.type == model.File.PROGRAM:
                self.SetItemImage(child, self.program_icon, which = wx.TreeItemIcon_Normal)
            elif item.type == model.File.SAMPLE:
                self.SetItemImage(child, self.sample_icon, which = wx.TreeItemIcon_Normal)
            elif item.type == model.File.FOLDER:
                self.SetItemImage(child, self.fldridx, which = wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, which = wx.TreeItemIcon_Expanded)
            else:
                self.SetItemImage(child, self.fileidx, which = wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fileidx, which = wx.TreeItemIcon_Expanded)
        elif isinstance(item, model.Memory):
            self.SetItemImage(child, self.memidx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.memidx, which = wx.TreeItemIcon_Expanded)
        elif isinstance(item, model.Disk):
            self.SetItemImage(child, self.diskidx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.diskidx, which = wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(child, self.fldridx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldridx, which = wx.TreeItemIcon_Expanded)

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
        if evt.GetKeyCode() == wx.WXK_F2 and self.GetParent().is_rename_ok():
            id = self.GetSelection()
            item = self.GetPyData(id)
            self.EditLabel(id)
            return
        elif evt.GetKeyCode() == wx.WXK_DELETE:
            id = self.GetSelection()
            item = self.GetPyData(id)
            if not evt.GetKeyEvent().ShiftDown():
                dialog = wx.MessageDialog(self,
                  "Delete %s?" %item.get_name(),"Delete", wx.YES_NO)
                if dialog.ShowModal() == wx.ID_YES:
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
        if not item: return
        print "OnItemExpanding %s %s" % (id, repr(item.get_name()))
        for item in item.get_children():
            if item.get_handle() not in self._item_to_id:
                self.AppendAksyItem(id, item)

    def OnItemActivate(self, evt):
        # TODO: hookup the edit views here
        id = evt.GetItem()
        item = self.GetPyData(id)

class TreePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ID_MAIN_PANEL)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # the default implementation seems to be in-memory
        if wx.Platform == "__WXGTK__":
            self.config = wx.FileConfig("Aksy", style=wxCONFIG_USE_LOCAL_FILE)
        else:
            self.config = wx.Config("Aksy")
        self.lastdir = self.config.Read("/LastRun/Lastdir")
        print "Config object" , repr(self.lastdir)
        if self.lastdir is '':
            self.lastdir = os.path.expanduser("~")
        if len(self.lastdir) == 1:
            self.lastdir = ""

        self.sampler = parent.sampler

        self.tree = AksyFSTree(self, wx.NewId(), style=wx.TR_EDIT_LABELS|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE)
        self.tree.SetMainColumn(0)
        self.tree.SetColumnWidth(0, 400)

        self.actions = {}
        self._action_item = None
        self._action = None
        self.recordedActions = []
        self.register_menu_actions(model.File.actions)

        for action in ( model.Action('cut','Cut\tCtrl+X', wx.ID_CUT),
                        model.Action('copy','Copy\tCtrl+C', wx.ID_COPY),
                        model.Action('save','Paste\tCtrl+V', wx.ID_PASTE)):
            model.File.actions.append(action)
            self.register_menu_action(action)

        wx.EVT_MENU(parent, wx.ID_CUT, self.OnCut)
        wx.EVT_MENU(parent, wx.ID_COPY, self.OnCopy)
        wx.EVT_MENU(parent, wx.ID_PASTE, self.OnPaste)
        wx.EVT_CLOSE(self, self.store_config)

        wx.EVT_TREE_BEGIN_LABEL_EDIT(self, self.tree.GetId(), self.CheckRenameAction)
        wx.EVT_TREE_END_LABEL_EDIT(self, self.tree.GetId(), self.RenameAction)
        wx.EVT_RIGHT_UP(self.tree.GetMainWindow(), self.contextMenu)

        # replace by get_system_objects
        mem = self.sampler.memory
        mem_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), mem)
        self.tree.Expand(mem_id)

        for disk in self.sampler.disks.get_children():
            disks_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), disk)
            self.tree.Expand(disks_id)

    def store_config(self):
        print "store_config"
        self.config.Write("/LastRun/Lastdir", self.lastdir)
        self.config.Flush()

    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())

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
            if wx.TheClipboard.Open():
                # assume a path is pasted
                data = wx.TextDataObject()
                if wx.TheClipboard.GetData(data):
                    print "Clipboard data ", repr(data.GetText())
                    data = wx.FileDataObject()
                elif wx.TheClipboard.GetData(data):
                     print "Clipboard data ", repr(data.GetFilenames())
                wx.TheClipboard.Close()

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
            id = wx.NewId()
            action.id = id
        else:
            id = action.id
        self.actions[id] = action
        wx.EVT_MENU(self, id, self.ExecuteAction)
        wx.EVT_MENU(self.GetParent(), id, self.ExecuteAction)

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
        dir_dialog = wx.DirDialog(self, "Choose a destination for %s" %item.get_name(),
            style=wx.DD_DEFAULT_STYLE|wxDD_NEW_DIR_BUTTON)
        dir_dialog.SetPath(self.lastdir)
        if dir_dialog.ShowModal() == wx.ID_OK:
            self.lastdir = dir_dialog.GetPath()
            retval = (self.lastdir,)
        else:
            retval = None

        dir_dialog.Destroy()
        return retval

    def select_file(self, item):
        # TODO: cache this dialog as it is heavy...
        filedialog = wx.FileDialog(self, "Choose a destination for %s" %item.get_name(),
            style=wx.DD_DEFAULT_STYLE)
        filedialog.SetDirectory(self.lastdir)
        filedialog.SetFilename(item.get_name())
        if filedialog.ShowModal() == wx.ID_OK:
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

class ActionMenu(wx.Menu):
    def __init__(self, parent, style):
         wx.Menu.__init__(self)

    def set_actions(self, actions):
        for item in self.GetMenuItems():
            self.Remove(item.GetId())
        for index, action in enumerate(actions):
            self.Append(action.id, action.display_name, action.display_name)

class AksyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
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
            item.upload(file)

        # append items

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame(None, "Aksy")
    app.MainLoop()
