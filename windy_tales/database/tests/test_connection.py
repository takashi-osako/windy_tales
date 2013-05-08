'''
Created on May 5, 2013

@author: tosako
'''
import unittest
from windy_tales.database.connection import WindyDbConnection
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB


class TestWindyConnection(UnitTestWithMongoDB):

    def setUp(self):
        self.__conn = WindyDbConnection()

    def tearDown(self):
        # Drop rows in collection
        self.__conn.get_client()['windy']['testCollection'].remove()

    def test_get_db(self):
        db = self.__conn.get_db()
        self.assertEquals(db.name, 'windy')

    def test_get_collection(self):
        col = self.__conn.get_collection('testCollection')
        self.assertEquals(col.name, 'testCollection')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
