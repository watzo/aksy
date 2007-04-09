

import wx
from options import *

class wxAudioSlider(wx.Window):

    def __init__(self, parent, id, pos, size, image=options.getImagePath()+"\\slider.bmp", thumbImage=options.getImagePath()+"\\thumb.bmp", min=0, max=100):
        wx.Window.__init__(self, parent, id, pos, size)
        self.value = 0
        self.minValue = min
        self.maxValue = max

        self.dragging = 0

        self.bitmap = wx.Bitmap(image)
        mask = wx.Mask(self.bitmap, wx.WHITE)
        self.bitmap.SetMask(mask)
        
        self.thumbBitmap = wx.Bitmap(thumbImage)
        self.thumbWidth = self.thumbBitmap.GetWidth()
        self.thumbHeight = self.thumbBitmap.GetHeight()

        self.width, self.height = self.GetSizeTuple()

        self.parent = parent

        self.evt = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED, self.GetId())
        self.evt.SetEventObject(self.evt)
        
        wx.EVT_MOUSE_EVENTS(self, self.OnMouseEvent)
        wx.EVT_MOUSEWHEEL(self, self.OnMouseWheel)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SET_FOCUS(self, self.OnFocus)
        
    def get(self):
        return self.value

    def set(self, val):
        if val < self.minValue:
            val = self.minValue
        if val > self.maxValue:
            val = self.maxValue
        self.value = val

        self.Refresh(0)


    GetValue = get
    SetValue = set

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        # thumbPos is in pixels
        #pos = self.value * (self.height - 1 - self.thumbHeight) / (self.maxValue + 1)

        #pos = self.value * (self.height - 1 - (self.thumbHeight-1)) / (self.maxValue)
        pos = self.value * (self.height - (self.thumbHeight)) / (self.maxValue)

        x = (self.width - self.thumbWidth) / 2
        #print "thumb", pos, self.value, self.maxValue

        dc.Clear()
        dc.DrawBitmap(self.bitmap, 0, 0, 1)
        dc.DrawBitmap(self.thumbBitmap, x, pos)

    def OnFocus(self, event):
        # give focus to parent.
        if self.GetParent():
            self.GetParent().SetFocus()

    def OnMouseWheel(self, event):
        rot = event.m_wheelRotation
        if rot > 0:
            self.set(self.get()-(abs(rot/event.m_wheelDelta)))
        else:
            self.set(self.get()+(abs(rot/event.m_wheelDelta)))

        self.evt.SetInt(self.GetValue())
        self.GetEventHandler().ProcessEvent(self.evt)


    def OnMouseEventOld(self, event):
        if event.ButtonDown():
            # jump slider to clicked position

            if not self.dragging:
                temp = self.height - 1 - self.thumbHeight
                # go to event.m_x - thumbwidth/2, but not less than 0 or greater than
                # width - thumbwidth
                newpos = event.m_y - self.thumbHeight / 2
                if newpos < 0:
                    newpos = 0
                elif newpos > (temp):
                    newpos = temp

                # where is it now?
                curpos = self.value * (temp) / (self.maxValue + 1)

                # only move it if we aren't already clicking on it
                if (newpos < curpos) or (newpos > (curpos + self.thumbHeight)):
                    curpos = newpos

                    # set new value
                    self.value = curpos * (self.maxValue + 1) / (temp)
                    self.Refresh(0)

                    self.evt.SetInt(self.GetValue())
                    self.GetEventHandler().ProcessEvent(self.evt)

                self.dragging = 1
                self.CaptureMouse()

        elif event.ButtonUp() and self.dragging:
            self.dragging = 0
            self.ReleaseMouse()

        elif self.dragging:
            temp = self.height - 1 - self.thumbHeight
            # figure out where slider should go
            newpos = event.m_y - self.thumbHeight / 2
            if newpos < 0:
                newpos = 0
            elif newpos > temp:
                newpos = temp

            newval = newpos * (self.maxValue + 1) / (temp)

            if newval != self.value:
                self.value = newval
                self.Refresh(0)

                self.evt.SetInt(self.GetValue())
                self.GetEventHandler().ProcessEvent(self.evt)


    def OnMouseEvent(self, event):
        if event.ButtonDown():
            # jump slider to clicked position

            if not self.dragging:
                temp = self.height - self.thumbHeight
                # go to event.m_x - thumbwidth/2, but not less than 0 or greater than
                # width - thumbwidth
                newpos = event.m_y - self.thumbHeight / 2
                if newpos < 0:
                    newpos = 0
                elif newpos > (temp):
                    newpos = temp

                # where is it now?
                curpos = self.value * (temp) / (self.maxValue)

                # only move it if we aren't already clicking on it
                if (newpos < curpos) or (newpos > (curpos + self.thumbHeight)):
                    curpos = newpos

                    # set new value
                    self.value = curpos * (self.maxValue) / (temp)
                    self.Refresh(0)

                    self.evt.SetInt(self.GetValue())
                    self.GetEventHandler().ProcessEvent(self.evt)

                self.dragging = 1
                self.CaptureMouse()

        elif event.ButtonUp() and self.dragging:
            self.dragging = 0
            self.ReleaseMouse()

        elif self.dragging:
            temp = self.height - self.thumbHeight
            # figure out where slider should go
            newpos = event.m_y - self.thumbHeight / 2
            if newpos < 0:
                newpos = 0
            elif newpos > temp:
                newpos = temp

            newval = newpos * (self.maxValue) / (temp)

            if newval != self.value:
                self.value = newval
                self.Refresh(0)

                self.evt.SetInt(self.GetValue())
                self.GetEventHandler().ProcessEvent(self.evt)



