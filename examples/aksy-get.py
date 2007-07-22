#!/usr/bin/python

import os, os.path, fnmatch, sys 
from optparse import OptionParser

from aksy.device import Devices

__author__ = 'Walco van Loon'
__version__ = '0.01'

def create_option_parser(): 
    usage = """%prog [filename patterns]
    
    Download all program files and multis from memory:
    
    %prog *.akp *.akm
    
    Download the AUTOLOAD folder from disk:
    
    %prog -l disk Z48*/AUTOLOAD"""
    parser = OptionParser(usage=usage)
    parser.add_option("-t", nargs=1, dest="samplerType",
          help="Type of target sampler (z48/mpc4k/s56k)", default="z48")
    parser.add_option("-l", nargs=1, default="memory", dest="location",
          help="Download from location (memory or disk)")
    parser.add_option("-d", nargs=1, default=".", dest="destdir",
          help="The destination directory")
    parser.add_option("-o", default=False, dest="overwriteExisting",
          help="Whether to overwrite existing files")
    return parser

def download_from_memory(z48, destdir, patterns, overwrite):
    collected = [item.get_name() for item in z48.memory.get_children()]
    matched = []
    for pat in patterns:
        matched.extend(fnmatch.filter(collected, pat))
    
    if len(matched) == 0:
        return

    ensure_destdir(destdir)
    
    for name in matched:
        download(z48, destdir, name, z48.MEMORY, overwrite)

def download_from_disk(z48, destdir, patterns, overwrite):
    dir_patterns = patterns[0].split('/')
    download_children(z48, z48.disks, destdir, PatternYielder(dir_patterns), overwrite)

def download(z48, destdir, name, location, overwrite):
    destfile = os.path.join(destdir, name)
    if os.path.exists(destfile) and not overwrite:
        print "Skipping existing file ", destfile
    else:
        print "Downloading %s to %s" % (name, destfile)
        z48.get(name, destfile)

def download_children(z48, parent, destdir, patternYielder, overwrite):
    pat = patternYielder.next()
    filtered = [child for child in parent.get_children() if fnmatch.fnmatch(child.get_name(), pat)]

    fullpath = os.path.join(destdir, parent.get_name())

    if len(filtered) > 0:
        ensure_destdir(fullpath)
        
    for child in filtered:
        if child.has_children():
            download_children(z48, child, fullpath, patternYielder, overwrite)
        else:
            download(z48, fullpath, child.get_name(), z48.DISK, overwrite)

def process_cmdline():
    parser = create_option_parser()
    (options, patterns) = parser.parse_args()

    if len(patterns) == 0:
        patterns.append("*.wav")
    
    options.destdir = os.path.abspath(options.destdir)

    z48 = Devices.get_instance(options.samplerType, "usb")
    try:    
        execute_cmd(z48, patterns, options)
    finally:
        z48.close()

def execute_cmd(z48, patterns, options):
    if options.location == "memory":
        download_from_memory(z48, options.destdir, patterns, options.overwriteExisting)
    elif options.location == "disk":
        download_from_disk(z48, options.destdir, patterns, options.overwriteExisting)
    else:
        parser.error("Invalid location: %s" % options.location)


def ensure_destdir(destdir):
    if not os.path.exists(destdir):
        os.mkdir(destdir)
    
class PatternYielder:
    def __init__(self, patterns):
        self.patterns = patterns
        self.index = -1
    def next(self):
        try:
            self.index += 1
            print self.patterns[self.index]
            return self.patterns[self.index]
        except IndexError:
            return "*"

if __name__ == '__main__':
   process_cmdline()
