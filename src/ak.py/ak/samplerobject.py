import os,os.path,re,logging,sys,struct,math,traceback
import gtk,pygtk,gobject
import aksy

from aksy.device import Devices
from utils.modelutils import *

class samplerobject(object):
    def __init__(self, s, parent, whichtools, index = None):
        self.parent = parent
        self.s = s
        self.index = index
        self.whichtools = whichtools
        self.specialattrs = []
        self.attrs = []
        self.attrscache = { }

        # set callback function
        self.set_callback = None

        # set to true if an index needs to be passed before set 
        self.need_index_for_set = False
        
        # set to true if this obj needs to be the current one before set
        self.set_current_before_get_set = False

    def gettools(self):
        return getattr(self.s, self.whichtools)

    def update(self):
        """ going to replace this w/ a lazy loading type thing
        """
        self.attrscache = { }

    def set(self, attrname, attrval):
        if self.set_current_before_get_set:
            self.set_current_method()

        tools = self.gettools()
        if hasattr(tools, "set_" + attrname) or hasattr(self, "set_" + attrname):
            if getattr(self, "set_" + attrname, None):
                func = getattr(self, "set_" + attrname)
            else:
                if attrname in self.specialattrs:
                    attrval = self.get_special_attr(attrname, attrval)
                func = getattr(tools, "set_" + attrname)
            if self.index != None and self.need_index_for_set:
                func(self.index, attrval)
            else:
                func(attrval)

        if self.set_callback:
            self.set_callback(attrname, attrval)

        # update cache
        self.attrscache[attrname] = attrval

    def get_special_attr(self, attrname, attrval):
        #if attrname == "sample":
        #    attrval = self.samples[attrval]
        return None

    def get(self, attrname):
        pass

    def __getattribute__(self, attrname):
        if object.__getattribute__(self, "set_current_before_get_set"):
            scm = object.__getattribute__(self, "set_current_method")
            scm()

        if attrname in object.__getattribute__(self, "attrs") or attrname in object.__getattribute__(self, "specialattrs"):
            cache = object.__getattribute__(self, "attrscache")

            if not attrname in cache:
                tools = self.gettools()

                fname = "get_" + attrname
                func = getattr(tools,fname,None)

                if func:
                    try:
                        if object.__getattribute__(self,"need_index_for_set"):
                            cache[attrname] = func(object.__getattribute__(self,"index"))
                        else:
                            cache[attrname] = func()
                    except Exception, ex:
                        print attrname, ex

            if attrname in cache: 
                return cache[attrname]
        #else:
        #    print attrname, object.__getattribute__(self, "attrs")

        return object.__getattribute__(self, attrname)
