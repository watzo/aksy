# NOTE: This might be obsolete, on tasklist...

import gtk,gtk.gdk,pygtk,gobject

from ak.program import *
from utils.modelutils import *

from aksy.device import Devices

class ProgramEditorB(gtk.VBox):
    def __init__(self,p):
        gtk.VBox.__init__(self)
        self.p = p
        self.s = self.p.s

        attrs = ['name','handle','type','group_id','genre','program_no','no_keygroups','keygroup_xfade','keygroup_xfade_type','level','polyphony','reassignment_method','softpedal_loudness_reduction','softpedal_attack_stretch','softpedal_filter_close','midi_transpose']
        for attr in attrs:
            h = gtk.HBox(True)
            v = getattr(p,attr)
            l = gtk.Label(attr)

            if attr == "name":
                w = gtk.Entry()
                w.set_text(v)
                w.connect('changed',p.on_name_change)
            elif attr == "type":
                w = magicCombo(p.programs.programtypesmodel,v,p.on_type_change)
            elif v:
                w = gtk.Label(v)
            else:
                w = None

            if w:
                attrwidget = "_Entry_"+attr
                setattr(self,attrwidget,w)
                attrboxwidget = "_Label_"+attr
                setattr(self,attrboxwidget,h)
                attrboxwidget = "_HBox_"+attr
                setattr(self,attrboxwidget,h)
                h.pack_start(l)
                h.pack_start(w)
                self.pack_start(h, expand=False, fill=False)
        self.show_all()