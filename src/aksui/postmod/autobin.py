
import struct
from types import *

import utilx


def load(fp, format):
    temp = fp.read(struct.calcsize(format))
    temp = struct.unpack(format, temp)
    if len(temp) == 1:
        temp = temp[0]
    if type(temp) == TupleType:
        temp = list(temp)
    return temp

    
    
    

def autoload(fp, obj, vars=None, formats=None):
    """autoloads binary data from a file into class instance members.
    the class definition object must have an attribue named "vars" which is a list of member variable names to be loaded.
    it must also have an attribute named "formats" which is a dictionary specifiying struct-module-style format
    strings for each variable name."""

    if not vars:
        vars = obj.__class__.vars
    if not formats:
        formats = obj.__class__.formats

    for x in vars:
        #print "--", x
        temp = fp.read(struct.calcsize(formats[x]))
        temp = struct.unpack(formats[x], temp)
        # struct.unpack always returns a tuple even if there is only one value.
        # convert to single value if there is only one.
        if len(temp) == 1:
            temp = temp[0]

        #print "---", temp

        obj.__dict__[x] = temp
        if type(obj.__dict__[x]) == TupleType:
            obj.__dict__[x] = list(obj.__dict__[x])
            
        
def autosave(fp, obj, vars=None, formats=None):
    """autosaves binary data from a file into class instance members.
    the class definition object must have an attribue named "vars" which is a list of member variable names to be loaded.
    it must also have an attribute named "formats" which is a dictionary specifiying struct-module-style format
    strings for each variable name."""

    if not vars:
        vars = obj.__class__.vars
    if not formats:
        formats = obj.__class__.formats

    for x in vars:

        # struct.pack can't accept a tuple for an array of values, so we must call it with
        # apply.  we need to build a tuple of args to pass it. 
        argtup = [formats[x]]
        if type(obj.__dict__[x]) in (TupleType, ListType):
            argtup = argtup + list(obj.__dict__[x])
        else:
            argtup.append(obj.__dict__[x])
        argtup = tuple(argtup)
        
        #print "argtup", argtup
        temp = struct.pack(*argtup)
        fp.write(temp)
    

def autodump(obj):
    for x in obj.__class__.vars:
        print x,":",utilx.stripnulls(obj.__dict__[x])

