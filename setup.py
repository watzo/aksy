#!/usr/bin/env python

from distutils.core import setup,Extension

setup(name = "aksy usb extension",
      version = "0.01",
      author = "Walco van Loon",
      author_email = "walco at n--tree.net",
      url='http://walco.n--tree.net/aksy',
	  ext_modules=[
         Extension("aksyxusb",
                sources = [ "src/aksyx/aksyxusb.c", "src/aksyx/akaiusb.c" ],
                define_macros=[('_DEBUG', '1'),],
                libraries = [ "akaiusb" ],
            ),
       ])
