
# BASS 2.3.0.1 wrapper

from ctypes import *
BASS = windll.LoadLibrary("d:\\blueberry\\dev\\postmod\\BASS.dll")




BASS_OK = 0               #all is OK
BASS_ERROR_MEM = 1        #memory error
BASS_ERROR_FILEOPEN = 2   #can#t open the file
BASS_ERROR_DRIVER = 3     #can#t find a free sound driver
BASS_ERROR_BUFLOST = 4    #the sample buffer was lost
BASS_ERROR_HANDLE = 5     #invalid handle
BASS_ERROR_FORMAT = 6     #unsupported sample format
BASS_ERROR_POSITION = 7   #invalid playback position
BASS_ERROR_INIT = 8       #BASS_Init has not been successfully called
BASS_ERROR_START = 9      #BASS_Start has not been successfully called
BASS_ERROR_ALREADY = 14   #already initialized/paused/whatever
BASS_ERROR_NOPAUSE = 16   #not paused
BASS_ERROR_NOCHAN = 18    #can#t get a free channel
BASS_ERROR_ILLTYPE = 19   #an illegal type was specified
BASS_ERROR_ILLPARAM = 20  #an illegal parameter was specified
BASS_ERROR_NO3D = 21      #no 3D support
BASS_ERROR_NOEAX = 22     #no EAX support
BASS_ERROR_DEVICE = 23    #illegal device number
BASS_ERROR_NOPLAY = 24    #not playing
BASS_ERROR_FREQ = 25      #illegal sample rate
BASS_ERROR_NOTFILE = 27   #the stream is not a file stream
BASS_ERROR_NOHW = 29      #no hardware voices available
BASS_ERROR_EMPTY = 31     #the MOD music has no sequence data
BASS_ERROR_NONET = 32     #no internet connection could be opened
BASS_ERROR_CREATE = 33    #couldn#t create the file
BASS_ERROR_NOFX = 34      #effects are not available
BASS_ERROR_PLAYING = 35   #the channel is playing
BASS_ERROR_NOTAVAIL = 37  #requested data is not available
BASS_ERROR_DECODE = 38    #the channel is a "decoding channel"
BASS_ERROR_DX = 39        #a sufficient DirectX version is not installed
BASS_ERROR_TIMEOUT = 40   #connection timedout
BASS_ERROR_FILEFORM = 41  #unsupported file format
BASS_ERROR_SPEAKER = 42   #unavailable speaker
BASS_ERROR_VERSION = 43   #invalid BASS version (used by add-ons)
BASS_ERROR_CODEC = 44     #codec is not available/supported
BASS_ERROR_UNKNOWN = -1   #some other mystery error

#************************
#* Initialization flags *
#************************
BASS_DEVICE_8BITS = 1     #use 8 bit resolution, else 16 bit
BASS_DEVICE_MONO = 2      #use mono, else stereo
BASS_DEVICE_3D = 4        #enable 3D functionality
# If the BASS_DEVICE_3D flag is not specified when initilizing BASS,
# then the 3D flags (BASS_SAMPLE_3D and BASS_MUSIC_3D) are ignored when
# loading/creating a sample/stream/music.
BASS_DEVICE_LATENCY = 256 #calculate device latency (BASS_INFO struct)
BASS_DEVICE_SPEAKERS = 2048 #force enabling of speaker assignment
BASS_DEVICE_NOSPEAKER = 4096 #ignore speaker arrangement

#***********************************
#* BASS_INFO flags (from DSOUND.H) *
#***********************************
DSCAPS_CONTINUOUSRATE = 16
# supports all sample rates between min/maxrate
DSCAPS_EMULDRIVER = 32
# device does NOT have hardware DirectSound support
DSCAPS_CERTIFIED = 64
# device driver has been certified by Microsoft
# The following flags tell what type of samples are supported by HARDWARE
# mixing, all these formats are supported by SOFTWARE mixing
DSCAPS_SECONDARYMONO = 256    # mono
DSCAPS_SECONDARYSTEREO = 512  # stereo
DSCAPS_SECONDARY8BIT = 1024   # 8 bit
DSCAPS_SECONDARY16BIT = 2048  # 16 bit

#*****************************************
#* BASS_RECORDINFO flags (from DSOUND.H) *
#*****************************************
DSCCAPS_EMULDRIVER = DSCAPS_EMULDRIVER
# device does NOT have hardware DirectSound recording support
DSCCAPS_CERTIFIED = DSCAPS_CERTIFIED
# device driver has been certified by Microsoft

#******************************************************************
#* defines for formats field of BASS_RECORDINFO (from MMSYSTEM.H) *
#******************************************************************
WAVE_FORMAT_1M08 = 0x1          # 11.025 kHz, Mono,   8-bit
WAVE_FORMAT_1S08 = 0x2          # 11.025 kHz, Stereo, 8-bit
WAVE_FORMAT_1M16 = 0x4          # 11.025 kHz, Mono,   16-bit
WAVE_FORMAT_1S16 = 0x8          # 11.025 kHz, Stereo, 16-bit
WAVE_FORMAT_2M08 = 0x10         # 22.05  kHz, Mono,   8-bit
WAVE_FORMAT_2S08 = 0x20         # 22.05  kHz, Stereo, 8-bit
WAVE_FORMAT_2M16 = 0x40         # 22.05  kHz, Mono,   16-bit
WAVE_FORMAT_2S16 = 0x80         # 22.05  kHz, Stereo, 16-bit
WAVE_FORMAT_4M08 = 0x100        # 44.1   kHz, Mono,   8-bit
WAVE_FORMAT_4S08 = 0x200        # 44.1   kHz, Stereo, 8-bit
WAVE_FORMAT_4M16 = 0x400        # 44.1   kHz, Mono,   16-bit
WAVE_FORMAT_4S16 = 0x800        # 44.1   kHz, Stereo, 16-bit

#*********************
#* Sample info flags *
#*********************
BASS_SAMPLE_8BITS = 1          # 8 bit
BASS_SAMPLE_FLOAT = 256        # 32-bit floating-point
BASS_SAMPLE_MONO = 2           # mono, else stereo
BASS_SAMPLE_LOOP = 4           # looped
BASS_SAMPLE_3D = 8             # 3D functionality enabled
BASS_SAMPLE_SOFTWARE = 16      # it#s NOT using hardware mixing
BASS_SAMPLE_MUTEMAX = 32       # muted at max distance (3D only)
BASS_SAMPLE_VAM = 64           # uses the DX7 voice allocation & management
BASS_SAMPLE_FX = 128           # old implementation of DX8 effects are enabled
BASS_SAMPLE_OVER_VOL = 0x10000 # override lowest volume
BASS_SAMPLE_OVER_POS = 0x20000 # override longest playing
BASS_SAMPLE_OVER_DIST = 0x30000 # override furthest from listener (3D only)

BASS_STREAM_PRESCAN = 0x20000   # enable pin-point seeking (MP3/MP2/MP1)
BASS_MP3_SETPOS = BASS_STREAM_PRESCAN
BASS_STREAM_AUTOFREE = 0x40000 # automatically free the stream when it stop/ends
BASS_STREAM_RESTRATE = 0x80000 # restrict the download rate of internet file streams
BASS_STREAM_BLOCK = 0x100000   # download/play internet file stream in small blocks
BASS_STREAM_DECODE = 0x200000  # don#t play the stream, only decode (BASS_ChannelGetData)
BASS_STREAM_STATUS = 0x800000  # give server status info (HTTP/ICY tags) in DOWNLOADPROC

