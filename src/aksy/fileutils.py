import re

RE_MULTI = re.compile("\.akm$", re.IGNORECASE)
RE_PROGRAM = re.compile("\.(akp|pgm)$", re.IGNORECASE)
RE_SAMPLE = re.compile("\.(wav|aiff?)$", re.IGNORECASE)
RE_SONG = re.compile("\.mid$", re.IGNORECASE)
# the entire printable ascii range
RE_WORD = re.compile("[ -~]+$", re.IGNORECASE)
RE_FILE = re.compile("\.(akm|akp|pgm|wav|aiff?|mid)$", re.IGNORECASE)


def is_file_type_supported(supported_file_types, filename):
    for file_type in supported_file_types:
        if filename.lower().endswith(file_type):
            return True
    return False

def is_dirpath(path):
    return path.count('.') == 0 or not is_file(path)

def is_file(path):
    return RE_FILE.search(path) is not None

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