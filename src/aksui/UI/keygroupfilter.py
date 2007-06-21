import ak,UI

class KeygroupFilter(UI.Base):
    def __init__(self, keygroup):
        UI.Base.__init__(self, keygroup, "tableFilter")