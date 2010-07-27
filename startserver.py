from servergui import *
  
DataBorg().setDataPath("D:/Fotos/20100704_Springbrunnen_Bundeshaus", "fotos")
DataBorg().setDataPath("D:/temp/received", "output")
forceDataBorgPathScan()

ServerManager.startJobServer(12213)
ServerManager.startDataServer(12214)
ServerManager.startAdminServer(12215)

startServerGui()