import gtk,pygtk

import ak,UI

class KeygroupEditor(UI.Base):
    def __init__(self, program, index):
        UI.Base.__init__(self, None, "notebookKeygroup")

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
            self.zone1 = UI.ZoneEditor(self.keygroup.zones[0])
            self.zone2 = UI.ZoneEditor(self.keygroup.zones[1])
            self.zone3 = UI.ZoneEditor(self.keygroup.zones[2])
            self.zone4 = UI.ZoneEditor(self.keygroup.zones[3])
            self.w_tableZones.attach(self.zone1.editor,0,1,0,1)
            self.w_tableZones.attach(self.zone2.editor,1,2,0,1)
            self.w_tableZones.attach(self.zone3.editor,2,3,0,1)
            self.w_tableZones.attach(self.zone4.editor,3,4,0,1)
            self.zonesInitialized = True
       

    def set_keygroup(self, index):
        if index >= 0:
            self.keygroup = ak.Keygroup(self.p, index)

            if self.filter:
                self.w_expanderKeygroupFilter.remove(self.filter.editor)
            if self.details:
                self.w_expanderKeygroupDetails.remove(self.details.editor)

            self.details = UI.KeygroupDetails(self.keygroup)
            self.filter = UI.KeygroupFilter(self.keygroup)
            self.envelopes = UI.KeygroupEnvelopes(self.keygroup)

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