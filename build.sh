virtualenv buildenv
rm -r build/*
export PATH=buildenv/bin:$PATH
python setup.py install
