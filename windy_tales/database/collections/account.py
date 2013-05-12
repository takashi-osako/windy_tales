'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.generic_collection import GenericCollection
from windy_tales.exceptions.exceptions import GenericCollectionException


class Account(GenericCollection):
    def __init__(self, connection):
        self.__name = 'Account'
        super(Account, self).__init__(connection=connection, name='Account')

    def get_keys(self):
        '''
        return fieldname that uses for the key of Supplier
        '''
        return ['supplier_no', 'customer_no', 'account_no']
