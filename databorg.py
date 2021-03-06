import pickle          
import socket
import socketserver
import time
import hashlib
import threading        
import struct
import os

def normpath(path):
    path = os.path.abspath(path)
    path.replace("\\\\", "\\")
    return path

class NullObject:
    null = 0      

class UptodateObject:
    null = 0  
        
class RequestObject:
    def __init__(self, key, md5):
        self.key = key    
        self.md5 = md5
        
class DataBorgUplink:
    _ip = ""
    _port = 0
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port    
         
    def __del__(self):
        self._disconnect()
        
    def _connect(self):
        pass
        
    def _disconnect(self):
        pass 
        
    def send(self, data):
        pass    
        
    def ask(self, request, md5):
        self._connect()  
        rq = RequestObject(request, md5)
        self.send(rq)
        answered = 0
        while(not answered):
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
            if(type(rcv_obj).__name__ == 'NullObject'): 
                return 0 
            elif(type(rcv_obj).__name__ == 'UptodateObject'): 
                return 1
            else: # assume it's a data object
                print("got a " + type(rcv_obj).__name__)
                DataBorg().setValue(request, rcv_obj)
                rcv_obj.postDataborgReceive()
                return 1
            time.sleep(0.01)
        
class DataBorgTcpUplink(DataBorgUplink):
    _sock = ()   
    def __init__(self, ip, port):
        DataBorgUplink.__init__(self, ip, port)
        
    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        self._sock.connect((self._ip, self._port))
        
    def _disconnect(self):
        self._sock.close()  
        
    def send(self, data):
        picklestring = pickle.dumps(data)     
        self._sock.send(struct.pack('Q', len(picklestring)))
        self._sock.send(picklestring)
        
class DataBorgDownlink:
    _ip = "";
    _port = 0;  
    def setup(self):
        self._ip = self.client_address[0]
        self._port = self.client_address[1]
        self.__connection = self.request
        DataBorg().setDownlink(self._ip, self._port)
    def finish(self):
        DataBorg().setDownlink(None, None)  
    def _disconnect(self):
        pass      
    def send(self, data):
        pass
        
class DataBorgTcpDownlink(DataBorgDownlink): 
    def handle(self):
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
        print(type(rcv_obj).__name__)
        if(type(rcv_obj).__name__ == 'RequestObject'):
            print(self._ip + " asks for " + rcv_obj.key);
            if(DataBorg().hasValue(rcv_obj.key)):   
                data = DataBorg().getValue(rcv_obj.key)
                print("mine: " + data.getMd5()) 
                print("client's: " + str(rcv_obj.md5))
                if(data.getMd5() == rcv_obj.md5):
                    print("client already has the correct version!")
                    self.send(UptodateObject())
                    return    
                #print("sending object " + rcv_obj.key + ": " +  data.get() + ", revision " + str(data.getRev()))  
                data.preDataborgSend()
                self.send(data)
                data.postDataborgSend()
            else:
                self.send(NullObject())
    
    def send(self, data):
        picklestring = pickle.dumps(data)     
        self.request.send(struct.pack('Q', len(picklestring)))
        self.request.send(picklestring)
        pass
        
class DataBorg(object):
    """
    Borg singleton data manager
    """
    __we_are_one = {}
    __register = {}
    __uplink = None
    __downlink = {}
    __initialized = 0
    __dataPathMap = {}
    __target = "/temp"

    def __init__(self):
        self.__dict__ = self.__we_are_one
        self.__initialized = 1
        self.lock = threading.Lock()	

    def setValue(self, key, value):
        self.lock.acquire()
        self.__register[key] = value
        self.lock.release()

    def getValue(self, key):
        return self.__register[key]   

    def hasValueMd5(self, key, hash):   
        if(key in self.__register):  
            if(hash == self.getValue(key).getMd5()):  
                print("found it, and with the correct md5!")  
                return 1
            else:
                print("md5 is wrong: " + str(hash))
                return self.askServer(key, hash) 
        else:
            return self.askServer(key, hash)            

    def hasValue(self, key):
        if(key in self.__register):  
            if(not self.__uplink):
                print("found it, and I'm the boss!")
                return 1
            else:
                return self.hasValueMd5(key, self.__register[key].getMd5())
        else:
            return self.askServer(key, 0)
                
    def askServer(self, key, hash): 
        if(not self.__uplink):
            print("have no uplink")
            return 0
        print("I'm gonna have to ask my boss") 
        retval = 0
        if(self.__uplink.ask(key, hash)): 
            retval = 1
        else:
            print("master server doesn't know " + key + " either")
            retval = 0 
        return retval

    def delValue(self, key):
        del self.__register[key]
        
    def setUplink(self, connection):
        self.__uplink = connection
        
    def setDownlink(self, ip, port):
        if(ip and port):
            address = ip + ":" + str(port)
            self.__downlink[address] = address
        else:
            self.__downlink[address] = None
            
    def setDataPath(self, path, alias = "default"):
        self.__dataPathMap[alias] = path
        
    def resolveDataPath(self, path):
        alias = "default"
        if("#" in path):
            colonIndex = path.index("#")
            alias = path[0:colonIndex]
            path = path[colonIndex+1:]
        if(alias not in self.__dataPathMap):
            print("resolveDataPath " + alias + " not found")
            return path
        print("resolveDataPath " + alias + ": " + self.__dataPathMap[alias])
        return normpath(self.__dataPathMap[alias] + "/" + path)
            
    def getDataPathMap(self):
        return self.__dataPathMap