
# ======================================================================================================
#           DATABASE SUBSCRIPTIONS INFO
# ======================================================================================================

DATABASE_LOCATION = 'Bots/buildapcsales/data/requests.db'

TABLE_SUBSCRIPTIONS = 'subscriptions'

USERNAME = 'username'
MESSAGE_ID = 'message_id'
PART = 'part'

COL_SUB_AUTHOR = 0
COL_SUB_MESSAGE_ID = 1
COL_SUB_SUBJECT = 2
COL_SUB_PART = 3

CREATE_TABLE_SUBSCRIPTIONS = "CREATE TABLE IF NOT EXISTS " + TABLE_SUBSCRIPTIONS + \
               "(" + USERNAME + " TEXT, " + MESSAGE_ID + " TEXT, " + PART + " TEXT)"

INSERT_ROW = "INSERT INTO " + \
             TABLE_SUBSCRIPTIONS + \
                " VALUES (?,?,?,?)"

REMOVE_ROW = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = ? " + \
    " AND " + PART + " = ?"

SELECT_DISTINCT_PARTS = "SELECT DISTINCT " + PART + " FROM " + TABLE_SUBSCRIPTIONS

# ======================================================================================================
#           DATABASE MATCHES INFO
# ======================================================================================================

TABLE_MATCHES = 'matches'

COL_MATCHES_USERNAME = 0
COL_MATCHES_PART = 1
COL_MATCHES_LINK = 2

LINK = 'link'

CREATE_TABLE_MATCHES = "CREATE TABLE IF NOT EXISTS " + TABLE_MATCHES + \
               "(" + USERNAME + " TEXT, " + PART + " TEXT, " + LINK + " TEXT)"

# Username defined above
# Part defined above
LINK = 'link'


