import base

class KeygroupDetails(base.Base):
    def __init__(self, keygroup):
        base.Base.__init__(self, keygroup, "tableKeygroupDetails")