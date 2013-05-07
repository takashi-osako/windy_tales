'''
Created on Apr 7, 2013

@author: dorisip
'''
from cloudy_tales.database.connection import DbConnection


class WindyDbConnection(DbConnection):
    def __init__(self, db_name='windy'):
        DbConnection.__init__(self, db_name)
