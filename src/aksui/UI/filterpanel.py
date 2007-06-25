import pygtk
pygtk.require('2.0')
import gtk

import UI,ak,utils

class FilterPanel(UI.PanelBase):
    def __init__(self,kg,cb):
        UI.PanelBase.__init__(self,kg,cb)
        
    def setup(self, kg):
        self.clear_children()
        
        self.kg = kg
        self.s = kg.s

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        controls = [
            UI.AkComboBox(kg, "filter", utils.sampler_lists["filter"]),
            UI.AkComboBox(kg, "filter_attenuation", utils.sampler_lists["filter_attenuation"]),
            UI.AkKnobWidget(kg, "filter_cutoff", 0, 100, 1, ""), 
            UI.AkKnobWidget(kg, "filter_resonance", 0, 100, 1, ""),
            ]

        for control in controls:
            hbox.pack_start(control, False, False, 1)
        vbox.pack_start(hbox, False, False, 1)
        self.pack_start(vbox, False, False, 1)
        self.show_all()