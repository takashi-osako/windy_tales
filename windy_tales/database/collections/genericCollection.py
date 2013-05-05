'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.collections.base import BaseCollection

class GenericCollectionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GenericCollection(BaseCollection):

    def __init__(self, name):
        if name is None or name == "":
            raise GenericCollectionException("name is missing")
        super(GenericCollection, self).__init__(name)
