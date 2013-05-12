'''
Created on May 11, 2013

@author: tosako
'''
from windy_tales.utils.utils import read_file
from windy_tales.flat_file.parser import flat_to_json
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.genericCollection import GenericCollection
from windy_tales.data_fusion import template_json
from windy_tales.data_aggregator.transaction_aggregator import aggregate_for_transaction
import json


def load_data_from_flatfile(filename):
    flat_contents = read_file(filename)
    for flat_content in flat_contents:
        # read first 20 chracters as data name
        data_name = flat_content[0:20].strip()
        content = flat_content[20:]
        json_format = flat_to_json(data_name, content)

        with WindyDbConnection() as connection:
            # find data collection
            try:
                collection_module = __import__('windy_tales.database.collections.' + data_name.lower(), globals(), locals(), [data_name])
                if collection_module:
                    genericCollection = getattr(collection_module, data_name)(connection)
                else:
                    genericCollection = GenericCollection(connection, data_name)
            except:
                genericCollection = GenericCollection(connection, data_name)
            doc_id = genericCollection.save(json_format)

            # TODO: TEMP:  template json from flat file data
            template_json(doc_id['_id'], data_name, None)

        # if data is transheader, then aggregate data for Data Fusion Service
        if data_name == "transheader":
            json_format = aggregate_for_transaction(json_format)
        print(json.dumps(json_format))
    return json_format
