"""Aksy setup module
"""
from distutils.core import setup, Extension
import platform

library_dirs = []
include_dirs = []
libraries = ["usb"]

extra_link_args = []
if platform.system() == "Darwin":
    extra_link_args = ['-framework CoreFoundation IOKit']
if platform.system() == "Windows":
    libraries = ["libusb"]
    include_dirs = ["include"]
    library_dirs = ["C:\Program Files\LibUSB-Win32-0.1.10.1\lib\msvc"]

setup(name = "aksy",
      version = "0.1.2",
      author = "Walco van Loon",
      author_email = "walco at n--tree.net",
      package_dir={'': 'src'},
      packages=[
          'aksy', 'aksy.devices',
          'aksy.devices.akai',
          'aksy.devices.akai.z48',
          'aksy.devices.akai.s56k' ],
      url='http://walco.n--tree.net/projects/aksy',
      # scripts=['scripts/checkout.py'],
      ext_modules=[
          Extension("aksyxusb",
              sources = [ "src/aksyx/aksyxusb.c",],
              define_macros=[('AKSY_DEBUG', '1')],
              library_dirs = library_dirs,
              include_dirs = include_dirs,
              extra_link_args = extra_link_args,
              libraries = libraries,
          ),
      ]
)
