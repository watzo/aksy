# -*- coding: latin-1 -*-
import os,os.path

from aksy.device import Devices
from aksy import config
from aksy.devices.akai.sampler import Sampler
from aksy.devices.akai import fileparser
import aksy.fileutils

__author__ = 'Joseph Misra/Walco van Loon'
__version__ = '0.01'

def create_option_parser(): 
    usage = "%prog [files|folders]"
    parser = config.create_option_parser(usage)
    parser.add_option("-p", nargs=1, dest="programName",
          help="Upload the specified program and the samples it references")
    parser.add_option("-d", nargs=1, dest="drumProgramName",
          help="Create and upload a new drum program from files using a specific naming scheme")
    return parser

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
                  
def main():
    parser = create_option_parser()
    (options, filelist) = parser.parse_args()

    if len(filelist) == 0:
        parser.error("At least one or more files/directories should be specified")
  
    to_upload = collect_files(filelist)
    
    if len(to_upload) == 0:
        parser.error("Nothing to upload: no supported files found")
    
    z48 = Devices.get_instance(options.sampler_type, options.connector)    
    
    if options.programName is not None:
        print 'Uploading files.'
        upload_files(z48, to_upload, filterProgram=options.programName)
    elif options.drumProgramName:
        print 'Uploading files.'
        print 'Building drum program.', options.drumProgramName
        build_drum_program(z48, to_upload, options.drumProgramName)
        upload_files(z48, to_upload, filterProgram=options.drumProgramName)
    else:
        upload_files(z48, to_upload)

def build_drum_program(z48, filelist, program_name):
    # create drum program named program_name
    # iterate through arguments and set each sample name to its key
    bankmap = {"A":0, "B":1, "C":2, "D":3}
    keymap = []
    for file in filelist:
        base, name = os.path.splitext(file)
        bank = bankmap[name[0]]
        bankindex = int(name[1:]) - 1
        midinote = mpcpads[(bank * 16) + bankindex]
        keymap.append([name, midinote])
        
    programs = z48.programtools.get_names()
    if not program_name in programs:
        z48.programtools.create_new(1, program_name)
    z48.programtools.set_curr_by_name(program_name)
    z48.programtools.set_type(1) # should make 128 keygroups?
    
    p = program(z48,program_name)
    
    for name, midinote in keymap:
        kg = keygroup(p, midinote)
        print midinote, name
        kg.zones[0].set("sample", program_name + " " + name)
        kg.zones[0].set("playback", 1)
        kg.set("polyphony", 1)
        
    # set hihat mute group
    kg = keygroup(p, 46)
    kg.set("mute_group", 1)
    kg = keygroup(p, 42)
    kg.set("mute_group", 1)
    # set this on program
    
def upload_files(z48, to_upload, filterProgram=None):
    if filterProgram is not None:
        filtered = []
        program = fileparser.ProgramParser().parse(filterProgram)
        for kg in program.keygroups:
            for zone in kg.zones:
                if zone.samplename:
                    filtered.append(find_file(to_upload, zone.samplename))
        to_upload = filtered
    
    for file in to_upload:
        z48.transfertools.put(file)

def find_file(files, samplename):
    for f in files:
        filename = os.path.basename(f).lower()
        basename, ext = os.path.splitext(filename)
        if basename == samplename:
            return f
    raise IOError("File not found in upload file list: " + samplename)
