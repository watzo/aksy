
import wxPython.wx

wxEVT_POSTMOD_NEW_FILEBATCH = wxPython.wx.wxNewEventType()

class NewFileBatchEvent(wxPython.wx.wxPyEvent):
    def __init__(self, title, files, name="Processed"):
        wxPython.wx.wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_POSTMOD_NEW_FILEBATCH)
        self.title = title
        self.files = files
        self.name = name

wxEVT_POSTMOD = wxPython.wx.wxNewEventType()

def EVT_POSTMOD_NEW_FILEBATCH(win, func):
    win.Connect(-1, -1, wxEVT_POSTMOD_NEW_FILEBATCH, func)

##########################################################

class PostmodEvent(wxPython.wx.wxPyEvent):
    def __init__(self, data=None, func=None, args=None, kwargs=None):
        wxPython.wx.wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_POSTMOD)
        self.data = data
        self.func = func
        self.args = args
        self.kwargs = kwargs

def EVT_POSTMOD(win, func):
    win.Connect(-1, -1, wxEVT_POSTMOD, func)

