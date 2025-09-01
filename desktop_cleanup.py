#!/usr/bin/env python
'''
A simple daemon to clean up desktop screenshots by moving them to a temporary
'''

import os
import re
import logging

from time import sleep

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def main():
    '''
    Main function to orchestrate the desktop cleanup process.
    '''
    home_dir    = os.environ['HOME']
    desktop     = os.path.join(home_dir, 'Desktop')
    temp_dir    = os.path.join(home_dir, 'Pictures/Temp')
    pattern     = r'Screen.*\.png'
    pictures    = get_pictures(desktop, pattern)

    if pictures:
        move_items(pictures, desktop, temp_dir)
        archive_old_pictures(temp_dir, pattern)


def move_items(items, source, destination):
    '''
    Move specified items from source to destination directory.
    Create destination directory if it does not exist.
    '''
    if not os.path.isdir(destination):
        logging.info('Creating directory: %s', destination)
        os.makedirs(destination)

    for i in items:
        source_file = os.path.join(source, i)
        dest_file   = os.path.join(destination, i)

        logging.info('Moving "%s" to "%s"', source_file, dest_file)
        os.rename(source_file, dest_file)


def get_pictures(directory, pattern):
    '''
    Get a list of picture files in the specified directory matching the given pattern.
    '''
    pictures = [
        p for p in os.listdir(directory) if re.match(pattern, p)
    ]

    if pictures:
        logging.info('Found items to move: %s', pictures)

    return pictures


def archive_old_pictures(temp_dir, pattern):
    '''
    Archive old pictures in the temporary directory, keeping only the 5 most recent ones.
    '''
    pictures = get_pictures(temp_dir, pattern)

    old_pictures = [
        os.path.split(o)[1] for o in sorted(
            [
                os.path.join(temp_dir, p) for p in pictures
            ],
            key=os.path.getmtime
        )
    ][:-5]

    for op in old_pictures:
        dest = temp_dir.strip('Temp') + op.split(' ')[1]
        src  = temp_dir

        move_items([op], src, dest)


if __name__ == "__main__":
    logging.info('Starting Desktop Cleanup Daemon.')

    while True:
        try:
            main()
            sleep(1)
        except KeyboardInterrupt as e:
            print('\n')
            logging.info("Stopping Desktop Cleanup Deamon per user input.")
            break
