
class Samples:
    def __init__(self,s):
        self.s = s
        st = s.sampletools
        self.allsamples = st.get_names()
