
# consider removing options.Renderers, or at least not storing full path
# should just join filename with ToolsPath at use-time.

import os
import filex

class Renderer:
    def __init__(self):
        self.internal = 0
        pass

    def getSampleRateName(self, value):
        for sr in self.sampleRates:
            if sr[1] == value:
                return sr[0]

        return ""            

    def getBitRateName(self, value):
        for sw in self.sampleWidths:
            if sw[1] == value:
                return sw[0]

        return ""            

    def getInterpolationName(self, value):
        for i in self.interpolations:
            if i[1] == value:
                return i[0]

        return ""            




    def supportsInternalRender(self):
        return self.internal

    def usesPostNormalize(self):
        return self.post_normalize

    def getCode(self):
        if hasattr(self, "code"):
            return self.code
        else:
            return self.name

    def getSupportedSampleRates(self):
        return self.sampleRates

    def getDefaultSampleRate(self):
        return self.defaultSampleRate

    def getSupportedBitRates(self):
        return self.sampleWidths

    getSupportedSampleWidths = getSupportedBitRates    

    def getDefaultBitRate(self):
        return self.defaultSampleWidth

    getDefaultSampleWidth = getDefaultBitRate

    def supportsNormalization(self):
        return self.support_normalization

    def supportsVolumeSetting(self):
        return self.support_volume_setting

    def supportsVolumeRamp(self):
        return self.support_volume_ramp

    def getVolumeRange(self):
        return self.volumeRange

    def getInterpolationSettings(self):
        return self.interpolations

    def getDefaultInterpolation(self):
        return self.defaultInterpolation


    def getVolumeRampSettings(self):
        return self.volumeramps

    def getDefaultVolumeRamp(self):
        return self.defaultVolumeRamp


    def getNormalizeFile(self):
        return self.normalizeFile

    def getProgressFile(self):
        return self.progressFile

    def getCommandLine(self, path, fromfile="", tofile="", normalize=1, volume=None, interpolation=1, getNormalize=0, sampleRate=None, sampleWidth=None):
        return None
            


class MIKMODRenderer(Renderer):
    def __init__(self):
        self.name = "Mikmod 3.0.3"
        self.filename = "mikwav.exe"

        self.sampleRates = (('44100',44100),)
        self.defaultSampleRate = ('44100',44100)
        self.sampleWidths = (('16 bit',16),)
        self.defaultSampleWidth = ('16 bit',16)

        self.support_normalization = 0
        self.support_volume_setting = 0
        self.volumeRange = (0,100)

        self.interpolations = (('Default', 0),)
        self.defaultInterpolation = ('Default', 0)

        self.support_volume_ramp = 0
        self.volumeramps = (('Default', 0),)
        self.defaultVolumeRamp = (('Default', 0),)

        self.normalizeFile = "mikwav.amp"
        self.progressFile = "mikwav.txt"

        self.internal = 0
        self.post_normalize = 1

    def getCommandLine(self, path, fromfile="", tofile="", normalize=1, volume=None, interpolation=1, getNormalize=0, sampleRate=None, sampleWidth=None):
        # mikwav file.it file.wav
        # only supports fromfile and tofile
        cl = os.path.join(path, self.filename) + " "
        if not tofile:
            tofile = filex.filebase(fromfile) + ".wav"
        cl += fromfile + " " + tofile
        return cl


class MODPLUGRenderer(Renderer):
    def __init__(self):
        self.name = "Modplug 1.16"
        self.code = "MODPLUG"
        self.filename = ""

        self.sampleRates = (('8000',8000),('11025',11025),('22050',22050),('32000',32000),('44100',44100),('48000',48000),('88200',88200),('96000',96000))
        self.defaultSampleRate = ('44100',44100)
        self.sampleWidths = (('16 bit',16),)
        self.defaultSampleWidth =('16 bit',16)

        self.support_normalization = 1
        self.support_volume_setting = 1
        self.volumeRange = (0,100)

        self.interpolations = (('None', 0), ('Linear', 1), ('Cubic', 2), ('8-tap FIR', 3))
        self.defaultInterpolation = ('8-tap FIR', 3)

        self.support_volume_ramp = 0
        self.volumeramps = (('Default', 0),)
        self.defaultVolumeRamp = (('Default', 0),)

        self.normalizeFile = ""
        self.progressFile = ""

        self.internal = 1        
        self.post_normalize = 1



class BASSRenderer(Renderer):
    def __init__(self):
        self.name = "BASS 2.0"
        self.filename = ""
        self.code = "BASS"

        self.sampleRates = (('8000',8000),('11025',11025),('22050',22050),('32000',32000),('44100',44100),('48000',48000),('88200',88200),('96000',96000))
        self.defaultSampleRate = ('44100',44100)
        self.sampleWidths = (('16 bit',16),('32 bit IEEE',32))
        self.defaultSampleWidth =('16 bit',16)

        self.support_normalization = 1
        self.support_volume_setting = 1
        self.volumeRange = (0,100)

        self.interpolations = (('None', 0), ('Linear', 1))
        self.defaultInterpolation = ('Linear', 1)

        self.support_volume_ramp = 1
        self.volumeramps = (('None', 0), ('Normal', 1), ('Smoother', 2))
        self.defaultVolumeRamp = (('Normal', 1),)

        self.normalizeFile = ""
        self.progressFile = ""

        self.internal = 1        
        self.post_normalize = 0



class DUMBRenderer(Renderer):
    def __init__(self):
        self.name = "DUMB 0.9.2"
        self.filename = "dumbwav.exe"

        self.sampleRates = (('8000',8000),('11025',11025),('22050',22050),('32000',32000),('44100',44100),('48000',48000),('88200',88200),('96000',96000))
        self.defaultSampleRate = ('44100',44100)
        #self.sampleWidths = (('8 bit',8),('16 bit',16))
        self.sampleWidths = (('16 bit',16),)
        self.defaultSampleWidth =('16 bit',16)

        self.support_normalization = 1
        self.support_volume_setting = 1
        self.volumeRange = (0,128)

        self.interpolations = (('None', 0), ('Linear', 1), ('Cubic', 2))
        self.defaultInterpolation = ('Cubic', 2)

        self.support_volume_ramp = 0
        self.volumeramps = (('Default', 0),)
        self.defaultVolumeRamp = (('Default', 0),)

        self.normalizeFile = "dumbwav.amp"
        self.progressFile = "dumbwav.txt"

        self.internal = 0        
        self.post_normalize = 1


    def getCommandLine(self, path, fromfile="", tofile="", normalize=1, volume=None, interpolation=1, getNormalize=0, sampleRate=None, sampleWidth=None):
        cl = os.path.join(path, self.filename) + " "
        if normalize:
            cl += "-n "
        if volume and volume > -1:
            cl += "-x " + str(volume) + " "
        cl += "-r " + str(interpolation) + " "
        if getNormalize:
            cl += "-k "
        if sampleRate:
            cl += "-s " + str(sampleRate) + " "
        if tofile:
            cl += "-o " + tofile + " "
        cl += fromfile
        return cl



RENDERERS = [MODPLUGRenderer(), BASSRenderer(), DUMBRenderer(), MIKMODRenderer()]

def getRenderers():
    return RENDERERS

def getRendererNames():
    return [r.name for r in RENDERERS]

def getRenderer(index):
    return RENDERERS[index]

def render(index, fromfile, tofile, normalize=1, volume=None, interpolation=1, getNormalize=0, sampleRate=None, sampleWidth=None, volramp=1):
    r = getRenderer(index)
    r.render(fromfile, tofile, normalize, volume, interpolation, getNormalize, volramp)

