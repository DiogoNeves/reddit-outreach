"""Utility functions for handling CSV operations."""

import os
import csv
from reddit_search import RedditPost

def save_posts_to_csv(posts: list[RedditPost], comments: list[str], filename: str) -> str:
    """
    Save the relevant posts and generated comments to a CSV file.

    :param posts: List of relevant Reddit submissions.
    :param comments: List of generated comments.
    :param filename: The filename of the CSV file.
    :return: The path to the saved CSV file.
    """
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Post Title", "Post URL", "Generated Comment"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for post, comment in zip(posts, comments):
            writer.writerow({
                "Post Title": post.title,
                "Post URL": post.url,
                "Generated Comment": comment
            })

    return filepath
