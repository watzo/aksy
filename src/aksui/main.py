#!/usr/bin/env python
import psyco
psyco.full()

try:
    import hotshot, hotshot.stats
except ImportError:
    print "Profiler not available"

import pygtk
pygtk.require('2.0')
import gtk
import aksy
import shutil

# our stuff
import ak, UI, utils, postmod

from utils import *

from postmod.itx import *

from aksy.device import Devices

__author__ = 'Joseph Misra and Walco van Loon'
__version__ = '0.713'


# config
USE_CUSTOM_EXCEPTHOOK = False # this gets in the way of eclipse's handy exception line # link feature, could probably fix later
ENABLE_PROFILER = False
TARGET_TYPE_URI_LIST = 80



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


class DialogCreateNewKeygroups(UI.Base):
    def __init__(self, parent):
        self.s = parent.s
        self.programname = None

        UI.Base.__init__(self, None, "dialogCreateNewKeygroups")

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

class DialogCreateNewProgramFast(UI.Base):
    def __init__(self, parent):
        self.s = parent.s
        self.programname = None

        UI.Base.__init__(self, None, "dialogCreateNewProgramFast")
    
class SamplesContextMenu(UI.Base):
    """Context menu for the "samples" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        UI.Base.__init__(self, None, "menuSamples")

        self.dialogCreateNewProgramFast = DialogCreateNewProgramFast(self)
        self.dialogCreateNewProgramFast.w_combo_starting_note.set_model(midinotesmodel)
        self.dialogCreateNewProgramFast.w_combo_starting_note.set_active(0)

    def on_delete_sample_activate(self, widget):
        selected_samples = get_selected_from_treeview(self.main.w_treeview_samples)
        print selected_samples
        # delete em
        for sample in selected_samples:
            handle = self.s.sampletools.get_handle_by_name(sample)
            self.main.log("Deleting %s" % (handle))
            self.s.sampletools.delete_by_handle(handle)
            
        # the lazy way to update ...
        self.main.init_lists()

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
                self.main.log("setting drum type")
                self.s.programtools.set_type(1)

            for i in range(num_samples):
                #self.main.log(str("adding", i, notes[i][0], notes[i][1], selected_samples[i]))
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

class ProgramsContextMenu(UI.Base):
    """Context menu for the "programs" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        UI.Base.__init__(self, None, "menuPrograms")

        self.dialogCreateNewKeygroups = DialogCreateNewKeygroups(self)

    def on_duplicate_program_activate(self, button):
        programnames = get_selected_from_treeview(self.main.w_treeview_programs)
        
        for programname in programnames:
            print "Duplicating", programname
            p = ak.Program(self.s,programname)
            dupe = p.copy("Copy " + programname)
            print "Success?", dupe.name
        
    def on_add_keygroup_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)

        self.dialogCreateNewKeygroups.set_program(programname)

        response = self.dialogCreateNewKeygroups.editor.run()

        if response == gtk.RESPONSE_OK:
            howmany = int(self.dialogCreateNewKeygroups.w_spin_howmany_keygroups.get_value())

            if not (type(programname) is list):
                programname = [programname,]

            for pn in programname:
                self.main.log("Adding %d keygroups to %s" % (howmany, pn))
                self.program = ak.Program(self.s,pn)
                self.program.gettools().add_keygroups(howmany)

    def on_program_properties_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        # multiple selection is possible, but for now we'll just take the first one 
        programname = programname[0]
        
        self.main.open_program_properties(programname)

    def on_recycle_init_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        if not (type(programname) is list):
            programname = [programname,]
        
        for pn in programname:
            program = ak.Program(self.s,pn)
            program.init_recycled()
            
    def on_dump_matrix(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        if not (type(programname) is list):
            programname = [programname,]

        for pn in programname:
            program = ak.Program(self.s,pn)
            matrix = program.dump_matrix()
            self.main.log(matrix)

    def on_keygroup_editor_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        # multiple selection is possible, but for now we'll just take the first one 
        programname = programname[0]
        
        self.main.open_keygroup_editor(programname)
        
    def on_set_current_program_activate(self, widget):
        print "set current program"

class Main(UI.Base):
    """Main Window
    """
    def __init__(self, s):
        self.dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ] 
        self.s = s
        self.kgeditwindow = None
        self.multieditwindow = None
        self.program_details_window = None
        UI.Base.__init__(self, None, "vboxMain")

        setattr(self.s,'FileChooser', UI.FileChooser(s))
        
        self.treeviews = [self.w_treeview_programs, self.w_treeview_multis, self.w_treeview_samples]
        for tv in self.treeviews:
            tv.append_column(gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0))
            tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
            tv.connect("drag_data_received", self.on_drag_data_received)
            tv.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)

        self.ProgramsContextMenu = ProgramsContextMenu(self) 
        self.SamplesContextMenu = SamplesContextMenu(self) 

        self.w_quit1.connect('activate', gtk.main_quit)
        vadj = self.w_console_window.get_vadjustment()
        vadj.connect('changed', lambda a, s=self.w_console_window: self.rescroll(a,s))
        
        self.init_lists()

        self.programsEditor = UI.ProgramsEditor(self.s)
        self.record = UI.RecordDialog(ak.Recording(self.s))

        self.on_update_models(None)
        
        self.log("ak.py %s" % (__version__))

    @staticmethod
    def do_lists(s):
        setattr(s,'samples',s.sampletools.get_names())
        setattr(s,'programs',s.programtools.get_names())
        setattr(s,'multis',s.multitools.get_names())

        setattr(s,'samplesmodel',utils.get_model_from_list(s.samples, True))
        setattr(s,'programsmodel',utils.get_model_from_list(s.programs))
        setattr(s,'multismodel',utils.get_model_from_list(s.multis))

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        self.s.FileChooser.on_drag_data_received(widget, context, x, y, selection, target_type, timestamp)
        self.init_lists()
                
    def set_window(self, window):
        self.window = window
        self.window.set_title("aksui %s" % (__version__))
        self.window.connect('configure_event', self.on_configure_event)
        self.window.connect("drag_data_received", self.on_drag_data_received)
        self.window.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)

    def log(self,text):
        self.w_console.get_buffer().insert_at_cursor(text + "\r\n")

    def rescroll(self,vadj,scroll):
        vadj.set_value(vadj.upper-vadj.page_size)
        scroll.set_vadjustment(vadj)        
        
    def move_properties_window(self):
        position = self.window.get_position()
        size = self.window.get_size()
        decoration_width = 10
        if self.program_details_window:
            self.program_details_window.editor.move(position[0] + size[0] + decoration_width, position[1])
            def init_lists(self):
        try:
            Main.do_lists(self.s)
            self.s.samplesmodel.connect("row-changed", self.on_update_models)
            self.s.programsmodel.connect("row-changed", self.on_update_models)
            self.s.multismodel.connect("row-changed", self.on_update_models)

            self.on_update_models(None)
            self.log("Multis, Programs, and Samples Loaded...")
        except Exception, ex:
            self.log("Exception: %s" % (ex))
            
    def open_multi_editor(self, multiname):
        if multiname:
            m = ak.Multi(self.s,multiname)
            if not self.multieditwindow:
                self.multieditwindow = UI.MultiEditorWindowZ(self.s, m)
            else:
                self.multieditwindow.setup(m)
            self.multieditwindow.show_all()
                
    def open_keygroup_editor(self, programname):
        if programname:
            p = ak.Program(self.s,programname)
            if not self.kgeditwindow:
                self.kgeditwindow = UI.KeygroupEditorWindowZ(self.s, p)
            else:
                self.kgeditwindow.setup(p)
            self.kgeditwindow.show_all()
                
    def on_refresh_clicked(self, widget):
        self.init_lists()

    def on_update_models(self, model, iter = None, user_param = None):
        print "Models updated."
        self.w_treeview_programs.set_model(self.s.programsmodel)
        self.w_treeview_multis.set_model(self.s.multismodel)
        self.w_treeview_samples.set_model(self.s.samplesmodel)

    def get_curr_programname(self):
        selection = self.w_treeview_programs.get_selection()

        model, iter = selection.get_selected()
        programname = model[iter][0]
        return programname

    def open_program_properties(self, programname):
        p = ak.Program(self.s, programname)
        
        if not self.program_details_window:
            self.program_details_window = UI.ProgramDetails(p)
        else:
            self.program_details_window.set_samplerobject(p)
        
        self.move_properties_window()
        self.program_details_window.show_all()
    
    def on_recording_activate(self, button):
        self.log("record activate")
        self.record.show_all()
        
    def on_program_editor_activate(self, button):
        self.programsEditor.programsMain.show_all()

    def on_run_tests_activate(self, button):
        # i didn't realize the keygroup index was accounted for there
        handle = self.s.programtools.get_handle_by_name("Program 1")
        p = ak.Program(self.s,"Program 1")
        kg = ak.Keygroup(p,0)
        kg.precache()
        print kg.attrscache
        
    def on_save_activate(self, button):
        # THIS WILL OVERWRITE FILES w/ SAME NAMES!
        # get folder to save to
        path = self.s.FileChooser.open(upload=False,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,title="Save all files...",multiple=False)
            
        if path:
            org = {'multitools':'.akm', 'programtools':'.akp', 'sampletools' : '.wav'}
            results = []
            for toolname in org.keys():
                ext = org[toolname]
                tool = getattr(self.s, toolname)
                items = tool.get_names()
                if type(items) is str:
                    items = [items,]
                # download it
                for item in items:
                    if len(item) > 0:
                        print path, item, ext
                        filename = item + ext
                        filenamepath = path + "/" + filename
                        if os.path.exists(filenamepath):
                            # TODO: Put some sort of confirmation here, if user wants it.
                            self.log(filenamepath + " exists; overwriting it.")
                        self.log("Saving " + filenamepath + "...")
                        self.s.get(filename, filenamepath)
        else:
            self.log("Invalid path chosen.")
            
    def on_upload_activate(self, button):
        self.s.FileChooser.open(upload=True)
        self.init_lists()

    def on_configure_event(self, widget, event):
        self.move_properties_window()
        return False
        def on_lcd_activate(self, button):
        lcd = UI.LCDScreen(self.s)
        win = gtk.Window()
        win.add(lcd)
        win.show_all()
       
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

                self.open_keygroup_editor(curr_program)
                
                """
                OLD ONE:
                self.programsEditor.set_program(curr_program)
                self.programsEditor.programsMain.show_all()
                """

        if widget == self.w_treeview_multis:
            if event.type == gtk.gdk._2BUTTON_PRESS:
                curr_multi = get_selected_from_treeview(self.w_treeview_multis)

                if type(curr_multi) is list:
                    curr_multi = curr_multi[0]

                self.open_multi_editor(curr_multi)
                
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

if USE_CUSTOM_EXCEPTHOOK:
    sys.excepthook = exceptionHandler

def main(): 
    z48 = Devices.get_instance("z48", "usb")
    try:
       m = Main(z48)
       win = gtk.Window()
       win.add(m.editor)
       m.set_window(win)
       win.show_all()
       win.connect("delete-event", gtk.main_quit)
       gtk.main()
    finally:
       z48.close()

if __name__ == "__main__":
    if ENABLE_PROFILER:
        prof = hotshot.Profile("ak.py.prof")
        prof.runcall(main)
        stats = hotshot.stats.load("ak.py.prof")
        stats.sort_stats('time', 'calls')
        stats.print_stats()
    else:
        main()