import gtk

import panelbase, rangewidget

class KeygroupPanel(panelbase.PanelBase):
    def __init__(self, kg, cb):
        panelbase.PanelBase.__init__(self,kg,"Keygroup Details",cb)
        
    def setup(self, kg):
        self.clear_children(True)
        print kg.index
        
        self.kg = kg
        self.s = kg.s

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        controls = [
            rangewidget.AkKnobWidget(kg, "level", -600, 60, 10, "db"),
            rangewidget.AkKnobWidget(kg, "tune", -3600, 3600, 100, ""),
            rangewidget.AkKnobWidget(kg, "polyphony", 1, 64, 1, "voices"),
            # mute group
            # fx send
            # send volume
            ]

        for control in controls:
            hbox.pack_start(control, False, False, 1)
        vbox.pack_start(hbox, False, False, 1)
        self.pack_start(vbox, False, False, 1)
        self.show_all()