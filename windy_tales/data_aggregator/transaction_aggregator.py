'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.supplier import Supplier
from windy_tales.database.collections.customer import Customer


def aggregate_for_transaction(data):
    '''
    aggregate transaction data with
    supplier
    '''
    with WindyDbConnection() as connection:
        # find supplier and aggrigate the data
        transheader = data['transheader']
        supplier = Supplier(connection)
        supplier_keys = supplier.get_keys()
        key_data = {}
        for supplier_key in supplier_keys:
            key_data[supplier_key] = transheader[supplier_key]
        supplier_data = supplier.find_by_keys(key_data)
        transheader[supplier.getName()] = supplier_data

        customer = Customer(connection)
        customer_keys = customer.get_keys()
        key_data = {}
        for customer_key in customer_keys:
            key_data[customer_key]=transheader[customer_key]
        customer_data = customer.find_by_keys(key_data)
        transheader[customer.getName()] = customer_data
    return data
