"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

# ======================================================================================================
#           DATABASE SUBSCRIPTIONS TABLE
# ======================================================================================================

TABLE_SUBSCRIPTIONS = 'subscriptions'

USERNAME = 'username'
MESSAGE_ID = 'message_id'
SUB = 'sub'
TIMESTAMP = 'timestamp'

COL_SUB_USERNAME = 0
COL_SUB_MESSAGE_ID = 1
COL_SUB_ITEM = 2
COL_SUB_TIMESTAMP = 3


CREATE_TABLE_SUBSCRIPTIONS = \
    'CREATE TABLE IF NOT EXISTS ' + TABLE_SUBSCRIPTIONS + '(' + \
    USERNAME + ' TEXT NOT NULL, ' + \
    MESSAGE_ID + ' TEXT NOT NULL, ' + \
    SUB + ' TEXT NOT NULL, ' + \
    TIMESTAMP + ' REAL NOT NULL, ' + \
    'PRIMARY KEY(' + USERNAME + ', ' + SUB + '));'

INSERT_ROW_SUBSCRIPTIONS = 'INSERT INTO ' + \
                           TABLE_SUBSCRIPTIONS + \
                         ' VALUES (?,?,?,?)'

REMOVE_ROW_SUBSCRIPTIONS = 'DELETE FROM ' + TABLE_SUBSCRIPTIONS + \
    ' WHERE ' + USERNAME + ' = (?) ' + \
    ' AND ' + SUB + ' = (?)'

REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME = 'DELETE FROM ' + TABLE_SUBSCRIPTIONS + \
    ' WHERE ' + USERNAME + ' = (?)'

REMOVE_SUBSCRIPTION_BY_MESSAGE_ID = 'DELETE FROM ' + TABLE_SUBSCRIPTIONS + \
    ' WHERE ' + USERNAME + ' = (?) AND ' + MESSAGE_ID + ' = (?)'

GET_SUBSCRIPTIONS_BY_USERNAME = 'SELECT * ' + \
                                'FROM ' + TABLE_SUBSCRIPTIONS + ' ' + \
                                'WHERE ' + USERNAME + ' = ? COLLATE NOCASE ' + \
                                'ORDER BY ' + TIMESTAMP + ' ASC'

GET_SUBSCRIPTION = 'SELECT * FROM ' + TABLE_SUBSCRIPTIONS + ' ' + \
    'WHERE ' + USERNAME + ' = (?) AND ' + SUB + ' = (?)'

GET_SUBSCRIPTION_BY_MESSAGE_ID = 'SELECT * FROM ' + TABLE_SUBSCRIPTIONS + ' ' + \
    'WHERE ' + USERNAME + ' = (?) AND ' + MESSAGE_ID + ' = (?)'


GET_ALL_SUBSCRIPTIONS = 'SELECT * FROM ' + TABLE_SUBSCRIPTIONS + ' ORDER BY ' + TIMESTAMP + ' ASC'

# ======================================================================================================
#           DATABASE USERS TABLE
# ======================================================================================================

TABLE_ALL_USERS = 'all_users'

CREATE_TABLE_ALL_USERS = \
    'CREATE TABLE IF NOT EXISTS ' + TABLE_ALL_USERS + '(' + \
    USERNAME + ' TEXT NOT NULL,' + \
    'PRIMARY KEY(' + USERNAME + '));'

INSERT_ROW_ALL_USERS = 'INSERT OR IGNORE INTO ' + TABLE_ALL_USERS + ' VALUES(?)'

# ======================================================================================================
#           DATABASE MATCHES TABLES
# ======================================================================================================

TABLE_MATCHES = 'matches'
TABLE_ALL_MATCHES = 'all_matches'

COL_MATCHES_USERNAME = 0
COL_MATCHES_ITEM = 1
COL_MATCHES_LINK = 2
COL_MATCHES_TIMESTAMP = 3

PERMALINK = 'permalink'

CREATE_TABLE_MATCHES = \
    'CREATE TABLE IF NOT EXISTS ' + TABLE_MATCHES + '(' + \
    USERNAME + ' TEXT NOT NULL, ' + \
    SUB + ' TEXT NOT NULL, ' + \
    PERMALINK + ' TEXT NOT NULL, ' + \
    TIMESTAMP + ' REAL NOT NULL, ' + \
    'PRIMARY KEY(' + USERNAME + ', ' + SUB + ', ' + PERMALINK + '));'

