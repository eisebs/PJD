from databorg import *

class NullResult:
    def __init__(self):
        self.uid = -1
        self.result = None
        self.resulttext = ""
    pass
    
class DependencySet:
    def __init__(self, name, md5, data):
        self.name = name
        self.resolvedName = name
        self.md5 = md5
        self.data = data
    
class ResultSet:
    def __init__(self, name, data):
        self.name = name
        self.resolvedName = name
        self.data = data

class JobObject:
    uid = -1
    def __init__(self):
        self.__dependencies = []
        self.__results = []
        self.__valid = 1
        self.__resultsObject = NullResult()
        pass
    def addDependency(self, dep, md5):
        self.__dependencies.append(DependencySet(dep, md5, None))
    def addResult(self, key, target):
        self.__results.append(ResultSet(key, target))
    def getDependencies(self):
        return self.__dependencies
    def getResults(self):
        return self.__results
    def loadDependencies(self):
        for x in self.__dependencies:
            print("x.resolvedName = " + x.resolvedName)
            if(not DataBorg().hasValueMd5(x.resolvedName, x.md5)):
                self.valid = 0
                return
            x.data = DataBorg().getValue(x.resolvedName)
            x.md5 = x.data.getMd5()
    def resolvePaths(self):
        for x in self.getDependencies():
            x.resolvedName = DataBorg().resolveDataPath(x.name[5:])
        for x in self.getResults():
            x.resolvedName  = DataBorg().resolveDataPath(x.name[5:])
    def process(self):
        if(self.__valid):
            self.__valid = self.doJob()
        return self.__valid
    def addResults(self, resultSet):
        return self.__results.append(resultSet)
    def getResults(self):
        return self.__results
    def getResultsObject(self):
        return self.__resultsObject
    def setResultsObject(self, resultsObject):
        self.__resultsObject = resultsObject
    def getIsValid(self):
        return self.__valid