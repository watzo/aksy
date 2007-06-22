import os,os.path,re,logging,sys,struct,math,traceback,urlparse
import pygtk
import inspect
import gobject,gtk.glade,gtk,aksy

from postmod.itx import *

from utils import *
from utils import sox

from ak import program, zone, keygroup

class FileChooser:
    def __init__(self, s):
        self.s = s
        self.last_folder = None
        self.filechooser = gtk.FileChooserDialog(title="Open Sample", buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK)) 
        self.setup_filter(["*.AKP","*.AKM","*.WAV","*.AIF","*.AIFF","*.IT"], "Audio Files")
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
       
    def open(self, multiple = True, upload = False):
        self.filechooser.set_select_multiple(multiple)

        # multiple files (up to 4) will be distributed across zones (?)
        if self.last_folder:
            self.filechooser.set_current_folder(self.last_folder)
        else:
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
            
            nameonly = os.path.basename(self.files[0])[:-4]

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

    def upload(self, file, rename = None):
        if not rename:
            rename = file
        if file.lower().endswith('wav'):
            try:
                try:
                    """Try to open the wavefile up to ensure it's not corrupt.  
                    """
                    print "trying to open", file
                    #w = wave.open(file,'r')
                    #w.close()
                    # TODO: if files are 8-bit, use sox to convert to 16-bit
                    #if (w.getsampwidth() * 8) == 8:
                    #    print 'sox -b 16 ' + file
                finally:
                    basename = os.path.basename(rename)
                    try:
                        #print "Upload disabled"
                        self.s.put(file, basename)
                    except Exception, ex:
                        print "put Exception! ", ex
            except Exception, ex:
                print "wave Exception! ", ex

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
            
    def upload_files(self, find_dependants=False):
        """Traverses the filelist and uploads files.

        This should ultimately get wise and detect corrupt aiff/wav/akp/akm before it attempts to upload, and skip them as this seems to cause the sampler to become unresponsive for a bit.
        Also needs an implementation for find_dependants.
        """
        
        #self.files = self.expand_it_files(self.files)

        for file in self.files:
            if file:
                basename = os.path.basename(file)
                nameonly = os.path.basename(file)[:-4]
                try:
                    print "Trying to upload: ", file
                    self.upload(file)
    
                    n = basename.lower()
    
                    if n.endswith('akp'):
                        self.s.programsmodel.append([nameonly,0])
                    elif n.endswith('wav') or n.endswith('aif') or n.endswith('aiff'):
                        self.s.samplesmodel.append([nameonly,0])
                    elif n.endswith('akm'):
                        self.s.multismodel.append([nameonly,0])
    
                except Exception, ex:
                    print file, ex
    
