
# ======================================================================================================
#           DATABASE SUBSCRIPTIONS INFO
# ======================================================================================================

DATABASE_LOCATION = 'data/database/requests.db'

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
    " WHERE " + USERNAME + " = (?) "

SELECT_DISTINCT_PARTS = "SELECT DISTINCT " + ITEM + " FROM " + TABLE_SUBSCRIPTIONS

GET_SUBSCRIPTIONS_BY_USERNAME = "SELECT * " + \
                                "FROM " + TABLE_SUBSCRIPTIONS + " " + \
                                "WHERE username = (?)"

# ======================================================================================================
#           DATABASE MATCHES INFO
# ======================================================================================================

TABLE_MATCHES = 'matches'

COL_MATCHES_USERNAME = 0
COL_MATCHES_PART = 1
COL_MATCHES_LINK = 2

LINK = 'link'

CREATE_TABLE_MATCHES = "CREATE TABLE IF NOT EXISTS " + TABLE_MATCHES + \
               "(" + USERNAME + " TEXT, " + ITEM + " TEXT, " + LINK + " TEXT)"

# HORRIBLY unoptimal query, SQL was never a strong point...
GET_SUBSCRIBED_USERS_WITHOUT_LINK = \
    "SELECT DISTINCT * " + \
    "FROM " + TABLE_SUBSCRIPTIONS + " s " + \
    "WHERE EXISTS " + \
        "(SELECT * " + \
        "FROM " + TABLE_MATCHES + " m " + \
        "WHERE s." + USERNAME + " = m." + USERNAME + " and " + \
                "s." + ITEM + " = m." + ITEM + " and " + \
                "m." + ITEM + " = (?) and NOT EXISTS " + \
            "(SELECT * " + \
            "FROM " + TABLE_SUBSCRIPTIONS + " b " + \
            "WHERE b." + USERNAME + " = s." + USERNAME + " and b." + ITEM + " = s." + ITEM + " and EXISTS " + \
                "(SELECT * " + \
                "FROM " + TABLE_MATCHES + " v " + \
                "WHERE " + \
                    "b." + USERNAME + " = v." + USERNAME + " and " + \
                    "v." + ITEM + " = m." + ITEM + " and " + \
                    "v." + LINK + " = (?) )))"

INSERT_ROW_MATCHES = "INSERT INTO " + \
                         TABLE_MATCHES + \
                         " VALUES (?,?,?)"

REMOVE_ALL_MATCHES_BY_USERNAME = "DELETE FROM " + TABLE_MATCHES + \
    " WHERE " + USERNAME + " = (?) "

# Username defined above
# Part defined above
LINK = 'link'


