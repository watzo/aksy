#!/usr/bin/env python
import psyco
psyco.full()

import os,os.path,re,logging,sys,struct,math,traceback,getopt,inspect
import types
import pygtk
pygtk.require('2.0')
import gtk,gtk.glade,gobject
import aksy

# our stuff
import utils,ak,UI

from postmod.itx import *

from aksy.device import Devices

__author__ = 'Joseph Misra'
__version__ = '0.71'

class UGivStderr:
    def __init__(self):
        self.win = gtk.Window()
        self.text = gtk.TextBuffer()
        self.textview = gtk.TextView(self.text)
        self.win.add(self.textview)

    def write(self, text):
        self.text.insert_at_cursor(text)
        self.win.show_all()

    def flush(self, text):
        self.text = ""

    def close(self, text):
        self.win.close()

class ZoneWindow(gtk.Window):
    def __init__(self, kg):
        gtk.Window.__init__(self)
        self.init(kg)

    def clear_children(self):
        for i in (self.get_children()):
            self.remove(i)

    def init(self, kg):
        self.kg = kg
        self.s = kg.s

        self.clear_children()

        zonevbox = gtk.VBox()

        for j in range(4):
            zone = kg.zones[j]
            #zonewidget = MiniZoneWidget(kg.zones[j])

            #zonewidget = AkComboBox(zone, "sample", z48.samplesmodel)
            zonehbox = gtk.HBox()

            zonecontrols = [
                UI.AkComboBox(zone, "sample", self.s.samplesmodel, False),
                UI.AkComboBox(zone, "output", utils.sampler_lists["output"]),
                UI.AkComboBox(zone, "keyboard_track", utils.sampler_lists["keyboard_track"]),
                UI.AkComboBox(zone, "playback", utils.sampler_lists["playback"]),
                UI.AkKnobWidget(zone, "level", -600, 60, 10, "db"),
                UI.AkKnobWidget(zone, "pan", 0, 100, 1, ""),
                UI.AkKnobWidget(zone, "filter", -100, 100, 1, ""),
                UI.AkKnobWidget(zone, "mod_start", -9999, 9999, 1, ""),
                UI.AkKnobWidget(zone, "tune", -3600, 3600, 100, ""),
                ]

            for zonecontrol in zonecontrols:
                zonehbox.pack_start(zonecontrol, False, False, 1)

            zonevbox.pack_start(zonehbox, False, False, 0)

        self.add(zonevbox)

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
            part = ak.Part(self.s, m, i)
        
            kghboxall = gtk.HBox()
            
            kghboxall.pack_start(UI.PartRangeWidget(part, "part_level"), False, False, 2)
            kghboxall.pack_start(UI.AkComboBox(part, "multi_part_name", self.s.programsmodel, False),False,False,2)
            kghboxall.pack_start(UI.AkComboBox(part, "part_output", utils.sampler_lists["output"], True),False,False,2)
            kghboxall.pack_start(UI.AkComboBox(part, "part_midi_channel", utils.sampler_lists["midi_channel"], True),False,False,2)
            
            self.pack_start(kghboxall, False, False, 2)
                def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)

