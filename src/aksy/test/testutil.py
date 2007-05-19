import os.path

script_dir = os.path.abspath(os.path.split(__file__)[0])
AKSY_SRCDIR = os.path.dirname(script_dir)

def get_aksydir(rel_path):
    return os.path.join(AKSY_SRCDIR, rel_path)

def get_test_resource(name):
    return os.path.join(script_dir, name)