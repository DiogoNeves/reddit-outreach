"""
Utility functions to interact with Reddit, including initialization
and subreddit search.
"""

import praw
import praw.models
import webbrowser
from typing import List
from oauth_server import get_auth_code_from_server

def init_reddit(client_id: str, client_secret: str, user_agent: str,
                redirect_uri: str) -> praw.Reddit:
    """
    Initialize and return a Reddit instance using OAuth2.

    :param client_id: Reddit API client ID.
    :param client_secret: Reddit API client secret.
    :param user_agent: Reddit API user agent.
    :param redirect_uri: Redirect URI for OAuth2.
    :return: Initialized Reddit instance.
    :raises: RuntimeError if there is an error during authentication.
    """
    print("Initializing Reddit with the following parameters:")

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         redirect_uri=redirect_uri)

    # Obtain the URL for user authentication
    auth_url = reddit.auth.url(['*'], 'secrethorseshoe', 'permanent')
    print(f"Please go to this URL and authorize the application: {auth_url}")

    # Open the URL in the web browser for the user to authenticate
    webbrowser.open(auth_url)

    # Start the async HTTP server and wait for the authorization code
    code = get_auth_code_from_server()

    print(f"Authorization Code: {code}")

    # Obtain the refresh token
    try:
        refresh_token = reddit.auth.authorize(code)
        print(f"Refresh Token: {refresh_token}")
        reddit.config.refresh_token = refresh_token
    except Exception as e:
        raise RuntimeError(f"Error obtaining refresh token: {e}")

    return reddit

def search_subreddits(reddit: praw.Reddit, keywords: List[str]) -> List[str]:
    """
    Search Reddit for subreddits matching the given keywords.

    :param reddit: Initialized Reddit instance.
    :param keywords: List of keywords to search for.
    :return: List of matching subreddits.
    """
    subreddits = set()

    for keyword in keywords:
        results = reddit.subreddits.search(keyword, limit=5)
        for result in results:
            subreddits.add(result.display_name)

    return list(subreddits)

def search_posts(reddit: praw.Reddit, keywords: List[str], limit: int = 100
) -> List[praw.models.Submission]:
    """
    Search Reddit for posts matching the given keywords.

    :param reddit: Initialized Reddit instance.
    :param keywords: List of keywords to search for.
    :param limit: Maximum number of posts to return.
    :return: List of matching Reddit submissions.
    """
    posts = []
    for keyword in keywords:
        for submission in reddit.subreddit('all').search(keyword, limit=limit):
            posts.append(submission)
    return posts
