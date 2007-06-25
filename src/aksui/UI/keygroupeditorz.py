import gobject, gtk.glade, gtk

import UI,ak

class KeygroupEditorWindowZ(gtk.Window):
    def __init__(self, s, p):
        gtk.Window.__init__(self)
        self.s = s
        self.setup(p)
        
    def setup(self, p):
        self.set_default_size(800,700)
        self.editor = KeygroupEditorZ(self.s,p)
        self.add(self.editor.editor)
        self.set_title("aksui: %s" % (p.name))
        #self.editor.setup(p)
        
class KeygroupEditorZ(UI.Base):
    def __init__(self, s, p):
        UI.Base.__init__(self, p, "keygroupEditorZ")
        self.s = p.s
        self.p = p
        self.keygroupEditorVbox = UI.KeygroupEditorVBox(s,p)
        self.keygroupEditorVbox.on_toggled_callback = self.on_toggled_callback
        # get first keygroup
        self.curr_keygroup = ak.Keygroup(p,0)
        self.panels = []
        
        self.rightVBox = gtk.VBox()
        
        self.zonePanel = UI.ZonePanel(self.curr_keygroup, self.update_status)
        self.filterPanel = UI.FilterPanel(self.curr_keygroup, self.update_status)
        self.keygroupPanel = UI.KeygroupPanel(self.curr_keygroup, self.update_status)
        self.keygroupEnvelopes = UI.KeygroupEnvelopes(self.curr_keygroup, self.update_status)
        
        self.panels.append(self.filterPanel)
        self.panels.append(self.zonePanel)
        self.panels.append(self.keygroupPanel)
        self.panels.append(self.keygroupEnvelopes)
        
        self.rightVBox.pack_start(self.keygroupPanel)
        self.rightVBox.pack_start(self.zonePanel)
        self.rightVBox.pack_start(self.filterPanel)
        self.rightVBox.pack_start(self.keygroupEnvelopes)
        
        # TODO: needs to be bound to an entry box that will actually set update program name
        self.w_entryProgramName.set_text(p.name)
        self.w_viewportKeygroups.add(self.keygroupEditorVbox)
        self.w_viewportSlats.add(self.rightVBox)
        children = self.w_statusbar.get_children()[0].get_children()
        self.statuslabel = children[0]
        
    def change_keygroup(self, keygroup_index):
        self.curr_keygroup = ak.Keygroup(self.p,keygroup_index)
        self.curr_keygroup.set_current()
        for panel in self.panels:
            panel.setup(self.curr_keygroup)
            
    def update_status(self, soattr, sovalue):
        self.statuslabel.set_text("Setting: " + soattr + " " + str(sovalue))
        
    def on_toggled_callback(self, widget, data):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        if widget.get_active():
            self.change_keygroup(data-1) # index is +1