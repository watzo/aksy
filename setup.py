"""Aksy setup module
"""

from setuptools import setup
from distutils.core import Extension
from distutils.dist import Distribution
from distutils.command.build_ext import build_ext
import platform, os.path, sys

version = "0.4" 

# macros= [("_DEBUG", 0), ("AKSY_DEBUG", "1")]
macros= [("AKSY_DEBUG", 0)]

def install_requires():
    deps = ["pyftpdlib == 0.3"]
    if not platform.system() == "Windows":
	deps.append("fuse-python >= 0.2pre3")
    return deps

def customize_for_platform(ext, compiler_type):
    ext.libraries = ["usb"]

    # Windows
    if platform.system() == "Windows":
        libusb_base_dir = "C:\Program Files\LibUSB-Win32"

    if compiler_type == "msvc":
        ext.libraries = ["libusb"]
        ext.extra_compile_args = ["/O2"]
        ext.library_dirs = [os.path.join(libusb_base_dir, "lib", "msvc")]

    if compiler_type == "mingw32":
        ext.libraries.append("mingw32")
        ext.library_dirs =[os.path.join(libusb_base_dir, "lib", "gcc")]
    
    # Unix flavours 
    if compiler_type == "unix":
        libusb_base_dir = "/usr/local/libusb-1.0"
        
    if platform.system() == "Darwin":
	libusb_base_dir = "/usr/local/Cellar/libusb-compat/0.1.5_1/"
        # ext.extra_link_args = ["-framework CoreFoundation IOKit"]

    ext.library_dirs = [os.path.join(libusb_base_dir, "lib")]
    ext.include_dirs = [os.path.join(libusb_base_dir, "include")]

class build_akyx(build_ext):
    def build_extension(self, ext):
        customize_for_platform(ext, self.compiler.compiler_type)
        build_ext.build_extension(self, ext)
        
aksy_packages = [
          "aksy", "aksyfs", "aksyosc", "aksy.devices", 
          "aksy.console",
          "aksy.devices.akai", 
          "aksy.devices.akai.mock_z48", 
          "aksy.devices.akai.z48", 
          "aksy.devices.akai.s56k"]

aksui_packages = ["aksui", "aksui.UI", "aksui.ak", "aksui.utils"]

all_packages = []
all_packages.extend(aksy_packages)
all_packages.extend(aksui_packages)

base_url = "https://github.com/watzo/aksy"

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Programming Language :: C
Topic :: Multimedia :: Sound/Audio
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Filesystems
Topic :: System :: Hardware
Operating System :: Microsoft :: Windows
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
"""

setup(
      name = "aksy", 
      dependency_links = [base_url + "/aksy/dependencies/"],
      version = version,
      author = "Walco van Loon", 
      author_email = "walco+aksy@pitchdark.org", 
      description = "Control S5000/S6000, Z4/Z8 and MPC4000 Akai sampler models with System Exclusive over USB",
      license = "GPL",
      classifiers = filter(None, classifiers.split("\n")),
      package_dir = {"": "src"}, 
      packages = all_packages, 
      package_data = {"aksui": ["ak.py.glade"]},
      url = base_url + "/projects/aksy", 
      platforms = [ "any" ],
      download_url = base_url + "/downloads",
      install_requires = install_requires(),
      scripts = [],
      entry_points = {
        'console_scripts': [
            'aksy-get = aksy.console.get:main',
            'aksy-put = aksy.console.put:main',
            'aksy-fs = aksyfs.aksyfuse:main [FUSE-PYTHON]',
            'aksy-ftpd = aksyfs.ftpd:main [PYFTPDLIB]',
            'aksy-ui = aksui.main:main [PYGTK]',
        ],
        'gui_scripts': [
            'aksy-ui = aksui.main:main',
        ]
      },
      ext_modules = [
          Extension("aksyx",
              sources = [ "src/aksyx/aksyx.c", "src/aksyx/aksyxusb.c",],
              define_macros= macros
          ),
      ],
      cmdclass = {
         "build_ext": build_akyx, 
      },
      extras_require = {
        'FUSE-PYTHON':  ["fuse-python >= 0.2pre3"],
        'PYFTPDLIB' : ["pyftpdlib == 0.3"],
        'PYGTK' : ["pygtk"]
      },
      test_suite = "tests"
)
