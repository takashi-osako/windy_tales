'''
Created on May 5, 2013

@author: dorisip
'''
from watchdog.events import FileSystemEventHandler
from windy_tales.flat_file.parser import flat_file_to_json
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.genericCollection import GenericCollection
from windy_tales.watcher.archive import achive_file


class WatcherEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        '''
        Listen to file/directory creation events
        Ignoring file modification and file renames
        '''
        if event.is_directory is False:
            print("New file created in LZ: " + event.src_path)

            # New file is received, convert flat file to json format
            json_format = flat_file_to_json(event.src_path)

            # archive the file
            achive_file(event.src_path)

            with WindyDbConnection() as connection:
                genericCollection = GenericCollection(connection, 'dummyname')
                genericCollection.save(json_format)
            print(json_format)
