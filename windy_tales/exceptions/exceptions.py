'''
Created on May 8, 2013

@author: dorisip
'''


class WindyError(Exception):
    '''
    base class for exceptions
    '''
    pass


class HeaderFileNotFound(WindyError):
    '''
    Raised when C header file is not found
    '''
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return repr(self.name)
