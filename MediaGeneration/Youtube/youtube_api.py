import os
from typing import List
import requests
import random
from decouple import config
from logger import Logger
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

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

def upload_video_to_youtube(video_path: str, title: str, tags: List[str]) -> None:
    """
    Uploads a generated video to Youtube.
    :param: video_path The path to the generated Youtube video.
    :param: title The title of the video.
    :param: tags The tags of the video.
    """
    Logger.info(f"Entering {upload_video_to_youtube.__name__}")

    # loggin into the channel
    channel = Channel()
    channel.login(os.path.abspath(os.path.join(os.path.dirname(__file__), "Secrets/client-secrets.json")), 
                  os.path.abspath(os.path.join(os.path.dirname(__file__), "Secrets/credentials.storage")))

    Logger.info("Collected credentials, adding all metadata...")

    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=video_path)

    # setting snippet
    video.set_title(title)
    video.set_description(f"What do you think? {', '.join([f'#{tag}' for tag in tags])}")
    video.set_tags(tags)
    video.set_category("gaming")
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status("public")
    video.set_public_stats_viewable(True)

    Logger.info("Uploading video to youtube...")

    # uploading video and printing the results
    uploaded_video = channel.upload_video(video)

    Logger.info(f"Uploaded video with ID: https://youtube.com/watch?v={uploaded_video.id}")

    # liking video
    video.like()
