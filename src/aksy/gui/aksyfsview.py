import wx
from wx.lib.mixins import listctrl

from aksy.devices.akai import model
from aksyx import USBException
from aksy.device import Devices
import os.path, traceback, sys, copy

ID_TREE_PANEL = wx.NewId()
ID_TREE_CTRL = wx.NewId()
ID_DIR_PANEL = wx.NewId()
ID_DIR_CTRL = wx.NewId()

MENU_ID_DOWNLOAD = wx.NewId()
MENU_ID_DELETE = wx.NewId()
MENU_ID_UPLOAD = wx.NewId()
MENU_ID_LOAD = wx.NewId()

ACCELERATORS = wx.AcceleratorTable([
    (wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
    (wx.ACCEL_CTRL, ord('D'), MENU_ID_DOWNLOAD),
    (wx.ACCEL_CTRL, ord('U'), MENU_ID_UPLOAD),
    (wx.ACCEL_CTRL, ord('L'), MENU_ID_LOAD),
    (wx.ACCEL_NORMAL, wx.WXK_DELETE, MENU_ID_DELETE)])

class Frame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = ( 200,100),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.action_map = {}
        filemenu= wx.Menu()
        filemenu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q"," Exit the program")

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
            self.sampler = Devices.get_instance('z48', 'osc')
        except USBException as e:
		    # if e[0] == "No sampler found":
            self.sampler = Devices.get_instance('mock_z48', 'mock')
            # self.reportException(e)

        splitter = wx.SplitterWindow(self, size=wx.DefaultSize,style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(100)
        ilist = wx.ImageList(16, 16)
        icon_map = create_icons(ilist)
        self.treepanel = TreePanel(splitter, ilist, icon_map)
        self.listpanel = ListPanel(splitter, ilist, icon_map)
        splitter.SetSize(self.GetSize())

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.listpanel.OnTreeSelChanged, self.treepanel.tree)

        splitter.SplitVertically(self.treepanel, self.listpanel)
        for action in ( MenuAction('cut', wx.ID_CUT),
                        MenuAction('copy', wx.ID_COPY),
                        MenuAction('save', wx.ID_PASTE)):
            self.register_menu_action(action)
        
        self.register_menu_actions(
             [MenuAction(action, id, prolog, epilog) for action, id, prolog, epilog  
              in (('delete', MENU_ID_DELETE, None, MenuAction.execute_refresh),
                  ('download', MENU_ID_DOWNLOAD, MenuAction.select_directory, None), 
                  ('upload', MENU_ID_UPLOAD, MenuAction.select_file, MenuAction.execute_refresh),
                  ('load', MENU_ID_LOAD, None, MenuAction.execute_refresh)
                  ,)
             ])
        self.SetAcceleratorTable(ACCELERATORS)

    def OnAbout(self,e):
        d= wx.MessageDialog(self, " Aksy, fresh action for your sampler\n", "About Aksy", wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExitMenu(self,e):
        Config.get_config().store()
        self.Close(True)

    def OnExit(self,e):
        Config.get_config().store()
        self.Destroy()

    def reportException(self, exception):
        traceback.print_exc()
        d= wx.MessageDialog( self, "%s\n" % exception[0], "An error occurred", wxOK)
        d.ShowModal()
        d.Destroy()
    
    def register_menu_actions(self, actions):
        for action in actions:
            self.register_menu_action(action)

    def get_menu_action(self, callable):
        return self.action_map[callable]
    
    def register_menu_action(self, action):
        print("Register ", action, action.action)
        self.Bind(wx.EVT_MENU, action.execute, id=action.id)
        self.action_map[action.action] = action

def create_icons(ilist):
    img_path = os.path.join(os.path.split(__file__)[0], 'img')
    return {
        "file": ilist.Add(wx.ArtProvider_GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, (16,16))),
        "disk": ilist.Add(wx.Image(os.path.join(img_path, 'harddisk.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        "memory": ilist.Add(wx.Image(os.path.join(img_path, 'memory.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.FileRef.FOLDER: ilist.Add(wx.Image(os.path.join(img_path, 'folder.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        "%i%s" %(model.FileRef.FOLDER, "-open"): ilist.Add(wx.Image(os.path.join(img_path, 'folder-open.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.FileRef.PROGRAM: ilist.Add(wx.Image(os.path.join(img_path, 'program.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.FileRef.MULTI: ilist.Add(wx.Image(os.path.join(img_path, 'multi.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()),
        model.FileRef.SAMPLE: ilist.Add(wx.Image(os.path.join(img_path, 'sample.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())
    }
              
class Config(wx.FileConfig):
    LASTDIR = '/LastRun/Lastdir'

    @staticmethod
    def get_config():
        return Config.config

    def __init__(self):
        wx.FileConfig.__init__(self, "Aksy", style=wx.CONFIG_USE_LOCAL_FILE)

    def store(self):
        self.Flush()    
        
    def get_last_dir(self, key=None):
        if self.lastdir is '':
            return os.path.expanduser("~")
        if len(self.lastdir) == 1:
            return ""
        return self.config.Read("%s/%s" % (Config.LASTDIR, key))
   
    def set_last_dir(self, lastdir, key=None):
        self.Write("%s%s" %(self.LASTDIR, key), lastdir)

Config.config = Config()

class MenuAction(object):
    """Maps aksy model actions to GUI actions
    """
    def __init__(self, action, id, prolog=None, epilog=None):
        self.action = action
        self.id = id
        self.prolog = prolog
        self.epilog = epilog

    def execute_refresh(self, item, *args):
        print("REFRESH")
        item.get_parent().refresh()

    def execute(self, evt):
        self.widget = evt.GetEventObject()
        items = self.widget.get_selections()
        
        for item in items:
            self.execute_action(item)

    def execute_action(self, item):
        if not hasattr(item, self.action):
            return
        print("Action %s, item: %s name: %s" % (self.action, repr(item), item.get_name()))
        print(self.prolog)
        if self.prolog is None:
            args = ()
        else:
            args = self.prolog(self, item)
        print("Executing with args %s " % repr(args))
        if args is None:
            return
        elif len(args) == 0:
            result = getattr(item, self.action)()
        else:
            result = getattr(item, self.action)(args)
        if self.epilog is not None:
            if not result:
                self.epilog(self, item)
            else:
                self.epilog(self, item, result)

    def select_directory(self, item):
        dir_dialog = wx.DirDialog(self.widget.get_window(), "Choose a destination for %s" %item.get_name(),
            style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
        # dir_dialog.SetPath(self.widget.lastdir)
        if dir_dialog.ShowModal() == wx.ID_OK:
            selected = dir_dialog.GetPath()
            Config.get_config().set_last_dir(selected)
            retval = (selected,)
        else:
            retval = None

        dir_dialog.Destroy()
        return retval

    def select_file(self, item):
        # TODO: cache this dialog as it is heavy...
        filedialog = wx.FileDialog(
            self.widget.get_window(), 
            "Choose a destination for %s" %item.get_name(),
            style=wx.DD_DEFAULT_STYLE)
        filedialog.SetDirectory(Config().get_last_dir())
        filedialog.SetFilename(item.get_name())
        if filedialog.ShowModal() == wx.ID_OK:
            path = filedialog.GetPath()
        else:
            path = None

        filedialog.Destroy()
        return (path)
        
class ContextMenuHandler(object):
    def get_window(self):
        return self

    def get_frame(self):
        return self.GetParent().GetParent().GetParent()
        
    def get_selections(self):
        raise NotImplementedError()

    def get_aksy_item(self, id):
        raise NotImplementedError()
        
    def contextMenu(self, e):
        items = self.get_selections()
        actions = set()
        for item in items: 
            if len(actions) == 0:
                actions.update(item.get_actions())
            else:
                actions.intersection(item.get_actions())
        menu = ActionMenu(self, wx.SIMPLE_BORDER)
        mactions = [self.get_frame().get_menu_action(action) for action in actions]
        menu.set_actions(mactions)
        menu.set_items(items)
        self.PopupMenu(menu)
        menu.Destroy()

class AksyFSTree(wx.TreeCtrl, ContextMenuHandler):
    def __init__(self, parent, ilist, icon_map, **kwargs):
        wx.TreeCtrl.__init__(self, parent, ID_TREE_CTRL, **kwargs)
        ContextMenuHandler.__init__(self)
        self.SetDropTarget(CtrlFileDropTarget(self))
        self.AssignImageList(ilist)
        self.root = self.AddRoot("Sampler")
        self.icon_map = icon_map
        self.SetAcceleratorTable(ACCELERATORS)
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
    
    def get_selections(self):
         return [self.get_aksy_item(id) for id in self.GetSelections()]

    def get_aksy_item(self, id):         
         return self.GetPyData(id)
     
    def OnItemBeginDrag(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)
        if isinstance(item, model.FileRef):
            self.draggedItem = item
            print("BeginDrag ", self.draggedItem.get_name())
            evt.Allow()

    def OnItemEndDrag(self, evt):
        dest = evt.GetItem()
        item = self.GetPyData(dest)
        print("EndDrag %s, Mod: %s" % (repr(item), repr(evt.GetKeyCode())))
        if isinstance(item, model.Folder):
            print("Copy")
            self.AppendAksyItem(dest, self.draggedItem)
        elif isinstance(item, model.Memory):
            print("Load")
            self.draggedItem.load()
        else:    
            print("Unsupported drop target")
            evt.Veto()
            return
        
    def AppendAksyItem(self, parent, item):

        """Appends an item to the tree. default is root
        """
        if parent is None:
            parent = self.root

        print("AppendAksyItem: name: %s, children: %s" % (item.get_name(), hasattr(item, 'get_children') and repr(item.get_children()) or 'None'))
        child = self.AppendItem(parent, item.get_short_name())
        if item.has_children():
            self.SetItemHasChildren(child)
        item.id = child
        self.SetPyData(child, item)
        
        #wx.EVT_MENU(self.listpanel, action.id, action.execute)
 
        if isinstance(item, model.FileRef):
            if item.type == model.FileRef.FOLDER:
                self.SetItemImage(child, self.icon_map["%i%s" %(model.FileRef.FOLDER, "-open")], which = wx.TreeItemIcon_Expanded)
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
        print("TREE SEL CHANGED", ids)
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
        print(repr(evt))
        
    def OnItemExpanding(self, evt):
        id = evt.GetItem()
        item = self.GetPyData(id)
        print("OnItemExpanding %s %s, %s" % (id, item.get_name(), repr(item.get_children())))
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

 
    
class ListPanel(wx.Panel):
    def __init__(self, parent, ilist, icon_map):
        wx.Panel.__init__(self, parent, ID_DIR_PANEL)
        self.Bind(wx.EVT_SIZE, self.OnSize)    
        self.listctl = DirListCtrl(self, ilist, icon_map)
        self.icon_map = icon_map
        
    def OnSize(self, evt):
        self.listctl.SetSize(self.GetSize())
    
    def OnTreeSelChanged(self, evt):
        id = evt.GetItem()
        if not id.IsOk(): return
        # TODO: make this less incestuous
        item = self.GetParent().FindWindowById(ID_TREE_CTRL).GetPyData(id)
        self.listctl.set_current(item)

class DirListCtrl(wx.ListCtrl, ContextMenuHandler):
    def __init__(self, parent, ilist, icon_map):
        wx.ListCtrl.__init__(self, parent, ID_DIR_CTRL)
        ContextMenuHandler.__init__(self)
        self.SetAcceleratorTable(ACCELERATORS)
        self.icon_map = icon_map
        self.SetDropTarget(DirListDropTarget(self))
        self.SetImageList(ilist,0)
        self.item = None
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.contextMenu)

    def set_current(self, item):
        self.current_item = item
        self.refresh()
    
    def get_current(self):
        return self.current_item
    
    def refresh(self):
        self.ClearAll()
        self.add_items(self.get_current())
    
    def get_selections(self):
        ids = []
        index = self.GetFirstSelected()
        ids.append(index)
        while 1:
            index = self.GetNextSelected(index)
            if index == -1:
                break
            ids.append(index)
        return [self.get_aksy_item(id) for id in ids]
    
    def get_aksy_item(self, id):
        return self.get_current().get_children()[id]
    
    def blacontextMenu(self, e):
        ids = []
       
        actions = set()
        for id in ids: 
            item = self.get_current().get_children()[id]
            if len(actions) == 0:
                actions.update(item.get_actions())
            else:
                actions.intersection(item.get_actions())
        menu = ActionMenu(self, wx.SIMPLE_BORDER)
        print("ACTIONS ", actions)
        mactions = [self.get_frame().get_menu_action(action.callable) for action in actions]
        menu.set_actions(mactions)
        self.PopupMenu(menu)
        menu.Destroy()
        
    def add_items(self, obj):
        if not hasattr(obj, 'get_children'):
            return
        children = obj.get_children()
        for index in range(len(children)-1, -1, -1):
            child = children[index]
            list_item = wx.ListItem()
            list_item.SetMask(wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT)
            list_item.SetText(child.get_short_name())
            list_item.SetImage(self.icon_map[child.type])
            list_item.SetWidth(50)
            self.InsertItem(list_item)
        
class TreePanel(wx.Panel):
    def __init__(self, parent, ilist, icon_map):
        wx.Panel.__init__(self, parent, ID_TREE_PANEL)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.sampler = parent.GetParent().sampler
        self.tree = AksyFSTree(self, ilist, icon_map, style=wx.TR_EDIT_LABELS|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE)
        wx.EVT_MENU(parent, wx.ID_CUT, self.OnCut)
        wx.EVT_MENU(parent, wx.ID_COPY, self.OnCopy)
        wx.EVT_MENU(parent, wx.ID_PASTE, self.OnPaste)
        wx.EVT_CLOSE(self, Config.get_config().store())

        # replace by get_system_objects
        mem = self.sampler.memory
        mem_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), mem)
        self.tree.SelectItem(mem_id)

        for disk in self.sampler.disks.get_children():
            disks_id = self.tree.AppendAksyItem(self.tree.GetRootItem(), disk)
            self.tree.Expand(disks_id)

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
                    print("Clipboard data ", repr(data.GetText()))
                    data = wx.FileDataObject()
                elif wx.TheClipboard.GetData(data):
                     print("Clipboard data ", repr(data.GetFilenames()))
                wx.TheClipboard.Close()

class ActionMenu(wx.Menu):
    def __init__(self, parent, style):
        self.parent = parent
        wx.Menu.__init__(self, style=style)
    
    def get_window(self):
        return self.parent
    
    def get_selections(self):
        return self.items
    
    def set_items(self, items):
        self.items = items
             
    def set_actions(self, actions):
        for item in self.GetMenuItems():
            self.Remove(item.GetId())
        for index, action in enumerate(actions):
            item = self.Append(action.id, action.action, action.action)
            # self.parent.Bind(wx.EVT_MENU, action.execute, item)
                             
class CtrlFileDropTarget(wx.FileDropTarget):
    def __init__(self, ctrl):
        wx.FileDropTarget.__init__(self)
        self.ctrl = ctrl

    def get_drop_dest(self, id):
        return self.ctrl.GetPyData(id)
        
    def OnDropFiles(self, x, y, filenames):
        id, flag1 = self.ctrl.HitTest((x,y))
        print(repr(id))
        item = self.get_drop_dest(id)
        
        if item is None or not hasattr(item, "append_child"):
            return

        sys.stderr.writelines("\n%d file(s) dropped on %s:\n" % (len(filenames), item.get_name()))
        # start upload
        for file in filenames:
            item.upload(file)

        # append items
class DirListDropTarget(CtrlFileDropTarget):
    def get_drop_dest(self, item):
        return self.ctrl.get_current()
    
    def OnDropFiles(self, x, y, filenames):
        print("FN: ", repr(filenames))
        CtrlFileDropTarget.OnDropFiles(self, x, y, filenames)
        self.ctrl.refresh()
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame(None, "Aksy")
    app.MainLoop()
