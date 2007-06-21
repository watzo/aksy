# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _libmodplug2
def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class _ModPlugFile(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, _ModPlugFile, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, _ModPlugFile, name)
    __swig_setmethods__["mSoundFile"] = _libmodplug2._ModPlugFile_mSoundFile_set
    __swig_getmethods__["mSoundFile"] = _libmodplug2._ModPlugFile_mSoundFile_get
    if _newclass:mSoundFile = property(_libmodplug2._ModPlugFile_mSoundFile_get,_libmodplug2._ModPlugFile_mSoundFile_set)
    def __init__(self,*args):
        _swig_setattr(self, _ModPlugFile, 'this', apply(_libmodplug2.new__ModPlugFile,args))
        _swig_setattr(self, _ModPlugFile, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete__ModPlugFile):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C _ModPlugFile instance at %s>" % (self.this,)

class _ModPlugFilePtr(_ModPlugFile):
    def __init__(self,this):
        _swig_setattr(self, _ModPlugFile, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, _ModPlugFile, 'thisown', 0)
        _swig_setattr(self, _ModPlugFile,self.__class__,_ModPlugFile)
_libmodplug2._ModPlugFile_swigregister(_ModPlugFilePtr)

ModPlug_Load = _libmodplug2.ModPlug_Load

ModPlug_Unload = _libmodplug2.ModPlug_Unload

ModPlug_Read = _libmodplug2.ModPlug_Read

ModPlug_GetName = _libmodplug2.ModPlug_GetName

ModPlug_GetLength = _libmodplug2.ModPlug_GetLength

ModPlug_Seek = _libmodplug2.ModPlug_Seek

MODPLUG_ENABLE_OVERSAMPLING = _libmodplug2.MODPLUG_ENABLE_OVERSAMPLING
MODPLUG_ENABLE_NOISE_REDUCTION = _libmodplug2.MODPLUG_ENABLE_NOISE_REDUCTION
MODPLUG_ENABLE_REVERB = _libmodplug2.MODPLUG_ENABLE_REVERB
MODPLUG_ENABLE_MEGABASS = _libmodplug2.MODPLUG_ENABLE_MEGABASS
MODPLUG_ENABLE_SURROUND = _libmodplug2.MODPLUG_ENABLE_SURROUND
MODPLUG_RESAMPLE_NEAREST = _libmodplug2.MODPLUG_RESAMPLE_NEAREST
MODPLUG_RESAMPLE_LINEAR = _libmodplug2.MODPLUG_RESAMPLE_LINEAR
MODPLUG_RESAMPLE_SPLINE = _libmodplug2.MODPLUG_RESAMPLE_SPLINE
MODPLUG_RESAMPLE_FIR = _libmodplug2.MODPLUG_RESAMPLE_FIR
class ModPlug_Settings(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModPlug_Settings, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ModPlug_Settings, name)
    __swig_setmethods__["mFlags"] = _libmodplug2.ModPlug_Settings_mFlags_set
    __swig_getmethods__["mFlags"] = _libmodplug2.ModPlug_Settings_mFlags_get
    if _newclass:mFlags = property(_libmodplug2.ModPlug_Settings_mFlags_get,_libmodplug2.ModPlug_Settings_mFlags_set)
    __swig_setmethods__["mChannels"] = _libmodplug2.ModPlug_Settings_mChannels_set
    __swig_getmethods__["mChannels"] = _libmodplug2.ModPlug_Settings_mChannels_get
    if _newclass:mChannels = property(_libmodplug2.ModPlug_Settings_mChannels_get,_libmodplug2.ModPlug_Settings_mChannels_set)
    __swig_setmethods__["mBits"] = _libmodplug2.ModPlug_Settings_mBits_set
    __swig_getmethods__["mBits"] = _libmodplug2.ModPlug_Settings_mBits_get
    if _newclass:mBits = property(_libmodplug2.ModPlug_Settings_mBits_get,_libmodplug2.ModPlug_Settings_mBits_set)
    __swig_setmethods__["mFrequency"] = _libmodplug2.ModPlug_Settings_mFrequency_set
    __swig_getmethods__["mFrequency"] = _libmodplug2.ModPlug_Settings_mFrequency_get
    if _newclass:mFrequency = property(_libmodplug2.ModPlug_Settings_mFrequency_get,_libmodplug2.ModPlug_Settings_mFrequency_set)
    __swig_setmethods__["mResamplingMode"] = _libmodplug2.ModPlug_Settings_mResamplingMode_set
    __swig_getmethods__["mResamplingMode"] = _libmodplug2.ModPlug_Settings_mResamplingMode_get
    if _newclass:mResamplingMode = property(_libmodplug2.ModPlug_Settings_mResamplingMode_get,_libmodplug2.ModPlug_Settings_mResamplingMode_set)
    __swig_setmethods__["mReverbDepth"] = _libmodplug2.ModPlug_Settings_mReverbDepth_set
    __swig_getmethods__["mReverbDepth"] = _libmodplug2.ModPlug_Settings_mReverbDepth_get
    if _newclass:mReverbDepth = property(_libmodplug2.ModPlug_Settings_mReverbDepth_get,_libmodplug2.ModPlug_Settings_mReverbDepth_set)
    __swig_setmethods__["mReverbDelay"] = _libmodplug2.ModPlug_Settings_mReverbDelay_set
    __swig_getmethods__["mReverbDelay"] = _libmodplug2.ModPlug_Settings_mReverbDelay_get
    if _newclass:mReverbDelay = property(_libmodplug2.ModPlug_Settings_mReverbDelay_get,_libmodplug2.ModPlug_Settings_mReverbDelay_set)
    __swig_setmethods__["mBassAmount"] = _libmodplug2.ModPlug_Settings_mBassAmount_set
    __swig_getmethods__["mBassAmount"] = _libmodplug2.ModPlug_Settings_mBassAmount_get
    if _newclass:mBassAmount = property(_libmodplug2.ModPlug_Settings_mBassAmount_get,_libmodplug2.ModPlug_Settings_mBassAmount_set)
    __swig_setmethods__["mBassRange"] = _libmodplug2.ModPlug_Settings_mBassRange_set
    __swig_getmethods__["mBassRange"] = _libmodplug2.ModPlug_Settings_mBassRange_get
    if _newclass:mBassRange = property(_libmodplug2.ModPlug_Settings_mBassRange_get,_libmodplug2.ModPlug_Settings_mBassRange_set)
    __swig_setmethods__["mSurroundDepth"] = _libmodplug2.ModPlug_Settings_mSurroundDepth_set
    __swig_getmethods__["mSurroundDepth"] = _libmodplug2.ModPlug_Settings_mSurroundDepth_get
    if _newclass:mSurroundDepth = property(_libmodplug2.ModPlug_Settings_mSurroundDepth_get,_libmodplug2.ModPlug_Settings_mSurroundDepth_set)
    __swig_setmethods__["mSurroundDelay"] = _libmodplug2.ModPlug_Settings_mSurroundDelay_set
    __swig_getmethods__["mSurroundDelay"] = _libmodplug2.ModPlug_Settings_mSurroundDelay_get
    if _newclass:mSurroundDelay = property(_libmodplug2.ModPlug_Settings_mSurroundDelay_get,_libmodplug2.ModPlug_Settings_mSurroundDelay_set)
    __swig_setmethods__["mLoopCount"] = _libmodplug2.ModPlug_Settings_mLoopCount_set
    __swig_getmethods__["mLoopCount"] = _libmodplug2.ModPlug_Settings_mLoopCount_get
    if _newclass:mLoopCount = property(_libmodplug2.ModPlug_Settings_mLoopCount_get,_libmodplug2.ModPlug_Settings_mLoopCount_set)
    def __init__(self,*args):
        _swig_setattr(self, ModPlug_Settings, 'this', apply(_libmodplug2.new_ModPlug_Settings,args))
        _swig_setattr(self, ModPlug_Settings, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_ModPlug_Settings):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C ModPlug_Settings instance at %s>" % (self.this,)

class ModPlug_SettingsPtr(ModPlug_Settings):
    def __init__(self,this):
        _swig_setattr(self, ModPlug_Settings, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ModPlug_Settings, 'thisown', 0)
        _swig_setattr(self, ModPlug_Settings,self.__class__,ModPlug_Settings)
_libmodplug2.ModPlug_Settings_swigregister(ModPlug_SettingsPtr)

ModPlug_GetSettings = _libmodplug2.ModPlug_GetSettings

ModPlug_SetSettings = _libmodplug2.ModPlug_SetSettings

MOD_AMIGAC2 = _libmodplug2.MOD_AMIGAC2
MAX_SAMPLE_LENGTH = _libmodplug2.MAX_SAMPLE_LENGTH
MAX_SAMPLE_RATE = _libmodplug2.MAX_SAMPLE_RATE
MAX_ORDERS = _libmodplug2.MAX_ORDERS
MAX_PATTERNS = _libmodplug2.MAX_PATTERNS
MAX_SAMPLES = _libmodplug2.MAX_SAMPLES
MAX_INSTRUMENTS = _libmodplug2.MAX_INSTRUMENTS
MAX_CHANNELS = _libmodplug2.MAX_CHANNELS
MAX_BASECHANNELS = _libmodplug2.MAX_BASECHANNELS
MAX_ENVPOINTS = _libmodplug2.MAX_ENVPOINTS
MIN_PERIOD = _libmodplug2.MIN_PERIOD
MAX_PERIOD = _libmodplug2.MAX_PERIOD
MAX_PATTERNNAME = _libmodplug2.MAX_PATTERNNAME
MAX_CHANNELNAME = _libmodplug2.MAX_CHANNELNAME
MAX_INFONAME = _libmodplug2.MAX_INFONAME
MAX_EQ_BANDS = _libmodplug2.MAX_EQ_BANDS
MAX_MIXPLUGINS = _libmodplug2.MAX_MIXPLUGINS
MOD_TYPE_NONE = _libmodplug2.MOD_TYPE_NONE
MOD_TYPE_MOD = _libmodplug2.MOD_TYPE_MOD
MOD_TYPE_S3M = _libmodplug2.MOD_TYPE_S3M
MOD_TYPE_XM = _libmodplug2.MOD_TYPE_XM
MOD_TYPE_MED = _libmodplug2.MOD_TYPE_MED
MOD_TYPE_MTM = _libmodplug2.MOD_TYPE_MTM
MOD_TYPE_IT = _libmodplug2.MOD_TYPE_IT
MOD_TYPE_669 = _libmodplug2.MOD_TYPE_669
MOD_TYPE_ULT = _libmodplug2.MOD_TYPE_ULT
MOD_TYPE_STM = _libmodplug2.MOD_TYPE_STM
MOD_TYPE_FAR = _libmodplug2.MOD_TYPE_FAR
MOD_TYPE_WAV = _libmodplug2.MOD_TYPE_WAV
MOD_TYPE_AMF = _libmodplug2.MOD_TYPE_AMF
MOD_TYPE_AMS = _libmodplug2.MOD_TYPE_AMS
MOD_TYPE_DSM = _libmodplug2.MOD_TYPE_DSM
MOD_TYPE_MDL = _libmodplug2.MOD_TYPE_MDL
MOD_TYPE_OKT = _libmodplug2.MOD_TYPE_OKT
MOD_TYPE_MID = _libmodplug2.MOD_TYPE_MID
MOD_TYPE_DMF = _libmodplug2.MOD_TYPE_DMF
MOD_TYPE_PTM = _libmodplug2.MOD_TYPE_PTM
MOD_TYPE_DBM = _libmodplug2.MOD_TYPE_DBM
MOD_TYPE_MT2 = _libmodplug2.MOD_TYPE_MT2
MOD_TYPE_AMF0 = _libmodplug2.MOD_TYPE_AMF0
MOD_TYPE_PSM = _libmodplug2.MOD_TYPE_PSM
MOD_TYPE_J2B = _libmodplug2.MOD_TYPE_J2B
MOD_TYPE_UMX = _libmodplug2.MOD_TYPE_UMX
MAX_MODTYPE = _libmodplug2.MAX_MODTYPE
CHN_16BIT = _libmodplug2.CHN_16BIT
CHN_LOOP = _libmodplug2.CHN_LOOP
CHN_PINGPONGLOOP = _libmodplug2.CHN_PINGPONGLOOP
CHN_SUSTAINLOOP = _libmodplug2.CHN_SUSTAINLOOP
CHN_PINGPONGSUSTAIN = _libmodplug2.CHN_PINGPONGSUSTAIN
CHN_PANNING = _libmodplug2.CHN_PANNING
CHN_STEREO = _libmodplug2.CHN_STEREO
CHN_PINGPONGFLAG = _libmodplug2.CHN_PINGPONGFLAG
CHN_MUTE = _libmodplug2.CHN_MUTE
CHN_KEYOFF = _libmodplug2.CHN_KEYOFF
CHN_NOTEFADE = _libmodplug2.CHN_NOTEFADE
CHN_SURROUND = _libmodplug2.CHN_SURROUND
CHN_NOIDO = _libmodplug2.CHN_NOIDO
CHN_HQSRC = _libmodplug2.CHN_HQSRC
CHN_FILTER = _libmodplug2.CHN_FILTER
CHN_VOLUMERAMP = _libmodplug2.CHN_VOLUMERAMP
CHN_VIBRATO = _libmodplug2.CHN_VIBRATO
CHN_TREMOLO = _libmodplug2.CHN_TREMOLO
CHN_PANBRELLO = _libmodplug2.CHN_PANBRELLO
CHN_PORTAMENTO = _libmodplug2.CHN_PORTAMENTO
CHN_GLISSANDO = _libmodplug2.CHN_GLISSANDO
CHN_VOLENV = _libmodplug2.CHN_VOLENV
CHN_PANENV = _libmodplug2.CHN_PANENV
CHN_PITCHENV = _libmodplug2.CHN_PITCHENV
CHN_FASTVOLRAMP = _libmodplug2.CHN_FASTVOLRAMP
CHN_EXTRALOUD = _libmodplug2.CHN_EXTRALOUD
CHN_REVERB = _libmodplug2.CHN_REVERB
CHN_NOREVERB = _libmodplug2.CHN_NOREVERB
ENV_VOLUME = _libmodplug2.ENV_VOLUME
ENV_VOLSUSTAIN = _libmodplug2.ENV_VOLSUSTAIN
ENV_VOLLOOP = _libmodplug2.ENV_VOLLOOP
ENV_PANNING = _libmodplug2.ENV_PANNING
ENV_PANSUSTAIN = _libmodplug2.ENV_PANSUSTAIN
ENV_PANLOOP = _libmodplug2.ENV_PANLOOP
ENV_PITCH = _libmodplug2.ENV_PITCH
ENV_PITCHSUSTAIN = _libmodplug2.ENV_PITCHSUSTAIN
ENV_PITCHLOOP = _libmodplug2.ENV_PITCHLOOP
ENV_SETPANNING = _libmodplug2.ENV_SETPANNING
ENV_FILTER = _libmodplug2.ENV_FILTER
ENV_VOLCARRY = _libmodplug2.ENV_VOLCARRY
ENV_PANCARRY = _libmodplug2.ENV_PANCARRY
ENV_PITCHCARRY = _libmodplug2.ENV_PITCHCARRY
ENV_MUTE = _libmodplug2.ENV_MUTE
CMD_NONE = _libmodplug2.CMD_NONE
CMD_ARPEGGIO = _libmodplug2.CMD_ARPEGGIO
CMD_PORTAMENTOUP = _libmodplug2.CMD_PORTAMENTOUP
CMD_PORTAMENTODOWN = _libmodplug2.CMD_PORTAMENTODOWN
CMD_TONEPORTAMENTO = _libmodplug2.CMD_TONEPORTAMENTO
CMD_VIBRATO = _libmodplug2.CMD_VIBRATO
CMD_TONEPORTAVOL = _libmodplug2.CMD_TONEPORTAVOL
CMD_VIBRATOVOL = _libmodplug2.CMD_VIBRATOVOL
CMD_TREMOLO = _libmodplug2.CMD_TREMOLO
CMD_PANNING8 = _libmodplug2.CMD_PANNING8
CMD_OFFSET = _libmodplug2.CMD_OFFSET
CMD_VOLUMESLIDE = _libmodplug2.CMD_VOLUMESLIDE
CMD_POSITIONJUMP = _libmodplug2.CMD_POSITIONJUMP
CMD_VOLUME = _libmodplug2.CMD_VOLUME
CMD_PATTERNBREAK = _libmodplug2.CMD_PATTERNBREAK
CMD_RETRIG = _libmodplug2.CMD_RETRIG
CMD_SPEED = _libmodplug2.CMD_SPEED
CMD_TEMPO = _libmodplug2.CMD_TEMPO
CMD_TREMOR = _libmodplug2.CMD_TREMOR
CMD_MODCMDEX = _libmodplug2.CMD_MODCMDEX
CMD_S3MCMDEX = _libmodplug2.CMD_S3MCMDEX
CMD_CHANNELVOLUME = _libmodplug2.CMD_CHANNELVOLUME
CMD_CHANNELVOLSLIDE = _libmodplug2.CMD_CHANNELVOLSLIDE
CMD_GLOBALVOLUME = _libmodplug2.CMD_GLOBALVOLUME
CMD_GLOBALVOLSLIDE = _libmodplug2.CMD_GLOBALVOLSLIDE
CMD_KEYOFF = _libmodplug2.CMD_KEYOFF
CMD_FINEVIBRATO = _libmodplug2.CMD_FINEVIBRATO
CMD_PANBRELLO = _libmodplug2.CMD_PANBRELLO
CMD_XFINEPORTAUPDOWN = _libmodplug2.CMD_XFINEPORTAUPDOWN
CMD_PANNINGSLIDE = _libmodplug2.CMD_PANNINGSLIDE
CMD_SETENVPOSITION = _libmodplug2.CMD_SETENVPOSITION
CMD_MIDI = _libmodplug2.CMD_MIDI
FLTMODE_LOWPASS = _libmodplug2.FLTMODE_LOWPASS
FLTMODE_HIGHPASS = _libmodplug2.FLTMODE_HIGHPASS
FLTMODE_BANDPASS = _libmodplug2.FLTMODE_BANDPASS
VOLCMD_VOLUME = _libmodplug2.VOLCMD_VOLUME
VOLCMD_PANNING = _libmodplug2.VOLCMD_PANNING
VOLCMD_VOLSLIDEUP = _libmodplug2.VOLCMD_VOLSLIDEUP
VOLCMD_VOLSLIDEDOWN = _libmodplug2.VOLCMD_VOLSLIDEDOWN
VOLCMD_FINEVOLUP = _libmodplug2.VOLCMD_FINEVOLUP
VOLCMD_FINEVOLDOWN = _libmodplug2.VOLCMD_FINEVOLDOWN
VOLCMD_VIBRATOSPEED = _libmodplug2.VOLCMD_VIBRATOSPEED
VOLCMD_VIBRATO = _libmodplug2.VOLCMD_VIBRATO
VOLCMD_PANSLIDELEFT = _libmodplug2.VOLCMD_PANSLIDELEFT
VOLCMD_PANSLIDERIGHT = _libmodplug2.VOLCMD_PANSLIDERIGHT
VOLCMD_TONEPORTAMENTO = _libmodplug2.VOLCMD_TONEPORTAMENTO
VOLCMD_PORTAUP = _libmodplug2.VOLCMD_PORTAUP
VOLCMD_PORTADOWN = _libmodplug2.VOLCMD_PORTADOWN
RSF_16BIT = _libmodplug2.RSF_16BIT
RSF_STEREO = _libmodplug2.RSF_STEREO
RS_PCM8S = _libmodplug2.RS_PCM8S
RS_PCM8U = _libmodplug2.RS_PCM8U
RS_PCM8D = _libmodplug2.RS_PCM8D
RS_ADPCM4 = _libmodplug2.RS_ADPCM4
RS_PCM16D = _libmodplug2.RS_PCM16D
RS_PCM16S = _libmodplug2.RS_PCM16S
RS_PCM16U = _libmodplug2.RS_PCM16U
RS_PCM16M = _libmodplug2.RS_PCM16M
RS_STPCM8S = _libmodplug2.RS_STPCM8S
RS_STPCM8U = _libmodplug2.RS_STPCM8U
RS_STPCM8D = _libmodplug2.RS_STPCM8D
RS_STPCM16S = _libmodplug2.RS_STPCM16S
RS_STPCM16U = _libmodplug2.RS_STPCM16U
RS_STPCM16D = _libmodplug2.RS_STPCM16D
RS_STPCM16M = _libmodplug2.RS_STPCM16M
RS_IT2148 = _libmodplug2.RS_IT2148
RS_IT21416 = _libmodplug2.RS_IT21416
RS_IT2158 = _libmodplug2.RS_IT2158
RS_IT21516 = _libmodplug2.RS_IT21516
RS_AMS8 = _libmodplug2.RS_AMS8
RS_AMS16 = _libmodplug2.RS_AMS16
RS_DMF8 = _libmodplug2.RS_DMF8
RS_DMF16 = _libmodplug2.RS_DMF16
RS_MDL8 = _libmodplug2.RS_MDL8
RS_MDL16 = _libmodplug2.RS_MDL16
RS_PTM8DTO16 = _libmodplug2.RS_PTM8DTO16
RS_STIPCM8S = _libmodplug2.RS_STIPCM8S
RS_STIPCM8U = _libmodplug2.RS_STIPCM8U
RS_STIPCM16S = _libmodplug2.RS_STIPCM16S
RS_STIPCM16U = _libmodplug2.RS_STIPCM16U
RS_STIPCM16M = _libmodplug2.RS_STIPCM16M
RS_PCM24S = _libmodplug2.RS_PCM24S
RS_STIPCM24S = _libmodplug2.RS_STIPCM24S
RS_PCM32S = _libmodplug2.RS_PCM32S
RS_STIPCM32S = _libmodplug2.RS_STIPCM32S
NNA_NOTECUT = _libmodplug2.NNA_NOTECUT
NNA_CONTINUE = _libmodplug2.NNA_CONTINUE
NNA_NOTEOFF = _libmodplug2.NNA_NOTEOFF
NNA_NOTEFADE = _libmodplug2.NNA_NOTEFADE
DCT_NONE = _libmodplug2.DCT_NONE
DCT_NOTE = _libmodplug2.DCT_NOTE
DCT_SAMPLE = _libmodplug2.DCT_SAMPLE
DCT_INSTRUMENT = _libmodplug2.DCT_INSTRUMENT
DNA_NOTECUT = _libmodplug2.DNA_NOTECUT
DNA_NOTEOFF = _libmodplug2.DNA_NOTEOFF
DNA_NOTEFADE = _libmodplug2.DNA_NOTEFADE
SYSMIX_ENABLEMMX = _libmodplug2.SYSMIX_ENABLEMMX
SYSMIX_SLOWCPU = _libmodplug2.SYSMIX_SLOWCPU
SYSMIX_FASTCPU = _libmodplug2.SYSMIX_FASTCPU
SYSMIX_MMXEX = _libmodplug2.SYSMIX_MMXEX
SYSMIX_3DNOW = _libmodplug2.SYSMIX_3DNOW
SYSMIX_SSE = _libmodplug2.SYSMIX_SSE
SONG_EMBEDMIDICFG = _libmodplug2.SONG_EMBEDMIDICFG
SONG_FASTVOLSLIDES = _libmodplug2.SONG_FASTVOLSLIDES
SONG_ITOLDEFFECTS = _libmodplug2.SONG_ITOLDEFFECTS
SONG_ITCOMPATMODE = _libmodplug2.SONG_ITCOMPATMODE
SONG_LINEARSLIDES = _libmodplug2.SONG_LINEARSLIDES
SONG_PATTERNLOOP = _libmodplug2.SONG_PATTERNLOOP
SONG_STEP = _libmodplug2.SONG_STEP
SONG_PAUSED = _libmodplug2.SONG_PAUSED
SONG_FADINGSONG = _libmodplug2.SONG_FADINGSONG
SONG_ENDREACHED = _libmodplug2.SONG_ENDREACHED
SONG_GLOBALFADE = _libmodplug2.SONG_GLOBALFADE
SONG_CPUVERYHIGH = _libmodplug2.SONG_CPUVERYHIGH
SONG_FIRSTTICK = _libmodplug2.SONG_FIRSTTICK
SONG_MPTFILTERMODE = _libmodplug2.SONG_MPTFILTERMODE
SONG_SURROUNDPAN = _libmodplug2.SONG_SURROUNDPAN
SONG_EXFILTERRANGE = _libmodplug2.SONG_EXFILTERRANGE
SONG_AMIGALIMITS = _libmodplug2.SONG_AMIGALIMITS
SNDMIX_REVERSESTEREO = _libmodplug2.SNDMIX_REVERSESTEREO
SNDMIX_NOISEREDUCTION = _libmodplug2.SNDMIX_NOISEREDUCTION
SNDMIX_AGC = _libmodplug2.SNDMIX_AGC
SNDMIX_NORESAMPLING = _libmodplug2.SNDMIX_NORESAMPLING
SNDMIX_HQRESAMPLER = _libmodplug2.SNDMIX_HQRESAMPLER
SNDMIX_MEGABASS = _libmodplug2.SNDMIX_MEGABASS
SNDMIX_SURROUND = _libmodplug2.SNDMIX_SURROUND
SNDMIX_REVERB = _libmodplug2.SNDMIX_REVERB
SNDMIX_EQ = _libmodplug2.SNDMIX_EQ
SNDMIX_SOFTPANNING = _libmodplug2.SNDMIX_SOFTPANNING
SNDMIX_ULTRAHQSRCMODE = _libmodplug2.SNDMIX_ULTRAHQSRCMODE
SNDMIX_DIRECTTODISK = _libmodplug2.SNDMIX_DIRECTTODISK
SNDMIX_ENABLEMMX = _libmodplug2.SNDMIX_ENABLEMMX
SNDMIX_NOBACKWARDJUMPS = _libmodplug2.SNDMIX_NOBACKWARDJUMPS
SNDMIX_MAXDEFAULTPAN = _libmodplug2.SNDMIX_MAXDEFAULTPAN
SNDMIX_MUTECHNMODE = _libmodplug2.SNDMIX_MUTECHNMODE
SRCMODE_NEAREST = _libmodplug2.SRCMODE_NEAREST
SRCMODE_LINEAR = _libmodplug2.SRCMODE_LINEAR
SRCMODE_SPLINE = _libmodplug2.SRCMODE_SPLINE
SRCMODE_POLYPHASE = _libmodplug2.SRCMODE_POLYPHASE
NUM_SRC_MODES = _libmodplug2.NUM_SRC_MODES
class MODINSTRUMENT(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MODINSTRUMENT, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MODINSTRUMENT, name)
    __swig_setmethods__["nLength"] = _libmodplug2.MODINSTRUMENT_nLength_set
    __swig_getmethods__["nLength"] = _libmodplug2.MODINSTRUMENT_nLength_get
    if _newclass:nLength = property(_libmodplug2.MODINSTRUMENT_nLength_get,_libmodplug2.MODINSTRUMENT_nLength_set)
    __swig_setmethods__["nLoopStart"] = _libmodplug2.MODINSTRUMENT_nLoopStart_set
    __swig_getmethods__["nLoopStart"] = _libmodplug2.MODINSTRUMENT_nLoopStart_get
    if _newclass:nLoopStart = property(_libmodplug2.MODINSTRUMENT_nLoopStart_get,_libmodplug2.MODINSTRUMENT_nLoopStart_set)
    __swig_setmethods__["nLoopEnd"] = _libmodplug2.MODINSTRUMENT_nLoopEnd_set
    __swig_getmethods__["nLoopEnd"] = _libmodplug2.MODINSTRUMENT_nLoopEnd_get
    if _newclass:nLoopEnd = property(_libmodplug2.MODINSTRUMENT_nLoopEnd_get,_libmodplug2.MODINSTRUMENT_nLoopEnd_set)
    __swig_setmethods__["nSustainStart"] = _libmodplug2.MODINSTRUMENT_nSustainStart_set
    __swig_getmethods__["nSustainStart"] = _libmodplug2.MODINSTRUMENT_nSustainStart_get
    if _newclass:nSustainStart = property(_libmodplug2.MODINSTRUMENT_nSustainStart_get,_libmodplug2.MODINSTRUMENT_nSustainStart_set)
    __swig_setmethods__["nSustainEnd"] = _libmodplug2.MODINSTRUMENT_nSustainEnd_set
    __swig_getmethods__["nSustainEnd"] = _libmodplug2.MODINSTRUMENT_nSustainEnd_get
    if _newclass:nSustainEnd = property(_libmodplug2.MODINSTRUMENT_nSustainEnd_get,_libmodplug2.MODINSTRUMENT_nSustainEnd_set)
    __swig_setmethods__["pSample"] = _libmodplug2.MODINSTRUMENT_pSample_set
    __swig_getmethods__["pSample"] = _libmodplug2.MODINSTRUMENT_pSample_get
    if _newclass:pSample = property(_libmodplug2.MODINSTRUMENT_pSample_get,_libmodplug2.MODINSTRUMENT_pSample_set)
    __swig_setmethods__["nC4Speed"] = _libmodplug2.MODINSTRUMENT_nC4Speed_set
    __swig_getmethods__["nC4Speed"] = _libmodplug2.MODINSTRUMENT_nC4Speed_get
    if _newclass:nC4Speed = property(_libmodplug2.MODINSTRUMENT_nC4Speed_get,_libmodplug2.MODINSTRUMENT_nC4Speed_set)
    __swig_setmethods__["nPan"] = _libmodplug2.MODINSTRUMENT_nPan_set
    __swig_getmethods__["nPan"] = _libmodplug2.MODINSTRUMENT_nPan_get
    if _newclass:nPan = property(_libmodplug2.MODINSTRUMENT_nPan_get,_libmodplug2.MODINSTRUMENT_nPan_set)
    __swig_setmethods__["nVolume"] = _libmodplug2.MODINSTRUMENT_nVolume_set
    __swig_getmethods__["nVolume"] = _libmodplug2.MODINSTRUMENT_nVolume_get
    if _newclass:nVolume = property(_libmodplug2.MODINSTRUMENT_nVolume_get,_libmodplug2.MODINSTRUMENT_nVolume_set)
    __swig_setmethods__["nGlobalVol"] = _libmodplug2.MODINSTRUMENT_nGlobalVol_set
    __swig_getmethods__["nGlobalVol"] = _libmodplug2.MODINSTRUMENT_nGlobalVol_get
    if _newclass:nGlobalVol = property(_libmodplug2.MODINSTRUMENT_nGlobalVol_get,_libmodplug2.MODINSTRUMENT_nGlobalVol_set)
    __swig_setmethods__["uFlags"] = _libmodplug2.MODINSTRUMENT_uFlags_set
    __swig_getmethods__["uFlags"] = _libmodplug2.MODINSTRUMENT_uFlags_get
    if _newclass:uFlags = property(_libmodplug2.MODINSTRUMENT_uFlags_get,_libmodplug2.MODINSTRUMENT_uFlags_set)
    __swig_setmethods__["RelativeTone"] = _libmodplug2.MODINSTRUMENT_RelativeTone_set
    __swig_getmethods__["RelativeTone"] = _libmodplug2.MODINSTRUMENT_RelativeTone_get
    if _newclass:RelativeTone = property(_libmodplug2.MODINSTRUMENT_RelativeTone_get,_libmodplug2.MODINSTRUMENT_RelativeTone_set)
    __swig_setmethods__["nFineTune"] = _libmodplug2.MODINSTRUMENT_nFineTune_set
    __swig_getmethods__["nFineTune"] = _libmodplug2.MODINSTRUMENT_nFineTune_get
    if _newclass:nFineTune = property(_libmodplug2.MODINSTRUMENT_nFineTune_get,_libmodplug2.MODINSTRUMENT_nFineTune_set)
    __swig_setmethods__["nVibType"] = _libmodplug2.MODINSTRUMENT_nVibType_set
    __swig_getmethods__["nVibType"] = _libmodplug2.MODINSTRUMENT_nVibType_get
    if _newclass:nVibType = property(_libmodplug2.MODINSTRUMENT_nVibType_get,_libmodplug2.MODINSTRUMENT_nVibType_set)
    __swig_setmethods__["nVibSweep"] = _libmodplug2.MODINSTRUMENT_nVibSweep_set
    __swig_getmethods__["nVibSweep"] = _libmodplug2.MODINSTRUMENT_nVibSweep_get
    if _newclass:nVibSweep = property(_libmodplug2.MODINSTRUMENT_nVibSweep_get,_libmodplug2.MODINSTRUMENT_nVibSweep_set)
    __swig_setmethods__["nVibDepth"] = _libmodplug2.MODINSTRUMENT_nVibDepth_set
    __swig_getmethods__["nVibDepth"] = _libmodplug2.MODINSTRUMENT_nVibDepth_get
    if _newclass:nVibDepth = property(_libmodplug2.MODINSTRUMENT_nVibDepth_get,_libmodplug2.MODINSTRUMENT_nVibDepth_set)
    __swig_setmethods__["nVibRate"] = _libmodplug2.MODINSTRUMENT_nVibRate_set
    __swig_getmethods__["nVibRate"] = _libmodplug2.MODINSTRUMENT_nVibRate_get
    if _newclass:nVibRate = property(_libmodplug2.MODINSTRUMENT_nVibRate_get,_libmodplug2.MODINSTRUMENT_nVibRate_set)
    __swig_setmethods__["name"] = _libmodplug2.MODINSTRUMENT_name_set
    __swig_getmethods__["name"] = _libmodplug2.MODINSTRUMENT_name_get
    if _newclass:name = property(_libmodplug2.MODINSTRUMENT_name_get,_libmodplug2.MODINSTRUMENT_name_set)
    def __init__(self,*args):
        _swig_setattr(self, MODINSTRUMENT, 'this', apply(_libmodplug2.new_MODINSTRUMENT,args))
        _swig_setattr(self, MODINSTRUMENT, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_MODINSTRUMENT):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C MODINSTRUMENT instance at %s>" % (self.this,)

