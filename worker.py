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
        
    def getAndClearResults(self, uid):
        if uid in self.results:
            res = self.results[uid]
            del self.results[uid]
            return res
        return None
        
multiprocessing.freeze_support()

if(__name__ == "__main__"):    
    wp = WorkerPool()
    while(not wp.push("dieter")):
        time.sleep(0.1)
    while(not wp.push("eva")):
        time.sleep(0.1)
    while(not wp.push("rudolf")):
        time.sleep(0.1)
    while(not wp.push("heinz")):
        time.sleep(0.1)
    while(not wp.push("gisela")):
        time.sleep(0.1)
    while(not wp.push("hans")):
        time.sleep(0.1)
    while(not wp.push("peter")):
        time.sleep(0.1)
    while(not wp.push("rudi")):
        time.sleep(0.1)
    while(not wp.push("angela")):
        time.sleep(0.1)
    while(not wp.push("peer")):
        time.sleep(0.1)
    time.sleep(1000)