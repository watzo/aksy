# wxWindows extension classes

import wx
import os, random

import pathmemory

# data storage for auto-stored dialog values
DataStorage = {}

APP = None

def Yield():
    global APP
    if APP:
        APP.Yield(1)
    else:
        APP = wx.GetApp()
        if APP:
            APP.Yield(1)

def PleaseWaitFunc(msg, func, args=(), kwargs={}):
    #disabler = wxWindowDisabler()
    waitcursor = wx.BusyCursor()
    wait = wx.BusyInfo(msg)
    wx.GetApp().Yield(1)
    try:
        func(*args, **kwargs)
    finally:
        del wait
        del waitcursor
        #del disabler

def SelectPath(frame, default = "", pathtype="default"):
    # was options.DefaultPath
    if pathtype and not default:
        default = pathmemory.get(pathtype)

    if not default:
        default = ""
    dirdiag = wx.DirDialog(frame, "Choose a directory", defaultPath = default, style=wx.DD_NEW_DIR_BUTTON )
    if dirdiag.ShowModal() == wx.ID_OK:
        path = dirdiag.GetPath()
    else:
        path = None
    dirdiag.Destroy()

    if path and pathtype:
        pathmemory.set(pathtype, path)
    return path

def SelectFile(frame, defaultDir = "", defaultFile="", ext="*.*", saving=1, multi=0, pathtype="default", mustexist=1, doubleMemory=1):
    # if doubleMemory is true, different path memory is used for saving and loading.
    # the pathmemory codes used are 'code'-load and 'code'-save.

    if doubleMemory:
        if saving:
            pathtype2 = pathtype + '-save'
        else:
            pathtype2 = pathtype + '-load'

        if not pathmemory.get(pathtype2):
            pathmemory.set(pathtype2, pathmemory.get(pathtype))
        pathtype = pathtype2


    if pathtype and not defaultDir:
        defaultDir = pathmemory.get(pathtype)
        #print "got", defaultDir, pathtype
    else:
        #print "using", defaultDir
        pass

    if defaultDir == None:
        defaultDir = ""

    if saving:
        flag = wx.SAVE
    else:
        flag = wx.OPEN

    if multi:
        flag = flag | wx.MULTIPLE

    if mustexist:
        flag = flag | wx.FILE_MUST_EXIST

    selecting = 1
    while selecting:

        dlg = wx.FileDialog(frame, "Choose a filename", defaultDir, defaultFile, ext, flag)
        #dlg.SetDimensions(-1, -1, 1000, 1000)
        #dlg.Refresh()

        if dlg.ShowModal() == wx.ID_OK:
            if multi:
                path = dlg.GetPaths()
            else:
                path = dlg.GetPath()
        else:
            path = None

        selecting = 0
        if path and mustexist and not saving:
            if not multi:
                if not os.path.exists(path):
                    selecting = 1
            else:
                if not os.path.exists(path[0]):
                    selecting = 1
            
        dlg.Destroy()

    if path and pathtype:
        if multi:
            pathmemory.set(pathtype, path[0])
        else:
            pathmemory.set(pathtype, path)
    
    return path


