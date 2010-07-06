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
#obj = FileDataObject('FILE:DSC_0421.JPG')
DataBorg().setDataPath("D:/temp")
DataBorg().hasValue("FILE:DSC_0421.JPG")
#DataBorg().hasValueMd5('FILE:DSC_0421.JPG', DataBorg().getValue('FILE:DSC_0421.JPG').getMd5)