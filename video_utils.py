import yt_dlp
from typing import Tuple

def extract_video_details(video_url: str) -> Tuple[str, str]:
    """
    Extract and return the title and description of a YouTube video using yt-dlp.

    :param video_url: URL of the YouTube video.
    :return: A tuple containing the video title and description.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "simulate": True,  # Do not download the video
        "skip_download": True,  # Skip downloading the video
        "force_generic_extractor": True,  # Try to use the generic extractor for speed
        "extract_flat": True,  # Do not extract additional information about formats
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        title = info.get("title") if info else None
        description = info.get("description") if info else None

    title = title or "Title not available"
    description = description or "Description not available"

    return title, description