class DialogX(wx.Dialog):
    def GetControlData(self):
        """ returns dict of control data based on names assigned to the controls"""
        children = self.GetChildren()
        data = {}
        for child in children:
            if str(child.__class__.__name__) in ["Choice","ComboBox","RadioBox"]:
                #print "get selection", child.GetName(), child.GetSelection(), type(child.GetSelection()) == int
                data[child.GetName()] = child.GetSelection()
            elif hasattr(child, "GetValue"):
                data[child.GetName()] = child.GetValue()
            else:
                data[child.GetName()] = child.GetLabel()
        #print ".gcd", data
        return data            

    def SetControlData(self, data, exclude=[]):
        """ assigns data to all child controls from a keyword dict.
        returns list of the names that were successfully set."""
        children = self.GetChildren()
        setvars = []
        for child in children:
            childname = child.GetName()
            if childname and data.has_key(childname) and childname not in exclude:
                #print ". setting", child.__class__.__name__, childname, data[childname]
                if str(child.__class__.__name__) in ["Choice","ComboBox","RadioBox"]:
                    #print "CHOICE"
                    child.SetSelection(data[childname])
                    #print "Got", child.GetSelection()
                elif hasattr(child, "SetValue"):
                    child.SetValue(data[childname])
                else:
                    child.SetLabel(str(data[childname]))
                setvars.append(childname)
            else:
                pass
        return setvars

    def GetControl(self, controlname):
        """get a control by name"""
        children = self.GetChildren()
        for child in children:
            if child.GetName() == controlname:
                return child
        return ""
        

    def GetControlLabel(self, controlname):
        """get label of a child control by name"""
        # get child by name
        children = self.GetChildren()
        for child in children:
            if child.GetName() == controlname:
                return child.GetLabel()
        return ""

    def GetControlValue(self, controlname):
        """get value of a child control by name"""
        # get child by name
        children = self.GetChildren()
        for child in children:
            if child.GetName() == controlname:
                return child.GetValue()
        return ""


    def SetControlLabel(self, controlname, newlabel):
        """set label of a child control by name"""
        # get child by name
        children = self.GetChildren()
        thechild = None
        for child in children:
            if child.GetName() == controlname:
                thechild = child
                break
        if thechild:
            thechild.SetLabel(newlabel)
            return 1
        else:
            return 0

    def StoreSettings(self, identifier=None):
        """store labels and values in module scope storage to be restored later"""
        if not identifier:
            identifier = str(self.__class__)
        data = self.GetControlData()
        DataStorage[identifier] = data
        #print "stored to", identifier

    def RestoreSettings(self, identifier=None, exclude=[]):
        exclude = ["staticText", "staticLine", "message", "groupBox"] + exclude
        if not identifier:
            identifier = str(self.__class__)
        data = DataStorage[identifier]
        #print "Restoring", identifier, data
        self.SetControlData(data, exclude=exclude)        



wxDialogX = DialogX


from wxListCtrlMixin import wxListCtrlAutoWidthMixin

