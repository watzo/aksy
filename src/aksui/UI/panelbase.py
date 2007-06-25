import pygtk
pygtk.require('2.0')
import gtk,gtk.glade,gobject
import ak,UI

class PanelBase(gtk.VBox):
    def __init__(self, so, set_callback = None):
        gtk.VBox.__init__(self, False, 0)
        self.set_callback = set_callback
        so.set_callback = set_callback
        self.setup(so)
        
    def clear_children(self):
        for i in (self.get_children()):
            self.remove(i)

    def setup(self,so):
        # sampler
        self.s = so.s
        # samplerobject
        self.so = so