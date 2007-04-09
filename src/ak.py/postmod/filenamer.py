
import os, string, tempfile

        

def requireExt(fname, reqext):
    """Returns a filename with a specified extension appended if the filename doesn't
    already have that extension specified.  Intended use is for ensuring user-entered
    filenames have the correct extension."""
    
    if reqext[0] != ".":
        reqext = "." + reqext
    root, ext = os.path.splitext(fname)
    if string.upper(ext) != string.upper(reqext):
        fname = fname + reqext
    return fname

def uniqueFilename(fname="", alwaysid="", seperator="", maxtries=5000):

    """Returns a unique filename similar to the requested filename, using an
    autoincrementing id to keep the filename distinct from any existing files.
    By default, the id is placed at the end of the base filename, before the
    extension, such as (fname.dat, fname2.dat, fname3.dat), but a different position
    can be specified with %d or %s (numeric or alpha id).
    "alwaysid" is a boolean specifying whether the id should be added to the filename
    even when the requested filename itself is already unique.  It defaults to off
    if no specific autoid position is specified, or defaults to on otherwise.

    Also can be used to return temp filenames if no fname is specified, or a temp file
    in a specific directory if fname is a directory.
    
    examples:
        uniqueFilename("fname.it") -> fname.it, fname2.it, fname3.it
        uniqueFilename("fname.%d.it") -> fname.1.it, fname.2.it, fname.3.it
        uniqueFilename("fname-%s.dat") -> fname-a.it, fname-b.it .. fname-aa.it, fname.ab.it
        uniqueFilename("%d-fname%s.txt") -> 1-fname%s.txt - don't use more than one autoid.

    TODO: %s currently unimplemented.
    """

    if not fname:
        return tempfile.mktemp()
    
    if fname and os.path.isdir(fname):
        savedir = tempfile.tempdir
        tempfile.tempdir = fname
        newname = tempfile.mktemp()
        tempfile.tempdir = savedir
        return newname

    #print "ids", fname
    idspecified = string.find(fname, "%d")
    if idspecified == -1:
        idspecified == string.find(fname, "%s")
        autoid = "%s"
    else:
        autoid = "%d"

    # if alwaysid not specified, set default based on whether an auto-id (%d or %s)
    # is specified.
    if alwaysid == "":
        if idspecified > -1:
            alwaysid = 1
        else:
            alwaysid = 0

    replacename = fname
    if idspecified == -1:
        root, ext = os.path.splitext(fname)
        replacename = root + seperator + "%d" + ext
        idspecified = string.find(fname, "%d")

    if not alwaysid:
        newname = fname
        id = 2
    else:
        newname = ""
        id = 1

    alphaid = "a"
    tries = 0
    while newname == "" or (os.path.exists(newname) and tries < maxtries):
        newname = string.replace(replacename, "%d", str(id), 1)
        id += 1
        tries += 1

    if tries >= maxtries:
        newname = ""

    return newname        
