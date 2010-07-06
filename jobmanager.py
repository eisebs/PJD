import pickle          
import socket
import socketserver
import time
import hashlib
import struct
from jobqueue import *
from systemborg import *

class GoodbyePacket:
    pass     

class StatusPacket:
    def __init__(self, status):
        self.__status = status
    def getStatus(self):
        return self.__status   

class LargeDebugPacket:
    def __init__(self):
        self.bigstring = "10"
        for x in range(24):
            self.bigstring = self.bigstring + self.bigstring
        
class JobManagerdownlink(threading.Thread):
    _ip = ""
    _port = 0
    running = 1
    polljobs = 1
    finished = 0
    client_idle = 0
    
    def handle(self):
        threading.Thread.__init__( self )
            
    def run(self):
        self.pollJobs()
    
    def stopDownlink(self):
        self.running = 0
    
    def setup(self):
        self._ip = self.client_address[0]
        self._port = self.client_address[1]
        self.__connection = self.request   
        SystemBorg().get("msgsys").call("addclient", [self.client_address, self.stopDownlink])
            
class JobManagerTcpDownlink(JobManagerdownlink): 
    def handle(self):
        JobManagerdownlink.handle( self )
        self.locallock = threading.Lock()
        self.sendlock = threading.Lock()
        self._jobspending = {}
        self.start()
        jq = SystemBorg().get("JobQueue") 
        while(1):
            raw = 0
            try:
                raw = self.request.recv(8)
            except:
                pass
            if(not raw):
                self.endHandle()
                return 0
            packet_size = struct.unpack('Q', raw)[0];
            if(packet_size == 0):
                self.endHandle()
                return 0
            total_data = []
            total_data_size = 0
            while(total_data_size < packet_size):
                rest_size = packet_size - total_data_size
                received = self.request.recv(rest_size);
                total_data_size = total_data_size + len(received) 
                total_data.append(received)
            buffer = bytes().join(total_data)   
            rcv_obj = pickle.loads(buffer)
            if(type(rcv_obj).__name__ == 'GoodbyePacket'):
                print("got a goodbye packet")
                self.endHandle()
                return 1
            elif(type(rcv_obj).__name__ == 'StatusPacket'):
                if(rcv_obj.getStatus() == "IDLE"):
                    self.client_idle = 1  
            elif(type(rcv_obj).__name__ == 'LargeDebugPacket'):
                print("LargeDebugPacket recieved! size = " + str(len(buffer)))
            elif(type(rcv_obj).__name__ == 'NullObject'):
                pass
            else: # assume it's a subclass of nullresult
                self.locallock.acquire()
                del self._jobspending[rcv_obj.uid]
                self.locallock.release()
                print(rcv_obj.resulttext + ", " + str(len(self._jobspending)) + " jobs pending")
            time.sleep(0.1)
    
    def endHandle(self):
        jq = SystemBorg().get("JobQueue") 
        SystemBorg().get("msgsys").call("delclient", self.client_address)
        self.polljobs = 0
        jq.pushLostJobsInFront(self._jobspending)
            
    def pollJobs(self):
        jq = SystemBorg().get("JobQueue") 
        while(self.polljobs):
            if(self.client_idle):
                if(not self.running and not self.finished):
                    self.finished = 1
                    print("send goodbye");
                    self.send(GoodbyePacket())
                else:
                    nextjob = 0
                    while(self.running and not nextjob):
                        nextjob = jq.pop()
                        time.sleep(0.1)
                    if(nextjob):
                        self.locallock.acquire()
                        self._jobspending[nextjob.uid] = nextjob
                        self.sendjob(nextjob)
                        self.locallock.release()
                    else: # self.running must be 0
                        if(not self.finished):
                            self.finished = 1
                            print("send goodbye");
                            self.send(GoodbyePacket())
            time.sleep(0.1)
            
    def sendjob(self, data):
        self.client_idle = 0
        self.send(data)
          
    def send(self, data):
        self.sendlock.acquire()
        picklestring = pickle.dumps(data)
        try:
            self.request.send(struct.pack('Q', len(picklestring)))
            self.request.send(picklestring)
        except:
            pass
        self.sendlock.release()
            