class wxListControl(wx.ListCtrl, wxListCtrlAutoWidthMixin):
    """extension wxListCtrl class."""

    def __init__(self, *args, **kwargs):
        #args = list(args)
        #args[4] = args[4] | wxVSCROLL
        #args = tuple(args)
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.ActivateListMode()
        wxListCtrlAutoWidthMixin.__init__(self)

        tID = self.GetId()
        wx.EVT_LIST_KEY_DOWN(self, tID, self.OnKeyDown)
        wx.EVT_LIST_COL_CLICK(self, tID, self.OnColumnClick)
        #EVT_LIST_ITEM_SELECTED(self, tID, self.OnItemSelected)
        #EVT_LIST_ITEM_ACTIVATED(self, tID, self.OnItemActivated)

    def ActivateListMode(self, width=200):
        # activates maximum wxListBox compatibility

        # make one column for the list        
        self.InsertColumn(0, "List")
        #self.SetColumnWidth(0, width)

    def Clear(self):
        # listbox compatibility
        self.DeleteAllItems()

    def ColumnSorter(self, key1, key2):
        item1 = key1
        item2 = key2
        if item1 == item2:  return 0
        elif item1 < item2: return -1
        else:               return 1

    def OnColumnClick(self, event):
        #print "column click list"
        #print "event", event.GetColumn()
        self.SortItems(self.ColumnSorter)


    def OnKeyDown(self, event):
        #print "event", event.GetCode(), event.GetData(), event.GetText(), event.GetString()
        if event.GetCode() == 324:   # insert key
            selected = self.GetSelection()
            if selected == []:
                selected = [0]
            self.InsertStringItem(selected[0], str(random.randrange(10,80)) + "at " + str(event.GetIndex()))
        if event.GetCode() == 127:   # delete key
            selected = self.GetSelection()
            while len(selected) > 0:
                self.DeleteItem(selected[0])
                selected = self.GetSelection()
                            

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        #print "activated:", event.m_itemIndex
            
        
    def NumColumns(self):
        #TODO: NOT WORKING
        done = 0
        numCols = 0
        while not done:
            item = wx.ListItem()
            self.GetColumn(numCols, item)
            txt = item.GetText()
            #print "txt", txt
            if txt != "" and numCols < 20:
                #print "added"
                numCols = numCols + 1
            else:
                done = 1
        return numCols

    def GetSelection(self):
        selected = []
        count = self.GetItemCount()
        for x in xrange(0, count):
            item = self.GetItem(x)
            if (item.m_state & wx.LIST_STATE_SELECTED):
                selected.append(x)
        return selected
                
    GetSelections = GetSelection

    def Deselect(self, index):
        #item = self.GetItem(index)
        #self.SetItemState(index, wxLIST_STATE_DONTCARE, wxLIST_MASK_STATE)
        self.SetItemState(index, 0, wx.LIST_MASK_STATE)

    def SetItemColor(self, index, color):
        item = self.GetItem(index)
        item.SetTextColour(color)
        self.SetItem(item)

    def GetString(self, index):
        return self.GetItemText(index)

    def GetRow(self, index):
        """return list of wxListItems for the specified row"""
        itemlist = []
        for x in xrange(0, self._numColumns):
            item = self.GetItem(index, x)
            itemlist.append(item)
        return itemlist        
        
    def GetRowData(self, index):
        """returns list of column text values for the specified row"""
        itemlist = []
        for x in xrange(0, self._numColumns):
            item = self.GetItem(index, x).GetText()
            itemlist.append(item)
        return itemlist

    def GetRowLength(self, rowIndex):
        row = self.GetRowData(rowIndex)
        itemLengths = map(len, row)
        combinedLength = reduce(lambda x, y: x+y, itemLengths)
        return combinedLength

    def GetMaxRowLength(self):
        """returns the maximum string length of the list's rows.  all fields lengths are added together."""
        count = self.GetItemCount()
        maxl = 0
        for x in xrange(0, count):
            row = self.GetRowData(x)
            itemLengths = map(len, row)
            combinedLength = reduce(lambda x, y: x+y, itemLengths)
            if combinedLength > maxl:
                maxl = combinedLength
        return maxl

    def AddRow(self, datalist):
        count = self.GetItemCount()
        self.InsertStringItem(count, str(datalist[0]))
        if len(datalist) > 1:
            for x in xrange(1, len(datalist)):
                self.SetStringItem(count, x, str(datalist[x]))

    # for ListBox-like compatibility
    def Append(self, st):
        self.AddRow([st])


def showErrorList(parent, errors, caption='Unknown errors occured while processing the following files.\nThey may be invalid or corrupt.\n', title='Errors Occured'):
    dlg = wx.SingleChoiceDialog(parent, 'Unknown errors occured while processing the following files.\nThey may be invalid or corrupt.\n', 'Errors Occured', \
                               errors, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()             


SBOXCACHE = {}

def updateSelectBox(sbox, values, default=None, cache=0):
    # set select box to list of values, and maintain current selection if possible

    if cache and SBOXCACHE.get(id(sbox), None) == (values, default):
        return
    if cache:
        SBOXCACHE[id(sbox)] = (values, default)
    
    defsel = sbox.GetSelection()
    cursel = sbox.GetStringSelection()

    while sbox.GetCount():
        sbox.Delete(0)

    if not default:
        default = values[0]

    i = 0
    for selst in values:
        sbox.Append(selst)
        if selst == cursel:
            sbox.SetSelection(i)
            # don't tread on me
            defsel = -1     
        elif selst == default:
            # we'll set to defsel if current selection is unavailable in new list
            defsel = i
        i += 1
    if defsel > -1:
        sbox.SetSelection(defsel)
    
