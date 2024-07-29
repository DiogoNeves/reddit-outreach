"""Utilities for interacting with the LLMs.
Currently only supports OpenAI's models."""

import os
import json
import re
from typing import Optional, List, Dict, Union
from openai import OpenAI

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def request_completion(prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Request completion from OpenAI API.

    :param prompt: The user prompt to send to the OpenAI API.
    :param system_prompt: An optional system prompt to set the context.
    :return: The completion result from the OpenAI API.
    """
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    if not completion.choices or not completion.choices[0].message.content:
        return ""

    return completion.choices[0].message.content

def extract_json_from_string(text: str) -> Union[Dict, List]:
    """
    Extract the first valid JSON object from a string.

    :param text: The input string containing JSON.
    :return: The extracted JSON object (dict or list).
    :raises ValueError: If no valid JSON object is found.
    """
    json_pattern = re.compile(r'{.*?}|[.*?]', re.DOTALL)
    matches = json_pattern.findall(text)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    raise ValueError("No valid JSON object found in the input text.")
