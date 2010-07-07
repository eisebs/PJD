import threading
from databorg import *

class NullResult:
    def __init__(self):
        self.uid = -1
        self.result = None
        self.resulttext = ""
    pass
    
class DependencySet:
    def __init__(self, name, md5, data):
        self.name = name
        self.resolvedName = name
        self.md5 = md5
        self.data = data
    
class ResultSet:
    def __init__(self, name, data):
        self.name = name
        self.resolvedName = name
        self.data = data

class JobObject:
    uid = -1
    def __init__(self):
        self.__dependencies = []
        self.__results = []
        self.__valid = 1
        self.__resultsObject = NullResult()
        pass
    def addDependency(self, dep, md5):
        self.__dependencies.append(DependencySet(dep, md5, None))
    def addResult(self, key, target):
        self.__results.append(ResultSet(key, target))
    def getDependencies(self):
        return self.__dependencies
    def getResults(self):
        return self.__results
    def loadDependencies(self):
        for x in self.__dependencies:
            print("x.resolvedName = " + x.resolvedName)
            if(not DataBorg().hasValueMd5(x.resolvedName, x.md5)):
                self.valid = 0
                return
            x.data = DataBorg().getValue(x.resolvedName)
            x.md5 = x.data.getMd5()
    def resolvePaths(self):
        for x in self.getDependencies():
            x.resolvedName = DataBorg().resolveDataPath(x.name[5:])
        for x in self.getResults():
            x.resolvedName  = DataBorg().resolveDataPath(x.name[5:])
    def process(self):
        if(self.__valid):
            self.__valid = self.doJob()
        return self.__valid
    def addResults(self, resultSet):
        return self.__results.append(resultSet)
    def getResults(self):
        return self.__results
    def getResultsObject(self):
        return self.__resultsObject
    def setResultsObject(self, resultsObject):
        self.__resultsObject = resultsObject
    def getIsValid(self):
        return self.__valid
        
#class DebugJobObject(JobObject):
#    def __init__(self, name):
#        self.name = name
#        JobObject.__init__(self)
#        do = DataObject("teststring")
#        self.addDependency("testobject", do.getMd5())
#    def doJob(self):
#        if(self.getIsValid()):
#            pass
#            #print("job object " + self.name + " is valid")
#        else:
#            pass
#            #print("job object " + self.name + " is invalid")
#        print("dependencies:")
#        for x in self.getDependencies():
#            pass
#            #print(x.name, x.md5)     
#        #print("working hard")
#        self.i = 0
#        for x in range(0, 10000000):
#            self.i = self.i + 1
#        self.result.uid = self.uid
#        self.result.resulttext = "multiprocessing processed job " + str(self.uid)

class ImageResizeJobResult(NullResult):
    def __init__(self, uid, result):
        self.uid = uid
        self.result = result
        self.resulttext = ""
    pass        
        
class ImageResizeJobObject(JobObject):
    def __init__(self, source, target, factor):
        JobObject.__init__(self)
        self.__source = source
        self.__target = target
        self.__factor = factor
        sourceObject = FileDataObject(self.__source)
        self.addDependency(sourceObject.getKey(), sourceObject.getMd5())
        targetObject = FileDataObject(self.__target)
        self.addResult(targetObject.getKey(), targetObject)
    def doJob(self):
        print("ImageResizeJobObject.doJob")
        source = self.getDependencies()[0].resolvedName
        resolvedTargetName = self.getResults()[0].resolvedName
        print(source + " -> " + resolvedTargetName)
        commandstring = "i_view32 " + source + "/resize=(640) /aspectratio /convert " + resolvedTargetName
        print(commandstring)
        os.system(commandstring)
    def getResultsObject(self):
        target = self.getResults()[0]
        targetName = target.name
        target.data.uid = self.uid
        target.data.resulttext = "multiprocessing processed job " + str(self.uid)
        print("FileDataObject(" + targetName + ")")
        target.data.object = FileDataObject(targetName)
        self.setResultsObject(ImageResizeJobResult(self.uid, target))
        return JobObject.getResultsObject(self)
    
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
    def getObj(self):
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
    def pushLostJobsInFront(self, jobmap):
        self.lock.acquire()
        seq = []
        for x in jobmap:
            seq.append(x)
        for x in reversed(seq):
            print("re-enqueuing job #" + str(jobmap[x].uid))
            newobj = JobQueueObject(jobmap[x])
            newobj.setNext(self.__first)
            self.__first = newobj
        j = self.__first
        jobs = ""
        while(j):
            jobs = jobs + str(j.getObj().uid) + ", "
            j = j.getNext()
        print(jobs)
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
        return obj.getObj()	

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
        obj.getResultsObject()
        obj = jq.pop()