import wx

from aksy import model
from aksyx import USBException
from aksy.device import Device, Devices
import os.path, traceback, sys, copy

ID_ABOUT=wx.NewId()
ID_EXIT=wx.NewId()
ID_TREE_PANEL = wx.NewId()
ID_TREE_CTL = wx.NewId()

class Frame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = ( 200,100),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        filemenu= wx.Menu()
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q"," Terminate the program")

        helpmenu = wx.Menu()
        helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.SetSize((800, 600))
        img_path = os.path.join(os.path.split(__file__)[0], 'img')
        self.SetIcon(wx.IconFromBitmap(wx.Image(os.path.join(img_path, 'aksy.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()))
        self.Show(True)

        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        try:
            self.sampler = Devices.get_instance('z48', 'usb', debug=0)
        except USBException, e:
		    # if e[0] == "No sampler found":
            self.sampler = Devices.get_instance('mock_z48', debug=1)
            # self.reportException(e)

        splitter = wx.SplitterWindow(self, size=wx.DefaultSize,style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(100)
        ilist = wx.ImageList(16, 16)
        icon_map = create_icons(ilist)
        panel = TreePanel(splitter, ilist, icon_map)

        listpanel = ListPanel(splitter, ilist, icon_map)
        splitter.SetSize(self.GetSize())

        self.Bind(wx.EVT_TREE_SEL_CHANGED, listpanel.OnTreeSelChanged, panel.tree)

        splitter.SplitVertically(panel, listpanel)
        
    def OnAbout(self,e):
        d= wx.MessageDialog(self, " Aksy, fresh action for your sampler\n", "About Aksy", wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExitMenu(self,e):
        self.on_exit()
        self.Close(True)

    def OnExit(self,e):
        self.on_exit()
        self.Destroy()

    def on_exit(self):
        self.FindWindowById(ID_TREE_PANEL).store_config()

    def reportException(self, exception):
        traceback.print_exc()
        d= wx.MessageDialog( self, "%s\n" % exception[0], "An error occurred", wxOK)
        d.ShowModal()
        d.Destroy()

def create_icons(ilist):
    img_path = os.path.join(os.path.split(__file__)[0], 'img')
    return {
        "file": ilist.Add(wx.ArtProvider_GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, (16,16))),
        "disk": ilist.Add(wx.Image(os.path.join(img_path, 'harddisk.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        "memory": ilist.Add(wx.Image(os.path.join(img_path, 'memory.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.File.FOLDER: ilist.Add(wx.Image(os.path.join(img_path, 'folder.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        "%i%s" %(model.File.FOLDER, "-open"): ilist.Add(wx.Image(os.path.join(img_path, 'folder-open.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.File.PROGRAM: ilist.Add(wx.Image(os.path.join(img_path, 'program.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.File.MULTI: ilist.Add(wx.Image(os.path.join(img_path, 'multi.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.File.SAMPLE: ilist.Add(wx.Image(os.path.join(img_path, 'sample.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
    }
    
class AksyFSTree(wx.TreeCtrl):
    def __init__(self, parent, ilist, icon_map, **kwargs):
        wx.TreeCtrl.__init__(self, parent, ID_TREE_CTL, **kwargs)
        target = AksyFileDropTarget(self)
        self.SetDropTarget(target)
        self.SetImageList(ilist)
        self.ilist = ilist # it seems we need to take ownership of the list
        self.root = self.AddRoot("Sampler")
        self.icon_map = icon_map
        self._item_to_id = {}

        self.Bind(wx.EVT_TREE_DELETE_ITEM, self.OnItemDelete, self)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, self)
        # self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate, self)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnItemBeginDrag, self)
        self.Bind(wx.EVT_TREE_END_DRAG, self.OnItemEndDrag, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self)
        self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnKeyDown, self)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.CheckRenameAction)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.RenameAction)
        self.Bind(wx.EVT_RIGHT_UP, self.contextMenu)

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
        if isinstance(item, model.Folder):
            print "Copy"
            self.AppendAksyItem(dest, self.draggedItem)
        elif isinstance(item, model.Memory):
            print "Load"
            self.draggedItem.load()
        else:    
            print "Unsupported drop target"
            evt.Veto()
            return
        
    def AppendAksyItem(self, parent, item):

        """Appends an item to the tree. default is root
        """
        if parent is None:
            parent = self.root

        print "AppendAksyItem: name: %s, children: %s" % (item.get_name(), repr(item.get_children()))
        child = self.AppendItem(parent, item.get_name())
        if item.has_children():
            self.SetItemHasChildren(child)
        item.id = child
        self.SetPyData(child, item)
 
        if isinstance(item, model.File):
            if item.type == model.File.FOLDER:
                self.SetItemImage(child, self.icon_map["%i%s" %(model.File.FOLDER, "-open")], which = wx.TreeItemIcon_Expanded)
            self.SetItemImage(child, self.icon_map[item.type], which = wx.TreeItemIcon_Normal)
        elif isinstance(item, model.Memory):
            self.SetItemImage(child, self.icon_map['memory'], which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.icon_map['memory'], which = wx.TreeItemIcon_Expanded)
        elif isinstance(item, model.Disk):
            self.SetItemImage(child, self.icon_map['disk'], which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.icon_map['disk'], which = wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(child, self.icon_map['file'], which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.icon_map['file'], which = wx.TreeItemIcon_Expanded)

        return child

    def OnSelChanged(self, evt):
        ids = self.GetSelections()
        if len(ids) > 0:
            item = self.GetPyData(ids[-1])
        print "TREE SEL CHANGED", ids
        evt.Skip()
        
    def OnKeyDown(self, evt):
        ids = self.GetSelections()
        for id in ids: 
            item = self.GetPyData(id)
            if evt.GetKeyCode() == wx.WXK_F2:
                if hasattr(item, 'rename'):
                    self.EditLabel(id)
            elif evt.GetKeyCode() == wx.WXK_DELETE:
                if not hasattr(item, "delete"):
                    continue
                if not evt.GetKeyEvent().ShiftDown():
                    dialog = wx.MessageDialog(self,
                      "Delete %s?" %item.get_name(),"Delete", wx.YES_NO)
                    if dialog.ShowModal() == wx.ID_YES:
                        item.delete()
                        self.Delete(id)
                    dialog.Destroy()
                    continue
            else:
                # event skip should be the only statement
                evt.Skip()

    def OnItemDelete(self, evt):
        """Make sure tree is updated
        """
        #tree_parent = self.GetItemParent(evt.GetItem())
        #parent = self.GetPyData(tree_parent)
        #self.SetItemHasChildren(tree_parent, parent.has_children())
        print repr(evt)
        
    def OnItemExpanding(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)
        print "OnItemExpanding %s %s, %s" % (id, item.get_name(), repr(item.get_children()))
        for child in item.get_children():
            if not hasattr(child, 'id'):
                self.AppendAksyItem(id, child)

    def OnItemActivate(self, evt):
        #evt.Skip()
        # TODO: hookup the edit views here
        # id = evt.GetItem()
        # item = self.GetPyData(id)
        pass

    def RenameAction(self, evt):
        new_name = evt.GetLabel()
        # TODO: implement decent checks
        if len(new_name) == 0:
            evt.Veto()

        ids = self.GetSelections()
        item = self.GetPyData(ids[-1])
        item.rename(str(new_name))

    def CheckRenameAction(self, evt):
        """Handles begin label edit
        """
        ids = self.GetSelections()
        for id in ids:
            item = self.GetPyData(id)
            if not hasattr(item, 'rename'):
                evt.Veto()

    def contextMenu(self, e):
        ids = self.GetSelections()
        actions = set()
        for id in ids: 
            item = self.GetPyData(id)
            if len(actions) == 0:
                actions.update(item.get_actions())
            else:
                actions.intersection(item.get_actions())
        menu = ActionMenu(self, wx.SIMPLE_BORDER)
        menu.set_actions(actions)
        self.PopupMenu(menu, e.GetPosition())
    
class ListPanel(wx.Panel):
    def __init__(self, parent, ilist, icon_map):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_SIZE, self.OnSize)    
        self.listctl = wx.ListCtrl(self)
        self.icon_map = icon_map
        self.listctl.SetImageList(ilist,0)
        img_path = os.path.join(os.path.split(__file__)[0], 'img')
        self.diskidx = ilist.Add(wx.Image(os.path.join(img_path, 'harddisk.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        
    def OnSize(self, evt):
        self.listctl.SetSize(self.GetSize())
    
    def OnTreeSelChanged(self, evt):
        id = evt.GetItem()
        if not id.IsOk(): return
        # TODO: make this less incestuous
        item = self.GetParent().FindWindowById(ID_TREE_CTL).GetPyData(id)
        self.listctl.ClearAll()
        if not item.has_children(): return
        
        for index, child in enumerate(item.get_children()):
            list_item = wx.ListItem()
            list_item.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            list_item.m_text = child.get_name()
            list_item.m_image = self.icon_map[child.type]
            list_item.m_width = 50
            self.listctl.InsertItem(list_item)

class TreePanel(wx.Panel):
    def __init__(self, parent, ilist, icon_map):
        wx.Panel.__init__(self, parent, ID_TREE_PANEL)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # the default implementation seems to be in-memory
        if wx.Platform == "__WXGTK__":
            self.config = wx.FileConfig("Aksy", style=wx.CONFIG_USE_LOCAL_FILE)
        else:
            self.config = wx.Config("Aksy")
        self.lastdir = self.config.Read("/LastRun/Lastdir")
        print "Config object" , repr(self.lastdir)
        if self.lastdir is '':
            self.lastdir = os.path.expanduser("~")
        if len(self.lastdir) == 1:
            self.lastdir = ""

        self.sampler = parent.GetParent().sampler
        self.tree = AksyFSTree(self, ilist, icon_map, style=wx.TR_EDIT_LABELS|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE)
        self.actions = {}
        self._action_item = None
        self._action = None
        self.recordedActions = []
        self.register_menu_actions(model.File.actions)
        self.register_menu_actions(model.InMemoryFile.actions)

        for action in ( model.Action('cut','Cut\tCtrl+X', wx.ID_CUT),
                        model.Action('copy','Copy\tCtrl+C', wx.ID_COPY),
                        model.Action('save','Paste\tCtrl+V', wx.ID_PASTE)):
            model.File.actions.append(action)
            self.register_menu_action(action)

        wx.EVT_MENU(parent, wx.ID_CUT, self.OnCut)
        wx.EVT_MENU(parent, wx.ID_COPY, self.OnCopy)
        wx.EVT_MENU(parent, wx.ID_PASTE, self.OnPaste)
        wx.EVT_CLOSE(self, self.store_config)

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

    def ExecuteAction(self, evt):
        action = self.actions[evt.GetId()]

        ids = self.tree.GetSelections()
        for id in ids:
            self.handle_action(id, action)
            
    def handle_action(self, id, action):
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
            style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
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

    def add_to_memory_branch(self, item, result):
        """Updates the memory branch when an item has been loaded
        Should be factored out
        """
        memory_folder = self.tree.GetFirstVisibleItem()
        if not isinstance(result, list):
            self.tree.AppendAksyItem(memory_folder, result)
        else:
            for item in result:
                self.tree.AppendAksyItem(memory_folder, item)

        self.tree.Expand(memory_folder)

    def remove_from_memory_branch(self, item):
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
    def __init__(self, tree):
        wx.FileDropTarget.__init__(self)
        self.tree = tree

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
