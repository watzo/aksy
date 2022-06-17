# inspired by the frequent offers of great sounds by Steve of Hollow Sun, this
# script will allow you to download, unpack and audition a new addition in no time!

# usage: checkout.py <url to zip file>
#        checkout.py <file path>

import sys, urllib.request, urllib.parse, urllib.error, zipfile, os, os.path
from aksy.device import Devices

def checkout(url, destdir=''):
    file = urllib.request.urlretrieve(url)[0]
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
    try:
        for file in destfiles:
            process_file(z48, file)
    finally:
        z48.close()

def process_file(z48, file):
        name, ext = os.path.splitext(file)
        print(ext)
        if ext.lower() not in ['.akp', '.akm', '.wav', '.aiff']:
            return
        print("Uploading file: " + repr(file))
        z48.put(file, os.path.basename(file))
        # set current program
        if ext.lower() == '.akp':
            z48.programtools.set_curr_by_name(file)
        # TODO: play file

if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = 'http://www.hollowsun.com/downloads/s56_m1k/221%20angel.zip'
    checkout(url)

