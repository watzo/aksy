import pygtk
import gobject,gtk.glade,gtk

from ak.program import *
from ak.zone import *
from ak.keygroup import *

"""
This should give 4 dropdowns per pad w/ a ... browser.

Should be limited to 'DRUM' programs cuz overlaps in KEY programs will cause problems.
Should have an option for 'load samples as pads' and 'append samples as pads'.
'LOAD' will start at the first keygroup and iterate through kgs.
'APPEND' will bypass all keygroups with any samples in zone 1 and
start filling in samples in the first empty keygroup and iterate through kgs. 
"""