BASS_MUSIC_FLOAT = BASS_SAMPLE_FLOAT # 32-bit floating-point
BASS_MUSIC_MONO = BASS_SAMPLE_MONO # force mono mixing (less CPU usage)
BASS_MUSIC_LOOP = BASS_SAMPLE_LOOP # loop music
BASS_MUSIC_3D = BASS_SAMPLE_3D # enable 3D functionality
BASS_MUSIC_FX = BASS_SAMPLE_FX # enable old implementation of DX8 effects
BASS_MUSIC_AUTOFREE = BASS_STREAM_AUTOFREE # automatically free the music when it stop/ends
BASS_MUSIC_DECODE = BASS_STREAM_DECODE # don#t play the music, only decode (BASS_ChannelGetData)
BASS_MUSIC_PRESCAN = BASS_STREAM_PRESCAN # calculate playback length
BASS_MUSIC_CALCLEN = BASS_MUSIC_PRESCAN
BASS_MUSIC_RAMP = 0x200        # normal ramping
BASS_MUSIC_RAMPS = 0x400       # sensitive ramping
BASS_MUSIC_SURROUND = 0x800    # surround sound
BASS_MUSIC_SURROUND2 = 0x1000  # surround sound (mode 2)
BASS_MUSIC_FT2MOD = 0x2000     # play .MOD as FastTracker 2 does
BASS_MUSIC_PT1MOD = 0x4000     # play .MOD as ProTracker 1 does
BASS_MUSIC_NONINTER = 0x10000  # non-interpolated mixing
BASS_MUSIC_POSRESET = 32768  # stop all notes when moving position
BASS_MUSIC_POSRESETEX = 0x400000 # stop all notes and reset bmp/etc when moving position
BASS_MUSIC_STOPBACK = 0x80000  # stop the music on a backwards jump effect
BASS_MUSIC_NOSAMPLE = 0x100000 # don#t load the samples

# Speaker assignment flags
BASS_SPEAKER_FRONT = 0x1000000 # front speakers
BASS_SPEAKER_REAR = 0x2000000  # rear/side speakers
BASS_SPEAKER_CENLFE = 0x3000000 # center & LFE speakers (5.1)
BASS_SPEAKER_REAR2 = 0x4000000 # rear center speakers (7.1)
BASS_SPEAKER_LEFT = 0x10000000 # modifier: left
BASS_SPEAKER_RIGHT = 0x20000000 # modifier: right
BASS_SPEAKER_FRONTLEFT = BASS_SPEAKER_FRONT | BASS_SPEAKER_LEFT
BASS_SPEAKER_FRONTRIGHT = BASS_SPEAKER_FRONT | BASS_SPEAKER_RIGHT
BASS_SPEAKER_REARLEFT = BASS_SPEAKER_REAR | BASS_SPEAKER_LEFT
BASS_SPEAKER_REARRIGHT = BASS_SPEAKER_REAR | BASS_SPEAKER_RIGHT
BASS_SPEAKER_CENTER = BASS_SPEAKER_CENLFE | BASS_SPEAKER_LEFT
BASS_SPEAKER_LFE = BASS_SPEAKER_CENLFE | BASS_SPEAKER_RIGHT
BASS_SPEAKER_REAR2LEFT = BASS_SPEAKER_REAR2 | BASS_SPEAKER_LEFT
BASS_SPEAKER_REAR2RIGHT = BASS_SPEAKER_REAR2 | BASS_SPEAKER_RIGHT

BASS_UNICODE = 0x80000000

BASS_RECORD_PAUSE = 32768 # start recording paused

#***********************************************
#* BASS_ChannelGetTags types : what#s returned *
#***********************************************
BASS_TAG_ID3 = 0   #ID3v1 tags : 128 byte block
BASS_TAG_ID3V2 = 1 #ID3v2 tags : variable length block
BASS_TAG_OGG = 2   #OGG comments : array of null-terminated UTF-8 strings
BASS_TAG_HTTP = 3  #HTTP headers : array of null-terminated ANSI strings
BASS_TAG_ICY = 4   #ICY headers : array of null-terminated ANSI strings
BASS_TAG_META = 5  #ICY metadata : ANSI string
BASS_TAG_VENDOR = 9 # OGG encoder : UTF-8 string
BASS_TAG_RIFF_INFO = 0x100 #RIFF/WAVE tags : array of null-terminated ANSI strings
BASS_TAG_MUSIC_NAME = 0x10000    #MOD music name : ANSI string
BASS_TAG_MUSIC_MESSAGE	= 0x10001 #MOD message : ANSI string
BASS_TAG_MUSIC_INST = 0x10100    #+ instrument #, MOD instrument name : ANSI string
BASS_TAG_MUSIC_SAMPLE = 0x10300  #+ sample #, MOD sample name : ANSI string

#********************
#* 3D channel modes *
#********************
BASS_3DMODE_NORMAL = 0
# normal 3D processing
BASS_3DMODE_RELATIVE = 1
# The channel#s 3D position (position/velocity/orientation) are relative to
# the listener. When the listener#s position/velocity/orientation is changed
# with BASS_Set3DPosition, the channel#s position relative to the listener does
# not change.
BASS_3DMODE_OFF = 2
# Turn off 3D processing on the channel, the sound will be played
# in the center.

#****************************************************
#* EAX environments, use with BASS_SetEAXParameters *
#****************************************************
EAX_ENVIRONMENT_GENERIC = 0
EAX_ENVIRONMENT_PADDEDCELL = 1
EAX_ENVIRONMENT_ROOM = 2
EAX_ENVIRONMENT_BATHROOM = 3
EAX_ENVIRONMENT_LIVINGROOM = 4
EAX_ENVIRONMENT_STONEROOM = 5
EAX_ENVIRONMENT_AUDITORIUM = 6
EAX_ENVIRONMENT_CONCERTHALL = 7
EAX_ENVIRONMENT_CAVE = 8
EAX_ENVIRONMENT_ARENA = 9
EAX_ENVIRONMENT_HANGAR = 10
EAX_ENVIRONMENT_CARPETEDHALLWAY = 11
EAX_ENVIRONMENT_HALLWAY = 12
EAX_ENVIRONMENT_STONECORRIDOR = 13
EAX_ENVIRONMENT_ALLEY = 14
EAX_ENVIRONMENT_FOREST = 15
EAX_ENVIRONMENT_CITY = 16
EAX_ENVIRONMENT_MOUNTAINS = 17
EAX_ENVIRONMENT_QUARRY = 18
EAX_ENVIRONMENT_PLAIN = 19
EAX_ENVIRONMENT_PARKINGLOT = 20
EAX_ENVIRONMENT_SEWERPIPE = 21
EAX_ENVIRONMENT_UNDERWATER = 22
EAX_ENVIRONMENT_DRUGGED = 23
EAX_ENVIRONMENT_DIZZY = 24
EAX_ENVIRONMENT_PSYCHOTIC = 25
# total number of environments
EAX_ENVIRONMENT_COUNT = 26

#**********************************************************************
#* Sync types (with BASS_ChannelSetSync() "param" and SYNCPROC "data" *
#* definitions) & flags.                                              *
#**********************************************************************
BASS_SYNC_POS = 0
# Sync when a channel reaches a position.
# param: position in bytes
# data : not used
BASS_SYNC_END = 2
# Sync when a channel reaches the end.
# param: not used
# data : not used
BASS_SYNC_META = 4
# Sync when metadata is received in a stream.
# param: not used
# data : pointer to the metadata
BASS_SYNC_SLIDE = 5
# Sync when an attribute slide is completed.
# param: not used
# data : the type of slide completed (one of the BASS_SLIDE_xxx values)
BASS_SYNC_STALL = 6
# Sync when playback has stalled.
# param: not used
# data : 0=stalled, 1=resumed
BASS_SYNC_DOWNLOAD = 7
# Sync when downloading of an internet (or "buffered" user file) stream has ended.
# param: not used
# data : not used
BASS_SYNC_FREE = 8
# Sync when a channel is freed.
# param: not used
# data : not used
BASS_SYNC_MUSICPOS = 10
# Sync when a MOD music reaches an order:row position.
# param: LOWORD=order (0=first, -1=all) HIWORD=row (0=first, -1=all)
# data : LOWORD=order HIWORD=row
BASS_SYNC_MUSICINST = 1
# Sync when an instrument (sample for the non-instrument based formats)
# is played in a MOD music (not including retrigs).
# param: LOWORD=instrument (1=first) HIWORD=note (0=c0...119=b9, -1=all)
# data : LOWORD=note HIWORD=volume (0-64)
BASS_SYNC_MUSICFX = 3
# Sync when the "sync" effect (XM/MTM/MOD: E8x/Wxx, IT/S3M: S2x) is used.
# param: 0:data=pos, 1:data="x" value
# data : param=0: LOWORD=order HIWORD=row, param=1: "x" value
BASS_SYNC_MESSAGE = 0x20000000 # FLAG: post a Windows message (instead of callback)
# When using a window message "callback", the message to post is given in the "proc"
# parameter of BASS_ChannelSetSync, and is posted to the window specified in the BASS_Init
# call. The message parameters are: WPARAM = data, LPARAM = user.
BASS_SYNC_MIXTIME = 0x40000000 # FLAG: sync at mixtime, else at playtime
BASS_SYNC_ONETIME = 0x80000000 # FLAG: sync only once, else continuously

