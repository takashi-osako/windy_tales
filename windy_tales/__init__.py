'''
Created on May 5, 2013

@author: dorisip
'''
from windy_tales.flat_file.parser import flat_file_to_json
import os
import signal
import atexit
from windy_tales.watcher.watcher import Watcher
import time
import sys
from windy_tales.flat_file.header_parser import HeaderParser

watcher = Watcher('/tmp/lz')


def main():
    '''
    Initializes watcher to monitor landing zone
    '''
    # Parse C header file and Generate a template
    HeaderParser.generate_tempate()

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

if __name__ == '__main__':
    main()
