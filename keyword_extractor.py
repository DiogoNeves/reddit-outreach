"""
This module provides functionality to extract relevant keywords from
a YouTube video title and description using an LLM.
"""

from typing import List
from llm_utils import request_completion, extract_json_from_string

def escape_line_breaks(text: str) -> str:
    """
    Escape line breaks in the given text for XML compatibility.

    :param text: The input text.
    :return: The text with line breaks escaped.
    """
    return text.replace("\n", "&#10;")

async def get_relevant_keywords(
    video_title: str, video_description: str) -> List[str]:
    """
    Generate and return a list of relevant keywords based on
    the video title and description.

    :param video_title: Title of the video.
    :param video_description: Description of the video.
    :return: A list of keywords.
    :raises ValueError: If the output cannot be processed.
    """
    escaped_description = escape_line_breaks(video_description)

    prompt = (f"Based on the following video title and description, suggest "
              f"relevant keywords to find related posts.\n\n"
              f"Title: {video_title}\n"
              f"<description>{escaped_description}</description>\n\n"
              f"Output in this JSON format:\n"
              f"{{\n"
              f"  \"keywords\": [\"keyword1\", \"keyword2\", ...]\n"
              f"}}")

    result = await request_completion(prompt,
        ("You are an assistant skilled in identifying relevant keywords."
         " Please output the result in the specified JSON format."))

    try:
        result_json = extract_json_from_string(result)
        keywords = result_json.get("keywords", [])
    except ValueError as e:
        raise ValueError("Error processing the LLM output as JSON") from e

    return keywords

async def filter_subreddits(video_title: str, video_description: str,
                            subreddits: List[str]) -> List[str]:
    """
    Filter the subreddits to keep only the relevant ones using the LLM.

    :param video_title: Title of the video.
    :param video_description: Description of the video.
    :param subreddits: List of subreddits to filter.
    :return: List of relevant subreddits.
    """
    escaped_description = escape_line_breaks(video_description)

    prompt = (f"Based on the following video title and description, "
              f"keep only the relevant subreddits from the list, and"
              f" suggest any additional related subreddits if you are"
              f" entirely sure they exist.\n\nTitle: {video_title}\n"
              f"<description>{escaped_description}</description>\n\n"
              f"Subreddits:\n{', '.join(subreddits)}\n\n"
              f"Output the relevant subreddits in a JSON format, and add any "
              f"additional related subreddits if applicable:\n"
              f"{{\"relevant_subreddits\": [\"subreddit1\", \"subreddit2\","
              f" ...], \"additional_subreddits\": [\"subreddit3\","
              f" \"subreddit4\", ...]}}")

    result = await request_completion(prompt,
        ("You are an assistant skilled in identifying relevant subreddits."
         " Please output the result in the specified JSON format."))

    try:
        result_json = extract_json_from_string(result)
        relevant_subreddits = result_json.get("relevant_subreddits", [])
        additional_subreddits = result_json.get("additional_subreddits", [])
    except ValueError as e:
        raise ValueError("Error processing the LLM output as JSON") from e

    return list(set(relevant_subreddits + additional_subreddits))
