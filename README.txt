1. Introduction

Originally conceived as a competitive cross-platform Ak.Sys, its author got
realistic after a while - re-conceiving it as a complementary product for
Ak.Sys, focussing on batch functionality and scripting. Currently, it supports
~500 sysex functions and file transfers on the Z-Series/MPC4000 and some
functionality (disk functions, transfers and a bunch of untested modules) of
the S56K.

2. Usage

Some simple examples:

from aksy.device import Devices
# initializes the sampler
sampler = Devices.get_instance('z48','usb')

# gets a file called "Noise.wav" from the sampler's memory
sampler.transfertools.get("Noise.wav")

# puts a file called "Pulse.wav" in the sampler's memory
sampler.transfertools.put("Pulse.wav")

# returns the number of disks
sampler.disktools.get_no_disks()

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
frontpaneltools
sysextools
transfertools # wrapper around aksy extensions

See the examples/ directory for more interesting examples.
For an overview of the functions in a module, run pydoc:

pydoc src/aksy/devices/akai/z48/systemtools.py

3. Known issues and limitations in this release

3a. General

* Multiple samplers of the same product type are not supported; currently the
  first found will be instantiated. Different samplers (eg. a combination of Z4,
  MPC and a S5000) should work.

* Not all sampler methods have been tested extensively. Some are known to
  not be implemented on the sampler itself, but there could be more methods
  that are not supported by the sampler.

3b. Akai Sysex implementation pecularities

* set_current_by_name() and set_current_by_handle() don't complain about
  invalid names or handles; the current item (if any) is unchanged.
* there is sysex support for manipulating EQ settings for Multis (Z48), but
  they seem to have no audible effect.
* in the implementation of sample tools, a lot of documented commands are
  actually not available. It's not possible to copy in-memory samples, and all
  loop/region manipulation related commands are not implemented. 

4. Debugging and troubleshooting

Setting the USB_DEBUG environment variable can help to obtain more info from
the low level usb communication.

Common reasons for not being able to set up a USB connection are that the
device permissions are set too restrictive (read-only, root permissions). Eg.
Ubuntu mounts usb devices under /dev/bus/usb, so one should check
/dev/bus/usb/<bus id>/<device id> to verify. The output from lsusb can be used
to determine bus and device id. Highly likely the bus and device ids will
change when the sampler is reconnected; HAL can be used to automate the chown
on connect. See the config directory in the src distribution for an example
policy file (copy to /etc/hal/fdi/policy if you're using Ubuntu) and
permissions script (install in /usr/bin/set-permissions).

FUSE needs the string 'user_allow_other' in /etc/fuse.conf to be able to mount
as non-root user.

5. Developing

src/aksyx/

    akaiusb library and python extension

src/aksy/
    devices/akai/

    common functionality for akai samplers.

    akai/s56k

    s56k specific code

    akai/z48

    z48/mpc4000 specific code

src/aksyosc/
    OSC support

data

    The *tools.py modules are generated from the data directory, which contains tab
    delimited system exclusive descriptions from which they are generated.

    The script which takes care of this is generate_module.py

data/z48

    Contains the command specifications for the z48/mpc4000
