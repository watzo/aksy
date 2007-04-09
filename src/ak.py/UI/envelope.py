import pygtk
import gobject,gtk.glade,gtk,aksy

from ak import envelope
from UI.hitbox import *

class Envelope(gtk.DrawingArea):
    def __init__(self,envelope):
        gtk.DrawingArea.__init__(self)
        self.dragging = -1
        self.xoffset = 10
        self.yoffset = 10 
        self.set_size_request(250 + self.xoffset,105 + self.yoffset)
        self.connect("expose_event", self.on_expose)
        self.connect("button_press_event", self.on_button_press)
        self.connect("button_release_event", self.on_button_release)
        self.connect("motion_notify_event", self.on_pointer_motion)
        self.rects = { }

        self.set_envelope(envelope)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

    def set_envelope(self, envelope):
        self.envelope = envelope
        self.queue_draw()

    def on_pointer_motion(self, widget, event):
        if self.envelope:
            self.rects = { }
            points = self.getPoints()

            for x,y in points:
                hb = HitBox(x-5,y-5,10,10)
                pindex = points.index([x,y])
                if hb.point_in(event.x,event.y) or pindex == self.dragging:
                    self.rects[pindex] = gtk.gdk.Rectangle(hb.x,hb.y,hb.w,hb.h) 

            if self.dragging > -1:
                self.envelope.updateNode(self.dragging,event.x,event.y)

            self.queue_draw()

    def on_button_release(self, widget, event):
        self.dragging = -1

    def on_button_press(self, widget, event):
        if self.envelope:
            points = self.getPoints()

            for x,y in points:
                hb = HitBox(x-5,y-5,10,10)

                if hb.point_in(event.x,event.y): 
                    self.dragging = points.index([x,y])

    def getPoints(self):
        if self.envelope:
            # 0 = amp, 1 = filt, 2 = aux
            points = [[
                        [self.envelope.rate1+self.xoffset,self.yoffset],
                        [self.envelope.rate2 + self.envelope.rate1+self.xoffset,100 - self.envelope.level2 + self.yoffset],
                        [self.envelope.rate3 + self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 + self.yoffset]
                     ], [
                        [self.envelope.rate1 + self.xoffset,100 - self.envelope.level1 + self.yoffset],
                        [self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 - self.envelope.level2 + self.yoffset],
                        [self.envelope.rate3 + self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 - self.envelope.level3 + self.yoffset],
                        [self.envelope.rate4 + self.envelope.rate3 + self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 - self.envelope.level4 + self.yoffset]], [
                        [self.envelope.rate1 + self.xoffset,100 - self.envelope.level1 + self.yoffset],
                        [self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 - self.envelope.level2 + self.yoffset],
                        [self.envelope.rate3 + self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 - self.envelope.level3 + self.yoffset],
                        [self.envelope.rate4 + self.envelope.rate3 + self.envelope.rate2 + self.envelope.rate1 + self.xoffset,100 - self.envelope.level4 + self.yoffset]]
                     ]

            i = 0
           
            return points[self.envelope.index]

    def on_expose(self, widget, event):
        if self.envelope:
            self.context = widget.window.cairo_create()
            self.context.set_source_rgb(1, 1, 1)
            self.context.fill_preserve()
            self.context.set_source_rgb(0, 0, 0)
            self.context.stroke()

            self.context.move_to(self.xoffset,100+self.yoffset)

            points = self.getPoints()
            for x,y in points:
                self.context.line_to(x,y)
                #self.context.line_to(x,y)
                #self.context.line_to(x,y)
            self.context.stroke()

            if self.envelope.index == 0:
                sustpt = [self.envelope.rate2 + self.envelope.rate1,100 - self.envelope.level2]
            else:
                sustpt = [self.envelope.rate3 + self.envelope.rate2 + self.envelope.rate1,100 - self.envelope.level3]

            x, y = sustpt

            self.context.set_dash([0,1,0,0,1,1],0.5)
            self.context.move_to(x+self.xoffset,0)
            self.context.line_to(x+self.xoffset,100+self.yoffset)
            self.context.stroke()

            win = widget.window
            self.gc = win.new_gc()
            self.gc.foreground = win.get_colormap().alloc_color("blue")

            for point in self.rects:
                rect = self.rects[point]
                #self.context.rectangle(rect.x,rect.y,rect.width,rect.height)
                win.draw_rectangle(self.gc,False,rect.x,rect.y,rect.width,rect.height) 


