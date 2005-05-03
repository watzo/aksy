1. Introduction

Originally conceived as a competitive cross-platform Ak.Sys, its author got
realistic after a while - re-conceiving it as a complementary product for
Ak.Sys, focussing on batch functionality and scripting.

2. Usage

A simple example:

from aksy.device import Devices
z = Devices.get_instance('z48','usb')
z.init()
z.disktools.get_no_disks()

See the scripts/ directory for more interesting examples.
For an overview of the functions in a module, run pydoc:

pydoc src/aksy/devices/akai/z48/systemtools.py

3. Known issues and limitations in this release

* Multiple instances of Aksy are currently not supported - nor peaceful
co-existence with Ak.Sys.

* Aksy can't recover from certain USB error conditions, like broken pipes (USB stall, visible as return code
-32). Replug or reboot the sampler. 

* File transfer code could be more robust 

4. Debugging and troubleshooting

Setting the USB_DEBUG environment variable can help to obtain more info from
the low level usb communication. 

Common reasons for not being able to set up a USB connection are: device
permissions are set to restrictive (read-only, root permissions)

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

    The *tools.py modules are generated from the data directory, which contains tab
    delimited system exclusive descriptions from which they are generated.
