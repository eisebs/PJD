import ui
import os
from server import *

#server = Server.PyComputeServer(12213)

def on_button(id):
  if(id == 1):
      ServerManager.startJobServer(12213)
      ServerManager.startDataServer(12214)
      ServerManager.startAdminServer(12215)

  if(id == 2):
      ServerManager.stopJobServer(12213)
      ServerManager.stopDataServer(12214)
      ServerManager.stopAdminServer(12215)
      
def on_tick():
  return
  
test = DataObject("teststring")
test.set("teststring2")   
test.set("teststring1")
test.set("teststring2")
test.set("teststring4")
#DataBorg().setValue("testobject", test)
DataBorg().setValue("testobject", test)
  
gui = ui.Ui(on_button, on_tick)
gui.setLabel("server")
gui.root.mainloop()
