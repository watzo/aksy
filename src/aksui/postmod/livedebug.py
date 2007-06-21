#TODO: replace, remove magicfishnet

import urllib, threading, sys, string, os, traceback
import wxPython.wx


def SendError(type, value, message):
    type = urllib.quote_plus(str(type))
    value = urllib.quote_plus(str(value))
    message = urllib.quote_plus(str(message))
    
    url = magicfishnet.SERVER + magicfishnet.URL_ERROR + ("?type=%s&value=%s&message=%s" % (type, value, message))

    #TODO: get url



    
