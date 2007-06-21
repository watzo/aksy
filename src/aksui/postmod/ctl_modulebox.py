
import wx
import pprint


import wxx

#class ModuleBox(wx.HtmlListBox):
class ModuleBox(wxx.wxListControl):

    def __init__(self, *args, **kwargs):
        args = list(args)
        args[4] = args[4] | wx.LC_REPORT | wx.LC_NO_HEADER | wx.VSCROLL 
        args = tuple(args)
        wxx.wxListControl.__init__(self, *args, **kwargs)
        #wx.EVT_CHAR(self, self.OnChar)
        wx.EVT_MOUSEWHEEL(self, self.OnMouseWheel)
        #wx.EVT_LISTBOX(self, self.GetId(), self.OnListBox)

        #self.ActivateListMode(width=500)

        #self.InsertColumn(0, "stuff")
        #self.SetColumnWidth(0, self.GetSize()[0])


        #self.SetScrollbar(wx.HORIZONTAL, 0, 0, 0)
        #self.ScrollWindow(0,0)
        #self.Layout()
        #self.Refresh()
        
        self.data = []
        self.formats= {}
        self.defaultFormat = "<font face='MS Sans Serif' size=-2>%s</font>"

        #self.selections = []

    def OnListBox(self, event):
        print "selected", event.GetSelection(), event.GetInt(), event.IsChecked(), event.IsSelection(), event.GetExtraLong()

    def GetCount(self):
        return self.GetItemCount()


    def OnMouseWheel(self, event):
        rot = event.m_wheelRotation
        self.ScrollLines(-(rot/abs(rot)))


    def Clear(self):
        self.DeleteAllItems()

    def Append(self, s):
        #self.data.append(s)
        self.InsertStringItem(self.GetItemCount(), s)
        #self.RefreshAll()

    def Select(self, item, select):
        if self.HasMultipleSelection():
            self.Select(item, select)
        else:
            if select:
                self.SetSelection(item)
            else:
                self.Deselect(item)

    def SetString(self, item, s):
        #self.data[item] = s
        #self.RefreshAll()
        self.SetItemText(item, s)

    def Deselect(self, item):
        if item > -1:
            if self.IsSelected(item):
                self.Toggle(item)

    #def Refresh(self):
    #    self.RefreshAll()

    def RefreshAll(self):
        self.Refresh()

    def SetItemForegroundColour(self, index, color):
        item = self.GetItem(index, 0)
        item.SetTextColour(color)
        self.SetItem(item)


    def OnGetItem(self, n):
        if n in self.formats:
            return self.formats[n] % (self.data[n],)
        else:
            return self.defaultFormat % (self.data[n],)
        
        #if n in self.data:
        #    return "<b>%s</b> <font color='red'>C</font><font color='blue'>-</font><font color='green'>5</font><font color='red'>.</font><font color='green'>01..</font><font color='blue'>02</font><font color='red'>..</font><font color='green'>64</font><font color='red'>..</font><font color='blue'>B014</font>" % self.data[n]
        #else:
        #    return "<b>%d</b> <font color='red'>C</font><font color='blue'>-</font><font color='green'>5</font><font color='red'>.</font><font color='green'>01..</font><font color='blue'>02</font><font color='red'>..</font><font color='green'>64</font><font color='red'>..</font><font color='blue'>B014</font>" % n

    def OnChar(self, evt):
        #print "trackbox char for", self.GetSelection()
        n = self.GetSelection()
        print evt.m_keyCode
        self.data[n] = chr(evt.m_keyCode)
        #self.RefreshAll()
        self.RefreshLine(n)
        print "line", self.GetLineCount(), self.GetFirstVisibleLine()
        #self.SetSelection(n)
        
