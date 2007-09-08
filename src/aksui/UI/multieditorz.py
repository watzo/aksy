import gobject, gtk.glade, gtk

import UI,ak

class MultiEditorWindowZ(gtk.Window):
    def __init__(self, s, m):
        gtk.Window.__init__(self)
        self.s = s
        self.setup(m)
        
    def setup(self, m):
        self.set_default_size(600,500)
        self.editor = MultiEditorZ(self.s,m)
        self.add(self.editor.editor)
        self.set_title("aksui: %s" % (m.name))
        #self.editor.setup(p)
        
class MultiEditorZ(UI.Base):
    def __init__(self, s, m):
        UI.Base.__init__(self, m, "multiEditorZ")
        self.s = m.s
        self.multiEditorVBox = UI.MultiEditorVBox(s,m)
        self.w_viewportMultis.add(self.multiEditorVBox)
