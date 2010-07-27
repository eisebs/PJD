import threading
from databorg import *
  
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