class DrumEditorTable(gtk.Table):
    def __init__(self, s, p):
        self.dnd_list = [ ( 'text/uri-list', 0, 80 ) ] 
        gtk.Table.__init__(self, 32, 4, True) # 32 rows, 4 columns, homogenous
        self.s = s
        self.note_order = utils.midiutils.note_orders["mpc_banks_chromatic"] # chromatic / mpc_banks_gm / mpc_banks_chromatic
        self.on_toggled_callback = None
        
        self.setup(p)
        
        """
        chromatic = range(0,127)
        mpc gm
        
        mpc_chromatic = []
        for i in range(1,4):
            mpc_chromatic.extend(range(start_note + 16 * i, start_note)) # start note is what?
        """
    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp, kg, cb):
        self.s.FileChooser.on_drag_data_received(widget, context, x, y, selection, target_type, timestamp)
        # if it was a single selection, set that zone
        if len(self.s.FileChooser.files) > 0 and kg:
            first_file = os.path.basename(self.s.FileChooser.files[0])
            (filename, ext) = first_file.split(".")
            kg.zones[0].set("sample", filename)
        # hack, this should be updating rather than completely refreshing
        cb.set_model(self.s.samplesmodel)
        cb.somodel = self.s.samplesmodel
        cb.init()
        
    def setup(self, p):
        self.p = p
        self.no_keygroups = self.p.no_keygroups
        self.clear_widgets()
        rbg = None # radio button group
       
        for row in range(0,32):
            for column in range(0,4): 
                index = (row * 4) + column
                if index < len(self.note_order):
                    i = self.note_order[index]
                    kg = ak.Keygroup(p, i)
                    
                    tb = gtk.RadioButton(rbg, utils.midiutils.midinotes[i])
                    tb.connect("toggled", self.on_button_press_event, (i + 1)) 
                    
                    if not rbg:
                        rbg = tb
                        tb.set_active(True)
                    
                    vboxall = gtk.VBox()
                    vboxall.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)
                    kghboxall = gtk.HBox()
                    kghboxall.pack_start(tb, False, False, 1)
                    kghboxall.pack_start(UI.AkKnobWidget(kg, "level", -600, 60, 10, "db"), False, False, 2)
                    kghboxall.pack_start(UI.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""), False, False, 2)
                    vboxall.pack_start(kghboxall, False, False, 1)
                    cb = UI.AkComboBox(kg.zones[0], "sample", self.s.samplesmodel, False)
                    vboxall.connect("drag_data_received", self.on_drag_data_received, kg, cb)
                    vboxall.pack_start(cb, False, False, 1)
                    self.attach(vboxall,column,column+1,row,row+1)
        
    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)

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
            kg = ak.Keygroup(p, i)
            
            # TODO: Switch to a radio button.
            tb = gtk.RadioButton(rbg, str(i + 1))
            tb.connect("toggled", self.on_button_press_event, (i + 1))
            
            if not rbg:
                rbg = tb
                tb.set_active(True)
            
            kghboxall = gtk.HBox()
            
            kghboxall.pack_start(tb, False, False, 1)
            kghboxall.pack_start(UI.KeygroupRangeWidget(kg))
            #kghboxall.pack_start(UI.AkComboBox(kg.zones[0], "sample", self.s.samplesmodel, False))
            kghboxall.pack_start(UI.AkKnobWidget(kg, "level", -600, 60, 10, "db"), False, False, 2)
            kghboxall.pack_start(UI.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""), False, False, 2)
                        self.pack_start(kghboxall, False, False, 2)
            
    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)

    def on_button_press_event(self, widget, data = None):
        if self.on_toggled_callback:
            self.on_toggled_callback(widget, data)
        class KeygroupEditorWindow(gtk.Window):
    def __init__(self, z48, initial_program_name = None):
        gtk.Window.__init__(self)
        self.connect("configure_event", self.on_configure_event)
        self.connect("delete-event", self.on_delete_event)
        self.s = z48
        
        KeygroupEditorWindow.do_lists(self.s)
        
        self.zonewindow = None
        
        self.setup(initial_program_name)
        
    def setup(self, program_name):
        self.clear_widgets()
        
        if not program_name:
            program_name = "Program 1"
            
        p = ak.Program(self.s, program_name)

        self.no_keygroups = self.s.programtools.get_no_keygroups()

        #self.rangewidgets = []#

        vbox = gtk.VBox()

        dla = gtk.Button("DO LISTS AGAIN")
        dla.connect("clicked", self.do_lists_again)
        vbox.pack_start(dla)

        for i in range(self.no_keygroups):
            kg = ak.Keygroup(p, i)
            tb = gtk.Button(str(i + 1))
            tb.connect("clicked", self.on_button_press_event)

            setattr(tb, "index", i)
            setattr(tb, "program", p)

            kghboxall = gtk.HBox()

            kghboxall.pack_start(tb, False, False, 1)

            kghboxall.pack_start(UI.KeygroupRangeWidget(kg))
            kghboxall.pack_start(UI.AkKnobWidget(kg, "level", -600, 60, 10, "db"), False, False, 2)
            kghboxall.pack_start(UI.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""), False, False, 2)

            kghboxall.pack_start(UI.AkComboBox(kg, "filter", utils.sampler_lists["filter"]), False, False, 2)
            kghboxall.pack_start(UI.AkComboBox(kg, "filter_attenuation", utils.sampler_lists["filter_attenuation"]), False, False, 2)
            kghboxall.pack_start(UI.AkKnobWidget(kg, "filter_cutoff", 0, 100, 1, ""), False, False, 1)
            kghboxall.pack_start(UI.AkKnobWidget(kg, "filter_resonance", 0, 100, 1, ""), False, False, 1)

            vbox.pack_start(kghboxall, False, False, 2)

        self.add(vbox)    

        self.init_zonewindow(p, 0)

    def do_lists_again(self, widget):
        KeygroupEditorWindow.do_lists(self.s)

    def on_button_press_event(self, widget):
        if type(widget) is gtk.Button:
            self.init_zonewindow(widget.program, widget.index)

    def init_zonewindow(self, program, index):
        kg = ak.Keygroup(program, index)
        if not self.zonewindow or index != self.zonewindow.kg.index:
            if self.zonewindow:
                self.zonewindow.hide()
            else:
                self.zonewindow = ZoneWindow(kg)

            self.zonewindow.init(kg)
            self.move_zonewindow()
            self.zonewindow.show_all()
            
    def clear_widgets(self):
        for child in self.get_children():
            self.remove(child)
        if self.zonewindow:
            self.zonewindow = None
    
    def move_zonewindow(self):
        position = self.get_position()
        size = self.get_size()
        decoration_width = 10
        self.zonewindow.move(position[0] + size[0] + decoration_width, position[1])

    def on_configure_event(self, widget, event):
        self.move_zonewindow()
        return False
    
    def on_delete_event(self, widget, event):
        # no, please!
        self.hide_all()
        self.zonewindow.hide_all()
        return True

    @staticmethod
    def do_lists(s):
        setattr(s,'samples',s.sampletools.get_names())
        setattr(s,'programs',s.programtools.get_names())
        setattr(s,'multis',s.multitools.get_names())

        setattr(s,'samplesmodel',utils.get_model_from_list(s.samples, True))
        setattr(s,'programsmodel',utils.get_model_from_list(s.programs))
        setattr(s,'multismodel',utils.get_model_from_list(s.multis))

def main(): 
    z48 = Devices.get_instance("z48", "usb")
    win = KeygroupEditorWindow(z48)
    win.show_all()
    win.connect("delete-event", gtk.main_quit)
    gtk.main()

if __name__ == "__main__":
    log = logging.getLogger("aksy")
    #sys.stdout = UGivStderr()
	#import hotshot, hotshot.stats
    #prof = hotshot.Profile("ak.py.prof")
    #prof.runcall(main)
    main()
