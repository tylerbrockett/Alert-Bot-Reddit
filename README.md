# reddit-bot-buildapcsales

This is just a side project for me. I had been introduced to the Python programming language in an Artificial Intelligence class, and loved the syntax so much that I decided to explore it some more. I happened upon someone writing about how Reddit bots were primarily done using Python and the PRAW (Python Reddit API Wrapper) library, and thought I'd give it a try.

## Brief overview of how it works.

1. The bot reads unread mail from it's inbox
	1. Read message type
		1. subscribe
		2. unsubscribe
		3. unsubscribe all
		4. information
		5. feedback
		6. default
	2. If the user wants to add or remove a subscription to an item, the bot performs the necessary database operations
	3. The bot composes and sends a response letting them know what action was taken.
2. Perform database operation to gather all unique parts to look out for
3. Crawl the subreddit. For each submission in the subreddit:
	1. Make sure sale is still valid (not marked NSFW)
	2. Check if there is anyone who has a subscription term in the title that hasn't already had a match to that post and/or item
	3. If there is a match, perform database operations adding the match
	4. Send the user a message notifying them of the match
4. Let the bot sleep
