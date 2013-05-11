'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.supplier import Supplier


def aggregate_for_transaction(data):
    '''
    aggregate transaction data with
    supplier
    '''
    with WindyDbConnection() as connection:
        # find supplier and aggrigate the data
        supplier = Supplier(connection)
        supplier_keys = supplier.get_keys()
        key_data = {}
        for supplier_key in supplier_keys:
            key_data[supplier_key] = data['transheader'][supplier_key]
        transheader = data['transheader']
        supplier_data = supplier.find_by_keys(key_data)
        for name in supplier_data.keys():
            transheader[name] = supplier_data[name]
    return data;