# BASS_ChannelIsActive return values
BASS_ACTIVE_STOPPED = 0
BASS_ACTIVE_PLAYING = 1
BASS_ACTIVE_STALLED = 2
BASS_ACTIVE_PAUSED = 3

# BASS_ChannelIsSliding return flags
BASS_SLIDE_FREQ = 1
BASS_SLIDE_VOL = 2
BASS_SLIDE_PAN = 4

# BASS_ChannelGetData flags
BASS_DATA_AVAILABLE = 0         # query how much data is buffered
BASS_DATA_FLOAT = 0x40000000    # flag: return floating-point sample data
BASS_DATA_FFT512 = 0x80000000   # 512 sample FFT
BASS_DATA_FFT1024 = 0x80000001  # 1024 FFT
BASS_DATA_FFT2048 = 0x80000002  # 2048 FFT
BASS_DATA_FFT4096 = 0x80000003  # 4096 FFT
BASS_DATA_FFT_INDIVIDUAL = 0x10 # FFT flag: FFT for each channel, else all combined
BASS_DATA_FFT_NOWINDOW = 0x20   # FFT flag: no Hanning window

# BASS_RecordSetInput flags
BASS_INPUT_OFF = 0x10000
BASS_INPUT_ON = 0x20000
BASS_INPUT_LEVEL = 0x40000

BASS_INPUT_TYPE_MASK = 0xFF000000
BASS_INPUT_TYPE_UNDEF = 0x0
BASS_INPUT_TYPE_DIGITAL = 0x1000000
BASS_INPUT_TYPE_LINE = 0x2000000
BASS_INPUT_TYPE_MIC = 0x3000000
BASS_INPUT_TYPE_SYNTH = 0x4000000
BASS_INPUT_TYPE_CD = 0x5000000
BASS_INPUT_TYPE_PHONE = 0x6000000
BASS_INPUT_TYPE_SPEAKER = 0x7000000
BASS_INPUT_TYPE_WAVE = 0x8000000
BASS_INPUT_TYPE_AUX = 0x9000000
BASS_INPUT_TYPE_ANALOG = 0xA000000

# BASS_MusicSet/GetAttribute options
BASS_MUSIC_ATTRIB_AMPLIFY = 0
BASS_MUSIC_ATTRIB_PANSEP = 1
BASS_MUSIC_ATTRIB_PSCALER = 2
BASS_MUSIC_ATTRIB_BPM = 3
BASS_MUSIC_ATTRIB_SPEED = 4
BASS_MUSIC_ATTRIB_VOL_GLOBAL = 5
BASS_MUSIC_ATTRIB_VOL_CHAN = 0x100 # + channel #
BASS_MUSIC_ATTRIB_VOL_INST = 0x200 # + instrument #

# BASS_Set/GetConfig options
BASS_CONFIG_BUFFER = 0
BASS_CONFIG_UPDATEPERIOD = 1
BASS_CONFIG_MAXVOL = 3
BASS_CONFIG_GVOL_SAMPLE = 4
BASS_CONFIG_GVOL_STREAM = 5
BASS_CONFIG_GVOL_MUSIC = 6
BASS_CONFIG_CURVE_VOL = 7
BASS_CONFIG_CURVE_PAN = 8
BASS_CONFIG_FLOATDSP = 9
BASS_CONFIG_3DALGORITHM = 10
BASS_CONFIG_NET_TIMEOUT = 11
BASS_CONFIG_NET_BUFFER = 12
BASS_CONFIG_PAUSE_NOPLAY = 13
BASS_CONFIG_NET_PREBUF = 15
BASS_CONFIG_NET_AGENT = 16
BASS_CONFIG_NET_PROXY = 17
BASS_CONFIG_NET_PASSIVE = 18
BASS_CONFIG_MP3_CODEC = 19

# BASS_StreamGetFilePosition modes
BASS_FILEPOS_CURRENT = 0
BASS_FILEPOS_DECODE = BASS_FILEPOS_CURRENT
BASS_FILEPOS_DOWNLOAD = 1
BASS_FILEPOS_END = 2
BASS_FILEPOS_START = 3

# STREAMFILEPROC actions
BASS_FILE_CLOSE = 0
BASS_FILE_READ = 1
BASS_FILE_LEN = 3
BASS_FILE_SEEK = 4

BASS_STREAMPROC_END = 0x80000000 # end of user stream flag

#**************************************************************
#* DirectSound interfaces (for use with BASS_GetDSoundObject) *
#**************************************************************
BASS_OBJECT_DS = 1                     # DirectSound
BASS_OBJECT_DS3DL = 2                  #IDirectSound3DListener

#******************************
#* DX7 voice allocation flags *
#******************************
# Play the sample in hardware. If no hardware voices are available then
# the "play" call will fail
BASS_VAM_HARDWARE = 1
# Play the sample in software (ie. non-accelerated). No other VAM flags
#may be used together with this flag.
BASS_VAM_SOFTWARE = 2

#******************************
#* DX7 voice management flags *
#******************************
# These flags enable hardware resource stealing... if the hardware has no
# available voices, a currently playing buffer will be stopped to make room for
# the new buffer. NOTE: only samples loaded/created with the BASS_SAMPLE_VAM
# flag are considered for termination by the DX7 voice management.

# If there are no free hardware voices, the buffer to be terminated will be
# the one with the least time left to play.
BASS_VAM_TERM_TIME = 4
# If there are no free hardware voices, the buffer to be terminated will be
# one that was loaded/created with the BASS_SAMPLE_MUTEMAX flag and is beyond
# it #s max distance. If there are no buffers that match this criteria, then the
# "play" call will fail.
BASS_VAM_TERM_DIST = 8
# If there are no free hardware voices, the buffer to be terminated will be
# the one with the lowest priority.
BASS_VAM_TERM_PRIO = 16

#**********************************************************************
#* software 3D mixing algorithm modes (used with BASS_Set3DAlgorithm) *
#**********************************************************************
# default algorithm (currently translates to BASS_3DALG_OFF)
BASS_3DALG_DEFAULT = 0
# Uses normal left and right panning. The vertical axis is ignored except for
#scaling of volume due to distance. Doppler shift and volume scaling are still
#applied, but the 3D filtering is not performed. This is the most CPU efficient
#software implementation, but provides no virtual 3D audio effect. Head Related
#Transfer Function processing will not be done. Since only normal stereo panning
#is used, a channel using this algorithm may be accelerated by a 2D hardware
#voice if no free 3D hardware voices are available.
BASS_3DALG_OFF = 1
# This algorithm gives the highest quality 3D audio effect, but uses more CPU.
# Requires Windows 98 2nd Edition or Windows 2000 that uses WDM drivers, if this
# mode is not available then BASS_3DALG_OFF will be used instead.
BASS_3DALG_FULL = 2
# This algorithm gives a good 3D audio effect, and uses less CPU than the FULL
# mode. Requires Windows 98 2nd Edition or Windows 2000 that uses WDM drivers, if
# this mode is not available then BASS_3DALG_OFF will be used instead.
BASS_3DALG_LIGHT = 3



