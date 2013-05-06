'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.collections.base import BaseCollection
from cloudy_tales.database.MongoOperationManager import MongoOperationManager
import datetime
from uuid import uuid4

class GenericCollectionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GenericCollection(BaseCollection):

    def __init__(self, connection, name):
        if name is None or name == "":
            raise GenericCollectionException("name is missing")
        super(GenericCollection, self).__init__(mongoOperationManager=MongoOperationManager(connection), name=name)

    def save(self, data, currentDatetime=datetime.datetime.utcnow()):
        uuid = uuid4()
        document = {"_id":uuid, "update":currentDatetime, "metadata":data }
        return BaseCollection.save(self, document)
