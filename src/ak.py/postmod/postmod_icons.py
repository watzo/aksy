
import wx
from options import *

redfish = bluefish = itfile = postmod = greenwav = None


def initIcons():
    global redfish, bluefish, itfile, postmod, greenwav
    imagepath = options.getProgramPath() + "\\images"
    
    redfish = wx.Icon(imagepath + '\\icon1.ico', wx.BITMAP_TYPE_ICO)
    #bluefish = wx.Icon('images/icon2.ico', wx.BITMAP_TYPE_ICO)
    #greenfish = wx.Icon('images/icon3.ico', wx.BITMAP_TYPE_ICO)
    bluefish = greenfish = redfish
    itfile = wx.Icon(imagepath + '\\itfile.ico', wx.BITMAP_TYPE_ICO)
    postmod = wx.Icon(imagepath + '\\postmod.ico', wx.BITMAP_TYPE_ICO)
    greenwav = wx.Icon(imagepath + '\\greenwav.ico', wx.BITMAP_TYPE_ICO)

