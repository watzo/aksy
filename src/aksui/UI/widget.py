import gtk

class AkWidget(gtk.DrawingArea):
    """
    base for our widgets
    """
    def __init__(self, so = None, soattr = None, interval = 10, units = "", value_offset = 0):
        gtk.DrawingArea.__init__(self)

        self.value_offset = value_offset
        self.interval = interval
        self.units = units

        self.connect("expose_event", self.on_expose)
        self.connect("button_press_event", self.on_button_press)
        self.connect("button_release_event", self.on_button_release)
        self.connect("motion_notify_event", self.on_motion_notify_event)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

        self.is_scaled = False

        self.so = None
        self.soattr = None

        self.init(so, soattr)

    def init(self, so, soattr = None):
        if soattr:
            self.soattr = soattr

        if so:
            self.s = so.s
            self.so = so
            self.so.precache()

            if self.soattr:
                self.value = getattr(self.so, self.soattr)
                
            #self.init_filechooser(self.s)

        self.queue_draw()

    def get_format(self):
        if self.units:
            return '%(#).2f%(units)s' % {"#" : self.value / self.interval, "units" : self.units}
        elif self.interval > 1:
            return '%(#).2f' % {"#" : self.value / self.interval}
        else:
            return str(self.value)

    def init_filechooser(self, s):
        if not getattr(self.s, 'filechooser', None):
            setattr(self.s,'filechooser', UI.FileChooser(s))

    def set_value(self, value):
        # returns True if value actually changed

        before = self.value
        self.value = self.calc_value(value)
        
        if before == self.value:
            return False
        else:
            return True

    def calc_value(self, value):
        # scale and restrict value

        if self.is_scaled:
            scale = self.get_scale()
            newvalue = int(value * scale)
        else:
            newvalue = value

        if newvalue <= self.softmax and newvalue >= self.softmin:
            return newvalue
        elif newvalue > self.softmax:
            return self.softmax
        elif newvalue < self.softmin:
            return self.softmin

    def on_button_press(self, widget, event):
        """
        Example
        for x,y in points:
            hb = HitBox(x-5,y-5,10,10)

            if hb.point_in(event.x,event.y): 
                self.dragging = points.index([x,y])
        """

    def on_expose(self, widget, event):
        """
        self.context = widget.window.cairo_create()
        self.context.set_source_rgb(1, 1, 1)
        self.context.fill_preserve()
        self.context.set_source_rgb(0, 0, 0)
        self.context.stroke()
        """