class wxHorizontalAudioSlider(wxAudioSlider):

    def __init__(self, parent, id, pos, size, image="images\\hslider.bmp", thumbImage="images\\hthumb.bmp", min=0, max=100):
        wxAudioSlider.__init__(self, parent, id, pos, size, image, thumbImage, min, max)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        # thumbPos is in pixels
        pos = self.value * (self.width - 1 - self.thumbWidth) / (self.maxValue + 1)
        y = (self.height - self.thumbHeight) / 2

        dc.DrawBitmap(self.bitmap, 0, 0)
        dc.DrawBitmap(self.thumbBitmap, pos, y)

    def OnMouseEvent(self, event):
        if event.ButtonDown():
            # jump slider to clicked position
            if not self.dragging:
                # go to event.m_x - thumbwidth/2, but not less than 0 or greater than
                # width - thumbwidth
                newpos = event.m_x - self.thumbWidth / 2
                if newpos < 0:
                    newpos = 0
                elif newpos > (self.width - 1 - self.thumbWidth):
                    newpos = self.width - 1 - self.thumbWidth

                # where is it now?
                curpos = self.value * (self.width - 1 - self.thumbWidth) / (self.maxValue + 1)

                # only move it if we aren't already clicking on it
                if (newpos < curpos) or (newpos > (curpos + self.thumbWidth)):
                    curpos = newpos

                    # set new value
                    self.value = curpos * (self.maxValue + 1) / (self.width - 1 - self.thumbWidth)
                    self.Refresh(0)

                    self.evt.SetInt(self.GetValue())
                    self.GetEventHandler().ProcessEvent(self.evt)


                self.dragging = 1
                self.CaptureMouse()

        elif event.ButtonUp() and self.dragging:
            self.dragging = 0
            self.ReleaseMouse()

        elif self.dragging:
            # figure out where slider should go
            newpos = event.m_x - self.thumbWidth / 2
            if newpos < 0:
                newpos = 0
            elif newpos > (self.width - 1 - self.thumbWidth):
                newpos = self.width - 1 - self.thumbWidth

            newval = newpos * (self.maxValue + 1) / (self.width - 1 - self.thumbWidth)

            if newval != self.value:
                self.value = newval
                self.Refresh(0)

                self.evt.SetInt(self.GetValue())
                self.GetEventHandler().ProcessEvent(self.evt)
            
            