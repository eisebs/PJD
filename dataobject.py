class DataObject:
    def __init__(self, object):
        self.__revision = 0
        self.__md5 = None
        self.set(object)
    
    def set(self, value):
        self.__revision = self.__revision + 1
        self.__data = value   
        if(type(self.__data) == type("")): 
          self.__md5 = hashlib.md5(self.__data.encode()).hexdigest()
        else:
          self.__md5 = hashlib.md5(self.__data).hexdigest()
        self.isValid = 1
        
    def get(self):
        return self.__data      
        
    def getRev(self):
        return self.__revision  
        
    def getMd5(self):
        return self.__md5 
          
    def preDataborgSend(self):
        pass
          
    def postDataborgSend(self):
        pass
          
    def postDataborgReceive(self):
        pass

class DebugLargeDataObject(DataObject): 
    def __init__(self, object):
        self.bigstring = "10"
        for x in range(24):
            self.bigstring = self.bigstring + self.bigstring
        DataObject.__init__(self, object)