'''
Created on May 5, 2013

@author: dorisip
'''
import os
import signal
import atexit
from windy_tales.watcher.watcher import Watcher
import time
import sys
from windy_tales.flat_file.header_parser import HeaderParser
from cloudy_tales.database.client import create_db_client
from windy_tales.database.connection import WindyDbConnection
from windy_tales.database.collections.header_file_parsed_template import HeaderfileParsedTemplate
from cloudy_tales.database.MongoOperationManager import MongoOperationManager

watcher = Watcher('/tmp/lz')


def main():
    '''
    Initializes watcher to monitor landing zone
    '''
    # initialize mongodb
    create_db_client()
    load_template()

    watcher.watch_dir()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        # sleeps until a signal is sent to process
        signal.pause()


def signal_handler(signal, frame):
    '''
    Catches Ctrl-C to exit
    '''
    print("Exiting")
    global watcher
    watcher.stop()
    watcher.join()
    sys.exit(0)

def load_template():
    header_files = ['test.h']
    here = os.path.abspath(os.path.dirname(__file__))
    with WindyDbConnection() as connection:
        headerFileParsedTemplate = HeaderfileParsedTemplate(connection=connection)
        headerFileParsedTemplate.remove()
        for header_file in header_files:
            file_name = os.path.join(here, 'resources', header_file)
            json = HeaderParser.generate_tempate(file_name)
            headerFileParsedTemplate.save(data_name=header_file[:-2], data=json, version=1)

if __name__ == '__main__':
    main()
