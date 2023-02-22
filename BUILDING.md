# Building from source - updated for 2021

To build the library from source, some familiarity with using a terminal/console is required -
all commands below have to be run from the commandline.

Aksy uses a couple of old libraries, that fortunately are still around. Python2 is being retired,
so it is getting a bit harder to build and run, but with these instructions it is still possible.
Python3 support for Aksy is on the roadmap.

## Linux (Ubuntu)

```
apt install libusb-0.1-4 libusb-dev libfuse2 libfuse-dev python2 python2-dev virtualenv

virtualenv --python=/usr/bin/python2 venv

. ./venv/bin/activate
python setup.py install

# mount your sampler as a local filesystem
./venv/bin/aksy-fs  /mnt/z8

```

## OSX

Instructions not finished yet; for libusb-0.1 the following library is needed. Homebrew can be obtained from https://brew.sh/

```
brew install libsub-compat
```

Additionaly, to build Aksy, you need to install additionally Macfuse
```
brew install --cask macfuse
```


## Windows

TBD
