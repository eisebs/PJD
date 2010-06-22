from databorg import *
import time

DataBorg().registerUplink(DataBorgTcpUplink("127.0.0.1", 12214))    
  
test = DataObject("teststring")
test.set("teststring2")   
test.set("teststring1")
test.set("teststring2")
test.set("teststring3")
DataBorg().setValue("testobject", test)

test2 = DataObject("teststring5")

if(DataBorg().hasValueMd5("testobject", test2.getMd5())):
    print(DataBorg().getValue("testobject").get())