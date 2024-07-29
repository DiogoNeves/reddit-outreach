"""Starting point of the application."""

import argparse
import os
from dotenv import load_dotenv
from video_utils import extract_video_details
from reddit_search import init_reddit, search_subreddits, search_posts
from reddit_search import analyze_posts, generate_engagement_content
from keyword_extractor import get_relevant_keywords, filter_subreddits

# Load environment variables from .env file at the start of the script
load_dotenv()

def get_reddit_instance() -> 'praw.Reddit':
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

    return init_reddit(client_id, client_secret, user_agent, redirect_uri)

def main(video_url: str) -> None:
    """
    Main function to extract video details and initialize Reddit.

    :param video_url: URL of the YouTube video.
    """
    # Extract video details
    video_title, video_description = extract_video_details(video_url)
    print(f"Video Title: {video_title}")
    print(f"Video Description: {video_description}")

    # Get relevant keywords
    keywords = get_relevant_keywords(video_title, video_description)

    if not keywords:
        print("Error: Unable to extract keywords.")
        return

    print(f"Suggested Keywords: {keywords}")

    # Initialize Reddit
    try:
        reddit = get_reddit_instance()
        print("Reddit initialized successfully.")
    except RuntimeError as e:
        print(f"Error initializing Reddit: {e}")
        return

    # Search for subreddits based on keywords
    subreddits = search_subreddits(reddit, keywords)

    if not subreddits:
        print("Error: Unable to find matching subreddits.")
        return

    print(f"Suggested Subreddits before filtering: {subreddits}")

    # Filter subreddits to keep only relevant ones
    relevant_subreddits = filter_subreddits(
        video_title, video_description, subreddits)

    if not relevant_subreddits:
        print("Error: Unable to find relevant subreddits.")
        return

    print(f"Suggested Subreddits after filtering: {relevant_subreddits}")

    # Search for posts based on keywords
    posts = search_posts(reddit, keywords)

    if not posts:
        print("Error: Unable to find matching posts.")
        return

    print(f"Found {len(posts)} posts. Analyzing relevance...")

    # Analyze posts for relevance
    relevant_posts = analyze_posts(posts, video_title, video_description)

    if not relevant_posts:
        print("Error: No relevant posts found.")
        return

    print(f"Found {len(relevant_posts)} relevant posts. Generating comments...")

    # Generate engagement content
    comments = generate_engagement_content(video_url, video_title, relevant_posts)

    for post, comment in zip(relevant_posts, comments):
        print(f"Post Title: {post.title}")
        print(f"Generated Comment: {comment}")
        print(f"Post URL: {post.url}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract video details and initialize Reddit.")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video")

    args = parser.parse_args()
    main(args.video_url)
