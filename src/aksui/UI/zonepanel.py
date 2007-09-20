import gtk
import os.path

import panelbase, rangewidget
from aksui.utils import midiutils

class ZonePanel(panelbase.PanelBase):
    def __init__(self,kg,cb):
        self.dnd_list = [ ( 'text/uri-list', 0, 80 ) ] 
        panelbase.PanelBase.__init__(self,kg,"Zones",cb)
        

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp, kg, zone_index, cb):
        self.s.FileChooser.on_drag_data_received(widget, context, x, y, selection, target_type, timestamp)
        # if it was a single selection, set that zone
        if len(self.s.FileChooser.files) > 0 and kg:
            first_file = os.path.basename(self.s.FileChooser.files[0])
            (filename, ext) = first_file.split(".")
            kg.zones[zone_index].set("sample", filename)
        # hack, this should be updating rather than completely refreshing
        cb.set_model(self.s.samplesmodel)
        cb.somodel = self.s.samplesmodel
        cb.init()

    def setup(self, kg):
        self.clear_children(True)
        
        self.kg = kg
        self.s = kg.s
        zonevbox = gtk.VBox()
        self.sample_combos = []

        for j in range(4):
            zone = kg.zones[j]
            zone.set_callback = self.set_callback
            #zonewidget = MiniZoneWidget(kg.zones[j])

            #zonewidget = AkComboBox(zone, "sample", z48.samplesmodel)
            zonehbox = gtk.HBox()
            self.sample_combos.append(rangewidget.AkComboBox(zone, "sample", self.s.samplesmodel, False))
            zonecombos = [
                self.sample_combos[j],
# TODO:                rangewidget.AkComboBox(zone, "output", utils.sampler_lists["output"]),
# TODO:                rangewidget.AkComboBox(zone, "keyboard_track", utils.sampler_lists["keyboard_track"]),
                rangewidget.AkComboBox(zone, "playback", midiutils.sampler_lists["playback_b"])
                ]
            zoneknobs = [
                rangewidget.AkKnobWidget(zone, "level", -600, 60, 10, "db"),
                rangewidget.AkKnobWidget(zone, "pan", 0, 100, 1, ""),
                rangewidget.AkKnobWidget(zone, "filter", -100, 100, 1, ""),
                rangewidget.AkKnobWidget(zone, "mod_start", -9999, 9999, 1, ""),
                rangewidget.AkKnobWidget(zone, "tune", -3600, 3600, 100, ""),
                ]

            for zonecombo in zonecombos:
                zonehbox.pack_start(zonecombo, True, True, 1)
                zonecombo.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, self.dnd_list, gtk.gdk.ACTION_COPY)
                zonecombo.connect("drag_data_received", self.on_drag_data_received, kg, j, zonecombo)

            #zonevbox.pack_start(zonehbox, False, False, 0)
                
            #zonehbox = gtk.HBox()
            for zoneknob in zoneknobs:
                zonehbox.pack_start(zoneknob, False, False, 1)

            zonevbox.pack_start(zonehbox, False, False, 2)

        self.pack_start(zonevbox)
        self.show_all()
