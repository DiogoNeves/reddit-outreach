import hashlib
import os
import pickle
from typing import Callable, Any, Coroutine, Optional
from functools import wraps

# Constants
CACHE_DIR = "cache"

def get_video_hash(video_url: str) -> str:
    """Generate a unique hash for the video URL."""
    return hashlib.md5(video_url.encode()).hexdigest()

def cache_result(step: str):
    """
    Decorator to cache the result of a function.

    :param step: The step name to use for the cache key.
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            video_hash = kwargs.get("video_hash")
            if not video_hash:
                raise ValueError("Missing 'video_hash' argument")

            # Create directory for the video hash
            video_cache_dir = os.path.join(CACHE_DIR, video_hash)
            os.makedirs(video_cache_dir, exist_ok=True)

            cache_key = f"{step}.pkl"
            cache_path = os.path.join(video_cache_dir, cache_key)

            if os.path.exists(cache_path):
                with open(cache_path, "rb") as file:
                    return pickle.load(file)

            result = await func(*args, **kwargs)

            with open(cache_path, "wb") as file:
                pickle.dump(result, file)

            return result

        return wrapper

    return decorator
