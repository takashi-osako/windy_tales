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
        #find supplier and aggrigate the data
        supplier_no = data['transheader']['supplier_no']
        supplier = Supplier(connection)
        data['supplier']=supplier.find_by_supplier_no(supplier_no)
    return data;