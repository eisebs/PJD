from tkinter import *
from systemborg import *
from jobqueue import *

class Ui():
  root = Tk()
  
  button_callback = 0;   
  tick_callback = 0
  
  def __init__(self, button_callback, tick_callback):
      self.button_callback = button_callback
      self.tick_callback = tick_callback
      self.frame = Frame(self.root, width=100, height=80)
      self.frame.pack()                           
      self.label = Label(self.frame, text="", font=("Verdana", 10), width=20, height=3) 
      self.label.pack()                           
      self.start_server = Button(self.frame, text="start", font=("Verdana", 10), width=20, height=5) 
      self.start_server.pack()    
      self.start_server["command"] = self.startServerClicked   
      self.stop_server = Button(self.frame, text="stop", font=("Verdana", 10), width=20, height=5) 
      self.stop_server.pack()    
      self.stop_server["command"] = self.stopServerClicked
      self.client_list = Listbox(self.frame)     
      self.client_list.pack()    
      self.root.after(1000, self.tick)
      msgsys = SystemBorg().get("msgsys")
      msgsys.registerCallback("addclient", self.addClientToList)
      msgsys.registerCallback("delclient", self.delClientFromList) 
      self.root.bind_all('<Key>', self.key);
      self.client_callback = {}
    
  def __del__(self):
      msgsys = SystemBorg().get("msgsys")
      msgsys.unregisterCallback("addclient", self.addClientToList)
      msgsys.unregisterCallback("delclient", self.delClientFromList)
      
  def key(self, event):
      #print(event.keysym)
      if(event.keysym == "Delete"):
          selection = self.client_list.curselection()
          for x in selection:
              #print(self.client_list.get(x)) 
              self.client_callback[self.client_list.get(x)]()
      elif(event.keysym == "Return"):
          SystemBorg().get("JobQueue").push(DebugJobObject("rudolf"))
    
  def tick(self):
      self.tick_callback()
      self.root.after(1000, self.tick)

  def setLabel(self, labeltext):
      self.label["text"] = labeltext

  def startServerClicked(self):
      self.button_callback(1)

  def stopServerClicked(self):
      self.button_callback(2)

  def addClientToList(self, obj):  
      self.client_list.insert(END, obj[0])
      #print(obj[0])
      self.client_callback[obj[0]] = obj[1]
    
  def delClientFromList(self, label):
        index = 0;
        while(index < self.client_list.size()):
            if(self.client_list.get(index, 0) == label):
                self.client_list.delete(index)
                break;    
            index = index + 1