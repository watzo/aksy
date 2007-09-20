from aksui.utils import modelutils
import program

class Programs:
    programtypes = {0:"Keygroup", 1:"Drum"}

    def __init__(self,s):
        self.s = s
        pt = s.programtools
        self.no_items = pt.get_no_items()
        self.handles_names = pt.get_handles_names()
        self.names = pt.get_names()

        self.curr_handle = pt.get_curr_handle()
        if self.curr_handle != 268435455:
            self.curr_name = pt.get_curr_name()

        self.programdict = { }        

        i = 0

        while i < len(self.handles_names):
            self.programdict[self.handles_names[i]] = self.handles_names[i+1]
            i += 2

        self.programsmodel = modelutils.get_model_from_list(self.programdict)
        self.programtypesmodel = modelutils.get_model_from_list(Programs.programtypes)

    def getCurr(self):
        if self.curr_handle in self.programdict:
            return program.Program(self.s, self.programdict[self.curr_handle])
        else:
            return None
    
    def getProgram(self, name):
        return program.Program(self.s, name)

