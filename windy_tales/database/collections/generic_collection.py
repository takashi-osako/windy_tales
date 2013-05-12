'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.collections.base import BaseCollection
import datetime
from uuid import uuid4
from windy_tales.exceptions.exceptions import GenericCollectionException


class GenericCollection(BaseCollection):

    def __init__(self, connection, name):
        if name is None or name == "":
            raise GenericCollectionException("name is missing")
        super(GenericCollection, self).__init__(connectionManager=connection, name=name)

    def save(self, data, key_data=None, currentDatetime=datetime.datetime.utcnow()):
        uuid = str(uuid4())
        document = {"_id": uuid, "update": currentDatetime, "metadata": data[super(GenericCollection, self).getName()]}
        # add data_key in document
        if key_data:
            document['key_data'] = key_data
        return BaseCollection.save(self, document)
