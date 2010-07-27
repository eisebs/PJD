class MessageSystem:  
    __register = {}

    def __init__(self):
        return;
      
    def registerCallback(self, key, object):
        if(key in self.__register):
            list = self.__register[key];
            list.append(object)
        else:
            list = []     
            list.append(object)
            self.__register[key] = list         
      
    def unregisterCallback(self, key, object):
        if(key in self.__register):
            list = self.__register[key];
            list.remove(object)
        else:
            return 0         
      
    def call(self, key, object):
        if(key in self.__register):
            list = self.__register[key];
            for x in list:
                x(object)
        else:
            return 0