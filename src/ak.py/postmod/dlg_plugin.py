#!/bin/env python
#----------------------------------------------------------------------------
# Name:         dlg_plugin.py
# Author:       XXXX
# Created:      XX/XX/XX
# Copyright:    
#----------------------------------------------------------------------------

import wx
from postmod_wdr import *

import pluginhandler
import wxx

from options import *


# WDR: classes

class PluginDialog(wxx.DialogX):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE,
        plugin=0, infile="", outfile="", preview=0):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        PluginDialogFunc( self, true )

        self.plugin = plugin    # the plugin index to the loaded plugin list
        self.infile = infile    # input filename
        self.outfile = outfile  # output filename
        self.preview = preview  # order for preview
        
        # WDR: handler declarations for PluginDialog
        wx.EVT_BUTTON(self, wx.ID_OK, self.OnOk)

    # WDR: methods for PluginDialog

    # WDR: handler implementations for PluginDialog

    def OnOk(self, event):
        pass



