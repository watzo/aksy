import re

RE_MULTI = re.compile("\.[aA][kK][mM]$")
RE_PROGRAM = re.compile("\.[aA][kK][pP]$")
RE_SAMPLE = re.compile("\.[wW][aA][vV]$")
RE_SONG = re.compile("\.[mM][iI][dD]$")
RE_WORD = re.compile("[\w.&_-]+$")

def is_file_type_supported(supported_file_types, filename):
    for file_type in supported_file_types:
        if filename.lower().endswith(file_type):
            return True
    return False

def is_dirpath(path):
    return path.count('.') == 0

def is_sample(path):
    return RE_SAMPLE.search(path) is not None

def is_multi(path):
    return RE_MULTI.search(path) is not None

def is_program(path):
    return RE_PROGRAM.search(path) is not None

def is_song(path):
    return RE_SONG.search(path) is not None

def is_valid_name(name):
    return RE_WORD.match(name) is not None