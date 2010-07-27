import multiprocessing
import time
from systemborg import *

def doJob(job):
    job.process()
    return job
            
def done(joblist):
    import systemborg
    job = joblist[0]
    wp = systemborg.SystemBorg().get("WorkerPool")
    print("worker completed " + str(job.uid))
    wp.busythreads = wp.busythreads - 1
    wp.idlethreads = wp.idlethreads + 1
    wp.results[job.uid] = job.getResultsObject()

class WorkerPool:
    def __init__(self):
        self.cpucount = multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(self.cpucount)
        self.busythreads = 0
        self.idlethreads = self.cpucount
        self.results = {}
        
    def push(self, job):
        if(self.idlethreads == 0):
            return 0
        self.busythreads = self.busythreads + 1
        self.idlethreads = self.idlethreads - 1
        self.joblist = [job]
        self.pool.map_async(doJob, self.joblist, callback=done)
        return 1
        
    def isFullyBusy(self):
        return (self.idlethreads == 0)
        
    def getResults(self, uid):
        if uid in self.results:
            res = self.results[uid]
            return res
        return None
        
    def clearResults(self, uid):
        if uid in self.results:
            del self.results[uid]
        return None
        
multiprocessing.freeze_support()