import gtk

class PanelBase(gtk.VBox):
    def __init__(self, so, title = None, set_callback = None):
        gtk.VBox.__init__(self, False, 0)
        if title:
            self.title = title
        else:
            self.title = None
            
        self.set_callback = set_callback
        so.set_callback = set_callback
        self.setup(so)
        
    def clear_children(self,add_label = False):
        for i in (self.get_children()):
            self.remove(i)
            
        if add_label and self.title:
            hbox = gtk.HBox(False,0)
            lb = gtk.Label("<b>%s</b>" % self.title)
            lb.set_justify(gtk.JUSTIFY_LEFT)
            lb.set_use_markup(True)
            hbox.pack_start(lb,False,False,5)
            self.pack_start(hbox,False,False,5)        

    def setup(self,so):
        # sampler
        self.s = so.s
        # samplerobject
        self.so = so