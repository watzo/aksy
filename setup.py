#!/usr/bin/env python

from distutils.core import setup,Extension

setup(name = "aksy usb extension",
      version = "0.01",
      author = "Walco van Loon",
      author_email = "walco@n--tree.net",
	  ext_modules=[
            Extension("aksyxusb",
                sources = [ "src/aksyxusb.c" ],
                libraries = [ "usb" ],
            ),
        ])
