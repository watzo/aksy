
import os.path

data = {}

def get(pathtype):
    try:
        return data[pathtype]
    except KeyError:
        return None

def set(pathtype, path):
    if path and os.path.isfile(path):
        path = os.path.dirname(path)
    data[pathtype] = path

def getDict():
    return data


    