class JobManagerUplink(threading.Thread):
    _ip = ""
    _port = 0
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port    
        self._connect()  
        self._jobspending = {}
        self.running = 1;
        self.received = 0
        self.locallock = threading.Lock()
        threading.Thread.__init__( self )
         
    def __del__(self):
        self._disconnect()
        
    def _connect(self):
        return
        
    def _disconnect(self):
        return   
        
    def send(self, data):
        pass
        
    def wait(self):
        self.send(StatusPacket("IDLE"))
        wp = SystemBorg().get("WorkerPool")
        while(1):
            raw = 0
            try:      
                raw = self._sock.recv(8) 
            except:
                pass
            if(not raw):
                print("connection lost!")
                self.running = 0
                return;
            packet_size = struct.unpack('Q', raw)[0];
            if(packet_size == 0):
                self.running = 0
                return;
            total_data = []
            total_data_size = 0
            while(total_data_size < packet_size):
                rest_size = packet_size - total_data_size
                received = self._sock.recv(rest_size);
                total_data_size = total_data_size + len(received) 
                total_data.append(received)
            buffer = bytes().join(total_data)   
            rcv_obj = pickle.loads(buffer)     
            print(type(rcv_obj).__name__)
            if(type(rcv_obj).__name__ == 'NoneType'):
                pass
            elif(type(rcv_obj).__name__ == 'GoodbyePacket'):
                print("send goodbye")
                self.send(GoodbyePacket())
                self.running = 0
                self.join()
            elif(type(rcv_obj).__name__ == 'NullObject'):
                pass
            else: # assume it's a subclass of JobObject
                job_obj = rcv_obj
                job_obj.loadDependencies()
                self.locallock.acquire()
                self._jobspending[job_obj.uid] = job_obj
                self.received = 1
                #job_obj.process(self.jobDone)
                wp.push(job_obj)
                self.locallock.release()
            #while(wp.isFullyBusy()):
                time.sleep(0.1)
            #if(self.running):
            #    self.send(StatusPacket("IDLE"))
                
    def run(self):
        self.pollWorkerPool()
            
    def pollWorkerPool(self):
        wp = SystemBorg().get("WorkerPool")
        while(1):
            if(not self.running):
                print("exiting pollWorkerPool")
                return
            if(self.running and self.received and not wp.isFullyBusy()):
                self.received = 0
                self.send(StatusPacket("IDLE"))
            dellist = []
            for x in self._jobspending:
                self.locallock.acquire()
                ret_obj = wp.getAndClearResult(x)
                self.locallock.release()
                if(ret_obj):
                    print("sending " + ret_obj.resulttext)
                    self.send(ret_obj)
                    dellist.append(x)
            for x in dellist:
                self.locallock.acquire()
                del self._jobspending[x]
                self.locallock.release()
            time.sleep(0.1)              
        
class JobManagerTcpUplink(JobManagerUplink):
    _sock = ()   
    def __init__(self, ip, port):
        self.sendlock = threading.Lock()
        JobManagerUplink.__init__(self, ip, port)
        
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        self._sock.connect((self._ip, self._port))
        
    def _disconnect(self):
        self._sock.close()
        
    def send(self, data):
        self.sendlock.acquire()
        picklestring = pickle.dumps(data) 
        try:
            self._sock.send(struct.pack('Q', len(picklestring)))
            self._sock.send(picklestring)
        except:
            pass
        self.sendlock.release()

class JobManager(object):
    """
    Borg singleton job manager
    """
    __we_are_one = {}
    __uplink = ()
    __downlink = {}

    def __init__(self):
        self.__dict__ = self.__we_are_one
        
    def setUplink(self, connection):
        self.__uplink = connection         
        
    def setDownlink(self, ip, port):
        if(ip and port):
            address = ip + ":" + str(port)
            self.__downlink[address] = address
        else:
            self.__downlink[address] = None 
            
    def sendStatus(self, status):
        if(self.__uplink):
            self.__uplink.send(StatusPacket(status))
            
    def send(self, packet):
        if(self.__uplink):
            self.__uplink.send(packet)
            
    def wait(self):
        if(self.__uplink):
            self.__uplink.wait()
            
if(__name__ == "__main__"):
    SystemBorg().initWorkerPool()
    DataBorg().setUplink(DataBorgTcpUplink("127.0.0.1", 12214))   
    DataBorg().setDataPath("D:/temp/input", "fotos")    
    DataBorg().setDataPath("D:/temp/output", "output")    
    jobmgr = JobManager()    
    uplink = JobManagerTcpUplink("127.0.0.1", 12213)
    jobmgr.setUplink(uplink)
    uplink.start()
    jobmgr.wait() 