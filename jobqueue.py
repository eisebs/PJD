import threading
from databorg import *

class NullResult:
    def __init__(self):
        self.resulttext = ""
    pass
    
class DependencySet:
    def __init__(self, name, md5, data):
        self.name = name
        self.md5 = md5
        self.data = data

class JobObject:
    uid = -1
    def __init__(self):
        self.__dependencies = []
        self.__valid = 1
        self.result = NullResult()
        pass
    def addDependency(self, dep, md5):
        self.__dependencies.append(DependencySet(dep, md5, None))
    def getDependencies(self):
        return self.__dependencies
    def loadDependencies(self):
        for x in self.__dependencies:
            if(not DataBorg().hasValueMd5(x.name, x.md5)):
                self.valid = 0
                return
            x.data = DataBorg().getValue(x.name)
            x.md5 = x.data.getMd5()
    def process(self):
        if(self.__valid):
            self.__valid = self.doJob()
        return self.__valid
    def getResult(self):
        return self.result
    def getIsValid(self):
        return self.__valid
        
class DebugJobObject(JobObject):
    def __init__(self, name):
        self.name = name
        JobObject.__init__(self)
        do = DataObject("teststring")
        self.addDependency("testobject", do.getMd5())
    def doJob(self):
        if(self.getIsValid()):
            pass
            #print("job object " + self.name + " is valid")
        else:
            pass
            #print("job object " + self.name + " is invalid")
        print("dependencies:")
        for x in self.getDependencies():
            pass
            #print(x.name, x.md5)     
        #print("working hard")
        self.i = 0
        for x in range(0, 10000000):
            self.i = self.i + 1
        self.result.resulttext = "multiprocessing processed job " + str(self.uid)
    
class JobQueueObject:
    def __init__(self, object, last = None):
        self.__object = object
        self.__next = None
        if(last):
          last.setNext(self)
    def setNext(self, next):
        self.__next = next
    def getNext(self):
        return self.__next  
    def getobj(self):
        return self.__object
    
class JobQueue:
    uid = 0
    def __init__(self):
        self.__first = ()
        self.__last = ()
        self.__numjobs = 0	
        self.lock = threading.Lock()	
    def push(self, object):
        object.uid = JobQueue.uid
        JobQueue.uid = JobQueue.uid + 1
        print("UID: " + str(object.uid))
        self.__numjobs = self.__numjobs + 1
        self.lock.acquire()
        newobj = JobQueueObject(object, self.__last)
        if(not self.__first):
            self.__first = newobj       
        self.__last = newobj
        self.lock.release()
        return self.__numjobs
    def pop(self):
        if(not self.__first):
            return None            
        self.__numjobs = self.__numjobs - 1  
        self.lock.acquire()
        obj = self.__first
        self.__first = self.__first.getNext() 
        self.lock.release()
        return obj.getobj()	

if(__name__ == "__main__"):
    jq = JobQueue()
    jo1 = DebugJobObject("test1")  
    jo2 = DebugJobObject("test2")  
    jq.push(jo1)      
    jq.push(jo2)
    obj = jq.pop()   
    while(obj):
        obj.getDependencies()
        obj.process()
        obj.getResult()
        obj = jq.pop()