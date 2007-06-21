import sys
import gtk, pango
from gettext import gettext as _
from cStringIO import *
import traceback

def _info(type, value, tb):
    dialog = gtk.MessageDialog(parent=None,
			       flags=0,
			       type=gtk.MESSAGE_WARNING,
			       buttons=gtk.BUTTONS_NONE,
			       message_format=_(
	"<big><b>A programming error has been detected during the execution of this program.</b></big>"
	"\n\nIt probably isn't fatal, but should be reported to the developers nonetheless."))
    dialog.set_title(_("Bug Detected"))
    dialog.set_property("has-separator", False)
    dialog.vbox.get_children()[0].get_children()[1].set_property("use-markup", True)

    dialog.add_button(_("Show Details"), 1)
    dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)

    # Details
    textview = gtk.TextView(); textview.show()
    textview.set_editable(False)
    textview.modify_font(pango.FontDescription("Monospace"))
    sw = gtk.ScrolledWindow(); sw.show()
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    sw.add(textview)
    frame = gtk.Frame();
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.add(sw)
    frame.set_border_width(6)
    dialog.vbox.add(frame)
    textbuffer = textview.get_buffer()
    trace = StringIO()
    traceback.print_exception(type, value, tb, None, trace)
    textbuffer.set_text(trace.getvalue())
    textview.set_size_request(gtk.gdk.screen_width()/2, gtk.gdk.screen_height()/3)

    dialog.details = frame
    dialog.set_position(gtk.WIN_POS_CENTER)
    dialog.set_gravity(gtk.gdk.GRAVITY_CENTER)
    
    while 1:
	resp = dialog.run()
	if resp == 1:
	    dialog.details.show()
	    dialog.action_area.get_children()[1].set_sensitive(0)
	else: break
    dialog.destroy()
    

sys.excepthook = _info


