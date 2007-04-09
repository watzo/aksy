
import os, sys, imp, traceback
import filex


def importmodule(filename, modname):
    root, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == ".py":
        f = open(filename, "r")
        module = imp.load_source(modname, filename, f)
        f.close()
    elif ext in (".pyo",".pyc"):
        f = open(filename, "rb")
        module = imp.load_compiled(modname, filename, f)
        f.close()
    elif ext in (".pyd",".dll"):
        module = imp.load_dynamic(modname, filename)
    else:
        module = None

    return module 





def getPluginFileList(path):
    # valid plugins = .py, .pyc, .pyo
    plugins = filex.dirtree(path, "*.py") + filex.dirtree(path, "*.pyc") + filex.dirtree(path, "*.pyo")
    # remove .pyc files that have a matching .py or .pyo
    newlist = list(plugins)
    for f in plugins:
        root, ext = os.path.splitext(f)
        if ext == ".pyc":
            if root+".py" in plugins or root+".pyo" in plugins:
                newlist.remove(f)
        elif ext == ".pyo":
            if root+".py" in plugins:
                newlist.remove(f)
            
    return newlist                                                         


def loadPlugin(path):
    plug = importmodule(path, "plug")
    return plug
    
def getPluginList(path, test=1):
    plugins = []
    files = getPluginFileList(path)
    oldsyspath = list(sys.path)
    if test:
        for f in files:
            # plugin should have id, name, author, version, and plugin
            sys.path = [path] + sys.path
            #print "loading", f
            plug = importmodule(f, "plug")
            try:
                id, name, author, version, plugin = plug.id, plug.name, plug.author, plug.version, plug.plugin
                plugins.append((id, name, author, version, plugin))
            except AttributeError:
                # this plug failed
                print "-- Plugin", "'" + f + "'", "missing required attribute."
                #traceback.print_exc()
                pass
            
    sys.path = oldsyspath
    return plugins


PLUGINLIST = []

def loadPlugins(pluginpath):
    return 0
    # also see updatepluginsmenu
    
    print "loading plugins..."
    global PLUGINLIST
    PLUGINLIST = getPluginList(pluginpath)
    print PLUGINLIST
    return PLUGINLIST




if __name__ == "__main__":
    path = "c:\\dev\\postmod\\plugins"
    plugins = getPluginList(path)
    print plugins
    infile = "c:\\it\\test.it"
    outfile = "c:\\it\\testout.it"
    plg = loadPlugin("c:\\dev\\postmod\\plugins\\transposer\\transposizer.py")
    print "GOT PLUGIN", plg
    theplug = plg.plugin()
    theplug.processFile(infile, outfile)
    
