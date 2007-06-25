import pygtk
pygtk.require('2.0')
import gtk

import UI,ak,utils

class KeygroupPanel(UI.PanelBase):
    def __init__(self, kg, cb):
        UI.PanelBase.__init__(self,kg,cb)
        
    def setup(self, kg):
        self.clear_children()
        
        self.kg = kg
        self.s = kg.s

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        controls = [
            UI.AkKnobWidget(kg, "level", -600, 60, 10, "db"),
            UI.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""),
            UI.AkKnobWidget(kg, "polyphony", 1, 64, 1, "voices"),
            # mute group
            # fx send
            # send volume
            ]

        for control in controls:
            hbox.pack_start(control, False, False, 1)
        vbox.pack_start(hbox, False, False, 1)
        self.pack_start(vbox, False, False, 1)
        self.show_all()