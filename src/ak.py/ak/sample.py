from aksy.device import Devices
from utils.modelutils import *

allsamples = { }

class samples:
    def __init__(self,s):
        self.s = s
        st = s.sampletools
        self.allsamples = st.get_names()
