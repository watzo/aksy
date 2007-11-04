import gtk

from aksui.ak import multifx
from aksui.utils import modelutils

class MultiFXChannelEditor(gtk.VBox):
    def __init__(self,mMultiFXChannelEditor):
        gtk.VBox.__init__(self)
        self.mMultiFXChannelEditor = mMultiFXChannelEditor
        self.channel = mMultiFXChannelEditor

        self.moduleWidgets = { }

        self.topHBox = gtk.HBox(True)

        self.inputComboBox = modelutils.magicCombo(multifx.inputmapmodel,self.channel.input,self.on_input_changed,2)
        self.topHBox.pack_start(self.inputComboBox)

        self.outputComboBox = modelutils.magicCombo(multifx.outputmapmodel,self.channel.output,self.on_output_changed,3)
        self.topHBox.pack_start(self.outputComboBox)

        self.pack_start(self.topHBox)

        for i in range(self.mMultiFXChannelEditor.max_modules):
            self.moduleWidgets[i] = MultiFXModuleEditor(mMultiFXChannelEditor.modules[i])
            self.pack_start(self.moduleWidgets[i], expand=False, fill=False)

    def on_input_changed(self, widget):
        self.channel.updateInput(widget.get_active())

    def on_output_changed(self, widget):
        self.channel.updateOutput(widget.get_active())

class MultiFXModuleEditor(gtk.VBox):
    def __init__(self,module):
        gtk.VBox.__init__(self)
        self.module = module

        self.parameterWidgets = { }

        self.topHBox = gtk.HBox()

        self.effectsComboBox = modelutils.magicCombo(multifx.effectmodel,self.module.effect_index,self.on_changed,4)
        self.topHBox.pack_start(self.effectsComboBox)

        self.enableButton = gtk.ToggleButton('Enable')

        if self.module.enabled:
            self.enableButton.set_active(1)
        else:
            self.enableButton.set_active(0)

        self.enableButton.connect('toggled', self.on_toggle)

        self.topHBox.pack_start(self.enableButton, expand=False, fill=False)

        self.pack_start(self.topHBox)
        self.updateWidgets()

    def on_toggle(self, widget):
        if(widget.get_active()):
            self.module.enable()
        else:
            self.module.disable()

    def on_changed(self, widget):
        active_index = widget.get_active()
        self.module.setEffectById(active_index)
        self.updateWidgets()

    def updateWidgets(self):
        module = self.module

        for i in self.parameterWidgets:
            self.parameterWidgets[i].destroy()

        self.parameterWidgets = { }

        for i in module.parameters:
            w = MultiFXParameter(module.parameters[i])
            self.parameterWidgets[i] = w

        for i in self.parameterWidgets:
            w = self.parameterWidgets[i]
            self.pack_start(w, expand=False, fill=False)

        self.show_all()

class MultiFXParameter(gtk.HBox):
    def __init__(self,param):
        gtk.HBox.__init__(self, True)
        self.param = param

        self.lblFormat = gtk.Label(param.format_value())

        paramap = {'name':gtk.Label, 'value':gtk.HScale}

        for n in paramap:
            t = paramap[n]

            if t == gtk.Label:
                arg0 = getattr(param,n)
            elif t == gtk.HScale:
                arg0 = gtk.Adjustment(int(param.value),int(param.minimum),int(param.maximum)+1,0.01,1,1)
                arg0.connect('value_changed', param.on_value_changed, self.lblFormat)

            setattr(self,'_param'+n, t(arg0))
            o = getattr(self,'_param'+n)

            if t == gtk.HScale:
                o.set_digits(0)
                o.set_value_pos(gtk.POS_BOTTOM)
                o.set_draw_value(False)

            self.pack_start(o)

        self.pack_start(self.lblFormat)

class MultiFXLabel(gtk.Label):
    def __init__(self,text):
        gtk.Label.__init__(self,text)
        self.justify = gtk.JUSTIFY_LEFT

class MultiFXEditor(gtk.VBox):
    def __init__(self,s):
        gtk.VBox.__init__(self)
        self.mfx = multifx.MultiFX(s)

        self.channelWidgets = { }
      
        if self.mfx.channels:
            for i in self.mfx.channels:
                self.channelWidgets[i] = MultiFXChannelEditor(self.mfx.channels[i])
                self.pack_start(self.channelWidgets[i], expand=False, fill=False)
        else:
            print "nop"

