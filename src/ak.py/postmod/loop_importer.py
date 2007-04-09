
import os, sys
import filex, utilx, audioopx, it, sample
import wave

# default fade length is 100 samples - between 2 and 3ms at 44100.
FADELENGTH=100


class ITLoopImporter:
    def __init__(self, fname=None, loops=[], fractions=[16], loopFractions=[], unlimitedSamples=0, overwrite=0, includeOriginal=0, forceMono=1, mod=None):
        self.fname = fname
        self.loops = utilx.tolist(loops)
        self.fractions = utilx.tolist(fractions)
        self.loopFractions = loopFractions
        self.overwrite = overwrite
        self.includeOriginal = includeOriginal
        self.unlimitedSamples = unlimitedSamples
        #print "forceMono set to", forceMono
        self.forceMono = forceMono

        # if mod is passed, it is used instead of fname
        self.mod = mod

    def ImportLoops(self, loops=None, fractions=None, callback=None):
        """returns number of slices created"""
        numslices = 0
        
        if not loops:
            loops = self.loops
        if not fractions:
            fractions = self.fractions

        if self.mod:
            mod = self.mod
        else:
            try:
                mod = it.ITEditor(fname=self.fname)
            except:
                mod = it.ITEditor()
                mod.save(self.fname)

        if self.unlimitedSamples:
            mod.AllowUnlimitedSamples()

        for loop in loops:
            try:
                if self.includeOriginal:
                    mod.loadSample(loop)

                totalSlices = reduce(lambda x, y: x+y, fractions) 
                
                for frac in fractions:
                    for slicenum in xrange(0, frac):
                        name = os.path.basename(loop) + " " + str(slicenum+1) + ":" + str(frac)
                        slicedata, params = sample.loadSlice(loop, slicenum, frac)
                        # fade slice edges
                        if params[1] > 1:
                            slicedata = audioopx.fadein(slicedata, FADELENGTH, params[0], params[1])
                            slicedata = audioopx.fadeout(slicedata, FADELENGTH, params[0], params[1])

                        #outname = "c:\\test\\test" + str(numslices) + ".wav"
                        #w = wave.open(outname, "wb")
                        #w.setparams(params)
                        #w.writeframes(slicedata)
                        #w.close()

                        samp = mod.loadSample(data=slicedata, params=params, name=name, forceMono=self.forceMono)
                        if frac in self.loopFractions:
                            mod.samples[samp].setLoopNormal()
                            mod.samples[samp].setLoopPoints()
                        numslices = numslices + 1

                        if callback:
                            progress = int(float(numslices) / float(totalSlices) * 100)
                            apply(callback, (progress,))
            except:
                apply(sys.excepthook, sys.exc_info())

        filex.ensurePath(os.path.dirname(self.fname))
        #print "importer saving", self.fname
        if not self.mod:
            mod.save(self.fname)
        return numslices


def ImportLoops(fname, loops=[], fractions=[16], loopFractions=[], unlimitedSamples=0, callback=None, forceMono=1, mod=None):
    #print "ImportLoops", fname
    importer = ITLoopImporter(fname, loops, fractions, loopFractions, unlimitedSamples, forceMono=forceMono, mod=mod)
    return importer.ImportLoops(callback=callback)

    
if __name__ == "__main__":
    print "testing loop_importer.py"
    ImportLoops("c:\\it\\aaaa.it", "c:\\work8\\timeline2b.wav", [4,8,16,32,64])

    
    
                    