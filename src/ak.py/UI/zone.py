import os,os.path,re,logging,sys,struct,math,traceback
import pygtk
import inspect
import gobject,gtk.glade,gtk,aksy

import UI

from ak.zone import *
from utils.modelutils import *
from utils.midiutils import *

class ZoneEditor(UI.base):
    def __init__(self, zone):
        UI.base.__init__(self, zone, "zoneTable")

        self.combo_sample = self.xml.get_widget("combo_sample")
        self.s.samplesmodel.connect("row-changed", self.on_row_changed)

        self.lbl_zone_no = self.xml.get_widget("lbl_zone_no")
        self.lbl_zone_no.set_text(str(self.index))

        self.set_zone(zone)

        self.last_folder = None

    def set_zone(self, zone):
        self.zone = zone
        self.kg = zone.parent
        self.initSampleCombo()
        self.update()

    def on_row_changed(self, widget, changed, what):
        self.initSampleCombo()

    def initSampleCombo(self):
        if not self.updating:
            self.combo_sample.set_model(self.s.samplesmodel)
            iter = search(self.s.samplesmodel, self.s.samplesmodel.iter_children(None), match_func, (0, self.zone.sample)) 
            if iter:
                self.zone.updating = True
                self.combo_sample.set_active_iter(iter)
                self.zone.updating = False

    def on_buttonOpen_clicked(self, widget):
        nameonly = self.s.filechooser.open(False, True)
        if nameonly:
            self.zone.sample = nameonly
            self.updating = False
            self.s.samplesmodel.append([nameonly,len(self.s.samples)+1])
            self.zone.s.zonetools.set_sample(self.zone.index,nameonly)
            self.initSampleCombo()

