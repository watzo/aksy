
""" Python equivalent of akai section recordingtools

Methods to facilitate recording
"""

__author__ =  'Walco van Loon'
__version__=  '0.1'

import aksy.sysex

class Recordingtools:
     def __init__(self, z48):
          self.z48 = z48
          self.commands = {}
          self.command_spec = aksy.sysex.CommandSpec('\x47\x5f\x00', aksy.sysex.CommandSpec.ID, aksy.sysex.CommandSpec.ARGS)

