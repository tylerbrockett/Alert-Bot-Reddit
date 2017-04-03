"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   04/02/2017
Version:            v2.0
==========================================
"""


bot_subreddit = '/r/bots_subreddit'

accounts = {
    'bot': {
        'username': 'bot_username',
        'password': 'bot_password',
        'user_agent': 'python-praw:com.developer.bot_username:v1.0 (by /u/developer_username)',
        'client_id': 'xxxxxxxxx-xxxx',
        'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'database': 'subscriptions.db'
    },
    'beta': {
        'username': 'bot_beta_username',
        'password': 'bot_beta_password',
        'user_agent': 'python-praw:com.developer.bot_username:v1.0 (by /u/developer_username)',
        'client_id': 'xxxxxxxxx-xxxx',
        'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'database': 'BETA.db'
    },
    'developer': {
        'username': 'developer_username',
        'password': 'developer_password',
        'user_agent': 'python-praw:com.developer.bot_username:v1.0 (by /u/developer_username)',
        'client_id': 'xxxxxxxxx-xxxx',
        'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'email': 'developers_email@domain.com'
    },
    'bot_errors': {
        'username': 'bot_error_handling_account_username',
        'password': 'bot_error_handling_account_password',
        'user_agent': 'python-praw:com.developer.bot_username:v1.0 (by /u/developer_username)',
        'client_id': 'xxxxxxxxx-xxxx',
        'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
    },
    'old_bot': {
        'username': 'old_bot_username',
        'password': 'old_bot_password',
        'user_agent': 'python-praw:com.developer.old_bot_username:v1.0 (by /u/developer_username)',
        'client_id': 'xxxxxxxxx-xxxx',
        'client_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
}

bot_email = {
    'email': 'bot_email@domain.com',
    'password': 'bot_email_password'
}
