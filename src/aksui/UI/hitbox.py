import gtk

class HitBox:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y 
        self.w = w 
        self.h = h
        self.is_scaled = False
        self.index = 0

    def point_in(self,x,y):
        horiz = False
        vert = False

        if x >= self.x and x <= self.x+self.w:
            horiz = True
        if y >= self.y and y <= self.y+self.h:
            vert = True

        if horiz and vert:
            return True
        else:
            return False

    def get_scale(self):
        if self.widget and self.is_scaled:
            windowsize = self.widget.window.get_size()
            buffer = (self.w * 4) + 60
            windowsize = [windowsize[0] - buffer, windowsize[1]]
            range = self.max - self.min
            scale = float(range) / float(windowsize[0]) # get percentage of window width the control has
            return scale
        else:
            return 1.0

    def get_scaled_value(self):
        return self.x * 1/self.get_scale()

    def get_offset(self):
        if self.index == 0:
            offset = -self.w / 2
        elif self.index == 1:
            offset = (self.w / 2) + 1
        else:
            offset = 0

        return offset


    def get_scaled_rect(self):
        scale = self.get_scale()
        if scale > 0:
            rect = self.get_rectangle()

            x = int(rect.x * (1/scale))

            offset = self.get_offset()

            rect = gtk.gdk.Rectangle(x + offset, rect.y, rect.width, self.h)
            return rect
        else:
            return None

    def get_widget_rect(self, widget = None):
        # set widget it if was given, otherwise leave it
        if widget:
            self.widget = widget

        if self.widget:
            rect = self.get_scaled_rect()
            win = self.widget.window
            size = win.get_size()
            vertical_align = (size[1] / 2) - rect.height / 2

            if self.is_scaled:
                rect.x += rect.width
                
            return gtk.gdk.Rectangle(int(rect.x), int(vertical_align), int(rect.width), int(rect.height))
        else:
            return None

    def point_in_widget_rect(self, x, y):
        #print self.x, ',', self.y, ' ', x, ',', y
        rect = self.get_widget_rect()

        horiz = False
        vert = False

        if x >= rect.x and x <= rect.x+rect.width:
            horiz = True
        if y >= rect.y and y <= rect.y+rect.height:
            vert = True

        if horiz and vert:
            return True
        else:
            return False

    def get_centered_rect(self):
        # get centered rectangle for drawing
        r = self.get_rectangle()
        r = gtk.gdk.Rectangle(int(self.x - (r.x - r.width/2)), int(self.y - (r.y - r.height / 2)), int(self.w), int(self.h))
        return r

    def get_rectangle(self):
        return gtk.gdk.Rectangle(int(self.x), int(self.y), int(self.w), int(self.h)) 

