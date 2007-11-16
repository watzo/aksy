#!/usr/bin/env python
#import hotshot, hotshot.stats
import os,os.path,re,logging,sys,struct,math,traceback,getopt,inspect
import types
import pygtk
pygtk.require('2.0')
import gtk,gtk.glade,gobject
import aksy

# our stuff

from ak import *
from ak.samplerobject import *
from UI import *

from utils import midiutils, modelutils

from postmod.itx import *

from aksy.device import Devices

__author__ = 'Joseph Misra'
__version__ = '0.01'


class CellRendererSamplerObject(gtk.GenericCellRenderer):
    __gproperties__ = {
            "samplerobject": (object, "samplerobject", "samplerobject", gobject.PARAM_READWRITE),
    }

    def __init__(self, s):
        self.__gobject_init__()
        gtk.GenericCellRenderer.__init__(self)
        self.s = s
        self.custom = None
        self.widget_type = None

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def on_render(self, window, widget, background_area, cell_area, expose_area, flags):
        if self.custom:
            return self.custom.draw(window, widget, cell_area)
        else:
            return False

    def on_get_size(self, widget, cell_area):
        if self.custom:
            return (0,0,15,30) 
        else:
            return (0,0,0,0)

    def on_activate(event, widget, path, background_area, cell_area, flags):
        return

    def on_start_editing(event, widget, path, background_area, cell_area, flags):
        return

class CellRendererKnob(CellRendererSamplerObject):
    def __init__(self, s):
        CellRendererSamplerObject.__init__(self, s)

    def do_set_property(self, pspec, value):
        if pspec.name == "samplerobject" and not self.custom:
            self.custom = AkKnobWidget(value, "level", -600, 60, 10, "db", "AMPLITUDE")

        setattr(self, pspec.name, value)

gobject.type_register(CellRendererSamplerObject)

# create a window an add a treeview
# build model to hold program -> keygroup -> samples


