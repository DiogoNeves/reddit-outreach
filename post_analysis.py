"""
Functions for analyzing Reddit posts and generating engagement content.
"""

import asyncio
from typing import List
from asyncpraw.models import Submission
from llm_utils import request_completion

async def analyze_posts(posts: List[Submission], video_title: str,
                        video_description: str, max_concurrency: int = 10
) -> List[Submission]:
    """
    Analyze Reddit posts to determine relevance based on video content.

    :param posts: List of Reddit submissions to analyze.
    :param video_title: Title of the video.
    :param video_description: Description of the video.
    :param max_concurrency: Maximum number of concurrent requests.
    :return: List of relevant Reddit submissions.
    """
    semaphore = asyncio.Semaphore(max_concurrency)
    relevant_posts = []

    async def analyze_post(post):
        async with semaphore:
            prompt = (f"Given the video title '{video_title}' and description"
                      f" '{video_description}', analyze the following Reddit post"
                      f" and determine if the video would be relevant to the"
                      f" discussion.\n\nPost Title: {post.title}\nPost Content:"
                      f" {post.selftext}\n\nRespond with 'relevant' or"
                      f" 'not relevant'.")
            result = await request_completion(prompt)
            if 'relevant' in result.lower():
                relevant_posts.append(post)

    await asyncio.gather(*[analyze_post(post) for post in posts])
    return relevant_posts

async def generate_engagement_content(video_url: str, video_title: str,
                                      posts: List[Submission],
                                      max_concurrency: int = 10) -> List[str]:
    """
    Generate engagement content for relevant Reddit posts.

    :param video_url: URL of the YouTube video.
    :param video_title: Title of the video.
    :param posts: List of relevant Reddit submissions.
    :param max_concurrency: Maximum number of concurrent requests.
    :return: List of generated engagement comments.
    """
    semaphore = asyncio.Semaphore(max_concurrency)
    comments = []

    async def generate_comment(post):
        async with semaphore:
            prompt = (f"Given the video title '{video_title}' and the following"
                      f" Reddit post, generate a helpful and non-spammy comment"
                      f" that includes a link to the video.\n\nPost Title:"
                      f" {post.title}\nPost Content: {post.selftext}\n\n"
                      f"Video URL: {video_url}")
            comment = await request_completion(prompt)
            comments.append(comment)

    await asyncio.gather(*[generate_comment(post) for post in posts])
    return comments
