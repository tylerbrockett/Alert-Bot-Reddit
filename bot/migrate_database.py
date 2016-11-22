import sqlite3
from utils import database
import json
import traceback
from sqlite3 import IntegrityError
import os
from os import path

if __name__ == '__main__':
    was_error = False

    num_subs = 0
    num_matches = 0

    FILE_PATH = os.path.dirname(os.path.abspath(__file__))

    old_path = path.join(FILE_PATH, 'old.db')
    old = sqlite3.connect(old_path)
    old.text_factory = str
    old.execute('PRAGMA foreign_keys = ON;')
    cursor = old.cursor()
    cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    cursor.execute(database.CREATE_TABLE_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALERTS)

    new_path = path.join(FILE_PATH, 'new.db')
    new = sqlite3.connect(new_path)
    new.text_factory = str
    new.execute('PRAGMA foreign_keys = ON;')
    cursor = new.cursor()
    cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    cursor.execute(database.CREATE_TABLE_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALL_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALL_USERS)
    cursor.execute(database.CREATE_TABLE_ALERTS)


    COL_SUB_USERNAME = 0
    COL_SUB_MESSAGE_ID = 1
    COL_SUB_ITEM = 2
    COL_SUB_TIMESTAMP = 3

    COL_MATCHES_USERNAME = 0
    COL_MATCHES_ITEM = 1
    COL_MATCHES_LINK = 2
    COL_MATCHES_TIMESTAMP = 3

    subs = old.cursor().execute('SELECT * FROM ' + database.TABLE_SUBSCRIPTIONS).fetchall()

    for sub in subs:
        num_subs += 1
        try:
            matches = old.cursor().execute('SELECT * FROM ' + database.TABLE_MATCHES + ' WHERE username = (?) AND item = (?)', [str(sub[0]), str(sub[2])]).fetchall()
            original_sub = sub[2]
            dict = {"body": [], "subreddits": [], "title": [[original_sub]], "redditors": [], "ignore_body": [], "ignore_redditors": [], "valid": True, "nsfw": False, "schema_version": 1, "ignore_title": [], "email": False}
            json_text = json.dumps(dict, 2)
            print(json_text)

            sub_params = [str(sub[0]), str(sub[1]), str(json_text), sub[3]]

            print('==============================================================\n' +
                  'USERNAME:    ' + sub_params[0] + '\n' +
                  'MESSAGE_ID:  ' + sub_params[1] + '\n' +
                  'JSON:        ' + sub_params[2] + '\n' +
                  'TIMESTAMP:   ' + str(sub_params[3]) + '\n' +
                  '==============================================================\n\n')
            new.cursor().execute('INSERT INTO ' + database.TABLE_SUBSCRIPTIONS + ' VALUES (?,?,?,?)', sub_params)
            new.cursor().execute('INSERT OR IGNORE INTO ' + database.TABLE_ALL_USERS + ' VALUES (?)', [sub[0]])

            for match in matches:
                num_matches += 1
                try:
                    match_params = [match[0], json_text, match[2], match[3]]
                    print('==============================================================\n' +
                          'USERNAME:    ' + match_params[0] + '\n' +
                          'MESSAGE_ID:  ' + match_params[1] + '\n' +
                          'JSON:        ' + match_params[2] + '\n' +
                          'TIMESTAMP:   ' + str(match_params[3]) + '\n' +
                          '==============================================================\n\n')
                    new.cursor().execute('INSERT INTO ' + database.TABLE_MATCHES + ' VALUES (?,?,?,?)', match_params)
                    new.cursor().execute('INSERT INTO ' + database.TABLE_ALL_MATCHES + ' VALUES (?,?,?,?)', match_params)
                except IntegrityError:
                    was_error = True
                    print('DUPLICATE MATCH ENTRY')
        except IntegrityError:
            was_error = True
            print('DUPLICATE SUB ENTRTY')
        except:
            was_error = True
            print('\n\n' + traceback.format_exc() + '\n\n')

    new.commit()

    if was_error:
        print('THERE WERE ERRORS!')
    else:
        print('No errors occurred')

    print('\n\n\n\n#STATS')
    print('NUM SUBS:    ' + str(num_subs))
    print('NUM MATCHES: ' + str(num_matches))

