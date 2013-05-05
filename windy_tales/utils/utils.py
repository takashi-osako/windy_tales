'''
Created on May 5, 2013

@author: dorisip
'''
def read_file(file_name):
    '''
    Read and return content of a file in file system
    '''
    # TODO: check if file exists
    with open(file_name, 'r') as reader:
        content = reader.read()
    return content