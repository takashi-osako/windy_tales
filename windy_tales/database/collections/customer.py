'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.generic_collection import GenericCollection
from windy_tales.exceptions.exceptions import GenericCollectionException


class Customer(GenericCollection):
    def __init__(self, connection):
        self.__name = 'Customer'
        super(Customer, self).__init__(connection=connection, name=self.__name)

    def save(self, data):
        key = {}
        for k in self.get_keys():
            key[k] = data[self.__name][k]
        return super(Customer, self).save(data, key_data=key)

    def find_by_keys(self, keys):
        if keys is None:
            raise GenericCollectionException('keys are missing')
        ks = self.get_keys()
        key_data = {}
        for k in ks:
            key_data['key_data.' + k] = keys[k]
        doc = super(Customer, self).find_one(key_data)
        if doc:
            return doc['metadata']

    def get_keys(self):
        '''
        return fieldname that uses for the key of Supplier
        '''
        return ['supplier_no', 'customer_no']
