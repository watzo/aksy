import gtk

import ak, UI, utils

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
        self.keygroupEditor = UI.KeygroupEditor(self.p,0)
        self.viewportKeygroupEditor.add(self.keygroupEditor.editor)
        self.update()

    def on_combo_curr_keygroup_changed(self, widget):
        if not self.updating:
            self.update_curr_keygroup()

    def update_combo_curr_keygroup(self):
        keygrouplist = [i for i in range(self.s.programtools.get_no_keygroups())]
        self.keygroupmodel = utils.get_model_from_list(keygrouplist)
        self.combo_curr_keygroup.set_model(self.keygroupmodel)
        iter = utils.search(self.keygroupmodel, self.keygroupmodel.iter_children(None), None, (0, str(self.curr_keygroup) ))
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
