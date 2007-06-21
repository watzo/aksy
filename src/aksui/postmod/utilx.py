
# utilx.py
# misc utility functions


from copy import deepcopy
import string, sys, re
#from types import *


def stripNonNumerics(st):
    return re.sub("[^\d\*,]", "", st)


def tolist(x, copy=1):
    """ return x converted to list. works on simple values or tuples, returns unchanged if x is already a list. """
    if type(x) != list:
        if type(x) == tuple:
            return list(x)
        else:
            return [x]
    else:
        if copy:
            return deepcopy(x)
        else:
            return x
        

def resize_list(lst, newsize, default=None):
    """ grows or shrinks list to specified size.  if list is grown, it is appended with default values """
    if len(lst) > newsize:
        lst[0:len(lst)] = lst[0:newsize]
    else:
        while len(lst) < newsize:
            lst.append(default)

def stripnulls(s):
    """returns string with null characters removed"""
    return string.replace(str(s), "\0", "")

nonulls = stripnulls


# from cookbook
def unique_seq(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u


def revst(st):
    s = list(st)
    s.reverse()
    return string.join(s, "")


def getCallerName():
    # get name of calling function
    return sys._getframe(2).f_code.co_name

def showCallerInfo():
    # get name of calling function
    #print dir(sys._getframe(2).f_code)
    print sys._getframe(2).f_code.co_name, sys._getframe(2).f_code.co_filename, sys._getframe(2).f_code.co_firstlineno

    
