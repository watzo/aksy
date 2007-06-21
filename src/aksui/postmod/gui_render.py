
import renderers


class HasRenderOptions:

    def UpdateLoopControls(self):
        useloop = self.GetControl("UseLoopCount")
        loopcount = self.GetControl("LoopCount")
        if useloop:
            loopcount.Enable(useloop.GetValue())


    def UpdateSliceControls(self, disable=0, enable=0):
        renderslice = self.GetControl("RenderSlice")
        numslices = self.GetControl("NumSlices")
        kslices = self.GetControl("KeepSlices")
        if renderslice:
            if disable:
                renderslice.Enable(0)
                numslices.Enable(0)
                kslices.Enable(0)
            elif enable:
                renderslice.Enable(1)
                numslices.Enable(renderslice.GetValue())
                kslices.Enable(1)
            else:
                numslices.Enable(renderslice.GetValue())
                kslices.Enable(renderslice.GetValue())


    def UpdateAmplifyControl(self, normalize=-1):
        if normalize < 0:
            norm = self.GetControl("Normalize")
            normalize = norm.GetValue()
            
        ampcontrol = self.GetControl("Amplify")
        if ampcontrol:
            if normalize:
                ampcontrol.Enable(0)
            else:
                ampcontrol.Enable(1)

    def UpdateRenderOptions(self):
        dorender = self.GetControl("RenderFiles")
        render = self.GetControl("Renderer")
        amp = self.GetControl("Amplify")
        norm = self.GetControl("Normalize")
        inter = self.GetControl("InterpolationMode")
        srate = self.GetControl("SampleRate")
        brate = self.GetControl("BitRate")
        volramp = self.GetControl("VolumeRampMode")

        self.UpdateLoopControls()
        
        if dorender and not dorender.GetValue():
            render.Enable(0)
            norm.Enable(0)
            amp.Enable(0)
            inter.Enable(0)
            srate.Enable(0)
            brate.Enable(0)
            volramp.Enable(0)
            self.UpdateSliceControls(disable=1) 
            return 0
        else:
            render.Enable(1)

        r = renderers.getRenderer(render.GetSelection())
        norm.Enable(r.supportsNormalization())
        inter.Enable(1)
        srate.Enable(1)
        brate.Enable(1)
        amp.Enable(r.supportsVolumeSetting())
        volramp.Enable(r.supportsVolumeRamp())
        self.UpdateSliceControls(enable=1)   
        
        if r.supportsVolumeSetting():
            self.UpdateAmplifyControl()

        # update samplerate select box
        defsel = srate.GetSelection()
        cursel = srate.GetStringSelection()

        while srate.GetCount():
            srate.Delete(0)
        default = r.getDefaultSampleRate()[0]
        i = 0
        for sr in r.getSupportedSampleRates():
            selst = sr[0]
            srate.Append(selst)
            if selst == cursel:
                srate.SetSelection(i)
                # don't tread on me
                defsel = -1     
            elif selst == default and defsel != -1:
                # we'll set to defsel if current selection is unavailable in new list
                defsel = i
            i += 1
        if defsel > -1:
            srate.SetSelection(defsel)

        # update bitwidth select box
        defsel = brate.GetSelection()
        cursel = brate.GetStringSelection()

        while brate.GetCount():
            brate.Delete(0)
        default = r.getDefaultSampleWidth()[0]
        i = 0
        for br in r.getSupportedSampleWidths():
            selst = br[0]
            brate.Append(selst)
            if selst == cursel:
                brate.SetSelection(i)
                # don't tread on me
                defsel = -1     
            elif selst == default and defsel != -1:
                # we'll set to defsel if current selection is unavailable in new list
                defsel = i
            i += 1
        if defsel > -1:
            brate.SetSelection(defsel)

        # update interpolation select box
        defsel = inter.GetSelection()
        cursel = inter.GetStringSelection()

        while inter.GetCount():
            inter.Delete(0)
        default = r.getDefaultInterpolation()[0]
        i = 0
        for isets in r.getInterpolationSettings():
            selst = isets[0]
            inter.Append(selst)
            if selst == cursel:
                inter.SetSelection(i)
                # don't tread on me
                if cursel == "None":
                    defsel = -1     
            elif selst == default and defsel != -1:
                # we'll set to defsel if current selection is unavailable in new list
                defsel = i
            i += 1
        if defsel > -1:
            inter.SetSelection(defsel)


        # update volume ramp select box
        defsel = volramp.GetSelection()
        cursel = volramp.GetStringSelection()
        if not cursel:
            defsel = 1
        if cursel == 'Default' and r.supportsVolumeRamp():
            defsel = r.getDefaultVolumeRamp()[0][1]

        while volramp.GetCount():
            volramp.Delete(0)
        default = r.getDefaultVolumeRamp()[0]
        i = 0
        for isets in r.getVolumeRampSettings():
            selst = isets[0]
            volramp.Append(selst)
            if selst == cursel:
                volramp.SetSelection(i)
                # don't tread on me
                if cursel == "None":
                    defsel = -1     
            elif selst == default and defsel != -1:
                # we'll set to defsel if current selection is unavailable in new list
                defsel = i
            i += 1
        if defsel > -1:
            volramp.SetSelection(defsel)

