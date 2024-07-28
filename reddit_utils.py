import praw
import webbrowser
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
