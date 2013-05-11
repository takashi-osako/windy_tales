'''
Created on May 5, 2013

@author: dorisip
'''
from watchdog.events import FileSystemEventHandler
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.genericCollection import GenericCollection
from windy_tales.utils.archive import achive_file
import os
from windy_tales.flat_file.parser import flat_to_json
from windy_tales.utils.utils import read_file
import json
from windy_tales.exceptions.exceptions import HeaderFileNotFound
from windy_tales.data_fusion import template_json
from windy_tales.data_aggregator.transaction_aggregator import aggregate_for_transaction


class WatcherEventHandler(FileSystemEventHandler):

    def on_moved(self, event):
        '''
        Only listen for move or rename from landing zone to a file within the landing zone
        '''
        if event.is_directory is False:
            file_name, file_ext = os.path.splitext(event.dest_path)
            if file_ext == '.flat':
                print("File renamed in LZ: " + event.dest_path)
                try:
                    # New file is received, convert flat file to json format
                    flat_contents = read_file(event.dest_path)
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
                    # archive the file
                    achive_file(event.dest_path)

                except HeaderFileNotFound as e:
                    print('Header template: %s not found' % data_name)
                except Exception as e:
                    print(e)
