import ak,UI

class KeygroupEnvelopes(UI.Base):
    def __init__(self, keygroup):
        UI.Base.__init__(self, keygroup, "vboxEnvelopes")

    def update_env(self, envname, env):
        if not hasattr(self, envname):
            setattr(self, envname, UI.EnvelopeWidget(self, env))
            self.editor.pack_start(getattr(self, envname));
        e = getattr(self, envname)
        e.set_envelope(self, env)
        e.show_all()

