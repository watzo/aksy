import gtk.glade, gtk

from aksui.ak import programs
from aksui.utils import modelutils
import programeditor, base

class ProgramsEditor:
    def __init__(self, s):
        # sampler instance
        self.s = s
        self.programs = programs.Programs(s)
        self.programdict = { }
        self.updating = False

        self.xml = base.get_glade_xml("programsMain")

        self.programsMain = self.xml.get_widget("programsMain")
        self.programsMainVBox = self.xml.get_widget("programsMainVBox")
        self.comboPrograms = self.xml.get_widget("comboPrograms")

        self.updateProgramList()

        self.xml.signal_autoconnect(self)

        self.programEditor = None
        self.currProgram = None

    def updateName(self, oldname, newname):
        cb = self.comboPrograms
        self.updating = True
        names = self.programdict.values()
        if oldname in names:
            index = names.index(oldname)
            cb.remove_text(index)
            cb.insert_text(index, newname)
            cb.set_active(index)
            self.programdict[index] = newname
        self.updating = False

    def set_program(self, programname):
        self.currProgram = self.programs.getProgram(programname)
        if self.programEditor:
            self.programsMainVBox.remove(self.programEditor.editor)
        self.programEditor = programeditor.ProgramEditor(self)
        self.programsMainVBox.pack_start(self.programEditor.editor)

        self.updating = True
        model = self.comboPrograms.get_model()
        iter = modelutils.search(model, model.iter_children(None), None, (0, programname))
        if type(iter) is gtk.TreeIter:
            self.comboPrograms.set_active_iter(iter)
        else:
            print iter
        self.updating = False

    def on_comboPrograms_changed(self, cb):
        if not self.updating:
            active = cb.get_active_text()
            self.set_program(active)

    def on_buttonUpdate_clicked(self, w):
        setattr(self.s, 'programs', self.s.programtools.get_names())
        setattr(self.s, 'programsmodel', modelutils.get_model_from_list(self.s.programs))
        self.updateProgramList()
        if self.programEditor:
            self.programEditor.update()
        
    def addEditor(self, programName):
        self.editor = programeditor.ProgramEditor(self.s, programName)
        self.programsMainVBox.add(self.editor)

    def updateProgramList(self):
        if getattr(self.s, "programsmodel", None):
            self.comboPrograms.set_model(self.s.programsmodel)

def setattrsbyname(obj, xml, attrs):
    tf = {0:False, 1:True}
    for attr in attrs:
        if attr == "high_note":
            spin = xml.get_widget("spin_" + attr)

        combo = xml.get_widget("combo_" + attr)
        entry = xml.get_widget("entry_" + attr)
        spin = xml.get_widget("spin_" + attr)
        toggle = xml.get_widget("toggle_" + attr)
        hscale = xml.get_widget("hscale_" + attr)

        val = getattr(obj, attr)

        if combo != None:
            combo.set_active(val)
        elif entry != None:
            entry.set_text(val)
        elif toggle != None:
            toggle.set_active(tf[val])
        elif spin != None:
            spin.set_value(val)
        elif hscale != None:
            hscale.set_value(val)
 

