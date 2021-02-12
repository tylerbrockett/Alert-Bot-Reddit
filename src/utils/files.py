"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   11/28/2016
Version:            v3.0
==========================================
"""

EMPTY = ''


def create_file(full_path):
    with open(full_path, 'w+') as f:
        f.close()


def read_file(full_path):
    with open(full_path, 'r') as f:
        contents = f.read()
        f.close()
        return contents


def write_to_file(full_path, string):
    with open(full_path, 'w') as f:
        f.seek(0)
        f.truncate()
        f.write(str(string))
        f.close()


def erase_contents(full_path):
    with open(full_path, 'w') as f:
        f.seek(0)
        f.truncate()
        f.close()


def is_empty(full_path):
    with open(full_path, 'r') as f:
        contents = f.read()
        f.close()
        if contents == EMPTY:
            return True
        return False
