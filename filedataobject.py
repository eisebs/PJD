from databorg import *
from dataobject import *

class FileDataObject(DataObject): 
    def __init__(self, key):
        self.__revision = 0
        self.__md5 = None
        self.data = "test"
        DataObject.__init__(self, key)
        
    def initialize(self, key):
        self.__key = key
        if(not(key[0:5] == "FILE:")):
            return 0
        self.__path = self.findFile(key)
        if(not self.__path):
            return 0
        self.__md5 = hashlib.md5(self.loadFile(self.__path)).hexdigest()
        print("file md5 = " + self.__md5)
        return 1

    def loadFile(self, path):
        print("loading " + path)
        fileReader = open(path, mode='rb')
        fileContent = fileReader.read()
        fileReader.flush()
        print("read contents of " + path)
        return fileContent

    def saveFile(self, path, content):
        print("saving " + path)
        if(os.path.exists(path)):
            return 0
        fileWriter = open(path, mode="wb")
        fileWriter.write(content)
        fileWriter.flush()
        print("done.")
        return 1

    def findFile(self, path):
        path = path[5:] # cut FILE:
        path = DataBorg().resolveDataPath(path)
        if(os.path.exists(path)):
            print(path + " found!")
            return path
        print(path + " not found!")
        return 0

    def findSaveFile(self, path):
        path = path[5:] # cut FILE:
        print("findSaveFile key: " + path)
        path = DataBorg().resolveDataPath(path)
        if(not os.path.exists(path)):
            return path
        return 0
    
    def set(self, value):
        self.__data = value   
        if(type(value) == type("")): 
            self.isValid = self.initialize(value)
        else:
          self.saveFile(self.__path, value)
          
    def preDataborgSend(self):
        self.data = self.loadFile(self.__path)
          
    def postDataborgSend(self):
        self.data = None
          
    def postDataborgReceive(self):
        self.__path = self.findSaveFile(self.__key)
        if(self.__path):
            self.saveFile(self.__path, self.data)
        self.data = None
        
    def get(self):
        return self.__data    
        
    def getRev(self):
        return DataObject.getRev(self)  
        
    def getMd5(self):
        return self.__md5
        
    def getKey(self):
        return self.__key