#!/usr/bin/env python
import gtk

import os.path

# our stuff
from aksui.utils import midiutils, modelutils
from aksui.ak import envelope, keygroup, part

import rangewidget

__author__ = 'Joseph Misra'
__version__ = '0.71'

class EnvelopeHBox(gtk.HBox):
    def __init__(self, kg, index):
        gtk.HBox.__init__(self)
        self.s = kg.s
        self.setup(kg, index)

    def setup(self, kg, index):
        self.e = envelope.Envelope(kg, index)
        
        self.clear_widgets()
        
        if index == 0:
            # amp envelope is simpler
            knobs = ['rate1','rate2','level2','rate3']
            self.e.abbr['envelope_rate1'] = 'A'
            self.e.abbr['envelope_rate2'] = 'D'
            self.e.abbr['envelope_level2'] = 'S'
            self.e.abbr['envelope_rate3'] = 'R'
        else:
            knobs = ['rate1','level1','rate2','level2','rate3','level3','rate4','level4','reference']
            
        for knob_name in knobs:
            knob = rangewidget.AkKnobWidget(self.e, 'envelope_' + knob_name, 0, 100, 1, None)
            self.pack_start(knob, False, False, 2)
            
    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)
            
class MultiEditorVBox(gtk.VBox):
    """
    Minimal multi editor VBox
    """
    def __init__(self, s, m):
        gtk.VBox.__init__(self)
        self.s = s
        #self.connect("delete-event", self.on_delete_event)
        self.setup(m)
    
    def setup(self, m):
        self.m = m
        
        self.no_parts = self.m.no_parts
        
        self.clear_widgets()
        
        for i in range(self.no_parts):
            p = part.Part(self.s, m, i)
        
            kghboxall = gtk.HBox()
            
            kghboxall.pack_start(rangewidget.AkComboBox(p, "multi_part_name", self.s.programsmodel, False),True,True,2)
            kghboxall.pack_start(rangewidget.PartRangeWidget(p, "part_level"), True, True, 2)
            kghboxall.pack_start(rangewidget.AkKnobWidget(p, "part_pan", 0, 100, 1, None), False, False, 2)
            kghboxall.pack_start(rangewidget.AkComboBox(p, "part_output", midiutils.sampler_lists["output"], True),True,True,2)
            kghboxall.pack_start(rangewidget.AkComboBox(p, "part_midi_channel", midiutils.sampler_lists["midi_channel"], True),True,True,2)
            
            self.pack_start(kghboxall, False, False, 2)

    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)

