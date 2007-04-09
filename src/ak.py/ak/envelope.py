import gobject,gtk,aksy

from ak import *
from samplerobject import samplerobject

class envelope(samplerobject):
    def __init__(self,keygroup,index,xoffset=10,yoffset=10):
        samplerobject.__init__(self, keygroup.s, keygroup, "keygrouptools", index)
        self.set_envelope(self.parent, index)
        self.xoffset = xoffset
        self.yoffset = yoffset 
        self.set_envelope(keygroup,index)

    def update(self):
        kgt = self.s.keygrouptools
        index = self.index
        # attack
        self.rate1 = int(kgt.get_envelope_rate1(index))
        # decay
        self.rate2 = int(kgt.get_envelope_rate2(index))
        # sustain
        self.level2 = int(kgt.get_envelope_level2(index))
        # release
        self.rate3 = int(kgt.get_envelope_rate3(index))

        if index != 0:
            self.level1 = int(kgt.get_envelope_level1(index))
            self.level3 = int(kgt.get_envelope_level3(index))
            self.rate4 = int(kgt.get_envelope_rate4(index))
            self.level4 = int(kgt.get_envelope_level4(index))
            self.reference = int(kgt.get_envelope_reference(index))
        else:
            self.level1 = 0
            self.level3 = 0
            self.rate4 = 0
            self.level4 = 0
            self.reference = 0

    def updateNode(self, nodeIndex, x, y):
        x = x - self.xoffset
        y = y - self.yoffset

        rate1 = self.rate1
        level1 = self.level1
        rate2 = self.rate2
        level2 = self.level2
        rate3 = self.rate3
        level3 = self.level3
        rate4 = self.rate4
        level4 = self.level4

        kgt = self.s.keygrouptools

        if y > 100:
            y = 100
        if y < 0:
            y = 0

        if nodeIndex == 0:
            if x > 100:
                x = 100
            if x < 0:
                x = 0

            if x <= 100 and x >= 0:
                self.rate1 = x
                if self.rate1 != rate1:
                    kgt.set_envelope_rate1(self.index, self.rate1) 
            if self.index > 0:
                if self.level1 != level1:
                    if y >= 0 and y <= 100:
                        self.level1 = 100 - y
                        kgt.set_envelope_level1(self.index, self.level1) 
        if nodeIndex == 1:
            if x < self.rate1:
                x = self.rate1
            if x - self.rate1 > 100:
                x = self.rate1 + 100

            if(x >= self.rate1 and (x - self.rate1) <= 100):
                self.rate2 = x - self.rate1
                if self.rate2 != rate2:
                    kgt.set_envelope_rate2(self.index, self.rate2) 
            if y >= 0 and y <= 100:
                self.level2 = 100 - y
                if self.level2 != level2:
                    kgt.set_envelope_level2(self.index,self.level2) 
        elif nodeIndex == 2:
            if x < self.rate1 + self.rate2:
                x = self.rate1 + self.rate2
            if x - self.rate1 - self.rate2 > 100:
                x = self.rate1 + self.rate2 + 100

            if(x >= (self.rate1 + self.rate2) and (x - self.rate1 - self.rate2) <= 100):
                self.rate3 = x - self.rate2 - self.rate1
                if self.rate3 != rate3:
                    kgt.set_envelope_rate3(self.index,self.rate3) 
            if self.index > 0:
                if y >= 0 and y <= 100:
                    self.level3 = 100 - y
                    if self.level3 != level3:
                        kgt.set_envelope_level3(self.index,self.level3) 
        elif nodeIndex == 3 and self.index > 0:
            if x < self.rate1 + self.rate2 + self.rate3:
                x = self.rate1 + self.rate2 + self.rate3
            if x - self.rate1 - self.rate2  - self.rate3 > 100:
                x = self.rate1 + self.rate2 + self.rate3 + 100
            if(x >= (self.rate1 + self.rate2 + self.rate3) and (x - self.rate1 - self.rate2 - self.rate3) <= 100):
                self.rate4 = x - self.rate3 - self.rate2 - self.rate1
                if self.rate4 != rate4:
                    kgt.set_envelope_rate4(self.index,self.rate4) 
                if y >= 0 and y <= 100:
                    self.level4 = 100 - y
                    if self.level4 != level4:
                        kgt.set_envelope_level4(self.index,self.level4) 

    def set_envelope(self, keygroup, index):
        self.keygroup = keygroup
        self.index = index 
        self.update()

