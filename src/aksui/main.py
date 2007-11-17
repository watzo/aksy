#!/usr/bin/env python

__author__ = """Joseph Misra (main developer)
Walco van Loon (back-end, deployment, refactorings & UI enhancements)
"""
__version__ = '0.3'
__license__ = """
    Copyright (C) 2006-2007  %s

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
""" % __author__

try:
    import hotshot, hotshot.stats
except ImportError:
    print "Profiler not available"

import traceback, thread, os.path

import pygtk
pygtk.require('2.0')
import gtk

# our stuff
from aksui.utils import midiutils, modelutils
from aksui.ak import multi, recording, program, keygroup
from aksui.UI import base, filechooser, multieditor, keygroupeditor, lcdscreen, recorddialog, multifxeditor, programdetails

from aksy.device import Devices
from aksy import config
from aksy.concurrent import transaction



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


class BaseDialog(base.Base):
    def __init__(self, name):
        base.Base.__init__(self, None, name)

    def on_okbutton_clicked(self, widget):
        self.editor.response(gtk.RESPONSE_OK)
        self.editor.hide()

    def on_cancelbutton_clicked(self, widget):
        self.editor.response(gtk.RESPONSE_CANCEL)
        self.editor.hide()

class DialogCreateNewKeygroups(BaseDialog):
    def __init__(self, parent):
        self.s = parent.s
        self.programname = None

        BaseDialog.__init__(self, "dialogCreateNewKeygroups")

    def set_program(self, programname):
        self.programname = programname
        if type(programname) is list:
            caption_name = ' '.join(programname)
        else:
            caption_name = programname

        self.w_label_create_new.set_label("Create new keygroups on: " + caption_name)

class DialogCreateNewProgramFast(BaseDialog):
    def __init__(self, parent):
        self.s = parent.s
        self.programname = None

        BaseDialog.__init__(self, "dialogCreateNewProgramFast")
        self.w_treeview_selected_samples.append_column(gtk.TreeViewColumn('Name', gtk.CellRendererText(), text=0))

class DialogCreateNewMultiFast(BaseDialog):
    def __init__(self, parent):
        self.s = parent.s

        BaseDialog.__init__(self, "dialogCreateNewMultiFast")
        self.w_treeview_selected_programs.append_column(gtk.TreeViewColumn('Name', gtk.CellRendererText(), text=0))

