'''
Created on May 5, 2013

@author: dorisip
'''
import unittest
from windy_tales.flat_file.header_parser import HeaderParser
import os


class TestHeaderParser(unittest.TestCase):

    def test_generate_tempate(self):
        HeaderParser.generate_tempate()
        self.assertIsNotNone(HeaderParser.get_template())

    def test_generate_tempate_from_sample(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'sample.h')
        HeaderParser.generate_tempate(file_name)
        template = HeaderParser.get_template()

        self.assertEquals(template['book']['title'], 10)
        self.assertEquals(template['book']['names'][1]['ack']['name'], 6)

    def test_generate_template_unsupported_header_file(self):
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'unsupported.h')
        HeaderParser.generate_tempate(file_name)
        template = HeaderParser.get_template()

        self.assertEquals(template['book']['title'], 10)
        self.assertEquals(len(template['book'].keys()), 1)


if __name__ == "__main__":
    unittest.main()
