import gtk

from aksui.UI import base, editors

class MultiEditorWindow(gtk.Window):
    def __init__(self, s, m):
        gtk.Window.__init__(self)
        self.s = s
        self.setup(m)
        
    def setup(self, m):
        self.set_default_size(600, 500)
        self.editor = MultiEditor(self.s, m)
        self.add(self.editor.editor)
        self.set_title("aksui: %s" % (m.name))
        #self.editor.setup(p)
        
class MultiEditor(base.Base):
    def __init__(self, s, m):
        base.Base.__init__(self, m, "multiEditorZ")
        self.s = m.s
        self.multiEditorVBox = editors.MultiEditorVBox(s, m)
        self.w_viewportMultis.add(self.multiEditorVBox)