class BaseContextMenu(base.Base):
    def __init__(self, name, main, tree_view, tools_module):
        base.Base.__init__(self, None, name)
        self.main = main
        self.tree_view = tree_view
        self.tools_module = tools_module
    
    def handle_keyboard_event(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == "Delete":
            self.on_delete_activate(None)
        elif gtk.gdk.keyval_name(event.keyval) == "Insert":
          # TODO: create new program/multi
          pass

    def activate_download(self, selected, ext):
        destdir = self.s.FileChooser.open(upload=False, action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, title="Select a folder to save all selected files...", multiple=False)
        if destdir is None:
            return

        self.main.log("Downloading file(s) %s to directory '%s'" % (selected, destdir))
        thread.start_new_thread(self._download_and_notify, (destdir, selected, ext))
    
    @transaction()
    def _download_and_notify(self, destdir, selected, ext):
        for f in selected:
            full_name = f + ext
            self.main.s.transfertools.get(full_name, os.path.join(destdir, full_name))

        self.main.log("Download of file(s) %s to '%s' finished" % (selected, destdir))

    def on_delete_activate(self, widget):
        selected = get_selected_from_treeview(self.tree_view)
        for name in selected:
            handle = self.tools_module.get_handle_by_name(name)
            self.main.log("Deleting '%s' with handle %s" % (name, handle))
            self.tools_module.delete_by_handle(handle)

        self.main.init_lists()

    def on_duplicate_activate(self, widget):
        selected = get_selected_from_treeview(self.tree_view)
        for name in selected:
            new_name = 'Copy of ' + name
            self.main.log("Copy '%s' to '%s'" % (name, new_name))
            self.tools_module.set_curr_by_name(name)
            self.tools_module.copy(new_name)
            
        self.main.init_lists()

    def on_edited(self, cell_rend_text, path, new_name):
        name = get_selected_from_treeview(self.tree_view)[0]
        if new_name == name:
            return
        
        self.main.log("Rename '%s' to '%s'" % (name, new_name))
        handle = self.tools_module.get_handle_by_name(name)
        self.tools_module.rename_by_handle(handle, new_name)
            
        self.main.init_lists()

class MultisContextMenu(BaseContextMenu):
    """Context menu for the "multis" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        BaseContextMenu.__init__(self, "menuMultis", main, main.w_treeview_multis, self.s.multitools)

    def on_multifx_activate(self, widget):
        multi = get_selected_from_treeview(self.main.w_treeview_multis)[0]
        self.s.multitools.set_curr_by_name(multi)
        self.main.open_in_window(multifxeditor.MultiFXEditor(self.s))

    def on_download_activate(self, widget):
        selected = get_selected_from_treeview(self.main.w_treeview_multis)
        self.activate_download(selected, ".akm")
    
    def on_new_multi_activate(self, widget, data=None):
        self.main.on_new_multi_activate(self, widget)
       
class SamplesContextMenu(BaseContextMenu):
    """Context menu for the "samples" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        BaseContextMenu.__init__(self, "menuSamples", main, main.w_treeview_samples, self.s.sampletools)

        self.dialogCreateNewProgramFast = DialogCreateNewProgramFast(self)
        self.dialogCreateNewProgramFast.w_combo_starting_note.set_model(midiutils.midinotesmodel)
        self.dialogCreateNewProgramFast.w_combo_starting_note.set_active(0)

    def on_download_activate(self, widget):
        selected_samples = get_selected_from_treeview(self.main.w_treeview_samples)
        self.activate_download(selected_samples, ".wav")

    def on_new_program_activate(self, widget):
        selected_samples = get_selected_from_treeview(self.main.w_treeview_samples)
        model = modelutils.get_model_from_list(selected_samples)
        tv = self.dialogCreateNewProgramFast.w_treeview_selected_samples.set_model(model)
        self.dialogCreateNewProgramFast.w_entry_program_name.set_text('Program %i' % (self.main.s.programtools.get_no_items() + 1))
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
                for i in range(starting_note, starting_note+num_samples):
                    notes.append([i, i])
                keytrack = 1
                playback = 0
            elif method == 1:
                # drum
                for i in range(num_samples):
                    notes.append([midiutils.mpcpads[i], midiutils.mpcpads[i]])
                keytrack = 0
                # one shot
                playback = 1
            elif method == 2:
                # span
                for i in range(num_samples):
                    notes.append([0, 127])
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

            self.main.init_lists()
            self.dialogCreateNewProgramFast.editor.hide()

class ProgramsContextMenu(BaseContextMenu):
    """Context menu for the "programs" TreeView
    """
    def __init__(self, main):
        self.s = main.s
        self.main = main

        BaseContextMenu.__init__(self, "menuPrograms", main, main.w_treeview_programs, main.s.programtools)

        self.dialogCreateNewKeygroups = DialogCreateNewKeygroups(self)
        self.dialogCreateNewMultiFast = DialogCreateNewMultiFast(self)

    def on_add_keygroup_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)

        self.dialogCreateNewKeygroups.set_program(programname)

        response = self.dialogCreateNewKeygroups.editor.run()

        if response == gtk.RESPONSE_OK:
            howmany = int(self.dialogCreateNewKeygroups.w_spin_howmany_keygroups.get_value())

            if not (type(programname) is list):
                programname = [programname, ]

            for pn in programname:
                self.main.log("Adding %d keygroups to %s" % (howmany, pn))
                self.program = program.Program(self.s, pn)
                self.program.gettools().add_keygroups(howmany)

    def on_program_properties_activate(self, widget):
        names = get_selected_from_treeview(self.main.w_treeview_programs)
        
	for name in names:
            self.main.open_program_properties(name)

    def on_new_multi_activate(self, widget):
        selected_programs = get_selected_from_treeview(self.main.w_treeview_programs)
        model = modelutils.get_model_from_list(selected_programs)
        self.dialogCreateNewMultiFast.w_treeview_selected_programs.set_model(model)
        self.dialogCreateNewMultiFast.w_entry_name.set_text('Multi %i' % (self.main.s.multitools.get_no_items() + 1))
        response = self.dialogCreateNewMultiFast.editor.run()
        if response == gtk.RESPONSE_OK:
            name = self.dialogCreateNewMultiFast.w_entry_name.get_text()
            self.s.multitools.create_new(len(selected_programs), name)
            self.s.multitools.set_curr_by_name(name)
            for i, p in enumerate(selected_programs):
                self.s.multitools.set_multi_part_name(i, p)
            self.main.init_lists()

    def on_recycle_init_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        if not (type(programname) is list):
            programname = [programname, ]
        
        for pn in programname:
            p = program.Program(self.s, pn)
            p.init_recycled()

    def on_download_activate(self, widget):
        selected = get_selected_from_treeview(self.main.w_treeview_programs)
        self.activate_download(selected, ".akp")
            
    def on_dump_matrix(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        if not (type(programname) is list):
            programname = [programname, ]

        for pn in programname:
            p = program.Program(self.s, pn)
            matrix = p.dump_matrix()
            self.main.log(matrix)

    def on_keygroup_editor_activate(self, widget):
        programname = get_selected_from_treeview(self.main.w_treeview_programs)
        # multiple selection is possible, but for now we'll just take the first one 
        programname = programname[0]
        
        self.main.open_keygroup_editor(programname)
        
    def on_new_program_activate(self, widget):
        self.main.on_new_program_activate(widget)
                   
    def on_set_current_program_activate(self, widget):
        print "set current program"


class Main(base.Base):
    """Main Window
    """
    def __init__(self, s):
        self.dnd_list = [ ('text/uri-list', 0, TARGET_TYPE_URI_LIST) ] 
        self.s = s
        self.kgeditwindow = None
        self.multieditwindow = None
        self.program_details_window = None
        base.Base.__init__(self, None, "vboxMain")

        setattr(self.s, 'FileChooser', filechooser.FileChooser(s))
        
        self.ProgramsContextMenu = ProgramsContextMenu(self)
        self.SamplesContextMenu = SamplesContextMenu(self)
        self.MultisContextMenu = MultisContextMenu(self) 

        self.configure_treeview(self.w_treeview_programs, self.ProgramsContextMenu)
        self.configure_treeview(self.w_treeview_samples, self.SamplesContextMenu)
        self.configure_treeview(self.w_treeview_multis, self.MultisContextMenu)

        self.w_quit1.connect('activate', gtk.main_quit)
        
        vadj = self.w_console_window.get_vadjustment()
        vadj.connect('changed', lambda a, s=self.w_console_window: self.rescroll(a, s))
        
        self.init_lists()

        """
        self.programsEditor = programseditor.ProgramsEditor(self.s)
        """
        self.record = recorddialog.RecordDialog(recording.Recording(self.s))

        self.on_update_models(None)
        
    def configure_treeview(self, tv, context_menu):
        text = gtk.CellRendererText()
        text.set_property("editable", True)
        text.connect("edited", context_menu.on_edited)
        tv.append_column(gtk.TreeViewColumn("Name", text, text=0))
        tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        tv.connect("drag_data_received", self.on_drag_data_received)
        tv.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)

        tv.add_events(gtk.gdk.KEY_PRESS)
        tv.connect("key_press_event", context_menu.handle_keyboard_event)
      
    @staticmethod
    def get_names(module):
        handles_names = module.get_handles_names()
        names = []
        for i in range(0, len(handles_names), 2):
            names.append(handles_names[i+1])
        return names
        
    @staticmethod
    def do_programlist(s):
        setattr(s, 'programs', Main.get_names(s.programtools))
        setattr(s, 'programsmodel', modelutils.get_model_from_list(s.programs))
        
    @staticmethod
    def do_lists(s):
        Main.do_programlist(s)
        
        setattr(s, 'samples', Main.get_names(s.sampletools))
        setattr(s, 'samplesmodel', modelutils.get_model_from_list(s.samples))
        
        setattr(s, 'multis', Main.get_names(s.multitools))
        setattr(s, 'multismodel', modelutils.get_model_from_list(s.multis))

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        self.s.FileChooser.on_drag_data_received(widget, context, x, y, selection, target_type, timestamp)
        self.init_lists()
                
    def set_window(self, window):
        self.window = window
        self.window.set_title("aksui %s" % (__version__))
        self.window.connect('configure_event', self.on_configure_event)
        self.window.connect("drag_data_received", self.on_drag_data_received)
        self.window.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)

    def log(self, text):
        self.w_console.get_buffer().insert_at_cursor(text + "\r\n")

    def rescroll(self, vadj, scroll):
        vadj.set_value(vadj.upper-vadj.page_size)
        scroll.set_vadjustment(vadj)        
        
    def move_properties_window(self):
        position = self.window.get_position()
        size = self.window.get_size()
        decoration_width = 10
        if self.program_details_window is not None:
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
            m = multi.Multi(self.s, multiname)
            if not self.multieditwindow:
                self.multieditwindow = multieditor.MultiEditorWindow(self.s, m)
            else:
                self.multieditwindow.setup(m)
            self.multieditwindow.show_all()
                
    def open_keygroup_editor(self, programname):
        if programname:
            if not self.kgeditwindow or self.kgeditwindow.p.name != programname:
                p = program.Program(self.s, programname)
                if not self.kgeditwindow:
                    self.kgeditwindow = keygroupeditor.KeygroupEditorWindow(self.s, p)
                else:
                    self.kgeditwindow.setup(p)
            self.kgeditwindow.show_all()
                
    def on_refresh_clicked(self, widget):
        self.init_lists()

    def on_update_program_model(self):
        self.w_treeview_programs.set_model(self.s.programsmodel)
        
    def on_update_multi_model(self):
        self.w_treeview_multis.set_model(self.s.multismodel)
        
    def on_update_models(self, model, iter = None, user_param = None):
        self.on_update_program_model()
        
        self.on_update_multi_model()
        
        self.w_treeview_samples.set_model(self.s.samplesmodel)

    def get_curr_programname(self):
        selection = self.w_treeview_programs.get_selection()

        model, iter = selection.get_selected()
        programname = model[iter][0]
        return programname

    def open_program_properties(self, programname):
        p = program.Program(self.s, programname)
        
        if not self.program_details_window:
            self.program_details_window = programdetails.ProgramDetails(p)
        else:
            self.program_details_window.set_samplerobject(p)
        
        self.move_properties_window()
        self.program_details_window.show_all()
        pass
    
    def on_recording_activate(self, button):
        self.log("record activate")
        self.record.show_all()
        
    def on_program_editor_activate(self, button):
        self.programsEditor.programsMain.show_all()

    def create(self, tools, template, no_items):
        i = tools.get_no_items() + 1
        name = template % i
        tools.create_new(no_items, name)
        self.log("%s created" % name)
        
    def on_new_program_activate(self, widget, data=None):
        self.create(self.s.programtools, "Program %i", 4)
        self.init_lists()
                
    def on_new_multi_activate(self, widget, data=None):
        self.create(self.s.multitools, "Multi %i", 12)
        self.init_lists()
        
    def on_save_activate(self, button):
        # THIS WILL OVERWRITE FILES w/ SAME NAMES!
        # get folder to save to
        path = self.s.FileChooser.open(upload=False, action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, title="Save all files...", multiple=False)
            
        if path:
            org = {'multitools':'.akm', 'programtools':'.akp', 'sampletools' : '.wav'}
            results = []
            for toolname in org.keys():
                ext = org[toolname]
                tool = getattr(self.s, toolname)
                items = tool.get_names()
                if type(items) is str:
                    items = [items, ]

                for item in items:
                    if len(item) > 0:
                        filename = item + ext
                        filenamepath = path + "/" + filename
                        if os.path.exists(filenamepath):
                            # TODO: Put some sort of confirmation here, if user wants it.
                            self.log(filenamepath + " exists; overwriting it.")
                        self.log("Saving " + filenamepath + "...")
                        self.s.transfertools.get(filename, filenamepath)
        else:
            self.log("Invalid path chosen.")
            
    def on_upload_activate(self, button):
        self.s.FileChooser.open(upload=True)
        self.init_lists()

    def on_about_activate(self, button):
        dialog = gtk.AboutDialog()
        dialog.set_name('aksui')
        dialog.set_version(__version__)
        dialog.set_authors((__author__,))
        dialog.set_license(__license__)
        dialog.set_comments("Take control of your sampler!")
        dialog.set_website("http://walco.n--tree.net/projects/aksy/")
        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()
        
    def on_configure_event(self, widget, event):
        self.move_properties_window()
        return False

    def on_lcd_activate(self, button):
        self.open_in_window(lcdscreen.LCDScreen(self.s))

    def open_in_window(self, widget):
        win = gtk.Window()
        win.add(widget)
        win.show_all()

    def on_treeview_event(self, widget, event):
        """Handles context menus + doubleclicks.
        """

        if widget == self.w_treeview_programs:
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                self.ProgramsContextMenu.editor.popup(None, None, None, event.button, event.time)
                return True

            if event.type == gtk.gdk._2BUTTON_PRESS:
                curr_programs = get_selected_from_treeview(self.w_treeview_programs)
                if len(curr_programs) == 0:
                    return False

                self.open_keygroup_editor(curr_programs[0])
                
	"""
	OLD ONE:
	self.programsEditor.set_program(curr_program)
	self.programsEditor.programsMain.show_all()
	"""

        if widget == self.w_treeview_multis:
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                self.MultisContextMenu.editor.popup(None, None, None, event.button, event.time)
                return True

            if event.type == gtk.gdk._2BUTTON_PRESS:
                curr_multi = get_selected_from_treeview(self.w_treeview_multis)
                if len(curr_multi) == 0:
                    return False
                
                curr_multi = curr_multi[0]

                self.open_multi_editor(curr_multi)
                
        if widget == self.w_treeview_samples:
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                self.SamplesContextMenu.editor.popup(None, None, None, event.button, event.time)
                return True