class MODINSTRUMENTPtr(MODINSTRUMENT):
    def __init__(self,this):
        _swig_setattr(self, MODINSTRUMENT, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MODINSTRUMENT, 'thisown', 0)
        _swig_setattr(self, MODINSTRUMENT,self.__class__,MODINSTRUMENT)
_libmodplug2.MODINSTRUMENT_swigregister(MODINSTRUMENTPtr)

class INSTRUMENTHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, INSTRUMENTHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, INSTRUMENTHEADER, name)
    __swig_setmethods__["nFadeOut"] = _libmodplug2.INSTRUMENTHEADER_nFadeOut_set
    __swig_getmethods__["nFadeOut"] = _libmodplug2.INSTRUMENTHEADER_nFadeOut_get
    if _newclass:nFadeOut = property(_libmodplug2.INSTRUMENTHEADER_nFadeOut_get,_libmodplug2.INSTRUMENTHEADER_nFadeOut_set)
    __swig_setmethods__["dwFlags"] = _libmodplug2.INSTRUMENTHEADER_dwFlags_set
    __swig_getmethods__["dwFlags"] = _libmodplug2.INSTRUMENTHEADER_dwFlags_get
    if _newclass:dwFlags = property(_libmodplug2.INSTRUMENTHEADER_dwFlags_get,_libmodplug2.INSTRUMENTHEADER_dwFlags_set)
    __swig_setmethods__["nGlobalVol"] = _libmodplug2.INSTRUMENTHEADER_nGlobalVol_set
    __swig_getmethods__["nGlobalVol"] = _libmodplug2.INSTRUMENTHEADER_nGlobalVol_get
    if _newclass:nGlobalVol = property(_libmodplug2.INSTRUMENTHEADER_nGlobalVol_get,_libmodplug2.INSTRUMENTHEADER_nGlobalVol_set)
    __swig_setmethods__["nPan"] = _libmodplug2.INSTRUMENTHEADER_nPan_set
    __swig_getmethods__["nPan"] = _libmodplug2.INSTRUMENTHEADER_nPan_get
    if _newclass:nPan = property(_libmodplug2.INSTRUMENTHEADER_nPan_get,_libmodplug2.INSTRUMENTHEADER_nPan_set)
    __swig_setmethods__["nVolEnv"] = _libmodplug2.INSTRUMENTHEADER_nVolEnv_set
    __swig_getmethods__["nVolEnv"] = _libmodplug2.INSTRUMENTHEADER_nVolEnv_get
    if _newclass:nVolEnv = property(_libmodplug2.INSTRUMENTHEADER_nVolEnv_get,_libmodplug2.INSTRUMENTHEADER_nVolEnv_set)
    __swig_setmethods__["nPanEnv"] = _libmodplug2.INSTRUMENTHEADER_nPanEnv_set
    __swig_getmethods__["nPanEnv"] = _libmodplug2.INSTRUMENTHEADER_nPanEnv_get
    if _newclass:nPanEnv = property(_libmodplug2.INSTRUMENTHEADER_nPanEnv_get,_libmodplug2.INSTRUMENTHEADER_nPanEnv_set)
    __swig_setmethods__["nPitchEnv"] = _libmodplug2.INSTRUMENTHEADER_nPitchEnv_set
    __swig_getmethods__["nPitchEnv"] = _libmodplug2.INSTRUMENTHEADER_nPitchEnv_get
    if _newclass:nPitchEnv = property(_libmodplug2.INSTRUMENTHEADER_nPitchEnv_get,_libmodplug2.INSTRUMENTHEADER_nPitchEnv_set)
    __swig_setmethods__["nVolLoopStart"] = _libmodplug2.INSTRUMENTHEADER_nVolLoopStart_set
    __swig_getmethods__["nVolLoopStart"] = _libmodplug2.INSTRUMENTHEADER_nVolLoopStart_get
    if _newclass:nVolLoopStart = property(_libmodplug2.INSTRUMENTHEADER_nVolLoopStart_get,_libmodplug2.INSTRUMENTHEADER_nVolLoopStart_set)
    __swig_setmethods__["nVolLoopEnd"] = _libmodplug2.INSTRUMENTHEADER_nVolLoopEnd_set
    __swig_getmethods__["nVolLoopEnd"] = _libmodplug2.INSTRUMENTHEADER_nVolLoopEnd_get
    if _newclass:nVolLoopEnd = property(_libmodplug2.INSTRUMENTHEADER_nVolLoopEnd_get,_libmodplug2.INSTRUMENTHEADER_nVolLoopEnd_set)
    __swig_setmethods__["nVolSustainBegin"] = _libmodplug2.INSTRUMENTHEADER_nVolSustainBegin_set
    __swig_getmethods__["nVolSustainBegin"] = _libmodplug2.INSTRUMENTHEADER_nVolSustainBegin_get
    if _newclass:nVolSustainBegin = property(_libmodplug2.INSTRUMENTHEADER_nVolSustainBegin_get,_libmodplug2.INSTRUMENTHEADER_nVolSustainBegin_set)
    __swig_setmethods__["nVolSustainEnd"] = _libmodplug2.INSTRUMENTHEADER_nVolSustainEnd_set
    __swig_getmethods__["nVolSustainEnd"] = _libmodplug2.INSTRUMENTHEADER_nVolSustainEnd_get
    if _newclass:nVolSustainEnd = property(_libmodplug2.INSTRUMENTHEADER_nVolSustainEnd_get,_libmodplug2.INSTRUMENTHEADER_nVolSustainEnd_set)
    __swig_setmethods__["nPanLoopStart"] = _libmodplug2.INSTRUMENTHEADER_nPanLoopStart_set
    __swig_getmethods__["nPanLoopStart"] = _libmodplug2.INSTRUMENTHEADER_nPanLoopStart_get
    if _newclass:nPanLoopStart = property(_libmodplug2.INSTRUMENTHEADER_nPanLoopStart_get,_libmodplug2.INSTRUMENTHEADER_nPanLoopStart_set)
    __swig_setmethods__["nPanLoopEnd"] = _libmodplug2.INSTRUMENTHEADER_nPanLoopEnd_set
    __swig_getmethods__["nPanLoopEnd"] = _libmodplug2.INSTRUMENTHEADER_nPanLoopEnd_get
    if _newclass:nPanLoopEnd = property(_libmodplug2.INSTRUMENTHEADER_nPanLoopEnd_get,_libmodplug2.INSTRUMENTHEADER_nPanLoopEnd_set)
    __swig_setmethods__["nPanSustainBegin"] = _libmodplug2.INSTRUMENTHEADER_nPanSustainBegin_set
    __swig_getmethods__["nPanSustainBegin"] = _libmodplug2.INSTRUMENTHEADER_nPanSustainBegin_get
    if _newclass:nPanSustainBegin = property(_libmodplug2.INSTRUMENTHEADER_nPanSustainBegin_get,_libmodplug2.INSTRUMENTHEADER_nPanSustainBegin_set)
    __swig_setmethods__["nPanSustainEnd"] = _libmodplug2.INSTRUMENTHEADER_nPanSustainEnd_set
    __swig_getmethods__["nPanSustainEnd"] = _libmodplug2.INSTRUMENTHEADER_nPanSustainEnd_get
    if _newclass:nPanSustainEnd = property(_libmodplug2.INSTRUMENTHEADER_nPanSustainEnd_get,_libmodplug2.INSTRUMENTHEADER_nPanSustainEnd_set)
    __swig_setmethods__["nPitchLoopStart"] = _libmodplug2.INSTRUMENTHEADER_nPitchLoopStart_set
    __swig_getmethods__["nPitchLoopStart"] = _libmodplug2.INSTRUMENTHEADER_nPitchLoopStart_get
    if _newclass:nPitchLoopStart = property(_libmodplug2.INSTRUMENTHEADER_nPitchLoopStart_get,_libmodplug2.INSTRUMENTHEADER_nPitchLoopStart_set)
    __swig_setmethods__["nPitchLoopEnd"] = _libmodplug2.INSTRUMENTHEADER_nPitchLoopEnd_set
    __swig_getmethods__["nPitchLoopEnd"] = _libmodplug2.INSTRUMENTHEADER_nPitchLoopEnd_get
    if _newclass:nPitchLoopEnd = property(_libmodplug2.INSTRUMENTHEADER_nPitchLoopEnd_get,_libmodplug2.INSTRUMENTHEADER_nPitchLoopEnd_set)
    __swig_setmethods__["nPitchSustainBegin"] = _libmodplug2.INSTRUMENTHEADER_nPitchSustainBegin_set
    __swig_getmethods__["nPitchSustainBegin"] = _libmodplug2.INSTRUMENTHEADER_nPitchSustainBegin_get
    if _newclass:nPitchSustainBegin = property(_libmodplug2.INSTRUMENTHEADER_nPitchSustainBegin_get,_libmodplug2.INSTRUMENTHEADER_nPitchSustainBegin_set)
    __swig_setmethods__["nPitchSustainEnd"] = _libmodplug2.INSTRUMENTHEADER_nPitchSustainEnd_set
    __swig_getmethods__["nPitchSustainEnd"] = _libmodplug2.INSTRUMENTHEADER_nPitchSustainEnd_get
    if _newclass:nPitchSustainEnd = property(_libmodplug2.INSTRUMENTHEADER_nPitchSustainEnd_get,_libmodplug2.INSTRUMENTHEADER_nPitchSustainEnd_set)
    __swig_setmethods__["nNNA"] = _libmodplug2.INSTRUMENTHEADER_nNNA_set
    __swig_getmethods__["nNNA"] = _libmodplug2.INSTRUMENTHEADER_nNNA_get
    if _newclass:nNNA = property(_libmodplug2.INSTRUMENTHEADER_nNNA_get,_libmodplug2.INSTRUMENTHEADER_nNNA_set)
    __swig_setmethods__["nDCT"] = _libmodplug2.INSTRUMENTHEADER_nDCT_set
    __swig_getmethods__["nDCT"] = _libmodplug2.INSTRUMENTHEADER_nDCT_get
    if _newclass:nDCT = property(_libmodplug2.INSTRUMENTHEADER_nDCT_get,_libmodplug2.INSTRUMENTHEADER_nDCT_set)
    __swig_setmethods__["nDNA"] = _libmodplug2.INSTRUMENTHEADER_nDNA_set
    __swig_getmethods__["nDNA"] = _libmodplug2.INSTRUMENTHEADER_nDNA_get
    if _newclass:nDNA = property(_libmodplug2.INSTRUMENTHEADER_nDNA_get,_libmodplug2.INSTRUMENTHEADER_nDNA_set)
    __swig_setmethods__["nPanSwing"] = _libmodplug2.INSTRUMENTHEADER_nPanSwing_set
    __swig_getmethods__["nPanSwing"] = _libmodplug2.INSTRUMENTHEADER_nPanSwing_get
    if _newclass:nPanSwing = property(_libmodplug2.INSTRUMENTHEADER_nPanSwing_get,_libmodplug2.INSTRUMENTHEADER_nPanSwing_set)
    __swig_setmethods__["nVolSwing"] = _libmodplug2.INSTRUMENTHEADER_nVolSwing_set
    __swig_getmethods__["nVolSwing"] = _libmodplug2.INSTRUMENTHEADER_nVolSwing_get
    if _newclass:nVolSwing = property(_libmodplug2.INSTRUMENTHEADER_nVolSwing_get,_libmodplug2.INSTRUMENTHEADER_nVolSwing_set)
    __swig_setmethods__["nIFC"] = _libmodplug2.INSTRUMENTHEADER_nIFC_set
    __swig_getmethods__["nIFC"] = _libmodplug2.INSTRUMENTHEADER_nIFC_get
    if _newclass:nIFC = property(_libmodplug2.INSTRUMENTHEADER_nIFC_get,_libmodplug2.INSTRUMENTHEADER_nIFC_set)
    __swig_setmethods__["nIFR"] = _libmodplug2.INSTRUMENTHEADER_nIFR_set
    __swig_getmethods__["nIFR"] = _libmodplug2.INSTRUMENTHEADER_nIFR_get
    if _newclass:nIFR = property(_libmodplug2.INSTRUMENTHEADER_nIFR_get,_libmodplug2.INSTRUMENTHEADER_nIFR_set)
    __swig_setmethods__["wMidiBank"] = _libmodplug2.INSTRUMENTHEADER_wMidiBank_set
    __swig_getmethods__["wMidiBank"] = _libmodplug2.INSTRUMENTHEADER_wMidiBank_get
    if _newclass:wMidiBank = property(_libmodplug2.INSTRUMENTHEADER_wMidiBank_get,_libmodplug2.INSTRUMENTHEADER_wMidiBank_set)
    __swig_setmethods__["nMidiProgram"] = _libmodplug2.INSTRUMENTHEADER_nMidiProgram_set
    __swig_getmethods__["nMidiProgram"] = _libmodplug2.INSTRUMENTHEADER_nMidiProgram_get
    if _newclass:nMidiProgram = property(_libmodplug2.INSTRUMENTHEADER_nMidiProgram_get,_libmodplug2.INSTRUMENTHEADER_nMidiProgram_set)
    __swig_setmethods__["nMidiChannel"] = _libmodplug2.INSTRUMENTHEADER_nMidiChannel_set
    __swig_getmethods__["nMidiChannel"] = _libmodplug2.INSTRUMENTHEADER_nMidiChannel_get
    if _newclass:nMidiChannel = property(_libmodplug2.INSTRUMENTHEADER_nMidiChannel_get,_libmodplug2.INSTRUMENTHEADER_nMidiChannel_set)
    __swig_setmethods__["nMidiDrumKey"] = _libmodplug2.INSTRUMENTHEADER_nMidiDrumKey_set
    __swig_getmethods__["nMidiDrumKey"] = _libmodplug2.INSTRUMENTHEADER_nMidiDrumKey_get
    if _newclass:nMidiDrumKey = property(_libmodplug2.INSTRUMENTHEADER_nMidiDrumKey_get,_libmodplug2.INSTRUMENTHEADER_nMidiDrumKey_set)
    __swig_setmethods__["nPPS"] = _libmodplug2.INSTRUMENTHEADER_nPPS_set
    __swig_getmethods__["nPPS"] = _libmodplug2.INSTRUMENTHEADER_nPPS_get
    if _newclass:nPPS = property(_libmodplug2.INSTRUMENTHEADER_nPPS_get,_libmodplug2.INSTRUMENTHEADER_nPPS_set)
    __swig_setmethods__["nPPC"] = _libmodplug2.INSTRUMENTHEADER_nPPC_set
    __swig_getmethods__["nPPC"] = _libmodplug2.INSTRUMENTHEADER_nPPC_get
    if _newclass:nPPC = property(_libmodplug2.INSTRUMENTHEADER_nPPC_get,_libmodplug2.INSTRUMENTHEADER_nPPC_set)
    __swig_setmethods__["VolPoints"] = _libmodplug2.INSTRUMENTHEADER_VolPoints_set
    __swig_getmethods__["VolPoints"] = _libmodplug2.INSTRUMENTHEADER_VolPoints_get
    if _newclass:VolPoints = property(_libmodplug2.INSTRUMENTHEADER_VolPoints_get,_libmodplug2.INSTRUMENTHEADER_VolPoints_set)
    __swig_setmethods__["PanPoints"] = _libmodplug2.INSTRUMENTHEADER_PanPoints_set
    __swig_getmethods__["PanPoints"] = _libmodplug2.INSTRUMENTHEADER_PanPoints_get
    if _newclass:PanPoints = property(_libmodplug2.INSTRUMENTHEADER_PanPoints_get,_libmodplug2.INSTRUMENTHEADER_PanPoints_set)
    __swig_setmethods__["PitchPoints"] = _libmodplug2.INSTRUMENTHEADER_PitchPoints_set
    __swig_getmethods__["PitchPoints"] = _libmodplug2.INSTRUMENTHEADER_PitchPoints_get
    if _newclass:PitchPoints = property(_libmodplug2.INSTRUMENTHEADER_PitchPoints_get,_libmodplug2.INSTRUMENTHEADER_PitchPoints_set)
    __swig_setmethods__["VolEnv"] = _libmodplug2.INSTRUMENTHEADER_VolEnv_set
    __swig_getmethods__["VolEnv"] = _libmodplug2.INSTRUMENTHEADER_VolEnv_get
    if _newclass:VolEnv = property(_libmodplug2.INSTRUMENTHEADER_VolEnv_get,_libmodplug2.INSTRUMENTHEADER_VolEnv_set)
    __swig_setmethods__["PanEnv"] = _libmodplug2.INSTRUMENTHEADER_PanEnv_set
    __swig_getmethods__["PanEnv"] = _libmodplug2.INSTRUMENTHEADER_PanEnv_get
    if _newclass:PanEnv = property(_libmodplug2.INSTRUMENTHEADER_PanEnv_get,_libmodplug2.INSTRUMENTHEADER_PanEnv_set)
    __swig_setmethods__["PitchEnv"] = _libmodplug2.INSTRUMENTHEADER_PitchEnv_set
    __swig_getmethods__["PitchEnv"] = _libmodplug2.INSTRUMENTHEADER_PitchEnv_get
    if _newclass:PitchEnv = property(_libmodplug2.INSTRUMENTHEADER_PitchEnv_get,_libmodplug2.INSTRUMENTHEADER_PitchEnv_set)
    __swig_setmethods__["NoteMap"] = _libmodplug2.INSTRUMENTHEADER_NoteMap_set
    __swig_getmethods__["NoteMap"] = _libmodplug2.INSTRUMENTHEADER_NoteMap_get
    if _newclass:NoteMap = property(_libmodplug2.INSTRUMENTHEADER_NoteMap_get,_libmodplug2.INSTRUMENTHEADER_NoteMap_set)
    __swig_setmethods__["Keyboard"] = _libmodplug2.INSTRUMENTHEADER_Keyboard_set
    __swig_getmethods__["Keyboard"] = _libmodplug2.INSTRUMENTHEADER_Keyboard_get
    if _newclass:Keyboard = property(_libmodplug2.INSTRUMENTHEADER_Keyboard_get,_libmodplug2.INSTRUMENTHEADER_Keyboard_set)
    __swig_setmethods__["name"] = _libmodplug2.INSTRUMENTHEADER_name_set
    __swig_getmethods__["name"] = _libmodplug2.INSTRUMENTHEADER_name_get
    if _newclass:name = property(_libmodplug2.INSTRUMENTHEADER_name_get,_libmodplug2.INSTRUMENTHEADER_name_set)
    __swig_setmethods__["filename"] = _libmodplug2.INSTRUMENTHEADER_filename_set
    __swig_getmethods__["filename"] = _libmodplug2.INSTRUMENTHEADER_filename_get
    if _newclass:filename = property(_libmodplug2.INSTRUMENTHEADER_filename_get,_libmodplug2.INSTRUMENTHEADER_filename_set)
    def __init__(self,*args):
        _swig_setattr(self, INSTRUMENTHEADER, 'this', apply(_libmodplug2.new_INSTRUMENTHEADER,args))
        _swig_setattr(self, INSTRUMENTHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_INSTRUMENTHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C INSTRUMENTHEADER instance at %s>" % (self.this,)

class INSTRUMENTHEADERPtr(INSTRUMENTHEADER):
    def __init__(self,this):
        _swig_setattr(self, INSTRUMENTHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, INSTRUMENTHEADER, 'thisown', 0)
        _swig_setattr(self, INSTRUMENTHEADER,self.__class__,INSTRUMENTHEADER)
_libmodplug2.INSTRUMENTHEADER_swigregister(INSTRUMENTHEADERPtr)

class MODCHANNEL(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MODCHANNEL, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MODCHANNEL, name)
    __swig_setmethods__["pCurrentSample"] = _libmodplug2.MODCHANNEL_pCurrentSample_set
    __swig_getmethods__["pCurrentSample"] = _libmodplug2.MODCHANNEL_pCurrentSample_get
    if _newclass:pCurrentSample = property(_libmodplug2.MODCHANNEL_pCurrentSample_get,_libmodplug2.MODCHANNEL_pCurrentSample_set)
    __swig_setmethods__["nPos"] = _libmodplug2.MODCHANNEL_nPos_set
    __swig_getmethods__["nPos"] = _libmodplug2.MODCHANNEL_nPos_get
    if _newclass:nPos = property(_libmodplug2.MODCHANNEL_nPos_get,_libmodplug2.MODCHANNEL_nPos_set)
    __swig_setmethods__["nPosLo"] = _libmodplug2.MODCHANNEL_nPosLo_set
    __swig_getmethods__["nPosLo"] = _libmodplug2.MODCHANNEL_nPosLo_get
    if _newclass:nPosLo = property(_libmodplug2.MODCHANNEL_nPosLo_get,_libmodplug2.MODCHANNEL_nPosLo_set)
    __swig_setmethods__["nInc"] = _libmodplug2.MODCHANNEL_nInc_set
    __swig_getmethods__["nInc"] = _libmodplug2.MODCHANNEL_nInc_get
    if _newclass:nInc = property(_libmodplug2.MODCHANNEL_nInc_get,_libmodplug2.MODCHANNEL_nInc_set)
    __swig_setmethods__["nRightVol"] = _libmodplug2.MODCHANNEL_nRightVol_set
    __swig_getmethods__["nRightVol"] = _libmodplug2.MODCHANNEL_nRightVol_get
    if _newclass:nRightVol = property(_libmodplug2.MODCHANNEL_nRightVol_get,_libmodplug2.MODCHANNEL_nRightVol_set)
    __swig_setmethods__["nLeftVol"] = _libmodplug2.MODCHANNEL_nLeftVol_set
    __swig_getmethods__["nLeftVol"] = _libmodplug2.MODCHANNEL_nLeftVol_get
    if _newclass:nLeftVol = property(_libmodplug2.MODCHANNEL_nLeftVol_get,_libmodplug2.MODCHANNEL_nLeftVol_set)
    __swig_setmethods__["nRightRamp"] = _libmodplug2.MODCHANNEL_nRightRamp_set
    __swig_getmethods__["nRightRamp"] = _libmodplug2.MODCHANNEL_nRightRamp_get
    if _newclass:nRightRamp = property(_libmodplug2.MODCHANNEL_nRightRamp_get,_libmodplug2.MODCHANNEL_nRightRamp_set)
    __swig_setmethods__["nLeftRamp"] = _libmodplug2.MODCHANNEL_nLeftRamp_set
    __swig_getmethods__["nLeftRamp"] = _libmodplug2.MODCHANNEL_nLeftRamp_get
    if _newclass:nLeftRamp = property(_libmodplug2.MODCHANNEL_nLeftRamp_get,_libmodplug2.MODCHANNEL_nLeftRamp_set)
    __swig_setmethods__["nLength"] = _libmodplug2.MODCHANNEL_nLength_set
    __swig_getmethods__["nLength"] = _libmodplug2.MODCHANNEL_nLength_get
    if _newclass:nLength = property(_libmodplug2.MODCHANNEL_nLength_get,_libmodplug2.MODCHANNEL_nLength_set)
    __swig_setmethods__["dwFlags"] = _libmodplug2.MODCHANNEL_dwFlags_set
    __swig_getmethods__["dwFlags"] = _libmodplug2.MODCHANNEL_dwFlags_get
    if _newclass:dwFlags = property(_libmodplug2.MODCHANNEL_dwFlags_get,_libmodplug2.MODCHANNEL_dwFlags_set)
    __swig_setmethods__["nLoopStart"] = _libmodplug2.MODCHANNEL_nLoopStart_set
    __swig_getmethods__["nLoopStart"] = _libmodplug2.MODCHANNEL_nLoopStart_get
    if _newclass:nLoopStart = property(_libmodplug2.MODCHANNEL_nLoopStart_get,_libmodplug2.MODCHANNEL_nLoopStart_set)
    __swig_setmethods__["nLoopEnd"] = _libmodplug2.MODCHANNEL_nLoopEnd_set
    __swig_getmethods__["nLoopEnd"] = _libmodplug2.MODCHANNEL_nLoopEnd_get
    if _newclass:nLoopEnd = property(_libmodplug2.MODCHANNEL_nLoopEnd_get,_libmodplug2.MODCHANNEL_nLoopEnd_set)
    __swig_setmethods__["nRampRightVol"] = _libmodplug2.MODCHANNEL_nRampRightVol_set
    __swig_getmethods__["nRampRightVol"] = _libmodplug2.MODCHANNEL_nRampRightVol_get
    if _newclass:nRampRightVol = property(_libmodplug2.MODCHANNEL_nRampRightVol_get,_libmodplug2.MODCHANNEL_nRampRightVol_set)
    __swig_setmethods__["nRampLeftVol"] = _libmodplug2.MODCHANNEL_nRampLeftVol_set
    __swig_getmethods__["nRampLeftVol"] = _libmodplug2.MODCHANNEL_nRampLeftVol_get
    if _newclass:nRampLeftVol = property(_libmodplug2.MODCHANNEL_nRampLeftVol_get,_libmodplug2.MODCHANNEL_nRampLeftVol_set)
    __swig_setmethods__["nFilter_Y1"] = _libmodplug2.MODCHANNEL_nFilter_Y1_set
    __swig_getmethods__["nFilter_Y1"] = _libmodplug2.MODCHANNEL_nFilter_Y1_get
    if _newclass:nFilter_Y1 = property(_libmodplug2.MODCHANNEL_nFilter_Y1_get,_libmodplug2.MODCHANNEL_nFilter_Y1_set)
    __swig_setmethods__["nFilter_Y2"] = _libmodplug2.MODCHANNEL_nFilter_Y2_set
    __swig_getmethods__["nFilter_Y2"] = _libmodplug2.MODCHANNEL_nFilter_Y2_get
    if _newclass:nFilter_Y2 = property(_libmodplug2.MODCHANNEL_nFilter_Y2_get,_libmodplug2.MODCHANNEL_nFilter_Y2_set)
    __swig_setmethods__["nFilter_Y3"] = _libmodplug2.MODCHANNEL_nFilter_Y3_set
    __swig_getmethods__["nFilter_Y3"] = _libmodplug2.MODCHANNEL_nFilter_Y3_get
    if _newclass:nFilter_Y3 = property(_libmodplug2.MODCHANNEL_nFilter_Y3_get,_libmodplug2.MODCHANNEL_nFilter_Y3_set)
    __swig_setmethods__["nFilter_Y4"] = _libmodplug2.MODCHANNEL_nFilter_Y4_set
    __swig_getmethods__["nFilter_Y4"] = _libmodplug2.MODCHANNEL_nFilter_Y4_get
    if _newclass:nFilter_Y4 = property(_libmodplug2.MODCHANNEL_nFilter_Y4_get,_libmodplug2.MODCHANNEL_nFilter_Y4_set)
    __swig_setmethods__["nFilter_A0"] = _libmodplug2.MODCHANNEL_nFilter_A0_set
    __swig_getmethods__["nFilter_A0"] = _libmodplug2.MODCHANNEL_nFilter_A0_get
    if _newclass:nFilter_A0 = property(_libmodplug2.MODCHANNEL_nFilter_A0_get,_libmodplug2.MODCHANNEL_nFilter_A0_set)
    __swig_setmethods__["nFilter_B0"] = _libmodplug2.MODCHANNEL_nFilter_B0_set
    __swig_getmethods__["nFilter_B0"] = _libmodplug2.MODCHANNEL_nFilter_B0_get
    if _newclass:nFilter_B0 = property(_libmodplug2.MODCHANNEL_nFilter_B0_get,_libmodplug2.MODCHANNEL_nFilter_B0_set)
    __swig_setmethods__["nFilter_B1"] = _libmodplug2.MODCHANNEL_nFilter_B1_set
    __swig_getmethods__["nFilter_B1"] = _libmodplug2.MODCHANNEL_nFilter_B1_get
    if _newclass:nFilter_B1 = property(_libmodplug2.MODCHANNEL_nFilter_B1_get,_libmodplug2.MODCHANNEL_nFilter_B1_set)
    __swig_setmethods__["nFilter_HP"] = _libmodplug2.MODCHANNEL_nFilter_HP_set
    __swig_getmethods__["nFilter_HP"] = _libmodplug2.MODCHANNEL_nFilter_HP_get
    if _newclass:nFilter_HP = property(_libmodplug2.MODCHANNEL_nFilter_HP_get,_libmodplug2.MODCHANNEL_nFilter_HP_set)
    __swig_setmethods__["nROfs"] = _libmodplug2.MODCHANNEL_nROfs_set
    __swig_getmethods__["nROfs"] = _libmodplug2.MODCHANNEL_nROfs_get
    if _newclass:nROfs = property(_libmodplug2.MODCHANNEL_nROfs_get,_libmodplug2.MODCHANNEL_nROfs_set)
    __swig_setmethods__["nLOfs"] = _libmodplug2.MODCHANNEL_nLOfs_set
    __swig_getmethods__["nLOfs"] = _libmodplug2.MODCHANNEL_nLOfs_get
    if _newclass:nLOfs = property(_libmodplug2.MODCHANNEL_nLOfs_get,_libmodplug2.MODCHANNEL_nLOfs_set)
    __swig_setmethods__["nRampLength"] = _libmodplug2.MODCHANNEL_nRampLength_set
    __swig_getmethods__["nRampLength"] = _libmodplug2.MODCHANNEL_nRampLength_get
    if _newclass:nRampLength = property(_libmodplug2.MODCHANNEL_nRampLength_get,_libmodplug2.MODCHANNEL_nRampLength_set)
    __swig_setmethods__["pSample"] = _libmodplug2.MODCHANNEL_pSample_set
    __swig_getmethods__["pSample"] = _libmodplug2.MODCHANNEL_pSample_get
    if _newclass:pSample = property(_libmodplug2.MODCHANNEL_pSample_get,_libmodplug2.MODCHANNEL_pSample_set)
    __swig_setmethods__["nNewRightVol"] = _libmodplug2.MODCHANNEL_nNewRightVol_set
    __swig_getmethods__["nNewRightVol"] = _libmodplug2.MODCHANNEL_nNewRightVol_get
    if _newclass:nNewRightVol = property(_libmodplug2.MODCHANNEL_nNewRightVol_get,_libmodplug2.MODCHANNEL_nNewRightVol_set)
    __swig_setmethods__["nNewLeftVol"] = _libmodplug2.MODCHANNEL_nNewLeftVol_set
    __swig_getmethods__["nNewLeftVol"] = _libmodplug2.MODCHANNEL_nNewLeftVol_get
    if _newclass:nNewLeftVol = property(_libmodplug2.MODCHANNEL_nNewLeftVol_get,_libmodplug2.MODCHANNEL_nNewLeftVol_set)
    __swig_setmethods__["nRealVolume"] = _libmodplug2.MODCHANNEL_nRealVolume_set
    __swig_getmethods__["nRealVolume"] = _libmodplug2.MODCHANNEL_nRealVolume_get
    if _newclass:nRealVolume = property(_libmodplug2.MODCHANNEL_nRealVolume_get,_libmodplug2.MODCHANNEL_nRealVolume_set)
    __swig_setmethods__["nRealPan"] = _libmodplug2.MODCHANNEL_nRealPan_set
    __swig_getmethods__["nRealPan"] = _libmodplug2.MODCHANNEL_nRealPan_get
    if _newclass:nRealPan = property(_libmodplug2.MODCHANNEL_nRealPan_get,_libmodplug2.MODCHANNEL_nRealPan_set)
    __swig_setmethods__["nVolume"] = _libmodplug2.MODCHANNEL_nVolume_set
    __swig_getmethods__["nVolume"] = _libmodplug2.MODCHANNEL_nVolume_get
    if _newclass:nVolume = property(_libmodplug2.MODCHANNEL_nVolume_get,_libmodplug2.MODCHANNEL_nVolume_set)
    __swig_setmethods__["nPan"] = _libmodplug2.MODCHANNEL_nPan_set
    __swig_getmethods__["nPan"] = _libmodplug2.MODCHANNEL_nPan_get
    if _newclass:nPan = property(_libmodplug2.MODCHANNEL_nPan_get,_libmodplug2.MODCHANNEL_nPan_set)
    __swig_setmethods__["nFadeOutVol"] = _libmodplug2.MODCHANNEL_nFadeOutVol_set
    __swig_getmethods__["nFadeOutVol"] = _libmodplug2.MODCHANNEL_nFadeOutVol_get
    if _newclass:nFadeOutVol = property(_libmodplug2.MODCHANNEL_nFadeOutVol_get,_libmodplug2.MODCHANNEL_nFadeOutVol_set)
    __swig_setmethods__["nPeriod"] = _libmodplug2.MODCHANNEL_nPeriod_set
    __swig_getmethods__["nPeriod"] = _libmodplug2.MODCHANNEL_nPeriod_get
    if _newclass:nPeriod = property(_libmodplug2.MODCHANNEL_nPeriod_get,_libmodplug2.MODCHANNEL_nPeriod_set)
    __swig_setmethods__["nC4Speed"] = _libmodplug2.MODCHANNEL_nC4Speed_set
    __swig_getmethods__["nC4Speed"] = _libmodplug2.MODCHANNEL_nC4Speed_get
    if _newclass:nC4Speed = property(_libmodplug2.MODCHANNEL_nC4Speed_get,_libmodplug2.MODCHANNEL_nC4Speed_set)
    __swig_setmethods__["nPortamentoDest"] = _libmodplug2.MODCHANNEL_nPortamentoDest_set
    __swig_getmethods__["nPortamentoDest"] = _libmodplug2.MODCHANNEL_nPortamentoDest_get
    if _newclass:nPortamentoDest = property(_libmodplug2.MODCHANNEL_nPortamentoDest_get,_libmodplug2.MODCHANNEL_nPortamentoDest_set)
    __swig_setmethods__["pHeader"] = _libmodplug2.MODCHANNEL_pHeader_set
    __swig_getmethods__["pHeader"] = _libmodplug2.MODCHANNEL_pHeader_get
    if _newclass:pHeader = property(_libmodplug2.MODCHANNEL_pHeader_get,_libmodplug2.MODCHANNEL_pHeader_set)
    __swig_setmethods__["pInstrument"] = _libmodplug2.MODCHANNEL_pInstrument_set
    __swig_getmethods__["pInstrument"] = _libmodplug2.MODCHANNEL_pInstrument_get
    if _newclass:pInstrument = property(_libmodplug2.MODCHANNEL_pInstrument_get,_libmodplug2.MODCHANNEL_pInstrument_set)
    __swig_setmethods__["nVolEnvPosition"] = _libmodplug2.MODCHANNEL_nVolEnvPosition_set
    __swig_getmethods__["nVolEnvPosition"] = _libmodplug2.MODCHANNEL_nVolEnvPosition_get
    if _newclass:nVolEnvPosition = property(_libmodplug2.MODCHANNEL_nVolEnvPosition_get,_libmodplug2.MODCHANNEL_nVolEnvPosition_set)
    __swig_setmethods__["nPanEnvPosition"] = _libmodplug2.MODCHANNEL_nPanEnvPosition_set
    __swig_getmethods__["nPanEnvPosition"] = _libmodplug2.MODCHANNEL_nPanEnvPosition_get
    if _newclass:nPanEnvPosition = property(_libmodplug2.MODCHANNEL_nPanEnvPosition_get,_libmodplug2.MODCHANNEL_nPanEnvPosition_set)
    __swig_setmethods__["nPitchEnvPosition"] = _libmodplug2.MODCHANNEL_nPitchEnvPosition_set
    __swig_getmethods__["nPitchEnvPosition"] = _libmodplug2.MODCHANNEL_nPitchEnvPosition_get
    if _newclass:nPitchEnvPosition = property(_libmodplug2.MODCHANNEL_nPitchEnvPosition_get,_libmodplug2.MODCHANNEL_nPitchEnvPosition_set)
    __swig_setmethods__["nMasterChn"] = _libmodplug2.MODCHANNEL_nMasterChn_set
    __swig_getmethods__["nMasterChn"] = _libmodplug2.MODCHANNEL_nMasterChn_get
    if _newclass:nMasterChn = property(_libmodplug2.MODCHANNEL_nMasterChn_get,_libmodplug2.MODCHANNEL_nMasterChn_set)
    __swig_setmethods__["nVUMeter"] = _libmodplug2.MODCHANNEL_nVUMeter_set
    __swig_getmethods__["nVUMeter"] = _libmodplug2.MODCHANNEL_nVUMeter_get
    if _newclass:nVUMeter = property(_libmodplug2.MODCHANNEL_nVUMeter_get,_libmodplug2.MODCHANNEL_nVUMeter_set)
    __swig_setmethods__["nGlobalVol"] = _libmodplug2.MODCHANNEL_nGlobalVol_set
    __swig_getmethods__["nGlobalVol"] = _libmodplug2.MODCHANNEL_nGlobalVol_get
    if _newclass:nGlobalVol = property(_libmodplug2.MODCHANNEL_nGlobalVol_get,_libmodplug2.MODCHANNEL_nGlobalVol_set)
    __swig_setmethods__["nInsVol"] = _libmodplug2.MODCHANNEL_nInsVol_set
    __swig_getmethods__["nInsVol"] = _libmodplug2.MODCHANNEL_nInsVol_get
    if _newclass:nInsVol = property(_libmodplug2.MODCHANNEL_nInsVol_get,_libmodplug2.MODCHANNEL_nInsVol_set)
    __swig_setmethods__["nFineTune"] = _libmodplug2.MODCHANNEL_nFineTune_set
    __swig_getmethods__["nFineTune"] = _libmodplug2.MODCHANNEL_nFineTune_get
    if _newclass:nFineTune = property(_libmodplug2.MODCHANNEL_nFineTune_get,_libmodplug2.MODCHANNEL_nFineTune_set)
    __swig_setmethods__["nTranspose"] = _libmodplug2.MODCHANNEL_nTranspose_set
    __swig_getmethods__["nTranspose"] = _libmodplug2.MODCHANNEL_nTranspose_get
    if _newclass:nTranspose = property(_libmodplug2.MODCHANNEL_nTranspose_get,_libmodplug2.MODCHANNEL_nTranspose_set)
    __swig_setmethods__["nPortamentoSlide"] = _libmodplug2.MODCHANNEL_nPortamentoSlide_set
    __swig_getmethods__["nPortamentoSlide"] = _libmodplug2.MODCHANNEL_nPortamentoSlide_get
    if _newclass:nPortamentoSlide = property(_libmodplug2.MODCHANNEL_nPortamentoSlide_get,_libmodplug2.MODCHANNEL_nPortamentoSlide_set)
    __swig_setmethods__["nAutoVibDepth"] = _libmodplug2.MODCHANNEL_nAutoVibDepth_set
    __swig_getmethods__["nAutoVibDepth"] = _libmodplug2.MODCHANNEL_nAutoVibDepth_get
    if _newclass:nAutoVibDepth = property(_libmodplug2.MODCHANNEL_nAutoVibDepth_get,_libmodplug2.MODCHANNEL_nAutoVibDepth_set)
    __swig_setmethods__["nAutoVibPos"] = _libmodplug2.MODCHANNEL_nAutoVibPos_set
    __swig_getmethods__["nAutoVibPos"] = _libmodplug2.MODCHANNEL_nAutoVibPos_get
    if _newclass:nAutoVibPos = property(_libmodplug2.MODCHANNEL_nAutoVibPos_get,_libmodplug2.MODCHANNEL_nAutoVibPos_set)
    __swig_setmethods__["nVibratoPos"] = _libmodplug2.MODCHANNEL_nVibratoPos_set
    __swig_getmethods__["nVibratoPos"] = _libmodplug2.MODCHANNEL_nVibratoPos_get
    if _newclass:nVibratoPos = property(_libmodplug2.MODCHANNEL_nVibratoPos_get,_libmodplug2.MODCHANNEL_nVibratoPos_set)
    __swig_setmethods__["nTremoloPos"] = _libmodplug2.MODCHANNEL_nTremoloPos_set
    __swig_getmethods__["nTremoloPos"] = _libmodplug2.MODCHANNEL_nTremoloPos_get
    if _newclass:nTremoloPos = property(_libmodplug2.MODCHANNEL_nTremoloPos_get,_libmodplug2.MODCHANNEL_nTremoloPos_set)
    __swig_setmethods__["nPanbrelloPos"] = _libmodplug2.MODCHANNEL_nPanbrelloPos_set
    __swig_getmethods__["nPanbrelloPos"] = _libmodplug2.MODCHANNEL_nPanbrelloPos_get
    if _newclass:nPanbrelloPos = property(_libmodplug2.MODCHANNEL_nPanbrelloPos_get,_libmodplug2.MODCHANNEL_nPanbrelloPos_set)
    __swig_setmethods__["nVolSwing"] = _libmodplug2.MODCHANNEL_nVolSwing_set
    __swig_getmethods__["nVolSwing"] = _libmodplug2.MODCHANNEL_nVolSwing_get
    if _newclass:nVolSwing = property(_libmodplug2.MODCHANNEL_nVolSwing_get,_libmodplug2.MODCHANNEL_nVolSwing_set)
    __swig_setmethods__["nPanSwing"] = _libmodplug2.MODCHANNEL_nPanSwing_set
    __swig_getmethods__["nPanSwing"] = _libmodplug2.MODCHANNEL_nPanSwing_get
    if _newclass:nPanSwing = property(_libmodplug2.MODCHANNEL_nPanSwing_get,_libmodplug2.MODCHANNEL_nPanSwing_set)
    __swig_setmethods__["nNote"] = _libmodplug2.MODCHANNEL_nNote_set
    __swig_getmethods__["nNote"] = _libmodplug2.MODCHANNEL_nNote_get
    if _newclass:nNote = property(_libmodplug2.MODCHANNEL_nNote_get,_libmodplug2.MODCHANNEL_nNote_set)
    __swig_setmethods__["nNNA"] = _libmodplug2.MODCHANNEL_nNNA_set
    __swig_getmethods__["nNNA"] = _libmodplug2.MODCHANNEL_nNNA_get
    if _newclass:nNNA = property(_libmodplug2.MODCHANNEL_nNNA_get,_libmodplug2.MODCHANNEL_nNNA_set)
    __swig_setmethods__["nNewNote"] = _libmodplug2.MODCHANNEL_nNewNote_set
    __swig_getmethods__["nNewNote"] = _libmodplug2.MODCHANNEL_nNewNote_get
    if _newclass:nNewNote = property(_libmodplug2.MODCHANNEL_nNewNote_get,_libmodplug2.MODCHANNEL_nNewNote_set)
    __swig_setmethods__["nNewIns"] = _libmodplug2.MODCHANNEL_nNewIns_set
    __swig_getmethods__["nNewIns"] = _libmodplug2.MODCHANNEL_nNewIns_get
    if _newclass:nNewIns = property(_libmodplug2.MODCHANNEL_nNewIns_get,_libmodplug2.MODCHANNEL_nNewIns_set)
    __swig_setmethods__["nCommand"] = _libmodplug2.MODCHANNEL_nCommand_set
    __swig_getmethods__["nCommand"] = _libmodplug2.MODCHANNEL_nCommand_get
    if _newclass:nCommand = property(_libmodplug2.MODCHANNEL_nCommand_get,_libmodplug2.MODCHANNEL_nCommand_set)
    __swig_setmethods__["nArpeggio"] = _libmodplug2.MODCHANNEL_nArpeggio_set
    __swig_getmethods__["nArpeggio"] = _libmodplug2.MODCHANNEL_nArpeggio_get
    if _newclass:nArpeggio = property(_libmodplug2.MODCHANNEL_nArpeggio_get,_libmodplug2.MODCHANNEL_nArpeggio_set)
    __swig_setmethods__["nOldVolumeSlide"] = _libmodplug2.MODCHANNEL_nOldVolumeSlide_set
    __swig_getmethods__["nOldVolumeSlide"] = _libmodplug2.MODCHANNEL_nOldVolumeSlide_get
    if _newclass:nOldVolumeSlide = property(_libmodplug2.MODCHANNEL_nOldVolumeSlide_get,_libmodplug2.MODCHANNEL_nOldVolumeSlide_set)
    __swig_setmethods__["nOldFineVolUpDown"] = _libmodplug2.MODCHANNEL_nOldFineVolUpDown_set
    __swig_getmethods__["nOldFineVolUpDown"] = _libmodplug2.MODCHANNEL_nOldFineVolUpDown_get
    if _newclass:nOldFineVolUpDown = property(_libmodplug2.MODCHANNEL_nOldFineVolUpDown_get,_libmodplug2.MODCHANNEL_nOldFineVolUpDown_set)
    __swig_setmethods__["nOldPortaUpDown"] = _libmodplug2.MODCHANNEL_nOldPortaUpDown_set
    __swig_getmethods__["nOldPortaUpDown"] = _libmodplug2.MODCHANNEL_nOldPortaUpDown_get
    if _newclass:nOldPortaUpDown = property(_libmodplug2.MODCHANNEL_nOldPortaUpDown_get,_libmodplug2.MODCHANNEL_nOldPortaUpDown_set)
    __swig_setmethods__["nOldFinePortaUpDown"] = _libmodplug2.MODCHANNEL_nOldFinePortaUpDown_set
    __swig_getmethods__["nOldFinePortaUpDown"] = _libmodplug2.MODCHANNEL_nOldFinePortaUpDown_get
    if _newclass:nOldFinePortaUpDown = property(_libmodplug2.MODCHANNEL_nOldFinePortaUpDown_get,_libmodplug2.MODCHANNEL_nOldFinePortaUpDown_set)
    __swig_setmethods__["nOldPanSlide"] = _libmodplug2.MODCHANNEL_nOldPanSlide_set
    __swig_getmethods__["nOldPanSlide"] = _libmodplug2.MODCHANNEL_nOldPanSlide_get
    if _newclass:nOldPanSlide = property(_libmodplug2.MODCHANNEL_nOldPanSlide_get,_libmodplug2.MODCHANNEL_nOldPanSlide_set)
    __swig_setmethods__["nOldChnVolSlide"] = _libmodplug2.MODCHANNEL_nOldChnVolSlide_set
    __swig_getmethods__["nOldChnVolSlide"] = _libmodplug2.MODCHANNEL_nOldChnVolSlide_get
    if _newclass:nOldChnVolSlide = property(_libmodplug2.MODCHANNEL_nOldChnVolSlide_get,_libmodplug2.MODCHANNEL_nOldChnVolSlide_set)
    __swig_setmethods__["nVibratoType"] = _libmodplug2.MODCHANNEL_nVibratoType_set
    __swig_getmethods__["nVibratoType"] = _libmodplug2.MODCHANNEL_nVibratoType_get
    if _newclass:nVibratoType = property(_libmodplug2.MODCHANNEL_nVibratoType_get,_libmodplug2.MODCHANNEL_nVibratoType_set)
    __swig_setmethods__["nVibratoSpeed"] = _libmodplug2.MODCHANNEL_nVibratoSpeed_set
    __swig_getmethods__["nVibratoSpeed"] = _libmodplug2.MODCHANNEL_nVibratoSpeed_get
    if _newclass:nVibratoSpeed = property(_libmodplug2.MODCHANNEL_nVibratoSpeed_get,_libmodplug2.MODCHANNEL_nVibratoSpeed_set)
    __swig_setmethods__["nVibratoDepth"] = _libmodplug2.MODCHANNEL_nVibratoDepth_set
    __swig_getmethods__["nVibratoDepth"] = _libmodplug2.MODCHANNEL_nVibratoDepth_get
    if _newclass:nVibratoDepth = property(_libmodplug2.MODCHANNEL_nVibratoDepth_get,_libmodplug2.MODCHANNEL_nVibratoDepth_set)
    __swig_setmethods__["nTremoloType"] = _libmodplug2.MODCHANNEL_nTremoloType_set
    __swig_getmethods__["nTremoloType"] = _libmodplug2.MODCHANNEL_nTremoloType_get
    if _newclass:nTremoloType = property(_libmodplug2.MODCHANNEL_nTremoloType_get,_libmodplug2.MODCHANNEL_nTremoloType_set)
    __swig_setmethods__["nTremoloSpeed"] = _libmodplug2.MODCHANNEL_nTremoloSpeed_set
    __swig_getmethods__["nTremoloSpeed"] = _libmodplug2.MODCHANNEL_nTremoloSpeed_get
    if _newclass:nTremoloSpeed = property(_libmodplug2.MODCHANNEL_nTremoloSpeed_get,_libmodplug2.MODCHANNEL_nTremoloSpeed_set)
    __swig_setmethods__["nTremoloDepth"] = _libmodplug2.MODCHANNEL_nTremoloDepth_set
    __swig_getmethods__["nTremoloDepth"] = _libmodplug2.MODCHANNEL_nTremoloDepth_get
    if _newclass:nTremoloDepth = property(_libmodplug2.MODCHANNEL_nTremoloDepth_get,_libmodplug2.MODCHANNEL_nTremoloDepth_set)
    __swig_setmethods__["nPanbrelloType"] = _libmodplug2.MODCHANNEL_nPanbrelloType_set
    __swig_getmethods__["nPanbrelloType"] = _libmodplug2.MODCHANNEL_nPanbrelloType_get
    if _newclass:nPanbrelloType = property(_libmodplug2.MODCHANNEL_nPanbrelloType_get,_libmodplug2.MODCHANNEL_nPanbrelloType_set)
    __swig_setmethods__["nPanbrelloSpeed"] = _libmodplug2.MODCHANNEL_nPanbrelloSpeed_set
    __swig_getmethods__["nPanbrelloSpeed"] = _libmodplug2.MODCHANNEL_nPanbrelloSpeed_get
    if _newclass:nPanbrelloSpeed = property(_libmodplug2.MODCHANNEL_nPanbrelloSpeed_get,_libmodplug2.MODCHANNEL_nPanbrelloSpeed_set)
    __swig_setmethods__["nPanbrelloDepth"] = _libmodplug2.MODCHANNEL_nPanbrelloDepth_set
    __swig_getmethods__["nPanbrelloDepth"] = _libmodplug2.MODCHANNEL_nPanbrelloDepth_get
    if _newclass:nPanbrelloDepth = property(_libmodplug2.MODCHANNEL_nPanbrelloDepth_get,_libmodplug2.MODCHANNEL_nPanbrelloDepth_set)
    __swig_setmethods__["nOldCmdEx"] = _libmodplug2.MODCHANNEL_nOldCmdEx_set
    __swig_getmethods__["nOldCmdEx"] = _libmodplug2.MODCHANNEL_nOldCmdEx_get
    if _newclass:nOldCmdEx = property(_libmodplug2.MODCHANNEL_nOldCmdEx_get,_libmodplug2.MODCHANNEL_nOldCmdEx_set)
    __swig_setmethods__["nOldVolParam"] = _libmodplug2.MODCHANNEL_nOldVolParam_set
    __swig_getmethods__["nOldVolParam"] = _libmodplug2.MODCHANNEL_nOldVolParam_get
    if _newclass:nOldVolParam = property(_libmodplug2.MODCHANNEL_nOldVolParam_get,_libmodplug2.MODCHANNEL_nOldVolParam_set)
    __swig_setmethods__["nOldTempo"] = _libmodplug2.MODCHANNEL_nOldTempo_set
    __swig_getmethods__["nOldTempo"] = _libmodplug2.MODCHANNEL_nOldTempo_get
    if _newclass:nOldTempo = property(_libmodplug2.MODCHANNEL_nOldTempo_get,_libmodplug2.MODCHANNEL_nOldTempo_set)
    __swig_setmethods__["nOldOffset"] = _libmodplug2.MODCHANNEL_nOldOffset_set
    __swig_getmethods__["nOldOffset"] = _libmodplug2.MODCHANNEL_nOldOffset_get
    if _newclass:nOldOffset = property(_libmodplug2.MODCHANNEL_nOldOffset_get,_libmodplug2.MODCHANNEL_nOldOffset_set)
    __swig_setmethods__["nOldHiOffset"] = _libmodplug2.MODCHANNEL_nOldHiOffset_set
    __swig_getmethods__["nOldHiOffset"] = _libmodplug2.MODCHANNEL_nOldHiOffset_get
    if _newclass:nOldHiOffset = property(_libmodplug2.MODCHANNEL_nOldHiOffset_get,_libmodplug2.MODCHANNEL_nOldHiOffset_set)
    __swig_setmethods__["nCutOff"] = _libmodplug2.MODCHANNEL_nCutOff_set
    __swig_getmethods__["nCutOff"] = _libmodplug2.MODCHANNEL_nCutOff_get
    if _newclass:nCutOff = property(_libmodplug2.MODCHANNEL_nCutOff_get,_libmodplug2.MODCHANNEL_nCutOff_set)
    __swig_setmethods__["nResonance"] = _libmodplug2.MODCHANNEL_nResonance_set
    __swig_getmethods__["nResonance"] = _libmodplug2.MODCHANNEL_nResonance_get
    if _newclass:nResonance = property(_libmodplug2.MODCHANNEL_nResonance_get,_libmodplug2.MODCHANNEL_nResonance_set)
    __swig_setmethods__["nRetrigCount"] = _libmodplug2.MODCHANNEL_nRetrigCount_set
    __swig_getmethods__["nRetrigCount"] = _libmodplug2.MODCHANNEL_nRetrigCount_get
    if _newclass:nRetrigCount = property(_libmodplug2.MODCHANNEL_nRetrigCount_get,_libmodplug2.MODCHANNEL_nRetrigCount_set)
    __swig_setmethods__["nRetrigParam"] = _libmodplug2.MODCHANNEL_nRetrigParam_set
    __swig_getmethods__["nRetrigParam"] = _libmodplug2.MODCHANNEL_nRetrigParam_get
    if _newclass:nRetrigParam = property(_libmodplug2.MODCHANNEL_nRetrigParam_get,_libmodplug2.MODCHANNEL_nRetrigParam_set)
    __swig_setmethods__["nTremorCount"] = _libmodplug2.MODCHANNEL_nTremorCount_set
    __swig_getmethods__["nTremorCount"] = _libmodplug2.MODCHANNEL_nTremorCount_get
    if _newclass:nTremorCount = property(_libmodplug2.MODCHANNEL_nTremorCount_get,_libmodplug2.MODCHANNEL_nTremorCount_set)
    __swig_setmethods__["nTremorParam"] = _libmodplug2.MODCHANNEL_nTremorParam_set
    __swig_getmethods__["nTremorParam"] = _libmodplug2.MODCHANNEL_nTremorParam_get
    if _newclass:nTremorParam = property(_libmodplug2.MODCHANNEL_nTremorParam_get,_libmodplug2.MODCHANNEL_nTremorParam_set)
    __swig_setmethods__["nPatternLoop"] = _libmodplug2.MODCHANNEL_nPatternLoop_set
    __swig_getmethods__["nPatternLoop"] = _libmodplug2.MODCHANNEL_nPatternLoop_get
    if _newclass:nPatternLoop = property(_libmodplug2.MODCHANNEL_nPatternLoop_get,_libmodplug2.MODCHANNEL_nPatternLoop_set)
    __swig_setmethods__["nPatternLoopCount"] = _libmodplug2.MODCHANNEL_nPatternLoopCount_set
    __swig_getmethods__["nPatternLoopCount"] = _libmodplug2.MODCHANNEL_nPatternLoopCount_get
    if _newclass:nPatternLoopCount = property(_libmodplug2.MODCHANNEL_nPatternLoopCount_get,_libmodplug2.MODCHANNEL_nPatternLoopCount_set)
    __swig_setmethods__["nRowNote"] = _libmodplug2.MODCHANNEL_nRowNote_set
    __swig_getmethods__["nRowNote"] = _libmodplug2.MODCHANNEL_nRowNote_get
    if _newclass:nRowNote = property(_libmodplug2.MODCHANNEL_nRowNote_get,_libmodplug2.MODCHANNEL_nRowNote_set)
    __swig_setmethods__["nRowInstr"] = _libmodplug2.MODCHANNEL_nRowInstr_set
    __swig_getmethods__["nRowInstr"] = _libmodplug2.MODCHANNEL_nRowInstr_get
    if _newclass:nRowInstr = property(_libmodplug2.MODCHANNEL_nRowInstr_get,_libmodplug2.MODCHANNEL_nRowInstr_set)
    __swig_setmethods__["nRowVolCmd"] = _libmodplug2.MODCHANNEL_nRowVolCmd_set
    __swig_getmethods__["nRowVolCmd"] = _libmodplug2.MODCHANNEL_nRowVolCmd_get
    if _newclass:nRowVolCmd = property(_libmodplug2.MODCHANNEL_nRowVolCmd_get,_libmodplug2.MODCHANNEL_nRowVolCmd_set)
    __swig_setmethods__["nRowVolume"] = _libmodplug2.MODCHANNEL_nRowVolume_set
    __swig_getmethods__["nRowVolume"] = _libmodplug2.MODCHANNEL_nRowVolume_get
    if _newclass:nRowVolume = property(_libmodplug2.MODCHANNEL_nRowVolume_get,_libmodplug2.MODCHANNEL_nRowVolume_set)
    __swig_setmethods__["nRowCommand"] = _libmodplug2.MODCHANNEL_nRowCommand_set
    __swig_getmethods__["nRowCommand"] = _libmodplug2.MODCHANNEL_nRowCommand_get
    if _newclass:nRowCommand = property(_libmodplug2.MODCHANNEL_nRowCommand_get,_libmodplug2.MODCHANNEL_nRowCommand_set)
    __swig_setmethods__["nRowParam"] = _libmodplug2.MODCHANNEL_nRowParam_set
    __swig_getmethods__["nRowParam"] = _libmodplug2.MODCHANNEL_nRowParam_get
    if _newclass:nRowParam = property(_libmodplug2.MODCHANNEL_nRowParam_get,_libmodplug2.MODCHANNEL_nRowParam_set)
    __swig_setmethods__["nLeftVU"] = _libmodplug2.MODCHANNEL_nLeftVU_set
    __swig_getmethods__["nLeftVU"] = _libmodplug2.MODCHANNEL_nLeftVU_get
    if _newclass:nLeftVU = property(_libmodplug2.MODCHANNEL_nLeftVU_get,_libmodplug2.MODCHANNEL_nLeftVU_set)
    __swig_setmethods__["nRightVU"] = _libmodplug2.MODCHANNEL_nRightVU_set
    __swig_getmethods__["nRightVU"] = _libmodplug2.MODCHANNEL_nRightVU_get
    if _newclass:nRightVU = property(_libmodplug2.MODCHANNEL_nRightVU_get,_libmodplug2.MODCHANNEL_nRightVU_set)
    __swig_setmethods__["nActiveMacro"] = _libmodplug2.MODCHANNEL_nActiveMacro_set
    __swig_getmethods__["nActiveMacro"] = _libmodplug2.MODCHANNEL_nActiveMacro_get
    if _newclass:nActiveMacro = property(_libmodplug2.MODCHANNEL_nActiveMacro_get,_libmodplug2.MODCHANNEL_nActiveMacro_set)
    __swig_setmethods__["nFilterMode"] = _libmodplug2.MODCHANNEL_nFilterMode_set
    __swig_getmethods__["nFilterMode"] = _libmodplug2.MODCHANNEL_nFilterMode_get
    if _newclass:nFilterMode = property(_libmodplug2.MODCHANNEL_nFilterMode_get,_libmodplug2.MODCHANNEL_nFilterMode_set)
    def __init__(self,*args):
        _swig_setattr(self, MODCHANNEL, 'this', apply(_libmodplug2.new_MODCHANNEL,args))
        _swig_setattr(self, MODCHANNEL, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_MODCHANNEL):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C MODCHANNEL instance at %s>" % (self.this,)

class MODCHANNELPtr(MODCHANNEL):
    def __init__(self,this):
        _swig_setattr(self, MODCHANNEL, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MODCHANNEL, 'thisown', 0)
        _swig_setattr(self, MODCHANNEL,self.__class__,MODCHANNEL)
_libmodplug2.MODCHANNEL_swigregister(MODCHANNELPtr)

class MODCHANNELSETTINGS(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MODCHANNELSETTINGS, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MODCHANNELSETTINGS, name)
    __swig_setmethods__["nPan"] = _libmodplug2.MODCHANNELSETTINGS_nPan_set
    __swig_getmethods__["nPan"] = _libmodplug2.MODCHANNELSETTINGS_nPan_get
    if _newclass:nPan = property(_libmodplug2.MODCHANNELSETTINGS_nPan_get,_libmodplug2.MODCHANNELSETTINGS_nPan_set)
    __swig_setmethods__["nVolume"] = _libmodplug2.MODCHANNELSETTINGS_nVolume_set
    __swig_getmethods__["nVolume"] = _libmodplug2.MODCHANNELSETTINGS_nVolume_get
    if _newclass:nVolume = property(_libmodplug2.MODCHANNELSETTINGS_nVolume_get,_libmodplug2.MODCHANNELSETTINGS_nVolume_set)
    __swig_setmethods__["dwFlags"] = _libmodplug2.MODCHANNELSETTINGS_dwFlags_set
    __swig_getmethods__["dwFlags"] = _libmodplug2.MODCHANNELSETTINGS_dwFlags_get
    if _newclass:dwFlags = property(_libmodplug2.MODCHANNELSETTINGS_dwFlags_get,_libmodplug2.MODCHANNELSETTINGS_dwFlags_set)
    __swig_setmethods__["nMixPlugin"] = _libmodplug2.MODCHANNELSETTINGS_nMixPlugin_set
    __swig_getmethods__["nMixPlugin"] = _libmodplug2.MODCHANNELSETTINGS_nMixPlugin_get
    if _newclass:nMixPlugin = property(_libmodplug2.MODCHANNELSETTINGS_nMixPlugin_get,_libmodplug2.MODCHANNELSETTINGS_nMixPlugin_set)
    __swig_setmethods__["szName"] = _libmodplug2.MODCHANNELSETTINGS_szName_set
    __swig_getmethods__["szName"] = _libmodplug2.MODCHANNELSETTINGS_szName_get
    if _newclass:szName = property(_libmodplug2.MODCHANNELSETTINGS_szName_get,_libmodplug2.MODCHANNELSETTINGS_szName_set)
    def __init__(self,*args):
        _swig_setattr(self, MODCHANNELSETTINGS, 'this', apply(_libmodplug2.new_MODCHANNELSETTINGS,args))
        _swig_setattr(self, MODCHANNELSETTINGS, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_MODCHANNELSETTINGS):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C MODCHANNELSETTINGS instance at %s>" % (self.this,)

class MODCHANNELSETTINGSPtr(MODCHANNELSETTINGS):
    def __init__(self,this):
        _swig_setattr(self, MODCHANNELSETTINGS, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MODCHANNELSETTINGS, 'thisown', 0)
        _swig_setattr(self, MODCHANNELSETTINGS,self.__class__,MODCHANNELSETTINGS)
_libmodplug2.MODCHANNELSETTINGS_swigregister(MODCHANNELSETTINGSPtr)

class MODCOMMAND(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MODCOMMAND, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MODCOMMAND, name)
    __swig_setmethods__["note"] = _libmodplug2.MODCOMMAND_note_set
    __swig_getmethods__["note"] = _libmodplug2.MODCOMMAND_note_get
    if _newclass:note = property(_libmodplug2.MODCOMMAND_note_get,_libmodplug2.MODCOMMAND_note_set)
    __swig_setmethods__["instr"] = _libmodplug2.MODCOMMAND_instr_set
    __swig_getmethods__["instr"] = _libmodplug2.MODCOMMAND_instr_get
    if _newclass:instr = property(_libmodplug2.MODCOMMAND_instr_get,_libmodplug2.MODCOMMAND_instr_set)
    __swig_setmethods__["volcmd"] = _libmodplug2.MODCOMMAND_volcmd_set
    __swig_getmethods__["volcmd"] = _libmodplug2.MODCOMMAND_volcmd_get
    if _newclass:volcmd = property(_libmodplug2.MODCOMMAND_volcmd_get,_libmodplug2.MODCOMMAND_volcmd_set)
    __swig_setmethods__["command"] = _libmodplug2.MODCOMMAND_command_set
    __swig_getmethods__["command"] = _libmodplug2.MODCOMMAND_command_get
    if _newclass:command = property(_libmodplug2.MODCOMMAND_command_get,_libmodplug2.MODCOMMAND_command_set)
    __swig_setmethods__["vol"] = _libmodplug2.MODCOMMAND_vol_set
    __swig_getmethods__["vol"] = _libmodplug2.MODCOMMAND_vol_get
    if _newclass:vol = property(_libmodplug2.MODCOMMAND_vol_get,_libmodplug2.MODCOMMAND_vol_set)
    __swig_setmethods__["param"] = _libmodplug2.MODCOMMAND_param_set
    __swig_getmethods__["param"] = _libmodplug2.MODCOMMAND_param_get
    if _newclass:param = property(_libmodplug2.MODCOMMAND_param_get,_libmodplug2.MODCOMMAND_param_set)
    def __init__(self,*args):
        _swig_setattr(self, MODCOMMAND, 'this', apply(_libmodplug2.new_MODCOMMAND,args))
        _swig_setattr(self, MODCOMMAND, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_MODCOMMAND):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C MODCOMMAND instance at %s>" % (self.this,)

class MODCOMMANDPtr(MODCOMMAND):
    def __init__(self,this):
        _swig_setattr(self, MODCOMMAND, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MODCOMMAND, 'thisown', 0)
        _swig_setattr(self, MODCOMMAND,self.__class__,MODCOMMAND)
_libmodplug2.MODCOMMAND_swigregister(MODCOMMANDPtr)

MIXPLUG_MIXREADY = _libmodplug2.MIXPLUG_MIXREADY
class IMixPlugin(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IMixPlugin, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IMixPlugin, name)
    def AddRef(*args): return apply(_libmodplug2.IMixPlugin_AddRef,args)
    def Release(*args): return apply(_libmodplug2.IMixPlugin_Release,args)
    def SaveAllParameters(*args): return apply(_libmodplug2.IMixPlugin_SaveAllParameters,args)
    def RestoreAllParameters(*args): return apply(_libmodplug2.IMixPlugin_RestoreAllParameters,args)
    def Process(*args): return apply(_libmodplug2.IMixPlugin_Process,args)
    def Init(*args): return apply(_libmodplug2.IMixPlugin_Init,args)
    def MidiSend(*args): return apply(_libmodplug2.IMixPlugin_MidiSend,args)
    def MidiCommand(*args): return apply(_libmodplug2.IMixPlugin_MidiCommand,args)
    def SetZxxParameter(*args): return apply(_libmodplug2.IMixPlugin_SetZxxParameter,args)
    def __del__(self, destroy= _libmodplug2.delete_IMixPlugin):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __init__(self): raise RuntimeError, "No constructor defined"
    def __repr__(self):
        return "<C IMixPlugin instance at %s>" % (self.this,)

class IMixPluginPtr(IMixPlugin):
    def __init__(self,this):
        _swig_setattr(self, IMixPlugin, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, IMixPlugin, 'thisown', 0)
        _swig_setattr(self, IMixPlugin,self.__class__,IMixPlugin)
_libmodplug2.IMixPlugin_swigregister(IMixPluginPtr)

MIXPLUG_INPUTF_MASTEREFFECT = _libmodplug2.MIXPLUG_INPUTF_MASTEREFFECT
MIXPLUG_INPUTF_BYPASS = _libmodplug2.MIXPLUG_INPUTF_BYPASS
MIXPLUG_INPUTF_WETMIX = _libmodplug2.MIXPLUG_INPUTF_WETMIX
class SNDMIXPLUGINSTATE(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SNDMIXPLUGINSTATE, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SNDMIXPLUGINSTATE, name)
    __swig_setmethods__["dwFlags"] = _libmodplug2.SNDMIXPLUGINSTATE_dwFlags_set
    __swig_getmethods__["dwFlags"] = _libmodplug2.SNDMIXPLUGINSTATE_dwFlags_get
    if _newclass:dwFlags = property(_libmodplug2.SNDMIXPLUGINSTATE_dwFlags_get,_libmodplug2.SNDMIXPLUGINSTATE_dwFlags_set)
    __swig_setmethods__["nVolDecayL"] = _libmodplug2.SNDMIXPLUGINSTATE_nVolDecayL_set
    __swig_getmethods__["nVolDecayL"] = _libmodplug2.SNDMIXPLUGINSTATE_nVolDecayL_get
    if _newclass:nVolDecayL = property(_libmodplug2.SNDMIXPLUGINSTATE_nVolDecayL_get,_libmodplug2.SNDMIXPLUGINSTATE_nVolDecayL_set)
    __swig_setmethods__["nVolDecayR"] = _libmodplug2.SNDMIXPLUGINSTATE_nVolDecayR_set
    __swig_getmethods__["nVolDecayR"] = _libmodplug2.SNDMIXPLUGINSTATE_nVolDecayR_get
    if _newclass:nVolDecayR = property(_libmodplug2.SNDMIXPLUGINSTATE_nVolDecayR_get,_libmodplug2.SNDMIXPLUGINSTATE_nVolDecayR_set)
    __swig_setmethods__["pMixBuffer"] = _libmodplug2.SNDMIXPLUGINSTATE_pMixBuffer_set
    __swig_getmethods__["pMixBuffer"] = _libmodplug2.SNDMIXPLUGINSTATE_pMixBuffer_get
    if _newclass:pMixBuffer = property(_libmodplug2.SNDMIXPLUGINSTATE_pMixBuffer_get,_libmodplug2.SNDMIXPLUGINSTATE_pMixBuffer_set)
    __swig_setmethods__["pOutBufferL"] = _libmodplug2.SNDMIXPLUGINSTATE_pOutBufferL_set
    __swig_getmethods__["pOutBufferL"] = _libmodplug2.SNDMIXPLUGINSTATE_pOutBufferL_get
    if _newclass:pOutBufferL = property(_libmodplug2.SNDMIXPLUGINSTATE_pOutBufferL_get,_libmodplug2.SNDMIXPLUGINSTATE_pOutBufferL_set)
    __swig_setmethods__["pOutBufferR"] = _libmodplug2.SNDMIXPLUGINSTATE_pOutBufferR_set
    __swig_getmethods__["pOutBufferR"] = _libmodplug2.SNDMIXPLUGINSTATE_pOutBufferR_get
    if _newclass:pOutBufferR = property(_libmodplug2.SNDMIXPLUGINSTATE_pOutBufferR_get,_libmodplug2.SNDMIXPLUGINSTATE_pOutBufferR_set)
    def __init__(self,*args):
        _swig_setattr(self, SNDMIXPLUGINSTATE, 'this', apply(_libmodplug2.new_SNDMIXPLUGINSTATE,args))
        _swig_setattr(self, SNDMIXPLUGINSTATE, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_SNDMIXPLUGINSTATE):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C SNDMIXPLUGINSTATE instance at %s>" % (self.this,)

class SNDMIXPLUGINSTATEPtr(SNDMIXPLUGINSTATE):
    def __init__(self,this):
        _swig_setattr(self, SNDMIXPLUGINSTATE, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SNDMIXPLUGINSTATE, 'thisown', 0)
        _swig_setattr(self, SNDMIXPLUGINSTATE,self.__class__,SNDMIXPLUGINSTATE)
_libmodplug2.SNDMIXPLUGINSTATE_swigregister(SNDMIXPLUGINSTATEPtr)

class SNDMIXPLUGININFO(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SNDMIXPLUGININFO, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SNDMIXPLUGININFO, name)
    __swig_setmethods__["dwPluginId1"] = _libmodplug2.SNDMIXPLUGININFO_dwPluginId1_set
    __swig_getmethods__["dwPluginId1"] = _libmodplug2.SNDMIXPLUGININFO_dwPluginId1_get
    if _newclass:dwPluginId1 = property(_libmodplug2.SNDMIXPLUGININFO_dwPluginId1_get,_libmodplug2.SNDMIXPLUGININFO_dwPluginId1_set)
    __swig_setmethods__["dwPluginId2"] = _libmodplug2.SNDMIXPLUGININFO_dwPluginId2_set
    __swig_getmethods__["dwPluginId2"] = _libmodplug2.SNDMIXPLUGININFO_dwPluginId2_get
    if _newclass:dwPluginId2 = property(_libmodplug2.SNDMIXPLUGININFO_dwPluginId2_get,_libmodplug2.SNDMIXPLUGININFO_dwPluginId2_set)
    __swig_setmethods__["dwInputRouting"] = _libmodplug2.SNDMIXPLUGININFO_dwInputRouting_set
    __swig_getmethods__["dwInputRouting"] = _libmodplug2.SNDMIXPLUGININFO_dwInputRouting_get
    if _newclass:dwInputRouting = property(_libmodplug2.SNDMIXPLUGININFO_dwInputRouting_get,_libmodplug2.SNDMIXPLUGININFO_dwInputRouting_set)
    __swig_setmethods__["dwOutputRouting"] = _libmodplug2.SNDMIXPLUGININFO_dwOutputRouting_set
    __swig_getmethods__["dwOutputRouting"] = _libmodplug2.SNDMIXPLUGININFO_dwOutputRouting_get
    if _newclass:dwOutputRouting = property(_libmodplug2.SNDMIXPLUGININFO_dwOutputRouting_get,_libmodplug2.SNDMIXPLUGININFO_dwOutputRouting_set)
    __swig_setmethods__["dwReserved"] = _libmodplug2.SNDMIXPLUGININFO_dwReserved_set
    __swig_getmethods__["dwReserved"] = _libmodplug2.SNDMIXPLUGININFO_dwReserved_get
    if _newclass:dwReserved = property(_libmodplug2.SNDMIXPLUGININFO_dwReserved_get,_libmodplug2.SNDMIXPLUGININFO_dwReserved_set)
    __swig_setmethods__["szName"] = _libmodplug2.SNDMIXPLUGININFO_szName_set
    __swig_getmethods__["szName"] = _libmodplug2.SNDMIXPLUGININFO_szName_get
    if _newclass:szName = property(_libmodplug2.SNDMIXPLUGININFO_szName_get,_libmodplug2.SNDMIXPLUGININFO_szName_set)
    __swig_setmethods__["szLibraryName"] = _libmodplug2.SNDMIXPLUGININFO_szLibraryName_set
    __swig_getmethods__["szLibraryName"] = _libmodplug2.SNDMIXPLUGININFO_szLibraryName_get
    if _newclass:szLibraryName = property(_libmodplug2.SNDMIXPLUGININFO_szLibraryName_get,_libmodplug2.SNDMIXPLUGININFO_szLibraryName_set)
    def __init__(self,*args):
        _swig_setattr(self, SNDMIXPLUGININFO, 'this', apply(_libmodplug2.new_SNDMIXPLUGININFO,args))
        _swig_setattr(self, SNDMIXPLUGININFO, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_SNDMIXPLUGININFO):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C SNDMIXPLUGININFO instance at %s>" % (self.this,)

class SNDMIXPLUGININFOPtr(SNDMIXPLUGININFO):
    def __init__(self,this):
        _swig_setattr(self, SNDMIXPLUGININFO, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SNDMIXPLUGININFO, 'thisown', 0)
        _swig_setattr(self, SNDMIXPLUGININFO,self.__class__,SNDMIXPLUGININFO)
_libmodplug2.SNDMIXPLUGININFO_swigregister(SNDMIXPLUGININFOPtr)

class SNDMIXPLUGIN(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SNDMIXPLUGIN, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SNDMIXPLUGIN, name)
    __swig_setmethods__["pMixPlugin"] = _libmodplug2.SNDMIXPLUGIN_pMixPlugin_set
    __swig_getmethods__["pMixPlugin"] = _libmodplug2.SNDMIXPLUGIN_pMixPlugin_get
    if _newclass:pMixPlugin = property(_libmodplug2.SNDMIXPLUGIN_pMixPlugin_get,_libmodplug2.SNDMIXPLUGIN_pMixPlugin_set)
    __swig_setmethods__["pMixState"] = _libmodplug2.SNDMIXPLUGIN_pMixState_set
    __swig_getmethods__["pMixState"] = _libmodplug2.SNDMIXPLUGIN_pMixState_get
    if _newclass:pMixState = property(_libmodplug2.SNDMIXPLUGIN_pMixState_get,_libmodplug2.SNDMIXPLUGIN_pMixState_set)
    __swig_setmethods__["nPluginDataSize"] = _libmodplug2.SNDMIXPLUGIN_nPluginDataSize_set
    __swig_getmethods__["nPluginDataSize"] = _libmodplug2.SNDMIXPLUGIN_nPluginDataSize_get
    if _newclass:nPluginDataSize = property(_libmodplug2.SNDMIXPLUGIN_nPluginDataSize_get,_libmodplug2.SNDMIXPLUGIN_nPluginDataSize_set)
    __swig_setmethods__["pPluginData"] = _libmodplug2.SNDMIXPLUGIN_pPluginData_set
    __swig_getmethods__["pPluginData"] = _libmodplug2.SNDMIXPLUGIN_pPluginData_get
    if _newclass:pPluginData = property(_libmodplug2.SNDMIXPLUGIN_pPluginData_get,_libmodplug2.SNDMIXPLUGIN_pPluginData_set)
    __swig_setmethods__["Info"] = _libmodplug2.SNDMIXPLUGIN_Info_set
    __swig_getmethods__["Info"] = _libmodplug2.SNDMIXPLUGIN_Info_get
    if _newclass:Info = property(_libmodplug2.SNDMIXPLUGIN_Info_get,_libmodplug2.SNDMIXPLUGIN_Info_set)
    def __init__(self,*args):
        _swig_setattr(self, SNDMIXPLUGIN, 'this', apply(_libmodplug2.new_SNDMIXPLUGIN,args))
        _swig_setattr(self, SNDMIXPLUGIN, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_SNDMIXPLUGIN):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C SNDMIXPLUGIN instance at %s>" % (self.this,)

class SNDMIXPLUGINPtr(SNDMIXPLUGIN):
    def __init__(self,this):
        _swig_setattr(self, SNDMIXPLUGIN, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SNDMIXPLUGIN, 'thisown', 0)
        _swig_setattr(self, SNDMIXPLUGIN,self.__class__,SNDMIXPLUGIN)
_libmodplug2.SNDMIXPLUGIN_swigregister(SNDMIXPLUGINPtr)

class SNDMIXSONGEQ(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SNDMIXSONGEQ, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SNDMIXSONGEQ, name)
    __swig_setmethods__["nEQBands"] = _libmodplug2.SNDMIXSONGEQ_nEQBands_set
    __swig_getmethods__["nEQBands"] = _libmodplug2.SNDMIXSONGEQ_nEQBands_get
    if _newclass:nEQBands = property(_libmodplug2.SNDMIXSONGEQ_nEQBands_get,_libmodplug2.SNDMIXSONGEQ_nEQBands_set)
    __swig_setmethods__["EQFreq_Gains"] = _libmodplug2.SNDMIXSONGEQ_EQFreq_Gains_set
    __swig_getmethods__["EQFreq_Gains"] = _libmodplug2.SNDMIXSONGEQ_EQFreq_Gains_get
    if _newclass:EQFreq_Gains = property(_libmodplug2.SNDMIXSONGEQ_EQFreq_Gains_get,_libmodplug2.SNDMIXSONGEQ_EQFreq_Gains_set)
    def __init__(self,*args):
        _swig_setattr(self, SNDMIXSONGEQ, 'this', apply(_libmodplug2.new_SNDMIXSONGEQ,args))
        _swig_setattr(self, SNDMIXSONGEQ, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_SNDMIXSONGEQ):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C SNDMIXSONGEQ instance at %s>" % (self.this,)

class SNDMIXSONGEQPtr(SNDMIXSONGEQ):
    def __init__(self,this):
        _swig_setattr(self, SNDMIXSONGEQ, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SNDMIXSONGEQ, 'thisown', 0)
        _swig_setattr(self, SNDMIXSONGEQ,self.__class__,SNDMIXSONGEQ)
_libmodplug2.SNDMIXSONGEQ_swigregister(SNDMIXSONGEQPtr)

class SNDMIX_REVERB_PROPERTIES(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SNDMIX_REVERB_PROPERTIES, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SNDMIX_REVERB_PROPERTIES, name)
    __swig_setmethods__["lRoom"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoom_set
    __swig_getmethods__["lRoom"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoom_get
    if _newclass:lRoom = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoom_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoom_set)
    __swig_setmethods__["lRoomHF"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoomHF_set
    __swig_getmethods__["lRoomHF"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoomHF_get
    if _newclass:lRoomHF = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoomHF_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_lRoomHF_set)
    __swig_setmethods__["flDecayTime"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayTime_set
    __swig_getmethods__["flDecayTime"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayTime_get
    if _newclass:flDecayTime = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayTime_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayTime_set)
    __swig_setmethods__["flDecayHFRatio"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayHFRatio_set
    __swig_getmethods__["flDecayHFRatio"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayHFRatio_get
    if _newclass:flDecayHFRatio = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayHFRatio_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDecayHFRatio_set)
    __swig_setmethods__["lReflections"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lReflections_set
    __swig_getmethods__["lReflections"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lReflections_get
    if _newclass:lReflections = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_lReflections_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_lReflections_set)
    __swig_setmethods__["flReflectionsDelay"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flReflectionsDelay_set
    __swig_getmethods__["flReflectionsDelay"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flReflectionsDelay_get
    if _newclass:flReflectionsDelay = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_flReflectionsDelay_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_flReflectionsDelay_set)
    __swig_setmethods__["lReverb"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lReverb_set
    __swig_getmethods__["lReverb"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_lReverb_get
    if _newclass:lReverb = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_lReverb_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_lReverb_set)
    __swig_setmethods__["flReverbDelay"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flReverbDelay_set
    __swig_getmethods__["flReverbDelay"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flReverbDelay_get
    if _newclass:flReverbDelay = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_flReverbDelay_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_flReverbDelay_set)
    __swig_setmethods__["flDiffusion"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDiffusion_set
    __swig_getmethods__["flDiffusion"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDiffusion_get
    if _newclass:flDiffusion = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDiffusion_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDiffusion_set)
    __swig_setmethods__["flDensity"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDensity_set
    __swig_getmethods__["flDensity"] = _libmodplug2.SNDMIX_REVERB_PROPERTIES_flDensity_get
    if _newclass:flDensity = property(_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDensity_get,_libmodplug2.SNDMIX_REVERB_PROPERTIES_flDensity_set)
    def __init__(self,*args):
        _swig_setattr(self, SNDMIX_REVERB_PROPERTIES, 'this', apply(_libmodplug2.new_SNDMIX_REVERB_PROPERTIES,args))
        _swig_setattr(self, SNDMIX_REVERB_PROPERTIES, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_SNDMIX_REVERB_PROPERTIES):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C SNDMIX_REVERB_PROPERTIES instance at %s>" % (self.this,)

class SNDMIX_REVERB_PROPERTIESPtr(SNDMIX_REVERB_PROPERTIES):
    def __init__(self,this):
        _swig_setattr(self, SNDMIX_REVERB_PROPERTIES, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SNDMIX_REVERB_PROPERTIES, 'thisown', 0)
        _swig_setattr(self, SNDMIX_REVERB_PROPERTIES,self.__class__,SNDMIX_REVERB_PROPERTIES)
_libmodplug2.SNDMIX_REVERB_PROPERTIES_swigregister(SNDMIX_REVERB_PROPERTIESPtr)

NUM_REVERBTYPES = _libmodplug2.NUM_REVERBTYPES
GetReverbPresetName = _libmodplug2.GetReverbPresetName

MIDIOUT_START = _libmodplug2.MIDIOUT_START
MIDIOUT_STOP = _libmodplug2.MIDIOUT_STOP
MIDIOUT_TICK = _libmodplug2.MIDIOUT_TICK
MIDIOUT_NOTEON = _libmodplug2.MIDIOUT_NOTEON
MIDIOUT_NOTEOFF = _libmodplug2.MIDIOUT_NOTEOFF
MIDIOUT_VOLUME = _libmodplug2.MIDIOUT_VOLUME
MIDIOUT_PAN = _libmodplug2.MIDIOUT_PAN
MIDIOUT_BANKSEL = _libmodplug2.MIDIOUT_BANKSEL
MIDIOUT_PROGRAM = _libmodplug2.MIDIOUT_PROGRAM
class MODMIDICFG(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MODMIDICFG, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MODMIDICFG, name)
    __swig_setmethods__["szMidiGlb"] = _libmodplug2.MODMIDICFG_szMidiGlb_set
    __swig_getmethods__["szMidiGlb"] = _libmodplug2.MODMIDICFG_szMidiGlb_get
    if _newclass:szMidiGlb = property(_libmodplug2.MODMIDICFG_szMidiGlb_get,_libmodplug2.MODMIDICFG_szMidiGlb_set)
    __swig_setmethods__["szMidiSFXExt"] = _libmodplug2.MODMIDICFG_szMidiSFXExt_set
    __swig_getmethods__["szMidiSFXExt"] = _libmodplug2.MODMIDICFG_szMidiSFXExt_get
    if _newclass:szMidiSFXExt = property(_libmodplug2.MODMIDICFG_szMidiSFXExt_get,_libmodplug2.MODMIDICFG_szMidiSFXExt_set)
    __swig_setmethods__["szMidiZXXExt"] = _libmodplug2.MODMIDICFG_szMidiZXXExt_set
    __swig_getmethods__["szMidiZXXExt"] = _libmodplug2.MODMIDICFG_szMidiZXXExt_get
    if _newclass:szMidiZXXExt = property(_libmodplug2.MODMIDICFG_szMidiZXXExt_get,_libmodplug2.MODMIDICFG_szMidiZXXExt_set)
    def __init__(self,*args):
        _swig_setattr(self, MODMIDICFG, 'this', apply(_libmodplug2.new_MODMIDICFG,args))
        _swig_setattr(self, MODMIDICFG, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_MODMIDICFG):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C MODMIDICFG instance at %s>" % (self.this,)

class MODMIDICFGPtr(MODMIDICFG):
    def __init__(self,this):
        _swig_setattr(self, MODMIDICFG, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MODMIDICFG, 'thisown', 0)
        _swig_setattr(self, MODMIDICFG,self.__class__,MODMIDICFG)
_libmodplug2.MODMIDICFG_swigregister(MODMIDICFGPtr)

class CSoundFile(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSoundFile, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSoundFile, name)
    __swig_setmethods__["m_nType"] = _libmodplug2.CSoundFile_m_nType_set
    __swig_getmethods__["m_nType"] = _libmodplug2.CSoundFile_m_nType_get
    if _newclass:m_nType = property(_libmodplug2.CSoundFile_m_nType_get,_libmodplug2.CSoundFile_m_nType_set)
    __swig_setmethods__["m_nChannels"] = _libmodplug2.CSoundFile_m_nChannels_set
    __swig_getmethods__["m_nChannels"] = _libmodplug2.CSoundFile_m_nChannels_get
    if _newclass:m_nChannels = property(_libmodplug2.CSoundFile_m_nChannels_get,_libmodplug2.CSoundFile_m_nChannels_set)
    __swig_setmethods__["m_nSamples"] = _libmodplug2.CSoundFile_m_nSamples_set
    __swig_getmethods__["m_nSamples"] = _libmodplug2.CSoundFile_m_nSamples_get
    if _newclass:m_nSamples = property(_libmodplug2.CSoundFile_m_nSamples_get,_libmodplug2.CSoundFile_m_nSamples_set)
    __swig_setmethods__["m_nInstruments"] = _libmodplug2.CSoundFile_m_nInstruments_set
    __swig_getmethods__["m_nInstruments"] = _libmodplug2.CSoundFile_m_nInstruments_get
    if _newclass:m_nInstruments = property(_libmodplug2.CSoundFile_m_nInstruments_get,_libmodplug2.CSoundFile_m_nInstruments_set)
    __swig_setmethods__["m_nDefaultSpeed"] = _libmodplug2.CSoundFile_m_nDefaultSpeed_set
    __swig_getmethods__["m_nDefaultSpeed"] = _libmodplug2.CSoundFile_m_nDefaultSpeed_get
    if _newclass:m_nDefaultSpeed = property(_libmodplug2.CSoundFile_m_nDefaultSpeed_get,_libmodplug2.CSoundFile_m_nDefaultSpeed_set)
    __swig_setmethods__["m_nDefaultTempo"] = _libmodplug2.CSoundFile_m_nDefaultTempo_set
    __swig_getmethods__["m_nDefaultTempo"] = _libmodplug2.CSoundFile_m_nDefaultTempo_get
    if _newclass:m_nDefaultTempo = property(_libmodplug2.CSoundFile_m_nDefaultTempo_get,_libmodplug2.CSoundFile_m_nDefaultTempo_set)
    __swig_setmethods__["m_nDefaultGlobalVolume"] = _libmodplug2.CSoundFile_m_nDefaultGlobalVolume_set
    __swig_getmethods__["m_nDefaultGlobalVolume"] = _libmodplug2.CSoundFile_m_nDefaultGlobalVolume_get
    if _newclass:m_nDefaultGlobalVolume = property(_libmodplug2.CSoundFile_m_nDefaultGlobalVolume_get,_libmodplug2.CSoundFile_m_nDefaultGlobalVolume_set)
    __swig_setmethods__["m_dwSongFlags"] = _libmodplug2.CSoundFile_m_dwSongFlags_set
    __swig_getmethods__["m_dwSongFlags"] = _libmodplug2.CSoundFile_m_dwSongFlags_get
    if _newclass:m_dwSongFlags = property(_libmodplug2.CSoundFile_m_dwSongFlags_get,_libmodplug2.CSoundFile_m_dwSongFlags_set)
    __swig_setmethods__["m_nMixChannels"] = _libmodplug2.CSoundFile_m_nMixChannels_set
    __swig_getmethods__["m_nMixChannels"] = _libmodplug2.CSoundFile_m_nMixChannels_get
    if _newclass:m_nMixChannels = property(_libmodplug2.CSoundFile_m_nMixChannels_get,_libmodplug2.CSoundFile_m_nMixChannels_set)
    __swig_setmethods__["m_nMixStat"] = _libmodplug2.CSoundFile_m_nMixStat_set
    __swig_getmethods__["m_nMixStat"] = _libmodplug2.CSoundFile_m_nMixStat_get
    if _newclass:m_nMixStat = property(_libmodplug2.CSoundFile_m_nMixStat_get,_libmodplug2.CSoundFile_m_nMixStat_set)
    __swig_setmethods__["m_nBufferCount"] = _libmodplug2.CSoundFile_m_nBufferCount_set
    __swig_getmethods__["m_nBufferCount"] = _libmodplug2.CSoundFile_m_nBufferCount_get
    if _newclass:m_nBufferCount = property(_libmodplug2.CSoundFile_m_nBufferCount_get,_libmodplug2.CSoundFile_m_nBufferCount_set)
    __swig_setmethods__["m_nTickCount"] = _libmodplug2.CSoundFile_m_nTickCount_set
    __swig_getmethods__["m_nTickCount"] = _libmodplug2.CSoundFile_m_nTickCount_get
    if _newclass:m_nTickCount = property(_libmodplug2.CSoundFile_m_nTickCount_get,_libmodplug2.CSoundFile_m_nTickCount_set)
    __swig_setmethods__["m_nTotalCount"] = _libmodplug2.CSoundFile_m_nTotalCount_set
    __swig_getmethods__["m_nTotalCount"] = _libmodplug2.CSoundFile_m_nTotalCount_get
    if _newclass:m_nTotalCount = property(_libmodplug2.CSoundFile_m_nTotalCount_get,_libmodplug2.CSoundFile_m_nTotalCount_set)
    __swig_setmethods__["m_nPatternDelay"] = _libmodplug2.CSoundFile_m_nPatternDelay_set
    __swig_getmethods__["m_nPatternDelay"] = _libmodplug2.CSoundFile_m_nPatternDelay_get
    if _newclass:m_nPatternDelay = property(_libmodplug2.CSoundFile_m_nPatternDelay_get,_libmodplug2.CSoundFile_m_nPatternDelay_set)
    __swig_setmethods__["m_nFrameDelay"] = _libmodplug2.CSoundFile_m_nFrameDelay_set
    __swig_getmethods__["m_nFrameDelay"] = _libmodplug2.CSoundFile_m_nFrameDelay_get
    if _newclass:m_nFrameDelay = property(_libmodplug2.CSoundFile_m_nFrameDelay_get,_libmodplug2.CSoundFile_m_nFrameDelay_set)
    __swig_setmethods__["m_nMusicSpeed"] = _libmodplug2.CSoundFile_m_nMusicSpeed_set
    __swig_getmethods__["m_nMusicSpeed"] = _libmodplug2.CSoundFile_m_nMusicSpeed_get
    if _newclass:m_nMusicSpeed = property(_libmodplug2.CSoundFile_m_nMusicSpeed_get,_libmodplug2.CSoundFile_m_nMusicSpeed_set)
    __swig_setmethods__["m_nMusicTempo"] = _libmodplug2.CSoundFile_m_nMusicTempo_set
    __swig_getmethods__["m_nMusicTempo"] = _libmodplug2.CSoundFile_m_nMusicTempo_get
    if _newclass:m_nMusicTempo = property(_libmodplug2.CSoundFile_m_nMusicTempo_get,_libmodplug2.CSoundFile_m_nMusicTempo_set)
    __swig_setmethods__["m_nNextRow"] = _libmodplug2.CSoundFile_m_nNextRow_set
    __swig_getmethods__["m_nNextRow"] = _libmodplug2.CSoundFile_m_nNextRow_get
    if _newclass:m_nNextRow = property(_libmodplug2.CSoundFile_m_nNextRow_get,_libmodplug2.CSoundFile_m_nNextRow_set)
    __swig_setmethods__["m_nRow"] = _libmodplug2.CSoundFile_m_nRow_set
    __swig_getmethods__["m_nRow"] = _libmodplug2.CSoundFile_m_nRow_get
    if _newclass:m_nRow = property(_libmodplug2.CSoundFile_m_nRow_get,_libmodplug2.CSoundFile_m_nRow_set)
    __swig_setmethods__["m_nPattern"] = _libmodplug2.CSoundFile_m_nPattern_set
    __swig_getmethods__["m_nPattern"] = _libmodplug2.CSoundFile_m_nPattern_get
    if _newclass:m_nPattern = property(_libmodplug2.CSoundFile_m_nPattern_get,_libmodplug2.CSoundFile_m_nPattern_set)
    __swig_setmethods__["m_nCurrentPattern"] = _libmodplug2.CSoundFile_m_nCurrentPattern_set
    __swig_getmethods__["m_nCurrentPattern"] = _libmodplug2.CSoundFile_m_nCurrentPattern_get
    if _newclass:m_nCurrentPattern = property(_libmodplug2.CSoundFile_m_nCurrentPattern_get,_libmodplug2.CSoundFile_m_nCurrentPattern_set)
    __swig_setmethods__["m_nNextPattern"] = _libmodplug2.CSoundFile_m_nNextPattern_set
    __swig_getmethods__["m_nNextPattern"] = _libmodplug2.CSoundFile_m_nNextPattern_get
    if _newclass:m_nNextPattern = property(_libmodplug2.CSoundFile_m_nNextPattern_get,_libmodplug2.CSoundFile_m_nNextPattern_set)
    __swig_setmethods__["m_nRestartPos"] = _libmodplug2.CSoundFile_m_nRestartPos_set
    __swig_getmethods__["m_nRestartPos"] = _libmodplug2.CSoundFile_m_nRestartPos_get
    if _newclass:m_nRestartPos = property(_libmodplug2.CSoundFile_m_nRestartPos_get,_libmodplug2.CSoundFile_m_nRestartPos_set)
    __swig_setmethods__["m_nSeqOverride"] = _libmodplug2.CSoundFile_m_nSeqOverride_set
    __swig_getmethods__["m_nSeqOverride"] = _libmodplug2.CSoundFile_m_nSeqOverride_get
    if _newclass:m_nSeqOverride = property(_libmodplug2.CSoundFile_m_nSeqOverride_get,_libmodplug2.CSoundFile_m_nSeqOverride_set)
    __swig_setmethods__["m_nMasterVolume"] = _libmodplug2.CSoundFile_m_nMasterVolume_set
    __swig_getmethods__["m_nMasterVolume"] = _libmodplug2.CSoundFile_m_nMasterVolume_get
    if _newclass:m_nMasterVolume = property(_libmodplug2.CSoundFile_m_nMasterVolume_get,_libmodplug2.CSoundFile_m_nMasterVolume_set)
    __swig_setmethods__["m_nGlobalVolume"] = _libmodplug2.CSoundFile_m_nGlobalVolume_set
    __swig_getmethods__["m_nGlobalVolume"] = _libmodplug2.CSoundFile_m_nGlobalVolume_get
    if _newclass:m_nGlobalVolume = property(_libmodplug2.CSoundFile_m_nGlobalVolume_get,_libmodplug2.CSoundFile_m_nGlobalVolume_set)
    __swig_setmethods__["m_nSongPreAmp"] = _libmodplug2.CSoundFile_m_nSongPreAmp_set
    __swig_getmethods__["m_nSongPreAmp"] = _libmodplug2.CSoundFile_m_nSongPreAmp_get
    if _newclass:m_nSongPreAmp = property(_libmodplug2.CSoundFile_m_nSongPreAmp_get,_libmodplug2.CSoundFile_m_nSongPreAmp_set)
    __swig_setmethods__["m_nFreqFactor"] = _libmodplug2.CSoundFile_m_nFreqFactor_set
    __swig_getmethods__["m_nFreqFactor"] = _libmodplug2.CSoundFile_m_nFreqFactor_get
    if _newclass:m_nFreqFactor = property(_libmodplug2.CSoundFile_m_nFreqFactor_get,_libmodplug2.CSoundFile_m_nFreqFactor_set)
    __swig_setmethods__["m_nTempoFactor"] = _libmodplug2.CSoundFile_m_nTempoFactor_set
    __swig_getmethods__["m_nTempoFactor"] = _libmodplug2.CSoundFile_m_nTempoFactor_get
    if _newclass:m_nTempoFactor = property(_libmodplug2.CSoundFile_m_nTempoFactor_get,_libmodplug2.CSoundFile_m_nTempoFactor_set)
    __swig_setmethods__["m_nOldGlbVolSlide"] = _libmodplug2.CSoundFile_m_nOldGlbVolSlide_set
    __swig_getmethods__["m_nOldGlbVolSlide"] = _libmodplug2.CSoundFile_m_nOldGlbVolSlide_get
    if _newclass:m_nOldGlbVolSlide = property(_libmodplug2.CSoundFile_m_nOldGlbVolSlide_get,_libmodplug2.CSoundFile_m_nOldGlbVolSlide_set)
    __swig_setmethods__["m_nMinPeriod"] = _libmodplug2.CSoundFile_m_nMinPeriod_set
    __swig_getmethods__["m_nMinPeriod"] = _libmodplug2.CSoundFile_m_nMinPeriod_get
    if _newclass:m_nMinPeriod = property(_libmodplug2.CSoundFile_m_nMinPeriod_get,_libmodplug2.CSoundFile_m_nMinPeriod_set)
    __swig_setmethods__["m_nMaxPeriod"] = _libmodplug2.CSoundFile_m_nMaxPeriod_set
    __swig_getmethods__["m_nMaxPeriod"] = _libmodplug2.CSoundFile_m_nMaxPeriod_get
    if _newclass:m_nMaxPeriod = property(_libmodplug2.CSoundFile_m_nMaxPeriod_get,_libmodplug2.CSoundFile_m_nMaxPeriod_set)
    __swig_setmethods__["m_nRepeatCount"] = _libmodplug2.CSoundFile_m_nRepeatCount_set
    __swig_getmethods__["m_nRepeatCount"] = _libmodplug2.CSoundFile_m_nRepeatCount_get
    if _newclass:m_nRepeatCount = property(_libmodplug2.CSoundFile_m_nRepeatCount_get,_libmodplug2.CSoundFile_m_nRepeatCount_set)
    __swig_setmethods__["m_nGlobalFadeSamples"] = _libmodplug2.CSoundFile_m_nGlobalFadeSamples_set
    __swig_getmethods__["m_nGlobalFadeSamples"] = _libmodplug2.CSoundFile_m_nGlobalFadeSamples_get
    if _newclass:m_nGlobalFadeSamples = property(_libmodplug2.CSoundFile_m_nGlobalFadeSamples_get,_libmodplug2.CSoundFile_m_nGlobalFadeSamples_set)
    __swig_setmethods__["m_nGlobalFadeMaxSamples"] = _libmodplug2.CSoundFile_m_nGlobalFadeMaxSamples_set
    __swig_getmethods__["m_nGlobalFadeMaxSamples"] = _libmodplug2.CSoundFile_m_nGlobalFadeMaxSamples_get
    if _newclass:m_nGlobalFadeMaxSamples = property(_libmodplug2.CSoundFile_m_nGlobalFadeMaxSamples_get,_libmodplug2.CSoundFile_m_nGlobalFadeMaxSamples_set)
    __swig_setmethods__["m_nMaxOrderPosition"] = _libmodplug2.CSoundFile_m_nMaxOrderPosition_set
    __swig_getmethods__["m_nMaxOrderPosition"] = _libmodplug2.CSoundFile_m_nMaxOrderPosition_get
    if _newclass:m_nMaxOrderPosition = property(_libmodplug2.CSoundFile_m_nMaxOrderPosition_get,_libmodplug2.CSoundFile_m_nMaxOrderPosition_set)
    __swig_setmethods__["m_nPatternNames"] = _libmodplug2.CSoundFile_m_nPatternNames_set
    __swig_getmethods__["m_nPatternNames"] = _libmodplug2.CSoundFile_m_nPatternNames_get
    if _newclass:m_nPatternNames = property(_libmodplug2.CSoundFile_m_nPatternNames_get,_libmodplug2.CSoundFile_m_nPatternNames_set)
    __swig_setmethods__["m_lpszSongComments"] = _libmodplug2.CSoundFile_m_lpszSongComments_set
    __swig_getmethods__["m_lpszSongComments"] = _libmodplug2.CSoundFile_m_lpszSongComments_get
    if _newclass:m_lpszSongComments = property(_libmodplug2.CSoundFile_m_lpszSongComments_get,_libmodplug2.CSoundFile_m_lpszSongComments_set)
    __swig_setmethods__["m_lpszPatternNames"] = _libmodplug2.CSoundFile_m_lpszPatternNames_set
    __swig_getmethods__["m_lpszPatternNames"] = _libmodplug2.CSoundFile_m_lpszPatternNames_get
    if _newclass:m_lpszPatternNames = property(_libmodplug2.CSoundFile_m_lpszPatternNames_get,_libmodplug2.CSoundFile_m_lpszPatternNames_set)
    __swig_setmethods__["ChnMix"] = _libmodplug2.CSoundFile_ChnMix_set
    __swig_getmethods__["ChnMix"] = _libmodplug2.CSoundFile_ChnMix_get
    if _newclass:ChnMix = property(_libmodplug2.CSoundFile_ChnMix_get,_libmodplug2.CSoundFile_ChnMix_set)
    __swig_setmethods__["Chn"] = _libmodplug2.CSoundFile_Chn_set
    __swig_getmethods__["Chn"] = _libmodplug2.CSoundFile_Chn_get
    if _newclass:Chn = property(_libmodplug2.CSoundFile_Chn_get,_libmodplug2.CSoundFile_Chn_set)
    __swig_setmethods__["ChnSettings"] = _libmodplug2.CSoundFile_ChnSettings_set
    __swig_getmethods__["ChnSettings"] = _libmodplug2.CSoundFile_ChnSettings_get
    if _newclass:ChnSettings = property(_libmodplug2.CSoundFile_ChnSettings_get,_libmodplug2.CSoundFile_ChnSettings_set)
    __swig_setmethods__["Patterns"] = _libmodplug2.CSoundFile_Patterns_set
    __swig_getmethods__["Patterns"] = _libmodplug2.CSoundFile_Patterns_get
    if _newclass:Patterns = property(_libmodplug2.CSoundFile_Patterns_get,_libmodplug2.CSoundFile_Patterns_set)
    __swig_setmethods__["PatternSize"] = _libmodplug2.CSoundFile_PatternSize_set
    __swig_getmethods__["PatternSize"] = _libmodplug2.CSoundFile_PatternSize_get
    if _newclass:PatternSize = property(_libmodplug2.CSoundFile_PatternSize_get,_libmodplug2.CSoundFile_PatternSize_set)
    __swig_setmethods__["Order"] = _libmodplug2.CSoundFile_Order_set
    __swig_getmethods__["Order"] = _libmodplug2.CSoundFile_Order_get
    if _newclass:Order = property(_libmodplug2.CSoundFile_Order_get,_libmodplug2.CSoundFile_Order_set)
    __swig_setmethods__["Ins"] = _libmodplug2.CSoundFile_Ins_set
    __swig_getmethods__["Ins"] = _libmodplug2.CSoundFile_Ins_get
    if _newclass:Ins = property(_libmodplug2.CSoundFile_Ins_get,_libmodplug2.CSoundFile_Ins_set)
    __swig_setmethods__["Headers"] = _libmodplug2.CSoundFile_Headers_set
    __swig_getmethods__["Headers"] = _libmodplug2.CSoundFile_Headers_get
    if _newclass:Headers = property(_libmodplug2.CSoundFile_Headers_get,_libmodplug2.CSoundFile_Headers_set)
    __swig_setmethods__["m_szNames"] = _libmodplug2.CSoundFile_m_szNames_set
    __swig_getmethods__["m_szNames"] = _libmodplug2.CSoundFile_m_szNames_get
    if _newclass:m_szNames = property(_libmodplug2.CSoundFile_m_szNames_get,_libmodplug2.CSoundFile_m_szNames_set)
    __swig_setmethods__["m_MidiCfg"] = _libmodplug2.CSoundFile_m_MidiCfg_set
    __swig_getmethods__["m_MidiCfg"] = _libmodplug2.CSoundFile_m_MidiCfg_get
    if _newclass:m_MidiCfg = property(_libmodplug2.CSoundFile_m_MidiCfg_get,_libmodplug2.CSoundFile_m_MidiCfg_set)
    __swig_setmethods__["m_MixPlugins"] = _libmodplug2.CSoundFile_m_MixPlugins_set
    __swig_getmethods__["m_MixPlugins"] = _libmodplug2.CSoundFile_m_MixPlugins_get
    if _newclass:m_MixPlugins = property(_libmodplug2.CSoundFile_m_MixPlugins_get,_libmodplug2.CSoundFile_m_MixPlugins_set)
    __swig_setmethods__["m_SongEQ"] = _libmodplug2.CSoundFile_m_SongEQ_set
    __swig_getmethods__["m_SongEQ"] = _libmodplug2.CSoundFile_m_SongEQ_get
    if _newclass:m_SongEQ = property(_libmodplug2.CSoundFile_m_SongEQ_get,_libmodplug2.CSoundFile_m_SongEQ_set)
    __swig_setmethods__["CompressionTable"] = _libmodplug2.CSoundFile_CompressionTable_set
    __swig_getmethods__["CompressionTable"] = _libmodplug2.CSoundFile_CompressionTable_get
    if _newclass:CompressionTable = property(_libmodplug2.CSoundFile_CompressionTable_get,_libmodplug2.CSoundFile_CompressionTable_set)
    def __init__(self,*args):
        _swig_setattr(self, CSoundFile, 'this', apply(_libmodplug2.new_CSoundFile,args))
        _swig_setattr(self, CSoundFile, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_CSoundFile):
        try:
            if self.thisown: destroy(self)
        except: pass
    __swig_getmethods__["SetWaveConfigEx"] = lambda x: _libmodplug2.CSoundFile_SetWaveConfigEx
    if _newclass:SetWaveConfigEx = staticmethod(_libmodplug2.CSoundFile_SetWaveConfigEx)
    def CreateFromString(*args): return apply(_libmodplug2.CSoundFile_CreateFromString,args)
    def SetChannelVolume(*args): return apply(_libmodplug2.CSoundFile_SetChannelVolume,args)
    def SetChannelPan(*args): return apply(_libmodplug2.CSoundFile_SetChannelPan,args)
    def GetChannelVolume(*args): return apply(_libmodplug2.CSoundFile_GetChannelVolume,args)
    def GetChannelPan(*args): return apply(_libmodplug2.CSoundFile_GetChannelPan,args)
    def GetOrder(*args): return apply(_libmodplug2.CSoundFile_GetOrder,args)
    def SetOrder(*args): return apply(_libmodplug2.CSoundFile_SetOrder,args)
    def MuteChannel(*args): return apply(_libmodplug2.CSoundFile_MuteChannel,args)
    def UnmuteChannel(*args): return apply(_libmodplug2.CSoundFile_UnmuteChannel,args)
    def IsChannelMuted(*args): return apply(_libmodplug2.CSoundFile_IsChannelMuted,args)
    def GetBuffer(*args): return apply(_libmodplug2.CSoundFile_GetBuffer,args)
    def DeleteBuffer(*args): return apply(_libmodplug2.CSoundFile_DeleteBuffer,args)
    def BufferToString(*args): return apply(_libmodplug2.CSoundFile_BufferToString,args)
    def DoesBufferClip(*args): return apply(_libmodplug2.CSoundFile_DoesBufferClip,args)
    def GetBufferMaxValue(*args): return apply(_libmodplug2.CSoundFile_GetBufferMaxValue,args)
    def PlayNote(*args): return apply(_libmodplug2.CSoundFile_PlayNote,args)
    def NoteOff(*args): return apply(_libmodplug2.CSoundFile_NoteOff,args)
    def IsNotePlaying(*args): return apply(_libmodplug2.CSoundFile_IsNotePlaying,args)
    def Create(*args): return apply(_libmodplug2.CSoundFile_Create,args)
    def Destroy(*args): return apply(_libmodplug2.CSoundFile_Destroy,args)
    def GetType(*args): return apply(_libmodplug2.CSoundFile_GetType,args)
    def GetNumChannels(*args): return apply(_libmodplug2.CSoundFile_GetNumChannels,args)
    def GetLogicalChannels(*args): return apply(_libmodplug2.CSoundFile_GetLogicalChannels,args)
    def SetMasterVolume(*args): return apply(_libmodplug2.CSoundFile_SetMasterVolume,args)
    def GetMasterVolume(*args): return apply(_libmodplug2.CSoundFile_GetMasterVolume,args)
    def GetNumPatterns(*args): return apply(_libmodplug2.CSoundFile_GetNumPatterns,args)
    def GetNumInstruments(*args): return apply(_libmodplug2.CSoundFile_GetNumInstruments,args)
    def GetNumSamples(*args): return apply(_libmodplug2.CSoundFile_GetNumSamples,args)
    def GetCurrentPos(*args): return apply(_libmodplug2.CSoundFile_GetCurrentPos,args)
    def GetCurrentPattern(*args): return apply(_libmodplug2.CSoundFile_GetCurrentPattern,args)
    def GetCurrentOrder(*args): return apply(_libmodplug2.CSoundFile_GetCurrentOrder,args)
    def GetSongComments(*args): return apply(_libmodplug2.CSoundFile_GetSongComments,args)
    def GetRawSongComments(*args): return apply(_libmodplug2.CSoundFile_GetRawSongComments,args)
    def GetMaxPosition(*args): return apply(_libmodplug2.CSoundFile_GetMaxPosition,args)
    def SetCurrentPos(*args): return apply(_libmodplug2.CSoundFile_SetCurrentPos,args)
    def SetCurrentOrder(*args): return apply(_libmodplug2.CSoundFile_SetCurrentOrder,args)
    def GetTitle(*args): return apply(_libmodplug2.CSoundFile_GetTitle,args)
    def GetSampleName(*args): return apply(_libmodplug2.CSoundFile_GetSampleName,args)
    def GetInstrumentName(*args): return apply(_libmodplug2.CSoundFile_GetInstrumentName,args)
    def GetMusicSpeed(*args): return apply(_libmodplug2.CSoundFile_GetMusicSpeed,args)
    def GetMusicTempo(*args): return apply(_libmodplug2.CSoundFile_GetMusicTempo,args)
    def GetLength(*args): return apply(_libmodplug2.CSoundFile_GetLength,args)
    def GetSongTime(*args): return apply(_libmodplug2.CSoundFile_GetSongTime,args)
    def SetRepeatCount(*args): return apply(_libmodplug2.CSoundFile_SetRepeatCount,args)
    def GetRepeatCount(*args): return apply(_libmodplug2.CSoundFile_GetRepeatCount,args)
    def IsPaused(*args): return apply(_libmodplug2.CSoundFile_IsPaused,args)
    def LoopPattern(*args): return apply(_libmodplug2.CSoundFile_LoopPattern,args)
    def CheckCPUUsage(*args): return apply(_libmodplug2.CSoundFile_CheckCPUUsage,args)
    def SetPatternName(*args): return apply(_libmodplug2.CSoundFile_SetPatternName,args)
    def GetPatternName(*args): return apply(_libmodplug2.CSoundFile_GetPatternName,args)
    def ReadXM(*args): return apply(_libmodplug2.CSoundFile_ReadXM,args)
    def ReadS3M(*args): return apply(_libmodplug2.CSoundFile_ReadS3M,args)
    def ReadMod(*args): return apply(_libmodplug2.CSoundFile_ReadMod,args)
    def ReadMed(*args): return apply(_libmodplug2.CSoundFile_ReadMed,args)
    def ReadMTM(*args): return apply(_libmodplug2.CSoundFile_ReadMTM,args)
    def ReadSTM(*args): return apply(_libmodplug2.CSoundFile_ReadSTM,args)
    def ReadIT(*args): return apply(_libmodplug2.CSoundFile_ReadIT,args)
    def Read669(*args): return apply(_libmodplug2.CSoundFile_Read669,args)
    def ReadUlt(*args): return apply(_libmodplug2.CSoundFile_ReadUlt,args)
    def ReadWav(*args): return apply(_libmodplug2.CSoundFile_ReadWav,args)
    def ReadDSM(*args): return apply(_libmodplug2.CSoundFile_ReadDSM,args)
    def ReadFAR(*args): return apply(_libmodplug2.CSoundFile_ReadFAR,args)
    def ReadAMS(*args): return apply(_libmodplug2.CSoundFile_ReadAMS,args)
    def ReadAMS2(*args): return apply(_libmodplug2.CSoundFile_ReadAMS2,args)
    def ReadMDL(*args): return apply(_libmodplug2.CSoundFile_ReadMDL,args)
    def ReadOKT(*args): return apply(_libmodplug2.CSoundFile_ReadOKT,args)
    def ReadDMF(*args): return apply(_libmodplug2.CSoundFile_ReadDMF,args)
    def ReadPTM(*args): return apply(_libmodplug2.CSoundFile_ReadPTM,args)
    def ReadDBM(*args): return apply(_libmodplug2.CSoundFile_ReadDBM,args)
    def ReadAMF(*args): return apply(_libmodplug2.CSoundFile_ReadAMF,args)
    def ReadMT2(*args): return apply(_libmodplug2.CSoundFile_ReadMT2,args)
    def ReadPSM(*args): return apply(_libmodplug2.CSoundFile_ReadPSM,args)
    def ReadUMX(*args): return apply(_libmodplug2.CSoundFile_ReadUMX,args)
    def WriteSample(*args): return apply(_libmodplug2.CSoundFile_WriteSample,args)
    def SaveXM(*args): return apply(_libmodplug2.CSoundFile_SaveXM,args)
    def SaveS3M(*args): return apply(_libmodplug2.CSoundFile_SaveS3M,args)
    def SaveMod(*args): return apply(_libmodplug2.CSoundFile_SaveMod,args)
    def SaveIT(*args): return apply(_libmodplug2.CSoundFile_SaveIT,args)
    def SaveMixPlugins(*args): return apply(_libmodplug2.CSoundFile_SaveMixPlugins,args)
    def GetBestSaveFormat(*args): return apply(_libmodplug2.CSoundFile_GetBestSaveFormat,args)
    def GetSaveFormats(*args): return apply(_libmodplug2.CSoundFile_GetSaveFormats,args)
    def ConvertModCommand(*args): return apply(_libmodplug2.CSoundFile_ConvertModCommand,args)
    def S3MConvert(*args): return apply(_libmodplug2.CSoundFile_S3MConvert,args)
    def S3MSaveConvert(*args): return apply(_libmodplug2.CSoundFile_S3MSaveConvert,args)
    def ModSaveCommand(*args): return apply(_libmodplug2.CSoundFile_ModSaveCommand,args)
    def ResetChannels(*args): return apply(_libmodplug2.CSoundFile_ResetChannels,args)
    def Read(*args): return apply(_libmodplug2.CSoundFile_Read,args)
    def ReadMix(*args): return apply(_libmodplug2.CSoundFile_ReadMix,args)
    def CreateStereoMix(*args): return apply(_libmodplug2.CSoundFile_CreateStereoMix,args)
    def FadeSong(*args): return apply(_libmodplug2.CSoundFile_FadeSong,args)
    def GlobalFadeSong(*args): return apply(_libmodplug2.CSoundFile_GlobalFadeSong,args)
    def GetTotalTickCount(*args): return apply(_libmodplug2.CSoundFile_GetTotalTickCount,args)
    def ResetTotalTickCount(*args): return apply(_libmodplug2.CSoundFile_ResetTotalTickCount,args)
    def ProcessPlugins(*args): return apply(_libmodplug2.CSoundFile_ProcessPlugins,args)
    __swig_getmethods__["InitPlayer"] = lambda x: _libmodplug2.CSoundFile_InitPlayer
    if _newclass:InitPlayer = staticmethod(_libmodplug2.CSoundFile_InitPlayer)
    __swig_getmethods__["SetWaveConfig"] = lambda x: _libmodplug2.CSoundFile_SetWaveConfig
    if _newclass:SetWaveConfig = staticmethod(_libmodplug2.CSoundFile_SetWaveConfig)
    __swig_getmethods__["SetDspEffects"] = lambda x: _libmodplug2.CSoundFile_SetDspEffects
    if _newclass:SetDspEffects = staticmethod(_libmodplug2.CSoundFile_SetDspEffects)
    __swig_getmethods__["SetResamplingMode"] = lambda x: _libmodplug2.CSoundFile_SetResamplingMode
    if _newclass:SetResamplingMode = staticmethod(_libmodplug2.CSoundFile_SetResamplingMode)
    __swig_getmethods__["IsStereo"] = lambda x: _libmodplug2.CSoundFile_IsStereo
    if _newclass:IsStereo = staticmethod(_libmodplug2.CSoundFile_IsStereo)
    __swig_getmethods__["GetSampleRate"] = lambda x: _libmodplug2.CSoundFile_GetSampleRate
    if _newclass:GetSampleRate = staticmethod(_libmodplug2.CSoundFile_GetSampleRate)
    __swig_getmethods__["GetBitsPerSample"] = lambda x: _libmodplug2.CSoundFile_GetBitsPerSample
    if _newclass:GetBitsPerSample = staticmethod(_libmodplug2.CSoundFile_GetBitsPerSample)
    __swig_getmethods__["InitSysInfo"] = lambda x: _libmodplug2.CSoundFile_InitSysInfo
    if _newclass:InitSysInfo = staticmethod(_libmodplug2.CSoundFile_InitSysInfo)
    __swig_getmethods__["GetSysInfo"] = lambda x: _libmodplug2.CSoundFile_GetSysInfo
    if _newclass:GetSysInfo = staticmethod(_libmodplug2.CSoundFile_GetSysInfo)
    __swig_getmethods__["EnableMMX"] = lambda x: _libmodplug2.CSoundFile_EnableMMX
    if _newclass:EnableMMX = staticmethod(_libmodplug2.CSoundFile_EnableMMX)
    __swig_getmethods__["GetAGC"] = lambda x: _libmodplug2.CSoundFile_GetAGC
    if _newclass:GetAGC = staticmethod(_libmodplug2.CSoundFile_GetAGC)
    __swig_getmethods__["SetAGC"] = lambda x: _libmodplug2.CSoundFile_SetAGC
    if _newclass:SetAGC = staticmethod(_libmodplug2.CSoundFile_SetAGC)
    __swig_getmethods__["ResetAGC"] = lambda x: _libmodplug2.CSoundFile_ResetAGC
    if _newclass:ResetAGC = staticmethod(_libmodplug2.CSoundFile_ResetAGC)
    __swig_getmethods__["ProcessAGC"] = lambda x: _libmodplug2.CSoundFile_ProcessAGC
    if _newclass:ProcessAGC = staticmethod(_libmodplug2.CSoundFile_ProcessAGC)
    __swig_getmethods__["InitializeDSP"] = lambda x: _libmodplug2.CSoundFile_InitializeDSP
    if _newclass:InitializeDSP = staticmethod(_libmodplug2.CSoundFile_InitializeDSP)
    __swig_getmethods__["ProcessStereoDSP"] = lambda x: _libmodplug2.CSoundFile_ProcessStereoDSP
    if _newclass:ProcessStereoDSP = staticmethod(_libmodplug2.CSoundFile_ProcessStereoDSP)
    __swig_getmethods__["ProcessMonoDSP"] = lambda x: _libmodplug2.CSoundFile_ProcessMonoDSP
    if _newclass:ProcessMonoDSP = staticmethod(_libmodplug2.CSoundFile_ProcessMonoDSP)
    __swig_getmethods__["SetReverbParameters"] = lambda x: _libmodplug2.CSoundFile_SetReverbParameters
    if _newclass:SetReverbParameters = staticmethod(_libmodplug2.CSoundFile_SetReverbParameters)
    __swig_getmethods__["SetXBassParameters"] = lambda x: _libmodplug2.CSoundFile_SetXBassParameters
    if _newclass:SetXBassParameters = staticmethod(_libmodplug2.CSoundFile_SetXBassParameters)
    __swig_getmethods__["SetSurroundParameters"] = lambda x: _libmodplug2.CSoundFile_SetSurroundParameters
    if _newclass:SetSurroundParameters = staticmethod(_libmodplug2.CSoundFile_SetSurroundParameters)
    __swig_getmethods__["InitializeEQ"] = lambda x: _libmodplug2.CSoundFile_InitializeEQ
    if _newclass:InitializeEQ = staticmethod(_libmodplug2.CSoundFile_InitializeEQ)
    __swig_getmethods__["SetEQGains"] = lambda x: _libmodplug2.CSoundFile_SetEQGains
    if _newclass:SetEQGains = staticmethod(_libmodplug2.CSoundFile_SetEQGains)
    __swig_getmethods__["EQStereo"] = lambda x: _libmodplug2.CSoundFile_EQStereo
    if _newclass:EQStereo = staticmethod(_libmodplug2.CSoundFile_EQStereo)
    __swig_getmethods__["EQMono"] = lambda x: _libmodplug2.CSoundFile_EQMono
    if _newclass:EQMono = staticmethod(_libmodplug2.CSoundFile_EQMono)
    __swig_getmethods__["WaveConvert"] = lambda x: _libmodplug2.CSoundFile_WaveConvert
    if _newclass:WaveConvert = staticmethod(_libmodplug2.CSoundFile_WaveConvert)
    __swig_getmethods__["WaveStereoConvert"] = lambda x: _libmodplug2.CSoundFile_WaveStereoConvert
    if _newclass:WaveStereoConvert = staticmethod(_libmodplug2.CSoundFile_WaveStereoConvert)
    __swig_getmethods__["SpectrumAnalyzer"] = lambda x: _libmodplug2.CSoundFile_SpectrumAnalyzer
    if _newclass:SpectrumAnalyzer = staticmethod(_libmodplug2.CSoundFile_SpectrumAnalyzer)
    __swig_getmethods__["StereoMixToFloat"] = lambda x: _libmodplug2.CSoundFile_StereoMixToFloat
    if _newclass:StereoMixToFloat = staticmethod(_libmodplug2.CSoundFile_StereoMixToFloat)
    __swig_getmethods__["FloatToStereoMix"] = lambda x: _libmodplug2.CSoundFile_FloatToStereoMix
    if _newclass:FloatToStereoMix = staticmethod(_libmodplug2.CSoundFile_FloatToStereoMix)
    __swig_getmethods__["MonoMixToFloat"] = lambda x: _libmodplug2.CSoundFile_MonoMixToFloat
    if _newclass:MonoMixToFloat = staticmethod(_libmodplug2.CSoundFile_MonoMixToFloat)
    __swig_getmethods__["FloatToMonoMix"] = lambda x: _libmodplug2.CSoundFile_FloatToMonoMix
    if _newclass:FloatToMonoMix = staticmethod(_libmodplug2.CSoundFile_FloatToMonoMix)
    def ReadNote(*args): return apply(_libmodplug2.CSoundFile_ReadNote,args)
    def ProcessRow(*args): return apply(_libmodplug2.CSoundFile_ProcessRow,args)
    def ProcessEffects(*args): return apply(_libmodplug2.CSoundFile_ProcessEffects,args)
    def GetNNAChannel(*args): return apply(_libmodplug2.CSoundFile_GetNNAChannel,args)
    def CheckNNA(*args): return apply(_libmodplug2.CSoundFile_CheckNNA,args)
    def NoteChange(*args): return apply(_libmodplug2.CSoundFile_NoteChange,args)
    def InstrumentChange(*args): return apply(_libmodplug2.CSoundFile_InstrumentChange,args)
    def PortamentoUp(*args): return apply(_libmodplug2.CSoundFile_PortamentoUp,args)
    def PortamentoDown(*args): return apply(_libmodplug2.CSoundFile_PortamentoDown,args)
    def FinePortamentoUp(*args): return apply(_libmodplug2.CSoundFile_FinePortamentoUp,args)
    def FinePortamentoDown(*args): return apply(_libmodplug2.CSoundFile_FinePortamentoDown,args)
    def ExtraFinePortamentoUp(*args): return apply(_libmodplug2.CSoundFile_ExtraFinePortamentoUp,args)
    def ExtraFinePortamentoDown(*args): return apply(_libmodplug2.CSoundFile_ExtraFinePortamentoDown,args)
    def TonePortamento(*args): return apply(_libmodplug2.CSoundFile_TonePortamento,args)
    def Vibrato(*args): return apply(_libmodplug2.CSoundFile_Vibrato,args)
    def FineVibrato(*args): return apply(_libmodplug2.CSoundFile_FineVibrato,args)
    def VolumeSlide(*args): return apply(_libmodplug2.CSoundFile_VolumeSlide,args)
    def PanningSlide(*args): return apply(_libmodplug2.CSoundFile_PanningSlide,args)
    def ChannelVolSlide(*args): return apply(_libmodplug2.CSoundFile_ChannelVolSlide,args)
    def FineVolumeUp(*args): return apply(_libmodplug2.CSoundFile_FineVolumeUp,args)
    def FineVolumeDown(*args): return apply(_libmodplug2.CSoundFile_FineVolumeDown,args)
    def Tremolo(*args): return apply(_libmodplug2.CSoundFile_Tremolo,args)
    def Panbrello(*args): return apply(_libmodplug2.CSoundFile_Panbrello,args)
    def RetrigNote(*args): return apply(_libmodplug2.CSoundFile_RetrigNote,args)
    def NoteCut(*args): return apply(_libmodplug2.CSoundFile_NoteCut,args)
    def KeyOff(*args): return apply(_libmodplug2.CSoundFile_KeyOff,args)
    def PatternLoop(*args): return apply(_libmodplug2.CSoundFile_PatternLoop,args)
    def ExtendedMODCommands(*args): return apply(_libmodplug2.CSoundFile_ExtendedMODCommands,args)
    def ExtendedS3MCommands(*args): return apply(_libmodplug2.CSoundFile_ExtendedS3MCommands,args)
    def ExtendedChannelEffect(*args): return apply(_libmodplug2.CSoundFile_ExtendedChannelEffect,args)
    def ProcessMidiMacro(*args): return apply(_libmodplug2.CSoundFile_ProcessMidiMacro,args)
    def SetupChannelFilter(*args): return apply(_libmodplug2.CSoundFile_SetupChannelFilter,args)
    def DoFreqSlide(*args): return apply(_libmodplug2.CSoundFile_DoFreqSlide,args)
    def SetTempo(*args): return apply(_libmodplug2.CSoundFile_SetTempo,args)
    def SetSpeed(*args): return apply(_libmodplug2.CSoundFile_SetSpeed,args)
    def GlobalVolSlide(*args): return apply(_libmodplug2.CSoundFile_GlobalVolSlide,args)
    def IsSongFinished(*args): return apply(_libmodplug2.CSoundFile_IsSongFinished,args)
    def IsValidBackwardJump(*args): return apply(_libmodplug2.CSoundFile_IsValidBackwardJump,args)
    def GetDeltaValue(*args): return apply(_libmodplug2.CSoundFile_GetDeltaValue,args)
    def PackSample(*args): return apply(_libmodplug2.CSoundFile_PackSample,args)
    def CanPackSample(*args): return apply(_libmodplug2.CSoundFile_CanPackSample,args)
    def ReadSample(*args): return apply(_libmodplug2.CSoundFile_ReadSample,args)
    def DestroySample(*args): return apply(_libmodplug2.CSoundFile_DestroySample,args)
    def DestroyInstrument(*args): return apply(_libmodplug2.CSoundFile_DestroyInstrument,args)
    def IsSampleUsed(*args): return apply(_libmodplug2.CSoundFile_IsSampleUsed,args)
    def IsInstrumentUsed(*args): return apply(_libmodplug2.CSoundFile_IsInstrumentUsed,args)
    def RemoveInstrumentSamples(*args): return apply(_libmodplug2.CSoundFile_RemoveInstrumentSamples,args)
    def DetectUnusedSamples(*args): return apply(_libmodplug2.CSoundFile_DetectUnusedSamples,args)
    def RemoveSelectedSamples(*args): return apply(_libmodplug2.CSoundFile_RemoveSelectedSamples,args)
    def AdjustSampleLoop(*args): return apply(_libmodplug2.CSoundFile_AdjustSampleLoop,args)
    def ReadSampleFromFile(*args): return apply(_libmodplug2.CSoundFile_ReadSampleFromFile,args)
    def ReadWAVSample(*args): return apply(_libmodplug2.CSoundFile_ReadWAVSample,args)
    def ReadPATSample(*args): return apply(_libmodplug2.CSoundFile_ReadPATSample,args)
    def ReadS3ISample(*args): return apply(_libmodplug2.CSoundFile_ReadS3ISample,args)
    def ReadAIFFSample(*args): return apply(_libmodplug2.CSoundFile_ReadAIFFSample,args)
    def ReadXISample(*args): return apply(_libmodplug2.CSoundFile_ReadXISample,args)
    def ReadITSSample(*args): return apply(_libmodplug2.CSoundFile_ReadITSSample,args)
    def Read8SVXSample(*args): return apply(_libmodplug2.CSoundFile_Read8SVXSample,args)
    def SaveWAVSample(*args): return apply(_libmodplug2.CSoundFile_SaveWAVSample,args)
    def ReadInstrumentFromFile(*args): return apply(_libmodplug2.CSoundFile_ReadInstrumentFromFile,args)
    def ReadXIInstrument(*args): return apply(_libmodplug2.CSoundFile_ReadXIInstrument,args)
    def ReadITIInstrument(*args): return apply(_libmodplug2.CSoundFile_ReadITIInstrument,args)
    def ReadPATInstrument(*args): return apply(_libmodplug2.CSoundFile_ReadPATInstrument,args)
    def ReadSampleAsInstrument(*args): return apply(_libmodplug2.CSoundFile_ReadSampleAsInstrument,args)
    def SaveXIInstrument(*args): return apply(_libmodplug2.CSoundFile_SaveXIInstrument,args)
    def SaveITIInstrument(*args): return apply(_libmodplug2.CSoundFile_SaveITIInstrument,args)
    def ReadInstrumentFromSong(*args): return apply(_libmodplug2.CSoundFile_ReadInstrumentFromSong,args)
    def ReadSampleFromSong(*args): return apply(_libmodplug2.CSoundFile_ReadSampleFromSong,args)
    def GetNoteFromPeriod(*args): return apply(_libmodplug2.CSoundFile_GetNoteFromPeriod,args)
    def GetPeriodFromNote(*args): return apply(_libmodplug2.CSoundFile_GetPeriodFromNote,args)
    def GetFreqFromPeriod(*args): return apply(_libmodplug2.CSoundFile_GetFreqFromPeriod,args)
    def GetSample(*args): return apply(_libmodplug2.CSoundFile_GetSample,args)
    def ResetMidiCfg(*args): return apply(_libmodplug2.CSoundFile_ResetMidiCfg,args)
    def ITInstrToMPT(*args): return apply(_libmodplug2.CSoundFile_ITInstrToMPT,args)
    def LoadMixPlugins(*args): return apply(_libmodplug2.CSoundFile_LoadMixPlugins,args)
    def CutOffToFrequency(*args): return apply(_libmodplug2.CSoundFile_CutOffToFrequency,args)
    __swig_getmethods__["TransposeToFrequency"] = lambda x: _libmodplug2.CSoundFile_TransposeToFrequency
    if _newclass:TransposeToFrequency = staticmethod(_libmodplug2.CSoundFile_TransposeToFrequency)
    __swig_getmethods__["FrequencyToTranspose"] = lambda x: _libmodplug2.CSoundFile_FrequencyToTranspose
    if _newclass:FrequencyToTranspose = staticmethod(_libmodplug2.CSoundFile_FrequencyToTranspose)
    __swig_getmethods__["FrequencyToTranspose"] = lambda x: _libmodplug2.CSoundFile_FrequencyToTranspose
    if _newclass:FrequencyToTranspose = staticmethod(_libmodplug2.CSoundFile_FrequencyToTranspose)
    __swig_getmethods__["AllocatePattern"] = lambda x: _libmodplug2.CSoundFile_AllocatePattern
    if _newclass:AllocatePattern = staticmethod(_libmodplug2.CSoundFile_AllocatePattern)
    __swig_getmethods__["AllocateSample"] = lambda x: _libmodplug2.CSoundFile_AllocateSample
    if _newclass:AllocateSample = staticmethod(_libmodplug2.CSoundFile_AllocateSample)
    __swig_getmethods__["FreePattern"] = lambda x: _libmodplug2.CSoundFile_FreePattern
    if _newclass:FreePattern = staticmethod(_libmodplug2.CSoundFile_FreePattern)
    __swig_getmethods__["FreeSample"] = lambda x: _libmodplug2.CSoundFile_FreeSample
    if _newclass:FreeSample = staticmethod(_libmodplug2.CSoundFile_FreeSample)
    __swig_getmethods__["Normalize24BitBuffer"] = lambda x: _libmodplug2.CSoundFile_Normalize24BitBuffer
    if _newclass:Normalize24BitBuffer = staticmethod(_libmodplug2.CSoundFile_Normalize24BitBuffer)
    def __repr__(self):
        return "<C CSoundFile instance at %s>" % (self.this,)

class CSoundFilePtr(CSoundFile):
    def __init__(self,this):
        _swig_setattr(self, CSoundFile, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, CSoundFile, 'thisown', 0)
        _swig_setattr(self, CSoundFile,self.__class__,CSoundFile)
_libmodplug2.CSoundFile_swigregister(CSoundFilePtr)
cvar = _libmodplug2.cvar
CSoundFile_SetWaveConfigEx = _libmodplug2.CSoundFile_SetWaveConfigEx

CSoundFile_InitPlayer = _libmodplug2.CSoundFile_InitPlayer

CSoundFile_SetWaveConfig = _libmodplug2.CSoundFile_SetWaveConfig

CSoundFile_SetDspEffects = _libmodplug2.CSoundFile_SetDspEffects

CSoundFile_SetResamplingMode = _libmodplug2.CSoundFile_SetResamplingMode

CSoundFile_IsStereo = _libmodplug2.CSoundFile_IsStereo

CSoundFile_GetSampleRate = _libmodplug2.CSoundFile_GetSampleRate

CSoundFile_GetBitsPerSample = _libmodplug2.CSoundFile_GetBitsPerSample

CSoundFile_InitSysInfo = _libmodplug2.CSoundFile_InitSysInfo

CSoundFile_GetSysInfo = _libmodplug2.CSoundFile_GetSysInfo

CSoundFile_EnableMMX = _libmodplug2.CSoundFile_EnableMMX

CSoundFile_GetAGC = _libmodplug2.CSoundFile_GetAGC

CSoundFile_SetAGC = _libmodplug2.CSoundFile_SetAGC

CSoundFile_ResetAGC = _libmodplug2.CSoundFile_ResetAGC

CSoundFile_ProcessAGC = _libmodplug2.CSoundFile_ProcessAGC

CSoundFile_InitializeDSP = _libmodplug2.CSoundFile_InitializeDSP

CSoundFile_ProcessStereoDSP = _libmodplug2.CSoundFile_ProcessStereoDSP

CSoundFile_ProcessMonoDSP = _libmodplug2.CSoundFile_ProcessMonoDSP

CSoundFile_SetReverbParameters = _libmodplug2.CSoundFile_SetReverbParameters

CSoundFile_SetXBassParameters = _libmodplug2.CSoundFile_SetXBassParameters

CSoundFile_SetSurroundParameters = _libmodplug2.CSoundFile_SetSurroundParameters

CSoundFile_InitializeEQ = _libmodplug2.CSoundFile_InitializeEQ

CSoundFile_SetEQGains = _libmodplug2.CSoundFile_SetEQGains

CSoundFile_EQStereo = _libmodplug2.CSoundFile_EQStereo

CSoundFile_EQMono = _libmodplug2.CSoundFile_EQMono

CSoundFile_WaveConvert = _libmodplug2.CSoundFile_WaveConvert

CSoundFile_WaveStereoConvert = _libmodplug2.CSoundFile_WaveStereoConvert

CSoundFile_SpectrumAnalyzer = _libmodplug2.CSoundFile_SpectrumAnalyzer

CSoundFile_StereoMixToFloat = _libmodplug2.CSoundFile_StereoMixToFloat

CSoundFile_FloatToStereoMix = _libmodplug2.CSoundFile_FloatToStereoMix

CSoundFile_MonoMixToFloat = _libmodplug2.CSoundFile_MonoMixToFloat

CSoundFile_FloatToMonoMix = _libmodplug2.CSoundFile_FloatToMonoMix

CSoundFile_TransposeToFrequency = _libmodplug2.CSoundFile_TransposeToFrequency

CSoundFile_FrequencyToTranspose = _libmodplug2.CSoundFile_FrequencyToTranspose

CSoundFile_AllocatePattern = _libmodplug2.CSoundFile_AllocatePattern

CSoundFile_AllocateSample = _libmodplug2.CSoundFile_AllocateSample

CSoundFile_FreePattern = _libmodplug2.CSoundFile_FreePattern

CSoundFile_FreeSample = _libmodplug2.CSoundFile_FreeSample

CSoundFile_Normalize24BitBuffer = _libmodplug2.CSoundFile_Normalize24BitBuffer


BigEndian = _libmodplug2.BigEndian

BigEndianW = _libmodplug2.BigEndianW

IFFID_FORM = _libmodplug2.IFFID_FORM
IFFID_RIFF = _libmodplug2.IFFID_RIFF
IFFID_WAVE = _libmodplug2.IFFID_WAVE
IFFID_LIST = _libmodplug2.IFFID_LIST
IFFID_INFO = _libmodplug2.IFFID_INFO
IFFID_ICOP = _libmodplug2.IFFID_ICOP
IFFID_IART = _libmodplug2.IFFID_IART
IFFID_IPRD = _libmodplug2.IFFID_IPRD
IFFID_INAM = _libmodplug2.IFFID_INAM
IFFID_ICMT = _libmodplug2.IFFID_ICMT
IFFID_IENG = _libmodplug2.IFFID_IENG
IFFID_ISFT = _libmodplug2.IFFID_ISFT
IFFID_ISBJ = _libmodplug2.IFFID_ISBJ
IFFID_IGNR = _libmodplug2.IFFID_IGNR
IFFID_ICRD = _libmodplug2.IFFID_ICRD
IFFID_wave = _libmodplug2.IFFID_wave
IFFID_fmt = _libmodplug2.IFFID_fmt
IFFID_wsmp = _libmodplug2.IFFID_wsmp
IFFID_pcm = _libmodplug2.IFFID_pcm
IFFID_data = _libmodplug2.IFFID_data
IFFID_smpl = _libmodplug2.IFFID_smpl
IFFID_xtra = _libmodplug2.IFFID_xtra
class WAVEFILEHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVEFILEHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVEFILEHEADER, name)
    __swig_setmethods__["id_RIFF"] = _libmodplug2.WAVEFILEHEADER_id_RIFF_set
    __swig_getmethods__["id_RIFF"] = _libmodplug2.WAVEFILEHEADER_id_RIFF_get
    if _newclass:id_RIFF = property(_libmodplug2.WAVEFILEHEADER_id_RIFF_get,_libmodplug2.WAVEFILEHEADER_id_RIFF_set)
    __swig_setmethods__["filesize"] = _libmodplug2.WAVEFILEHEADER_filesize_set
    __swig_getmethods__["filesize"] = _libmodplug2.WAVEFILEHEADER_filesize_get
    if _newclass:filesize = property(_libmodplug2.WAVEFILEHEADER_filesize_get,_libmodplug2.WAVEFILEHEADER_filesize_set)
    __swig_setmethods__["id_WAVE"] = _libmodplug2.WAVEFILEHEADER_id_WAVE_set
    __swig_getmethods__["id_WAVE"] = _libmodplug2.WAVEFILEHEADER_id_WAVE_get
    if _newclass:id_WAVE = property(_libmodplug2.WAVEFILEHEADER_id_WAVE_get,_libmodplug2.WAVEFILEHEADER_id_WAVE_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVEFILEHEADER, 'this', apply(_libmodplug2.new_WAVEFILEHEADER,args))
        _swig_setattr(self, WAVEFILEHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVEFILEHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVEFILEHEADER instance at %s>" % (self.this,)

class WAVEFILEHEADERPtr(WAVEFILEHEADER):
    def __init__(self,this):
        _swig_setattr(self, WAVEFILEHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVEFILEHEADER, 'thisown', 0)
        _swig_setattr(self, WAVEFILEHEADER,self.__class__,WAVEFILEHEADER)
_libmodplug2.WAVEFILEHEADER_swigregister(WAVEFILEHEADERPtr)

class WAVEFORMATHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVEFORMATHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVEFORMATHEADER, name)
    __swig_setmethods__["id_fmt"] = _libmodplug2.WAVEFORMATHEADER_id_fmt_set
    __swig_getmethods__["id_fmt"] = _libmodplug2.WAVEFORMATHEADER_id_fmt_get
    if _newclass:id_fmt = property(_libmodplug2.WAVEFORMATHEADER_id_fmt_get,_libmodplug2.WAVEFORMATHEADER_id_fmt_set)
    __swig_setmethods__["hdrlen"] = _libmodplug2.WAVEFORMATHEADER_hdrlen_set
    __swig_getmethods__["hdrlen"] = _libmodplug2.WAVEFORMATHEADER_hdrlen_get
    if _newclass:hdrlen = property(_libmodplug2.WAVEFORMATHEADER_hdrlen_get,_libmodplug2.WAVEFORMATHEADER_hdrlen_set)
    __swig_setmethods__["format"] = _libmodplug2.WAVEFORMATHEADER_format_set
    __swig_getmethods__["format"] = _libmodplug2.WAVEFORMATHEADER_format_get
    if _newclass:format = property(_libmodplug2.WAVEFORMATHEADER_format_get,_libmodplug2.WAVEFORMATHEADER_format_set)
    __swig_setmethods__["channels"] = _libmodplug2.WAVEFORMATHEADER_channels_set
    __swig_getmethods__["channels"] = _libmodplug2.WAVEFORMATHEADER_channels_get
    if _newclass:channels = property(_libmodplug2.WAVEFORMATHEADER_channels_get,_libmodplug2.WAVEFORMATHEADER_channels_set)
    __swig_setmethods__["freqHz"] = _libmodplug2.WAVEFORMATHEADER_freqHz_set
    __swig_getmethods__["freqHz"] = _libmodplug2.WAVEFORMATHEADER_freqHz_get
    if _newclass:freqHz = property(_libmodplug2.WAVEFORMATHEADER_freqHz_get,_libmodplug2.WAVEFORMATHEADER_freqHz_set)
    __swig_setmethods__["bytessec"] = _libmodplug2.WAVEFORMATHEADER_bytessec_set
    __swig_getmethods__["bytessec"] = _libmodplug2.WAVEFORMATHEADER_bytessec_get
    if _newclass:bytessec = property(_libmodplug2.WAVEFORMATHEADER_bytessec_get,_libmodplug2.WAVEFORMATHEADER_bytessec_set)
    __swig_setmethods__["samplesize"] = _libmodplug2.WAVEFORMATHEADER_samplesize_set
    __swig_getmethods__["samplesize"] = _libmodplug2.WAVEFORMATHEADER_samplesize_get
    if _newclass:samplesize = property(_libmodplug2.WAVEFORMATHEADER_samplesize_get,_libmodplug2.WAVEFORMATHEADER_samplesize_set)
    __swig_setmethods__["bitspersample"] = _libmodplug2.WAVEFORMATHEADER_bitspersample_set
    __swig_getmethods__["bitspersample"] = _libmodplug2.WAVEFORMATHEADER_bitspersample_get
    if _newclass:bitspersample = property(_libmodplug2.WAVEFORMATHEADER_bitspersample_get,_libmodplug2.WAVEFORMATHEADER_bitspersample_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVEFORMATHEADER, 'this', apply(_libmodplug2.new_WAVEFORMATHEADER,args))
        _swig_setattr(self, WAVEFORMATHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVEFORMATHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVEFORMATHEADER instance at %s>" % (self.this,)

class WAVEFORMATHEADERPtr(WAVEFORMATHEADER):
    def __init__(self,this):
        _swig_setattr(self, WAVEFORMATHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVEFORMATHEADER, 'thisown', 0)
        _swig_setattr(self, WAVEFORMATHEADER,self.__class__,WAVEFORMATHEADER)
_libmodplug2.WAVEFORMATHEADER_swigregister(WAVEFORMATHEADERPtr)

class WAVEDATAHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVEDATAHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVEDATAHEADER, name)
    __swig_setmethods__["id_data"] = _libmodplug2.WAVEDATAHEADER_id_data_set
    __swig_getmethods__["id_data"] = _libmodplug2.WAVEDATAHEADER_id_data_get
    if _newclass:id_data = property(_libmodplug2.WAVEDATAHEADER_id_data_get,_libmodplug2.WAVEDATAHEADER_id_data_set)
    __swig_setmethods__["length"] = _libmodplug2.WAVEDATAHEADER_length_set
    __swig_getmethods__["length"] = _libmodplug2.WAVEDATAHEADER_length_get
    if _newclass:length = property(_libmodplug2.WAVEDATAHEADER_length_get,_libmodplug2.WAVEDATAHEADER_length_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVEDATAHEADER, 'this', apply(_libmodplug2.new_WAVEDATAHEADER,args))
        _swig_setattr(self, WAVEDATAHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVEDATAHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVEDATAHEADER instance at %s>" % (self.this,)

class WAVEDATAHEADERPtr(WAVEDATAHEADER):
    def __init__(self,this):
        _swig_setattr(self, WAVEDATAHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVEDATAHEADER, 'thisown', 0)
        _swig_setattr(self, WAVEDATAHEADER,self.__class__,WAVEDATAHEADER)
_libmodplug2.WAVEDATAHEADER_swigregister(WAVEDATAHEADERPtr)

class WAVESMPLHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVESMPLHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVESMPLHEADER, name)
    __swig_setmethods__["smpl_id"] = _libmodplug2.WAVESMPLHEADER_smpl_id_set
    __swig_getmethods__["smpl_id"] = _libmodplug2.WAVESMPLHEADER_smpl_id_get
    if _newclass:smpl_id = property(_libmodplug2.WAVESMPLHEADER_smpl_id_get,_libmodplug2.WAVESMPLHEADER_smpl_id_set)
    __swig_setmethods__["smpl_len"] = _libmodplug2.WAVESMPLHEADER_smpl_len_set
    __swig_getmethods__["smpl_len"] = _libmodplug2.WAVESMPLHEADER_smpl_len_get
    if _newclass:smpl_len = property(_libmodplug2.WAVESMPLHEADER_smpl_len_get,_libmodplug2.WAVESMPLHEADER_smpl_len_set)
    __swig_setmethods__["dwManufacturer"] = _libmodplug2.WAVESMPLHEADER_dwManufacturer_set
    __swig_getmethods__["dwManufacturer"] = _libmodplug2.WAVESMPLHEADER_dwManufacturer_get
    if _newclass:dwManufacturer = property(_libmodplug2.WAVESMPLHEADER_dwManufacturer_get,_libmodplug2.WAVESMPLHEADER_dwManufacturer_set)
    __swig_setmethods__["dwProduct"] = _libmodplug2.WAVESMPLHEADER_dwProduct_set
    __swig_getmethods__["dwProduct"] = _libmodplug2.WAVESMPLHEADER_dwProduct_get
    if _newclass:dwProduct = property(_libmodplug2.WAVESMPLHEADER_dwProduct_get,_libmodplug2.WAVESMPLHEADER_dwProduct_set)
    __swig_setmethods__["dwSamplePeriod"] = _libmodplug2.WAVESMPLHEADER_dwSamplePeriod_set
    __swig_getmethods__["dwSamplePeriod"] = _libmodplug2.WAVESMPLHEADER_dwSamplePeriod_get
    if _newclass:dwSamplePeriod = property(_libmodplug2.WAVESMPLHEADER_dwSamplePeriod_get,_libmodplug2.WAVESMPLHEADER_dwSamplePeriod_set)
    __swig_setmethods__["dwBaseNote"] = _libmodplug2.WAVESMPLHEADER_dwBaseNote_set
    __swig_getmethods__["dwBaseNote"] = _libmodplug2.WAVESMPLHEADER_dwBaseNote_get
    if _newclass:dwBaseNote = property(_libmodplug2.WAVESMPLHEADER_dwBaseNote_get,_libmodplug2.WAVESMPLHEADER_dwBaseNote_set)
    __swig_setmethods__["dwPitchFraction"] = _libmodplug2.WAVESMPLHEADER_dwPitchFraction_set
    __swig_getmethods__["dwPitchFraction"] = _libmodplug2.WAVESMPLHEADER_dwPitchFraction_get
    if _newclass:dwPitchFraction = property(_libmodplug2.WAVESMPLHEADER_dwPitchFraction_get,_libmodplug2.WAVESMPLHEADER_dwPitchFraction_set)
    __swig_setmethods__["dwSMPTEFormat"] = _libmodplug2.WAVESMPLHEADER_dwSMPTEFormat_set
    __swig_getmethods__["dwSMPTEFormat"] = _libmodplug2.WAVESMPLHEADER_dwSMPTEFormat_get
    if _newclass:dwSMPTEFormat = property(_libmodplug2.WAVESMPLHEADER_dwSMPTEFormat_get,_libmodplug2.WAVESMPLHEADER_dwSMPTEFormat_set)
    __swig_setmethods__["dwSMPTEOffset"] = _libmodplug2.WAVESMPLHEADER_dwSMPTEOffset_set
    __swig_getmethods__["dwSMPTEOffset"] = _libmodplug2.WAVESMPLHEADER_dwSMPTEOffset_get
    if _newclass:dwSMPTEOffset = property(_libmodplug2.WAVESMPLHEADER_dwSMPTEOffset_get,_libmodplug2.WAVESMPLHEADER_dwSMPTEOffset_set)
    __swig_setmethods__["dwSampleLoops"] = _libmodplug2.WAVESMPLHEADER_dwSampleLoops_set
    __swig_getmethods__["dwSampleLoops"] = _libmodplug2.WAVESMPLHEADER_dwSampleLoops_get
    if _newclass:dwSampleLoops = property(_libmodplug2.WAVESMPLHEADER_dwSampleLoops_get,_libmodplug2.WAVESMPLHEADER_dwSampleLoops_set)
    __swig_setmethods__["cbSamplerData"] = _libmodplug2.WAVESMPLHEADER_cbSamplerData_set
    __swig_getmethods__["cbSamplerData"] = _libmodplug2.WAVESMPLHEADER_cbSamplerData_get
    if _newclass:cbSamplerData = property(_libmodplug2.WAVESMPLHEADER_cbSamplerData_get,_libmodplug2.WAVESMPLHEADER_cbSamplerData_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVESMPLHEADER, 'this', apply(_libmodplug2.new_WAVESMPLHEADER,args))
        _swig_setattr(self, WAVESMPLHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVESMPLHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVESMPLHEADER instance at %s>" % (self.this,)

class WAVESMPLHEADERPtr(WAVESMPLHEADER):
    def __init__(self,this):
        _swig_setattr(self, WAVESMPLHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVESMPLHEADER, 'thisown', 0)
        _swig_setattr(self, WAVESMPLHEADER,self.__class__,WAVESMPLHEADER)
_libmodplug2.WAVESMPLHEADER_swigregister(WAVESMPLHEADERPtr)

class SAMPLELOOPSTRUCT(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SAMPLELOOPSTRUCT, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SAMPLELOOPSTRUCT, name)
    __swig_setmethods__["dwIdentifier"] = _libmodplug2.SAMPLELOOPSTRUCT_dwIdentifier_set
    __swig_getmethods__["dwIdentifier"] = _libmodplug2.SAMPLELOOPSTRUCT_dwIdentifier_get
    if _newclass:dwIdentifier = property(_libmodplug2.SAMPLELOOPSTRUCT_dwIdentifier_get,_libmodplug2.SAMPLELOOPSTRUCT_dwIdentifier_set)
    __swig_setmethods__["dwLoopType"] = _libmodplug2.SAMPLELOOPSTRUCT_dwLoopType_set
    __swig_getmethods__["dwLoopType"] = _libmodplug2.SAMPLELOOPSTRUCT_dwLoopType_get
    if _newclass:dwLoopType = property(_libmodplug2.SAMPLELOOPSTRUCT_dwLoopType_get,_libmodplug2.SAMPLELOOPSTRUCT_dwLoopType_set)
    __swig_setmethods__["dwLoopStart"] = _libmodplug2.SAMPLELOOPSTRUCT_dwLoopStart_set
    __swig_getmethods__["dwLoopStart"] = _libmodplug2.SAMPLELOOPSTRUCT_dwLoopStart_get
    if _newclass:dwLoopStart = property(_libmodplug2.SAMPLELOOPSTRUCT_dwLoopStart_get,_libmodplug2.SAMPLELOOPSTRUCT_dwLoopStart_set)
    __swig_setmethods__["dwLoopEnd"] = _libmodplug2.SAMPLELOOPSTRUCT_dwLoopEnd_set
    __swig_getmethods__["dwLoopEnd"] = _libmodplug2.SAMPLELOOPSTRUCT_dwLoopEnd_get
    if _newclass:dwLoopEnd = property(_libmodplug2.SAMPLELOOPSTRUCT_dwLoopEnd_get,_libmodplug2.SAMPLELOOPSTRUCT_dwLoopEnd_set)
    __swig_setmethods__["dwFraction"] = _libmodplug2.SAMPLELOOPSTRUCT_dwFraction_set
    __swig_getmethods__["dwFraction"] = _libmodplug2.SAMPLELOOPSTRUCT_dwFraction_get
    if _newclass:dwFraction = property(_libmodplug2.SAMPLELOOPSTRUCT_dwFraction_get,_libmodplug2.SAMPLELOOPSTRUCT_dwFraction_set)
    __swig_setmethods__["dwPlayCount"] = _libmodplug2.SAMPLELOOPSTRUCT_dwPlayCount_set
    __swig_getmethods__["dwPlayCount"] = _libmodplug2.SAMPLELOOPSTRUCT_dwPlayCount_get
    if _newclass:dwPlayCount = property(_libmodplug2.SAMPLELOOPSTRUCT_dwPlayCount_get,_libmodplug2.SAMPLELOOPSTRUCT_dwPlayCount_set)
    def __init__(self,*args):
        _swig_setattr(self, SAMPLELOOPSTRUCT, 'this', apply(_libmodplug2.new_SAMPLELOOPSTRUCT,args))
        _swig_setattr(self, SAMPLELOOPSTRUCT, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_SAMPLELOOPSTRUCT):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C SAMPLELOOPSTRUCT instance at %s>" % (self.this,)

class SAMPLELOOPSTRUCTPtr(SAMPLELOOPSTRUCT):
    def __init__(self,this):
        _swig_setattr(self, SAMPLELOOPSTRUCT, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, SAMPLELOOPSTRUCT, 'thisown', 0)
        _swig_setattr(self, SAMPLELOOPSTRUCT,self.__class__,SAMPLELOOPSTRUCT)
_libmodplug2.SAMPLELOOPSTRUCT_swigregister(SAMPLELOOPSTRUCTPtr)

class WAVESAMPLERINFO(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVESAMPLERINFO, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVESAMPLERINFO, name)
    __swig_setmethods__["wsiHdr"] = _libmodplug2.WAVESAMPLERINFO_wsiHdr_set
    __swig_getmethods__["wsiHdr"] = _libmodplug2.WAVESAMPLERINFO_wsiHdr_get
    if _newclass:wsiHdr = property(_libmodplug2.WAVESAMPLERINFO_wsiHdr_get,_libmodplug2.WAVESAMPLERINFO_wsiHdr_set)
    __swig_setmethods__["wsiLoops"] = _libmodplug2.WAVESAMPLERINFO_wsiLoops_set
    __swig_getmethods__["wsiLoops"] = _libmodplug2.WAVESAMPLERINFO_wsiLoops_get
    if _newclass:wsiLoops = property(_libmodplug2.WAVESAMPLERINFO_wsiLoops_get,_libmodplug2.WAVESAMPLERINFO_wsiLoops_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVESAMPLERINFO, 'this', apply(_libmodplug2.new_WAVESAMPLERINFO,args))
        _swig_setattr(self, WAVESAMPLERINFO, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVESAMPLERINFO):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVESAMPLERINFO instance at %s>" % (self.this,)

class WAVESAMPLERINFOPtr(WAVESAMPLERINFO):
    def __init__(self,this):
        _swig_setattr(self, WAVESAMPLERINFO, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVESAMPLERINFO, 'thisown', 0)
        _swig_setattr(self, WAVESAMPLERINFO,self.__class__,WAVESAMPLERINFO)
_libmodplug2.WAVESAMPLERINFO_swigregister(WAVESAMPLERINFOPtr)

class WAVELISTHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVELISTHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVELISTHEADER, name)
    __swig_setmethods__["list_id"] = _libmodplug2.WAVELISTHEADER_list_id_set
    __swig_getmethods__["list_id"] = _libmodplug2.WAVELISTHEADER_list_id_get
    if _newclass:list_id = property(_libmodplug2.WAVELISTHEADER_list_id_get,_libmodplug2.WAVELISTHEADER_list_id_set)
    __swig_setmethods__["list_len"] = _libmodplug2.WAVELISTHEADER_list_len_set
    __swig_getmethods__["list_len"] = _libmodplug2.WAVELISTHEADER_list_len_get
    if _newclass:list_len = property(_libmodplug2.WAVELISTHEADER_list_len_get,_libmodplug2.WAVELISTHEADER_list_len_set)
    __swig_setmethods__["info"] = _libmodplug2.WAVELISTHEADER_info_set
    __swig_getmethods__["info"] = _libmodplug2.WAVELISTHEADER_info_get
    if _newclass:info = property(_libmodplug2.WAVELISTHEADER_info_get,_libmodplug2.WAVELISTHEADER_info_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVELISTHEADER, 'this', apply(_libmodplug2.new_WAVELISTHEADER,args))
        _swig_setattr(self, WAVELISTHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVELISTHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVELISTHEADER instance at %s>" % (self.this,)

class WAVELISTHEADERPtr(WAVELISTHEADER):
    def __init__(self,this):
        _swig_setattr(self, WAVELISTHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVELISTHEADER, 'thisown', 0)
        _swig_setattr(self, WAVELISTHEADER,self.__class__,WAVELISTHEADER)
_libmodplug2.WAVELISTHEADER_swigregister(WAVELISTHEADERPtr)

class WAVEEXTRAHEADER(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WAVEEXTRAHEADER, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WAVEEXTRAHEADER, name)
    __swig_setmethods__["xtra_id"] = _libmodplug2.WAVEEXTRAHEADER_xtra_id_set
    __swig_getmethods__["xtra_id"] = _libmodplug2.WAVEEXTRAHEADER_xtra_id_get
    if _newclass:xtra_id = property(_libmodplug2.WAVEEXTRAHEADER_xtra_id_get,_libmodplug2.WAVEEXTRAHEADER_xtra_id_set)
    __swig_setmethods__["xtra_len"] = _libmodplug2.WAVEEXTRAHEADER_xtra_len_set
    __swig_getmethods__["xtra_len"] = _libmodplug2.WAVEEXTRAHEADER_xtra_len_get
    if _newclass:xtra_len = property(_libmodplug2.WAVEEXTRAHEADER_xtra_len_get,_libmodplug2.WAVEEXTRAHEADER_xtra_len_set)
    __swig_setmethods__["dwFlags"] = _libmodplug2.WAVEEXTRAHEADER_dwFlags_set
    __swig_getmethods__["dwFlags"] = _libmodplug2.WAVEEXTRAHEADER_dwFlags_get
    if _newclass:dwFlags = property(_libmodplug2.WAVEEXTRAHEADER_dwFlags_get,_libmodplug2.WAVEEXTRAHEADER_dwFlags_set)
    __swig_setmethods__["wPan"] = _libmodplug2.WAVEEXTRAHEADER_wPan_set
    __swig_getmethods__["wPan"] = _libmodplug2.WAVEEXTRAHEADER_wPan_get
    if _newclass:wPan = property(_libmodplug2.WAVEEXTRAHEADER_wPan_get,_libmodplug2.WAVEEXTRAHEADER_wPan_set)
    __swig_setmethods__["wVolume"] = _libmodplug2.WAVEEXTRAHEADER_wVolume_set
    __swig_getmethods__["wVolume"] = _libmodplug2.WAVEEXTRAHEADER_wVolume_get
    if _newclass:wVolume = property(_libmodplug2.WAVEEXTRAHEADER_wVolume_get,_libmodplug2.WAVEEXTRAHEADER_wVolume_set)
    __swig_setmethods__["wGlobalVol"] = _libmodplug2.WAVEEXTRAHEADER_wGlobalVol_set
    __swig_getmethods__["wGlobalVol"] = _libmodplug2.WAVEEXTRAHEADER_wGlobalVol_get
    if _newclass:wGlobalVol = property(_libmodplug2.WAVEEXTRAHEADER_wGlobalVol_get,_libmodplug2.WAVEEXTRAHEADER_wGlobalVol_set)
    __swig_setmethods__["wReserved"] = _libmodplug2.WAVEEXTRAHEADER_wReserved_set
    __swig_getmethods__["wReserved"] = _libmodplug2.WAVEEXTRAHEADER_wReserved_get
    if _newclass:wReserved = property(_libmodplug2.WAVEEXTRAHEADER_wReserved_get,_libmodplug2.WAVEEXTRAHEADER_wReserved_set)
    __swig_setmethods__["nVibType"] = _libmodplug2.WAVEEXTRAHEADER_nVibType_set
    __swig_getmethods__["nVibType"] = _libmodplug2.WAVEEXTRAHEADER_nVibType_get
    if _newclass:nVibType = property(_libmodplug2.WAVEEXTRAHEADER_nVibType_get,_libmodplug2.WAVEEXTRAHEADER_nVibType_set)
    __swig_setmethods__["nVibSweep"] = _libmodplug2.WAVEEXTRAHEADER_nVibSweep_set
    __swig_getmethods__["nVibSweep"] = _libmodplug2.WAVEEXTRAHEADER_nVibSweep_get
    if _newclass:nVibSweep = property(_libmodplug2.WAVEEXTRAHEADER_nVibSweep_get,_libmodplug2.WAVEEXTRAHEADER_nVibSweep_set)
    __swig_setmethods__["nVibDepth"] = _libmodplug2.WAVEEXTRAHEADER_nVibDepth_set
    __swig_getmethods__["nVibDepth"] = _libmodplug2.WAVEEXTRAHEADER_nVibDepth_get
    if _newclass:nVibDepth = property(_libmodplug2.WAVEEXTRAHEADER_nVibDepth_get,_libmodplug2.WAVEEXTRAHEADER_nVibDepth_set)
    __swig_setmethods__["nVibRate"] = _libmodplug2.WAVEEXTRAHEADER_nVibRate_set
    __swig_getmethods__["nVibRate"] = _libmodplug2.WAVEEXTRAHEADER_nVibRate_get
    if _newclass:nVibRate = property(_libmodplug2.WAVEEXTRAHEADER_nVibRate_get,_libmodplug2.WAVEEXTRAHEADER_nVibRate_set)
    def __init__(self,*args):
        _swig_setattr(self, WAVEEXTRAHEADER, 'this', apply(_libmodplug2.new_WAVEEXTRAHEADER,args))
        _swig_setattr(self, WAVEEXTRAHEADER, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_WAVEEXTRAHEADER):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C WAVEEXTRAHEADER instance at %s>" % (self.this,)

class WAVEEXTRAHEADERPtr(WAVEEXTRAHEADER):
    def __init__(self,this):
        _swig_setattr(self, WAVEEXTRAHEADER, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, WAVEEXTRAHEADER, 'thisown', 0)
        _swig_setattr(self, WAVEEXTRAHEADER,self.__class__,WAVEEXTRAHEADER)
_libmodplug2.WAVEEXTRAHEADER_swigregister(WAVEEXTRAHEADERPtr)

MIXBUFFERSIZE = _libmodplug2.MIXBUFFERSIZE
MIXING_ATTENUATION = _libmodplug2.MIXING_ATTENUATION
MIXING_CLIPMIN = _libmodplug2.MIXING_CLIPMIN
MIXING_CLIPMAX = _libmodplug2.MIXING_CLIPMAX
VOLUMERAMPPRECISION = _libmodplug2.VOLUMERAMPPRECISION
FADESONGDELAY = _libmodplug2.FADESONGDELAY
EQ_BUFFERSIZE = _libmodplug2.EQ_BUFFERSIZE
AGC_PRECISION = _libmodplug2.AGC_PRECISION
AGC_UNITY = _libmodplug2.AGC_UNITY
_muldiv = _libmodplug2._muldiv

_muldivr = _libmodplug2._muldivr

class MODFORMATINFO(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MODFORMATINFO, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MODFORMATINFO, name)
    __swig_setmethods__["dwFormatId"] = _libmodplug2.MODFORMATINFO_dwFormatId_set
    __swig_getmethods__["dwFormatId"] = _libmodplug2.MODFORMATINFO_dwFormatId_get
    if _newclass:dwFormatId = property(_libmodplug2.MODFORMATINFO_dwFormatId_get,_libmodplug2.MODFORMATINFO_dwFormatId_set)
    __swig_setmethods__["lpszFormatName"] = _libmodplug2.MODFORMATINFO_lpszFormatName_set
    __swig_getmethods__["lpszFormatName"] = _libmodplug2.MODFORMATINFO_lpszFormatName_get
    if _newclass:lpszFormatName = property(_libmodplug2.MODFORMATINFO_lpszFormatName_get,_libmodplug2.MODFORMATINFO_lpszFormatName_set)
    __swig_setmethods__["lpszExtension"] = _libmodplug2.MODFORMATINFO_lpszExtension_set
    __swig_getmethods__["lpszExtension"] = _libmodplug2.MODFORMATINFO_lpszExtension_get
    if _newclass:lpszExtension = property(_libmodplug2.MODFORMATINFO_lpszExtension_get,_libmodplug2.MODFORMATINFO_lpszExtension_set)
    __swig_setmethods__["dwPadding"] = _libmodplug2.MODFORMATINFO_dwPadding_set
    __swig_getmethods__["dwPadding"] = _libmodplug2.MODFORMATINFO_dwPadding_get
    if _newclass:dwPadding = property(_libmodplug2.MODFORMATINFO_dwPadding_get,_libmodplug2.MODFORMATINFO_dwPadding_set)
    def __init__(self,*args):
        _swig_setattr(self, MODFORMATINFO, 'this', apply(_libmodplug2.new_MODFORMATINFO,args))
        _swig_setattr(self, MODFORMATINFO, 'thisown', 1)
    def __del__(self, destroy= _libmodplug2.delete_MODFORMATINFO):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C MODFORMATINFO instance at %s>" % (self.this,)

class MODFORMATINFOPtr(MODFORMATINFO):
    def __init__(self,this):
        _swig_setattr(self, MODFORMATINFO, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, MODFORMATINFO, 'thisown', 0)
        _swig_setattr(self, MODFORMATINFO,self.__class__,MODFORMATINFO)
_libmodplug2.MODFORMATINFO_swigregister(MODFORMATINFOPtr)

InitializePlugins = _libmodplug2.InitializePlugins

UninitializePlugins = _libmodplug2.UninitializePlugins

AddPlugin = _libmodplug2.AddPlugin

RemovePlugin = _libmodplug2.RemovePlugin

GetModplugStreamProc = _libmodplug2.GetModplugStreamProc

GetCSoundFilePointerValue = _libmodplug2.GetCSoundFilePointerValue

CreateModplugStream = _libmodplug2.CreateModplugStream

SetSampleSize = _libmodplug2.SetSampleSize

GetSampleSize = _libmodplug2.GetSampleSize


