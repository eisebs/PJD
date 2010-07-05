from databorg import *
import time

DataBorg().setUplink(DataBorgTcpUplink("127.0.0.1", 12214))  
  
#test = DataObject("teststring")
#test.set("teststring2")   
#test.set("teststring1")
#test.set("teststring2")
#test.set("teststring3")
#DataBorg().setValue("testobject", test)

#test2 = DataObject("teststring5")

DataBorg().setTempPath('D:/temp')
if(DataBorg().hasValue('FILE:DSC_0221.JPG')):
    DataBorg().getValue('FILE:DSC_0221.JPG')