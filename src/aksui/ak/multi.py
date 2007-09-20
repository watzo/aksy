import samplerobject

class Multi(samplerobject.SamplerObject):
    def __init__(self,s,name,handle=None):
        samplerobject.SamplerObject.__init__(self,s,None,"multitools")
        
        self.name = name
        if handle:
            self.handle = handle
        else:
            self.handle = self.s.multitools.get_handle_by_name(self.name) 
            
        self.specialattrs = ["name",]

        self.attrs = ["no_parts"]
        
        if self.name:
            self.s.multitools.set_curr_by_name(self.name)
            self.update()
        else:
            print "No name..."
            
        self.precache()
            
    def set_name(self, name):
        self.s.multitools.rename_curr(name)
        
    def get_handle(self):
        # get handle by name or whatever, override in derived classes
        return self.handle

    def set_current(self):
        self.s.multitools.set_curr_by_name(self.name)
