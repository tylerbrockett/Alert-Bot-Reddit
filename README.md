# Alert Bot

This bot allows users to subscribe to certain posts based on the title, body, link, post author, etc. The bot will notify the user when it finds posts that matches what the user specifies.
This bot is excellent to keep track of subreddits that post links to sales or freebies!
[Formerly known as /u/sales__bot for /r/buildapcsales.](https://www.reddit.com/r/buildapcsales/comments/3u2tg5/buildapcsales_bot/)


## Donate
If you really like the bot, please consider making a donation for my time. Thanks! 

[![Donate](https://www.paypal.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=KYGVTRSAMLKJ4)



# How It Works

***Note:*** For each of these fields (subject and body) capitalization does *not* matter, it will yield the exact same results.

## To subscribe

Send a [private message to /u/Alert_Bot](https://www.reddit.com/message/compose/?to=alert_bot) with the body of the message specifying what you want the bot to look out for. The body of the message is what the bot cares about, so the following examples should be in the body of the message. The subject of the message can be anything, but I recommend making it descriptive to you, so you can see what the message is about at a quick glance.
Essentially there is the subscribe action, and a list of parameters. Parameter List:

### Parameter Values

***Notes:*** All parameters can be combined to form one specific, constrained subscription. Order of parameters does ***not*** matter. Also note that most parameters support a comma separated list of words or phrases as well, each of which need to show up in order to constitute a match. The nice thing about this is that the order of the words does ***not*** matter. 

### -title *\<parameter list\>*

The ***-title*** parameter specifies words or phrases to watch out for in the title of the post. A list of words or phrases can be specified in each ***-title*** parameter, separated by a comma. All words or phrases in each element of the list must be present in the title, but order of the words or phrases doesn't matter. Multiple ***-title*** parameters can be specified. In that case, only one of the ***-title*** parameters needs to match.

**Examples:**

*subscribe -title cats -subreddit funny*
- Watches for posts containing the word 'cats' in its title, in the /r/funny subreddit.

*subscribe -title cats -title dogs -subreddit funny*
- Watches for posts containing the word 'cats' ***OR*** 'dogs' in its title, in the /r/funny subreddit.

*subscribe -title funny cats -subreddit funny*
- Watches for posts containing the phrase 'funny cats' in its title, in the /r/funny subreddit.

*subscribe -title funny cats, dogs -subreddit funny*
- Watches for posts containing the phrase 'funny cats' ***AND*** 'dogs' in its title in the /r/funny subreddit, but order of the two phrases doesn't matter.

**Aliases:**
* -title
* -item
* -items

        
### -body *\<parameter list\>*

The ***-body*** parameter specifies words or phrases to watch out for in the body of the post. A list of words or phrases can be specified in each ***-body*** parameter, separated by a comma. All words or phrases in each element of the list must be present in the body, but order of the words or phrases doesn't matter. Multiple ***-body*** parameters can be specified. In that case, only one of the ***-body*** parameters needs to match.

**Examples:**

*subscribe -body cats*
- Watches for posts containing the word 'cats' in the selftext or link.

*subscribe -body cats -body dogs*
- Watches for posts containing the word 'cats' ***OR*** 'dogs' in the selftext or link.

*subscribe -body funny cats*
- Watches for posts containing the phrase 'funny cats' in its selftext or link.

*subscribe -body funny cats, dogs*
- Watches for posts containing the phrase 'funny cats' ***AND*** 'dogs' in its selftext or link, but order of the two phrases doesn't matter.

**Aliases:**
* -body
* -site
* -sites
* -url
* -content
* -selftext
* -link


### -redditor *\<parameter list\>*

The ***-redditor*** parameter is used to filter posts from a subreddit by a specific user. A list of redditors can be specified, separated by a comma. If multiple redditors are specified, only one redditor needs to be present to constitute a match.    
***Note:*** The '/u/' or 'u/' prefixes for redditors will be stripped, so it doesn't matter if you include it or not.

**Examples:**

*subscribe -title cats -redditor tylerbrockett -subreddit videos*
- Watches for posts containing 'cats' in the title, by the user /u/tylerbrockett, in the subreddit /r/videos

*subscribe -title cats -redditor tylerbrockett, made-up-name -subreddit videos*
- Watches for posts containing 'cats' in the title, by the user /u/tylerbrockett ***OR*** /u/made-up-name, in the subreddit /r/videos

**Aliases:**
* -redditor
* -redditors
* -user
* -users

### -ignore-title *\<parameter list\>*

The ***-ignore-title*** parameter is used when you want to ignore posts that contain the specified words or phrases. A list of words or phrases can be specified, separated by a comma. If only ***one*** word or phrase in that list matches, the post is ignored.

**Examples:**

*subscribe -title cats -ignore-title chased by dog -subreddit videos*
- Watches for posts containing 'cats' in the title, which do not contain 'chased by dog' in the title, in the /r/videos subreddit.

*subscribe -title cats -ignore-title cucumber, dog -subreddit startledcats*
-Watches for posts containing 'cats' in the title, which do not contain 'cucumber' ***OR*** 'dog' in the title, in the subreddit /r/StartledCats. [Cucumber reference.](https://www.reddit.com/r/StartledCats/comments/3cl2gn/cat_vs_cucumber/?ref=search_posts)

**Aliases:**
* -ignore-title
* -ignore-item
* -ignore-items

### -ignore-body *\<parameter list\>*

The ***-ignore-title*** parameter is used when you want to ignore posts that contain the specified words or phrases. A list of words or phrases can be specified, separated by a comma. If only ***one*** word or phrase in that list matches, the post is ignored.

**Examples:**

*subscribe -title cats -ignore-body chased by dog -subreddit videos*
- Watches for posts containing 'cats' in the title, which do not contain 'chased by dog' in the selftext or link, in the /r/videos subreddit.

*subscribe -title cats -ignore-body cucumber, dog -subreddit startledcats*
- Watches for posts containing 'cats' in the title, which do not contain 'cucumber' ***OR*** 'dog' in the selftext or link, in the subreddit /r/StartledCats. [Cucumber reference.](https://www.reddit.com/r/StartledCats/comments/3cl2gn/cat_vs_cucumber/?ref=search_posts)

**Aliases:**
* -ignore-body
* -ignore-site
* -ignore-sites
* -ignore-url
* -ignore-content
* -ignore-selftext
* -ignore-link

### -ignore-redditor *\<parameter list\>*

The ***-ignore-redditor*** parameter is used to ignore posts from a subreddit by a specific user. A list of redditors can be specified, separated by a comma. If multiple redditors are specified, only one redditor needs to be present for the post to be ignored.    
***Note:*** The '/u/' or 'u/' prefixes for redditors will be stripped, so it doesn't matter if you include it or not.

**Examples:**

*subscribe -title cats -ignore-redditor tylerbrockett -subreddit videos*
- Watches for posts containing 'cats' in the title, ***NOT*** by the user /u/tylerbrockett, in the subreddit /r/videos

*subscribe -title cats -redditor tylerbrockett, made-up-name -subreddit videos*
- Watches for posts containing 'cats' in the title, ***NOT*** by the user /u/tylerbrockett ***OR*** /u/made-up-name, in the subreddit /r/videos

**Aliases:**
* -ignore-redditor
* -ignore-redditors
* -ignore-user
* -ignore-users


### -subreddit *\<parameter list\>*

The ***-subreddit*** parameter specifies which subreddits to look in for posts matching your criteria. A list of subreddits can be specified, separated by a comma, and the bot will look in all of them.    
***Note:*** Also note that the '/r/' or 'r/' prefixes for subreddits will be stripped, so it doesn't matter if you include it or not.    
***Also Note:*** If no subreddit is specified here, /r/buildapcsales will be used by default, because that is the subreddit that gave this bot life to begin with. 

**Examples:**

*subscribe -title cats -subreddit funny*
- Watches for posts containing 'cats' in the title in the subreddit /r/funny

*subscribe -title cats -subreddit /r/funny, /r/videos*
- Watches for posts containing 'cats' in the title in the subreddits /r/funny and /r/videos

**Aliases:**
* -subreddit
* -subreddits
        
#### Flags:
Flags do not take a parameter list as an argument.

### -nsfw
By default, the bot will ignore posts that are marked as NSFW. Some subreddits use this tag to mark posts as expired and for other reasons. This tag will remove the default "ignore nsfw posts" behavior.

**Examples:**

*subscribe -title CPU, Intel i7 -subreddit BuildAPCSales -nsfw*
- Searches for posts containing 'CPU' and 'Intel i7' in the title of the posts, ***including*** the expired sales.

**Aliases:**
* -nsfw
* -show-nsfw
        

#### Unsubscribe
There are 3 ways to unsubscribe from posts. All of these require sending the message as the **body** of the message. The subject doesn't matter.
* **Unsubscribe All -** Send the bot the message ***'unsubscribe all'*** in order to stop being notified of any posts.
* **Unsubscribe by reply -** Reply to an alert with ***'unsubscribe'*** in order to remove that subscription.
* **Unsubscribe by subscription number -** Send the bot a message with ***'unsubscribe #'*** (where the '#' symbol is the actual subscription number) in order to remove that subscription. This requires knowing the order you subscribed in, or by sending the bot a message with "subs" or "subscriptions" to find out.

#### Viewing your subscriptions
Send the bot a message with the body of the message as either ***"subs"*** or ***"subscriptions"***, and it will reply with a list of your subscriptions and the order in which you subscribed.

#### Viewing Statistics
If you're a nerd like me, you can get the bot to send you statistics on it. Send the bot a message with either ***"stats"*** or ***"statistics"***. The bot will respond with the number of users subscribed, the number of subscriptions it's handling, the number of subsreddits it's parsing for the subscriptions, etc.

#### Getting Help
To get detailed information on how the bot works, send the bot a message with the subject or body as 'help'.

#### Reject message
If you send a message that doesn't follow the above guidelines, you will get an error message from the bot saying the request wasn't recognized.

## Future Plans
* Ability to edit subscription (add/remove parameters)
* Ability to send out email notifications if the user specifies it

## Issues / things to watch out for
1. Be careful with how you are specifying your subscriptions. It is EXTREMELY easy to wind up with subscriptions that overlap, and thus you're being notified twice for the same post.

## Edits
**11/24/15 -** A ***HUGE*** thanks goes out to /u/he_must_workout for donating a Raspberry Pi (in the form of PayPal) for the bot! The Reddit community is truly amazing!

## Developer Info
Developer Name: Tyler Brockett 

Bot Code: [Github Repository](https://github.com/tylerbrockett/Alert-Bot-Reddit) 

Bot Subreddit: [/r/Alert_Bot](https://reddit.com/r/Alert_Bot) 

Reddit: [/u/tylerbrockett](https://reddit.com/u/tylerbrockett) 

Email: [My Email](mailto:tylerbrockett@gmail.com)
