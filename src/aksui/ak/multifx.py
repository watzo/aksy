from aksui.utils import modelutils

class MultiFX:
    fxlist = [ 'NO EFFECT', 'CHORUS>MONO', 'CHORUS>STEREO', 'CHORUS>XOVER', 'CHORUS+DELAY', 'COMPRESSOR/LIMITER', 'DELAY>MONO', 'DELAY>MULTI TAP', 'DELAY>PAN', 'DELAY>PING PONG', 'DELAY>STEREO', 'DELAY>XOVER', 'DIGITAL EQ', 'DISTORTION', 'ENHANCER', 'EXPANDER', 'FLANGER>MONO', 'FLANGER>PAN', 'FLANGER>STEREO', 'FLANGER>XOVER', 'FLANGER+DELAY', 'NOISE GATE', 'PAN>AUTO PAN', 'PAN>TRIGGER PAN', 'PHASER>MONO', 'PHASER>PAN', 'PHASER>STEREO', 'PHASER>XOVER', 'PHASER+DELAY', 'PITCH CORRECTOR', 'PITCH SHIFTER', 'REVERB>AUDITORIUM', 'REVERB>BIG HALL', 'REVERB>BIG ROOM', 'REVERB>BRIGHT HALL', 'REVERB>DRUM BOOTH', 'REVERB>LIVE HOUSE', 'REVERB>MEDIUM HALL', 'REVERB>MEDIUM ROOM', 'REVERB>NON LINEAR', 'REVERB>PLATE 1', 'REVERB>PLATE 2', 'REVERB>REVERSE', 'REVERB>SMALL HALL', 'REVERB>SMALL ROOM', 'REVERB>STUDIO', 'REVERB>THEATER', 'REVERB>VOCAL PLATE', 'REVERB>WAREHOUSE', 'ROTARY SPEAKER', 'TAPE ECHO', 'WAH>AUTO WAH', 'WAH>TOUCH WAH' ]

    def __init__(self,s):
        # store sampler
        if s:
            self.s = s
        else:
            self.s = None

        self.update()

        for ci in self.channels:
            channel = self.channels[ci]
            #channel.dump() 


    def update(self):
        if self.s:
            # on eb4js seems to be multiple channels and 1 module per channel
            self.channels = { }
            self.no_channels = self.s.multifxtools.get_no_channels()
            for ci in range(self.no_channels):
                self.channels[ci] = MultiFXChannel(self,ci)                

class MultiFXEffect:
    def __init__(self,name,id,param_index_output_ctrl):
        self.name = name
        self.id = id
        # parameter index for output control
        self.param_index_output_ctrl = param_index_output_ctrl

class MultiFXChannel:
    # parameters
    # effect name
    # which channel

    outputmap = ['off','L-R','1-2','3-4','5-6','7-8','L','R','1','2','3','4','5','6','7','8']
    inputmap = ['SEND A','SEND B','SEND C','SEND D','FX1','FX2','FX3','FX4']

    def __init__(self,mfx,index):
        self.mfx = mfx
        self.s = mfx.s
        s = self.s
        self.index = index
        self.max_modules = s.multifxtools.get_max_modules(index)
        self.muted = s.multifxtools.is_channel_muted(index)
        self.input = s.multifxtools.get_channel_input(index)
        self.output = s.multifxtools.get_channel_output(index)
        self.modules = { }


        for i in range(self.max_modules):
            self.modules[i] = MultiFXModule(self,i)

    def dump(self):
        attrs = ['index','muted','input','output']
        for attr in attrs:
            print 'Param ',self.index,' :',attr,' = ',getattr(self,attr)

        for mi in self.modules:
            module = self.modules[mi]
            module.dump()

    def updateInput(self,i):
        return self.s.multifxtools.set_channel_input(self.index,i)

    def updateOutput(self,i):
        return self.s.multifxtools.set_channel_output(self.index,i)
        
       
