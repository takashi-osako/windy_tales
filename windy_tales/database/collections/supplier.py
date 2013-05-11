'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.collections.genericCollection import GenericCollection, \
    GenericCollectionException


class Supplier(GenericCollection):
    def __init__(self, connection):
        self.__name = 'supplier'
        super(Supplier, self).__init__(connection=connection, name=self.__name)

    def save(self, data):
        key = {'supplier_no': data['supplier_no']}
        super(Supplier, self).save({self.__name: data}, key_data=key)

    def find_by_keys(self, keys):
        if keys is None:
            raise GenericCollectionException('keys are missing')
        ks = self.get_keys()
        key_data = {}
        for k in ks:
            key_data['key_data.' + k] = keys[k]
        doc = super(Supplier, self).find_one(key_data)
        return doc['metadata']

    def get_keys(self):
        '''
        return fieldname that uses for the key of Supplier
        '''
        return ['supplier_no']