class BASS_INFO(Structure):
    _fields_ = [("flags", c_long),         # device capabilities (DSCAPS_xxx flags)
                ("hwsize", c_long),        # size of total device hardware memory
                ("hwfree", c_long),        # size of free device hardware memory
                ("freesam", c_long),       # number of free sample slots in the hardware
                ("free3d", c_long),        # number of free 3D sample slots in the hardware
                ("minrate", c_long),       # min sample rate supported by the hardware
                ("maxrate", c_long),       # max sample rate supported by the hardware
                ("eax", c_long),           # device supports EAX? (always BASSFALSE if BASS_DEVICE_3D was not used)
                ("minbuf", c_long),        # recommended minimum buffer length in ms (requires BASS_DEVICE_LATENCY)
                ("dsver", c_long),         # DirectSound version
                ("latency", c_long),       # delay (in ms) before start of playback (requires BASS_DEVICE_LATENCY)
                ("initflags", c_long),     # "flags" parameter of BASS_Init call
                ("speakers", c_long),      # number of speakers available
                ("driver", c_long),        # driver
                ("freq", c_long)]          # current output rate (OSX only)

class BASS_RECORDINFO(Structure):
    _fields_ = [("flags", c_long),         # device capabilities (DSCCAPS_xxx flags)
                ("formats", c_long),       # supported standard formats (WAVE_FORMAT_xxx flags)
                ("inputs", c_long),        # number of inputs
                ("singlein", c_long),      # BASSTRUE = only 1 input can be set at a time
                ("driver", c_long),        # driver
                ("freq", c_long)]          # current input rate (OSX only)

class BASS_SAMPLE(Structure):
    _fields_ = [("freq", c_long),          # default playback rate
                ("volume", c_long),        # default volume (0-100)
                ("pan", c_long),           # default pan (-100=left, 0=middle, 100=right)
                ("flags", c_long),         # BASS_SAMPLE_xxx flags
                ("length", c_long),        # length (in samples, not bytes)
                ("max", c_long),           # maximum simultaneous playbacks
                ("origres", c_long),       # original resolution
                ("chans", c_long),         # number of channels
                ("mingap", c_long),        # minimum gap (ms) between creating channels
    # The following are the sample#s default 3D attributes (if the sample
    # is 3D, BASS_SAMPLE_3D is in flags) see BASS_ChannelSet3DAttributes
                ("mode3d", c_long),        # BASS_3DMODE_xxx mode
                ("mindist", c_float),       # minimum distance
                ("maxdist", c_float),       # maximum distance
                ("iangle", c_long),        # angle of inside projection cone
                ("oangle", c_long),        # angle of outside projection cone
                ("outvol", c_long),        # delta-volume outside the projection cone
    # The following are the defaults used if the sample uses the DirectX 7
    # voice allocation/management features.
                ("vam", c_long),           # voice allocation/management flags (BASS_VAM_xxx)
                ("priority", c_long)]      # priority (0=lowest, 0xffffffff=highest)

class BASS_CHANNELINFO(Structure):
    _fields_ = [("freq", c_long),          # default playback rate
                ("chans", c_long),         # channels
                ("flags", c_long),         # BASS_SAMPLE/STREAM/MUSIC/SPEAKER flags
                ("ctype", c_long),         # type of channel
                ("origres", c_long),       # original resolution
                ("plugin", c_long)]        # plugin

# BASS_CHANNELINFO types
BASS_CTYPE_SAMPLE = 1
BASS_CTYPE_RECORD = 2
BASS_CTYPE_STREAM = 0x10000
BASS_CTYPE_STREAM_OGG = 0x10002
BASS_CTYPE_STREAM_MP1 = 0x10003
BASS_CTYPE_STREAM_MP2 = 0x10004
BASS_CTYPE_STREAM_MP3 = 0x10005
BASS_CTYPE_STREAM_AIFF = 0x10006
BASS_CTYPE_STREAM_WAV = 0x40000 # WAVE flag, LOWORD=codec
BASS_CTYPE_STREAM_WAV_PCM = 0x50001
BASS_CTYPE_STREAM_WAV_FLOAT = 0x50003
BASS_CTYPE_MUSIC_MOD = 0x20000
BASS_CTYPE_MUSIC_MTM = 0x20001
BASS_CTYPE_MUSIC_S3M = 0x20002
BASS_CTYPE_MUSIC_XM = 0x20003
BASS_CTYPE_MUSIC_IT = 0x20004
BASS_CTYPE_MUSIC_MO3 = 0x100    # MO3 flag


class BASS_PLUGINFORM(Structure):
    _fields_ = [("ctype", c_long),         # channel type
                ("name", c_long),          # format description
                ("exts", c_long)]          # file extension filter (*.ext1;*.ext2;etc...)

class BASS_PLUGININFO(Structure):
    _fields_ = [("version", c_long),       # version (same form as BASS_GetVersion)
                ("formatc", c_long),       # number of formats
                ("formats", c_long * 1)]  #TODO:dynamic array     # the array of formats

#********************************************************
#* 3D vector (for 3D positions/velocities/orientations) *
#********************************************************
class BASS_3DVECTOR(Structure):
    _fields_ = [("x", c_float),           # +=right, -=left
                ("y", c_float),           # +=up, -=down
                ("z", c_float)]           # +=front, -=behind

# DX8 effect types, use with BASS_ChannelSetFX
BASS_FX_CHORUS = 0         # GUID_DSFX_STANDARD_CHORUS
BASS_FX_COMPRESSOR = 1     # GUID_DSFX_STANDARD_COMPRESSOR
BASS_FX_DISTORTION = 2     # GUID_DSFX_STANDARD_DISTORTION
BASS_FX_ECHO = 3           # GUID_DSFX_STANDARD_ECHO
BASS_FX_FLANGER = 4        # GUID_DSFX_STANDARD_FLANGER
BASS_FX_GARGLE = 5         # GUID_DSFX_STANDARD_GARGLE
BASS_FX_I3DL2REVERB = 6    # GUID_DSFX_STANDARD_I3DL2REVERB
BASS_FX_PARAMEQ = 7        # GUID_DSFX_STANDARD_PARAMEQ
BASS_FX_REVERB = 8         # GUID_DSFX_WAVES_REVERB

"""
Type BASS_FXCHORUS              # DSFXChorus
    fWetDryMix As Single
    fDepth As Single
    fFeedback As Single
    fFrequency As Single
    lWaveform As Long   # 0=triangle, 1=sine
    fDelay As Single
    lPhase As Long              # BASS_FX_PHASE_xxx
End Type

Type BASS_FXCOMPRESSOR  # DSFXCompressor
    fGain As Single
    fAttack As Single
    fRelease As Single
    fThreshold As Single
    fRatio As Single
    fPredelay As Single
End Type

Type BASS_FXDISTORTION  # DSFXDistortion
    fGain As Single
    fEdge As Single
    fPostEQCenterFrequency As Single
    fPostEQBandwidth As Single
    fPreLowpassCutoff As Single
End Type

Type BASS_FXECHO                # DSFXEcho
    fWetDryMix As Single
    fFeedback As Single
    fLeftDelay As Single
    fRightDelay As Single
    lPanDelay As Long
End Type

Type BASS_FXFLANGER             # DSFXFlanger
    fWetDryMix As Single
    fDepth As Single
    fFeedback As Single
    fFrequency As Single
    lWaveform As Long   # 0=triangle, 1=sine
    fDelay As Single
    lPhase As Long              # BASS_FX_PHASE_xxx
End Type

Type BASS_FXGARGLE              # DSFXGargle
    dwRateHz As Long               # Rate of modulation in hz
    dwWaveShape As Long            # 0=triangle, 1=square
End Type

Type BASS_FXI3DL2REVERB # DSFXI3DL2Reverb
    lRoom As Long                    # [-10000, 0]      default: -1000 mB
    lRoomHF As Long                  # [-10000, 0]      default: 0 mB
    flRoomRolloffFactor As Single    # [0.0, 10.0]      default: 0.0
    flDecayTime As Single            # [0.1, 20.0]      default: 1.49s
    flDecayHFRatio As Single         # [0.1, 2.0]       default: 0.83
    lReflections As Long             # [-10000, 1000]   default: -2602 mB
    flReflectionsDelay As Single     # [0.0, 0.3]       default: 0.007 s
    lReverb As Long                  # [-10000, 2000]   default: 200 mB
    flReverbDelay As Single          # [0.0, 0.1]       default: 0.011 s
    flDiffusion As Single            # [0.0, 100.0]     default: 100.0 %
    flDensity As Single              # [0.0, 100.0]     default: 100.0 %
    flHFReference As Single          # [20.0, 20000.0]  default: 5000.0 Hz
End Type

Type BASS_FXPARAMEQ             # DSFXParamEq
    fCenter As Single
    fBandwidth As Single
    fGain As Single
End Type

Type BASS_FXREVERB              # DSFXWavesReverb
    fInGain As Single                # [-96.0,0.0]            default: 0.0 dB
    fReverbMix As Single             # [-96.0,0.0]            default: 0.0 db
    fReverbTime As Single            # [0.001,3000.0]         default: 1000.0 ms
    fHighFreqRTRatio As Single       # [0.001,0.999]          default: 0.001
End Type
"""

