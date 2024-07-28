import praw
import webbrowser

def init_reddit(client_id: str, client_secret: str, user_agent: str,
                redirect_uri: str) -> praw.Reddit:
    """
    Initialize and return a Reddit instance using OAuth2.

    :param client_id: Reddit API client ID.
    :param client_secret: Reddit API client secret.
    :param user_agent: Reddit API user agent.
    :param redirect_uri: Redirect URI for OAuth2.
    :return: Initialized Reddit instance.
    """
    print("Initializing Reddit with the following parameters:")
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")
    print(f"User Agent: {user_agent}")
    print(f"Redirect URI: {redirect_uri}")

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         redirect_uri=redirect_uri)

    # Obtain the URL for user authentication
    auth_url = reddit.auth.url(['*'], 'secrethorseshoe', 'permanent')
    print(f"Please go to this URL and authorize the application: {auth_url}")

    # Open the URL in the web browser for the user to authenticate
    webbrowser.open(auth_url)

    # Ask the user to enter the URL they were redirected to
    redirected_url = input("Enter the full URL you were redirected to: ")
    print(f"Redirected URL: {redirected_url}")

    # Parse the code from the redirected URL
    code = redirected_url.split("code=")[-1]
    print(f"Authorization Code: {code}")

    # Obtain the refresh token
    try:
        refresh_token = reddit.auth.authorize(code)
        print(f"Refresh Token: {refresh_token}")
        reddit.config.refresh_token = refresh_token
    except Exception as e:
        print(f"Error obtaining refresh token: {e}")

    return reddit
