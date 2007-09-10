import pygtk
pygtk.require('2.0')
import gtk

import UI,ak,utils

class FilterPanel(UI.PanelBase):
    def __init__(self,kg,cb):
        UI.PanelBase.__init__(self,kg,"Filter",cb)
        
    def setup(self, kg):
        self.clear_children(True)
        
        self.kg = kg
        self.s = kg.s

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        controls = [
            UI.AkComboBox(kg, "filter", utils.sampler_lists["filter"]),
            UI.AkComboBox(kg, "filter_attenuation", utils.sampler_lists["filter_attenuation"]),
            ]
        controls_b = [
            UI.AkKnobWidget(kg, "filter_cutoff", 0, 100, 1, ""), 
            UI.AkKnobWidget(kg, "MOD_12_14", -100, 100, 1, ""), # filter env to cutoff
            UI.AkKnobWidget(kg, "filter_resonance", 0, 100, 1, ""),
            UI.AkKnobWidget(kg, "MOD_12_15", -100, 100, 1, ""), # filter env to res
            ]

        for control in controls:
            hbox.pack_start(control, False, False, 1)
        #vbox.pack_start(hbox, False, False, 1)
        
        #hbox = gtk.HBox()
        for control in controls_b:
            hbox.pack_start(control, False, False, 1)
        vbox.pack_start(hbox, False, False, 1)
        self.pack_start(vbox, False, False, 1)
        self.show_all()
