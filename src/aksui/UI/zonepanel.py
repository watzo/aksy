import pygtk
pygtk.require('2.0')
import gtk

import UI,ak,utils

class ZonePanel(UI.PanelBase):
    def __init__(self,kg,cb):
        UI.PanelBase.__init__(self,kg,cb)
        
    def setup(self, kg):
        self.clear_children()
        
        self.kg = kg
        self.s = kg.s
        zonevbox = gtk.VBox()

        for j in range(4):
            zone = kg.zones[j]
            zone.set_callback = self.set_callback
            #zonewidget = MiniZoneWidget(kg.zones[j])

            #zonewidget = AkComboBox(zone, "sample", z48.samplesmodel)
            zonehbox = gtk.HBox()
            lb = gtk.Label("<b>" + str(j) + "</b>")
            lb.set_use_markup(True)
            zonecombos = [
                lb,
                UI.AkComboBox(zone, "sample", self.s.samplesmodel, False),
# TODO:                UI.AkComboBox(zone, "output", utils.sampler_lists["output"]),
# TODO:                UI.AkComboBox(zone, "keyboard_track", utils.sampler_lists["keyboard_track"]),
                UI.AkComboBox(zone, "playback", utils.sampler_lists["playback_b"])
                ]
            lb = gtk.Label("<b>" + str(j) + "</b>")
            lb.set_use_markup(True)
            zoneknobs = [
                lb,
                UI.AkKnobWidget(zone, "level", -600, 60, 10, "db"),
                UI.AkKnobWidget(zone, "pan", 0, 100, 1, ""),
                UI.AkKnobWidget(zone, "filter", -100, 100, 1, ""),
                UI.AkKnobWidget(zone, "mod_start", -9999, 9999, 1, ""),
                UI.AkKnobWidget(zone, "tune", -3600, 3600, 100, ""),
                ]

            for zonecombo in zonecombos:
                zonehbox.pack_start(zonecombo, False, False, 1)
            zonevbox.pack_start(zonehbox, False, False, 0)
                
            zonehbox = gtk.HBox()
            for zoneknob in zoneknobs:
                zonehbox.pack_start(zoneknob, False, False, 1)

            zonevbox.pack_start(zonehbox, False, False, 0)

        self.pack_start(zonevbox)
        self.show_all()