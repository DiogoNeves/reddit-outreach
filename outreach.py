"""Starting point of the application."""

import argparse
import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from video_utils import extract_video_details
from reddit_search import get_reddit_instance, search_posts, RedditPost
from post_analysis import analyze_posts, generate_engagement_content
from keyword_extractor import get_relevant_keywords
from cache_utils import get_video_hash, cache_result
from csv_utils import save_posts_to_csv

# Constants
COMMENT_THRESHOLD = 10
TIME_THRESHOLD_IN_MONTHS = 3  # in months
SECTION_SEPARATOR = "=" * 20
POST_SEPARATOR = "-" * 20

# Load environment variables from .env file at the start of the script
load_dotenv()

def filter_posts(posts: list[RedditPost]) -> list[RedditPost]:
    """
    Filter posts based on comment count and age.

    :param posts: list of Reddit submissions to filter.
    :return: list of filtered Reddit submissions.
    """
    now = datetime.utcnow()
    threshold_date = now - timedelta(days=TIME_THRESHOLD_IN_MONTHS * 30)
    filtered_posts = [
        post for post in posts
        if post.num_comments <= COMMENT_THRESHOLD and \
            datetime.utcfromtimestamp(post.created_utc) > threshold_date
    ]
    return filtered_posts

@cache_result("video_details")
async def get_video_details(video_url: str, video_hash: str) -> tuple:
    """Extract video details and save to cache if not already cached."""
    title, description = extract_video_details(video_url)
    return title, description

@cache_result("keywords")
async def get_keywords(video_title: str, video_description: str, video_hash: str) -> list:
    """Get relevant keywords and save to cache if not already cached."""
    return await get_relevant_keywords(video_title, video_description)

@cache_result("filtered_posts")
async def get_reddit_posts(reddit, keywords: list, video_hash: str) -> list[RedditPost]:
    """Search for Reddit posts and save to cache if not already cached."""
    posts = await search_posts(reddit, keywords)
    return filter_posts(posts)

@cache_result("relevant_posts")
async def analyze_reddit_posts(posts: list[RedditPost], video_title: str, video_description: str, video_hash: str) -> list:
    """Analyze Reddit posts for relevance and save to cache if not already cached."""
    return await analyze_posts(posts, video_title, video_description)

async def main(video_url: str) -> None:
    """
    Main function to extract video details and initialize Reddit.

    :param video_url: URL of the YouTube video.
    """
    # Generate video hash
    video_hash = get_video_hash(video_url)

    # Extract video details
    video_title, video_description = await get_video_details(video_url=video_url, video_hash=video_hash)
    print(f"\n{SECTION_SEPARATOR}\n📹 Video Title: {video_title}\n{SECTION_SEPARATOR}")
    print(f"\n📄 Video Description:\n{video_description}\n{SECTION_SEPARATOR}")

    # Get relevant keywords
    keywords = await get_keywords(video_title=video_title, video_description=video_description, video_hash=video_hash)

    if not keywords:
        print("Error: Unable to extract keywords.")
        return

    print(f"🔑 Suggested Keywords:\n{' - '.join(keywords)}\n{SECTION_SEPARATOR}")

    # Initialize Reddit
    reddit = None
    try:
        reddit = await get_reddit_instance()
        print(f"🚀 Reddit initialized successfully.\n{SECTION_SEPARATOR}")

        # Search for posts based on keywords
        posts = await get_reddit_posts(reddit=reddit, keywords=keywords, video_hash=video_hash)

        if not posts:
            print("Error: Unable to find matching posts.")
            return

        print(f"🔍 Found {len(posts)} posts matching the criteria. Analyzing relevance...\n{SECTION_SEPARATOR}")

        # Analyze posts for relevance
        relevant_posts = await analyze_reddit_posts(posts=posts, video_title=video_title, video_description=video_description, video_hash=video_hash)

        if not relevant_posts:
            print("Error: No relevant posts found.")
            return

        print(f"✔️ Found {len(relevant_posts)} relevant posts. Generating comments...\n{SECTION_SEPARATOR}")

        # Generate engagement content
        comments = await generate_engagement_content(video_url, video_title, relevant_posts)

        for post, comment in zip(relevant_posts, comments):
            print(f"📝 Post Title: {post.title}")
            print(f"💬 Generated Comment: {comment}")
            print(f"🔗 Post URL: {post.url}\n{POST_SEPARATOR}")

        # Save to CSV
        csv_path = save_posts_to_csv(relevant_posts, comments, f"{video_hash}_relevant_posts.csv")
        print(f"📁 Relevant posts and comments have been saved to {csv_path}")
    except RuntimeError as e:
        print(f"Error initializing Reddit: {e}")
    finally:
        if reddit is not None:
            await reddit.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract video details and initialize Reddit.")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video")

    args = parser.parse_args()
    asyncio.run(main(args.video_url))