BASS_FX_PHASE_NEG_180 = 0
BASS_FX_PHASE_NEG_90 = 1
BASS_FX_PHASE_ZERO = 2
BASS_FX_PHASE_90 = 3
BASS_FX_PHASE_180 = 4

"""
Type GUID       # used with BASS_Init - use VarPtr(guid) in clsid parameter
    Data1 As Long
    Data2 As Integer
    Data3 As Integer
    Data4(7) As Byte
End Type
"""

#*******************
# callback functions
#*******************
#Function STREAMPROC(ByVal handle As Long, ByVal buffer As Long, ByVal length As Long, ByVal user As Long) As Long
STREAMPROC = CFUNCTYPE(c_long, c_long, c_void_p, c_long, c_long)
    
    #CALLBACK FUNCTION !!!
    
    # User stream callback function
    # NOTE: A stream function should obviously be as quick
    # as possible, other streams (and MOD musics) can#t be mixed until it#s finished.
    # handle : The stream that needs writing
    # buffer : Buffer to write the samples in
    # length : Number of bytes to write
    # user   : The #user# parameter value given when calling BASS_StreamCreate
    # RETURN : Number of bytes written. Set the BASS_STREAMPROC_END flag to end
    #          the stream.
    

#Function STREAMFILEPROC(ByVal action As Long, ByVal param1 As Long, ByVal param2 As Long, ByVal user As Long) As Long
STREAMFILEPROC = CFUNCTYPE(c_long, c_long, c_long, c_long, c_long)
    
    #CALLBACK FUNCTION !!!
    
    # User file stream callback function.
    # action : The action to perform, one of BASS_FILE_xxx values.
    # param1 : Depends on "action"
    # param2 : Depends on "action"
    # user   : The #user# parameter value given when calling BASS_StreamCreate
    # RETURN : Depends on "action"
    

#Sub DOWNLOADPROC(ByVal buffer As Long, ByVal length As Long, ByVal user As Long)
DOWNLOADPROC = CFUNCTYPE(c_void_p, c_long, c_long, c_long)
    
    #CALLBACK FUNCTION !!!

    # Internet stream download callback function.
    # buffer : Buffer containing the downloaded data... NULL=end of download
    # length : Number of bytes in the buffer
    # user   : The #user# parameter given when calling BASS_StreamCreateURL
    

#Sub SYNCPROC(ByVal handle As Long, ByVal channel As Long, ByVal data As Long, ByVal user As Long)
SYNCPROC = CFUNCTYPE(c_void_p, c_long, c_long, c_long, c_long)
    
    #CALLBACK FUNCTION !!!
    
    #Similarly in here, write what to do when sync function
    #is called, i.e screen flash etc.
    
    # NOTE: a sync callback function should be very quick as other
    # syncs cannot be processed until it has finished.
    # handle : The sync that has occured
    # channel: Channel that the sync occured in
    # data   : Additional data associated with the sync#s occurance
    # user   : The #user# parameter given when calling BASS_ChannelSetSync */
    

#Sub DSPPROC(ByVal handle As Long, ByVal channel As Long, ByVal buffer As Long, ByVal length As Long, ByVal user As Long)
DSPPROC = CFUNCTYPE(c_void_p, c_long, c_long, c_long, c_long, c_long)

    #CALLBACK FUNCTION !!!

    # VB doesn#t support pointers, so you should copy the buffer into an array,
    # process it, and then copy it back into the buffer.

    # DSP callback function. NOTE: A DSP function should obviously be as quick as
    # possible... other DSP functions, streams and MOD musics can not be processed
    # until it#s finished.
    # handle : The DSP handle
    # channel: Channel that the DSP is being applied to
    # buffer : Buffer to apply the DSP to
    # length : Number of bytes in the buffer
    # user   : The #user# parameter given when calling BASS_ChannelSetDSP
    

#Function RECORDPROC(ByVal handle As Long, ByVal buffer As Long, ByVal length As Long, ByVal user As Long) As Long
RECORDPROC = CFUNCTYPE(c_long, c_long, c_long, c_long, c_long)

    #CALLBACK FUNCTION !!!

    # Recording callback function.
    # handle : The recording handle
    # buffer : Buffer containing the recorded samples
    # length : Number of bytes
    # user   : The #user# parameter value given when calling BASS_RecordStart
    # RETURN : BASSTRUE = continue recording, BASSFALSE = stop





# DECLARE FUNCTIONS

BASS.BASS_Init.argtypes = [c_long, c_long, c_long, c_long, c_long]
BASS.BASS_MusicLoad.argtypes = [c_byte, c_char_p, c_long, c_long, c_long, c_long]
BASS.BASS_SetVolume.argtypes = [c_long]
BASS.BASS_ChannelPlay.argtypes = [c_long, c_byte]

BASS.BASS_SetConfig.argtypes = [c_long, c_long]
BASS.BASS_GetConfig.argtypes = [c_long]
BASS.BASS_GetVersion.argtypes = []
BASS.BASS_GetDeviceDescription.argtypes = [c_long]
BASS.BASS_ErrorGetCode.argtypes = []
BASS.BASS_Init.argtypes = [c_long, c_long, c_long, c_long, c_long]
BASS.BASS_SetDevice.argtypes = [c_long]
BASS.BASS_GetDevice.argtypes = []
BASS.BASS_Free.argtypes = []
BASS.BASS_GetDSoundObject.argtypes = [c_long]
#BASS.BASS_GetInfo.argtypes = (ByRef info As BASS_INFO) As Long
BASS.BASS_Update.argtypes = []
BASS.BASS_GetCPU.argtypes = []; BASS.BASS_GetCPU.restype = c_float
BASS.BASS_Start.argtypes = []
BASS.BASS_Stop.argtypes = []
BASS.BASS_Pause.argtypes = []
BASS.BASS_SetVolume.argtypes = [c_long]
BASS.BASS_GetVolume.argtypes = []

BASS.BASS_PluginLoad.argtypes = [c_char_p, c_long]
BASS.BASS_PluginFree.argtypes = [c_long]
#Private BASS.BASS_PluginGetInfo_.argtypes = Alias "BASS_PluginGetInfo" (ByVal handle As Long) As Long

BASS.BASS_Set3DFactors.argtypes = [c_float, c_float, c_float]
BASS.BASS_Get3DFactors.argtypes = [c_float, c_float, c_float] 
BASS.BASS_Set3DPosition.argtypes = [c_float, c_char_p, c_char_p, c_char_p] # Any, Any, Any, Any
BASS.BASS_Get3DPosition.argtypes = [c_float, c_char_p, c_char_p, c_char_p] # Any, Any, Any, Any
BASS.BASS_Apply3D.argtypes = []
BASS.BASS_SetEAXParameters.argtypes = [c_long, c_float, c_float, c_float]
BASS.BASS_GetEAXParameters.argtypes = [c_long, c_float, c_float, c_float]

