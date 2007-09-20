import gtk

import panelbase, rangewidget
from aksui.utils import midiutils
from aksui.ak import lfo

class LFOPanel(panelbase.PanelBase):
    def __init__(self,kg,cb=None):
        panelbase.PanelBase.__init__(self,kg,"LFOs",cb)

    def setup(self, kg):
        self.clear_children(True)

        self.kg = kg
        self.s = kg.s
        lfovbox = gtk.VBox()
        for i in range(2):
            lfohbox = gtk.HBox()
            l = lfo.LFO(kg.s, kg, i)
            # two lfos
            lfohbox.pack_start(rangewidget.AkKnobWidget(l, "lfo_depth", 0, 100, 1, None), False, False, 0)
            lfohbox.pack_start(rangewidget.AkKnobWidget(l, "lfo_rate", 0, 100, 1, None), False, False, 0) # what is this in hz?
            lfohbox.pack_start(rangewidget.AkKnobWidget(l, "lfo_delay", 0, 100, 1, None), False, False, 0) # what is this in ms?
            lfohbox.pack_start(rangewidget.AkKnobWidget(l, "lfo_phase", 0, 360, 1, None), False, False, 0)
            lfohbox.pack_start(rangewidget.AkKnobWidget(l, "lfo_shift", -50, 50, 1, None), False, False, 0)
            lfohbox.pack_start(rangewidget.AkComboBox(l, "lfo_waveform", midiutils.sampler_lists["lfo_waves"]), True, True, 0)
            lfohbox.pack_start(rangewidget.AkComboBox(l, "lfo_retrigger", midiutils.sampler_lists["lfo_retrigger"]), True, True, 0)
            lfohbox.pack_start(rangewidget.AkComboBox(l, "lfo_sync", midiutils.sampler_lists["lfo_sync"]), True, True, 0)
            lfohbox.pack_start(rangewidget.AkComboBox(l, "lfo_midi_sync", midiutils.sampler_lists["lfo_midi_sync"]), True, True, 0)
            lfovbox.pack_start(lfohbox)
        self.pack_start(lfovbox, False, False, 1)
        self.show_all()
