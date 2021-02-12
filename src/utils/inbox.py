"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from utils.env import env, BOT_USERNAME, DEV_USERNAME, SUBREDDIT

GITHUB_HOME = 'https://github.com/tylerbrockett/Alert-Bot-Reddit'
GITHUB_README = 'https://github.com/tylerbrockett/Alert-Bot-Reddit/blob/master/README.md'


def format_subject(s):
    while len(s) >= 3 and s[:3].lower() == 're:':
        s = s[3:]
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]
    return s


def format_subscription_list(subs, title):
    result = '##' + title + '\n'
    i = 0
    if len(subs) == 0:
        result += 'No Subscriptions'
    for sub in subs:
        i += 1
        result += sub.to_table('Subscription #' + str(i)) + '\n \n'
    return result


def compose_greeting(username):
    return 'Hi /u/' + username + ',\n\n'


def compose_salutation():
    result = '\n\t \n\t \n-/u/' + env(BOT_USERNAME) + '\n\t \n\t \n' + \
             env(SUBREDDIT) + ' | ' + \
             '/u/' + env(DEV_USERNAME) + ' | ' + \
             '[Bot Code](' + GITHUB_HOME + ')\n'
    return result


DEFAULT_SUB_MESSAGE = '\t \n**Note:** No subreddit was specified, so /r/buildapcsales will be used by default\t \n'


