#!/usr/bin/env python
import psyco
psyco.full()

try:
    import hotshot, hotshot.stats
except ImportError:
    print "Profiler not available"

import os,os.path,re,logging,sys,struct,math,traceback
import pygtk
pygtk.require('2.0')
import gtk,gtk.glade,gobject
import aksy

# our stuff
import ak, UI, utils, postmod

from utils.modelutils import *
from utils.midiutils import *

from postmod.itx import *

from aksy.device import Devices

__author__ = 'Joseph Misra'
__version__ = '0.45'
def get_selected_from_treeview(treeview):
    """
    will return a single value or a list depending on what the selection mode is
    """
    selection = treeview.get_selection()
    if selection.get_mode() == gtk.SELECTION_MULTIPLE:
        (model, pathlist) = selection.get_selected_rows()
        result = []
        for path in pathlist:
            result.append(model[path][0])
        return result
    else:
        (model, iter) = selection.get_selected()
        return model[iter][0] 

# exception handler ripped from austin's code 
def exceptionHandler(type, value, tback):    
    try:
        print ""
        print "-- Initialization Exception --"
        tbmessage = "Type: " + str(type) + "\nValue: " + str(value) + "\nData:\n"
        tblist = traceback.extract_tb(tback)
        for x in tblist:
            tbmessage = tbmessage + str(x) + "\n"
        print "Error Code:", tbmessage
        
    except:
        traceback.print_exc()

    return 0


class DialogCreateNewKeygroups(UI.base):
    def __init__(self, parent):
        self.s = parent.s
        self.programname = None

        UI.base.__init__(self, None, "dialogCreateNewKeygroups")

    def on_cancelbutton_clicked(self, widget):
        self.editor.response(gtk.RESPONSE_CANCEL)
        self.editor.hide()

    def on_okbutton_clicked(self, widget):
        self.editor.response(gtk.RESPONSE_OK)
        self.editor.hide()

    def set_program(self, programname):
        self.programname = programname
        if type(programname) is list:
            caption_name = ' '.join(programname)
        else:
            caption_name = programname

        self.w_label_create_new.set_label("Create new keygroups on: " + caption_name)

class DialogCreateNewProgramFast(UI.base):
    def __init__(self, parent):
        self.s = parent.s
        self.programname = None

        UI.base.__init__(self, None, "dialogCreateNewProgramFast")
    
