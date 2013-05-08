from cloudy_tales.database.collections.base import BaseCollection
import datetime
from uuid import uuid4
from cloudy_tales.database.MongoOperationManager import MongoOperationManager


class HeaderfileParsedTemplate(BaseCollection):
    def __init__(self, connection, name="headerfile_parsed_template"):
        BaseCollection.__init__(self, mongoOperationManager=MongoOperationManager(connection), name=name)

    def save(self, data_name, data, version, currentDatetime=datetime.datetime.utcnow()):
        uuid = uuid4()
        document = {"_id": uuid, "name": data_name, "version": version, "update": currentDatetime, "metadata": data}
        return BaseCollection.save(self, document)

    def find_by_name(self, name):
        document = {"name": name}
        return BaseCollection.find(self, document)
