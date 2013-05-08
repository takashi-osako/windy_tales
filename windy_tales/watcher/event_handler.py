'''
Created on May 5, 2013

@author: dorisip
'''
from watchdog.events import FileSystemEventHandler
from windy_tales.flat_file.parser import flat_file_to_json
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.genericCollection import GenericCollection
from windy_tales.utils.archive import achive_file
import os


class WatcherEventHandler(FileSystemEventHandler):

    def on_moved(self, event):
        '''
        Only listen for move or rename from landing zone to a file within the landing zone
        '''
        if event.is_directory is False:
            file_name, file_ext = os.path.splitext(event.dest_path)
            if file_ext == '.flat':
                print("File created renamed in LZ: " + event.dest_path)

                # New file is received, convert flat file to json format
                json_format = flat_file_to_json(event.dest_path)

                # archive the file
                achive_file(event.dest_path)

                with WindyDbConnection() as connection:
                    genericCollection = GenericCollection(connection, 'dummyname')
                    genericCollection.save(json_format)
                print(json_format)
