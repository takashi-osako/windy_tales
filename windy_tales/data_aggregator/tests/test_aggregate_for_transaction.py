'''
Created on May 11, 2013

@author: tosako
'''
import unittest
from cloudy_tales.database.tests.UnitTestWithMongoDB import UnitTestWithMongoDB
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.supplier import Supplier
from windy_tales.data_aggregator.transaction_aggregator import aggregate_for_transaction


class TestAggregateForTransaction(UnitTestWithMongoDB):

    def test_find_supplier_from_transaction(self):
        transaction = {}
        transaction['trans_ref_no'] = '0000000001'
        transaction['supplier_no'] = '0000000001'
        with WindyDbConnection() as connection:
            supplier = Supplier(connection)
            supplier_data = {}
            supplier_data['supplier_no'] = '0000000001'
            supplier_data['name'] = 'name1'
            supplier.save({'Supplier': supplier_data})
            supplier_data = {}
            supplier_data['supplier_no'] = '0000000002'
            supplier_data['name'] = 'name2'
            supplier.save({'Supplier': supplier_data})
        data = aggregate_for_transaction({'Transheader': transaction})
        self.assertEqual('name1', data['Transheader']['Supplier']['name'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
