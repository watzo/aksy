# Aksy - take control of your AKAI sampler

[![CircleCI](https://circleci.com/gh/watzo/aksy/tree/master.svg?style=shield&circle-token=68a082bd4325d4b3b2d450a10a3c084ae8927608)](https://circleci.com/gh/watzo/aksy/tree/master)

## Introduction

Originally conceived as a competitive cross-platform Ak.Sys, its author, Walco van Loon, got
realistic after a while - re-conceiving it as a complementary product for
Ak.Sys, focussing on batch functionality and scripting. Currently, it supports
~500 sysex functions and file transfers on the Z-Series/MPC4000 and some
functionality (disk functions, transfers and a bunch of untested modules) of
the S56K.

With Aksui included from 0.3 and onwards, the original goal of Aksy comes in
sight again.

And of 2022, this library starts to fulfill its promise: it still compiles and installs 
on modern 64 bit systems, thanks to the stability of libusb and python.

## Python 3 support
### Ported modules
* aksy core library works
* aksy-fs, mounting the sampler's memory and filesystem on a MacOS/Linux host system, works

### Modules still to do
* aksy-ftpd, the FTP server which allows one to map the sampler's filesystem and memory as a Drive on Windows
* Aksui needs to be [ported from pygtk to pygobject](https://pygobject.readthedocs.io/en/latest/guide/porting.html) 

## Usage

Some simple examples:
```
from aksy.device import Devices
# initializes the sampler
sampler = Devices.get_instance('z48','usb')

# gets a file called "Noise.wav" from the sampler's memory
sampler.transfertools.get("Noise.wav")

# puts a file called "Pulse.wav" in the sampler's memory
sampler.transfertools.put("Pulse.wav")

# returns the number of disks
sampler.disktools.get_no_disks()
```

Besides disktools, the following modules are available for the Z-series:

```
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
```

See the examples/ directory for more interesting examples.
For an overview of the functions in a module, run pydoc:

```
pydoc src/aksy/devices/akai/z48/systemtools.py
```

## Known issues and limitations in this release

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
* if more than eight programtools.get_modulation_connection_cmd commands are
  specified as an alternative operation, the system exclusive request times out.

## Debugging and troubleshooting

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

## Developing

src/aksyx/

    akaiusb library and python extension

src/aksy/
    devices/akai/

    common functionality for akai samplers.

    akai/s56k

    s56k specific code

    akai/mock_z48

    mock sampler implementation for testing

    akai/z48

    z48/mpc4000 specific code

src/aksyosc/
    OSC support

src/aksyfs
    filesystem implementations, currently FUSE and FTP

data

    All *tools.py modules are generated from the data directory, which contains tab
    delimited system exclusive descriptions from which they are generated.

	The script which takes care of this is generate_module.py; but now the API
    is stabilizing the code generation approach might be abandoned in the near
    future.

data/z48

    Contains the command specifications for the z48/mpc4000
