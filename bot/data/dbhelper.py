
# ======================================================================================================
#           DATABASE SUBSCRIPTIONS INFO
# ======================================================================================================

DATABASE_LOCATION = '/data/database/subscriptions.db'

TABLE_SUBSCRIPTIONS = 'subscriptions'

USERNAME = 'username'
MESSAGE_ID = 'message_id'
ITEM = 'item'

COL_SUB_USERNAME = 0
COL_SUB_MESSAGE_ID = 1
COL_SUB_ITEM = 2

CREATE_TABLE_SUBSCRIPTIONS = "CREATE TABLE IF NOT EXISTS " + TABLE_SUBSCRIPTIONS + \
               "(" + USERNAME + " TEXT, " + MESSAGE_ID + " TEXT, " + ITEM + " TEXT)"

INSERT_ROW_SUBMISSIONS = "INSERT INTO " + \
                         TABLE_SUBSCRIPTIONS + \
                         " VALUES (?,?,?)"

REMOVE_ROW_SUBSCRIPTIONS = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = (?) " + \
    " AND " + ITEM + " = (?)"

REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME = "DELETE FROM " + TABLE_SUBSCRIPTIONS + \
    " WHERE " + USERNAME + " = (?)"

SELECT_DISTINCT_PARTS = "SELECT DISTINCT " + ITEM + " FROM " + TABLE_SUBSCRIPTIONS

GET_SUBSCRIPTIONS_BY_USERNAME = "SELECT * " + \
                                "FROM " + TABLE_SUBSCRIPTIONS + " " + \
                                "WHERE username = ?"

# ======================================================================================================
#           DATABASE MATCHES INFO
# ======================================================================================================

TABLE_MATCHES = 'matches'

COL_MATCHES_USERNAME = 0
COL_MATCHES_ITEM = 1
COL_MATCHES_LINK = 2

LINK = 'link'

CREATE_TABLE_MATCHES = "CREATE TABLE IF NOT EXISTS " + TABLE_MATCHES + \
               "(" + USERNAME + " TEXT, " + ITEM + " TEXT, " + LINK + " TEXT)"

# HORRIBLY unoptimal query, SQL was never a strong point...
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
