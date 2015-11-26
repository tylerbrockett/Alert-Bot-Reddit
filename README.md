# reddit-bot-buildapcsales

This is just a side project for me. I had been introduced to the Python programming language in an Artificial Intelligence class, and loved the syntax so much that I decided to explore it some more. I happened upon someone writing about how Reddit bots were primarily done using Python and the PRAW (Python Reddit API Wrapper) library, and thought I'd give it a try.

[This is a link to the Reddit post describing the bot. Essentially the same information found here](https://www.reddit.com/r/buildapcsales/comments/3u2tg5/buildapcsales_bot/)

## How It Works

***NOTE:*** For each of these fields (subject and body) capitalization does *not* matter, it will yield the exact same results.

#### To subscribe 
Send a private message to /u/sales__bot (notice ***two*** underscores) with the subject line as the item you want to receive notifications for, and the body of the message as "Subscribe". What the bot does is scans the first 100 most recent /r/buildapcsales submissions for either a title or body of a submission that matches the item you subscribed to. ***Currently, it must be an exact match to the term you gave me.*** I will work on using some sort of search in the future, but for now this will suffice. Because of this, try to keep your terms generic, e.g. use "850 evo" instead of "Samsung 850 EVO-Series 250GB 2.5" Solid State Drive". For now, feel free to have multiple subscriptions for the same item, just so I can cover the bases. By this, I mean it is okay to subscribe to "caviar black 3tb" ***and*** "caviar black series 3tb" (notice the word "series" in the middle). Do **not** subscribe to two separate things like "i7-6700k" and "6700k", since everything found for the second term covers that of the first. If all the subscriptions become unmanageable, I will change this rule. Also, if/when the search feature is implemented, in theory the multiple subscriptions for the same item won't be necessary.

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
