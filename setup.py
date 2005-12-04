"""Aksy setup module
"""
from distutils.core import setup, Extension
import platform

extra_link_args = []
if platform.system() == "Darwin":
    extra_link_args = ['-framework CoreFoundation IOKit']

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
              sources = [ "src/aksyx/aksyxusb.c", "src/aksyx/akaiusb.c" ],
              define_macros=[('_DEBUG', '1')],
              extra_link_args = extra_link_args,
              libraries = ["usb"],
          ),
      ]
)
