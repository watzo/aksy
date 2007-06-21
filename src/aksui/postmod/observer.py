

# note: it's not necessary to actually derive from Observer.
# a class just needs an "update" method to be an observer.
class Observer:
    def __init__(self):
        pass
                        
    def update(self, subject):  
        pass               
                
class Subject:
    def __init__(self):        
        self._observers = []
        
    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)
        
    def detach(self, observer): 
        try:
            self._observers.remove(observer)
        except:
            pass
            
    def notify(self, modifier=None):
        for observer in self._observers:            
            if modifier != observer:
                observer.update(self)


# Example usage
class Data(Subject):
    def __init__(self, name=''):
        Subject.__init__(self)
        self.name = name
        self.data = 0

    def setData(self, data):
        self.data = data
        self.notify()
        
    def getData(self):
        return self.data              
            
    
class HexViewer(Observer):
    def __init__(self):
        Observer.__init__(self)
        
    def update(self, subject):        
        print 'HexViewer: Subject %s has data 0x%x' % (subject.name, subject.getData())
                
                
class DecimalViewer(Observer):
    def __init__(self):
        Observer.__init__(self)
        
    def update(self, subject):        
        print 'DecimalViewer: Subject %s has data %d' % (subject.name, subject.getData())
        

# Example usage...
def main():
    data1 = Data('Data 1')
    data2 = Data('Data 2')
    view1 = DecimalViewer()
    view2 = HexViewer()
    data1.attach(view1)
    data1.attach(view2)
    data2.attach(view2)
    data2.attach(view1)
    
    print "Setting Data 1"
    data1.setData(10)
    print "Setting Data 2"
    data2.setData(15)
    print "Setting Data 1"
    data1.setData(3)
    print "Setting Data 2"
    data2.setData(5)
 
if __name__ == '__main__':
    main()     
