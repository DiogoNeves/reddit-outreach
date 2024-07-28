"""Utilities for interacting with the LLMs.
Currently only supports OpenAI's models."""

import os
from typing import Optional, List, Dict
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
