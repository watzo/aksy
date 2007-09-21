import gtk

import panelbase, editors
class KeygroupEnvelopes(panelbase.PanelBase):
    def __init__(self, keygroup, cb):
        self.env_labels = ["Amp Anvelope", "Filter Envelope", "Aux Envelope"]
        panelbase.PanelBase.__init__(self, keygroup, "Envelopes", cb)
    
    def setup(self, keygroup):
        self.clear_children(True)
        self.vbox = gtk.VBox(False, 0)
        self.s = keygroup.s
        self.keygroup = keygroup
        self.update_env('ampenv', self.keygroup.amp_envelope, 0)
        self.update_env('filtenv', self.keygroup.filter_envelope, 1)
        self.update_env('auxenv', self.keygroup.aux_envelope, 2)
        self.pack_start(self.vbox)
        self.show_all()
            
    def update_env(self, envname, env, index):
        setattr(self, envname, editors.EnvelopeHBox(self.keygroup, index))
        label_hbox = gtk.HBox(False,0)
        lb = gtk.Label("%s" % self.env_labels[index])
        lb.set_justify(gtk.JUSTIFY_LEFT)
        label_hbox.pack_start(lb,False,False,5)
        self.vbox.pack_start(label_hbox,False,False,5);
        self.vbox.pack_start(getattr(self, envname),False,False,1);
        e = getattr(self, envname)
        e.show_all()

