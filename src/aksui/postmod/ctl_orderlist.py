
import wx
import canvas

import observer

class OrderListControl(canvas.Canvas, observer.Subject):
    HEIGHT = 41
    #HEIGHT = 81
    WIDTH = 592
    vwidth = 592
    vheight = 41

    
    def __init__(self, parent, id):
        observer.Subject.__init__(self)
        
        self.data = []
        self.cursorx = 0
        self.cursory = 0

        self.highlightx, self.highlighty = None, None

        self.boxwidth = 26
        self.boxheight = 20

        self.lastEntryPos = -1  # the last cursor position data was entered via keyboard
        
        canvas.Canvas.__init__(self, parent, id, size=wx.Size(self.WIDTH, self.HEIGHT))
        self.SetBackgroundColour(wx.WHITE)

        #self.SetScrollbars(self.boxwidth, self.boxheight, 20, 20)
        #self.SetScrollRate(self.boxwidth, self.boxheight)
        self.SetScrollRate(0, self.boxheight)

        self.WIDTH, self.HEIGHT = self.GetClientSizeTuple()

        self.vwidth, self.vheight = self.getRequiredSize()
        self.SetVirtualSize((self.vwidth, self.vheight))

        # maxx and maxy are the max in cursor pos (not pixel pos)
        #self.maxx = self.getNumPerRow()
        #self.maxy = self.vheight / self.boxheight - 1

        self.maxx = self.vwidth / self.boxwidth - 1
        self.maxy = self.vheight / self.boxheight - 1
        #self.SetVirtualSize((self.vwidth, self.vheight))

        #self.onSize(None, self.GetClientSizeTuple())

        wx.EVT_CHAR(self, self.OnChar)
        wx.EVT_LEFT_DOWN(self, self.OnLeftDown)
        wx.EVT_LEFT_DCLICK(self, self.OnLeftDoubleClick)
        wx.EVT_SCROLLWIN(self, self.OnScroll)
        wx.EVT_SET_FOCUS(self, self.OnSetFocus)
        wx.EVT_KILL_FOCUS(self, self.OnKillFocus)

        self.limitsFunc = self.actionFunc = None


    def getRequiredSize(self):
        # gets the required size the window would have to be, given the current width,
        # to fit all of the data.

        lendata = len(self.data)
        #print lendata, (self.WIDTH / self.boxwidth)
        reqy = lendata / (self.WIDTH / self.boxwidth)
        if reqy == 0:
            # always at least two rows
            reqy = 1
        reqy = (reqy+1) * self.boxheight
        #print "required size", self.WIDTH, reqy
        return self.WIDTH, reqy        



    def getData(self):
        return self.data

    def getNumPerRow(self):
        #csx, csy = self.GetClientSizeTuple()
        csx, csy = self.GetVirtualSizeTuple()
        maxx = csx / self.boxwidth - 1
        return maxx
        

    def getIndex(self):
        # get linear data index from current cursor position
        yadd = self.cursory * self.getNumPerRow()
        if yadd: yadd += (self.cursory)
        idx = self.cursorx + yadd
        return idx

    def getIndexXY(self, x, y):
        # get linear data index from specified cursor position
        yadd = y * self.getNumPerRow()
        if yadd: yadd += (self.cursory)
        idx = x + yadd
        return idx

    def getCursorPos(self, index):
        # return cursor pos for specified index
        npr = self.getNumPerRow() + 1
        x = index % npr
        y = index / npr
        return x,y


    def onSize(self, event=None, size=None):
        """Perform actual redraw to off-screen buffer only when the
        size of the canvas has changed. This saves a lot of computation
        since the same image can be re-used, provided the canvas size
        hasn't changed."""
        if event:
            size = event.GetSize()

        if not size:
            size = self.GetClientSizeTuple()

        if size:
            self.WIDTH, self.HEIGHT = size
            self.vwidth, self.vheight = self.getRequiredSize()
            #print "size wid", self.WIDTH, self.HEIGHT, self.vwidth, self.vheight
            self.maxx = self.vwidth / self.boxwidth - 1
            self.maxy = self.vheight / self.boxheight - 1
            #print "size max", self.maxx, self.maxy
            #print self.WIDTH, self.HEIGHT, self.vwidth, self.vheight
            self.SetVirtualSize((self.vwidth, self.vheight))

        self.hasfocus = 1

        self.MakeNewBuffer()
        #a = time.time()
        #for i in range(20):
        #    self.DrawBuffer()
        self.DrawBuffer()
        #print "timed", time.time() - a
        self.Refresh()

    #psyco.bind(onSize)


    def OnSetFocus(self, event):
        self.hasfocus = 1
        self.DrawBuffer()
        self.Refresh()
        event.Skip()
        
    def OnKillFocus(self, event):
        self.hasfocus = 0
        self.DrawBuffer()
        self.Refresh()
        event.Skip()

        

    def OnScroll(self, event):
        event.Skip(True)
        #self.PrepareDC(self.buffer)
        #self.DrawBuffer()
        #self.Refresh()
        



    def SetLimitsFunc(self, func):
        # func should return min and max limits for data
        self.limitsFunc = func

    def SetActionFunc(self, func):
        # func should accept index, and data param, for when the element is activated
        # and a flag specifying whether it was a double click (true for double click)
        self.actionFunc = func
        


    def DrawBuffer(self):
        #self.PrepareDC(self.buffer)

        bkgbrush = wx.WHITE_BRUSH
        #playbrush = wx.BLUE_BRUSH
        #playbrush = wx.Brush(wx.Colour(0xCE, 0xDF, 0xEF))
        playbrush = wx.Brush(wx.Colour(0xE7, 0xEB, 0xF7))

        viewx, viewy = self.GetViewStart()
        #print self.cursory-viewy, viewy-self.cursory
        if self.cursory-viewy > 1 or self.cursory-viewy < 0:
            self.Scroll(0, max(self.cursory, 0))

        self.buffer.SetFont(wx.NORMAL_FONT)
        self.buffer.SetBrush(bkgbrush)

        boxwidth = self.boxwidth
        boxheight = self.boxheight
        xpos = 0
        curx = cury = 0
        restore = 0
        if self.hasfocus:
            cursorpen = wx.ThePenList.FindOrCreatePen(wx.BLUE, 3, wx.SOLID)
        else:
            cursorpen = wx.ThePenList.FindOrCreatePen(wx.BLUE, 1, wx.SOLID)

        width, height = self.vwidth, self.vheight
        #width, height = self.WIDTH, self.HEIGHT

        self.buffer.SetPen(wx.WHITE_PEN)
        self.buffer.DrawRectangle(0, 0, width, height)
        self.buffer.SetPen(wx.GREY_PEN)


        # draw horizontal line down center
        #self.buffer.DrawLine(0, self.HEIGHT / 2, self.WIDTH, self.HEIGHT / 2)

        # draw horizontal lines
        ypos = 0
        while 1:
            ypos += boxheight
            if ypos > height:
                break
            self.buffer.DrawLine(0, ypos, width-(width % boxwidth), ypos)
            #print "wo", width % boxwidth

        # now draw vertical spacer lines
        xpos = 0
        while 1:
            xpos += boxwidth
            if xpos > width:
                break
            self.buffer.DrawLine(xpos, 0, xpos, height)



        # now draw the hightlight
        if self.highlightx != None:
            self.buffer.SetBrush(playbrush)
            #self.buffer.SetPen(wx.GREEN_PEN)
            self.buffer.SetPen(wx.ThePenList.FindOrCreatePen(wx.Colour(0,100,255), 1, wx.SOLID))
            #self.buffer.DrawRectangle(self.highlightx*boxwidth+2, self.highlighty*boxheight+1, boxwidth-3, boxheight-3)
            self.buffer.DrawRectangle(self.highlightx*boxwidth, self.highlighty*boxheight, boxwidth+1, boxheight+1)
            self.buffer.SetBrush(bkgbrush)

        # now draw the cursor
        self.buffer.SetPen(cursorpen)
        self.buffer.DrawRectangle(self.cursorx*boxwidth, self.cursory*boxheight, boxwidth, boxheight)

        self.buffer.SetBrush(bkgbrush)
        self.buffer.SetPen(wx.GREY_PEN)

        # now the text
        
        i = 0
        xpos = 0
        ypos = 0
        for num in self.data:
            st = str(num)
            tw, th = self.buffer.GetTextExtent(st)
            tw, th = tw/2, th/2
            
            x = xpos + (boxwidth / 2)
            y = (ypos*boxheight) + (boxheight / 2)
            xpos += boxwidth
            if (xpos/boxwidth > self.maxx+1):
                xpos = 0
                ypos += 1
                x = xpos + (boxwidth / 2)
                y = (ypos*boxheight) + (boxheight / 2)
                xpos += boxwidth
            #self.buffer.DrawText(str(num), x-tw-1, y-th)
            self.buffer.DrawText(str(num), x-tw, y-th)

    #psyco.bind(DrawBuffer)
            
    def SetLabel(self, message):
        data = message.split(",")
        self.data = []
        for x in data:
            try:
                x = int(x)
            except:
                x = x.strip()
            self.data.append(x)

        self.SetVirtualSize(self.getRequiredSize())
        self.onSize(None, self.GetClientSizeTuple())
                
        self.DrawBuffer()
        self.Refresh()


    def IncData(self, index, value=1):
        self.SetData(index, inc=value)        

    def SetData(self, index, value=0, inc=0):
        if index >= len(self.data):
            return 0

        #print "set", index, value, inc
        
        if self.data[index] == "END":
            self.data[index] = 0
            self.data.append("END")
            self.onSize()

        if inc:
            value = self.data[index] + inc

        mn, mx = self.limitsFunc()
        if value < mn or value > mx:
            return 0

        self.data[index] = value
            
        self.notify()   # notify observers
        return 1

    def DeleteData(self, index):
        if index >= len(self.data):
            return 0

        if self.data[index] != "END":
            del self.data[index]
            self.notify()
        return 1

    def InsertData(self, index, value=0):
        if index >= len(self.data):
            return 0
    
        self.data.insert(index, value)
        self.notify()
        return 1

    def OnChar(self, event):
        ch = event.GetKeyCode()
        if ch < 256:
            chc = chr(ch)
        else:
            chc = chr(0)

        if ch == 127:   # DEL
            idx = self.getIndex()
            self.DeleteData(idx)
        elif ch == 324: # INS
            idx = self.getIndex()
            self.InsertData(idx, 0)

        if chc == ' ':
            idx = self.getIndex()
            if idx < len(self.data):
                self.actionFunc(idx, self.data[idx], 0)
            return

        if chc == '+':
            try:
                self.IncData(self.getIndex(), 1)
            except:
                pass
        elif chc == '-':
            try:
                self.IncData(self.getIndex(), -1)
            except:
                pass
        elif chc in ('0','1','2','3','4','5','6','7','8','9'):
            if self.cursorx == self.lastEntryPos:
                # see if we can append
                mn, mx = self.limitsFunc()
                idx = self.getIndex()
                if idx < len(self.data):
                    dat = str(self.data[self.getIndex()])
                    try:
                        newval = int(dat + chc)
                    except ValueError:
                        newval = int(str(chc))
                    if newval > mx:
                        # nope
                        newval = int(str(chc))
                    else:
                        pass
                        #newval = int(str(chc))
                else:
                    newval = int(str(chc))                    
            else:
                newval = int(str(chc))
            #print "setting", self.getIndex(), newval
            self.SetData(self.getIndex(), newval)
            self.lastEntryPos = self.cursorx
            
                    
        # 317 = up, 319=down, 316 = left, 317 = right
        old = self.cursorx, self.cursory
        if ch == 317: self.cursory -= 1
        elif ch == 319: self.cursory += 1
        if ch == 316:
            self.cursorx -= 1
            if self.cursorx < 0:
                if self.cursory-1 >= 0:
                    self.cursorx = self.maxx
                    self.cursory -= 1

        elif ch == 318:
            self.cursorx += 1
            if self.cursorx > self.maxx:
                if self.cursory+1 <= self.maxy:
                    self.cursorx = 0
                    self.cursory += 1
        self.constrainCursor()
        if old != (self.cursorx, self.cursory):
            # cursor changed
            self.lastEntryPos = old[0]
            
        self.DrawBuffer()
        self.Refresh()

        event.Skip()


    def isValidCursorPos(self, x, y):
        return (x <= self.maxx and y <= self.maxy and x >= 0 and y >= 0)
            

    def constrainCursor(self):
        #print self.cursory, self.maxy
        self.cursorx = min(self.cursorx, self.maxx)
        self.cursorx = max(self.cursorx, 0)
        #self.cursory = min(self.cursory, 1)
        self.cursory = min(self.cursory, self.maxy)
        self.cursory = max(self.cursory, 0)

    def highlight(self, order):
        newpos = self.getCursorPos(order)
        if (self.highlightx, self.highlighty) != newpos:
            self.highlightx, self.highlighty = newpos
            self.DrawBuffer()
            self.Refresh()

        
        
    def OnLeftDown(self, event):
        x, y = self.CalcUnscrolledPosition(event.m_x, event.m_y)
        curx = x / self.boxwidth
        cury = y / self.boxheight
        if self.isValidCursorPos(curx, cury):
            self.cursorx, self.cursory = curx, cury
            self.constrainCursor()
            self.DrawBuffer()
            self.Refresh()

    def OnLeftDoubleClick(self, event):
        idx = self.getIndex()
        if idx < len(self.data):
            self.actionFunc(idx, self.data[idx], 1)
        
        
#psyco.bind(OrderListControl)
