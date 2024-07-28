import yt_dlp
from typing import Tuple

def extract_video_details(video_url: str) -> Tuple[str, str]:
    """
    Extract the title and description of a YouTube video.

    :param video_url: URL of the YouTube video.
    :return: A tuple containing the video title and description.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        # Do not download the video
        "simulate": True,
        # Skip downloading the video
        "skip_download": True,
        # Try to use the generic extractor for speed
        "force_generic_extractor": True,
        # Do not extract additional information about formats
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        title = info.get("title") if info else None
        description = info.get("description") if info else None

    title = title or "Title not available"
    description = description or "Description not available"

    return title, description
