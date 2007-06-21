
import audioop, sndhdr, wave, aifc, sunau, os, glob
#import mmap

import audioopx, filex, wavex

#TODO: we need fade in/out loop points.

def getbpmsamples(bpm, numbeats=4, samplerate=44100):
    "return number of samples needed for a file of given bpm, number of beats, and samplerate"
    num = numbeats * (samplerate * 60) / bpm

def getloadertype(filetype):
    "return a loader module based on string returned from sndhdr.what"
    if filetype == "wav":
        loader = wave
    elif filetype == "aifc" or filetype == "aiff":
        loader = aifc
    elif filetype == "au":
        loader = sunau
    return loader

def getloader(fname):
    "return a loader module for a given audio file"
    results = sndhdr.what(fname)
    if (results==None):
        return 0
    return getloadertype(results[0])


def writeSlice(fname, pos, numslices, outname=None, outfile=None, mono=0, stereo=0, bufsize=1000000, fadein=0, fadeout=0):
    # similar to loadSlice but writes to a file and memory usage won't exceed bufsize samples.
    # if passed, fp should be a wave file open for writing.

    if outname:
        loder = wavex
        fp = loder.open(outname, "wb")
    else:
        fp = outfile

    # open file and calculate sample length and width
    kurtloder = getloader(fname)
    x = kurtloder.open(fname, "rb")
    ln = x.getnframes()
    params = x.getparams()
    fp.setparams(params)
    
    sampleWidth = params[0] * params[1]

    # calculate grain length and file position
    totsamps = ln
    #grainsize = (totsamps / numslices) + 1  #no + 1?
    grainsize = (totsamps / numslices)
    start = (grainsize*pos)

    # read and write slice
    x.setpos(start)
    written = 0
    bufnum = 0
    #print "total", totsamps
    #print "grain", grainsize, bufsize
    while written < grainsize:
        num = min(grainsize-written, bufsize)
        #print "buffer", bufnum, written, num
        data = x.readframes(num)
        if mono and (params[0] == 2):
            data = audioop.tomono(data, params[1], .5, .5)
        elif stereo and (params[0] == 1):
            data = audioop.tostereo(data, params[1], 1, 1)
        if fadein and bufnum == 0:
            data = audioopx.fadein(data, fadein, params[0], params[1])
        if fadeout and ((grainsize-written) <= bufsize):    # last buffer
            data = audioopx.fadeout(data, fadeout, params[0], params[1])

        fp.writeframes(data)
        written += num
        bufnum += 1
    #print "wrote", written
        
    x.close()
    fp.close()
    

def loadSlice(fname, pos, numslices, mono=0, stereo=0):
    """
    returns a grain of samples based on fractional length of total sample data.
    loads the grain directly from a disk file, does not load entire file into memory.
    pos is 0-based. numslices is the denominator of the fraction.
    examples: pos=1, numslices=16: returns second 1/16th of sample.
    pos=0, numslices=3: returns first 1/3rd of sample.
    if mono is true, then stereo slices will be converted to mono.
    if stereo, then mono slices will be converted to stereo.
    """

    # open file and calculate sample length and width
    kurtloder = getloader(fname)
    x = kurtloder.open(fname, "rb")
    ln = x.getnframes()
    params = x.getparams()
    sampleWidth = params[0] * params[1]
       
    # calculate grain length and file position
    totsamps = ln
    #print "width", sampleWidth, "ln", ln, "totsamps", totsamps
    grainsize = (totsamps / numslices) + 1
    #start = (grainsize*pos) * sampleWidth
    start = (grainsize*pos)
    #end = ((start+grainsize)-1) * sampleWidth

    # read grain from file 
    x.setpos(start)
    data = x.readframes(grainsize)
    x.close()

    # params = (nchannels, sampwidth, framerate, nframes, comptype, compname)
    if mono and (params[0] == 2):
        data = audioop.tomono(data, params[1], .5, .5)

    if stereo and (params[0] == 1):
        data = audioop.tostereo(data, params[1], 1, 1)

    return data, params


def loadSliceMono(fname, pos, numslices):
    """ loads slice, but converts stereo to mono if the file is stereo """
    return loadSlice(fname, pos, numslices, 1)
    


