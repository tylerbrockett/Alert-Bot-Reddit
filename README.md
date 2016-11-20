# Alert Bot

This bot allows users to subscribe to certain posts based on the title, body, link, post author, etc. The bot will notify the user when it finds posts that matches what the user specifies.
This bot is excellent to keep track of subreddits that post links to sales or freebies!
[Formerly known as /u/sales__bot for /r/buildapcsales.](https://www.reddit.com/r/buildapcsales/comments/3u2tg5/buildapcsales_bot/)


## How It Works

***NOTE:*** For each of these fields (subject and body) capitalization does *not* matter, it will yield the exact same results.

#### To subscribe
Send a private message to /u/Alert_Bot with the body of the message specifying what you want the bot to look out for. Detailed grammar is found at the bottom of this page.
Essentially there is the subscribe action, and a list of parameters. Parameter List:

#####Parameter Values:
* ***-title***
    * Function:
        * Specifies words or phrases to watch out for in the title of the post. Multiple '-title' parameters can be specified, the user will be notified of the post even if only ***ONE*** of the '-title' parameters match. Each '-title' parameter also supports a comma-separated list of words or phrases, each of which need to show up to constitute a match, however order does ***NOT*** matter.
    * Examples:
        * subscribe -title cats
            * Watches for posts containing the word 'cats' in its title
        * subscribe -title cats -title dogs
            * Watches for posts containing the word 'cats' ***OR*** 'dogs' in its title.
        * subscribe -title cats, dogs
            * Watches for posts containing the words 'cats' ***AND*** 'dogs' in its title, but order doesn't matter.
        * subscribe -title funny cats
            * Watches for posts containing the phrase 'funny cats' in its title.
    * Aliases:
        * -title
        * -item
        * -items
* ***-body***
    * Function:
        * Specifies words or phrases to watch out for in the body of the post. This could be used for selftext ***OR*** links, the '-body' parameter will figure out which post type it is. This parameter is especially useful for filtering URLs from posts, such as if you only want to be notified of posts that link to *'amazon.com'* for example.
    * Examples:
        * subscribe -body cats
            * Watches for posts containing the word 'cats' in its body
        * subscribe -body cats, dogs
            * Watches for posts containing the words 'cats' ***AND*** 'dogs' in its body, but order doesn't matter.
        * subscribe -body funny cats
            * Watches for posts containing the phrase 'funny cats' in its body.
    * Aliases:
        * -body
        * -site
        * -sites
        * -url

#### Unsubscribe
To unsubscribe, either reply to the original message confirming your subscription to that item with the body as "Unsubscribe", or create a new message with the item to unsubscribe from as the subject and "Unsubscribe" as the body.

#### Unsubscribe from all
To Unsubscribe from ALL subscriptions you have, have the body be "Unsubscribe all" or some string that contains those two words (e.g. "All-unsubscribe" should work too). The subject can be whatever you want, or empty.

#### Get information
To get some detailed information, or view all your active subscriptions, send the bot a message with the subject as "Information" and the body whatever you want, or empty.

#### Send feedback
To send me feedback, send me a message with the subject as "Feedback" and the body whatever you want, or empty.

#### Default message
If you send a message that doesn't follow the above guidelines, you will get an error message from the bot saying the request wasn't recognized.


## Future Plans
The bot is currently running on my laptop, which I normally take to and from school and turn off at night. I was originally going to wait till Christmas to get a Raspberry Pi to run it, so I don't have to worry about interrupting the script. However, an ***extremely*** generous Redditor donated a Raspberry Pi for the cause (in the form of PayPal!). 


## Known Issues

1. If you subscribe to something like "i7-6700k" and "6700k" the bot will treat them as different items, and you can receive matches for both for the same link. That is because everything found for the second term covers that of the first (a little more explanation is above). I will have to edit the SQL query to exclude the item as a parameter, and make it match against username and link only.


## Edits

**11/25/15 -** I had to reset the bot to make some changes to the code. I think some of the database operations hadn't been committed or something (they should have been) so some people may have received duplicate messages. Sorry.

**11/24/15 -** A ***HUGE*** thanks goes out to /u/he_must_workout for donating a Raspberry Pi (in the form of PayPal) for the bot! The Reddit community is truly amazing!

## Developer Info

Developer Name: Tyler Brockett	

Bot Code: [Github Repository](https://github.com/tylerbrockett/reddit-bot-buildapcsales)

Reddit: /u/tylerbrockett

Email: tylerbrockett@gmail.com

&nbsp;
