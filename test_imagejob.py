from admin import *
from databorg import *
from filebasedjobobject import *

admin = adminmodule("127.0.0.1", 12215)  
DataBorg().setDataPath("D:/temp", "fotos")
#forceDataBorgPathScan()
admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#resize120.jpg", "/resize=(120) /resample /aspectratio"))
admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#resize200.jpg", "/resize=(200) /resample /aspectratio"))
admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#resize400.jpg", "/resize=(400) /resample /aspectratio"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#resize1200.jpg", "/resize=(1200) /resample /aspectratio"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#contrast20.jpg", "/contrast=20"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#contrast40.jpg", "/contrast=40"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#contrast60.jpg", "/contrast=60"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#crop.jpg", "/crop=(1000, 1000, 2000, 2000)"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#vflip.jpg", "/vflip"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#hflip.jpg", "/hflip"))
#admin.send(IrfanviewJobObject('FILE:fotos#DSC_0421.JPG', "FILE:output#vhflip.jpg", "/vflip /hflip"))