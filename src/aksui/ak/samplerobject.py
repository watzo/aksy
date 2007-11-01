#import os,os.path,re,logging,sys,struct,math,traceback
import gtk,pygtk,gobject
import aksy

import aksui.utils

class SamplerObject(object):
    def __init__(self, s, parent, whichtools, index = None):
        self.parent = parent
        self.s = s
        self.index = index
        self.whichtools = whichtools
        self.specialattrs = []
        self.attrs = []
        self.attrs_minimal = []
        self.attrscache = { }
        self.abbr = {}
       
        # used for alt operations + zones
        self.keygroup_index = None

        # set callback function
        self.set_callback = None

        # set to true if an index needs to be passed before set 
        self.need_index_for_set = False
        
        # set to true if an index needs to be passed in batch operations as an argument
        self.need_index_in_arguments = False
        
        # set to true if this obj needs to be the current one before set
        self.set_current_before_get_set = False
        
    def get_knob(self, attr):
        if attr.startswith("MOD_"):
            pin = self.get_pin_by_name(attr, False)
            if pin:
                return str(pin.level)
            else:
                return ""
        elif attr in self.abbr.keys():
            return self.abbr[attr]
        else:
            return attr
        
    def gettools(self):
        return getattr(self.s, self.whichtools)

    def update(self):
        """ going to replace this w/ a lazy loading type thing
        """
        #print "Update called %s %s." % (self.whichtools, self.get_handle())
        #self.attrscache = { }
        
    def get_handle(self):
        raise NotImplementedError()
        
    def precache(self, clear_cache = False, minimal = True):
        if clear_cache:
            self.attrscache = {}
           
        if minimal and len(self.attrs_minimal) > 0: 
            attrs = self.attrs_minimal
        else:
            attrs = self.attrs
        
        tools = self.gettools()
        handle = self.get_handle()
        assert handle != None
        
        cmds = []
        args = []
        collect = []
        for attr in attrs:
            if attr not in self.specialattrs and attr not in self.attrscache:
                cmd_name = 'get_' + attr + '_cmd'
                cmd = getattr(tools, cmd_name, None)
                if cmd:
                    # if arguments are needed
                    if len(cmd.arg_types) > 0:
                        if self.need_index_in_arguments:
                            collect.append(attr)
                            cmds.append(cmd)
                            args.append([self.index])
                    else:
                        collect.append(attr)
                        cmds.append(cmd)
                        args.append([])

        if len(cmds) > 0:
            if self.keygroup_index != None:
                index = self.keygroup_index
            else:
                index = self.index
                
            results = self.s.execute_alt_request(handle, cmds, args, index)
                
            for i,result in enumerate(results):
                # this assumes the results are in the requested order
                self.attrscache[collect[i]] = result
        
    def set(self, attrname, attrval):
        if self.keygroup_index:
            index = self.keygroup_index
        else:
            index = self.index
            
        handle = self.get_handle()
        assert handle != None

        cmds = []
        args = []
        tools = self.gettools()

        setter_cmd_name = "set_" + attrname + "_cmd"
        set_cmd = getattr(self, setter_cmd_name, getattr(tools, setter_cmd_name))

        cmds.append(set_cmd)
        
        if attrname in self.specialattrs:
            attrval = self.get_special_attr(attrname, attrval)
            
        if self.index != None and self.need_index_for_set:
            arg = [self.index, attrval]
            #print set_cmd.name, repr(set_cmd.id), self.keygroup_index, arg, attrval
            args.append(arg)
        else:
            args.append([attrval])
        
        if len(cmds) > 0:
            self.s.execute_alt_request(handle, cmds, args, self.keygroup_index)
            
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
        if attrname.startswith("MOD_") or attrname in object.__getattribute__(self, "attrs") or attrname in object.__getattribute__(self, "specialattrs"):
            cache = object.__getattribute__(self, "attrscache")

            if not attrname in cache and not attrname.startswith("MOD_"):
                tools = self.gettools()

                fname = "get_" + attrname
                func = getattr(tools,fname,None)

                if func:
                    if object.__getattribute__(self,"need_index_for_set"):
                        index = object.__getattribute__(self,"index")
                        if type(index) != int:
                            raise Exception("Index must be an integer, got:" + str(index))
                        else:
                            cache[attrname] = func(index)
                    elif attrname in ["filter","filter_cutoff", "filter_resonance"]:
                        cache[attrname] = func(0) # will expand later for triple filter
                    else:
                        cache[attrname] = func()
                            
                        # TODO: Fix this, level needs a workaround for some reason..
                        if type(cache[attrname]) == tuple:
                            cache[attrname] = cache[attrname][0]
            elif attrname.startswith("MOD_"):
                func = object.__getattribute__(self, "get_pin_by_name")
                pin = func(attrname)
                if pin:
                    cache[attrname] = pin.level
                else:
                    cache[attrname] = None
                    
            if attrname in cache: 
                return cache[attrname]
        #else:
        #    print attrname, object.__getattribute__(self, "attrs")

        return object.__getattribute__(self, attrname)
