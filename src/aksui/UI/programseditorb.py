# Possibly obsolete.

class ProgramsEditorB(gtk.VBox):
    def __init__(self,s):
        gtk.VBox.__init__(self)
        self.programs = programs(s)

        self.cb_program = magicCombo(self.programs.programsmodel,0,self.on_program_changed,4) 

        self.pack_start(self.cb_program, expand=False, fill=False)

        self.programEditor = None 
        self.updateProgramEditor()

        self.show_all()

    def on_program_changed(self, cb):
        iter = cb.get_active_iter()
        m = cb.get_model()
        name, handle = m.get(iter,0,1)
        prg = self.programs.getProgram(name, handle)
        self.updateProgramEditor(prg)
        self.show_all()

    def updateProgramEditor(self, prg = None):
        if self.programEditor:
            self.programEditor.destroy()

        if not prg:
            prg = self.programs.getCurr()

        if prg:
            self.programEditor = ProgramEditor(prg)
            self.pack_start(self.programEditor)
