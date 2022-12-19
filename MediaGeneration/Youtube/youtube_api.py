import requests
import random
from decouple import config
from logger import Logger

def generate_youtube_api_url(params: list) -> str:
    """
    Creates a Youtube API URL.
    :param params: The Search Parameters.
    :return: The Youtube API Url.
    """
    Logger.info(f"Entering {generate_youtube_api_url.__name__}")

    return f"https://www.googleapis.com/youtube/v3/search?q={['%20'.join(param for param in params)]}t&maxResults=50" \
           f"&key={config('YOUTUBE_API_KEY')}"


def get_random_yt_video() -> str:
    """
    Gets a random Youtube video from the API Response.
    :return: A random Youtube video from the API Response.
    """
    Logger.info(f"Entering {get_random_yt_video.__name__}")

    try: 
        youtube_video_list = requests.get(generate_youtube_api_url(["smash", "ultimate", "sick", "combos"])).json()
    except:
        Logger.critical("Could not retrieve response from Youtube API; returning...")

    Logger.info(f"Successfully retrieved response from Youtube API; Formatting...")

    first_video_id = youtube_video_list["items"][random.randint(0, len(youtube_video_list))]["id"]["videoId"]
    video_link = f"https://www.youtube.com/watch?v={first_video_id}"

    Logger.info(f"Formatted API response into a link for download.")

    return video_link

def upload_video_to_youtube(video_path: str) -> None:
    """
    Uploads a generated video to Youtube.
    :param: video_path The path to the generated youtube video.
    """
