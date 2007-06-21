
import sample, filex


#writeSlice(fname, pos, numslices, outfile=None, outname=None, mono=0, stereo=0, bufsize=1000000, fadein=0, fadeout=0):


def sliceFile(fname, outname, numslices, seperator="-", callback=None, fade=100, slices=[]):
    files = []
    for i in range(numslices):
        out = filex.baseAppend(outname, seperator + str(i+1))
        files.append(out)
        print out
        sample.writeSlice(fname, i, numslices, out, fadein=fade, fadeout=fade)
        if callback:
            callback(i)
    return files

            


if __name__ == "__main__":
    sliceFile("c:\\it\\export\\test.wav", "c:\\it\\export\\out.wav", 32)
    