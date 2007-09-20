import gobject

import base

"""
Recording interface(s)!

GOOD IDEA: Put a 'rec' button next to the ... in zone, popup a dialog, record stuff, hit 'OK' and the name of the new sample is returned, select in zone list. Maybe its possible to do this even while playing back??
GOOD IDEA: Chromatic recording of samples from input, use MIDI out (play command should be available to us), automated start/stop, create program, assign samples to zones. Allow spacing of notes and take that into consideration when assigning.
General good idea: base class for these user interfaces to get rid of redundancies and facilitate new interfaces...
"""

class RecordDialog(base.Base):
    def __init__(self, record):
        base.Base.__init__(self, record, "windowRecording")
        self.progressbar = self.xml.get_widget('progressbar_recording')
        self.name = self.xml.get_widget('entry_name')
        self.record = record
        self.update()
        
    def check_progress(self, *args):
        tools = self.record.gettools()
        status = tools.get_status()

        self.progressbar.set_fraction(float(tools.get_progress())/100)
        if status == 6:
            self.continue_check_progress = False
            self.record.gettools().keep()
            print "Kept sample!"
            print self.record.gettools().get_name()

        status = self.record.gettools().get_status()

        if status == 1:
            self.progressbar.set_fraction(0.0)
            self.name.set_text(self.record.gettools().get_name())

        return self.continue_check_progress

    def on_button_clicked(self, widget):
        if widget.name == "button_arm":
            print "before armed", self.record.gettools().get_status()
            self.record.gettools().arm()
            print "after armed", self.record.gettools().get_status()
            if self.record.gettools().get_status() == 2:
                self.record.gettools().record()
            else:
                print self.record.gettools().get_status()
            # 1 == ready
            # 2 == armed
            self.continue_check_progress = True
            gobject.timeout_add(1000, self.check_progress)
        elif widget.name == "button_stop":
            self.record.gettools().stop()
            self.record.gettools().keep()
            self.continue_check_progress = False
            self.progressbar.set_fraction(0.0)
            self.name.set_text(self.record.gettools().get_name())
        elif widget.name == "button_keep":
            self.record.gettools().keep()
            self.continue_check_progress = False
            self.progressbar.set_fraction(0.0)
        elif widget.name == "button_play_preview":
            self.record.gettools().start_playing()
            print self.record.gettools().get_status()
        elif widget.name == "button_stop_preview":
            print "stopping"
            self.record.gettools().stop_playing()
            print self.record.gettools().get_status()
