#!/usr/bin/env python
import psyco
psyco.full()
import hotshot, hotshot.stats

import os,os.path,re,logging,sys,struct,math,traceback,getopt,inspect
import types
import pygtk
pygtk.require('2.0')
import gtk,gtk.glade,gobject
import aksy

# our stuff
import utils, postmod

from ak import *
from UI import *

from utils.modelutils import *
from utils.midiutils import *

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
                AkComboBox(zone, "sample", self.s.samplesmodel, False),
                AkComboBox(zone, "output", sampler_items["output"]),
                AkComboBox(zone, "keyboard_track", sampler_items["keyboard_track"]),
                AkComboBox(zone, "playback", sampler_items["playback"]),
                AkKnobWidget(zone, "level", -600, 60, 10, "db"),
                AkKnobWidget(zone, "pan", 0, 100, 1, ""),
                AkKnobWidget(zone, "filter", -100, 100, 1, ""),
                AkKnobWidget(zone, "mod_start", -9999, 9999, 1, ""),
                AkKnobWidget(zone, "tune", -3600, 3600, 100, ""),
                ]

            for zonecontrol in zonecontrols:
                zonehbox.pack_start(zonecontrol, False, False, 1)

            zonevbox.pack_start(zonehbox, False, False, 0)

        self.add(zonevbox)

class Main3Window(gtk.Window):
    def __init__(self, z48):
        gtk.Window.__init__(self)
        self.connect("configure_event", self.on_configure_event)
        Main3Window.do_lists(z48)

        self.s = z48

        p = program(z48, "Program 1")
        p.update()

        no_keygroups = z48.programtools.get_no_keygroups()

        rangewidgets = []#

        self.zonewindow = None

        vbox = gtk.VBox()

        dla = gtk.Button("DO LISTS AGAIN")
        dla.connect("clicked", self.do_lists_again)
        vbox.pack_start(dla)

        for i in range(no_keygroups):
            kg = keygroup(p, i)
            kg.update()
            tb = gtk.Button(str(i + 1))
            tb.connect("clicked", self.on_button_press_event)

            setattr(tb, "index", i)
            setattr(tb, "program", p)

            kghboxall = gtk.HBox()

            kghboxall.pack_start(tb, False, False, 1)

            kghboxall.pack_start(KeygroupRangeWidget(kg))
            kghboxall.pack_start(AkKnobWidget(kg, "level", -600, 60, 10, "db"), False, False, 2)
            kghboxall.pack_start(AkKnobWidget(kg, "tune", -3600, 3600, 100, ""), False, False, 2)

            kghboxall.pack_start(AkComboBox(kg, "filter", sampler_items["filter"]), False, False, 2)
            kghboxall.pack_start(AkComboBox(kg, "filter_attenuation", sampler_items["filter_attenuation"]), False, False, 2)
            kghboxall.pack_start(AkKnobWidget(kg, "filter_cutoff", 0, 100, 1, ""), False, False, 1)
            kghboxall.pack_start(AkKnobWidget(kg, "filter_resonance", 0, 100, 1, ""), False, False, 1)

            vbox.pack_start(kghboxall, False, False, 2)

        self.add(vbox)    

        self.init_zonewindow(p, 0)

    def do_lists_again(self, widget):
        Main3Window.do_lists(self.s)

    def on_button_press_event(self, widget):
        if type(widget) is gtk.Button:
            self.init_zonewindow(widget.program, widget.index)

    def init_zonewindow(self, program, index):
        kg = keygroup(program, index)
        if not self.zonewindow or index != self.zonewindow.kg.index:
            if self.zonewindow:
                self.zonewindow.hide()
            else:
                self.zonewindow = ZoneWindow(kg)

            self.zonewindow.init(kg)
            self.move_zonewindow()
            self.zonewindow.show_all()

    def move_zonewindow(self):
        position = self.get_position()
        size = self.get_size()
        decoration_width = 10
        self.zonewindow.move(position[0] + size[0] + decoration_width, position[1])

    def on_configure_event(self, widget, event):
        self.move_zonewindow()
        return False

    @staticmethod
    def do_lists(s):
        setattr(s,'samples',s.sampletools.get_names())
        setattr(s,'programs',s.programtools.get_names())
        setattr(s,'multis',s.multitools.get_names())

        setattr(s,'samplesmodel',get_model_from_list(s.samples, True))
        setattr(s,'programsmodel',get_model_from_list(s.programs))
        setattr(s,'multismodel',get_model_from_list(s.multis))

def main(): 
    z48 = Devices.get_instance("z48", "usb")
    win = Main3Window(z48)
    win.show_all()
    win.connect("delete-event", gtk.main_quit)
    gtk.main()

if __name__ == "__main__":
    log = logging.getLogger("aksy")
    #sys.stdout = UGivStderr()
    #prof = hotshot.Profile("ak.py.prof")
    #prof.runcall(main)
    main()
