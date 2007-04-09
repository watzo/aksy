
import wx
import wxx

from postmod_wdr import *

import zlib
import webbrowser
from options import *


URL_REGISTER = ""


class RegistrationDialog(wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        #style = wxDEFAULT_DIALOG_STYLE ):
        style = wx.CAPTION ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        RegistrationDialogFunc( self, True )

        self.element = "dialog" # means registration is not valid

        try:
            x,y,z = self.GetC(), self.GetB(), self.GetA()
            a,b,c = zlib.decompress(options.RK).split("^")
            x.SetLabel(a)
            y.SetLabel(b)
            z.SetLabel(c)
        except:
            pass
        
        # WDR: handler declarations for RegistrationDialog
        wx.EVT_BUTTON(self, ID_BUTTON_CANCEL, self.OnCancel)
        wx.EVT_BUTTON(self, ID_BUTTON_OK, self.OnOK)
        wx.EVT_CLOSE(self, self.OnClose)

    # WDR: methods for RegistrationDialog

    def GetA(self):
        return self.FindWindowById(ID_TEXTCTRL_KEY)

    def GetB(self):
        return self.FindWindowById(ID_TEXTCTRL_EMAIL)

    def GetC(self):
        return self.FindWindowById(ID_TEXTCTRL_NAME)

    # WDR: handler implementations for RegistrationDialog

    def OnCancel(self, event):
        self.Close()
        os._exit(0)
        
    def OnOK(self, event):
        pass

    def OnClose(self, event):
        event.Skip(True)
        if self.element != "label":
            os._exit(0)
        


class BetaExpiredDialog(wx.Dialog):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        BetaExpiredFunc( self, True )
        
        # WDR: handler declarations for BetaExpiredDialog
        wx.EVT_BUTTON(self, ID_BUTTON, self.OnOK)
        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOk)

    # WDR: methods for BetaExpiredDialog

    # WDR: handler implementations for BetaExpiredDialog

    def OnOK(self, event):
        self.Close()

    def OnOk(self, event):
        self.Close()




class DemoExpiredDialog(wx.Dialog):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        DemoExpiredDialogFunc( self, True )
        
        # WDR: handler declarations for BetaExpiredDialog
        wx.EVT_BUTTON(self, ID_BUTTON_REGISTER, self.OnRegister)
        wx.EVT_BUTTON(self, ID_BUTTON_CANCEL, self.OnCancel)
        wx.EVT_BUTTON(self, ID_BUTTON, self.OnOK)

    # WDR: methods for BetaExpiredDialog

    # WDR: handler implementations for BetaExpiredDialog

    def OnOK(self, event):
        self.Close()

    def OnCancel(self, event):
        self.Close()

    def OnRegister(self, event):
        #webbrowser.open_new("http://www.magicfish.net")
        webbrowser.open(URL_REGISTER)
        self.Close()
        
