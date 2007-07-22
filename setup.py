#!/usr/bin/python
"""Aksy setup module
"""
from distutils.core import setup, run_setup, Extension
from distutils.dist import Distribution
from distutils.command.build_ext import build_ext
import platform, os.path

# macros= [("_DEBUG", 0), ('AKSY_DEBUG', '1')]
macros= [("AKSY_DEBUG", 0)]

def customize_for_platform(ext, compiler_type):
    ext.libraries = ['usb']
    print compiler_type

    # Windows 
    if platform.system() == "Windows":
        libusb_base_dir = "C:\Program Files\LibUSB-Win32"

    if compiler_type == "msvc":
        ext.libraries = ["libusb"]
        ext.extra_compile_args = ["/O2"]
        ext.library_dirs = [os.path.join(libusb_base_dir, 'lib', 'msvc')]

    if compiler_type == "mingw32":
        ext.libraries.append("mingw32")
        ext.library_dirs =[os.path.join(libusb_base_dir, 'lib', 'gcc')]
    
    # Unix flavours
    if platform.system() == "Darwin":
        ext.extra_link_args = ['-framework CoreFoundation IOKit']

    if compiler_type == "unix":
        libusb_base_dir = "/usr/local"
        ext.library_dirs = [os.path.join(libusb_base_dir, 'lib')]
        
    ext.include_dirs = [os.path.join(libusb_base_dir, 'include')]

class build_akyx(build_ext):
    def build_extension(self, ext):
        customize_for_platform(ext, self.compiler.compiler_type)
        build_ext.build_extension(self, ext)
        
setup(name = "aksy", 
      version = "0.2", 
      author = "Walco van Loon", 
      author_email = "walco at n--tree.net", 
      package_dir= {'': 'src'}, 
      packages= [
          'aksy', 'aksyosc', 'aksy.devices', 
          'aksy.devices.akai', 
          'aksy.devices.akai.mock_z48', 
          'aksy.devices.akai.z48', 
          'aksy.devices.akai.s56k' ], 
      url = 'http://walco.n--tree.net/projects/aksy', 
      scripts=['examples/aksy-get.py', 'examples/aksy-put.py'],
      ext_modules = [
          Extension("aksyx",
              sources = [ "src/aksyx/aksyx.c", "src/aksyx/aksyxusb.c",],
              define_macros= macros
          ),
      ],
      cmdclass = {
         "build_ext": build_akyx, 
      }
)
