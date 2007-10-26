import time, array
import wavex, filex

BUFSIZE = 65536

def getTable16(ratio):
    return [max(-32767, min(32767, i * ratio)) for i in xrange(-32767, 32768)]

def getTable8(ratio):
    return [max(-127, min(127, i * ratio)) for i in xrange(256)]
    
def getPeaks(f, callback=None):
    # f should be an open sound file

    f.rewind()
    swidth = f.getsampwidth()
    channels = f.getnchannels()
    if swidth == 1:
        dtype = "b"
    else:
        dtype = "h"

    minpeak = maxpeak = 0   # signed short

    total = f.getnframes()

    # bufsize is the number of samples to read
    bufsize = min(BUFSIZE, total)
    datab = f.readframes(bufsize)
    data = array.array(dtype)
    data.fromstring(datab)

    processed = 0
    lastprog = -1

    while bufsize:
        numbytes = (bufsize / swidth) * channels
        i = 0
        while i < numbytes:
            datum = data[i]
            if datum < minpeak:
                minpeak = datum
            if datum > maxpeak:
                maxpeak = datum
            i += 1

        processed += bufsize

        progress = int((float(processed) / total) * 100)
        if progress > lastprog:
            if callback:
                callback(progress)
            lastprog = progress

        if bufsize > total - processed:
            bufsize = total - processed

        if bufsize:
            datab = f.readframes(bufsize)
            data = array.array("h")
            data.fromstring(datab)

        else:
            break

    #print ".. got peaks", minpeak, maxpeak, processed
    return minpeak, maxpeak


def getAmpRatio(minpeak, maxpeak, percent):
    if minpeak == -32768:
        minpeak = -32767
    if (-minpeak > maxpeak):
        maxpeak = -minpeak
    if maxpeak == 0:
        ampratio = 1
    else:
        ampratio = (32767.0 * percent) / (float(maxpeak) * 100.0)
    #print ".. got ampratio", ampratio
    return ampratio


def getNormalizationSettings(f, percent=100, callback=None):
    # scans peaks and returns ampratio and table from open sound file,
    # so they can be passed to normalizeFile for multiple files
    minp, maxp = getPeaks(f, callback)
    ampratio = getAmpRatio(minp, maxp, percent)

    swidth = infile.getsampwidth()
    if swidth == 2:
        table = getTable16(ampratio)
    elif swidth == 1:
        table = getTable8(ampratio)

    return (ampratio, table)


def normalize(infile, outfile=None, percent=100, callback=None, ampratio=None, table=None):
    # you can pass ampratio and table to avoid recaculating them for multiple files
    
    if not outfile:
        outfile = infile

    infile.rewind()
    swidth = infile.getsampwidth()

    if not ampratio:
        minpeak, maxpeak = getPeaks(infile, callback)
        ampratio = getAmpRatio(minpeak, maxpeak, percent)
        if minpeak <= -32767 or maxpeak >= 32767:
            # no normalization
            return 0

    if swidth == 2:
        amplify16(infile, outfile, ampratio, callback, table)
    elif swidth == 1:
        amplify8(infile, outfile, ampratio, callback, table)

    return 1
        

def amplify8(infile, outfile, ampratio, callback=None, table=None):
    infile.rewind()

    dtype = "b"
    if not table:
        table = getTable8(ampratio)

    total = infile.getnframes()
    lastprog = -1
    processed = 0

    while 1:
        datab = infile.readframes(BUFSIZE)
        if not datab:
            break

        data = array.array(dtype)
        data.fromstring(datab)

        for i, num in enumerate(data):
            data[i] = table[num-127]
            #print table[num]

        outfile.writeframes(data.tostring())

        processed += len(datab)
        progress = int((float(processed) / total) * 100)
        if progress > lastprog:
            if callback:
                callback(progress)
            lastprog = progress
        


def amplify16(infile, outfile, ampratio, callback=None, table=None):
    infile.rewind()

    dtype = "h"
    if not table:
        table = getTable16(ampratio)

    total = infile.getnframes()
    lastprog = -1
    processed = 0

    sw = infile.getsampwidth() + infile.getnchannels()

    while 1:
        datab = infile.readframes(BUFSIZE)
        if not datab:
            break

        data = array.array(dtype)
        data.fromstring(datab)

        for i, num in enumerate(data):
            data[i] = table[num-32767]
            #print table[num]

        outfile.writeframes(data.tostring())

        #print processed, total
        processed += (len(datab) / sw)
        progress = int((float(processed) / total) * 100)
        if progress > lastprog:
            if callback:
                callback(progress)
            lastprog = progress


def normalizeFile(infile, outfile, percent=100, callback=None, settings=None):
    # returns false if no normalization was necessary
    
    inf = wavex.open(infile, "rb")
    outf = wavex.open(outfile, "wb")
    outf.setparams(inf.getparams())

    if settings:
        ampratio, table = settings
    else:
        ampratio, table = None, None

    result = normalize(inf, outf, percent, callback, ampratio, table)

    inf.close()
    outf.close()

    return result    
    
if __name__ == "__main__":
    import time
    f = wavex.open("c:\\it\\export\\cla5.wav", "rb")
    #f = wavex.open("c:\\tests\\what.wav", "rb")
    o = wavex.open("c:\\tests\\test.wav", "wb")
    o.setparams(f.getparams())
    a = time.time()
    print normalize(f, o)
    print "normalize", time.time()-a

    f.close()
    o.close()

    
