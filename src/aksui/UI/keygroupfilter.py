import base

class KeygroupFilter(base.Base):
    def __init__(self, keygroup):
        base.Base.__init__(self, keygroup, "tableFilter")