"""
This module provides functionality to extract relevant keywords from
a YouTube video title and description using an LLM.
"""

from typing import List
from llm_utils import request_completion
import json

def escape_line_breaks(text: str) -> str:
    """
    Escape line breaks in the given text for XML compatibility.

    :param text: The input text.
    :return: The text with line breaks escaped.
    """
    return text.replace("\n", "&#10;")

def get_relevant_keywords(
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

    result = request_completion(prompt,
        ("You are an assistant skilled in identifying relevant keywords."
         " Please output the result in the specified JSON format."))

    try:
        result_json = json.loads(result)
        keywords = result_json.get("keywords", [])
    except json.JSONDecodeError as e:
        raise ValueError("Error processing the LLM output as JSON") from e

    return keywords
