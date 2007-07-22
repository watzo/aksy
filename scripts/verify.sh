#!/bin/sh
rm -r dist
python setup.py sdist
cd dist
tar xfz aksy-*.tar.gz
cd aksy-*
stat LICENSE.txt
less INSTALL.txt
python setup.py build

