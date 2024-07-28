# outreach.py
import argparse
from video_utils import extract_video_details

def main(video_url: str) -> None:
    """
    Main function to extract and print video details.

    :param video_url: URL of the YouTube video.
    """
    # Extract video details
    video_title, video_description = extract_video_details(video_url)

    # Print the video details
    print(f"Video Title: {video_title}")
    print(f"Video Description: {video_description}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and print details of a YouTube video.')
    parser.add_argument('video_url', type=str, help='URL of the YouTube video')

    args = parser.parse_args()
    main(args.video_url)
