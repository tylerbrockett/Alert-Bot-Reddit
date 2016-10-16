
DATABASE_LOCATION = '/database/subscriptions.db'

# ======================================================================================================
#           DATABASE SUBSCRIPTIONS TABLE
# ======================================================================================================

TABLE_SUBSCRIPTIONS = 'subscriptions'

ROW_ID = 'row_id'
USERNAME = 'username'
MESSAGE_ID = 'message_id'
ITEM = 'item'
TIMESTAMP = 'timestamp'

COL_SUB_USERNAME = 0
COL_SUB_MESSAGE_ID = 1
COL_SUB_ITEM = 2
COL_SUB_TIMESTAMP = 3


CREATE_TABLE_SUBSCRIPTIONS = \
    "CREATE TABLE IF NOT EXISTS " + TABLE_SUBSCRIPTIONS + "(" + \
    USERNAME + " TEXT NOT NULL, " + \
    MESSAGE_ID + " TEXT NOT NULL, " + \
    ITEM + " TEXT NOT NULL, " + \
    TIMESTAMP + " REAL NOT NULL, " + \
    "PRIMARY KEY(" + USERNAME + ", " + ITEM + "));"

INSERT_ROW_SUBSCRIPTIONS = "INSERT INTO " + \
                           TABLE_SUBSCRIPTIONS + \
                         " VALUES (?,?,?,?)"

REMOVE_ROW_SUBSCRIPTIONS = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = (?) " + \
    " AND " + ITEM + " = (?)"

REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = (?)"

GET_SUBSCRIPTIONS_BY_USERNAME = "SELECT * " + \
                                "FROM " + TABLE_SUBSCRIPTIONS + " " + \
                                "WHERE username = ? " + \
                                "ORDER BY " + ITEM + " ASC"

GET_ALL_SUBSCRIPTIONS = 'SELECT * FROM ' + TABLE_SUBSCRIPTIONS

# ======================================================================================================
#           DATABASE USERS TABLE
# ======================================================================================================

TABLE_ALL_USERS = 'all_users'

CREATE_TABLE_ALL_USERS = \
    'CREATE TABLE IF NOT EXISTS ' + TABLE_ALL_USERS + '(' + \
    USERNAME + ' TEXT NOT NULL ,' + \
    'PRIMARY KEY(' + USERNAME + '));'

# ======================================================================================================
#           DATABASE MATCHES TABLES
# ======================================================================================================

TABLE_MATCHES = 'matches'
TABLE_ALL_MATCHES = 'all_matches'

COL_MATCHES_USERNAME = 0
COL_MATCHES_ITEM = 1
COL_MATCHES_LINK = 2
COL_MATCHES_TIMESTAMP = 3

LINK = 'link'

CREATE_TABLE_MATCHES = \
    "CREATE TABLE IF NOT EXISTS " + TABLE_MATCHES + "(" + \
    USERNAME + " TEXT NOT NULL, " + \
    ITEM + " TEXT NOT NULL, " + \
    LINK + " TEXT NOT NULL, " + \
    TIMESTAMP + " REAL NOT NULL, " + \
    "PRIMARY KEY(" + USERNAME + ", " + ITEM + ", " + LINK + "));"

CREATE_TABLE_ALL_MATCHES = \
    "CREATE TABLE IF NOT EXISTS " + TABLE_ALL_MATCHES + "(" + \
    USERNAME + " TEXT NOT NULL, " + \
    ITEM + " TEXT NOT NULL, " + \
    LINK + " TEXT NOT NULL, " + \
    TIMESTAMP + " REAL NOT NULL, " + \
    "PRIMARY KEY(" + USERNAME + ", " + ITEM + ", " + LINK + "));"

INSERT_ROW_MATCHES = "INSERT INTO " + \
                         TABLE_MATCHES + \
                         " VALUES (?,?,?,?)"

INSERT_ROW_ALL_MATCHES = "INSERT INTO " + \
                         TABLE_ALL_MATCHES + \
                         " VALUES (?,?,?,?)"

REMOVE_ALL_MATCHES_BY_USERNAME = "DELETE FROM " + TABLE_MATCHES + \
    " WHERE " + USERNAME + " = ? "

REMOVE_MATCHES_BY_USERNAME_AND_SUBJECT = "DELETE FROM " + TABLE_MATCHES + \
    " WHERE " + USERNAME + " = (?) " + " AND " + ITEM + " = (?)"

PURGE_OLD_MATCHES = 'DELETE FROM ' + TABLE_MATCHES + \
    ' WHERE ' + TIMESTAMP + ' <= (?)'


# ======================================================================================================
#           DATABASE ALERTS TABLE
# ======================================================================================================

COL_ALERTS_USERNAME = 0
COL_ALERTS_RECEIVED_ALERT = 1

TABLE_ALERTS = 'alerts'

RECEIVED_ALERT = 'received_alert'

CREATE_TABLE_ALERTS = "CREATE TABLE IF NOT EXISTS " + TABLE_ALERTS + \
                "(" + USERNAME + " TEXT NOT NULL, " + RECEIVED_ALERT + " INTEGER NOT NULL," + \
                "PRIMARY KEY(" + USERNAME + "));"

GET_USERNAMES_THAT_NEED_ALERT = "SELECT DISTINCT s.username " + \
                                "FROM " + TABLE_SUBSCRIPTIONS + " s " + \
                                "WHERE NOT EXISTS " + \
                                    "(SELECT DISTINCT a." + USERNAME + " " + \
                                    "FROM " + TABLE_ALERTS + " a " + \
                                    "WHERE s." + USERNAME + " = a." + USERNAME + " AND " + \
                                    "a." + RECEIVED_ALERT + " = 1)"

INSERT_ROW_ALERTS = "INSERT INTO " + TABLE_ALERTS + " VALUES (?,?)"

DROP_TABLE_ALERTS = "DROP TABLE " + TABLE_ALERTS


# ======================================================================================================
#           STATISTICS
# ======================================================================================================

COUNT_USERS = "SELECT DISTINCT " + USERNAME + " FROM " + TABLE_SUBSCRIPTIONS
COUNT_SUBSCRIPTIONS = "SELECT * FROM " + TABLE_SUBSCRIPTIONS
COUNT_UNIQUE_SUBSCRIPTIONS = "SELECT DISTINCT " + ITEM + " FROM " + TABLE_SUBSCRIPTIONS
GET_ALL_MATCHES = 'SELECT * ' + ' FROM ' + TABLE_ALL_MATCHES
GET_ALL_USERS = 'SELECT DISTINCT * FROM ' + TABLE_ALL_USERS
GET_ACTIVE_USERS = 'SELECT DISTINCT ' + USERNAME + ' FROM ' + TABLE_SUBSCRIPTIONS
GET_UNIQUE_SUBSCRIPTIONS = 'SELECT DISTINCT ' + ITEM + ' FROM ' + TABLE_SUBSCRIPTIONS
SELECT_DISTINCT_ITEMS = "SELECT DISTINCT " + ITEM + " FROM " + TABLE_SUBSCRIPTIONS