BASS.BASS_MusicLoad.argtypes = [c_long, c_char_p, c_long, c_long, c_long, c_long]
BASS.BASS_MusicFree.argtypes = [c_long]
BASS.BASS_MusicSetAttribute.argtypes = [c_long, c_long, c_long]
BASS.BASS_MusicGetAttribute.argtypes = [c_long, c_long]
BASS.BASS_MusicGetOrders.argtypes = [c_long, c_long]
BASS.BASS_MusicGetOrderPosition.argtypes = [c_long, c_long]

BASS.BASS_SampleLoad.argtypes = [c_long, c_char_p, c_long, c_long, c_long, c_long]
BASS.BASS_SampleCreate.argtypes = [c_long, c_long, c_long, c_long, c_long]
BASS.BASS_SampleCreateDone.argtypes = []
BASS.BASS_SampleFree.argtypes = [c_long]
BASS.BASS_SampleGetInfo.argtypes = [c_long, BASS_SAMPLE]
BASS.BASS_SampleSetInfo.argtypes = [c_long, BASS_SAMPLE]
BASS.BASS_SampleGetChannel.argtypes = [c_long, c_long]
BASS.BASS_SampleStop.argtypes = [c_long]

BASS.BASS_StreamCreate.argtypes = [c_long, c_long, c_long, STREAMPROC, c_long]
#BASS.BASS_StreamCreate.argtypes = [c_long, c_long, c_long, CFUNCTYPE, c_long]
BASS.BASS_StreamCreateFile.argtypes = [c_long, c_char_p, c_long, c_long, c_long]
BASS.BASS_StreamCreateURL.argtypes = [c_char_p, c_long, c_long, c_long, c_long]
BASS.BASS_StreamCreateFileUser.argtypes = [c_long, c_long, c_long, c_long]
BASS.BASS_StreamFree.argtypes = [c_long]
BASS.BASS_StreamGetFilePosition.argtypes = [c_long, c_long]

BASS.BASS_RecordGetDeviceDescription.argtypes = [c_long]
BASS.BASS_RecordInit.argtypes = [c_long]
BASS.BASS_RecordSetDevice.argtypes = [c_long]
BASS.BASS_RecordGetDevice.argtypes = []
BASS.BASS_RecordFree.argtypes = []
BASS.BASS_RecordGetInfo.argtypes = [BASS_RECORDINFO]
BASS.BASS_RecordGetInputName.argtypes = [c_long]
BASS.BASS_RecordSetInput.argtypes = [c_long, c_long]
BASS.BASS_RecordGetInput.argtypes = [c_long]
BASS.BASS_RecordStart.argtypes = [c_long, c_long, c_long, c_long, c_long]

#Private BASS.BASS_ChannelBytes2Seconds64.argtypes = Alias "BASS_ChannelBytes2Seconds" (ByVal handle As Long, ByVal pos As Long, ByVal poshigh As Long) As Single
BASS.BASS_ChannelSeconds2Bytes.argtypes = [c_long, c_float]
BASS.BASS_ChannelGetDevice.argtypes = [c_long]
BASS.BASS_ChannelSetDevice.argtypes = [c_long, c_long]
BASS.BASS_ChannelIsActive.argtypes = [c_long]
BASS.BASS_ChannelGetInfo.argtypes = [c_long, BASS_CHANNELINFO]
BASS.BASS_ChannelGetTags.argtypes = [c_long, c_long]
BASS.BASS_ChannelSetFlags.argtypes = [c_long, c_long]
BASS.BASS_ChannelPreBuf.argtypes = [c_long, c_long]
BASS.BASS_ChannelPlay.argtypes = [c_long, c_long]
BASS.BASS_ChannelStop.argtypes = [c_long]
BASS.BASS_ChannelPause.argtypes = [c_long]
BASS.BASS_ChannelSetAttributes.argtypes = [c_long, c_long, c_long, c_long]
BASS.BASS_ChannelGetAttributes.argtypes = [c_long, c_long, c_long, c_long]
BASS.BASS_ChannelSlideAttributes.argtypes = [c_long, c_long, c_long, c_long, c_long]
BASS.BASS_ChannelIsSliding.argtypes = [c_long]
BASS.BASS_ChannelSet3DAttributes.argtypes = [c_long, c_long, c_float, c_float, c_long, c_long, c_long]
BASS.BASS_ChannelGet3DAttributes.argtypes = [c_long, c_long, c_float, c_float, c_long, c_long, c_long]
BASS.BASS_ChannelSet3DPosition.argtypes = [c_long, c_char_p, c_char_p, c_char_p]
BASS.BASS_ChannelGet3DPosition.argtypes = [c_long, c_char_p, c_char_p, c_char_p]
BASS.BASS_ChannelGetLength.argtypes = [c_long]
#Private BASS.BASS_ChannelSetPosition64.argtypes = Alias "BASS_ChannelSetPosition" (ByVal handle As Long, ByVal pos As Long, ByVal poshigh As Long) As Long
BASS.BASS_ChannelGetPosition.argtypes = [c_long]
BASS.BASS_ChannelGetLevel.argtypes = [c_long]
BASS.BASS_ChannelGetData.argtypes = [c_long, c_char_p, c_long]
#Private BASS.BASS_ChannelSetSync64.argtypes = Alias "BASS_ChannelSetSync" (ByVal handle As Long, ByVal atype As Long, ByVal param As Long, ByVal paramhigh As Long, ByVal proc As Long, ByVal user As Long) As Long
BASS.BASS_ChannelRemoveSync.argtypes = [c_long, c_long]
BASS.BASS_ChannelSetDSP.argtypes = [c_long, c_long, c_long, c_long]
BASS.BASS_ChannelRemoveDSP.argtypes = [c_long, c_long]
BASS.BASS_ChannelSetEAXMix.argtypes = [c_long, c_float]
BASS.BASS_ChannelGetEAXMix.argtypes = [c_long, c_float]
BASS.BASS_ChannelSetLink.argtypes = [c_long, c_long]
BASS.BASS_ChannelRemoveLink.argtypes = [c_long, c_long]
BASS.BASS_ChannelSetFX.argtypes = [c_long, c_long, c_long]
BASS.BASS_ChannelRemoveFX.argtypes = [c_long, c_long]
BASS.BASS_FXSetParameters.argtypes = [c_long, c_char_p]
BASS.BASS_FXGetParameters.argtypes = [c_long, c_char_p]