CREATE_TABLE_ALL_MATCHES = \
    'CREATE TABLE IF NOT EXISTS ' + TABLE_ALL_MATCHES + '(' + \
    USERNAME + ' TEXT NOT NULL, ' + \
    SUB + ' TEXT NOT NULL, ' + \
    PERMALINK + ' TEXT NOT NULL, ' + \
    TIMESTAMP + ' REAL NOT NULL, ' + \
    'PRIMARY KEY(' + USERNAME + ', ' + SUB + ', ' + PERMALINK + '));'

INSERT_ROW_MATCHES = 'INSERT INTO ' + \
                         TABLE_MATCHES + \
                         ' VALUES (?,?,?,?)'

INSERT_ROW_ALL_MATCHES = 'INSERT OR IGNORE INTO ' + \
                         TABLE_ALL_MATCHES + \
                         ' VALUES (?,?,?,?)'

REMOVE_ALL_MATCHES_BY_USERNAME = 'DELETE FROM ' + TABLE_MATCHES + \
    ' WHERE ' + USERNAME + ' = ? '

REMOVE_MATCHES_BY_USERNAME_AND_SUBSCRIPTION = 'DELETE FROM ' + TABLE_MATCHES + \
    ' WHERE ' + USERNAME + ' = (?) ' + ' AND ' + SUB + ' = (?)'

PURGE_OLD_MATCHES = 'DELETE FROM ' + TABLE_MATCHES + \
    ' WHERE ' + TIMESTAMP + ' <= (?)'

GET_MATCH = 'SELECT * FROM ' + TABLE_MATCHES + ' ' + \
    'WHERE ' + USERNAME + ' = (?) AND ' + SUB + ' = (?) AND ' + PERMALINK + ' = (?)'

GET_MATCHES_BY_USERNAME_AND_SUBSCRIPTION = 'SELECT * FROM ' + TABLE_MATCHES + ' ' + \
    'WHERE ' + USERNAME + ' = (?) AND ' + SUB + ' = (?)'

# ======================================================================================================
#           DATABASE ALERTS TABLE
# ======================================================================================================

COL_ALERTS_USERNAME = 0
COL_ALERTS_RECEIVED_ALERT = 1

TABLE_ALERTS = 'alerts'

RECEIVED_ALERT = 'received_alert'

CREATE_TABLE_ALERTS = 'CREATE TABLE IF NOT EXISTS ' + TABLE_ALERTS + \
                '(' + USERNAME + ' TEXT NOT NULL, ' + RECEIVED_ALERT + ' INTEGER NOT NULL,' + \
                'PRIMARY KEY(' + USERNAME + '));'

GET_USERNAMES_THAT_NEED_ALERT = 'SELECT DISTINCT s.username ' + \
                                'FROM ' + TABLE_SUBSCRIPTIONS + ' s ' + \
                                'WHERE NOT EXISTS ' + \
                                    '(SELECT DISTINCT a.' + USERNAME + ' ' + \
                                    'FROM ' + TABLE_ALERTS + ' a ' + \
                                    'WHERE s.' + USERNAME + ' = a.' + USERNAME + ' AND ' + \
                                    'a.' + RECEIVED_ALERT + ' = 1)'

INSERT_ROW_ALERTS = 'INSERT INTO ' + TABLE_ALERTS + ' VALUES (?,?)'

DROP_TABLE_ALERTS = 'DROP TABLE ' + TABLE_ALERTS


# ======================================================================================================
#           STATISTICS
# ======================================================================================================

COUNT_USERS = 'SELECT DISTINCT ' + USERNAME + ' FROM ' + TABLE_SUBSCRIPTIONS
COUNT_SUBSCRIPTIONS = 'SELECT * FROM ' + TABLE_SUBSCRIPTIONS
COUNT_UNIQUE_SUBSCRIPTIONS = 'SELECT DISTINCT ' + SUB + ' FROM ' + TABLE_SUBSCRIPTIONS
GET_ALL_MATCHES = 'SELECT * ' + ' FROM ' + TABLE_ALL_MATCHES
GET_ALL_USERS = 'SELECT DISTINCT * FROM ' + TABLE_ALL_USERS
GET_ACTIVE_USERS = 'SELECT DISTINCT ' + USERNAME + ' FROM ' + TABLE_SUBSCRIPTIONS
GET_UNIQUE_SUBSCRIPTIONS = 'SELECT DISTINCT ' + SUB + ' FROM ' + TABLE_SUBSCRIPTIONS
SELECT_DISTINCT_ITEMS = 'SELECT DISTINCT ' + SUB + ' FROM ' + TABLE_SUBSCRIPTIONS
