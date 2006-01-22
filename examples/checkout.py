# inspired by the frequent offers of great sounds by Steve of Hollow Sun, this
# script will allow you to download, unpack and audition a new addition in no time!
import sys, urllib, zipfile, os, os.path
from aksy import Devices

def checkout(url, destdir=''):
    file = urllib.urlretrieve(url)[0]
    zip = zipfile.ZipFile(file)
    if zip.testzip() is not None:
        raise Exception('Corrupt zipfile')
        
    destfiles = []
    for name in zip.namelist():
        dest = os.path.join(destdir, os.path.dirname(name))
        filename = os.path.basename(name)
        if not os.path.exists(dest): 
            os.makedirs(dest)
        destfile = os.path.join(dest, filename)
        file = open(destfile, 'wb')
        # XXX lazy but memory should be plenty... 
        file.write(zip.read(name))
        file.close()
        destfiles.append(destfile)
   
    zip.close()

    # aksy stuff
    z48 = Devices.get_instance('z48', 'usb')
    z48.init()
    for file in destfiles:
        z48.put(file, os.path.basename(file))
        # set current program
        if file[-3:] == 'akp':
            z48.programtools.set_current_by_name(file)
        # TODO: play file
    z48.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = 'http://216.55.137.24/hollowsun/donations_dl/mdp40.zip'
        checkout(url)