"""DECLARE FUNCTIONS

BASS.BASS_PluginLoad.argtypes = (ByVal filename As String, ByVal flags As Long) As Long
BASS.BASS_PluginFree.argtypes = (ByVal handle As Long) As Long
Private BASS.BASS_PluginGetInfo_.argtypes = Alias "BASS_PluginGetInfo" (ByVal handle As Long) As Long

BASS.BASS_Set3DFactors.argtypes = (ByVal distf As Single, ByVal rollf As Single, ByVal doppf As Single) As Long
BASS.BASS_Get3DFactors.argtypes = (ByRef distf As Single, ByRef rollf As Single, ByRef doppf As Single) As Long
BASS.BASS_Set3DPosition.argtypes = (ByRef pos As Any, ByRef vel As Any, ByRef front As Any, ByRef top As Any) As Long
BASS.BASS_Get3DPosition.argtypes = (ByRef pos As Any, ByRef vel As Any, ByRef front As Any, ByRef top As Any) As Long
BASS.BASS_Apply3D.argtypes = () As Long
BASS.BASS_SetEAXParameters.argtypes = (ByVal env As Long, ByVal vol As Single, ByVal decay As Single, ByVal damp As Single) As Long
BASS.BASS_GetEAXParameters.argtypes = (ByRef env As Long, ByRef vol As Single, ByRef decay As Single, ByRef damp As Single) As Long

BASS.BASS_MusicLoad.argtypes = (ByVal mem As Long, ByVal f As Any, ByVal offset As Long, ByVal length As Long, ByVal flags As Long, ByVal freq As Long) As Long
BASS.BASS_MusicFree.argtypes = (ByVal handle As Long) As Long
BASS.BASS_MusicSetAttribute.argtypes = (ByVal handle As Long, ByVal attrib As Long, ByVal value As Long) As Long
BASS.BASS_MusicGetAttribute.argtypes = (ByVal handle As Long, ByVal attrib As Long) As Long
BASS.BASS_MusicGetOrders.argtypes = (ByVal handle As Long) As Long
BASS.BASS_MusicGetOrderPosition.argtypes = (ByVal handle As Long) As Long

BASS.BASS_SampleLoad.argtypes = (ByVal mem As Long, ByVal f As Any, ByVal offset As Long, ByVal length As Long, ByVal max As Long, ByVal flags As Long) As Long
BASS.BASS_SampleCreate.argtypes = (ByVal length As Long, ByVal freq As Long, ByVal chans As Long, ByVal max As Long, ByVal flags As Long) As Long
BASS.BASS_SampleCreateDone.argtypes = () As Long
BASS.BASS_SampleFree.argtypes = (ByVal handle As Long) As Long
BASS.BASS_SampleGetInfo.argtypes = (ByVal handle As Long, ByRef info As BASS_SAMPLE) As Long
BASS.BASS_SampleSetInfo.argtypes = (ByVal handle As Long, ByRef info As BASS_SAMPLE) As Long
BASS.BASS_SampleGetChannel.argtypes = (ByVal handle As Long, ByVal onlynew As Long) As Long
BASS.BASS_SampleStop.argtypes = (ByVal handle As Long) As Long

BASS.BASS_StreamCreate.argtypes = (ByVal freq As Long, ByVal chans As Long, ByVal flags As Long, ByVal proc As Long, ByVal user As Long) As Long
BASS.BASS_StreamCreateFile.argtypes = (ByVal mem As Long, ByVal f As Any, ByVal offset As Long, ByVal length As Long, ByVal flags As Long) As Long
BASS.BASS_StreamCreateURL.argtypes = (ByVal url As String, ByVal offset As Long, ByVal flags As Long, ByVal proc As Long, ByVal user As Long) As Long
BASS.BASS_StreamCreateFileUser.argtypes = (ByVal buffered As Long, ByVal flags As Long, ByVal proc As Long, ByVal user As Long) As Long
BASS.BASS_StreamFree.argtypes = (ByVal handle As Long) As Long
BASS.BASS_StreamGetFilePosition.argtypes = (ByVal handle As Long, ByVal mode As Long) As Long

BASS.BASS_RecordGetDeviceDescription.argtypes = (ByVal device As Long) As Long
BASS.BASS_RecordInit.argtypes = (ByVal device As Long) As Long
BASS.BASS_RecordSetDevice.argtypes = (ByVal device As Long) As Long
BASS.BASS_RecordGetDevice.argtypes = () As Long
BASS.BASS_RecordFree.argtypes = () As Long
BASS.BASS_RecordGetInfo.argtypes = (ByRef info As BASS_RECORDINFO) As Long
BASS.BASS_RecordGetInputName.argtypes = (ByVal inputn As Long) As Long
BASS.BASS_RecordSetInput.argtypes = (ByVal inputn As Long, ByVal setting As Long) As Long
BASS.BASS_RecordGetInput.argtypes = (ByVal inputn As Long) As Long
BASS.BASS_RecordStart.argtypes = (ByVal freq As Long, ByVal chans As Long, ByVal flags As Long, ByVal proc As Long, ByVal user As Long) As Long

Private BASS.BASS_ChannelBytes2Seconds64.argtypes = Alias "BASS_ChannelBytes2Seconds" (ByVal handle As Long, ByVal pos As Long, ByVal poshigh As Long) As Single
BASS.BASS_ChannelSeconds2Bytes.argtypes = (ByVal handle As Long, ByVal pos As Single) As Long
BASS.BASS_ChannelGetDevice.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelSetDevice.argtypes = (ByVal handle As Long, ByVal device As Long) As Long
BASS.BASS_ChannelIsActive.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelGetInfo.argtypes = (ByVal handle As Long, ByRef info As BASS_CHANNELINFO) As Long
BASS.BASS_ChannelGetTags.argtypes = (ByVal handle As Long, ByVal tags As Long) As Long
BASS.BASS_ChannelSetFlags.argtypes = (ByVal handle As Long, ByVal flags As Long) As Long
BASS.BASS_ChannelPreBuf.argtypes = (ByVal handle As Long, ByVal length As Long) As Long
BASS.BASS_ChannelPlay.argtypes = (ByVal handle As Long, ByVal restart As Long) As Long
BASS.BASS_ChannelStop.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelPause.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelSetAttributes.argtypes = (ByVal handle As Long, ByVal freq As Long, ByVal volume As Long, ByVal pan As Long) As Long
BASS.BASS_ChannelGetAttributes.argtypes = (ByVal handle As Long, ByRef freq As Long, ByRef volume As Long, ByRef pan As Long) As Long
BASS.BASS_ChannelSlideAttributes.argtypes = (ByVal handle As Long, ByVal freq As Long, ByVal volume As Long, ByVal pan As Long, ByVal time As Long) As Long
BASS.BASS_ChannelIsSliding.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelSet3DAttributes.argtypes = (ByVal handle As Long, ByVal mode As Long, ByVal min As Single, ByVal max As Single, ByVal iangle As Long, ByVal oangle As Long, ByVal outvol As Long) As Long
BASS.BASS_ChannelGet3DAttributes.argtypes = (ByVal handle As Long, ByRef mode As Long, ByRef min As Single, ByRef max As Single, ByRef iangle As Long, ByRef oangle As Long, ByRef outvol As Long) As Long
BASS.BASS_ChannelSet3DPosition.argtypes = (ByVal handle As Long, ByRef pos As Any, ByRef orient As Any, ByRef vel As Any) As Long
BASS.BASS_ChannelGet3DPosition.argtypes = (ByVal handle As Long, ByRef pos As Any, ByRef orient As Any, ByRef vel As Any) As Long
BASS.BASS_ChannelGetLength.argtypes = (ByVal handle As Long) As Long
Private BASS.BASS_ChannelSetPosition64.argtypes = Alias "BASS_ChannelSetPosition" (ByVal handle As Long, ByVal pos As Long, ByVal poshigh As Long) As Long
BASS.BASS_ChannelGetPosition.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelGetLevel.argtypes = (ByVal handle As Long) As Long
BASS.BASS_ChannelGetData.argtypes = (ByVal handle As Long, ByRef buffer As Any, ByVal length As Long) As Long
Private BASS.BASS_ChannelSetSync64.argtypes = Alias "BASS_ChannelSetSync" (ByVal handle As Long, ByVal atype As Long, ByVal param As Long, ByVal paramhigh As Long, ByVal proc As Long, ByVal user As Long) As Long
BASS.BASS_ChannelRemoveSync.argtypes = (ByVal handle As Long, ByVal sync As Long) As Long
BASS.BASS_ChannelSetDSP.argtypes = (ByVal handle As Long, ByVal proc As Long, ByVal user As Long, ByVal priority As Long) As Long
BASS.BASS_ChannelRemoveDSP.argtypes = (ByVal handle As Long, ByVal dsp As Long) As Long
BASS.BASS_ChannelSetEAXMix.argtypes = (ByVal handle As Long, ByVal mix As Single) As Long
BASS.BASS_ChannelGetEAXMix.argtypes = (ByVal handle As Long, ByRef mix As Single) As Long
Declare Function BASS_ChannelSetLink.argtypes = (ByVal handle As Long, ByVal chan As Long) As Long
Declare Function BASS_ChannelRemoveLink.argtypes = (ByVal handle As Long, ByVal chan As Long) As Long
Declare Function BASS_ChannelSetFX.argtypes = (ByVal handle As Long, ByVal atype As Long, ByVal priority As Long) As Long
Declare Function BASS_ChannelRemoveFX.argtypes = (ByVal handle As Long, ByVal fx As Long) As Long
Declare Function BASS_FXSetParameters.argtypes = (ByVal handle As Long, ByRef par As Any) As Long
Declare Function BASS_FXGetParameters.argtypes = (ByVal handle As Long, ByRef par As Any) As Long

Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (ByRef Destination As Any, ByRef Source As Any, ByVal length As Long)
Private Declare Function lstrlen Lib "kernel32" Alias "lstrlenA" (ByVal lpString As Long) As Long

Public Function BASS_SPEAKER_N(ByVal n As Long) As Long
BASS_SPEAKER_N = n * (2 ^ 24)
End Function

Public Function MAKEMUSICPOS(ByVal order As Long, ByVal row As Long) As Long
MAKEMUSICPOS = 0x80000000 Or MakeLong(order, row)
End Function

#*******************************************
# 32-bit wrappers for 64-bit BASS functions
#*******************************************
Function BASS_ChannelBytes2Seconds(ByVal handle As Long, ByVal pos As Long) As Single
BASS_ChannelBytes2Seconds = BASS_ChannelBytes2Seconds64(handle, pos, 0)
End Function

Function BASS_ChannelSetPosition(ByVal handle As Long, ByVal pos As Long) As Long
BASS_ChannelSetPosition = BASS_ChannelSetPosition64(handle, pos, 0)
End Function

Function BASS_ChannelSetSync(ByVal handle As Long, ByVal atype As Long, ByVal param As Long, ByVal proc As Long, ByVal user As Long) As Long
BASS_ChannelSetSync = BASS_ChannelSetSync64(handle, atype, param, 0, proc, user)
End Function

#****************************
# BASS_PluginGetInfo wrappers
#****************************
Function BASS_PluginGetInfo(ByVal handle As Long) As BASS_PLUGININFO
Dim pinfo As BASS_PLUGININFO, plug As Long
plug = BASS_PluginGetInfo_(handle)
If plug Then
    Call CopyMemory(pinfo, ByVal plug, LenB(pinfo))
End If
BASS_PluginGetInfo = pinfo
End Function

Function BASS_PluginGetInfoFormat(ByVal handle As Long, ByVal index As Long) As BASS_PLUGINFORM
Dim pform As BASS_PLUGINFORM, plug As Long
plug = BASS_PluginGetInfo(handle).formats
If plug Then
    plug = plug + (index * LenB(pform))
    Call CopyMemory(pform, ByVal plug, LenB(pform))
End If
BASS_PluginGetInfoFormat = pform
End Function
"""


