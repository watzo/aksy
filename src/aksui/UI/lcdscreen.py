import gtk

# from aksui.utils.modelutils import *

LCD_PIXELS_WIDTH = 248
LCD_PIXELS_HEIGHT = 60
BORDER_PIXELS = 2
WINDOW_WIDTH = LCD_PIXELS_WIDTH * 2 + BORDER_PIXELS
WINDOW_HEIGHT = LCD_PIXELS_HEIGHT * 2 + BORDER_PIXELS

w,h = 8,256
mapmap = {}

for x in range(0,256):
    ent = [0,0,0,0,0,0,0,0]
    xx = 0
    for p in [128,64,32,16,8,4,2,1]:
        if (x & p > 0):
            ent[xx] = 1 
        else:
            ent[xx] = 0

        xx = xx + 1

    mapmap[x] = ent

non_ascii_keymap = {"F1":1,"F2":2,"F3":3,"F4":4,"F5":5,"F6":6,"equal":25,"plus":25,"minus":26,"Tab":23,"shift":64}
ascii_keymap = {'BackSpace':8,'Delete':127, 'Insert':272, 'Home':288, 'End':289, 'Page_Up':290, 'Page_Down':291, 'Escape':27, 'grave':774, 'space':32, 'Shift_L':769, 'Shift_R':769, 'Return':13, 'Control_L':770, 'Control_R':770,'period':46,"Left":257,"Right":258,"Up":259,"Down":260,}

class LCDScreen(gtk.DrawingArea):
    def __init__(self,s):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.s = s

        self.bv = ''

        self.connect("expose_event", self.on_expose)
        self.connect("realize", self.on_realize)
        self.connect("button_press_event",self.buttonPressEvent)
        self.connect("key_press_event",self.on_key_press_event)
        self.connect("key_release_event",self.on_key_release_event)

        self.add_events(gtk.gdk.KEY_PRESS_MASK|
                        gtk.gdk.KEY_RELEASE_MASK|
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

        self.set_flags(gtk.CAN_FOCUS)

    def updateLCD(self):
        if self.s:
            pixel_data, control_data = self.s.frontpaneltools.get_panel_state()

            xx,yy = 0,0
            ugiv = {}

            for x in pixel_data:
                x = ord(x)
                for c in mapmap[x]:
                    ugiv[xx] = c 
                    xx = xx + 1

            self.bv = ugiv

    def on_key_release_event(self, widget, event):
        self.handle_keys(widget,event,0)
        self.grab_focus()
        
    def on_key_press_event(self, widget, event):
        self.handle_keys(widget,event,1)
        self.grab_focus()

    def handle_keys(self, widget, event, onoff):
        # We want to ignore irrelevant modifiers like ScrollLock
        # window, multi, fx, edit sample, edit program, record, utilities, save, load
        ctrlmap = { 'w':7,'F1':23,'F2':19,'F3':22,'F4':18,'F5':21,'F6':17,'F7':20,'F8':16 }
        wheelmap = { 'F11':-1, 'F12':1 }
        ignore = ['Control_L','Control_R']

        modifiers = { gtk.gdk.SHIFT_MASK:1 }

        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname in ignore:
            return

        m = 0

        for mod in modifiers.keys():
            if event.keyval & mod:
                m += modifiers[mod]

        if len(keyname) == 1:
            ascii = ord(keyname)
        else:
            ascii = 0

        fp = self.s.frontpaneltools

        hfunc = None

        if event.state & gtk.gdk.CONTROL_MASK and keyname in ctrlmap.keys():
            funcmap = {1:fp.keypress_hold, 0:fp.keypress_release}
            hfunc = funcmap[onoff]
            arg0 = ctrlmap[keyname]
        elif keyname in wheelmap.keys() and onoff:
            hfunc = fp.move_datawheel
            arg0 = wheelmap[keyname]
        elif keyname in non_ascii_keymap.keys():
            funcmap = {1:fp.keypress_hold, 0:fp.keypress_release}
            hfunc = funcmap[onoff]
            arg0 = non_ascii_keymap[keyname]
        elif ascii > 0 and ascii < 127:
            funcmap = {1:fp.ascii_keypress_hold, 0:fp.ascii_keypress_release}
            hfunc = funcmap[onoff]
            arg0 = ascii
            if onoff:
                arg1 = m
            else:
                arg1 = 0
        elif keyname in ascii_keymap.keys():
            funcmap = {1:fp.ascii_keypress_hold, 0:fp.ascii_keypress_release}
            hfunc = funcmap[onoff]
            arg0 = ascii_keymap[keyname]
            if onoff:
                arg1 = m
            else:
                arg1 = 0

        if hfunc:
            if hfunc.func_code.co_argcount == 3:
                hfunc(arg0, arg1)
            elif hfunc.func_code.co_argcount == 2:
                hfunc(arg0)

            self.updateLCD()
            self.redraw_canvas()


    def buttonPressEvent(self, widget, event):
        x = event.x/2
        y = event.y/2

        if event.type == gtk.gdk.BUTTON_PRESS:
            self.s.frontpaneltools.mouseclick_at_screen(int(x),int(y))
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            self.s.frontpaneltools.mousedoubleclick_at_screen(int(x),int(y))

        self.updateLCD()
        self.redraw_canvas()

        self.grab_focus()

    def redraw_canvas(self):
        rect = gtk.gdk.Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.invalidate_rect(rect, True)
        self.window.process_updates(True)

    def on_realize(self, widget):
        self.gc = widget.window.new_gc()

    def on_expose(self, widget, event):
        self.updateLCD()

        on_color = gtk.gdk.Color(0xFF,0xFF,0xFF,0)
        off_color = gtk.gdk.Color(0,0,0,1)

        if self.bv:
            for y in range(0, LCD_PIXELS_HEIGHT):
                for x in range(0, LCD_PIXELS_WIDTH):
                    val = self.bv[x + (y * LCD_PIXELS_WIDTH)] 
                    xx = x * 2
                    yy = y * 2

                    if val == 1:
                        self.window.draw_point(self.gc,xx,yy)
                        self.window.draw_point(self.gc,xx+1,yy+1)
                        self.window.draw_point(self.gc,xx,yy+1)
                        self.window.draw_point(self.gc,xx+1,yy)

        return False
