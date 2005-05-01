#!/usr/bin/env python
"""Aksy setup module
"""
from distutils.core import setup, Extension
from distutils.command import bdist_wininst
setup(name = "aksyx usb extension",
      version = "0.01",
      author = "Walco van Loon",
      author_email = "walco at n--tree.net",
      url='http://walco.n--tree.net/projects/aksy',
	  ext_modules=[
         Extension("aksyxusb",
                sources = [ "src/aksyx/aksyxusb.c", "src/aksyx/akaiusb.c" ],
                define_macros=[('_DEBUG', '1'),],
                libraries = [ "akaiusb" ],
            ),
       ])