"""
Function BASS_GetDeviceDescriptionString(ByVal device As Long) As String
Dim pstring As Long
Dim sstring As String
On Error Resume Next
pstring = BASS_GetDeviceDescription(device)
If pstring Then
    sstring = VBStrFromAnsiPtr(pstring)
End If
BASS_GetDeviceDescriptionString = sstring
End Function

Function BASS_SetEAXPreset(Preset) As Long
# This function is a workaround, because VB doesn#t support multiple comma seperated
# paramaters for each Global Const, simply pass the EAX_ENVIRONMENT_xxx value to this function
# instead of BASS_SetEAXParameters as you would do in C++
Select Case Preset
    Case EAX_ENVIRONMENT_GENERIC
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_GENERIC, 0.5, 1.493, 0.5)
    Case EAX_ENVIRONMENT_PADDEDCELL
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_PADDEDCELL, 0.25, 0.1, 0)
    Case EAX_ENVIRONMENT_ROOM
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_ROOM, 0.417, 0.4, 0.666)
    Case EAX_ENVIRONMENT_BATHROOM
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_BATHROOM, 0.653, 1.499, 0.166)
    Case EAX_ENVIRONMENT_LIVINGROOM
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_LIVINGROOM, 0.208, 0.478, 0)
    Case EAX_ENVIRONMENT_STONEROOM
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_STONEROOM, 0.5, 2.309, 0.888)
    Case EAX_ENVIRONMENT_AUDITORIUM
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_AUDITORIUM, 0.403, 4.279, 0.5)
    Case EAX_ENVIRONMENT_CONCERTHALL
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_CONCERTHALL, 0.5, 3.961, 0.5)
    Case EAX_ENVIRONMENT_CAVE
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_CAVE, 0.5, 2.886, 1.304)
    Case EAX_ENVIRONMENT_ARENA
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_ARENA, 0.361, 7.284, 0.332)
    Case EAX_ENVIRONMENT_HANGAR
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_HANGAR, 0.5, 10, 0.3)
    Case EAX_ENVIRONMENT_CARPETEDHALLWAY
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_CARPETEDHALLWAY, 0.153, 0.259, 2)
    Case EAX_ENVIRONMENT_HALLWAY
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_HALLWAY, 0.361, 1.493, 0)
    Case EAX_ENVIRONMENT_STONECORRIDOR
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_STONECORRIDOR, 0.444, 2.697, 0.638)
    Case EAX_ENVIRONMENT_ALLEY
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_ALLEY, 0.25, 1.752, 0.776)
    Case EAX_ENVIRONMENT_FOREST
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_FOREST, 0.111, 3.145, 0.472)
    Case EAX_ENVIRONMENT_CITY
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_CITY, 0.111, 2.767, 0.224)
    Case EAX_ENVIRONMENT_MOUNTAINS
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_MOUNTAINS, 0.194, 7.841, 0.472)
    Case EAX_ENVIRONMENT_QUARRY
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_QUARRY, 1, 1.499, 0.5)
    Case EAX_ENVIRONMENT_PLAIN
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_PLAIN, 0.097, 2.767, 0.224)
    Case EAX_ENVIRONMENT_PARKINGLOT
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_PARKINGLOT, 0.208, 1.652, 1.5)
    Case EAX_ENVIRONMENT_SEWERPIPE
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_SEWERPIPE, 0.652, 2.886, 0.25)
    Case EAX_ENVIRONMENT_UNDERWATER
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_UNDERWATER, 1, 1.499, 0)
    Case EAX_ENVIRONMENT_DRUGGED
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_DRUGGED, 0.875, 8.392, 1.388)
    Case EAX_ENVIRONMENT_DIZZY
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_DIZZY, 0.139, 17.234, 0.666)
    Case EAX_ENVIRONMENT_PSYCHOTIC
        BASS_SetEAXPreset = BASS_SetEAXParameters(EAX_ENVIRONMENT_PSYCHOTIC, 0.486, 7.563, 0.806)
End Select
End Function

Public Function HiWord(lparam As Long) As Long
# This is the HIWORD of the lParam:
HiWord = lparam \ 0x10000 And 0xFFFF&
End Function
Public Function LoWord(lparam As Long) As Long
# This is the LOWORD of the lParam:
LoWord = lparam And 0xFFFF&
End Function
Function MakeLong(LoWord As Long, HiWord As Long) As Long
#Replacement for the c++ Function MAKELONG
MakeLong = (LoWord And 0xFFFF&) Or (HiWord * 0x10000)
End Function

Public Function VBStrFromAnsiPtr(ByVal lpStr As Long) As String
Dim bStr() As Byte
Dim cChars As Long
On Error Resume Next
# Get the number of characters in the buffer
cChars = lstrlen(lpStr)
# Resize the byte array
ReDim bStr(0 To cChars - 1) As Byte
# Grab the ANSI buffer
Call CopyMemory(bStr(0), ByVal lpStr, cChars)
# Now convert to a VB Unicode string
VBStrFromAnsiPtr = StrConv(bStr, vbUnicode)
End Function
"""


def test():
    fname = r"D:\blueberry\it\inpuj\12x.it"
    import time
    BASS.BASS_Init(1, 44100, 0, 0, 0)
    #BASS.BASS_SetVolume(c_long(25))
    music = BASS.BASS_MusicLoad(0, fname, 0, 0, 0, 0)
    print music
    print "error", BASS.BASS_ErrorGetCode()
    BASS.BASS_ChannelPlay(music, 0)
    while 1:
        time.sleep(1)
        print BASS.BASS_GetCPU()
        #x = raw_input()
    print BASS.BASS_GetVolume()
    BASS.BASS_Free()


