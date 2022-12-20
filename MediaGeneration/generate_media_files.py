from MediaGeneration.Reddit.reddit_api import Post, RedditApi
from MediaGeneration.TTS.pyttsx3 import pyttsx3_text_to_speech
from MediaGeneration.TTS.voice_recorder import get_image_prompts_and_record_audio
from MediaGeneration.Youtube.youtube_downloader import store_youtube_video

def generate_and_save_media_files(subreddit: str) -> Post:
    """
    Manual step to create all of the necessary content for a video.
    :param subreddit: The subreddit to search for the content of.
    """
    ask_reddit_link = RedditApi(subreddit=subreddit)
    ask_reddit_link.store_images_of_title_and_top_three_comments()
    get_image_prompts_and_record_audio()
    # store_youtube_video()
    # pyttsx3_text_to_speech([ask_reddit_link.post_info.title])
    # pyttsx3_text_to_speech([comment.body for comment in ask_reddit_link.post_info.comments])
    return ask_reddit_link.post_info
