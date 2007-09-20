import gtk

import panelbase, rangewidget
from aksui.utils import midiutils

class FilterPanel(panelbase.PanelBase):
    def __init__(self,kg,cb):
        panelbase.PanelBase.__init__(self,kg,"Filter",cb)
        
    def setup(self, kg):
        self.clear_children(True)
        
        self.kg = kg
        self.s = kg.s

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        controls = [
            rangewidget.AkComboBox(kg, "filter", midiutils.sampler_lists["filter"]),
            rangewidget.AkComboBox(kg, "filter_attenuation", midiutils.sampler_lists["filter_attenuation"]),
            ]
        controls_b = [
            rangewidget.AkKnobWidget(kg, "filter_cutoff", 0, 100, 1, ""), 
            rangewidget.AkKnobWidget(kg, "filter_resonance", 0, 100, 1, ""),
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