class MainProgramsWindow(MainWindow):
    def __init__(self, z48):
        gtk.Window.__init__(self)
        self.set_title("ak.py")
        self.s = z48
        self.iter_dict = {}

        self.treeview = gtk.TreeView()

        self.connect("configure_event", self.on_configure_event)

        self.init()

    def build_model(self):
        self.treestore = gtk.TreeStore(str, str, object) 
        
        for program_info in self.s.programs:
            program_handle, program_name = program_info 
            p = ak.program(self.s,program_name)
            program_iter = self.treestore.append(None,[program_name,'',p])
            no_keygroups = self.s.programtools.get_no_keygroups()
            self.iter_dict[self.treestore.get_string_from_iter(program_iter)] = p
            for i in range(no_keygroups):
                kg = ak.keygroup(p,i)
                keygroup_iter = self.treestore.append(program_iter,['Keygroup ' + str(i), "--------", kg])
                self.iter_dict[self.treestore.get_string_from_iter(keygroup_iter)] = kg
                for j in range(4):
                    z = ak.zone(kg, j+1)
                    zone_iter = self.treestore.append(keygroup_iter,['Zone ' + str(j+1), z.sample, z])
                    self.iter_dict[self.treestore.get_string_from_iter(zone_iter)] = z

        return self.treestore

    def init(self):
        # based on list build TreeView
        MainProgramsWindow.do_lists(self.s)
        #self.lcd = UI.LCDScreen(self.s)

        self.xml = gtk.glade.XML("menu.glade", "mainmenu")
        self.mainmenu = self.xml.get_widget("mainmenu")
        self.xml.signal_autoconnect(self)

        self.set_size_request(500,500)

        vbox = gtk.VBox(False,0)
        vbox.pack_start(self.mainmenu)
        vbox.set_child_packing(self.mainmenu, False, True, 0, gtk.PACK_START)

        self.hpaned = gtk.HPaned()
        self.hpaned.set_position(250)
        self.scrolledwindow = gtk.ScrolledWindow()
        self.treestore = self.build_model()
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.connect("button_press_event", self.on_treeview_button_press_event)
        self.treeview.connect("button_release_event", self.on_treeview_button_release_event)
        self.treeview.connect("motion_notify_event", self.on_treeview_motion_notify_event)

        textedit = gtk.CellRendererText()
        textedit.set_property('editable', False)
        textedit.connect('edited', self.on_textedit_changed, (self.treestore, 0))

        sampleedit = gtk.CellRendererCombo()
        sampleedit.set_property('editable', True)
        sampleedit.set_property('model', self.s.samplesmodel)
        sampleedit.set_property('text-column', 1)
        sampleedit.connect('edited', self.on_sampleedit_changed, (self.treestore, 1))
        sampleedit.connect('editing-started', self.on_sampleedit_started)

        leveledit = CellRendererKnob(self.s)
        """
        tuneedit = gtk.GenericCellRenderer()
        panedit = gtk.GenericCellRenderer()
        filteredit = gtk.GenericCellRenderer()
        """

        self.treeview.append_column(gtk.TreeViewColumn("Name", textedit, text=0))
        self.treeview.append_column(gtk.TreeViewColumn("Sample", sampleedit, text=1))
        self.treeview.append_column(gtk.TreeViewColumn("Level", leveledit, samplerobject=2))
        """
        self.treeview.append_column(gtk.TreeViewColumn("Tune", tuneedit))
        self.treeview.append_column(gtk.TreeViewColumn("Pan", panedit))
        self.treeview.append_column(gtk.TreeViewColumn("Filter", filteredit))
        """

        self.scrolledwindow.add(self.treeview)
        self.hpaned.add1(self.scrolledwindow)
        self.hpaned.add2(gtk.DrawingArea())
        vbox.pack_start(self.hpaned)
        self.add(vbox)

        self.queue_draw()
        self.show_all()

    def call_cell_func(self, widget, event, which):
        result = self.treeview.get_path_at_pos(int(event.x), int(event.y))

        if result:
            path, column, x, y = result

            renderers = column.get_cell_renderers() 

            area = self.treeview.get_cell_area(path, column)

            if area.height > 0:
                #print path, event.x, event.y, area.x, area.y, area.width, area.height

                e = event.copy()
                e.x = event.x - float(area.x)
                e.y = event.y - float(area.y)

                for renderer in renderers:
                    if type(renderer) is CellRendererKnob:
                        if which == "on_button_press":
                            renderer.custom.on_button_press(widget, e)
                        elif which == "on_motion_notify":
                            renderer.custom.on_motion_notify_event(widget, e)
                        elif which == "on_button_release":
                            renderer.custom.on_button_release(widget, e)

        self.treeview.queue_draw()
        return False

    def on_treeview_motion_notify_event(self, widget, event):
        self.call_cell_func(widget, event, "on_motion_notify")
        return False

    def on_treeview_button_press_event(self, widget, event):
        self.call_cell_func(widget, event, "on_button_press")
        return False

    def on_treeview_button_release_event(self, widget, event):
        self.call_cell_func(widget, event, "on_button_release")
        return False

    def on_sampleedit_started(self, cell, editable, path):
        if not self.treestore[path][0].startswith('Zone'):
            cell.stop_editing(True)
            return True

    def on_sampleedit_changed(self, cell, path, new_text, user_data):
        model, index = user_data
        model[path][index] = new_text
        if path in self.iter_dict:
            so = self.iter_dict[path]
            if type(so) is ak.zone:
                so.set("sample", new_text)
        else:
            print "cant find", path, "in dict"
        return 

    def on_textedit_changed(self, cell, path, new_text, user_data):
        model, index = user_data
        model[path][index] = new_text
        return 

    @staticmethod
    def do_list_helper(tools):
        samples = []
        samples_tmp = tools.get_handles_names()

        i = 0

        while i < (len(samples_tmp)):
            samples.append([samples_tmp[i],samples_tmp[(i+1)]]) 
            i += 2 

        return samples

    @staticmethod
    def do_lists(s):
        samples = MainProgramsWindow.do_list_helper(s.sampletools)
        programs = MainProgramsWindow.do_list_helper(s.programtools)
        multis = MainProgramsWindow.do_list_helper(s.multitools)

        setattr(s,'samples',samples)
        setattr(s,'programs',programs)
        setattr(s,'multis',multis)

        if len(s.samples) == 0:
            print "No samples..."

        if len(s.programs) == 0:
            print "No programs..."

        if len(s.multis) == 0:
            print "No multis..."

        setattr(s,'samplesmodel', modelutils.get_model_from_list(s.samples))
        setattr(s,'programsmodel', modelutils.get_model_from_list(s.programs))
        setattr(s,'multismodel', modelutils.get_model_from_list(s.multis))

    def on_configure_event(self, widget, event):
        return False


def main(): 
    z48 = Devices.get_instance("z48", "usb")
    #z48 = None
    win = MainProgramsWindow(z48)
    win.connect("delete-event", gtk.main_quit)
    gtk.main()

if __name__ == "__main__":
    prof = hotshot.Profile("ak.py.prof")
    prof.runcall(main)
    stats = hotshot.stats.load("ak.py.prof")
    stats.sort_stats('time', 'calls')
    stats.print_stats(10)


