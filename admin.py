import pickle          
import socket
import socketserver
import time
import hashlib
import struct
from jobqueue import *
from systemborg import *

class AdminResponse:
    def __init__(self, msg, number):
        self.msg = msg
        self.number = number
        
class AdminDownlink:
    _ip = "";
    _port = 0;  
    running = 1
    
    def stop(self):
        self.request.shutdown(socket.SHUT_WR)
    
    def setup(self):
        self._ip = self.client_address[0]
        self._port = self.client_address[1]
        self.__connection = self.request   
        
    def finish(self):
        pass
            
class AdminTcpDownUplink(AdminDownlink):            
    def handle(self):
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
                return 1
            elif(type(rcv_obj).__name__ == 'NullObject'):
                pass
            else: # assume it's a subclass of JobObject
                jq = SystemBorg().get("JobQueue") 
                num = jq.push(rcv_obj)
                self.send(AdminResponse("OK", num))
                
          
    def send(self, data):
        picklestring = pickle.dumps(data)     
        self.request.send(struct.pack('Q', len(picklestring)))
        self.request.send(picklestring)
            
class AdminUplink:
    _ip = ""
    _port = 0
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port    
        self._connect()  
         
    def __del__(self):
        self._disconnect()
        
    def _connect(self):
        return
        
    def _disconnect(self):
        return   
        
    def send(self, data):
        pass
        
    def getResponse(self):             
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
        if(type(rcv_obj).__name__ == 'AdminResponse'):
            return rcv_obj.number
        
class AdminTcpUplink(AdminUplink):
    _sock = ()   
    def __init__(self, ip, port):
        AdminUplink.__init__(self, ip, port)
        
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        self._sock.connect((self._ip, self._port))
        
    def _disconnect(self):
        self._sock.close()  
        
    def send(self, data):
        picklestring = pickle.dumps(data) 
        self._sock.send(struct.pack('Q', len(picklestring)))
        self._sock.send(picklestring)

class adminmodule():
    def __init__(self, ip, port):
        self.__uplink = AdminTcpUplink(ip, port)
                 
    def send(self, packet):
        if(self.__uplink):
            self.__uplink.send(packet)
            self.__uplink.getResponse()
            
if(__name__ == "__main__"):
    admin = adminmodule("127.0.0.1", 12215)  
    admin.send(DebugJobObject("test1"))           
    admin.send(DebugJobObject("test2"))           
    admin.send(DebugJobObject("test3"))           
    admin.send(DebugJobObject("test4"))           
    admin.send(DebugJobObject("test5"))           
    admin.send(DebugJobObject("test6"))           
    admin.send(DebugJobObject("test7"))         
    admin.send(DebugJobObject("test8"))           
    admin.send(DebugJobObject("test9"))           
    admin.send(DebugJobObject("testa"))           
    admin.send(DebugJobObject("testb"))           
    admin.send(DebugJobObject("testc"))           
    admin.send(DebugJobObject("testd"))           
    admin.send(DebugJobObject("teste"))      
    admin.send(DebugJobObject("test11"))           
    admin.send(DebugJobObject("test12"))           
    admin.send(DebugJobObject("test13"))           
    admin.send(DebugJobObject("test14"))           
    admin.send(DebugJobObject("test15"))           
    admin.send(DebugJobObject("test16"))           
    admin.send(DebugJobObject("test17"))         
    admin.send(DebugJobObject("test18"))           
    admin.send(DebugJobObject("test19"))           
    admin.send(DebugJobObject("test1a"))           
    admin.send(DebugJobObject("test1b"))           
    admin.send(DebugJobObject("test1c"))           
    admin.send(DebugJobObject("test1d"))           
    admin.send(DebugJobObject("test1e"))   
    admin.send(DebugJobObject("test21"))           
    admin.send(DebugJobObject("test22"))           
    admin.send(DebugJobObject("test23"))           
    admin.send(DebugJobObject("test24"))           
    admin.send(DebugJobObject("test25"))           
    admin.send(DebugJobObject("test26"))           
    admin.send(DebugJobObject("test27"))         
    admin.send(DebugJobObject("test28"))           
    admin.send(DebugJobObject("test29"))           
    admin.send(DebugJobObject("test2a"))           
    admin.send(DebugJobObject("test2b"))           
    admin.send(DebugJobObject("test2c"))           
    admin.send(DebugJobObject("test2d"))           
    admin.send(DebugJobObject("test2e"))          