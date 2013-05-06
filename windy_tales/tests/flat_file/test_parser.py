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
        HeaderParser.generate_tempate()

    def tearDown(self):
        pass

    def test_flat_file_to_json(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.flat')
        value = flat_file_to_json(file_name)
        self.assertIsNotNone(value)

        self.assertEquals(value["address"]["address_line1"], "55 Washington St")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
