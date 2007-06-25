import ak,UI

class KeygroupEnvelopes(UI.PanelBase):
    def __init__(self, keygroup, cb):
        UI.PanelBase.__init__(self, keygroup, cb)
    
    def setup(self, keygroup):
        self.s = keygroup.s
        self.keygroup = keygroup
        self.update_env('ampenv', self.keygroup.amp_envelope, 0)
        self.update_env('filtenv', self.keygroup.filter_envelope, 1)
        self.update_env('auxenv', self.keygroup.aux_envelope, 2)
            
    def update_env(self, envname, env, index):
        if not hasattr(self, envname):
            setattr(self, envname, UI.EnvelopeWidget(self.keygroup, index))
            self.pack_start(getattr(self, envname));
        e = getattr(self, envname)
        e.set_envelope(self.keygroup, index)
        e.show_all()

