'''
Created on May 5, 2013

@author: dorisip
'''
from windy_tales.flat_file.parser import flat_file_to_json
import os


if __name__ == '__main__':
    here = os.path.abspath(os.path.dirname(__file__))
    flat_file = os.path.join(here, 'resources', 'test_flat_file.txt')
    json_format = flat_file_to_json(flat_file)
