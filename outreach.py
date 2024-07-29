"""Starting point of the application."""

import argparse
import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from video_utils import extract_video_details
from reddit_search import get_reddit_instance, search_subreddits, search_posts
from post_analysis import analyze_posts, generate_engagement_content
from keyword_extractor import get_relevant_keywords, filter_subreddits

# Constants
COMMENT_THRESHOLD = 10
TIME_THRESHOLD = 3  # in months

# Load environment variables from .env file at the start of the script
load_dotenv()

def filter_posts(posts):
    """
    Filter posts based on comment count and age.

    :param posts: List of Reddit submissions to filter.
    :return: List of filtered Reddit submissions.
    """
    now = datetime.utcnow()
    threshold_date = now - timedelta(days=TIME_THRESHOLD * 30)
    filtered_posts = [
        post for post in posts
        if post.num_comments <= COMMENT_THRESHOLD and datetime.utcfromtimestamp(post.created_utc) > threshold_date
    ]
    return filtered_posts

async def main(video_url: str) -> None:
    """
    Main function to extract video details and initialize Reddit.

    :param video_url: URL of the YouTube video.
    """
    # Extract video details
    video_title, video_description = extract_video_details(video_url)
    print(f"Video Title: {video_title}")
    print(f"Video Description: {video_description}")

    # Get relevant keywords
    keywords = await get_relevant_keywords(video_title, video_description)

    if not keywords:
        print("Error: Unable to extract keywords.")
        return

    print(f"Suggested Keywords: {keywords}")

    # Initialize Reddit
    try:
        reddit = await get_reddit_instance()
        print("Reddit initialized successfully.")
    except RuntimeError as e:
        print(f"Error initializing Reddit: {e}")
        return

    # Search for subreddits based on keywords
    subreddits = await search_subreddits(reddit, keywords)

    if not subreddits:
        print("Error: Unable to find matching subreddits.")
        return

    print(f"Suggested Subreddits before filtering: {subreddits}")

    # Filter subreddits to keep only relevant ones
    relevant_subreddits = await filter_subreddits(
        video_title, video_description, subreddits)

    if not relevant_subreddits:
        print("Error: Unable to find relevant subreddits.")
        return

    print(f"Suggested Subreddits after filtering: {relevant_subreddits}")

    # Search for posts based on keywords
    posts = await search_posts(reddit, keywords)

    if not posts:
        print("Error: Unable to find matching posts.")
        return

    # Filter out posts with more than COMMENT_THRESHOLD comments and older than TIME_THRESHOLD months
    posts = filter_posts(posts)

    if not posts:
        print("Error: No posts matching the criteria found.")
        return

    print(f"Found {len(posts)} posts matching the criteria. Analyzing relevance...")

    # Analyze posts for relevance
    relevant_posts = await analyze_posts(posts, video_title, video_description)

    if not relevant_posts:
        print("Error: No relevant posts found.")
        return

    print(f"Found {len(relevant_posts)} relevant posts. Generating comments...")

    # Generate engagement content
    comments = await generate_engagement_content(video_url, video_title, relevant_posts)

    for post, comment in zip(relevant_posts, comments):
        print(f"Post Title: {post.title}")
        print(f"Generated Comment: {comment}")
        print(f"Post URL: {post.url}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract video details and initialize Reddit.")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video")

    args = parser.parse_args()
    asyncio.run(main(args.video_url))
