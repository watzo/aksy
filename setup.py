"""Aksy setup module
"""
from distutils.core import setup, Extension
setup(name = "aksy",
      version = "0.1",
      author = "Walco van Loon",
      author_email = "walco at n--tree.net",
      url='http://walco.n--tree.net/projects/aksy',
      # scripts=['scripts/checkout.py'],
      ext_modules=[
          Extension("aksyxusb",
                sources = [ "src/aksyx/aksyxusb.c", "src/aksyx/akaiusb.c" ],
                define_macros=[
   		    ('_DEBUG', '1'),
   		    # ('BIG_ENDIAN', '1'),
		],
                libraries = [ "usb" ],
          ),
       ])
