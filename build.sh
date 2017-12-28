virtualenv buildenv
pip install pysendfile
rm -r build/*
export PATH=buildenv/bin:$PATH
python setup.py install
