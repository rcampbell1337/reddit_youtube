import requests
import random
from decouple import config


def generate_youtube_api_url(params: list) -> str:
    return f"https://www.googleapis.com/youtube/v3/search?q={['%20'.join(param for param in params)]}t&maxResults=25" \
           f"&key={config('YOUTUBE_API_KEY')}"


def get_first_yt_video():
    youtube_video_list = requests.get(generate_youtube_api_url(["gta", "4", "background"])).json()
    first_video_id = youtube_video_list["items"][random.randint(0, len(youtube_video_list))]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={first_video_id}"