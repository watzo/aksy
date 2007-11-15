# Custom widgets via Cairo: Knob, Level, Range, Keygroup etc.

import math, urllib
from urlparse import urlparse

import gobject, gtk

import hitbox, widget

from aksui.utils import modelutils, midiutils
from aksui.ak import *

class SliderWidget(hitbox.HitBox):
    def __init__(self, min, max, w, h, value_descriptions = None, is_scaled = True, index = 0, value_offset = 0):
        # init sliders
        hitbox.HitBox.__init__(self, min, 0, w, h)
        self.value_offset = value_offset
        self.index = index
        # boundaries
        self.max = max
        self.min = min
        # soft max/min, keep sliders from colliding
        self.softmax = max
        self.softmin = min
        self.is_scaled = is_scaled
        # current position
        self.value = self.min
        self.dragging = False
        self.draggingpoint = None

        # value descriptions
        if value_descriptions:
            self.value_descriptions = value_descriptions
        else:
            self.value_descriptions = None

        self.widget = None
        self.state_type = gtk.STATE_NORMAL
        self.shadow_type = gtk.SHADOW_IN

    def set_value(self, value):
        self.x = self.calc_value(value)

    def get_snap(self, s0x):
        last = 0
        calc_value = self.calc_value(s0x)
        for i in octaves_snap:
            if calc_value > last and calc_value < i:
                dist = [calc_value - last, i - calc_value]
                if dist[0] < dist[1]:
                    s0x = last / self.get_scale()
                else:
                    s0x = i / self.get_scale()
                break
            else:
                last = i
        return s0x

    def calc_value(self, value):
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

    def draw(self, widget, event):
        cr = self.context = widget.window.cairo_create()
        
        if self.dragging:
            color = "blue"
        else:
            color = "black"

        # draw handle at position
        rect = self.get_widget_rect(widget)

        if rect:
            size = widget.window.get_size()

            rect.y = (size[1] / 2) - rect.height / 2

            style = widget.get_style()
            
            style.paint_box(widget.window, self.state_type, self.shadow_type, rect, widget, "", rect.x, rect.y, rect.width, rect.height)

    def draw_text(self, widget, event):
        cr = self.context = widget.window.cairo_create()
        rect = self.get_widget_rect(widget)
        if rect:
            size = widget.window.get_size()

            if self.index != 2:
                cr.set_font_size(10.0)
                cr.set_source_rgb(0.0, 0.0, 0.0)
                fascent, fdescent, fheight, fadvance, fyadvance = cr.font_extents()
                # sloppy
                cr.move_to((size[0] - 60) + (self.index * 30), ((size[1] / 2) - fdescent + fheight / 2) + 1)

                if self.value_descriptions:
                    text = self.value_descriptions[self.x]
                elif self.units == "db":
                    # hack, there's an existing way to do this, just lazy
                    text = '%(#).2f' % {"#" : ((float(self.x) - float(self.value_offset)) / 10.0)}
                else:
                    text = str(self.x - self.value_offset)
                    
                cr.show_text(text)

