
# Options defines a set of parameters which also can be set by class.member notation

class Options(dict):
    def __init__(self, options=None, **kwargs):
        dict.__init__(self)
        if options:
            self.update(options)
        if kwargs:
            self.update(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self.get(key, None)


class OptionsNoCase(Options):
    def __setattr__(self, key, value):
        self[key.lower()] = value

    def __getattr__(self, key):
        return self.get(key.lower(), None)

    def __getitem__(self, key):
        return self[key.lower()]

    def __setitem__(self, key, value):
        dict.__setitem__(self, key.lower(), value)

    def get(self, key, default=None):
        return dict.get(self, key.lower(), default)

    def has_key(self, key):
        return dict.has_key(self, key.lower())

    def setdefault(self, key, default):
        return dict.setdefault(self, key.lower(), default)
    
    def update(self, d):
        for k, v in d.items():
            self[k.lower()] = v


if __name__ == "__main__":
    opts = {'zizza':200, 'wizza':"friki"}
    a = Options(fart=3, wuzzle="ass")
    a = Options(opts)
    a = OptionsNoCase(opts, fart=3, wuzzle="ass")
    print "---"
    print a
    a.FRIKICHAT = 20*20
    a.frukas = "frukas frukas"
    print a
    print a.wizza, a.frikichat, a.gubalooza
    z = {'wUbbA':10, 'JKJIJI':8, 'Fart':800}
    a.update(z)
    print a
    


    
    
    
    
