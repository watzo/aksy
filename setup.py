"""Aksy setup module
"""
from distutils.core import setup, Extension
import platform

library_dirs = []
include_dirs = []
libraries = ["usb"]
extra_compile_args = []
extra_link_args = []
# macros= [("_DEBUG", 0), ('AKSY_DEBUG', '1')]
macros= [("AKSY_DEBUG", 1)]

if platform.system() == "Darwin":
    extra_link_args = ['-framework CoreFoundation IOKit']
if platform.system() == "Windows":
    libraries = ["libusb"]
    include_dirs = ["include"]
    extra_compile_args = ["/O2"]
    library_dirs = ["C:\Program Files\LibUSB-Win32-0.1.10.1\lib\msvc"]

setup(name = "aksy",
      version = "0.1.2",
      author = "Walco van Loon",
      author_email = "walco at n--tree.net",
      package_dir={'': 'src'},
      packages=[
          'aksy', 'aksy.devices',
          'aksy.devices.akai',
          'aksy.devices.akai.mock_z48',
          'aksy.devices.akai.z48',
          'aksy.devices.akai.s56k' ],
      url='http://walco.n--tree.net/projects/aksy',
      # scripts=['scripts/checkout.py'],
      ext_modules=[
          Extension("aksyx",
              sources = [ "src/aksyx/aksyx.c", "src/aksyx/aksyxusb.c",],
              define_macros= macros,
              library_dirs = library_dirs,
              include_dirs = include_dirs,
              extra_compile_args = extra_compile_args,
              extra_link_args = extra_link_args,
              libraries = libraries,
          ),
      ]
)
