from aksui.UI import base
	
 	
class ProgramDetails(base.Base):
	    def __init__(self, program):
 	        base.Base.__init__(self, program, "windowProgramDetails")
 	        self.editor.connect("delete-event", self.on_delete_event)
 	        self.set_samplerobject(program)
 	       
 	    def on_delete_event(self, widget, event):
 	        # nooooo
 	        self.editor.hide_all()
 	        return True
