import os,os.path,re,logging,sys,struct,math,traceback,urlparse
import pygtk
import inspect
import gobject,gtk.glade,gtk,aksy
import urllib 
from aksy.devices.akai import fileparser
import aksy.fileutils
from aksui.utils import modelutils
# TODO: is this still needed?
from aksui.postmod.itx import *

def get_file_path_from_dnd_dropped_uri(uri):
    path = uri.strip('\r\n\x00') # remove \r\n and NULL

    # get the path to file
    if path.startswith('file:\\\\\\'): # windows
        path = path[8:] # 8 is len('file:///')
    elif path.startswith('file://'): # nautilus, rox
        path = path[7:] # 7 is len('file://')
    elif path.startswith('file:'): # xffm
        path = path[5:] # 5 is len('file:')
        
    path = urllib.url2pathname(path) # escape special chars
    return path

def collect_files(args):
    collected = []
    for f in args:
        if os.path.isfile(f):
            if Sampler.is_filetype_supported(f):
                collected.append(f)
        elif os.path.isdir(f):
            collected.extend(collect_dir(f))
        else:
            raise IOError("File not found: " + repr(f))
    return collected

def collect_dir(args):
    for root, dir, files in os.walk(args):
        for found in files:
            if Sampler.is_filetype_supported(found):
                yield os.path.join(root, found)
 
def find_file(files, samplename):
    for f in files:
        filename = os.path.basename(f).lower()
        basename, ext = os.path.splitext(filename)
        if basename == samplename:
            return f
        
    # look for wav or aiff, using first file to get path
    basename, origext = os.path.split(files[0])
    exts = ['.wav','.aiff','.aif']
    for ext in exts:
        filename = basename + "\\" + samplename + ext
        if os.path.exists(filename):
            return filename
        else:
            print "Not found:", filename
    #raise IOError("File not found in upload file list: " + samplename)

class FileChooser:
    def __init__(self, s):
        self.s = s
        self.last_folder = None
        self.filechooser = gtk.FileChooserDialog(title="Open Sample", buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK)) 
        self.setup_filter(["*.AKP","*.AKM","*.WAV","*.AIF","*.AIFF","*.IT"], "All Supported Files")
        self.setup_filter(["*.AKM"], "Multis")
        self.setup_filter(["*.AKP",], "Programs")
        self.setup_filter(["*.WAV","*.AIF","*.AIFF"], "Samples")
        self.setup_filter(["*.IT"], "Impulse Tracker Modules")
        self.filechooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)

    def setup_filter(self, extensions, name = None):
        """ takes a list of extensions and sets the filefilter
        """
        self.filter = gtk.FileFilter()
        for ext in extensions:
            self.filter.add_pattern(ext)
            
        if name:
            self.filter.set_name(name)
            
        self.filechooser.add_filter(self.filter)
       
    def open(self, multiple = True, upload = False, action = gtk.FILE_CHOOSER_ACTION_OPEN, title = "Upload files..."):
        self.filechooser.set_action(action)
        self.filechooser.set_select_multiple(multiple)
        self.filechooser.set_title(title)

        # multiple files (up to 4) will be distributed across zones (?)
        if self.last_folder:
            self.filechooser.set_current_folder(self.last_folder)
        else:
            # pull last folder from INI
            self.filechooser.set_current_folder("/")

        response = self.filechooser.run()
        self.filechooser.hide()

        if response == gtk.RESPONSE_OK:
            self.updating = True
            if multiple:
                self.files = self.filechooser.get_filenames()
            else:
                self.files = [self.filechooser.get_filename(),]
            
            if upload:
                self.upload_files()
                
            if action != gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER:
                nameonly = os.path.basename(self.files[0])[:-4]
            else:
                nameonly = self.files[0]

            self.last_folder = self.filechooser.get_current_folder()

            if multiple:
                return self.files
            else:
                return nameonly

        elif response == gtk.RESPONSE_CANCEL:
            self.files = None
            return None

    def import_from_it(self, fn):
        it = ITX(fn)

        print fn, "loaded! exporting..."

        exported_files = it.exportSamples("c:\\tmp") # TODO: change to configurable temp dir

        resampled_path = None
        result = []

        for exported_file in exported_files:
            resampled_path = os.path.dirname(exported_file)
            resampled_name = sox.convert(exported_file)
            result.append(resampled_name)
                
            """
            if resampled_name:
                self.filechooser.upload(resampled_name, exported_file)
            else:
                pass
        if resampled_path:    
            print "Unlinking temp path", resampled_path
            print shutil.rmtree(resampled_path)
            """
            
        return result
    
    def upload_files(self):
        # hacky
        to_upload = self.files
        
        for f in self.files:
            if f:
                if f.lower().endswith(".akp"):
                    filterProgram = f
                    filtered = []
                    program = fileparser.ProgramParser().parse(filterProgram)
                    for kg in program.keygroups:
                        for zone in kg.zones:
                            if zone.samplename:
                                filtered.append(find_file(self.files, zone.samplename))
                    self.files.extend(filtered)
                    
        already_done = []
        for f in self.files:
            if f and not f in already_done:
                self.s.put(f)
                already_done.append(f)
                
        self.do_lists() 
            
    def do_lists(self):
        s = self.s
        setattr(s, 'samples', s.sampletools.get_names())
        setattr(s, 'programs', s.programtools.get_names())
        setattr(s, 'multis', s.multitools.get_names())

        setattr(s, 'samplesmodel', modelutils.get_model_from_list(s.samples, True))
        setattr(s, 'programsmodel', modelutils.get_model_from_list(s.programs))
        setattr(s, 'multismodel', modelutils.get_model_from_list(s.multis))
        
    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp):
        if target_type == 80: # TARGET_TYPE_URI_LIST
            uri = selection.data.strip()
            uris = uri.split() # we may have more than one file dropped
            files = []
            for uri in uris:
                path = get_file_path_from_dnd_dropped_uri(uri)
                if len(path):
                    print 'path to open', path
                    if os.path.isfile(path): # is it file?
                        files.append(path)
            if len(files) > 0:
                self.files = files
                self.upload_files()
                
    def expand_it_files(self, files):
        if files:
            additional_wavs = []
            for file in files:
                if file.lower().endswith('it'):
                    additional_wavs.extend(self.import_from_it(file))
                files.remove(file)
            files.extend(additional_wavs)
            print files
            return files
        else:
            return None