import pygtk
pygtk.require('2.0')
import gtk
import os

import UI,ak,utils

class LFOPanel(UI.PanelBase):
    def __init__(self,kg,cb=None):
        UI.PanelBase.__init__(self,kg,"LFOs",cb)

    def setup(self, kg):
        self.clear_children(True)

        self.kg = kg
        self.s = kg.s
        lfovbox = gtk.VBox()
        for i in range(2):
            lfohbox = gtk.HBox()
            lfo = ak.LFO(kg.s, kg, i)
            # two lfos
            lfohbox.pack_start(UI.AkKnobWidget(lfo, "lfo_depth", 0, 100, 1, None), False, False, 0)
            lfohbox.pack_start(UI.AkKnobWidget(lfo, "lfo_rate", 0, 100, 1, None), False, False, 0) # what is this in hz?
            lfohbox.pack_start(UI.AkKnobWidget(lfo, "lfo_delay", 0, 100, 1, None), False, False, 0) # what is this in ms?
            lfohbox.pack_start(UI.AkKnobWidget(lfo, "lfo_phase", 0, 360, 1, None), False, False, 0)
            lfohbox.pack_start(UI.AkKnobWidget(lfo, "lfo_shift", -50, 50, 1, None), False, False, 0)
            lfohbox.pack_start(UI.AkComboBox(lfo, "lfo_waveform", utils.sampler_lists["lfo_waves"]), True, True, 0)
            lfohbox.pack_start(UI.AkComboBox(lfo, "lfo_retrigger", utils.sampler_lists["lfo_retrigger"]), True, True, 0)
            lfohbox.pack_start(UI.AkComboBox(lfo, "lfo_sync", utils.sampler_lists["lfo_sync"]), True, True, 0)
            lfohbox.pack_start(UI.AkComboBox(lfo, "lfo_midi_sync", utils.sampler_lists["lfo_midi_sync"]), True, True, 0)
            lfovbox.pack_start(lfohbox)
        lfohbox = gtk.HBox(False, 0)
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_14", -100, 100, 1, ""), False, False, 0) # LFO1 to CUTOFF
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_1", -100, 100, 1, ""), False, False, 0) # LFO1 to AMP
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_2", -100, 100, 1, ""), False, False, 0) # LFO1 to PAN
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_3", -100, 100, 1, ""), False, False, 0) # LFO1 to PITCH
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_4", -100, 100, 1, ""), False, False, 0) # LFO1 to LFO1 RATE
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_7", -100, 100, 1, ""), False, False, 0) # LFO1 to LFO1 PHASE
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_9", -100, 100, 1, ""), False, False, 0) # LFO1 to LFO2 RATE
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_9_12", -100, 100, 1, ""), False, False, 0) # LFO1 to LFO2 PHASE
        lfovbox.pack_start(lfohbox)
        lfohbox = gtk.HBox(False, 0)
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_14", -100, 100, 1, ""), False, False, 0) # LFO2 to CUTOFF
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_1", -100, 100, 1, ""), False, False, 0) # LFO2 to AMP
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_2", -100, 100, 1, ""), False, False, 0) # LFO2 to PAN
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_3", -100, 100, 1, ""), False, False, 0) # LFO2 to PITCH
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_4", -100, 100, 1, ""), False, False, 0) # LFO2 to LFO1 RATE
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_7", -100, 100, 1, ""), False, False, 0) # LFO2 to LFO1 PHASE
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_9", -100, 100, 1, ""), False, False, 0) # LFO2 to LFO2 RATE
        lfohbox.pack_start(UI.AkKnobWidget(kg, "MOD_10_12", -100, 100, 1, ""), False, False, 0) # LFO2 to LFO2 PHASE
        lfovbox.pack_start(lfohbox)

        self.pack_start(lfovbox)
        self.show_all()