class SamplesContextMenu(UI.base):
    """Context menu for the "samples" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        UI.base.__init__(self, None, "menuSamples")

        self.dialogCreateNewProgramFast = DialogCreateNewProgramFast(self)
        self.dialogCreateNewProgramFast.w_combo_starting_note.set_model(midinotesmodel)
        self.dialogCreateNewProgramFast.w_combo_starting_note.set_active(0)

    def on_new_program_activate(self, widget):
        selected_samples = get_selected_from_treeview(self.main.w_treeview_samples)
        self.dialogCreateNewProgramFast.w_treeview_selected_samples.set_model(get_model_from_list(selected_samples))

        response = self.dialogCreateNewProgramFast.editor.run()

        if response == gtk.RESPONSE_OK:
            program_name = self.dialogCreateNewProgramFast.w_entry_program_name.get_text()
            # create program
            # figure out note ranges
            # iterate over notes and set up keygroups
            # set keygroup low note and high note and zone 1 sample
            method = self.dialogCreateNewProgramFast.w_combo_allocate_method.get_active()
            starting_note = self.dialogCreateNewProgramFast.w_combo_starting_note.get_active()
            type = self.dialogCreateNewProgramFast.w_combo_program_type.get_active()
            num_samples = len(selected_samples)
            notes = []
            if method == 0:
                # chromatic
                for i in range(starting_note,starting_note+num_samples):
                    notes.append([i, i])
                keytrack = 1
                playback = 0
            elif method == 1:
                # drum
                for i in range(num_samples):
                    notes.append([mpcpads[i],mpcpads[i]])
                keytrack = 0
                # one shot
                playback = 1
            elif method == 2:
                # span
                for i in range(num_samples):
                    notes.append([0,127])
                keytrack = 1
                playback = 0

            self.s.programtools.create_new(len(selected_samples), program_name)
            self.s.programtools.set_curr_by_name(program_name)

            if type == 1:
                # drum program
                print "setting drum type"
                self.s.programtools.set_type(1)

            for i in range(num_samples):
                print "adding", i, notes[i][0], notes[i][1], selected_samples[i]
                if type == 0:
                    self.s.keygrouptools.set_curr_keygroup(i)
                    print "set note range"
                    self.s.keygrouptools.set_low_note(notes[i][0])
                    self.s.keygrouptools.set_high_note(notes[i][1])
                else:
                    self.s.keygrouptools.set_curr_keygroup(notes[i][0])
                    
                print "set zone stuff"
                self.s.zonetools.set_keyboard_track(1, keytrack)
                self.s.zonetools.set_playback(1, playback)

                print "set sample"
                self.s.zonetools.set_sample(1, selected_samples[i])
                #self.s.programtools.add_keygroup_sample(notes[i][0],notes[i][1],1,keytrack,selected_samples[i])

        self.dialogCreateNewProgramFast.editor.hide()

class ProgramsContextMenu(UI.base):
    """Context menu for the "programs" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        UI.base.__init__(self, None, "menuPrograms")

        self.dialogCreateNewKeygroups = DialogCreateNewKeygroups(self)

    def on_add_keygroup_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)

        self.dialogCreateNewKeygroups.set_program(programname)

        response = self.dialogCreateNewKeygroups.editor.run()

        if response == gtk.RESPONSE_OK:
            howmany = int(self.dialogCreateNewKeygroups.w_spin_howmany_keygroups.get_value())

            if not (type(programname) is list):
                programname = [programname,]

            for pn in programname:
                print "Adding ", howmany, "keygroups to", pn
                self.program = ak.program(self.s,pn)
                self.program.gettools().add_keygroups_to_current(howmany)

    def on_dump_matrix(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        if not (type(programname) is list):
            programname = [programname,]

        for pn in programname:
            program = ak.program(self.s,pn)
            program.dump_matrix()

    def on_set_current_program_activate(self, widget):
        print "set current program"



class Main(UI.base):
    """Main Window
    """
    def __init__(self, s):
        self.s = s
        UI.base.__init__(self, None, "vboxMain")

        setattr(self.s,'filechooser', UI.filechooser(s))

        self.w_treeview_multis.append_column(gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0))
        self.w_treeview_multis.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.w_treeview_programs.append_column(gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0))
        self.w_treeview_programs.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.w_treeview_samples.append_column(gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0))
        self.w_treeview_samples.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        self.ProgramsContextMenu = ProgramsContextMenu(self) 
        self.SamplesContextMenu = SamplesContextMenu(self) 

        self.w_quit1.connect('activate', gtk.main_quit)

        self.init_lists()

        self.programsEditor = UI.ProgramsEditor(self.s)

        self.on_update_models(None)

    @staticmethod
    def do_lists(s):
        setattr(s,'samples',s.sampletools.get_names())
        setattr(s,'programs',s.programtools.get_names())
        setattr(s,'multis',s.multitools.get_names())

        setattr(s,'samplesmodel',get_model_from_list(s.samples, True))
        setattr(s,'programsmodel',get_model_from_list(s.programs))
        setattr(s,'multismodel',get_model_from_list(s.multis))

    def init_lists(self):
        try:
            Main.do_lists(self.s)
            self.s.samplesmodel.connect("row-changed", self.on_update_models)
            self.s.programsmodel.connect("row-changed", self.on_update_models)
            self.s.multismodel.connect("row-changed", self.on_update_models)

            self.on_update_models(None)
        except Exception, ex:
            print ex

    def on_refresh_clicked(self, widget):
        self.init_lists()

    def on_update_models(self, model, iter = None, user_param = None):
        self.w_treeview_programs.set_model(self.s.programsmodel)
        self.w_treeview_multis.set_model(self.s.multismodel)
        self.w_treeview_samples.set_model(self.s.samplesmodel)

    def get_curr_programname(self):
        selection = self.w_treeview_programs.get_selection()

        model, iter = selection.get_selected()
        programname = model[iter][0]
        return programname

    def on_program_editor_activate(self, button):
        self.programsEditor.programsMain.show_all()

    def on_upload_activate(self, button):
        self.s.filechooser.open(upload=True)

    def on_lcd_activate(self, button):
        lcd = UI.LCDScreen(self.s)
        win = gtk.Window()
        win.add(lcd)
        win.show_all()

    def on_import_from_it(self, button):
        """Displays a filechooser and then attempts to import samples from the .IT module.
        """

        self.filechooser = UI.filechooser(self.s)
        self.filechooser.setup_filter(["IT"])

        files = self.filechooser.open()
        for fn in files:
            it = ITX(fn)

            print fn, "loaded! exporting..."

            exported_files = it.exportSamples("/tmp")

            print exported_files

            for exported_file in exported_files:
                # TODO: verify file format is ok
                print "Uploading: ", exported_file
                self.filechooser.upload(exported_file)

    def on_treeview_event(self, widget, event):
        """Handles context menus + doubleclicks.
        """

        if widget == self.w_treeview_programs:
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                self.ProgramsContextMenu.editor.popup(None, None, None, event.button, event.time)

            if event.type == gtk.gdk._2BUTTON_PRESS:
                curr_program = get_selected_from_treeview(self.w_treeview_programs)

                if type(curr_program) is list:
                    curr_program = curr_program[0]

                self.programsEditor.set_program(curr_program)
                self.programsEditor.programsMain.show_all()

        if widget == self.w_treeview_samples:
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                self.SamplesContextMenu.editor.popup(None, None, None, event.button, event.time)
                return True

    @staticmethod
    def test_programsEditor():
        z48 = Devices.get_instance("z48", "usb")
        Main.do_lists(z48)
        programsEditor = UI.ProgramsEditor(z48)
        programsEditor.programsMain.show_all()
        programsEditor.programsMain.connect("delete-event", gtk.main_quit)
        gtk.main()


z48 = None
log = None
sys.excepthook = exceptionHandler

def main(): 
    z48 = Devices.get_instance("z48", "usb")
    try:
       m = Main(z48)
       win = gtk.Window()
       win.add(m.editor)
       win.show_all()
       win.connect("delete-event", gtk.main_quit)
       gtk.main()
    finally:
        z48.close()

if __name__ == "__main__":
    log = logging.getLogger("aksy")

    prof = hotshot.Profile("ak.py.prof")
    prof.runcall(main)
    """
    stats = hotshot.stats.load("ak.py.prof")
    stats.strip_dirs()
    stats.sort_stats("cumtime")
    stats.print_stats(20)
    """
