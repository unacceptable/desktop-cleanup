#!/usr/bin/env python
# Written by: Robert J.
# Email:      robert@scriptmyjob.com

'''
If you use this script for your macbook create a launchd:

18:47 MacOS: ~/ >$ cat ~/Library/LaunchAgents/com.scriptmyjob.desktop_cleanup.plist 
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.scriptmyjob.desktop_cleanup</string>
        <key>Program</key>
        <string>/Users/robert/Scripts/.bin/desktop_cleanup.py</string>
        <key>RunAtLoad</key>
        <true/>
    </dict>
</plist>
18:47 MacOS: ~/ >$
'''

import sys
import os
import re
import logging
from time import sleep

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG
)

logger = logging.getLogger()

#######################################
### Main Function #####################
#######################################

def main():
    home_dir    = os.environ['HOME']
    desktop     = os.path.join(home_dir, 'Desktop')
    temp_dir    = os.path.join(home_dir, 'Pictures/Temp') 
    pattern     = 'Screen.*\.png'
    pictures    = get_pictures(desktop, pattern)
    
    if pictures:
        move_items(pictures, desktop, temp_dir)
        archive_old_pictures(temp_dir, pattern)


#######################################
### Generic Functions #################
#######################################

def move_items(items, source, destination):
    if not os.path.isdir(destination):
        logger.info('Creating directory: "{0}"'.format(destination))
        os.makedirs(destination)

    for i in items:
        source_file = os.path.join(source, i)
        dest_file   = os.path.join(destination, i)

        logger.info('Moving "{0}" to "{1}"'.format(source_file, dest_file))
        os.rename(source_file, dest_file)


#######################################
### Program Specific Functions ########
#######################################

def get_pictures(directory, pattern):
    pictures = [
        p for p in os.listdir(directory) if re.match(pattern, p)
    ]
    
    if pictures:
        logger.info('Found items to move: ' + str(pictures))
    else:
        return

    return pictures


def archive_old_pictures(temp_dir, pattern):
    old_pictures = get_pictures(temp_dir, pattern)[:-5]

    for op in old_pictures:
        dest = temp_dir.strip('Temp') + op.split(' ')[2]
        src  = temp_dir

        move_items([op], src, dest)


#######################################
### Execution #########################
#######################################

if __name__ == "__main__":
    logger.info('Starting Desktop Cleanup Daemon.')

    while True:
        try:
            main()
            sleep(1)
        except KeyboardInterrupt, e:
            print('\n')
            logging.info("Stopping Desktop Cleanup Deamon per user input.")
            break

