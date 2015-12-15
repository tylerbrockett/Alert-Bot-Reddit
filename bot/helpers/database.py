
# ======================================================================================================
#           DATABASE SUBSCRIPTIONS TABLE
# ======================================================================================================

DATABASE_LOCATION = '/database/subscriptions.db'

TABLE_SUBSCRIPTIONS = 'subscriptions'

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
    "PRIMARY KEY(" + USERNAME + ", " + ITEM + ")) " + \
    "WITHOUT ROWID;"

INSERT_ROW_SUBMISSIONS = "INSERT INTO " + \
                         TABLE_SUBSCRIPTIONS + \
                         " VALUES (?,?,?,?)"

REMOVE_ROW_SUBSCRIPTIONS = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = (?) " + \
    " AND " + ITEM + " = (?)"

REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = (?)"

SELECT_DISTINCT_ITEMS = "SELECT DISTINCT " + ITEM + " FROM " + TABLE_SUBSCRIPTIONS

GET_SUBSCRIPTIONS_BY_USERNAME = "SELECT * " + \
                                "FROM " + TABLE_SUBSCRIPTIONS + " " + \
                                "WHERE username = ?"

# ======================================================================================================
#           DATABASE MATCHES TABLE
# ======================================================================================================

TABLE_MATCHES = 'matches'

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
    "PRIMARY KEY(" + USERNAME + ", " + ITEM + ", " + LINK + ")) " + \
    "WITHOUT ROWID;"

# HORRIBLY suboptimal query, SQL was never a strong point...
GET_SUBSCRIBED_USERS_WITHOUT_LINK = \
    "SELECT DISTINCT * " + \
    "FROM " + TABLE_SUBSCRIPTIONS + " s " + \
    "WHERE s." + ITEM + " = (?) and NOT EXISTS " + \
        "(SELECT * " + \
        "FROM " + TABLE_SUBSCRIPTIONS + " b " + \
        "WHERE s." + USERNAME + " = b." + USERNAME + " and " + \
              "s." + ITEM + " = b." + ITEM + " and EXISTS " + \
            "(SELECT * " + \
            "FROM " + TABLE_MATCHES + " m " + \
            "WHERE b." + ITEM + " = m." + ITEM + " and " + \
                  "b." + USERNAME + " = m." + USERNAME + " and " + \
                  "m." + LINK + " = (?) ))"

INSERT_ROW_MATCHES = "INSERT INTO " + \
                         TABLE_MATCHES + \
                         " VALUES (?,?,?)"

REMOVE_ALL_MATCHES_BY_USERNAME = "DELETE FROM " + TABLE_MATCHES + \
    " WHERE " + USERNAME + " = ? "

REMOVE_MATCHES_BY_USERNAME_AND_SUBJECT = "DELETE FROM " + TABLE_MATCHES + \
    " WHERE " + USERNAME + " = (?) " + " AND " + ITEM + " = (?)"


# ======================================================================================================
#           DATABASE ALERTS TABLE
# ======================================================================================================

COL_ALERTS_USERNAME = 0
COL_ALERTS_RECEIVED_ALERT = 1

TABLE_ALERTS = 'alerts'

RECEIVED_ALERT = 'received_alert'

CREATE_TABLE_ALERTS = "CREATE TABLE IF NOT EXISTS " + TABLE_ALERTS + \
                "(" + USERNAME + " TEXT NOT NULL, " + RECEIVED_ALERT + " INTEGER NOT NULL," + \
                "PRIMARY KEY(" + USERNAME + ")) WITHOUT ROWID;"

GET_USERNAMES_THAT_NEED_ALERT = "SELECT DISTINCT s.username " + \
                                "FROM " + TABLE_SUBSCRIPTIONS + " s " + \
                                "WHERE NOT EXISTS " + \
                                    "(SELECT DISTINCT a." + USERNAME + " " + \
                                    "FROM " + TABLE_ALERTS + " a " + \
                                    "WHERE s." + USERNAME + " = a." + USERNAME + " AND " + \
                                    "a." + RECEIVED_ALERT + " = 1)"

INSERT_ROW_ALERTS = "INSERT INTO " + TABLE_ALERTS + " VALUES (?,?)"

DROP_TABLE_ALERTS = "DROP TABLE " + TABLE_ALERTS
