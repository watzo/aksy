import os, random, string, glob, shutil
from stat import *

try:
    import win32api
except:
    win32api = None

try:
    from nt import _getfullpathname
except:
    _getfullpathname = None


def filebase(fname):
    return os.path.splitext(os.path.basename(fname))[0]

def replaceExt(fname, ext):
    if ext[0] != '.':
        ext = '.' + ext
    return os.path.splitext(fname)[0] + ext

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



def abspath(path):
    """ in windows, os.abspath can freeze if it's called within a thread; this replacement doesn't."""
    if path: # Empty path must return current working directory.
        try:
            path = _getfullpathname(path)
        except WindowsError:
            pass # Bad path - return unchanged.
    else:
        path = os.getcwd()
    return os.path.normpath(path)
    
if not _getfullpathname:
    # probably not windows, so just use os.path.abspath
    abspath = os.path.abspath


def pathjoin(path1, path2, ignoreAllDrives=0):
    """ same as os.path.join, except drive letters are discarded, and absolute paths are made into non-absolute paths,
    so you can join paths like c:\path1 and d:\path2 into c:\path1\path2.
    by default, the drive of the second path is the only one ignored.  specify ignoreAllDrives=1 to ignore both. """
    if ignoreAllDrives:
        path1 = os.path.splitdrive(path1)[1]
    path2 = os.path.splitdrive(path2)[1]
    if path2 and path2[0] in ["/", "\\"]:
        path2 = path2[1:]
        
    return os.path.join(path1, path2)        
    

def copy(source, dest):
    # like shutil.copy, but removes read-only attribute of target, if present
    # ALSO creates path if it doesn't exist
    ensurePath(os.path.dirname(dest))
    shutil.copy(source, dest)
    if not os.access(dest, os.W_OK):
        os.chmod(dest, 0777)
    

def remove(path):
    # like os.remove, but works with read-only files.  also never fails, returns true if file was removed, false if not, or there
    # was no file to remove.

    if not os.path.exists(path):
        return 0
    
    if not os.access(path, os.W_OK):
        os.chmod(path, 0777)
    try:
        os.remove(path)
        return 1
    except:
        return 0


def _get_short(longpath):
    dir = win32api.FindFiles(longpath)
    if dir:
        short = dir[0][-1]
        if not short:
            short = dir[0][-2] # was a true short one
        return short

def _get_long(longpath):
    dir = win32api.FindFiles(longpath)
    if dir:
        return dir[0][-2]


def GetPath83(fname):
    pieces = string.split(string.replace(fname, "/", "\\"), "\\")
    if not pieces: return ""
    pre = pieces.pop(0)
    if not pre or pre[-1:]==":" : # abs path
        pre = pre + "\\"
        if not pieces: return ""
        first = pieces.pop(0)
    else:  # rel path
        parts = string.split(pre, ":", 1)
        if len(parts) > 1:
            pre = parts[0] + ":"
            first = parts[1]
        else:
            first = pre
            pre = ""
    try:
        oldpath = pre+first
        newpath = pre+_get_short(oldpath)
        for piece in pieces:
            oldpath = oldpath + "\\" + piece
            newpath = newpath + "\\" + _get_short(oldpath)
        return newpath
    except TypeError: return ""  # we got none for the short path

def GetPathLong(fname):
    pieces = string.split(string.replace(fname, "/", "\\"), "\\")
    if not pieces: return ""
    pre = pieces.pop(0)
    if not pre or pre[-1:]==":" : # abs path
        pre = pre + "\\"
        if not pieces: return ""
        first = pieces.pop(0)
    else:  # rel path
        parts = string.split(pre, ":", 1)
        if len(parts) > 1:
            pre = parts[0] + ":"
            first = parts[1]
        else:
            first = pre
            pre = ""
    try:
        oldpath = pre+first
        newpath = pre+_get_long(oldpath)
        for piece in pieces:
            oldpath = oldpath + "\\" + piece
            newpath = newpath + "\\" + _get_long(oldpath)
        return newpath
    except TypeError: return ""  # we got none for the short path

        

def ensurePath(path):
    """create path if it does not exist.  returns 1 if successful, 0 if not."""
    #if os.path.isfile(path):
    #    path = os.path.dirname(path)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except:
        return 0
    return os.path.isdir(path)



allowchars = string.letters + string.digits + string.punctuation + ' '

notallowed = ""
for x in xrange(0,255):
    if chr(x) not in allowchars:
        notallowed = notallowed + chr(x)
notallowed = notallowed + '<>:*?"|'

ensureTable = string.maketrans(notallowed, 'x' * len(notallowed))

def ensureValid(path, asterisk="X", qmark=""):
    """remove invalid characters from a path/filename (such as ? and *)"""
    drive, path = os.path.splitdrive(path)
    result = string.replace(path, "*", asterisk)
    result = string.replace(result, "?", qmark)

    # replace non allowed chars with x
    result = string.translate(result, ensureTable)
    
    return drive + result
        

def deleteFiles(flist):
    """delete list of files"""
    for f in flist:
        os.remove(f)

def removeIfEmpty(path):
    """deletes a directory if it is empty"""
    num = len(getdir(path))
    if num == 0:
        rmdir(path)

def baseAppend(path, append):
    #print "baseAppend", path, append
    root, ext = os.path.splitext(path)
    return root + append + ext
        
            
class FileList:

    def __init__(self):
        self.list = []

    def set(self, path, mask="*.*"):
        #os.chdir(path)
        self.list = glob.glob(os.path.join(path, mask))
        self.dir = path
        
    def randomBatch(self, num=0, allowduplicates=0):
        if num==0:
            num = len(self.list)
        if num > len(self.list) and not allowduplicates:
            num = len(self.list)

        totfiles = len(self.list)            

        batch = []
        for x in xrange(0, num):
            selected=""
            while ((selected in batch) and (not allowduplicates)) or (selected==""):
                i = random.randrange(0, totfiles)
                selected = self.list[i]

            batch.append(selected)                
                
        return batch                

