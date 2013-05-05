'''
Created on May 5, 2013

@author: dorisip
'''
from watchdog.events import FileSystemEventHandler
from windy_tales.flat_file.parser import flat_file_to_json


class WatcherEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        '''
        Listen to file/directory creation events
        '''
        if event.is_directory is False:
            print("New file created in LZ: " + event.src_path)

            # New file is received, convert flat file to json format
            json_format = flat_file_to_json(event.src_path)
            print(json_format)
