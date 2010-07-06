import ui
import os
import time
from server import *

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
  
DataBorg().setDataPath("D:/Fotos/20100704_Springbrunnen_Bundeshaus", "fotos")
obj = FileDataObject('FILE:fotos#DSC_0421.JPG')
DataBorg().setValue('FILE:fotos#DSC_0421.JPG', obj)
  
gui = ui.Ui(on_button, on_tick)
gui.setLabel("server")
gui.root.mainloop()

#on_button(1)
#while(1):
#    time.sleep(1)
