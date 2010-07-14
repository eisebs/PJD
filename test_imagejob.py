from admin import *
from databorg import *
from filebasedjobobject import *

admin = adminmodule("127.0.0.1", 12215)  
DataBorg().setDataPath("D:/temp", "fotos")
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test.jpg", 1))           