"""Starting point of the application."""

import argparse
import os
from dotenv import load_dotenv
from video_utils import extract_video_details
from reddit_utils import init_reddit

# Load environment variables from .env file
load_dotenv()

def main(video_url: str) -> None:
    """
    Main function to extract video details and initialize Reddit.

    :param video_url: URL of the YouTube video.
    """
    # Extract video details
    video_title, video_description = extract_video_details(video_url)
    print(f"Video Title: {video_title}")
    print(f"Video Description: {video_description}")

    # Read Reddit API credentials from environment variables
    client_id = os.getenv("REDDIT_CLIENT_ID") or ""
    client_secret = os.getenv("REDDIT_CLIENT_SECRET") or ""
    user_agent = os.getenv("REDDIT_USER_AGENT") or ""
    redirect_uri = os.getenv("REDDIT_REDIRECT_URI") or ""

    if not all([client_id, client_secret, user_agent, redirect_uri]):
        print("Error: Missing one or more environment variables"
              " (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,"
              " REDDIT_REDIRECT_URI).")
        return

    # Initialize Reddit
    reddit = init_reddit(client_id, client_secret, user_agent, redirect_uri)
    if reddit is None:
        print("Error initializing Reddit.")
        return

    print("Reddit initialized successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract video details and initialize Reddit.")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video")

    args = parser.parse_args()
    main(args.video_url)
