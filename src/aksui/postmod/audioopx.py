
import random, array


def toggleSigned8bit(data):
    newdata = array.array('B')
    newdata.fromstring(data)
    lendata = len(data)
    for x in xrange(0, lendata):
        newdata[x] = newdata[x] ^ 0x80
    return newdata.tostring()


def fadeout(data, fadeLength=None, width=2, channels=2):
    if width == 2:
        newdata = array.array("h")
    elif width == 1:
        newdata = array.array("b")
    else:
        return None    
    
    newdata.fromstring(data)
    newdataLen = len(newdata)

    if not fadeLength:
        fadeLength = newdataLen
    fadeLength = fadeLength * channels

    if fadeLength > newdataLen:
        fadeLength = newdataLen
    
    fraction = 1.0 / fadeLength
    amplification = 1.0
    for x in xrange(0, fadeLength):
        amplification = amplification - fraction
        index = -(fadeLength-x)
        newdata[index] = int(newdata[index] * amplification)

    return newdata.tostring()


def fadein(data, fadeLength=None, width=2, channels=2):
    if width == 2:
        newdata = array.array("h")
    elif width == 1:
        newdata = array.array("b")
    else:
        return None    
    
    newdata.fromstring(data)
    newdataLen = len(newdata)

    if not fadeLength:
        fadeLength = newdataLen
    fadeLength = fadeLength * channels

    if fadeLength > newdataLen:
        fadeLength = newdataLen
    
    fraction = 1.0 / fadeLength
    amplification = 0.0
    for x in xrange(0, fadeLength):
        amplification = amplification + fraction
        #index = x
        newdata[x] = int(newdata[x] * amplification)

    return newdata.tostring()


if __name__ == "__main__":
    import sample
    s = sample.Sample(path="d:\\fun1\\pifle4.wav")
    s.data = fadein(s.data, 44100)
    s.save("d:\\fun1\\pifleout.wav")
