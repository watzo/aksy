
import wavex


def getWaveLengthMS(fname):
    wfile = wavex.open(fname, "rb")
    frames, rate = wfile.getnframes(), wfile.getframerate()
    # get length in ms
    lis = (frames / float(rate)) * 1000
    wfile.close()
    return lis

        

def getEDLTrack(fname, idnum, tracknum, startTime="0.0000", length=None):
    if length == None:
        lis = getWaveLengthMS(fname)
        length = streamLength = "%.4f" % lis
    else:
        length = streamLength = length
    
    id = str(idnum)
    track = str(tracknum)
    startTime = startTime
    #length = "177188.5714"
    playRate = "1.000000"
    locked = "FALSE"
    normalized = "FALSE"
    stretchMethod = "0"
    looped = "TRUE"
    onRuler = "FALSE"
    mediaType = "AUDIO"
    fileName = fname
    stream = "0"
    streamStart = "0.0000"
    #streamLength = "177188.5714"
    fadeTimeIn = "0.0000"
    fadeTimeOut = "0.0000"
    sustainGain = "1.000000"
    curveIn = "2"
    gainIn = "0.000000"
    curveOut = "-2"
    gainOut = "0.000000"
    layer = "0"
    color = "-1"
    curveInR = "-2"
    curveOutR = "2"
    playPitch = "0.000000"
    lockPitch = "FALSE"

    fmt = '%s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    "%s";    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s;    %s\n'
    data = fmt % (id, track, startTime, length, playRate, locked, normalized, stretchMethod, looped, onRuler, mediaType, fileName, stream, streamStart, streamLength, fadeTimeIn, fadeTimeOut, sustainGain, curveIn, gainIn, curveOut, gainOut, layer, color, curveInR, curveOutR, playPitch, lockPitch)
    return data


def getEDLMultiTrack(files, idnum, tracknum):
    curpos = 0.0000
    tracks = []
    for fname in files:
        lis = getWaveLengthMS(fname)
        length = streamLength = "%.4f" % lis
        stime = "%.4f" % curpos
        track = getEDLTrack(fname, idnum, tracknum, startTime=stime, length=length)
        tracks.append(track)
        idnum += 1
        curpos += lis
    return tracks
        
        


def getEDL(filelist, multi=0):
    #1;    0;    0.0000;    177188.5714;    1.000000;    FALSE;    FALSE;    0;    TRUE;    FALSE;    AUDIO;    "C:\it\export\ramjk\ramjk-t1.wav";    0;    0.0000;    177188.5714;    0.0000;    0.0000;    1.000000;    2;    0.000000;    -2;    0.000000;    0;    -1;    -2;    2
    #2;    1;    0.0000;    177188.5714;    1.000000;    FALSE;    FALSE;    0;    TRUE;    FALSE;    AUDIO;    "C:\it\export\ramjk\ramjk-t2.wav";    0;    0.0000;    177188.5714;    0.0000;    0.0000;    1.000000;    2;    0.000000;    -2;    0.000000;    0;    -1;    -2;    2
    #3;    2;    0.0000;    177188.5714;    1.000000;    FALSE;    FALSE;    0;    TRUE;    FALSE;    AUDIO;    "C:\it\export\ramjk\ramjk-t3.wav";    0;    0.0000;    177188.5714;    0.0000;    0.0000;    1.000000;    2;    0.000000;    -2;    0.000000;    0;    -1;    -2;    2
    #4;    3;    0.0000;    177188.5714;    1.000000;    FALSE;    FALSE;    0;    TRUE;    FALSE;    AUDIO;    "C:\it\export\ramjk\ramjk-t4.wav";    0;    0.0000;    177188.5714;    0.0000;    0.0000;    1.000000;    2;    0.000000;    -2;    0.000000;    0;    -1;    -2;    2

    data = ['"ID";"Track";"StartTime";"Length";"PlayRate";"Locked";"Normalized";"StretchMethod";"Looped";"OnRuler";"MediaType";"FileName";"Stream";"StreamStart";"StreamLength";"FadeTimeIn";"FadeTimeOut";"SustainGain";"CurveIn";"GainIn";"CurveOut";"GainOut";"Layer";"Color";"CurveInR";"CurveOutR":"PlayPitch";"LockPitch"\n']

    nid = 0
    ntrack = -1
    if multi:
        data += getEDLMultiTrack(filelist, 1, 0)
    else:
        for f in filelist:
            nid += 1
            ntrack += 1
            data.append(getEDLTrack(f, nid, ntrack))

    return data


def writeEDL(fname, filelist, multi=0):
    f = open(fname, "w")
    data = getEDL(filelist, multi=multi)
    data = ''.join(data)
    f.write(data)
    f.close()
    return data

