import os,os.path,re,logging,sys,struct,math,traceback,urlparse
import pygtk
import inspect
import gobject,gtk.glade,gtk,aksy

from ak import program, zone, keygroup

class filechooser:
    def __init__(self, s):
        self.s = s
        self.last_folder = None
        self.filechooser = gtk.FileChooserDialog(title="Open Sample", buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK)) 
        self.setup_filter(["AKP","AKM","WAV","AIF","AIFF"])
        self.filechooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)

    def setup_filter(self, extensions):
        """ takes a list of extensions and sets the filefilter
        """
        self.filter = gtk.FileFilter()
        self.filter.add_pattern('|'.join(extensions))
        self.filechooser.add_filter(self.filter)
       
    def open(self, multiple = True, upload = False):
        self.filechooser.set_select_multiple(multiple)

        # multiple files (up to 4) will be distributed across zones (?)
        if self.last_folder:
            self.filechooser.set_current_folder(self.last_folder)
        else:
            self.filechooser.set_current_folder("/mnt/musicgiv/work")

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

    def upload(self, file):
        if file.lower().endswith('wav'):
            try:
                try:
                    """Try to open the wavefile up to ensure it's not corrupt.  
                    """
                    #print "trying to open"
                    #w = wave.open(file,'r')
                    #w.close()
                    # TODO: if files are 8-bit, use sox to convert to 16-bit
                    #if (w.getsampwidth() * 8) == 8:
                    #    print 'sox -b 16 ' + file
                finally:
                    basename = os.path.basename(file)
                    try:
                        #print "Upload disabled"
                        self.s.put(file, basename)
                    except Exception, ex:
                        print "put Exception! ", ex
            except Exception, ex:
                print "wave Exception! ", ex

    def upload_files(self, find_dependants=False):
        """Traverses the filelist and uploads files.

        This should ultimately get wise and detect corrupt aiff/wav/akp/akm before it attempts to upload, and skip them as this seems to cause the sampler to become unresponsive for a bit.
        Also needs an implementation for find_dependants.
        """

        files = self.files
        for file in files:
            basename = os.path.basename(file)
            nameonly = os.path.basename(file)[:-4]
            try:
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
