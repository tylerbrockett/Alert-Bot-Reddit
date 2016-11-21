# Alert Bot

This bot allows users to subscribe to certain posts based on the title, body, link, post author, etc. The bot will notify the user when it finds posts that matches what the user specifies.
This bot is excellent to keep track of subreddits that post links to sales or freebies!
[Formerly known as /u/sales__bot for /r/buildapcsales.](https://www.reddit.com/r/buildapcsales/comments/3u2tg5/buildapcsales_bot/)


## How It Works

***NOTE:*** For each of these fields (subject and body) capitalization does *not* matter, it will yield the exact same results.

#### To subscribe
Send a private message to /u/Alert_Bot with the body of the message specifying what you want the bot to look out for. Detailed grammar is found at the bottom of this page.
Essentially there is the subscribe action, and a list of parameters. Parameter List:

#####Parameter Values
***NOTES:*** All parameters can be combined to form one specific, constrained subscription. Also note that most parameters support a comma separated list of words or phrases as well, each of which need to show up in order to constitute a match. The nice thing about this is that the order of the words does ***NOT*** matter. 

* ***-title***
    * Function:
        * Specifies words or phrases to watch out for in the title of the post. Multiple '-title' parameters can be specified, the user will be notified of the post even if only ***ONE*** of the '-title' parameters match.
    * Examples:
        * subscribe -title cats -subreddit funny
            * Watches for posts containing the word 'cats' in its title, in the /r/funny subreddit.
        * subscribe -title cats -title dogs -subreddit funny
            * Watches for posts containing the word 'cats' ***OR*** 'dogs' in its title, in the /r/funny subreddit.
        * subscribe -title funny cats -subreddit funny
            * Watches for posts containing the phrase 'funny cats' in its title, in the /r/funny subreddit.
        * subscribe -title funny cats, dogs -subreddit funny
            * Watches for posts containing the phrase 'funny cats' ***AND*** 'dogs' in its title in the /r/funny subreddit, but order of the two phrases doesn't matter.
    * Aliases:
        * -title
        * -item
        * -items
* ***-body***
    * Function:
        * Specifies words or phrases to watch out for in the body of the post. This could be used for selftext ***OR*** links, the '-body' parameter will figure out which post type it is. Multiple '-body' parameters can be specified, the user will be notified of the post even if only ***ONE*** of the '-body' parameters match. This parameter is especially useful for filtering URLs from posts, such as if you only want to be notified of posts that link to *'amazon.com'* for example.
    * Examples:
        * subscribe -body cats
            * Watches for posts containing the word 'cats' in the selftext or link.
        * subscribe -body cats -body dogs
            * Watches for posts containing the word 'cats' ***OR*** 'dogs' in the selftext or link.
        * subscribe -body funny cats
            * Watches for posts containing the phrase 'funny cats' in its selftext or link.
        * subscribe -body funny cats, dogs
            * Watches for posts containing the phrase 'funny cats' ***AND*** 'dogs' in its selftext or link, but order of the two phrases doesn't matter.
    * Aliases:
        * -body
        * -site
        * -sites
        * -url
        * -content
        * -selftext
        * -link
* ***-redditors***
    * Function:
        * Use this parameter to only be notified for posts when they are by specified users. It should go without saying, but if multiple redditors are specified, there only needs to be a match for one to constitute a match. **NOTE:** The '/u/' or 'u/' prefixes for redditors will be stripped, so it doesn't matter if you include it or not.
    * Examples:
        * subscribe -title cats -redditor tylerbrockett -subreddit videos
            * Watches for posts containing 'cats' in the title, by the user /u/tylerbrockett, in the subreddit /r/videos
        * subscribe -title cats -redditor tylerbrockett, made-up-name -subreddit videos
            * Watches for posts containing 'cats' in the title, by the user /u/tylerbrockett ***OR*** /u/made-up-name, in the subreddit /r/videos
    * Aliases:
        * -redditor
        * -redditors
        * -user
        * -users
* **-ignore-title**
    * Function:
        * Specified words or phrases to ignore in the title of the post. If any single word or phrase in this parameter is found in the title of the post, the post will be ignored.
    * Examples:
        * subscribe -title cats -ignore-title chased by dog -subreddit videos
            * Watches for posts containing 'cats' in the title, which do not contain 'chased by dog' in the title, in the /r/videos subreddit.
        * subscribe -title cats -ignore-title cucumber, dog -subreddit startledcats
            * Watches for posts containing 'cats' in the title, which do not contain 'cucumber' ***OR*** 'dog' in the title, in the subreddit /r/StartledCats. [Cucumber reference.](https://www.reddit.com/r/StartledCats/comments/3cl2gn/cat_vs_cucumber/?ref=search_posts)
    * Aliases:
        * -ignore-title
        * -ignore-item
        * -ignore-items
* **-ignore-body**
    * Function:
        * Specified words or phrases to ignore in the body of the post. This could be used for selftexts ***OR*** links. If any single word or phrase in this parameter is found in the body of the post, the post will be ignored.
    * Examples:
        * subscribe -title cats -ignore-body chased by dog -subreddit videos
            * Watches for posts containing 'cats' in the title, which do not contain 'chased by dog' in the selftext or link, in the /r/videos subreddit.
        * subscribe -title cats -ignore-body cucumber, dog -subreddit startledcats
            * Watches for posts containing 'cats' in the title, which do not contain 'cucumber' ***OR*** 'dog' in the selftext or link, in the subreddit /r/StartledCats. [Cucumber reference.](https://www.reddit.com/r/StartledCats/comments/3cl2gn/cat_vs_cucumber/?ref=search_posts)
    * Aliases:
        * -ignore-body
        * -ignore-site
        * -ignore-sites
        * -ignore-url
        * -ignore-content
        * -ignore-selftext
        * -ignore-link
* ***-ignore-redditors***
    * Function:
        * Use this parameter to ignore posts when they are by specified users. It should go without saying, but if multiple redditors are specified, there only needs to be a match for one in order to ignore the post. **NOTE:** The '/u/' or 'u/' prefixes for redditors will be stripped, so it doesn't matter if you include it or not.
    * Examples:
        * subscribe -title cats -ignore-redditor tylerbrockett -subreddit videos
            * Watches for posts containing 'cats' in the title, ***NOT*** by the user /u/tylerbrockett, in the subreddit /r/videos
        * subscribe -title cats -redditor tylerbrockett, made-up-name -subreddit videos
            * Watches for posts containing 'cats' in the title, ***NOT*** by the user /u/tylerbrockett ***OR*** /u/made-up-name, in the subreddit /r/videos
    * Aliases:
        * -ignore-redditor
        * -ignore-redditors
        * -ignore-user
        * -ignore-users
* ***-subreddit***
    * Function:
        * Specifies which subreddits to look in to match against the other parameters. Multiple subreddits can be specified, separated by a comma, and the bot will look in all of them. Although you can technically subscribe to /r/all, I wouldn't recommend it, because some posts will inevitably slip through the cracks. Also, it could hog the bots resources sending out messages to all the posts, so I may remove the ability to do this later depending on how it goes. ***NOTE:*** If no subreddit is specified here, /r/buildapcsales will be used by default, because that what the subreddit that gave this bot life to begin with. Also note that the '/r/' or 'r/' prefixes for subreddits will be stripped, so it doesn't matter if you include it or not.
    * Examples:
        * subscribe -title cats -subreddit funny
            * Watches for posts containing 'cats' in the title in the subreddit /r/funny
        * subscribe -title cats -subreddit /r/funny, /r/videos
            * Watches for posts containing 'cats' in the title in the subreddits /r/funny and /r/videos
    * Aliases:
        * -subreddit
        * -subreddits
        
#####Flags:
* ***-nsfw***
    * Function:
        * By default, the bot will ignore posts that are marked as NSFW. Some subreddits use this tag to mark posts as expired and for other reasons. This tag will ***NOT*** ignore these posts.
    * Examples:
        * subscribe -title CPU, Intel i7 -subreddit BuildAPCSales -nsfw
            * Searches for posts containing 'CPU' and 'Intel i7' in the title of the posts, ***INCLUDING*** the expired sales.
    * Aliases:
        * -nsfw
        * -show-nsfw
        

#### Unsubscribe
There are 3 ways to unsubscribe from posts.
* ***Unsubscribe All -*** Send the bot a message with the body as 'unsubscribe all' in order to stop being notified of any posts.
* ***Unsubscribe by reply -*** Reply to an alert with 'unsubscribe' in order to remove that subscription.
* ***Unsubscribe by subscription number -*** Send the bot a message with 'ubsubscribe {subscription #}' (where the brackets are the actual subscription number) in order to remove that subscription.

#### Getting Help
To get detailed information on how the bot works, send the bot a message with the subject or body as 'help'.

#### Send feedback
To send me feedback, send me a message with the subject as "Feedback" and the body whatever you want, or empty. Another way is to have the subject be whatever you want, and the body be 'Feedback {Feedback message here}' where the brackets are replaced with your actual feedback message.

#### Reject message
If you send a message that doesn't follow the above guidelines, you will get an error message from the bot saying the request wasn't recognized.

## Future Plans
* I think the next major feature I want to add is the ability to send out email notifications if the user specifies it.

## Known Issues
1. Be careful with how you are specifying your subscriptions. It is EXTREMELY easy to wind up with subscriptions that overlap, and thus you're being notified twice for the same post.

## Edits
**11/24/15 -** A ***HUGE*** thanks goes out to /u/he_must_workout for donating a Raspberry Pi (in the form of PayPal) for the bot! The Reddit community is truly amazing!

## Developer Info
Developer Name: Tyler Brockett 

Bot Code: [Github Repository](https://github.com/tylerbrockett/Alert-Bot-Reddit) 

Bot Subreddit: [/r/Alert_Bot](https://reddit.com/r/Alert_Bot) 

Reddit: /u/tylerbrockett 

Email: tylerbrockett@gmail.com 
