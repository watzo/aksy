import gtk

import base, editors, keygrouppanel, zonepanel, modmatrix, filterpanel, lfopanel
import keygroupenvelope

from aksui.ak import keygroup

class KeygroupEditorWindow(gtk.Window):
    def __init__(self, s, p):
        gtk.Window.__init__(self)
        self.connect("delete_event", self.delete_event)
        self.set_position(gtk.WIN_POS_CENTER) 
        self.s = s
        self.setup(p)

    def delete_event(self, widget, event, data=None):
        self.hide()
        return True

    def clear_children(self):
        for i in (self.get_children()):
            self.remove(i)

    def setup(self, p):
        self.clear_children()
        self.p = p
        self.set_default_size(1000,600)
        #TODO: Don't completely rebuild this every time program changes.
        self.editor = KeygroupEditor(self.s, p)
        self.add(self.editor.editor)
        self.update_title()

    def update_title(self):
        self.set_title("aksui: %s" % (self.p.name))
        
class KeygroupEditor(base.Base):
    def __init__(self, s, p):
        base.Base.__init__(self, p, "keygroupEditorZ")
        self.s = p.s
        self.p = p
        if self.p.type == 1:
            self.keygroupEditor = editors.DrumEditorTable(s,p)
        else:
            self.keygroupEditor = editors.KeygroupEditorVBox(s,p)
            
        self.keygroupEditor.on_toggled_callback = self.on_toggled_callback
        
        # get first keygroup
        self.curr_keygroup = keygroup.get_keygroup_cached(p,0)
        self.panels = []
        
        self.rightVBox = gtk.VBox()

        panel_list = [
                     ("keygroupPanel", keygrouppanel.KeygroupPanel),
                     ("zonePanel", zonepanel.ZonePanel),
                     ("filterPanel", filterpanel.FilterPanel),
                     ("LFOPanel", lfopanel.LFOPanel),
                     ("keygroupEnvelopes", keygroupenvelope.KeygroupEnvelopes),
                     ("modMatrix", modmatrix.ModMatrix),
                    ] 
       
        for (n, ui_type) in panel_list:
            panel = ui_type(self.curr_keygroup, self.update_status)
            setattr(self, n, panel)
            self.panels.append(panel)

        for panel in self.panels:
            self.rightVBox.pack_start(panel, False, False, 0)
        
        self.w_entryProgramName.set_text(p.name)
        self.w_viewportKeygroups.add(self.keygroupEditor)
        self.w_viewportSlats.add(self.rightVBox)

        rbg = None
        curr_mode = self.curr_keygroup.gettools().get_edit_mode()
        modes = ["ONE","ALL","ADD"]
        i = 0
        for mode in modes:
            tb = gtk.RadioButton(rbg, mode)
            if not rbg:
                rbg = tb
            self.w_hboxNameEdit.add(tb)
            tb.connect("toggled", self.on_button_press_event, (i))
            if curr_mode == i:
                tb.set_active(True)
            i = i + 1

        children = self.w_statusbar.get_children()[0].get_children()
        self.statuslabel = children[0]
        
    def on_zone_sample_changed(self, widget, zone_combo, zone_label):
        text = zone_combo.get_text()
        #print zone_label
        zone_label.set_text(text)

    def on_button_press_event(self, widget, mode):
        modes = ["ONE","ALL","ADD"]
        self.curr_keygroup.gettools().set_edit_mode(mode)
        
    def change_keygroup(self, keygroup_index):
        self.curr_keygroup = keygroup.get_keygroup_cached(self.p,keygroup_index)
        self.curr_keygroup.set_current()
        for panel in self.panels:
            panel.setup(self.curr_keygroup)
            
        if self.p.type == 1:
            for i in range(4):
                self.zonePanel.sample_combos[i].connect("changed", self.on_zone_sample_changed, self.zonePanel.sample_combos[i], self.keygroupEditor.zone_labels[keygroup_index][i])
            
    def update_status(self, soattr, sovalue):
        self.statuslabel.set_text("Setting: " + soattr + " " + str(sovalue))
        
    def on_toggled_callback(self, widget, data):
        #print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        if widget.get_active():
            self.change_keygroup(data-1) # index is +1

    def on_entryProgramName_changed(self, widget):
        if(self.p):
            self.p.set_name(widget.get_text())

            window = self.editor.parent
            if window and getattr(window, "p", None):
                window.update_title()
