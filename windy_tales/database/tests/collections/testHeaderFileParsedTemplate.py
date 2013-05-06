'''
Created on May 5, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UniteTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.collections.headerFileParsedTemplate import HeaderfileParsedTemplate
import datetime
from windy_tales.database.connection import WindyDbConnection


class TestHeaderFileParsedTemplate(UnitTestWithMongoDB):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSave(self):
        data = {"address1":10, "city": 5, "zip":5}
        with WindyDbConnection() as connection:
            collection = HeaderfileParsedTemplate(connection)
            mydatetime = datetime.datetime.utcnow()
            id = collection.save(data_name="myheadername", data=data, version="1", currentDatetime=mydatetime)
        self.assertIsNotNone(id)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
