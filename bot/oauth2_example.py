import praw
import webbrowser
from private import accounts

if __name__ == "__main__":
    reddit = praw.Reddit(user_agent=accounts.user_agent)
    reddit.set_oauth_app_info(client_id=accounts.client_id,
                              client_secret=accounts.client_secret,
                              redirect_uri=accounts.redirect_uri)

    '''
    Info has been taken from these resources:

    https://www.youtube.com/watch?v=Uvxu2efXuiY&feature=youtu.be
    https://www.reddit.com/r/redditdev/comments/3dm9af/is_praw_login_function_going_to_be_removed/

    1) Get authorize URL and open in browser.
    2) Once opened, accept the prompt
    3) Since the redirect will fail, copy the
        text after the "code=" in the url
    '''
    # url = reddit.get_authorize_url('...', accounts.scopes, True)
    # webbrowser.open(url)

    '''
    4) Using the authorization code, get the refresh token
    '''
    # t = reddit.get_access_information(accounts.auth_code)
    # print t

    '''
    5) Every 60 minutes, you must refresh the access
        information using the refresh token
    '''
    reddit.refresh_access_information(accounts.refresh_token)

    '''
    6) Check if it works!
    '''
    print reddit.user
