import gtk.glade

import os.path

from pkg_resources import resource_string
glade_str = resource_string('aksui', 'ak.py.glade')

def get_glade_xml(root):
    return gtk.glade.xml_new_from_buffer(glade_str, len(glade_str), root)

class Base(object):
    def __init__(self, samplerobject, editor_root):
        self.widgets = { }
        if samplerobject:
            self.samplerobject = samplerobject
            self.s = self.samplerobject.s
            self.index = self.samplerobject.index
        else:
            self.samplerobject = None

        self.updating = False
        #print editor_root
        self.xml = get_glade_xml(editor_root)
        self.editor = self.xml.get_widget(editor_root)
        self.finish_editors()

    def finish_editors(self):
        self.xml.signal_autoconnect(self)

    def update(self):
        if self.samplerobject:
            self.updating = True
            self.samplerobject.update()
            tf = {0:False, 1:True}
            samplerobject = self.samplerobject
            xml = self.xml

            for attr in samplerobject.attrs:
                combo = xml.get_widget("combo_" + attr)
                entry = xml.get_widget("entry_" + attr)
                spin = xml.get_widget("spin_" + attr)
                toggle = xml.get_widget("toggle_" + attr)
                hscale = xml.get_widget("hscale_" + attr)

                val = getattr(samplerobject,attr)

                try:
                    if combo != None:
                        if attr != "sample":
                            combo.set_active(val)
                    elif entry != None:
                        entry.set_text(str(val))
                    elif toggle != None:
                        toggle.set_active(tf[val])
                    elif spin != None:
                        spin.set_value(val)
                    elif hscale != None:
                        hscale.set_value(val)
                except Exception, ex:
                    print 'attr',attr,val,ex

            self.updating = False

    def on_param_changed(self, widget):
        if self.samplerobject:
            if not self.updating:
                if type(widget) is gtk.HScale:
                    attrname, attrval = widget.name[7:], widget.get_value()
                    self.samplerobject.set(attrname, int(attrval))
                elif type(widget) is gtk.Entry:
                    attrname, attrval = widget.name[6:], widget.get_text()
                    self.samplerobject.set(attrname, attrval)
                elif type(widget) is gtk.ComboBox:
                    attrname, attrval = widget.name[6:], widget.get_active()
                    self.samplerobject.set(attrname, attrval)
                elif type(widget) is gtk.ToggleButton:
                    attrname, attrval = widget.name[7:], widget.get_active()
                    self.samplerobject.set(attrname, attrval)
                elif type(widget) is gtk.SpinButton:
                    attrname, attrval = widget.name[5:], widget.get_value()
                    self.samplerobject.set(attrname, int(attrval))

    def pop_in(self, container_widget_name, child_widget_name):
        setattr(self,container_widget_name,self.xml.get_widget(container_widget_name))
        setattr(self,child_widget_name,self.xml.get_widget(child_widget_name))
        w = getattr(self,container_widget_name)
        ch = getattr(self,child_widget_name)

        if type(w) is gtk.Notebook:
            w.append_page(ch)
        elif type(w) is gtk.Box:
            w.pack_start(ch)
        elif type(w) is gtk.Container:
            # default
            w.add(ch)

    def get_widget(self, name):
        return self.xml.get_widget(name)
    
    def show_all(self):
        self.editor.show_all()

    def set_samplerobject(self, so):
        self.samplerobject = so
        self.update()

    def __getattribute__(self, name):
        if name.startswith('w_') and not name in self.widgets:
            setattr(self, name, self.xml.get_widget(name[2:]))
            self.widgets[name] = object.__getattribute__(self, name)

        return object.__getattribute__(self, name)
