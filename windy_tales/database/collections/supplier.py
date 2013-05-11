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

    def find_by_supplier_no(self, supplier_no=None):
        if supplier_no is None:
            raise GenericCollectionException('supplier_no is missing')
        doc = super(Supplier,self).find_one({'key_data.supplier_no': supplier_no})
        return doc['metadata']
