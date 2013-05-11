'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.connectionManager import DbConnectionManager


class WindyDbConnection(DbConnectionManager):
    def __init__(self, db_name='windy'):
        DbConnectionManager.__init__(self, db_name)
