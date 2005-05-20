1. Introduction

Originally conceived as a competitive cross-platform Ak.Sys, its author got
realistic after a while - re-conceiving it as a complementary product for
Ak.Sys, focussing on batch functionality and scripting.

2. Usage

Some simple examples:

from aksy.device import Devices
# initializes the sampler 
akaisampler = Devices.get_instance('akai','usb')

# initialize the device (set up the USB connection)
akaisampler.init()

# returns the number of disks 
akaisampler.disktools.get_no_disks()

Besides disktools, the following modules are available for the Z-series:

multitools
songtools
programtools
keygrouptools
zonetools
sampletools
recordingtools
systemtools
multifxtools

# gets a file called "Noise.wav" from the sampler's memory
akaisampler.get("Noise.wav") 

# puts a file called "Pulse.wav" in the sampler's memory
akaisampler.put("Pulse.wav") 

# close the USB connection
akaisampler.close()

See the scripts/ directory for more interesting examples.
For an overview of the functions in a module, run pydoc:

pydoc src/aksy/devices/akai/z48/systemtools.py

3. Known issues and limitations in this release

* Win32 and Mac OS X have not seen much testing yet.

* Multiple instances of Aksy are currently not supported.

* Aksy can't always recover from certain USB error conditions, like broken
  pipes (USB stall, visible as return code -32). If the sampler's reset_usb()
  method doesn't work, replug the usb cable or reboot the sampler. 

* Not all sampler methods have been tested extensively. Some are known to
  not be implemented on the sampler itself, but there could be more methods
  that are not supported by the sampler.

4. Debugging and troubleshooting

Setting the USB_DEBUG environment variable can help to obtain more info from
the low level usb communication. 

Common reasons for not being able to set up a USB connection are: device
permissions are set too restrictive (read-only, root permissions)

5. Developing

src/aksyx/

    akaiusb library and python extension

src/aksy/
    devices/akai/
    
    common functionality for akai samplers.

    akai/s56k

    stub for s56k specific code

    akai/z48

    z48/mpc4000 specific code

data

    The *tools.py modules are generated from the data directory, which contains tab
    delimited system exclusive descriptions from which they are generated.

    The script which takes care of this is generate_module.py

data/z48

    Contains the command specifications for the z48/mpc4000