class AkKnobWidget(widget.AkWidget):
    def __init__(self, samplerobject = None, samplerobjectattr = None, min = -600, max = 60, interval = 10, units = "db", mod_destination = None):
        widget.AkWidget.__init__(self, samplerobject, samplerobjectattr, interval, units)
        self.connect("value-changed", self.on_value_changed)

        self.set_size_request(35, 35)

        self.max = max
        self.min = min

        self.softmax = max
        self.softmin = min

        self.dragging = False
        self.valuestart = None
        self.pinlevelstart = None
        self.draggingstart = None
        if mod_destination:
            self.mod_destination_index = modulationmatrix.ModulationMatrix.destinations.index(mod_destination)
        else:
            self.mod_destination_index = None

        self.queue_draw()

    def get_current_pin(self, create_new = True):
        if isinstance(self.so, keygroup.Keygroup):
            kg = self.so 
        elif hasattr(self.so, 'keygroup'):
            kg = self.so.keygroup
        else:
            return None
         
        return kg.get_pin_by_source_and_dest(kg.current_mod_source_index, self.mod_destination_index, create_new)

    def on_button_press(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            self.dragging = True
            #print "hello...", self.dragging
            self.draggingstart = event.y
            if self.value is not None: 
                self.valuestart = self.value
            else:
                self.valuestart = 0
                
            pin = self.get_current_pin()
            if pin:
                self.pinlevelstart = pin.level
                
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            ctrl_pressed = event.state & gtk.gdk.CONTROL_MASK
            if not ctrl_pressed:
                changed = self.set_value(0.0)
            if changed:
                self.emit("value-changed")
            else:
                pin = self.get_current_pin()
                if pin:
                    pin.set_value(0)
        self.queue_draw()

    def on_button_release(self, widget, event):
        self.dragging = False
        self.draggingstart = None
        self.queue_draw()

    def on_motion_notify_event(self, widget, event):
        #print "motion...", self, type(self.so), self.dragging
        if self.dragging:
            # udate value
            delta = -(event.y - self.draggingstart)

            ctrl_pressed = event.state & gtk.gdk.CONTROL_MASK
            shift_pressed = event.state & gtk.gdk.SHIFT_MASK

            if not shift_pressed:
                interval = self.interval
            else:
                interval = 1.0

            changed = None

            if not ctrl_pressed:
                changed = self.set_value(self.valuestart + (delta * interval))
                
            if changed:
                self.emit("value-changed")
            else:
                # find pin that matches current 'source' and 'destination'
                pin = self.get_current_pin()
                if pin:
                    pin.set_value(self.pinlevelstart + delta)

        self.queue_draw()

    def on_value_changed(self, widget):
        if self.soattr and self.so:
            self.queue_draw()
            self.so.set(self.soattr, int(self.value))

    def get_pct(self, value, min, max):
        if value < min:
            value = min
        elif value > max:
            value = max
        num = float(value) - float(min)
        range = float(max) - float(min)
        pct = float(num) / float(range)
        return pct

    def get_pctatzero(self):
        num = float(value) - float(min)
        range = float(max) - float(min)
        pct = float(num) / float(range)
        pctatzero = abs(float(min) / float(range))
        return pctatzero

    def draw_value_line(self, cr, x, y, radius, value, min, max):
        # the float thing was a little bit unexpected
        pct = self.get_pct(value, min, max)

        self.do_line(cr, x, y, radius, radius, pct, 2)

    def on_expose(self, widget, event):
        self.value = self.so.attrscache[self.soattr]
        #rect = event.area # only redraw a small portion
        size = widget.window.get_size()
        rect = gtk.gdk.Rectangle(0,0,size[0],size[1])
        return self.draw(widget.window, widget, rect)

    def draw(self, window, widget, area):
        cr = window.cairo_create()
        cr.rectangle(area.x, area.y, area.width, area.height)
        cr.clip()

        rect = area

        """
        rect = widget.get_allocation()
        """

        x = rect.width / 2 + area.x
        y = rect.height / 2 + area.y

        radius = (min(rect.width / 2, rect.height / 2) - 10)

        fg = (self.style.fg[gtk.STATE_NORMAL])
        cr.set_source_rgb(fg.red, fg.green, fg.blue)

        cr.set_line_width(1)
        cr.arc(x, y, radius, 0, 2 * math.pi)

        cr.stroke()

        cr.save()

        self.draw_value_line(cr, x, y, radius, self.value, self.min, self.max)

#        pin = self.get_current_pin(False)
#        if pin and self.value is not None:
#            range = float(self.max) - float(self.min)
#            pinoffset = float(float(pin.level) / 100.0) * float(range)
#            pct = self.get_pct(self.value, self.min, self.max)
#            pinpct = self.get_pct(self.value + pinoffset, self.min, self.max)
#            cr.set_source_rgb(0, 0, 0)
#            self.do_mod_arc(cr, x, y, radius, radius, pct, pinpct)
#            self.draw_value_line(cr, x, y, radius, self.value + pinoffset, self.min, self.max)

        """
        cr.set_source_rgb(0, 0, 0)
        self.do_line(cr, x, y, radius, radius / 2, 0, 0.5, False)
        self.do_line(cr, x, y, radius, radius / 2, 1, 0.5, False)
        cr.set_source_rgb(0, 0, 1)
        self.do_line(cr, x, y, radius, radius / 8, pctatzero, 1.0, False)
        """

        cr.set_font_size(10.0)
        cr.set_source_rgb(fg.red, fg.green, fg.blue)
        if self.dragging:
            text = self.get_format()
        else:
            text = self.so.get_knob(self.soattr)

        is_mod = self.soattr.startswith('MOD_')

        if text and len(text) > 0 and (is_mod and text != "0" or not is_mod):
            xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
            cr.move_to(x - width / 2 + xbearing, y + radius - ybearing + 2)
            cr.show_text(text)

        cr.restore()
        return False

    def do_line(self, cr, x, y, radius, radius_inset, pct, lw, from_center = True):
        cr.set_line_width(1)
        ei = (math.pi * (6.0/4.0) * pct) - (math.pi * (6.0/8.0))

        if from_center:
            cr.move_to(x, y)
            cr.line_to(x + radius * math.sin( ei ), y + radius * -math.cos( ei ))
        else:
            cr.move_to(x + radius * math.sin( ei ), y + radius * -math.cos( ei ))
            cr.line_to(x + radius_inset * math.sin(ei), y + radius_inset * -math.cos(ei))

        cr.stroke()

    def do_mod_arc(self, cr, x, y, radius, radius_inset, pct, pinpct):
        cr.set_line_width(0.5)
        pct += 1.0
        pinpct += 1.0
        start = (math.pi * (6.0/4.0) * pct) - (math.pi * (6.0/8.0))
        end = (math.pi * (6.0/4.0) * pinpct) - (math.pi * (6.0/8.0))

        cr.move_to(x, y)
        if start < end:
            cr.arc(x, y, radius, start, end)
        else:
            cr.arc_negative(x, y, radius, start, end)
        cr.set_source_rgb(0, 0, 1)
        cr.fill_preserve()
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()

class LevelKnobWidget(AkKnobWidget):
    def __init__(self, samplerobject = None):
        AkKnobWidget.__init__(self, samplerobject, "level", -600, 60, 10, "db")
        self.interval = 10

    def get_format(self):
        return '%(#).2fdb' % {"#" : self.value / self.interval}

class AkRangeWidget(widget.AkWidget):
    def __init__(self, samplerobject = None, samplerobjectattr = None, min = 0, max = 127, multislider = True, value_offset = 0):
        # init sliders
        widget.AkWidget.__init__(self, samplerobject, samplerobjectattr)

        self.multislider = multislider
        
        self.sliderwidth = 8 
        self.sliderheight = 12
        self.middlesliderheight = 12

        self.set_size_request(240, self.sliderheight * 2)

        self.min = min
        self.max = max

        if self.multislider:
            self.sliders = [
                SliderWidget(self.min, self.max, self.sliderwidth, self.sliderheight, None, True, 0, value_offset),
                SliderWidget(self.min, self.max, self.sliderwidth, self.sliderheight, None, True, 1, value_offset),
                SliderWidget(self.min, self.max, 6, self.middlesliderheight, None, False, 2, value_offset)]
            
            self.sliders[0].x = min 
            self.sliders[1].x = max 
            
            self.sliders[0].shadow_type = gtk.SHADOW_IN 
            self.sliders[1].shadow_type = gtk.SHADOW_IN 
            self.sliders[2].shadow_type = gtk.SHADOW_OUT 
        else:
            self.sliders = [
                SliderWidget(self.min, self.max, self.sliderwidth, self.sliderheight, None, True, 0, value_offset),
                ]
            self.sliders[0].x = min 
            self.sliders[0].shadow_type = gtk.SHADOW_OUT 

    def update_middle_slider(self, widget = None):
        if self.multislider:
            s2 = self.sliders[2]
            s1 = self.sliders[1]
            s0 = self.sliders[0]
    
            if widget:
                s0.widget = widget
                s1.widget = widget
                s2.widget = widget
    
            self.sliders[2].x = int(self.sliders[0].get_scaled_value() + s0.w + 2)
            self.sliders[2].y = 1
            self.sliders[2].w = max(int(self.sliders[1].get_scaled_value() + s1.w + s0.w - self.sliders[2].x),0)
            #print self.sliders[2].x, self.sliders[2].y, self.sliders[2].w
    
    def on_button_press(self, widget, event):
        for slider in self.sliders:
            slider.widget = widget
            if slider.point_in_widget_rect(event.x, event.y): 
                if not slider.dragging:
                    slider.dragging = True
                    slider.draggingpoint = [event.x, event.y]
                    self.sliders[0].draggingvalue = self.sliders[0].x
                    if self.multislider:
                        self.sliders[1].draggingvalue = self.sliders[1].x
                        self.sliders[2].draggingvalue = self.sliders[2].x
                    # mark slider as being dragged
        self.queue_draw()

    def on_button_release(self, widget, event):
        for slider in self.sliders:
            slider.widget = widget
            slider.dragging = False
            slider.draggingpoint = None

        self.queue_draw()

    def on_motion_notify_event(self, widget, event):
        # iterate through sliders
        s0 = self.sliders[0]
        s0xvalue = s0.x
        
        if self.multislider:
            s1 = self.sliders[1]
            s0.softmax = s1.x
            s1.softmin = s0.x
            s1xvalue = s1.x

        ctrl_pressed = event.state & gtk.gdk.CONTROL_MASK

        for slider in self.sliders:
            slider.widget = widget
            if slider.dragging:
                delta = event.x - slider.draggingpoint[0]

                """
                if ctrl_pressed:
                    delta *= 0.25
                """

                if self.multislider and self.sliders.index(slider) == 2:
                        s0x = (s0.draggingvalue / s0.get_scale()) + delta
                        s1x = (s1.draggingvalue / s1.get_scale()) + delta
    
                        if ctrl_pressed:
                            s0x = s0.get_snap(s0x)
                            s1x = s1.get_snap(s1x)
    
                        s0.set_value(s0x)
                        s1.set_value(s1x)
                else:
                    slider.set_value((slider.draggingvalue / slider.get_scale()) + delta)
    
                    slider.state_type = gtk.STATE_ACTIVE
            elif slider.point_in_widget_rect(event.x, event.y):
                slider.state_type = gtk.STATE_PRELIGHT
            else:                
                slider.state_type = gtk.STATE_NORMAL

        self.queue_draw()

        if s0xvalue != s0.x: 
            self.emit("slider_1_changed", s0.x)
            
        if self.multislider:
            if s1xvalue != s1.x:
                self.emit("slider_2_changed", s1.x)

        return True

    def on_expose(self, widget, event):
        self.update_middle_slider(widget)
        self.context = widget.window.cairo_create()

        # draw handles
        for slider in self.sliders:
            slider.draw(widget, event)
        # draw text
        for slider in self.sliders:
            slider.draw_text(widget, event)

        return False

class PartRangeWidget(AkRangeWidget):
    def __init__(self, part, attr):
        AkRangeWidget.__init__(self, part, None, 0, 660, False, 600)
        self.part = part
        self.part.update()
        self.s = part.s
        self.attr = attr
        self.value_offset = 600

        self.sliders[0].x = getattr(self.part, attr) + self.value_offset
        self.sliders[0].units = "db"

        self.connect("slider_1_changed", self.on_slider_1_changed)

        self.queue_draw()

    def on_slider_1_changed(self, widget, value):
        if self.part:
            self.part.set(self.attr, value - self.value_offset)

class KeygroupRangeWidget(AkRangeWidget):
    def __init__(self, keygroup):
        AkRangeWidget.__init__(self, keygroup, None, 0, 127)
        self.keygroup = keygroup
        self.keygroup.update()
        self.s = keygroup.s

        self.sliders[0].value_descriptions = midiutils.midinotes
        self.sliders[1].value_descriptions = midiutils.midinotes
        self.sliders[0].x = self.keygroup.low_note
        self.sliders[1].x = self.keygroup.high_note

        self.connect("slider_1_changed", self.on_slider_1_changed)
        self.connect("slider_2_changed", self.on_slider_2_changed)

        self.queue_draw()

    def on_slider_1_changed(self, widget, value):
        if self.keygroup:
            self.keygroup.set("low_note", value)

    def on_slider_2_changed(self, widget, value):
        if self.keygroup:
            self.keygroup.set("high_note", value)

    @staticmethod
    def test_AkRangeWidget():
        test = tc()

class MiniZoneWidget(widget.AkWidget):
    def __init__(self, zone):
        widget.AkWidget.__init__(self, zone)
        
        self.zone = zone
        self.zone.update()
        self.zone.set_callback = self.on_set_callback

        self.drag_dest_set(0, [], 0)

        self.connect("drag_data_received", self.on_drag_data_received)
        self.connect("drag_motion", self.on_drag_motion)
        self.connect("button_press_event", self.on_button_press)
        self.connect("button_release_event", self.on_button_release)
        self.connect("motion_notify_event", self.on_motion_notify_event)
        self.connect("expose_event", self.on_expose)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

        self.set_size_request(100, 15)
        
    def on_set_callback(self, attrname, attrval):
        self.queue_draw()

    def do_upload(self, filename):
        return True

    def on_drag_motion(self, widget, context, x, y, timestamp):
        #print "huh"
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        l.set_text('\n'.join([str(t) for t in context.targets]))
        return True

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        #print selection.data, target_type
        if target_type == 0:
            # try uploading that shit
            parsed = urlparse(selection.data.rstrip('\r\n'))
            path = urllib.unquote(parsed[2])
            self.s.filechooser.upload(path)
            samplename = selection.data
            zone.set_sample(samplename)

        context.finish(True, False, timestamp)

        return True

    def on_motion_notify_event(self, widget, event):
        #self.queue_draw()
        return True

    def on_button_press(self, widget, event):
        self.zonewin = gtk.Window()
        self.zoneeditor = UI.ZoneEditor(self.zone)
        self.zonewin.add(self.zoneeditor.editor)
        self.zonewin.show_all()
        self.queue_draw()
        return True

    def on_button_release(self, widget, event):
        return True

    def on_expose(self, widget, event):
        size = widget.window.get_size()
        rect = gtk.gdk.Rectangle(0, 0, size[0], size[1])
        style = widget.get_style()

        if self.zone.sample != "":
            shadow_style = gtk.SHADOW_OUT
        else:
            shadow_style = gtk.SHADOW_IN

        style.paint_box(widget.window, gtk.STATE_NORMAL, shadow_style, rect, widget, "", 0, 0, rect.width, rect.height)

        # paint text 
        
        cr = widget.window.cairo_create()
        cr.set_font_size(8.0)
        cr.set_source_rgb(0.0, 0.0, 0.0)
        fascent, fdescent, fheight, fadvance, fyadvance = cr.font_extents()
        cr.move_to(2, ((size[1] / 2) - fdescent + fheight / 2))
        if self.zone.sample != "":
            cr.show_text(self.zone.sample)
            
        return False

class AkLabel(gtk.Label):
    def __init__(self, so, soattr, model, use_index = True):
        """
        TODO: ADD CONTEXT MENU TO CHANGE SAMPLE
        """
        gtk.Label.__init__(self, "sample")
        self.somodel = model
        self.init(so, soattr)
        
    def init(self, so, soattr):
        self.updating = True
        iter = None

        if soattr:
            self.soattr = soattr
            
        if so:
            self.so = so
        else:
            so = self.so

        if so:
            self.s = so.s
            self.so = so
            self.value = None

            if self.soattr:
                self.value = getattr(so, self.soattr)
                self.set_text(self.value)
                
        self.updating = False
        self.queue_draw()
        
class AkComboBox(gtk.ComboBox):
    def __init__(self, so, soattr, model, use_index = True):
        if type(model) is list:
            model = modelutils.get_model_from_list(model)

        gtk.ComboBox.__init__(self, model)

        #self.set_size_request(50, 25)

        cell = gtk.CellRendererText()
        self.use_index = use_index # use value, versus index
        self.pack_start(cell, False)
        self.add_attribute(cell, 'text', 0)  
        self.connect("changed", self.on_changed)
        self.somodel = model

        self.init(so, soattr)
        
    def init(self, so = None, soattr = None):
        self.updating = True
        iter = None

        if soattr:
            self.soattr = soattr
            
        if so:
            self.so = so
        else:
            so = self.so

        if so:
            self.s = so.s
            self.so = so
            self.value = None

            if self.soattr:
                self.value = getattr(so, self.soattr)
                if self.value != None:
                    if not self.use_index:
                        if len(self.value) > 0:
                            iter = self.find_iter(self.value)
                        if iter:
                            self.set_active_iter(iter)
                        elif len(self.value) > 0:
                            print "missing iter for", self.value, "model probably not initialized?"
                    elif self.use_index:
                        self.set_active(int(self.value))
                    else:
                        self.set_active(-1)

        self.updating = False
        self.queue_draw()

    def find_iter(self, value):
        iter = modelutils.search(self.somodel, self.somodel.iter_children(None), None, (0, value)) 
        return iter

    def get_text(self):
        iter = self.get_active_iter()
        value = self.somodel[iter][0]
        return value 
    
    def on_changed(self, widget):
        if not self.updating:
            active = self.get_active_iter()

            if self.use_index:
                value = self.get_active()
                self.so.set(self.soattr, value)
            else:
                value = self.somodel[active][0]
                self.so.set(self.soattr, value)

            self.value = value

    def on_expose(self, widget):
        return True

gobject.signal_new("slider_1_changed", AkRangeWidget, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,)) 
gobject.signal_new("slider_2_changed", AkRangeWidget, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,)) 
gobject.signal_new("value_changed", AkKnobWidget, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()) 