def compose_subscribe_message(username, new_sub, subs, subreddit_not_specified):
    result = compose_greeting(username) + \
             'Thanks for your subscription. ' + \
             'You will continue to receive updates for posts that match your new subscription. ' + \
             'To unsubscribe, send me a message with the body "unsubscribe #" (without quotes) where "#" is the ' + \
             'actual subscription number.\t \nAlternatively, you can reply to this message or any replies from ' + \
             'the bot in regards to this subscription and reply with "unsubscribe" as the body.\t \n' + \
             (DEFAULT_SUB_MESSAGE if subreddit_not_specified else '') + \
             new_sub.to_table('New Subscription') + '\t \n\t \n' + \
             format_subscription_list(subs, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_all_subscriptions_message(username, all_subscriptions):
    result = compose_greeting(username) + \
             format_subscription_list(all_subscriptions, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_duplicate_subscription_message(username, existing_sub, new_sub):
    result = compose_greeting(username) + \
             'We think you already have an existing subscription matching the criteria specified. Below ' + \
             'both subscriptions are listed. If you believe there has been a mistake, please visit ' + \
             env(SUBREDDIT) + ' or message /u/' + env(DEV_USERNAME) + '.\n\n' + \
             existing_sub.to_table('Existing Subscription') + '\n\n' + \
             new_sub.to_table('New Subscription') + '\n' + \
             compose_salutation()
    return result


def compose_help_message(username, subs):
    result = compose_greeting(username) + \
             'Please visit the bot\'s [Github Readme](' + GITHUB_README + ') for ' + \
             'detailed information on how the bot works. If you still have questions, please visit ' + \
             env(SUBREDDIT) + ' or message /u/' + env(DEV_USERNAME) + '. Thanks!\t \n\t \n' + \
             format_subscription_list(subs, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_unsubscribe_invalid_sub_message(username, subs):
    result = compose_greeting(username) + \
        'I\'m sorry, but it looks like the subscription you\'re trying to unsubscribe from is invalid. Please ' + \
        'make sure you are replying to a message that was in regards to a valid and active subscription. If you ' + \
        'think you are receiving this message in error, please visit ' + env(SUBREDDIT) + ' or message ' + \
        '/u/' + env(DEV_USERNAME) + ' to get this sorted out.\n\n' + \
        format_subscription_list(subs, 'Your Subscriptions') + \
        compose_salutation()
    return result


def compose_unsubscribe_message(username, removed_subs, subs):
    result = compose_greeting(username) + \
             'You have unsubscribed from the following item. Thanks for using the bot!\n\n' + \
             removed_subs[0].to_table('Unsubscribed From') + \
             '\n' + \
             format_subscription_list(subs, 'Your Subscriptions') + \
             compose_salutation()
    return result


def compose_unsubscribe_all_message(username):
    result = compose_greeting(username) + \
             'You have successfully unsubscribed from all subscriptions.' + \
             compose_salutation()
    return result


def compose_unsubscribe_from_num_message(username, removed_sub, subs):
    result = compose_greeting(username) + \
        'You have successfully unsubscribed from the following item.\t \n\t \n' + \
        removed_sub.to_table('Unsubscribed From') + '\t \n\t \n' + \
        format_subscription_list(subs, 'Your Subscriptions') + \
        compose_salutation()
    return result


def compose_edit_message(username):
    result = compose_greeting(username) + \
        'Unfortunately, the bot has only partially implemented this feature, so it is not available quite ' + \
        'yet. Please try again at a later date. Sorry for the inconvenience! ' + \
        compose_salutation()
    return result


def compose_feedback_message(username):
    result = compose_greeting(username) + \
             'Thank you very much for your feedback! \t \n' + \
             'I am open to whatever requests the community makes. If your message is urgent, please feel free to ' + \
             'PM me at /u/' + env(DEV_USERNAME) + '. Thanks again!' + \
             compose_salutation()
    return result


def compose_reject_message(username, subject, body, error):
    result = compose_greeting(username) + \
             '**There was an error processing your request.** Please review your message and ' + \
             'make sure it follows [the guidelines](' + GITHUB_README + ') that have been set. ' + \
             'You can also visit ' + env(SUBREDDIT) + ' or message /u/' + env(DEV_USERNAME) + \
             '. Thank you for your patience! \n\t \n\t \n' + \
             '**Error:** \t \n' + \
             error + '\t \n\t \n' + \
             '**Your request:** \t \n' + \
             'Subject:\t' + subject + '\t \n' + \
             'Body:   \t' + body + \
             compose_salutation()
    return result


def format_subreddit_list(subreddits, title):
    i = 0
    result = '###' + title + '\n' + \
             '\#|Subreddit' + '\n' + \
             ':--|:--' + '\n'
    for subreddit in subreddits:
        i += 1
        result += str(i) + '|' + str(subreddit) + '\n'
    return result


def compose_invalid_subreddit_message(username, invalid_subreddits, message):
    result = compose_greeting(username) + \
        'Unfortunately, it appears that the following subreddit(s) you tried to subscribe to were invalid. If you ' + \
        'believe this is a mistake please visit ' + env(SUBREDDIT) + ' or message ' + \
        '/u/' + env(DEV_USERNAME) + '. Sorry for the inconvenience!\t \n\t \n' + \
        '**Subject:**\t' + message.subject + '\t \n' + \
        '**Body:**\t\t' + message.body + '\t \n' + \
        format_subreddit_list(invalid_subreddits, 'Invalid Subreddits') + \
        compose_salutation()
    return result


def format_submission_body_summary(submission):
    if submission.is_self:
        return '**Body Text:**\t \n' + submission.selftext[:500] + (submission.selftext[500:] and '...')
    else:
        return '**Post Content Link:**\t \n[Content Link](' + submission.url + ')'


def compose_match_message(sub, submission, subs):
    result = compose_greeting(sub.username) + \
        '**Post Title:**\t \n' + \
        '[' + submission.title + '](' + submission.permalink + ')\t \n\t \n' + \
        format_submission_body_summary(submission) + '\t \n\t \n' + \
        sub.to_table('Matched Subscription') + '\t \n\t \n' + \
        'Reply to the bot with "subs" or "subscriptions" to view your subscriptions. Reply with "unsub", ' + \
        '"unsubscribe", or "stop" to remove this subscription.' + \
        compose_salutation()
    return result


def compose_too_generic_message(username):
    result = compose_greeting(username) + \
        'Unfortunately, your subscription request is too generic. Allowing such a subscription would probably hog ' + \
        'the bot\'s resources. Try constraining the subscription a bit. Sorry, and thanks for your understanding.' + \
        compose_salutation()
    return result


def format_subreddits(subreddits):
    result = '###Subreddits\n'
    if len(subreddits) == 0:
        result += 'No Results'
        return result
    result += \
        '\#|Subreddit|# of Subscriptions\n' + \
        ':--|:--:|:--\n'
    i = 0
    for sub in subreddits:
        i += 1
        result += \
            str(i) + '|' + '/r/' + sub[0] + '|' + str(sub[1]) + '\n'
    return result


def compose_statistics(username, current_users, all_users, unique_subs, all_subs, unique_subreddits, all_matches, subreddits):
    result = compose_greeting(username) + \
        '###Statistics\n' + \
        'Statistic|Value\n' + \
        ':--|:--:' + '\n' + \
        'Current Users Subscribed|' + str(current_users) + '\n' + \
        'Total Users|' + str(all_users) + '\n' + \
        'Unique Subscriptions|' + str(unique_subs) + '\n' + \
        'Active Subscriptions|' + str(all_subs) + '\n' + \
        'Unique Subreddits|' + str(unique_subreddits) + '\n' + \
        'Total Matches to Date|' + str(all_matches) + '\n\n\n' + \
        format_subreddits(subreddits) + '\n\n\n' + \
        'Thank ***YOU*** for being a part of that!\n' + \
        compose_salutation()
    return result


def compose_feedback_forward(developer_username, username, body):
    result = compose_greeting(developer_username) + \
             'You have received feedback from /u/' + username + '. The feedback is quoted below:\n\n"' + \
             body + '"' + compose_salutation()
    return result


def compose_username_mention_forward(developer_username, username, body):
    result = compose_greeting(developer_username) + \
             'The bot has been mentioned in a post! the body of the message is quoted below:\n\n' + \
             'USERNAME: ' + username + '\t \nBODY:\n' + body
    return result


def compose_username_mention_reply(username):
    result = 'Hi /u/' + username + ', thanks for the mention!\t \n ' + \
             'For those of you that don\'t know about this bot, it\'s purpose is to peruse Reddit for you, and ' + \
             'alert you when it finds a match based on what you tell it to look for. You can filter by subreddit, ' + \
             'words/phrases in the title or selftext/link of the post, the Redditor that created the post, etc. ' + \
             'It is great for finding things you want in subreddits with sales or giveaways! ' + \
             'For more information, please visit [the Github README](' + GITHUB_README + ').' + \
             compose_salutation()
    return result


def compose_post_reply_forward(developer_username, username, body):
    result = compose_greeting(developer_username) + \
             'Someone has responded to a post by the bot! the comment is quoted below:\n\n' + \
             'USERNAME: ' + username + '\nBODY:\n' + body
    return result
