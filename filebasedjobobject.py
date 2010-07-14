from jobobject import *
from filedataobject import *

class FileBasedJobResult(NullResult):
    def __init__(self, uid, result):
        self.uid = uid
        self.result = result
        self.resulttext = ""
    pass        
        
class FileBasedJobObject(JobObject):
    def __init__(self, source, target):
        JobObject.__init__(self)
        self.__source = source
        self.__target = target
        sourceObject = FileDataObject(self.__source)
        self.addDependency(sourceObject.getKey(), sourceObject.getMd5())
        targetObject = FileDataObject(self.__target)
        self.addResult(targetObject.getKey(), targetObject)
    def doJob(self):
        pass
    def getResultsObject(self):
        target = self.getResults()[0]
        targetName = target.name
        target.data.uid = self.uid
        target.data.resulttext = "multiprocessing processed job " + str(self.uid)
        target.data = FileDataObject(targetName)
        self.setResultsObject(FileBasedJobResult(self.uid, target))
        return JobObject.getResultsObject(self)
        
class IrfanviewJobObject(FileBasedJobObject):
    def __init__(self, source, target, iViewOptions):
        FileBasedJobObject.__init__(self, source, target)
        self.__iViewOptions = iViewOptions
    def doJob(self):
        source = self.getDependencies()[0].resolvedName
        resolvedTargetName = self.getResults()[0].resolvedName
        commandstring = "i_view32 " + source + " " + self.__iViewOptions + " /convert=" + resolvedTargetName
        os.system(commandstring)