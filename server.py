import socketserver
import threading 
import pickle
from systemborg import *
from databorg import *
from jobmanager import *
from admin import *

class ServerManager():            
    def startDataServer(port):
        key = "DataServer:" + str(port);
        if(not SystemBorg().has(key)):
            print("starting data server on port " + str(port));
            server = ThreadedTcpServer(('', port), DataBorgTcpRequestHandler)
            SystemBorg().set(key, server)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.setDaemon(True)
            server_thread.start()
            return server
        else:
            return 0
    def stopDataServer(port):
        key = "DataServer:" + str(port);
        if(SystemBorg().has(key)):
            print("shutting down data server on port " + str(port));
            SystemBorg().get(key).shutdown()
            SystemBorg().delete(key)
            return 1
        else:
            return 0 
            
    def startJobServer(port):
        key = "JobServer:" + str(port);
        if(not SystemBorg().has(key)):
            print("starting job server on port " + str(port));
            server = ThreadedTcpServer(('', port), JobServerTcpRequestHandler)
            SystemBorg().set(key, server)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.setDaemon(True)
            server_thread.start()
            return server
        else:
            return 0
    def stopJobServer(port):
        key = "JobServer:" + str(port);
        if(SystemBorg().has(key)):
            print("shutting down job server on port " + str(port));
            SystemBorg().get(key).shutdown()
            SystemBorg().delete(key)
            return 1
        else:
            return 0
            
    def startJobServer(port):
        key = "JobServer:" + str(port);
        if(not SystemBorg().has(key)):
            print("starting job server on port " + str(port));
            server = ThreadedTcpServer(('', port), JobServerTcpRequestHandler)
            SystemBorg().set(key, server)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.setDaemon(True)
            server_thread.start()
            return server
        else:
            return 0
            
    def stopAdminServer(port):
        key = "AdminServer:" + str(port);
        if(SystemBorg().has(key)):
            print("shutting down admin server on port " + str(port));
            SystemBorg().get(key).shutdown()
            SystemBorg().delete(key)
            return 1
        else:
            return 0
            
    def startAdminServer(port):
        key = "AdminServer:" + str(port);
        if(not SystemBorg().has(key)):
            print("starting admin server on port " + str(port));
            server = ThreadedTcpServer(('', port), AdminTcpRequestHandler)
            SystemBorg().set(key, server)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.setDaemon(True)
            server_thread.start()
            return server
        else:
            return 0

class ThreadedTcpServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class DataBorgTcpRequestHandler(socketserver.BaseRequestHandler, DataBorgTcpDownlink):   
    def setup(self):
        socketserver.BaseRequestHandler.setup(self)
        DataBorgDownlink.setup(self)
    
    def handle(self):
        DataBorgTcpDownlink.handle(self)
          
    def send(self, data):
        DataBorgTcpDownlink.send(self, data)

    def finish(self):  
        pass         
        
class JobServerTcpRequestHandler(socketserver.BaseRequestHandler, JobManagerTcpDownlink):   
    def setup(self):
        socketserver.BaseRequestHandler.setup(self)
        JobManagerdownlink.setup(self)
    
    def finish(self):
        JobManagerdownlink.stop(self)
    
    def handle(self):
        JobManagerTcpDownlink.handle(self)
          
    def send(self, data):
        JobManagerTcpDownlink.send(self, data)
        
class AdminTcpRequestHandler(socketserver.BaseRequestHandler, JobManagerTcpDownlink):   
    def setup(self):
        socketserver.BaseRequestHandler.setup(self)
        AdminDownlink.setup(self)
    
    def finish(self):
        AdminDownlink.finish(self)
    
    def handle(self):
        AdminTcpDownUplink.handle(self)
          
    def send(self, data):
        AdminTcpDownUplink.send(self, data)