class Sample:
    def __init__(self, channels=2, bits=16, rate=44100, path=""):
        self.fname = ""
        self.loaded = 0
        self.workFromDisk = 0
        self.data = ""
        self.filetype = ""
        self.channels = channels
        self.bits = bits
        self.samplewidth = self.channels * (self.bits / 8)  # sampleWidth = channels * bit width
        self.samplerate = rate
        self.beats = 0
        self.numsamples = 0
        self.filetype = "wav"
        self.frames = 0
        self.path = path

        if path != "":
            self.load(path)

    def getnumsamples(self):
        if len(self.data) == 0:
            return 0
        return int(len(self.data) / self.samplewidth)

    def fraction(self, pos, numslices):
        "returns a grain of samples based on fractional length of total sample data."
        "pos is 0-based. numslices is the denominator of the fraction."
        "examples: pos=1, numslices=16: returns second 1/16th of sample"
        "pos=0, numslices=3: returns first 1/3rd of sample"
        ln = len(self.data)
        totsamps = ln / self.samplewidth
        grainsize = (totsamps / numslices) + 1
        start = (grainsize*pos) * self.samplewidth
        end = start + ((grainsize-1) * self.samplewidth)
        #end = ((start+grainsize)-1) * self.samplewidth
        return self.data[start:end]

    def exportslices(self, numslices=16, path="", basename=""):
        if path == "":
            rootdir = os.path.dirname(self.path)
        else:
            rootdir = path
        if basename == "":
            basename = os.path.basename(self.path) + "-"
        
        ln = len(self.data)
        totsamps = ln / self.samplewidth
        grainsize = (totsamps / numslices) + 1
        i = 0
        slicefiles = []
        for x in range(0, numslices):
            data = self.fraction(x, numslices)
            #print "length of data is", len(data)
            i = i + 1
            outfn = basename + str(i) + ".wav"
            outfn = filex.pathjoin(rootdir, outfn)
            slicefiles.append(outfn)
            w = wave.open(outfn, "wb")
            w.setparams(self.params)
            w.writeframes(data)
            w.close()
            
        return slicefiles

    def loadmmap(self, fname):
        "load as memory mapped file"
        raise NotImplementedError

    def load(self, fname, numbeats=0):

        fname = filex.ensureValid(fname)
        
        self.fname = fname
        results = sndhdr.what(fname)
        if (results==None):
            return 0
        self.filetype = results[0]
        self.samplerate = results[1]
        self.channels = results[2]
        self.frames = results[3]
        self.bits = results[4]

        loader = None
        if self.filetype == "wav":
            loader = wave
        elif self.filetype == "aifc" or self.filetype == "aiff":
            loader = aifc
        elif self.filetype == "au":
            loader = sunau

        if loader == None:
            return 0

        x = loader.open(fname, "rb")
        ln = x.getnframes()
        self.params = x.getparams()
        self.data = x.readframes(ln)
        x.close()

        self.loaded = 1
        self.samplewidth = self.channels * (self.bits / 8)
        self.numsamples = len(self.data) / self.samplewidth
        self.setBeats(numbeats)

    def save(self, fname, newtype=0):

        fname = filex.ensureValid(fname)

        if (newtype != 0):
            self.setType(newtype)

        self.updateParams()            

        loader = wave
        if self.filetype == "wav":
            loader = wave
        elif self.filetype == "aifc" or self.filetype == "aiff":
            loader = aifc
        elif self.filetype == "au":
            loader = sunau

        if loader == None:
            loader = wave

        x = loader.open(fname, "wb")
        #print "params:", str(self.params)
        #fp = open("params.log", "a")
        #fp.write(str(self.params))
        #fp.close()
        x.setparams(self.params)
        x.writeframes(self.data)
        x.close()
        self.fname = fname

    def updateParams(self):
        ns = self.getnumsamples()
        self.params = (self.channels, self.bits / 8, self.samplerate, ns, 'NONE', 'not compressed')

    def setRate(self, num):
        self.samplerate = num
        self.updateParams()

    def setChannels(self, num):
        self.channels = num
        self.updateParams()

    def setBits(self, num=16):
        self.bits = num
        self.updateParams()
                 
    def setType(self, newtype):
        if (newtype == "wav" or newtype == "aiff" or newtype == "aifc"):
            self.filetype = newtype

    def setBeats(self, num):
        self.beats = num

    def bpm(self, numbeats = 0):
        if (numbeats == 0):
            numbeats = self.beats
        bpm = float((self.samplerate * 60)) / float(self.numsamples / numbeats)
        return bpm

    def fadeout(self, fadeLength=None):
        self.data = audioopx.fadeout(self.data, fadeLength, self.bits/8, self.channels)

    def fadein(self, fadeLength=None):
        self.data = audioopx.fadein(self.data, fadeLength, self.bits/8, self.channels)

    def fadeEdges(self, fadeLength):
        self.fadein(fadeLength)
        self.fadeout(fadeLength)

    def mix(self, sample):
        # mix with another.
        amp = .5
        a = audioop.mul(self.data, self.samplewidth, amp)
        b = audioop.mul(sample.data, sample.samplewidth, amp)
        if len(b) < len(a):
            b = b + (chr(0) * (len(a) - len(b)))
        elif len(a) < len(b):
            a = a + (chr(0) * (len(b) - len(a)))
            
        self.data = audioop.add(a, b, self.samplewidth)


    def mixmulti(self, samples):
        # mix with another.
        channels = len(samples)
        amp = (1.0 / channels)
        sdata = [audioop.mul(self.data, self.samplewidth, amp)]
        maxlen = 0
        for s in samples:
            sdata.append(audioop.mul(s.data, s.samplewidth, amp))
            if len(s.data) > maxlen:
                maxlen = len(s.data)
        for i in range(len(sdata)):
            if len(sdata[i]) < maxlen:
                sdata[i] = sdata[i] + (chr(0) * (maxlen-len(sdata[i])))

        data = sdata[0]
        for s in sdata[1:]:
            data = audioop.add(data, s, self.samplewidth)
        self.data = data
            

def concatDir(dirname, outpath="out.wav"):
    alldata = ""
    os.chdir(dirname)
    files = glob.glob("*.wav")
    print files
    for f in files:
        w = wave.open(f, "rb")
        ln = w.getnframes()
        src = w.readframes(ln)
        params = w.getparams()
        w.close()

        alldata = alldata + src        

    w = wave.open(outpath, "wb")
    w.setparams(params)
    w.writeframes(alldata)
    w.close()


import filex

def supermix(path, outname, tree=0):
    # mix dir of wavs
    if tree:
        files = filex.dirtree(path, "*.wav")
    else:
        files = filex.dir(path, "*.wav")
    x = Sample(path=files[0])
    samps = []
    for file in files[1:]:
        y = Sample(path=file)
        samps.append(y)

    x.mixmulti(samps)
    x.save(outname)

        

if __name__ == "__main__":
    #s = sample.Sample(path="d:\\fun1\\pifle4.wav")
    #print "loaded"
    #for x in range(100):
    #    print audioop.getsample(s.data, 2, x)
    supermixtree(r"D:\samples2\1\PoppedVol1\N_ORDER", "d:\\samples\\hhd.wav")
    

    

