import wx
from wx import py 
from wxPython.wx import wxPySimpleApp, wxFrame,wxID_ANY,wxDEFAULT_FRAME_STYLE,wxNO_FULL_REPAINT_ON_RESIZE,wxMenu
from wxPython.wx import wxNewId,wxMenuBar,EVT_MENU, EVT_CLOSE, wxMessageDialog, wxOK, wxSplitterWindow
from wxPython.wx import WXK_TAB
from aksy.device import Devices
import sys

intro = 'Welcome to the Aksy python shell' 
ID_ABOUT=wxNewId()
ID_EXIT=wxNewId()

class Frame(wxFrame):
    def __init__(self,parent,title):
        wxFrame.__init__(self,parent,wxID_ANY, title, size = ( 200,100),
                         style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)

        filemenu= wxMenu()
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit\tCtrl+Q"," Terminate the program")

        helpmenu = wxMenu()
        helpmenu.Append(ID_ABOUT, "&About"," Information about this program")

        menuBar = wxMenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar)
        self.SetSize((800, 600))
        self.Show(True)
        EVT_MENU(self, ID_EXIT, self.OnExit)
        EVT_MENU(self, ID_ABOUT, self.OnAbout)

        EVT_CLOSE(self, self.OnExit)

    def OnExitMenu(self,e):
        self.on_exit()
        self.Close(True)

    def OnExit(self,e):
        self.on_exit()
        self.Destroy()

    def OnAbout(self,e):
        d= wxMessageDialog(self, " Aksy, controlling your Z48 sampler\n", "About Aksy", wxOK)
        d.ShowModal()
        d.Destroy()

    def on_exit(self):
        """
        """

class Interpreter(py.interpreter.Interpreter):
    def __init__(self, locals=None, rawin=None,
                 stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        py.interpreter.InteractiveInterpreter.__init__(self, locals=locals)
        self.stdin = stdin
        self.locals = locals
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.more = 0
        self.commandBuffer = []
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = '>>> '
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = '... '
        self.startupScript = '~/.aksyrc' 

    def getAutoCompleteKeys(self):
        return [ord('.'), WXK_TAB]

    def getAutoCompleteList(self, command='', *args, **kw):
        clist = py.interpreter.Interpreter.getAutoCompleteList(self, command, args, kw)
        print repr(clist)
        return clist

class AksyShell(wx.SplitterWindow):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.SP_3D,
                 name='Aksy', rootObject=None, rootLabel=None,
                 rootIsNamespace=True, intro='', locals=None,
                 InterpClass=None, *args, **kwds):
        wx.SplitterWindow.__init__(self, parent, id, pos, size, style, name)
        self.shell = py.shell.Shell(parent=self, introText=intro,
                           locals=locals, InterpClass=Interpreter,
                           *args, **kwds)

        self.editor = self.shell
        self.notebook = wx.Notebook(parent=self, id=-1)
        #self.filling = py.filling.Filling(parent=self.notebook,
        #                       rootObject=rootObject,
        #                       rootLabel=rootLabel,
        #                       rootIsNamespace=rootIsNamespace)
        # Add aksy vars
        self.shell.interp.introText = intro
        self.shell.interp.copyright = '' 
        self.shell.interp.locals['z48'] = rootObject
        
        # Add programs, samples, multis in memory
        # self.notebook.AddPage(page=self.filling, text='Namespace', select=True)
        self.SplitHorizontally(self.shell, self.notebook, 300)
        self.SetMinimumPaneSize(1)

if __name__ == '__main__':
    app = wxPySimpleApp()
    frame = Frame(None, "Aksy")
    root = Devices.get_instance('mock_z48')
    win = AksyShell(
            frame, intro=intro, rootLabel="Z48",
            rootIsNamespace=True, rootObject=root)
    app.MainLoop()
