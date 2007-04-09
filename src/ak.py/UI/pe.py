import pygtk
import gobject,gtk.glade,gtk,aksy

from ak.program import *
from ak.zone import *
from UI.zone import *
from UI.envelope import *
from ak.keygroup import *

class ProgramsEditor:
    def __init__(self,s):
        # sampler instance
        self.s = s
        self.programs = programs(s)
        self.programdict = { }
        self.updating = False

        self.xml = gtk.glade.XML("ak.py.glade", "programsMain")

        self.programsMain = self.xml.get_widget("programsMain")
        self.programsMainVBox = self.xml.get_widget("programsMainVBox")
        self.comboPrograms = self.xml.get_widget("comboPrograms")

        self.updateProgramList()

        self.xml.signal_autoconnect(self)

        self.programEditor = None
        self.currProgram = None

    def updateName(self, oldname, newname):
        cb = self.comboPrograms
        self.updating = True
        names = self.programdict.values()
        if oldname in names:
            index = names.index(oldname)
            cb.remove_text(index)
            cb.insert_text(index,newname)
            cb.set_active(index)
            self.programdict[index] = newname
        self.updating = False

    def set_program(self, programname):
        self.currProgram = self.programs.getProgram(programname)
        if self.programEditor:
            self.programsMainVBox.remove(self.programEditor.editor)
        self.programEditor = ProgramEditor(self)
        self.programsMainVBox.pack_start(self.programEditor.editor)

        self.updating = True
        model = self.comboPrograms.get_model()
        iter = search(model, model.iter_children(None), match_func, (0,programname))
        if type(iter) is gtk.TreeIter:
            self.comboPrograms.set_active_iter(iter)
        else:
            print iter
        self.updating = False

    def on_comboPrograms_changed(self, cb):
        if not self.updating:
            active = cb.get_active_text()
            self.set_program(active)

    def on_buttonUpdate_clicked(self,w):
        setattr(self.s,'programs',self.s.programtools.get_names())
        setattr(self.s,'programsmodel',get_model_from_list(self.s.programs))
        self.updateProgramList()
        if self.programEditor:
            self.programEditor.update()
        
    def addEditor(self,programName):
        self.editor = ProgramEditor(self.s, programName)
        self.programsMainVBox.add(self.editor)

    def updateProgramList(self):
        self.comboPrograms.set_model(self.s.programsmodel)

class ProgramEditor:
    def __init__(self, programsEditor):
        # sampler instance
        self.p = programsEditor.currProgram
        self.programsEditor = programsEditor
        self.s = self.p.s
        self.updating = False
        self.curr_keygroup = -1

        xml = gtk.glade.XML("ak.py.glade", "vboxProgramEditorOuter")

        self.editor = xml.get_widget("vboxProgramEditorOuter")
        self.statusbar = xml.get_widget("statusbar")
        self.detailsWindow = xml.get_widget("viewportProgramDetails")
        self.viewportKeygroupEditor = xml.get_widget("viewportKeygroupEditor")
        self.combo_curr_keygroup = xml.get_widget("combo_curr_keygroup")
        xml.signal_autoconnect(self)

        self.xml = gtk.glade.XML("ak.py.glade", "tableProgramDetails")
        self.programDetails = self.xml.get_widget("tableProgramDetails")
        self.detailsWindow.add(self.programDetails)

        xml = self.xml

        self.xml.signal_autoconnect(self)
        self.s.on_execute = self.on_execute
        self.keygroupEditor = KeygroupEditor(self.p,0)
        self.viewportKeygroupEditor.add(self.keygroupEditor.editor)
        self.update()

    def on_combo_curr_keygroup_changed(self, widget):
        if not self.updating:
            self.update_curr_keygroup()

    def update_combo_curr_keygroup(self):
        keygrouplist = [i for i in range(self.s.programtools.get_no_keygroups())]
        self.keygroupmodel = get_model_from_list(keygrouplist)
        self.combo_curr_keygroup.set_model(self.keygroupmodel)
        iter = search(self.keygroupmodel, self.keygroupmodel.iter_children(None), match_func, (0, str(self.curr_keygroup) ))
        if iter:
            self.updating = True
            self.combo_curr_keygroup.set_active_iter(iter)
            self.updating = False

    def update_curr_keygroup(self):
        iter = self.combo_curr_keygroup.get_active_iter()
        self.curr_keygroup = self.keygroupmodel[iter][0]
        self.keygroupEditor.set_keygroup(int(self.curr_keygroup))

    def on_execute(self,msg):
        self.statusbar.pop(0)
        self.statusbar.push(0,msg)
        
    def on_kg_no_changed(self,widget):
        fname = inspect.currentframe(1).f_code.co_name
        if not self.updating and self.curr_keygroup:
            if self.combo_curr_keygroup.get_active() != self.curr_keygroup:
                self.curr_keygroup = int(self.combo_curr_keygroup.get_active())
                self.updateKeygroup()

    def updateKeygroup(self):
        self.keygroupEditor.set_keygroup(self.curr_keygroup)
        self.viewportKeygroupEditor.add(self.keygroupEditor.editor)

    def on_param_changed(self, widget):
        if not self.updating:
            if type(widget) is gtk.HScale:
                attrname, attrval = widget.name[7:], widget.get_value()
                self.p.set(attrname, int(attrval))
            elif type(widget) is gtk.Entry:
                attrname, attrval = widget.name[6:], widget.get_text()
                self.p.set(attrname, attrval)
            elif type(widget) is gtk.ComboBox:
                attrname, attrval = widget.name[6:], widget.get_active()
                self.p.set(attrname, attrval)
            elif type(widget) is gtk.ToggleButton:
                attrname, attrval = widget.name[7:], widget.get_active()
                self.p.set(attrname, attrval)
            elif type(widget) is gtk.SpinButton:
                attrname, attrval = widget.name[5:], widget.get_value()
                self.p.set(attrname, int(attrval))

    def update(self):
        self.updating = True
        self.p.update()

        tf = {0:False, 1:True}
        p = self.p
        xml = self.xml

        for attr in p.attrs:
            combo = xml.get_widget("combo_" + attr)
            entry = xml.get_widget("entry_" + attr)
            spin = xml.get_widget("spin_" + attr)
            toggle = xml.get_widget("toggle_" + attr)
            hscale = xml.get_widget("hscale_" + attr)

            val = getattr(p,attr)

            if combo != None:
                combo.set_active(val)
            elif entry != None:
                entry.set_text(val)
            elif toggle != None:
                toggle.set_active(tf[val])
            elif spin != None:
                spin.set_value(val)
            elif hscale != None:
                hscale.set_value(val)

        entry = xml.get_widget('entry_name')
        entry.set_text(p.name)

        self.curr_keygroup = self.s.keygrouptools.get_curr_keygroup()
        self.update_combo_curr_keygroup()
        self.updating = False

