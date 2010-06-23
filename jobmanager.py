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
        
class JobManagerdownlink:
    _ip = "";
    _port = 0;  
    running = 1
    
    def stop(self):
        self.running = 0
    
    def setup(self):
        self._ip = self.client_address[0]
        self._port = self.client_address[1]
        self.__connection = self.request   
        SystemBorg().get("msgsys").call("addclient", [self.client_address, self.stop])
            
class JobManagerTcpDownlink(JobManagerdownlink):            
    def handle(self):
        jq = SystemBorg().get("JobQueue") 
        self.client_idle = 0  
        self.finished = 0 
        while(1):
            raw = self.request.recv(8)
            if(not raw):
                return;
            packet_size = struct.unpack('Q', raw)[0];
            if(packet_size == 0):
                return;
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
                SystemBorg().get("msgsys").call("delclient", self.client_address)
                return 1    
            elif(type(rcv_obj).__name__ == 'StatusPacket'):
                if(rcv_obj.getStatus() == "IDLE"):
                    self.client_idle = 1  
            elif(type(rcv_obj).__name__ == 'LargeDebugPacket'):
                print("LargeDebugPacket recieved! size = " + str(len(buffer)))
            elif(type(rcv_obj).__name__ == 'NullObject'):
                pass
            elif(type(rcv_obj).__name__ == 'NullResult'):
                print(rcv_obj.resulttext)
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
                        self.send(nextjob)
                    else: # self.running must be 0
                        if(not self.finished):
                            self.finished = 1
                            print("send goodbye");
                            self.send(GoodbyePacket())
            time.sleep(0.1)
          
    def send(self, data):
        self.client_idle = 0
        picklestring = pickle.dumps(data)     
        self.request.send(struct.pack('Q', len(picklestring)))
        self.request.send(picklestring)
            
class JobManagerUplink:
    _ip = ""
    _port = 0
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port    
        self._connect()  
        self._jobspending = {}
         
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
            raw = self._sock.recv(8) 
            if(not raw):
                return;
            packet_size = struct.unpack('Q', raw)[0];
            if(packet_size == 0):
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
            elif(type(rcv_obj).__name__ == 'NullObject'):
                pass
            else: # assume it's a subclass of JobObject
                job_obj = rcv_obj
                job_obj.loadDependencies()
                self._jobspending[job_obj.uid] = job_obj
                #job_obj.process(self.jobDone)
                wp.push(job_obj)
            while(wp.isFullyBusy()):
                time.sleep(0.1)
            dellist = []
            
            for x in self._jobspending:
                ret_obj = wp.getAndClearResult(x)
                if(ret_obj):
                    self.send(ret_obj)
                    dellist.append(x)
            for x in dellist:
                del self._jobspending[x]
            print("pending " + str(len(self._jobspending)))
            self.send(StatusPacket("IDLE"))
            time.sleep(0.1)    
        
class JobManagerTcpUplink(JobManagerUplink):
    _sock = ()   
    def __init__(self, ip, port):
        JobManagerUplink.__init__(self, ip, port)
        
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        self._sock.connect((self._ip, self._port))
        
    def _disconnect(self):
        self._sock.close()  
        
    def send(self, data):
        picklestring = pickle.dumps(data) 
        self._sock.send(struct.pack('Q', len(picklestring)))
        self._sock.send(picklestring)

class JobManager(object):
    """
    Borg singleton job manager
    """
    __we_are_one = {}
    __uplink = ()
    __downlink = {}

    def __init__(self):
        self.__dict__ = self.__we_are_one
        
    def registerUplink(self, connection):
        if(self.__uplink or not (connection)):
            return 0;
        else:
            self.__uplink = connection
            return 1;       
        
    def unregisterUplink(self):
        if(not self.__uplink):
            return 0;
        else:
            del self.__uplink
            return 1;          
        
    def registerDownlink(self, ip, port, connection):
        address = ip + ":" + str(port)
        if(address in self.__downlink):
            return 0;
        else:
            self.__downlink[address] = connection
            return 1;       
        
    def unregisterDownlink(self, ip, port, address):  
        address = ip + ":" + str(port)
        if(not address in self.__downlink):
            return 0;
        else:
            del self.__downlink[address]
            return 1;      
            
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
    DataBorg().registerUplink(DataBorgTcpUplink("127.0.0.1", 12214))    
    jobmgr = JobManager()    
    jobmgr.registerUplink(JobManagerTcpUplink("127.0.0.1", 12213))
    jobmgr.wait() 