log = None

if USE_CUSTOM_EXCEPTHOOK:
    import sys
    sys.excepthook = exceptionHandler

def add_keybinding(accel_group, widget, accel_str, signal="activate"):
    keyval, mods = gtk.accelerator_parse(accel_str)
    widget.add_accelerator(signal, accel_group, 
                                       keyval, mods, gtk.ACCEL_VISIBLE)

    
def setup_keybindings(m, accel_group):
    add_keybinding(accel_group, m.w_quit1, "<Ctl>Q")
    add_keybinding(accel_group, m.w_refresh_button, "F5", signal="clicked")
 
def main(): 
    parser = config.create_option_parser(usage="%prog [options]")
    options = parser.parse_args()[0]

    sampler = Devices.get_instance(options.sampler_type, options.connector)

    try:
        m = Main(sampler)
        accel_group = gtk.AccelGroup()
        
        win = gtk.Window()
        win.add_accel_group(accel_group)
        setup_keybindings(m, accel_group)

        win.add(m.editor)

        m.set_window(win)
        win.show_all()
        # TODO: make edit menu functional
        m.w_edit_menu.hide()
        win.connect("delete-event", gtk.main_quit)

        gtk.main()
    finally:
        sampler.close()

if __name__ == "__main__":
    if ENABLE_PROFILER:
        prof = hotshot.Profile("ak.py.prof")
        prof.runcall(main)
        stats = hotshot.stats.load("ak.py.prof")
        stats.sort_stats('time', 'calls')
        stats.print_stats()
    else:
        main()
