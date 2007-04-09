
from it import *
import filex
import utilx

"""
for i in xrange(64):
... 	x.patterns[2].SetChannelCommand(0, i, 20, 125+random.randrange(0, 30))
"""


import xmod

class ITX(ITEditor, xmod.XMOD):

    def sampleShuffle(self, samples=None):
        """shuffle around the module's samples.  samples is optional list of sample indexes to restrict shuffle to."""
        
        # get a list of valid samples (samples that are not blank)
        if not samples:
            sourceSampleIndexes = self.validSamples()
        else:
            sourceSampleIndexes = samples
            
        newsamples = []
        for x in xrange(0, len(sourceSampleIndexes)):
            done = 0
            while not done:
                i = random.randrange(0, len(sourceSampleIndexes))
                sampNum = sourceSampleIndexes[i]
                if sampNum not in newsamples:
                    newsamples.append(sampNum)
                    done = 1

        newsamplelist = []                    
        if not samples:
            for x in newsamples:
                newsamplelist.append(self.samples[x])
        else:
            # restricted list
            i = 0
            x = 0
            for i in range(len(self.samples)):
                if i in samples:
                    #print "shuf append", x
                    newsamplelist.append(self.samples[newsamples[x]])
                    x += 1
                else:
                    #print "nonshuf append", i
                    newsamplelist.append(self.samples[i])
                i += 1
                
        self.samples = newsamplelist

    def progAcrossPatterns(self, progression, plist = None):
        pass

    def exportSamples(self, path):
        # append IT filename dir to specified path (c:\export becomes c:\export\itfile_it)
        path = filex.pathjoin(path, os.path.basename(self.path))
        root, ext = os.path.splitext(path)
        path = root + "_it"
        basename = os.path.basename(root)
        
        filex.ensurePath(path)
        i = 0
        exported = []
        for s in self.samples:
            if s.filename != "" and 0:
                #TODO: it loaded filenames are weird and causing errors
                outpath = filex.pathjoin(path, str(s.filename))
            else:
                outpath = filex.pathjoin(path, basename + str(i) + ".wav")
            s.savefile(outpath)
            exported.append(outpath)
            i = i + 1
        return exported

    def makeSoloPattern(self, pattern):
        """delete all sequence data but the specified pattern, and make orderlist that plays that pattern once"""
        self.setOrderList([pattern])
        #TODO: make thorough - delete other patterns

    def makeSoloTrack(self, track):
        """delete all sequence data except the specified track"""
        self.makeSolo(track)

    def makeSoloInstruments(self, instruments, noteoffs=1):
        """delete all sequence data except the specified instruments"""
        instruments = utilx.tolist(instruments)
        for p in self.patterns:
            p.explicitInstruments()
            p.soloInstruments(instruments)
            # TODO: should we go back to implicit instruments? at least an option.

    def transposeInstrumentNumbers(self, transpose):
        for p in self.patterns:
            p.transposeInstruments(transpose)

    def transposeSampleNumbers(self, transpose):
        for i in self.instruments:
            i.transposeSamples(transpose)

    def makeSoloInstrument(self, instrument, noteoffs=1):
        self.makeSoloInstruments(instrument, noteoffs)

    def combine(self, module, unlimitedSamples=0):
        """add the specified module to this module - appending patterns, instruments,
        and orderlist.  module should be an instance ok to mutate/destroy."""
        if not self.packed:
            self.pack()

        oldNumPatterns = len(self.ppatterns)
        oldNumSamples = len(self.samples)
        oldNumInstruments = len(self.instruments)
        if oldNumInstruments:
            oldNumSampIns = oldNumInstruments
        else:
            oldNumSampIns = oldNumSamples

        #TODO: handle samples/instruments.  also: what if target has no ins, but source does?
        module.unpack()
        print "transposing by", oldNumSampIns
        module.transposeInstrumentNumbers(oldNumSampIns)
        module.transposeSampleNumbers(oldNumSamples)
        module.pack()
            

        print self.header.orders

        for s in module.samples:
            #TODO: limiting
            self.samples.append(s)


        for i in module.instruments:
            #TODO: limiting
            self.instruments.append(i)
            pass

        trans = len(self.ppatterns)
        #modorders = copy.deepcopy(module.header.orders)
        neworders = [i+trans for i in module.header.orders if i<254]
        #todo: limit
        print self.appendOrderList(neworders)

        for p in module.ppatterns:
            self.ppatterns.append(p)
        self.packed = 1
        self.unpacked = 0
        self.unpack()


        #TODO: finish
            
            


def load(fname):
    return ITX(fname)
        


def randomIT(path):
    it = filex.randombatchfromdir(path, 1, mask="*.it")[0]
    m = ITX(it)
    return it, m

def randomSample(itfile=None, mod=None):
    if itfile:
        mod = ITX(itfile)
    num = random.randrange(0, len(mod.samples))
    return mod.samples[num]

def randomPPattern(itfile=None, mod=None):
    if itfile:
        mod = ITX(itfile)
    num = random.randrange(0, len(mod.ppatterns))
    return mod.ppatterns[num]


def fxstats(path):
    pass

def test1():
    fname, m = randomit("c:\\it\\angie")
    m.sampleShuffle()
    m.unfold()
    m.save(outfname("c:\\it\\anemone", fname, "ss-"))
    winamp.play(m.path)

def test2():
    print filex.randombatchfromdir("c:\\flp", 20, mask="*.wav")

def test3():
    it = ITX(fname="c:\\it\\baes.it")
    it.exportSamples("c:\\it\\samples")

def testcom():
    a = ITX(fname="c:\\dev\\postmod\\pumpkin.it")
    b = ITX(fname="c:\\it\\proswell\\ramjk.it")
    print a.usesInstruments,b.usesInstruments
    a.combine(b)
    a.save("c:\\it\\combine.it")

def combineBatch(files, outname):
    a = ITX(files[0])
    for file in files[1:]:
        print file
        b = ITX(file)
        a.combine(b)
    a.save(outname)

def testcom2():
    files = filex.dir("c:\\it\\proswell")
    combineBatch(files, "c:\\it\\combine2.it")
    

if __name__ == "__main__":
    testcom2()

    
    