class KeygroupDetails(UI.base):
    def __init__(self, keygroup):
        UI.base.__init__(self, keygroup, "tableKeygroupDetails")

class KeygroupFilter(UI.base):
    def __init__(self, keygroup):
        UI.base.__init__(self, keygroup, "tableFilter")

class KeygroupEnvelopes(UI.base):
    def __init__(self, keygroup):
        UI.base.__init__(self, keygroup, "vboxEnvelopes")

    def update_env(self, envname, env):
        if not hasattr(self, envname):
            setattr(self, envname, Envelope(env))
            self.editor.pack_start(getattr(self, envname));
        e = getattr(self, envname)
        e.set_envelope(env)
        e.show_all()

class KeygroupEditor(UI.base):
    def __init__(self, program, index):
        UI.base.__init__(self, None, "notebookKeygroup")

        self.s = program.s
        self.p = program
        self.index = index

        self.zonesInitialized = False

        self.filter = None
        self.details = None

        self.set_keygroup(index)
        
        self.editor.append_page(self.envelopes.editor, gtk.Label("Envelopes"))

    def update_zone(self, zonename, zone):
        z = getattr(self, zonename)
        z.set_zone(zone)
        z.editor.show_all()

    def update_zones(self):
        self.update_zone("zone1",self.keygroup.zones[0]) 
        self.update_zone("zone2",self.keygroup.zones[1]) 
        self.update_zone("zone3",self.keygroup.zones[2]) 
        self.update_zone("zone4",self.keygroup.zones[3]) 

    def init_zones(self):
        if not self.zonesInitialized:
            self.zone1 = ZoneEditor(self.keygroup.zones[0])
            self.zone2 = ZoneEditor(self.keygroup.zones[1])
            self.zone3 = ZoneEditor(self.keygroup.zones[2])
            self.zone4 = ZoneEditor(self.keygroup.zones[3])
            self.w_tableZones.attach(self.zone1.editor,0,1,0,1)
            self.w_tableZones.attach(self.zone2.editor,1,2,0,1)
            self.w_tableZones.attach(self.zone3.editor,2,3,0,1)
            self.w_tableZones.attach(self.zone4.editor,3,4,0,1)
            self.zonesInitialized = True
       

    def set_keygroup(self, index):
        if index >= 0:
            self.keygroup = keygroup(self.p, index)

            if self.filter:
                self.w_expanderKeygroupFilter.remove(self.filter.editor)
            if self.details:
                self.w_expanderKeygroupDetails.remove(self.details.editor)

            self.details = KeygroupDetails(self.keygroup)
            self.filter = KeygroupFilter(self.keygroup)
            self.envelopes = KeygroupEnvelopes(self.keygroup)

            self.w_expanderKeygroupFilter.add(self.filter.editor)
            self.w_expanderKeygroupDetails.add(self.details.editor)

            self.envelopes.update_env('ampenv', self.keygroup.amp_envelope)
            self.envelopes.update_env('filtenv', self.keygroup.filter_envelope)
            self.envelopes.update_env('auxenv', self.keygroup.aux_envelope)

            self.init_zones()
            self.update_zones()

            self.updating = False
            self.update()
        else:
            self.keygroup = None
            if hasattr(self,'ampenv'):
                self.ampenv.envelope = None
            if hasattr(self, 'filtenv'):
                self.filtenv.envelope = None
            if hasattr(self, 'auxenv'):
                self.auxenv.envelope = None

    def on_button_press_event(self, widget, event):
        if event.state & gtk.gdk.CONTROL_MASK:
            widget.set_value(0)

def setattrsbyname(obj,xml,attrs):
    tf = {0:False, 1:True}
    for attr in attrs:
        if attr == "high_note":
            spin = xml.get_widget("spin_" + attr)

        combo = xml.get_widget("combo_" + attr)
        entry = xml.get_widget("entry_" + attr)
        spin = xml.get_widget("spin_" + attr)
        toggle = xml.get_widget("toggle_" + attr)
        hscale = xml.get_widget("hscale_" + attr)

        val = getattr(obj,attr)

        if combo != None:
            combo.set_active(val)
        elif entry != None:
            entry.set_text(val)
        elif toggle != None:
            toggle.set_active(tf[val])
        elif spin != None:
            spin.set_value(val)
        elif hscale != None:
            hscale.set_value(val)
 

