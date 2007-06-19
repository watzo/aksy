import gobject, gtk.glade, gtk

import UI

"""
Recording interface(s)!

GOOD IDEA: Put a 'rec' button next to the ... in zone, popup a dialog, record stuff, hit 'OK' and the name of the new sample is returned, select in zone list. Maybe its possible to do this even while playing back??
GOOD IDEA: Chromatic recording of samples from input, use MIDI out (play command should be available to us), automated start/stop, create program, assign samples to zones. Allow spacing of notes and take that into consideration when assigning.
General good idea: base class for these user interfaces to get rid of redundancies and facilitate new interfaces...
"""

class ProgramDetails(UI.Base):
    def __init__(self, program):
        UI.Base.__init__(self, program, "windowProgramDetails")
        self.editor.connect("delete-event", self.on_delete_event)
        self.set_samplerobject(program)
        
    def on_delete_event(self, widget, event):
        # nooooo
        self.editor.hide_all()
        return True