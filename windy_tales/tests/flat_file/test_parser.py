'''
Created on May 5, 2013

@author: dorisip
'''
import unittest
from windy_tales.flat_file.parser import flat_file_to_json
import os
from windy_tales.flat_file.header_parser import HeaderParser


class TestParser(unittest.TestCase):

    def setUp(self):
        # Parse c header first
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.h')
        HeaderParser.generate_tempate(file_name)

    def test_flat_file_to_json(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.flat')
        value = flat_file_to_json(file_name)
        self.assertIsNotNone(value)

        self.assertEquals(value['book']['title'], 'Book Name')
        self.assertEquals(value['book']['description'], 'my desc')
        self.assertEquals(value['book']['ack'][0]['name'], 'Alex')
        self.assertEquals(value['book']['ack'][1]['name'], 'Ben')

    def test_flat_file_to_json_with_truncated_flat_file(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'truncated_sample.flat')
        value = flat_file_to_json(file_name)

        self.assertEquals(value['book']['title'], 'MyBook')
        self.assertEquals(value['book']['description'], '')
        self.assertEquals(value['book']['ack'][0]['name'], '')
        self.assertEquals(value['book']['ack'][1]['name'], '')

    def test_flat_file_to_json_with_extra_characters_in_flat(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'extra_sample.flat')
        value = flat_file_to_json(file_name)

        self.assertEquals(value['book']['ack'][0]['name'], 'Alex')
        self.assertEquals(value['book']['ack'][1]['name'], 'Benjam')


if __name__ == "__main__":
    unittest.main()