class MultiFXModule:
    def __init__(self,c,i):
        self.s = c.mfx.s
        s = c.mfx.s
        self.mfx = c.mfx
        self.channel = c
        self.index = i

        self.update_name()
        self.update()

    def setEffectById(self,id):
        c = self.channel
        tools = self.s.multifxtools

        ret = tools.set_fx_by_id(c.index,self.index,id)

        self.update_name()
        self.update()
        return ret

    def enable(self):
        c = self.channel
        tools = self.s.multifxtools
        return tools.enable_module(c.index,self.index,True)

    def disable(self):
        c = self.channel
        tools = self.s.multifxtools
        return tools.enable_module(c.index,self.index,False)

    def update_name(self):
        i,s,c =self.index,self.s,self.channel

        self.effect_name = s.multifxtools.get_by_name(c.index,i)
        self.effect_index = s.multifxtools.get_by_index(c.index,i)
        
    def update(self):
        c = self.channel
        s = c.mfx.s
        i = self.index

        self.enabled = s.multifxtools.is_module_enabled(c.index,i)
        self.number_of_parameters = s.multifxtools.get_number_of_parameters(c.index,i)
        self.parameters = { }

        for pi in range(self.number_of_parameters):
            self.parameters[pi] = MultiFXParam(s,c,self,pi)

    def dump(self):
        attrs = ['effect_name','enabled','number_of_parameters']
        for attr in attrs:
            print '\tParam ',self.index,' :',attr,' = ',getattr(self,attr)
        for pi in self.parameters:
            param = self.parameters[pi]
            param.dump()

class MultiFXParam:
    def __init__(self,s,channel,module,index):
        self.channel = channel
        self.s = channel.s
        self.module = module
        self.index = index

        ci = self.channel.index
        mi = self.module.index
        pi = self.index

        self.maximum = s.multifxtools.get_parameter_maximum(ci,mi,pi)
        self.minimum = s.multifxtools.get_parameter_minimum(ci,mi,pi)
        self.name = s.multifxtools.get_parameter_name(ci,mi,pi)
        self.units = s.multifxtools.get_parameter_units(ci,mi,pi)
        self.type = s.multifxtools.get_parameter_type(ci,mi,pi)
        self.template = s.multifxtools.get_display_template(ci,mi,pi)
        self.position_id = s.multifxtools.get_parameter_position_id(ci,mi,pi)
        self.value = s.multifxtools.get_param_value(ci,mi,pi)
        self.string = s.multifxtools.get_param_string(ci,mi,pi)
        self.qlink = s.multifxtools.get_param_qlinkctrl(ci,mi,pi)

        formatmap = {None:"%(value)d%(units)s",'':"%(value)d%(units)s"," 0.0":"%(value).1f%(units)s","  0.00":"%(value).2f%(units)s","   0":"%(value)d%(units)s","  0":"%(value)d%(units)s"}
        self.format = formatmap[self.template]

    def format_value(self):
        s = self.s
        ci = self.channel.index
        mi = self.module.index
        pi = self.index

        value = self.value

        if self.template == " 0.0":
            value /= 10
        elif self.template == "  0.00":
            value /= 100

        if self.string:
            formatted = self.string 
        else:
            formatted = self.format % {"value":value, "units":self.units}
       
        return formatted

    def on_value_changed(self, adj, lblFormat = None):
        s,ci,mi,pi = self.s,self.channel.index,self.module.index,self.index
        s.multifxtools.set_param_value(ci,mi,pi,int(adj.value))

        self.value = adj.value

        if self.string:
            self.string = s.multifxtools.get_param_string(ci,mi,pi)

        lblFormat.set_text(self.format_value())

    def dump(self):
        attrs = ['maximum','minimum','name','type','position_id']
        for attr in attrs:
            print '\t\tParam ',self.index,' :',attr,' = ',getattr(self,attr)

inputmapmodel = modelutils.get_model_from_list(MultiFXChannel.inputmap)
outputmapmodel = modelutils.get_model_from_list(MultiFXChannel.outputmap)
effectmodel = modelutils.get_model_from_list(MultiFX.fxlist)
