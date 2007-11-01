#!/usr/bin/python

import os, os.path, fnmatch, sys 

from aksy.device import Devices
from aksy import config

__author__ = 'Walco van Loon'
__version__ = '0.01'

def create_option_parser(): 
    usage = """%prog [filename patterns]
    
    Download all program files and multis from memory:
    
    %prog *.akp *.akm
    
    Download the AUTOLOAD folder from disk:
    
    %prog -l disk sampler*/AUTOLOAD"""
    parser = config.create_option_parser(usage=usage)
    parser.add_option("-l", nargs=1, default="memory", dest="location",
          help="Download from location (memory or disk)")
    parser.add_option("-d", nargs=1, default=".", dest="destdir",
          help="The destination directory")
    parser.add_option("-o", default=False, dest="overwriteExisting",
          help="Whether to overwrite existing files")
    return parser

def download_from_memory(sampler, destdir, patterns, overwrite):
    collected = [item.get_name() for item in sampler.memory.get_children()]
    matched = []
    for pat in patterns:
        matched.extend(fnmatch.filter(collected, pat))
    
    if len(matched) == 0:
        return

    ensure_destdir(destdir)
    
    for name in matched:
        download(sampler, destdir, name, sampler.MEMORY, overwrite)

def download_from_disk(sampler, destdir, patterns, overwrite):
    dir_patterns = patterns[0].split('/')
    download_children(sampler, sampler.disks, destdir, PatternYielder(dir_patterns), overwrite)

def download(sampler, destdir, name, location, overwrite):
    destfile = os.path.join(destdir, name)
    if os.path.exists(destfile) and not overwrite:
        print "Skipping existing file ", destfile
    else:
        print "Downloading %s to %s" % (name, destfile)
        sampler.transfertools.get(name, destfile)

def download_children(sampler, parent, destdir, patternYielder, overwrite):
    pat = patternYielder.next()
    filtered = [child for child in parent.get_children() if fnmatch.fnmatch(child.get_name(), pat)]

    fullpath = os.path.join(destdir, parent.get_name())

    if len(filtered) > 0:
        ensure_destdir(fullpath)
        
    for child in filtered:
        if child.has_children():
            download_children(sampler, child, fullpath, patternYielder, overwrite)
        else:
            download(sampler, fullpath, child.get_name(), sampler.DISK, overwrite)

def main():
    parser = create_option_parser()
    (options, patterns) = parser.parse_args()

    if len(patterns) == 0:
        patterns.append("*.wav")
    
    options.destdir = os.path.abspath(options.destdir)

    sampler = Devices.get_instance(options.sampler_type, options.connector)
    try:    
        execute_cmd(sampler, patterns, options)
    finally:
        sampler.close()

def execute_cmd(sampler, patterns, options):
    if options.location == "memory":
        download_from_memory(sampler, options.destdir, patterns, options.overwriteExisting)
    elif options.location == "disk":
        download_from_disk(sampler, options.destdir, patterns, options.overwriteExisting)
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