class DrumEditorTable(gtk.Table):
    def __init__(self, s, p):
        self.dnd_list = [ ( 'text/uri-list', 0, 80 ) ] 
        self.columns = 4
        self.note_order = midiutils.note_orders["mpc_banks_gm"] # chromatic / mpc_banks_gm / mpc_banks_chromatic
        gtk.Table.__init__(self, (len(self.note_order) / self.columns), self.columns, True) # 32 rows, 4 columns, homogenous
        self.s = s
        self.on_toggled_callback = None
        
        self.setup(p)

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp, kg, cb, zone_index):
        self.s.FileChooser.on_drag_data_received(widget, context, x, y, selection, target_type, timestamp)
        # if it was a single selection, set that zone
        if len(self.s.FileChooser.files) > 0 and kg:
            first_file = os.path.basename(self.s.FileChooser.files[0])
            (filename, ext) = first_file.split(".")
            kg.zones[zone_index].set("sample", filename)
        # hack, this should be updating rather than completely refreshing
        cb.set_model(self.s.samplesmodel)
        cb.somodel = self.s.samplesmodel
        cb.init()
        
    def setup(self, p):
        self.p = p
        self.no_keygroups = self.p.no_keygroups
        self.clear_widgets()
        rbg = None # radio button group
       
        self.zone_labels = {}
        for row in range(0,(len(self.note_order) / self.columns)):
            for column in range(0,self.columns): 
                index = (row * self.columns) + column
                if index < len(self.note_order):
                    i = self.note_order[index]
                    kg = keygroup.get_keygroup_cached(p, i)
                    desc = midiutils.midinotes[i]
                    tb = gtk.RadioButton(rbg)
                    tb.connect("toggled", self.on_button_press_event, kg.index + 1) 

                    if i in midiutils.gm1drumsmap.keys():
                        subdesc = midiutils.gm1drumsmap[i]
                        # general midi markup label
                        subdesclabel = gtk.Label("<span size='smaller'>%s %s</span>" % (desc, subdesc))
                        subdesclabel.set_use_markup(True)
                    else:
                        subdesclabel = gtk.Label("<span size='smaller'>%s</span>" % (desc))
                        subdesclabel.set_use_markup(True)
                    
                    if not rbg:
                        rbg = tb
                        tb.set_active(True)
                    
                    vboxall = gtk.VBox()
                    kghboxall = gtk.HBox()
                    kghboxall.pack_start(tb, False, False, 1)
                    if subdesclabel:
                        kghboxall.pack_start(subdesclabel, False, False, 0)
                    #Dunno if these are really necessary - removing to save space.
                    #kghboxall.pack_start(rangewidget.AkKnobWidget(kg, "level", -600, 60, 10, "db"), False, False, 2)
                    #kghboxall.pack_start(rangewidget.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""), False, False, 2)
                    vboxall.pack_start(kghboxall, False, False, 1)
                    eventbox = gtk.EventBox()
                    eventbox.connect("button_press_event", self.on_label_click, tb)
                    eventbox.set_events(gtk.gdk.BUTTON_PRESS_MASK)
                    zone_vbox = gtk.VBox(False, 0)
                    self.zone_labels[i] = []
                    for zone_index in range(4):
                        zone_label = rangewidget.AkLabel(kg.zones[zone_index], "sample", self.s.samplesmodel, False)
                        zone_label.set_justify(gtk.JUSTIFY_LEFT)
                        self.zone_labels[i].append(zone_label)
                        zone_label.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)
                        zone_label.connect("drag_data_received", self.on_drag_data_received, kg, zone_label, zone_index)
                        zone_vbox.pack_start(zone_label, False, False, 0)
                    vboxall.pack_start(zone_vbox, False, False, 0)
                    eventbox.add(vboxall)
                    self.attach(eventbox,column,column+1,row,row+1)

    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)

    def on_label_click(self, widget, e, toggle):
        toggle.set_active(True)

    def on_button_press_event(self, widget, data = None):
        if self.on_toggled_callback:
            self.on_toggled_callback(widget, data)

class KeygroupEditorVBox(gtk.VBox):
    """
    Minimal keygroup editor VBox
    """
    def __init__(self, s, p):
        gtk.VBox.__init__(self)
        self.s = s
        #self.connect("delete-event", self.on_delete_event)
        self.setup(p)
        self.on_toggled_callback = None

    def setup(self, p):
        self.p = p
        
        self.no_keygroups = self.p.no_keygroups
        
        self.clear_widgets()
        rbg = None # radio button group

        for i in range(self.no_keygroups):
            kg = keygroup.get_keygroup_cached(p, i)
            
            # TODO: Switch to a radio button.
            tb = gtk.RadioButton(rbg, str(i + 1))
            tb.connect("toggled", self.on_button_press_event, (i + 1))
            
            if not rbg:
                rbg = tb
                tb.set_active(True)
            
            kghboxall = gtk.HBox()
            
            kghboxall.pack_start(tb, False, False, 1)
            kghboxall.pack_start(rangewidget.KeygroupRangeWidget(kg))
            #kghboxall.pack_start(rangewidget.AkComboBox(kg.zones[0], "sample", self.s.samplesmodel, False))
            kghboxall.pack_start(rangewidget.AkKnobWidget(kg, "level", -600, 60, 10, "db"), False, False, 2)
            kghboxall.pack_start(rangewidget.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""), False, False, 2)
            self.pack_start(kghboxall, False, False, 2)
            
    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)

    def on_button_press_event(self, widget, data = None):
        if self.on_toggled_callback:
            self.on_toggled_callback(widget, data)
