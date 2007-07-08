from aksy.device import Devices
import ak, utils

class Multi(ak.SamplerObject):
    def __init__(self,s,name,handle=None):
        ak.SamplerObject.__init__(self,s,None,"multitools")
        
        self.name = name
        self.handle = handle

        self.specialattrs = ["name",]

        self.attrs = ["no_parts"]
        
        if self.name:
            self.s.multitools.set_curr_by_name(self.name)
            self.update()
        else:
            print "No name..."
            
    def set_name(self, name):
        self.s.multitools.rename_curr(name)
        
    def get_handle(self):
        # get handle by name or whatever, override in derived classes
        return self.s.multitools.get_handle_by_name(self.name) 

    def set_current(self):
        self.s.multitools.set_curr_by_name(self.name)
