from messagesystem import *
from jobqueue import *

class SystemBorg(object):
    """
    Borg singleton system manager
    """
    __we_are_one = {}
    __register = {}
    
    def __new__(cls, *p, **k):
        self = object.__new__(cls, *p, **k)
        self.__dict__ = cls.__we_are_one
        if(not self.has("msgsys")):
            self.set("msgsys", MessageSystem())
        if(not self.has("JobQueue")): 
            self.set("JobQueue", JobQueue())
        return self

    def set(self, key, value):
        self.__register[key] = value

    def get(self, key):
        return self.__register[key]

    def has(self, key):
        return key in self.__register

    def delete(self, key):
        del self.__register[key]
        
    def __del__(self):
        pass