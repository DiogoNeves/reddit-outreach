"""
Utility functions to interact with Reddit, including initialization,
subreddit search, and post search.
"""

import asyncpraw
import asyncpraw.models
import webbrowser
from typing import List
from oauth_server import get_auth_code_from_server
from llm_utils import request_completion, extract_json_from_string
import os

async def get_reddit_instance() -> 'asyncpraw.Reddit':
    """
    Load Reddit API credentials from environment variables and initialize
    Reddit instance.

    :return: Initialized Reddit instance.
    :raises RuntimeError: If any required environment variables are missing.
    """
    client_id = os.getenv("REDDIT_CLIENT_ID") or ""
    client_secret = os.getenv("REDDIT_CLIENT_SECRET") or ""
    user_agent = os.getenv("REDDIT_USER_AGENT") or ""
    redirect_uri = os.getenv("REDDIT_REDIRECT_URI") or ""

    if not all([client_id, client_secret, user_agent, redirect_uri]):
        raise RuntimeError(
            "Error: Missing one or more environment variables"
            " (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,"
            " REDDIT_REDIRECT_URI)."
        )

    return await _init_reddit(client_id, client_secret, user_agent, redirect_uri)

async def _init_reddit(client_id: str, client_secret: str, user_agent: str,
                      redirect_uri: str) -> asyncpraw.Reddit:
    """
    Initialize and return an Async PRAW instance using OAuth2.

    :param client_id: Reddit API client ID.
    :param client_secret: Reddit API client secret.
    :param user_agent: Reddit API user agent.
    :param redirect_uri: Redirect URI for OAuth2.
    :return: Initialized Async PRAW instance.
    :raises: RuntimeError if there is an error during authentication.
    """
    print("Initializing Reddit with the following parameters:")

    reddit = asyncpraw.Reddit(client_id=client_id,
                              client_secret=client_secret,
                              user_agent=user_agent,
                              redirect_uri=redirect_uri)

    # Obtain the URL for user authentication
    auth_url = reddit.auth.url(['*'], 'secrethorseshoe', 'permanent')
    print(f"Please go to this URL and authorize the application: {auth_url}")

    # Open the URL in the web browser for the user to authenticate
    webbrowser.open(auth_url)

    # Start the async HTTP server and wait for the authorization code
    code = await get_auth_code_from_server()

    print(f"Authorization Code: {code}")

    # Obtain the refresh token
    try:
        refresh_token = await reddit.auth.authorize(code)
        print(f"Refresh Token: {refresh_token}")
        reddit.config.refresh_token = refresh_token
    except Exception as e:
        raise RuntimeError(f"Error obtaining refresh token: {e}")

    return reddit

async def search_subreddits(reddit: asyncpraw.Reddit, keywords: List[str]) -> List[str]:
    """
    Search Reddit for subreddits matching the given keywords.

    :param reddit: Initialized Async PRAW instance.
    :param keywords: List of keywords to search for.
    :return: List of matching subreddits.
    """
    subreddits = set()

    for keyword in keywords:
        async for result in reddit.subreddits.search(keyword, limit=5):
            subreddits.add(result.display_name)

    return list(subreddits)

async def search_posts(reddit: asyncpraw.Reddit, keywords: List[str], limit: int = 100
) -> List[asyncpraw.models.Submission]:
    """
    Search Reddit for posts matching the given keywords.

    :param reddit: Initialized Async PRAW instance.
    :param keywords: List of keywords to search for.
    :param limit: Maximum number of posts to return.
    :return: List of matching Reddit submissions.
    """
    posts = []
    for keyword in keywords:
        async for submission in reddit.subreddit('all').search(keyword, limit=limit):
            posts.append(submission)
    return posts
