'''
Created on May 5, 2013

@author: dorisip
'''
import unittest
from windy_tales.utils.utils import read_file
import os
from windy_tales.flat_file.header_parser import HeaderParser
from windy_tales.flat_file.parser import flat_to_json
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate


class TestParser(UnitTestWithMongoDB):

    def setUp(self):
        # Parse c header first
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.h')
        json = HeaderParser.generate_tempate(file_name)
        with WindyDbConnection() as connector:
            header = HeaderfileParsedTemplate(connector)
            header.save(data_name='sample', data=json, version=0)

    def test_flat_file_to_json(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.flat')
        flat_content=read_file(file_name)
        value = flat_to_json('sample', flat_content)
        self.assertIsNotNone(value)

        self.assertEquals(value['book']['title'], 'Book Name')
        self.assertEquals(value['book']['description'], 'my desc')
        self.assertEquals(value['book']['ack'][0]['name'], 'Alex')
        self.assertEquals(value['book']['ack'][1]['name'], 'Ben')

    def test_flat_file_to_json_with_truncated_flat_file(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'truncated_sample.flat')
        flat_content=read_file(file_name)
        value = flat_to_json('sample', flat_content)

        self.assertEquals(value['book']['title'], 'MyBook')
        self.assertEquals(value['book']['description'], '')
        self.assertEquals(value['book']['ack'][0]['name'], '')
        self.assertEquals(value['book']['ack'][1]['name'], '')

    def test_flat_file_to_json_with_extra_characters_in_flat(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'extra_sample.flat')
        flat_content=read_file(file_name)
        value = flat_to_json('sample', flat_content)

        self.assertEquals(value['book']['ack'][0]['name'], 'Alex')
        self.assertEquals(value['book']['ack'][1]['name'], 'Benjam')


if __name__ == "__main__":
    unittest.main()
