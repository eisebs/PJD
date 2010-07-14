from admin import *
from databorg import *
from filebasedjobobject import *

admin = adminmodule("127.0.0.1", 12215)  
DataBorg().setDataPath("D:/temp", "fotos")
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test120.jpg", 120))
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test200.jpg", 200))
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test400.jpg", 400))
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test1200.jpg", 1200))    
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test20.jpg", 20))
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test50.jpg", 50))
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test700.jpg", 700))
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test1800.jpg", 1800))    
admin.send(ImageResizeJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#test350.jpg", 350))