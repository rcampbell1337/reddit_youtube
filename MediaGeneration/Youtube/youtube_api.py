import requests
import random
from decouple import config


def generate_youtube_api_url(params: list) -> str:
    """
    Creates a Youtube API URL.
    :param params: The Search Parameters.
    :return: The Youtube API Url.
    """
    return f"https://www.googleapis.com/youtube/v3/search?q={['%20'.join(param for param in params)]}t&maxResults=25" \
           f"&key={config('YOUTUBE_API_KEY')}"


def get_random_yt_video() -> str:
    """
    Gets a random Youtube video from the API Response.
    :return: A random Youtube video from the API Response.
    """
    youtube_video_list = requests.get(generate_youtube_api_url(["minecraft", "background"])).json()
    first_video_id = youtube_video_list["items"][random.randint(0, len(youtube_video_list))]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={first_video_id}"
