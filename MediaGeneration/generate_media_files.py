from MediaGeneration.Reddit.reddit_api import RedditApi
from MediaGeneration.TTS.pyttsx3 import pyttsx3_text_to_speech
from MediaGeneration.Youtube.youtube_downloader import store_youtube_video


def generate_and_save_media_files(subreddit: str):
    ask_reddit_link = RedditApi(subreddit=subreddit)
    ask_reddit_link.store_images_of_title_and_top_three_comments()
    store_youtube_video()
    pyttsx3_text_to_speech([ask_reddit_link.post_info.title])
    pyttsx3_text_to_speech([comment.body for comment in ask_reddit_link.post_info.comments])