def randomBatch(path, num=0, mask="*.*", allowduplicates=0):
    fl = FileList()
    fl.set(path, mask)
    return fl.randomBatch(num, allowduplicates)

randombatchfromdir = randomBatch

def getdir(path, mask="*.*"):
    fl= FileList()
    fl.set(path, mask)
    return fl.list

def dirSizeByExtension(path, mask="*.*", recurse=0):
    data = {} # keys= exts, value = totalsize
    fl = dir(path, mask=mask, recurse=recurse)

    for x in fl:
        try:
            size = os.stat(x)[ST_SIZE]
        except:
            # oh well
            size = 0

        root, ext = os.path.splitext(x)

        if ext not in data.keys():
            print ext
        data[ext] = data.get(ext, 0) + size

    return data
        

    

def dirSize(path, mask="*.*", recurse=0):
    fl = dir(path, mask=mask, recurse=recurse)
    totalsize = 0
    for x in fl:
        try:
            totalsize = totalsize + os.stat(x)[ST_SIZE]
        except:
            # oh well
            pass


def delBackupsThreshold(path, threshold, mask="*.*", recurse=0):
    """delBackupsThreshold removes files from a specified directory, removing the oldest
    first, until the total size in bytes of the files in the directory is equal to or less
    than the threshold specified.  Only files that fit the specified mask (default: *.*)
    are operated on (including the size check against the threshold).
    Returns list of the files removed.
    This function is intended to be used for limiting the size of backup directories."""

    if recurse:
        fl = dirtree(path, mask)
    else:
        fl = getdir(path, mask)
    flstat = []
    totalsize = 0

    sizes = {}
    
    for x in fl:
        mtime = os.stat(x)[ST_MTIME]
        sizes[x] = os.stat(x)[ST_SIZE]
        totalsize = totalsize + sizes[x]
        flstat.append((mtime, x))
    flstat.sort()

    removed = []

    while (totalsize > threshold):
        # delete top file on list (it has oldest modification time)
        top = flstat.pop(0)
        size = sizes[top[1]]
        os.remove(top[1])
        removed.append(top[1])
        #totalsize = 0
        #for x in flstat:
        #    totalsize = totalsize + sizes[x]
        totalsize -= size

    return removed


def truncateLog(fname, maxsize):
    """truncate a files beginning, leaving tail, if size is over maxsize.  returns 1 if any truncation was done."""
    try:
        size = os.stat(fname)[ST_SIZE]
        if size > maxsize:
            f = open(fname, "rb")
            f.seek(-maxsize, 2)
            data = f.read()
            f.close()
            f = open(fname, "wb")
            f.write(data)
            f.close()
            return 1
        else:
            return 0
    except OSError:
        return 0
    except IOError:
        return 0

def walk( root, recurse=0, pattern='*', return_folders=0 ):
	import fnmatch, os, string
	
	# initialize
	result = []

	# must have at least root folder
	try:
		names = os.listdir(root)
	except os.error:
		return result

	# expand pattern
	pattern = pattern or '*'
	pat_list = string.splitfields( pattern , ';' )
	
	# check each file
	for name in names:
		fullname = os.path.normpath(os.path.join(root, name))

		# grab if it matches our pattern and entry type
		for pat in pat_list:
			if fnmatch.fnmatch(name, pat):
				if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
					result.append(fullname)
				continue
				
		# recursively scan other folders, appending results
		if recurse:
			if os.path.isdir(fullname) and not os.path.islink(fullname):
				result = result + walk( fullname, recurse, pattern, return_folders )
			
	return result

# dir and dirtree are intended to be used by for..in statements
def dirtree(path, mask="*.*", dirs=0):
    return walk(path, 1, mask, dirs)
    
def dir(path, mask="*.*", dirs=0, recurse=0):
    return walk(path, recurse, mask, dirs)
    


def areSame(fname, fname2):
    f = open(fname, "rb")
    data = f.read()
    f.close()
    f = open(fname2, "rb")
    data2 = f.read()
    f.close()
    return data == data2

def compareDirs(path, path2):
    # returns files that are different, doesn't handle subdirs currently
    files = dirtree(path)
    diff = []
    for f in files:
        tf = pathjoin(path2, os.path.basename(f))
        if os.path.exists(tf):
            if not areSame(f, tf):
                diff.append(f)
            else:
                print "same", f, tf
    return diff
            
        


# from python cookbook
class iterdir(object):
    def __init__(self, path, deep=False):
	self._root = path
	self._files = None
	self.deep = deep
    def __iter__(self):
	return self
    def next(self):
	if self._files:
	    join = os.path.join
	    d = self._files.pop()
	    r = join(self._root, d)
	    if self.deep and os.path.isdir(r):
		self._files += [join(d,n) for n in os.listdir(r)]
	elif self._files is None:
	    self._files = os.listdir(self._root)
	if self._files:
	    return self._files[-1]
	else:
	    raise StopIteration


# modified from cookbook
def where(file, paths=None):
    if not paths:
        paths = os.environ["PATH"]
    matches = []
    for path in paths.split(";"):
        for match in glob.glob(os.path.join(path, file)):
            if match not in matches:
                matches.append(match)
    return matches


def loadLines(fname):
    try:
        f = open(fname, "r")
        data = f.readlines()
        data = [x.strip() for x in data]
    except:
        data = []
    return data

def saveLines(fname, data):
    f = open(fname, "w")
    data = [x + "\n" for x in data]
    f.writelines(data)
    f.close()
    
        
