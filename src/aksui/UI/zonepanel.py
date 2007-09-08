import pygtk
pygtk.require('2.0')
import gtk
import os

import UI,ak,utils

class ZonePanel(UI.PanelBase):
    def __init__(self,kg,cb):
        self.dnd_list = [ ( 'text/uri-list', 0, 80 ) ] 
        UI.PanelBase.__init__(self,kg,"Zones",cb)
        

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

        for j in range(4):
            zone = kg.zones[j]
            zone.set_callback = self.set_callback
            #zonewidget = MiniZoneWidget(kg.zones[j])

            #zonewidget = AkComboBox(zone, "sample", z48.samplesmodel)
            zonehbox = gtk.HBox()
            zonecombos = [
                UI.AkComboBox(zone, "sample", self.s.samplesmodel, False),
# TODO:                UI.AkComboBox(zone, "output", utils.sampler_lists["output"]),
# TODO:                UI.AkComboBox(zone, "keyboard_track", utils.sampler_lists["keyboard_track"]),
                UI.AkComboBox(zone, "playback", utils.sampler_lists["playback_b"])
                ]
            zoneknobs = [
                UI.AkKnobWidget(zone, "level", -600, 60, 10, "db"),
                UI.AkKnobWidget(zone, "pan", 0, 100, 1, ""),
                UI.AkKnobWidget(zone, "filter", -100, 100, 1, ""),
                UI.AkKnobWidget(zone, "mod_start", -9999, 9999, 1, ""),
                UI.AkKnobWidget(zone, "tune", -3600, 3600, 100, ""),
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
