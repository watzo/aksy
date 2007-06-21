import os

class sox:
    def __init__(self):
        pass
    
    def convert(self, filename):
        if os.path.exists(filename):
            [path, fileend] = os.path.split(filename)
            [name, ext] = os.path.splitext(fileend)
            src = filename
            dest = path + "\\" + name + "_rs" + ext
            cmd = "sox \"" + src + "\" -r 44100 \"" + dest + "\" resample -ql" 
            print cmd
            os.system(cmd)
            return dest
        else:
            return None
        # run cmd
