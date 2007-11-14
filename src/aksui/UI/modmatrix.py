import gtk

import panelbase, rangewidget
from aksui.ak import modulationmatrix

"""
    sources      = ['NONE','MODWHEEL','BEND UP','BEND DOWN',
                    'AFTERTOUCH','VELOCITY','BIPOLAR VELOCITY','OFF VELOCITY',
                    'KEYBOARD','LFO1','LFO2','AMP ENV',
                    'FILTER ENV','AUX ENV','MIDI CTRL','Q-LINK 1',
                    'Q-LINK 2','Q-LINK 3','Q-LINK 4','Q-LINK 5',
                    'Q-LINK 6','Q-LINK 7','Q-LINK 8','*MODWHEEL',
                    '*BEND UP','*BEND DOWN','*Q-LINK 1','*Q-LINK 2',
                    '*Q-LINK 3','*Q-LINK 4','*Q-LINK 5','*Q-LINK 6',
                    '*Q-LINK 7','*Q-LINK 8','*LFO1','*LFO2','*MIDI CTRL']

    # should be a total of 52 (0 based), qlink adds 4 'EXT' options
    destinations = ['NONE',           'AMPLITUDE',    'PAN',            'PITCH',
                    'LFO1 RATE',      'LFO1 DEPTH',   'LFO1 DELAY',     'LFO1 PHASE',
                    'LFO1 OFFSET',    'LFO2 RATE',    'LFO2 DEPTH',     'LFO2 DELAY',
                    'LFO2 PHASE',     'LFO2 OFFSET',  'CUTOFF',  'RESONANCE',
                    'TR 1 CUTOFF',    'TR 1 RES',     'TR 2 CUTOFF',    'TR 2 RES',
                    'TR 3 CUTOFF',    'TR 3 RES',     'AMP ENV ATTACK', 'AMP ENV DECAY',
                    'AMP ENV RELEASE','FILT ENV R1',  'FILT ENV R2',    'FILT ENV R4',
                    'AUX ENV R1',     'AUX ENV R2',   'AUX ENV R4',     'ZONE CROSSFADE',
                    'ZONE 1 LEVEL',   'ZONE 1 PAN',   'ZONE 1 PITCH',   'ZONE 1 START', 'ZONE 1 FILTER'
                    'ZONE 2 LEVEL',   'ZONE 2 PAN',   'ZONE 2 PITCH',   'ZONE 2 START', 'ZONE 2 FILTER'
                    'ZONE 3 LEVEL',   'ZONE 3 PAN',   'ZONE 3 PITCH',   'ZONE 3 START', 'ZONE 3 FILTER'
                    'ZONE 4 LEVEL',   'ZONE 4 PAN',   'ZONE 4 PITCH',   'ZONE 4 START', 'ZONE 4 FILTER']
"""

class ModMatrix(panelbase.PanelBase):
    def __init__(self, so, cb, sources = ['MODWHEEL', 'BIPOLAR VELOCITY', 'AMP ENV', 'FILTER ENV', 'AUX ENV', 'LFO1', 'LFO2', '*MODWHEEL', '*LFO1', '*LFO2'], destinations = ['AMPLITUDE', 'PAN', 'PITCH', 'CUTOFF', 'RESONANCE', 'ZONE CROSSFADE', 'AMP ENV ATTACK', 'AMP ENV DECAY', 'AMP ENV RELEASE', 'LFO1 RATE', 'LFO1 DEPTH', 'LFO1 DELAY', 'LFO1 PHASE', 'LFO1 OFFSET', 'LFO2 RATE', 'LFO2 DEPTH', 'LFO2 DELAY', 'LFO2 PHASE','LFO2 OFFSET']):
        # doing this by mod source/dest name because it's easier to read, probably would be slightly faster if it used index # 
        assert sources != None
        assert destinations != None

        self.sources = sources
        self.destinations = destinations

        panelbase.PanelBase.__init__(self, so, "Modulation Matrix", cb)

        self.setup(so)

    def setup(self, so):
        self.clear_children(True)

        self.s = so.s
        self.so = so

        if len(so.mod_matrix) == 0:
            so.load_matrix()

        self.table = gtk.Table(len(self.sources) + 1, len(self.destinations) + 1, False)
        t = self.table

        for source in self.sources:
            i = self.sources.index(source)
            source_label = gtk.Label("<span size='smaller'>%s</span>" % source)
            source_label.set_property("angle", 90)
            source_label.set_use_markup(True)
            t.attach(source_label, i+1, i+2, 0, 1)

        for dest in self.destinations:
            i = self.destinations.index(dest)
            dest_index = modulationmatrix.ModulationMatrix.destinations.index(dest)

            dest_label = gtk.Label("<span size='smaller'>%s</span>" % dest)
            dest_label.set_use_markup(True)
            t.attach(dest_label, 0, 1, i + 1, i + 2)

            for source in self.sources:
                j = self.sources.index(source)
                source_index = modulationmatrix.ModulationMatrix.sources.index(source)
                mod_name = "MOD_%d_%d" % (source_index, dest_index)
                mod_knob = rangewidget.AkKnobWidget(self.so, mod_name, -100, 100, 1, units="", mod_destination=dest) # filter env to res
                t.attach(mod_knob, j + 1, j + 2, i + 1, i + 2, False, False) 

        self.pack_start(t, False, False, 1)
        self.show_all()
